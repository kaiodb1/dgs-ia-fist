import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "..", "..", "..", "..");
const configPath = path.join(repoRoot, ".mcp", "mcp.json");
const outputJsonPath = path.join(scriptDir, "mcp-evidence.json");
const outputMarkdownPath = path.join(scriptDir, "mcp-evidence.md");
const config = JSON.parse(await readFile(configPath, "utf8"));

const corpusQuestion = "Qual o multiplicador para o Sudeste?";
const corpusChunkMarker = "Chunk PROC-042v2-B";
const docsFilePath = path.join(
  repoRoot,
  "docs",
  "novatech",
  "POL-001-politica-devolucao.md",
);
const corpusFilePath = path.join(
  repoRoot,
  "data",
  "retrieval-corpus",
  "chunks-novatech.md",
);

function clip(value, maxLength = 1200) {
  if (typeof value !== "string") {
    return value;
  }

  if (value.length <= maxLength) {
    return value;
  }

  return `${value.slice(0, maxLength)}\n...[truncated]`;
}

function firstTextContent(toolResult) {
  if (!Array.isArray(toolResult?.content)) {
    return "";
  }

  const textBlock = toolResult.content.find((block) => block.type === "text");

  return textBlock?.text ?? "";
}

function findTool(tools, names) {
  for (const name of names) {
    const exactMatch = tools.find((tool) => tool.name === name);

    if (exactMatch) {
      return exactMatch;
    }
  }

  const lowered = names.map((name) => name.toLowerCase());

  return tools.find((tool) =>
    lowered.some((name) => tool.name.toLowerCase().includes(name)),
  );
}

function buildFallbackArgs(tool) {
  const fallbackArgs = {};
  const properties = tool?.inputSchema?.properties ?? {};
  const required = tool?.inputSchema?.required ?? [];

  for (const name of required) {
    const lower = String(name).toLowerCase();

    if (lower.includes("path") || lower.includes("file")) {
      fallbackArgs[name] = ".";
      continue;
    }

    if (lower.includes("repo")) {
      fallbackArgs[name] = repoRoot;
      continue;
    }

    if (
      lower.includes("limit") ||
      lower.includes("count") ||
      lower.includes("max") ||
      lower === "n"
    ) {
      fallbackArgs[name] = 3;
      continue;
    }

    if (
      lower.includes("ref") ||
      lower.includes("rev") ||
      lower.includes("commit") ||
      lower.includes("branch")
    ) {
      fallbackArgs[name] = "HEAD";
      continue;
    }

    if (properties[name]?.type === "boolean") {
      fallbackArgs[name] = false;
      continue;
    }

    fallbackArgs[name] = "";
  }

  return fallbackArgs;
}

