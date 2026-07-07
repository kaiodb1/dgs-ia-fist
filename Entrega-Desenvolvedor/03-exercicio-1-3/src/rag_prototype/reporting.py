from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import ScenarioResult


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def shorten_text(value: str, max_chars: int = 240) -> str:
    compact = " ".join(value.split())
    if len(compact) <= max_chars:
        return compact
    return f"{compact[: max_chars - 1]}…"


def escape_pipes(value: str) -> str:
    return value.replace("|", "\\|")


def render_markdown_report(
    results: tuple[ScenarioResult, ...],
    *,
    chunk_count: int,
    model_name: str,
    docs_dir: str,
) -> str:
    generated_at = datetime.now().isoformat(timespec="seconds")
    correct = sum(1 for result in results if result.verdict == "Correto")
    partial = sum(1 for result in results if result.verdict == "Parcial")
    incorrect = sum(1 for result in results if result.verdict == "Incorreto")

    lines = [
        "# Resultados dos testes do protótipo RAG",
        "",
        f"- Gerado em: `{generated_at}`",
        f"- Diretório dos documentos ingeridos: `{docs_dir}`",
        f"- Modelo de embeddings: `{model_name}`",
        f"- Chunks indexados no ChromaDB: `{chunk_count}`",
        f"- Cenários executados: `{len(results)}`",
        f"- Veredictos: `{correct}` corretos, `{partial}` parciais, `{incorrect}` incorretos",
        "",
        "## Estratégia de leitura dos resultados",
        "- `Chunks esperados`: gabarito do Anexo B.",
        "- `Recuperado`: IDs de referência encontrados nos chunks retornados.",
        "- O corpo do chunk abaixo mostra o trecho realmente recuperado pelo protótipo.",
        "",
    ]

    for index, result in enumerate(results, start=1):
        scenario = result.scenario
        expected = ", ".join(scenario.must_have) if scenario.must_have else "Nenhum chunk formal esperado"
        optional = ", ".join(scenario.optional) if scenario.optional else "—"
        recovered = ", ".join(result.recovered_reference_ids) if result.recovered_reference_ids else "—"
        missing = ", ".join(result.missing_reference_ids) if result.missing_reference_ids else "—"
        observations = " ".join(result.observations)

        lines.extend(
            [
                f"## {index}. {scenario.slug}",
                f"- Pergunta: `{scenario.question}`",
                f"- Chunks esperados (Anexo B): `{expected}`",
                f"- Chunks opcionais / risco: `{optional}`",
                f"- Recuperado: `{recovered}`",
                f"- Faltantes: `{missing}`",
                f"- Veredito: **{result.verdict}**",
                f"- Observações: {observations}",
                "",
                "| Rank | Similaridade | Chunk interno | Referência(s) | Documento | Seção |",
                "|---:|---:|---|---|---|---|",
            ]
        )

        for hit in result.hits:
            reference_ids = ", ".join(hit.reference_ids) if hit.reference_ids else "—"
            lines.append(
                f"| {hit.rank} | {hit.similarity:.4f} | `{hit.chunk_id}` | `{reference_ids}` | `{hit.document_id}` | `{escape_pipes(hit.section_path)}` |"
            )

        lines.append("")
        for hit in result.hits[:3]:
            reference_ids = ", ".join(hit.reference_ids) if hit.reference_ids else "sem mapeamento"
            lines.extend(
                [
                    f"### Chunk rank {hit.rank}",
                    f"- Similaridade: `{hit.similarity:.4f}`",
                    f"- Documento: `{hit.document_id}`",
                    f"- Referência(s) do Anexo B: `{reference_ids}`",
                    "",
                    "> " + hit.text.replace("\n", "\n> "),
                    "",
                ]
            )

    return "\n".join(lines).strip() + "\n"
