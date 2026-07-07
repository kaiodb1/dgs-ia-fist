from __future__ import annotations

import argparse
from pathlib import Path

from .config import ARTIFACTS_DIR, DEFAULT_DOCS_DIR, DELIVERABLE_ROOT, TOP_K_DEFAULT
from .pipeline import RAGPipeline
from .reporting import render_markdown_report, write_json
from .scenarios import TEST_SCENARIOS, evaluate_scenario


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="novatech-rag",
        description="Protótipo local de RAG para os 5 documentos simulados da NovaTech.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Lê os documentos, gera embeddings e recria o índice local.")
    ingest_parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    ingest_parser.add_argument("--manifest-path", type=Path, default=ARTIFACTS_DIR / "ingestion_manifest.json")

    query_parser = subparsers.add_parser("query", help="Executa retrieval para uma pergunta.")
    query_parser.add_argument("--question", required=True)
    query_parser.add_argument("--top-k", type=int, default=TOP_K_DEFAULT)
    query_parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    query_parser.add_argument("--json-output", type=Path)
    query_parser.add_argument("--prompt-output", type=Path)
    query_parser.add_argument("--show-prompt", action="store_true")

    prompt_parser = subparsers.add_parser("prompt", help="Monta apenas o prompt final para colar em um LLM.")
    prompt_parser.add_argument("--question", required=True)
    prompt_parser.add_argument("--top-k", type=int, default=TOP_K_DEFAULT)
    prompt_parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    prompt_parser.add_argument("--output", type=Path)

    tests_parser = subparsers.add_parser("run-tests", help="Executa os cenários de validação do Anexo B.")
    tests_parser.add_argument("--top-k", type=int, default=TOP_K_DEFAULT)
    tests_parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    tests_parser.add_argument("--reuse-index", action="store_true")
    tests_parser.add_argument("--json-output", type=Path, default=ARTIFACTS_DIR / "test_results.json")
    tests_parser.add_argument("--markdown-output", type=Path, default=DELIVERABLE_ROOT / "resultados-testes.md")
    tests_parser.add_argument(
        "--sample-prompt-output",
        type=Path,
        default=ARTIFACTS_DIR / "prompt_exemplo_frete_manaus.txt",
    )

    return parser.parse_args()


def print_hits(question: str, hits) -> None:
    print(f"Pergunta: {question}")
    for hit in hits:
        reference_ids = ", ".join(hit.reference_ids) if hit.reference_ids else "sem mapeamento"
        excerpt = " ".join(hit.text.split())
        if len(excerpt) > 180:
            excerpt = f"{excerpt[:179]}…"
        print(
            f"{hit.rank}. sim={hit.similarity:.4f} | {hit.document_id} | refs={reference_ids} | seção={hit.section_path}"
        )
        print(f"   {excerpt}")


def handle_ingest(args: argparse.Namespace) -> int:
    pipeline = RAGPipeline(docs_dir=args.docs_dir)
    manifest = pipeline.ingest()
    write_json(args.manifest_path, manifest)
    print(f"Ingestão concluída: {manifest['document_count']} documentos, {manifest['chunk_count']} chunks.")
    print(f"Manifesto salvo em: {args.manifest_path}")
    return 0


def handle_query(args: argparse.Namespace) -> int:
    pipeline = RAGPipeline(docs_dir=args.docs_dir)
    hits = pipeline.retrieve(args.question, args.top_k)
    prompt = pipeline.build_prompt(args.question, hits)
    print_hits(args.question, hits)

    if args.json_output:
        payload = {
            "question": args.question,
            "hits": [
                {
                    "rank": hit.rank,
                    "chunk_id": hit.chunk_id,
                    "document_id": hit.document_id,
                    "section_path": hit.section_path,
                    "reference_ids": list(hit.reference_ids),
                    "similarity": hit.similarity,
                    "text": hit.text,
                }
                for hit in hits
            ],
            "prompt": prompt,
        }
        write_json(args.json_output, payload)

    if args.prompt_output:
        args.prompt_output.parent.mkdir(parents=True, exist_ok=True)
        args.prompt_output.write_text(prompt, encoding="utf-8")
        print(f"Prompt salvo em: {args.prompt_output}")

    if args.show_prompt:
        print("\n--- PROMPT ---\n")
        print(prompt)

    return 0


def handle_prompt(args: argparse.Namespace) -> int:
    pipeline = RAGPipeline(docs_dir=args.docs_dir)
    hits = pipeline.retrieve(args.question, args.top_k)
    prompt = pipeline.build_prompt(args.question, hits)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(prompt, encoding="utf-8")
        print(f"Prompt salvo em: {args.output}")
    else:
        print(prompt)
    return 0


def handle_run_tests(args: argparse.Namespace) -> int:
    pipeline = RAGPipeline(docs_dir=args.docs_dir)
    if not args.reuse_index:
        manifest = pipeline.ingest()
        write_json(ARTIFACTS_DIR / "ingestion_manifest.json", manifest)

    results = []
    for scenario in TEST_SCENARIOS:
        hits = pipeline.retrieve(scenario.question, args.top_k)
        prompt = pipeline.build_prompt(scenario.question, hits)
        result = evaluate_scenario(scenario, hits, prompt)
        results.append(result)

        if scenario.slug == "frete-600kg-manaus":
            args.sample_prompt_output.parent.mkdir(parents=True, exist_ok=True)
            args.sample_prompt_output.write_text(prompt, encoding="utf-8")

    tuple_results = tuple(results)
    payload = {
        "docs_dir": str(args.docs_dir),
        "chunk_count": pipeline.collection_count(),
        "model_name": pipeline.model_name,
        "results": [result.to_dict() for result in tuple_results],
    }
    write_json(args.json_output, payload)

    markdown = render_markdown_report(
        tuple_results,
        chunk_count=pipeline.collection_count(),
        model_name=pipeline.model_name,
        docs_dir=str(args.docs_dir),
    )
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text(markdown, encoding="utf-8")

    correct = sum(1 for result in tuple_results if result.verdict == "Correto")
    partial = sum(1 for result in tuple_results if result.verdict == "Parcial")
    incorrect = sum(1 for result in tuple_results if result.verdict == "Incorreto")
    print(
        f"Testes concluídos: {len(tuple_results)} cenários | corretos={correct} | parciais={partial} | incorretos={incorrect}"
    )
    print(f"JSON salvo em: {args.json_output}")
    print(f"Markdown salvo em: {args.markdown_output}")
    print(f"Prompt de exemplo salvo em: {args.sample_prompt_output}")
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "ingest":
        return handle_ingest(args)
    if args.command == "query":
        return handle_query(args)
    if args.command == "prompt":
        return handle_prompt(args)
    if args.command == "run-tests":
        return handle_run_tests(args)
    return 1