async function safeRequest(operation) {
  try {
    return {
      ok: true,
      value: await operation(),
    };
  } catch (error) {
    return {
      ok: false,
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

async function callToolWithFallback(client, tool) {
  const firstAttempt = await client.callTool({ name: tool.name });

  if (!firstAttempt.isError) {
    return firstAttempt;
  }

  return client.callTool({
    name: tool.name,
    arguments: buildFallbackArgs(tool),
  });
}

function extractChunkSection(markdown, marker) {
  const markerIndex = markdown.indexOf(marker);

  if (markerIndex === -1) {
    return "";
  }

  const remaining = markdown.slice(markerIndex);
  const nextHeadingIndex = remaining.indexOf("\n**Chunk ", marker.length);

  if (nextHeadingIndex === -1) {
    return remaining.trim();
  }

  return remaining.slice(0, nextHeadingIndex).trim();
}

async function connectServer(name) {
  const serverConfig = config.mcpServers[name];

  if (!serverConfig) {
    throw new Error(`Missing server config for ${name}`);
  }

  const stderrChunks = [];
  const transport = new StdioClientTransport({
    command: serverConfig.command,
    args: serverConfig.args,
    cwd: repoRoot,
    env: {
      ...process.env,
      ...(serverConfig.env ?? {}),
    },
    stderr: "pipe",
  });

  if (transport.stderr) {
    transport.stderr.on("data", (chunk) => {
      stderrChunks.push(chunk.toString("utf8"));
    });
  }

  const client = new Client({
    name: "copilot-cli-mcp-evidence",
    version: "1.0.0",
  });

  client.onerror = (error) => {
    stderrChunks.push(`CLIENT_ERROR ${error.message}\n`);
  };

  await client.connect(transport);

  return {
    client,
    transport,
    stderrChunks,
  };
}

async function runServer(name, handler) {
  const { client, transport, stderrChunks } = await connectServer(name);

  try {
    const tools = await safeRequest(() => client.listTools());
    const resources = await safeRequest(() => client.listResources());
    const prompts = await safeRequest(() => client.listPrompts());

    return await handler({
      client,
      tools,
      resources,
      prompts,
      stderr: stderrChunks.join("").trim(),
    });
  } finally {
    await transport.close();
  }
}

const results = {
  generatedAt: new Date().toISOString(),
  repoRoot,
  question: corpusQuestion,
  servers: {},
};

results.servers["filesystem-workspace"] = await runServer(
  "filesystem-workspace",
  async ({ client, tools, resources, prompts, stderr }) => ({
    toolNames: tools.ok ? tools.value.tools.map((tool) => tool.name) : [],
    resources,
    prompts,
    stderr,
    allowedDirectories: await safeRequest(() =>
      client.callTool({
        name: "list_allowed_directories",
        arguments: {},
      }),
    ),
  }),
);

results.servers["filesystem-docs"] = await runServer(
  "filesystem-docs",
  async ({ client, tools, resources, prompts, stderr }) => {
    const docRead = await safeRequest(() =>
      client.callTool({
        name: "read_text_file",
        arguments: { path: docsFilePath },
      }),
    );
    const directoryListing = await safeRequest(() =>
      client.callTool({
        name: "list_directory",
        arguments: { path: path.dirname(docsFilePath) },
      }),
    );

    return {
      toolNames: tools.ok ? tools.value.tools.map((tool) => tool.name) : [],
      resources,
      prompts,
      stderr,
      directoryListing,
      docRead,
      docExcerpt: docRead.ok ? clip(firstTextContent(docRead.value), 900) : "",
    };
  },
);

results.servers["filesystem-corpus"] = await runServer(
  "filesystem-corpus",
  async ({ client, tools, resources, prompts, stderr }) => {
    const corpusRead = await safeRequest(() =>
      client.callTool({
        name: "read_text_file",
        arguments: { path: corpusFilePath },
      }),
    );
    const corpusText = corpusRead.ok ? firstTextContent(corpusRead.value) : "";

    return {
      toolNames: tools.ok ? tools.value.tools.map((tool) => tool.name) : [],
      resources,
      prompts,
      stderr,
      corpusRead,
      domainQuestion: corpusQuestion,
      expectedChunkMarker: corpusChunkMarker,
      retrievedChunkExcerpt: clip(
        extractChunkSection(corpusText, corpusChunkMarker),
        900,
      ),
    };
  },
);

results.servers.git = await runServer(
  "git",
  async ({ client, tools, resources, prompts, stderr }) => {
    const toolList = tools.ok ? tools.value.tools : [];
    const statusTool = findTool(toolList, ["git_status", "status"]);
    const logTool = findTool(toolList, ["git_log", "log"]);

    const status =
      statusTool === undefined
        ? { ok: false, error: "No git status tool found." }
        : await safeRequest(() => callToolWithFallback(client, statusTool));

    const log =
      logTool === undefined
        ? { ok: false, error: "No git log tool found." }
        : await safeRequest(async () => {
            try {
              return await callToolWithFallback(client, logTool);
            } catch {
              return client.callTool({
                name: logTool.name,
                arguments: buildFallbackArgs(logTool),
              });
            }
          });

    return {
      toolNames: toolList.map((tool) => tool.name),
      resources,
      prompts,
      stderr,
      status,
      log,
      logExcerpt: log.ok ? clip(firstTextContent(log.value), 900) : "",
    };
  },
);

results.servers.memory = await runServer(
  "memory",
  async ({ tools, resources, prompts, stderr }) => ({
    toolNames: tools.ok ? tools.value.tools.map((tool) => tool.name) : [],
    resources,
    prompts,
    stderr,
  }),
);

results.servers.everything = await runServer(
  "everything",
  async ({ tools, resources, prompts, stderr }) => ({
    toolNames: tools.ok ? tools.value.tools.map((tool) => tool.name) : [],
    resourceUris: resources.ok ? resources.value.resources.map((resource) => resource.uri) : [],
    promptNames: prompts.ok ? prompts.value.prompts.map((prompt) => prompt.name) : [],
    stderr,
  }),
);

await mkdir(path.dirname(outputJsonPath), { recursive: true });

await writeFile(outputJsonPath, `${JSON.stringify(results, null, 2)}\n`, "utf8");

const markdown = `# Evidência MCP\n\n## Resumo\n\n- Data/hora: ${results.generatedAt}\n- Pergunta de domínio usada no corpus: ${results.question}\n\n## filesystem-workspace\n\n- Tools: ${results.servers["filesystem-workspace"].toolNames.join(", ")}\n- Allowed directories:\n\n\`\`\`json\n${JSON.stringify(results.servers["filesystem-workspace"].allowedDirectories, null, 2)}\n\`\`\`\n\n## filesystem-docs\n\n- Tools: ${results.servers["filesystem-docs"].toolNames.join(", ")}\n- Exemplo de leitura do documento oficial:\n\n\`\`\`\n${results.servers["filesystem-docs"].docExcerpt}\n\`\`\`\n\n## filesystem-corpus\n\n- Tools: ${results.servers["filesystem-corpus"].toolNames.join(", ")}\n- Chunk recuperado para a pergunta "${results.question}":\n\n\`\`\`\n${results.servers["filesystem-corpus"].retrievedChunkExcerpt}\n\`\`\`\n\n## git\n\n- Tools: ${results.servers.git.toolNames.join(", ")}\n- Exemplo de histórico/status:\n\n\`\`\`\n${results.servers.git.logExcerpt || JSON.stringify(results.servers.git.status, null, 2)}\n\`\`\`\n\n## memory\n\n- Tools: ${results.servers.memory.toolNames.join(", ")}\n- Resources:\n\n\`\`\`json\n${JSON.stringify(results.servers.memory.resources, null, 2)}\n\`\`\`\n\n## everything\n\n- Tools: ${results.servers.everything.toolNames.join(", ")}\n- Resources: ${results.servers.everything.resourceUris.join(", ")}\n- Prompts: ${results.servers.everything.promptNames.join(", ")}\n`;

await writeFile(outputMarkdownPath, markdown, "utf8");
