from __future__ import annotations

import re
from dataclasses import dataclass

from .config import OVERLAP_BLOCKS, TARGET_CHARS_PER_CHUNK
from .markdown_loader import parse_sections
from .models import Chunk, Section, SourceDocument

TABLE_LINE_RE = re.compile(r"^\|.*\|$")
LIST_LINE_RE = re.compile(r"^(\d+\.\s+|- |\* )")


@dataclass(frozen=True)
class Block:
    kind: str
    text: str


@dataclass(frozen=True)
class SectionSlice:
    label: str
    text: str


def slugify(value: str) -> str:
    text = value.lower()
    text = (
        text.replace("á", "a")
        .replace("à", "a")
        .replace("ã", "a")
        .replace("â", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("õ", "o")
        .replace("ú", "u")
        .replace("ç", "c")
    )
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def detect_block_kind(line: str) -> str:
    stripped = line.strip()
    if TABLE_LINE_RE.match(stripped):
        return "table"
    if LIST_LINE_RE.match(stripped):
        return "list"
    return "paragraph"


def extract_blocks(content: str) -> list[Block]:
    blocks: list[Block] = []
    buffer: list[str] = []
    current_kind = ""

    def flush() -> None:
        nonlocal buffer, current_kind
        if buffer:
            blocks.append(Block(kind=current_kind or "paragraph", text="\n".join(buffer).strip()))
            buffer = []
            current_kind = ""

    for raw_line in content.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            flush()
            continue
        line_kind = detect_block_kind(raw_line)
        if line_kind != current_kind and buffer:
            flush()
        current_kind = line_kind
        buffer.append(raw_line)

    flush()
    return [block for block in blocks if block.text]


def split_sla_table_section(section: Section) -> list[SectionSlice]:
    lines = [line for line in section.content.splitlines() if line.strip()]
    table_lines = [line for line in lines if TABLE_LINE_RE.match(line.strip())]
    if len(table_lines) < 3:
        return []

    intro_lines = [line for line in lines if line not in table_lines]
    header, divider, *rows = table_lines
    general_rows = [row for row in rows if "chamados gerais" in row.lower()]
    critical_rows = [row for row in rows if "incidentes críticos" in row.lower()]
    extra_rows = [row for row in rows if row not in general_rows + critical_rows]
    intro = "\n".join(intro_lines).strip()

    slices: list[SectionSlice] = []
    groups = (
        ("sla-geral", general_rows),
        ("sla-critico", critical_rows),
        ("sla-complementar", extra_rows),
    )
    for label, grouped_rows in groups:
        if not grouped_rows:
            continue
        parts = []
        if intro:
            parts.append(intro)
        parts.append("\n".join([header, divider, *grouped_rows]))
        slices.append(SectionSlice(label=label, text="\n\n".join(parts).strip()))
    return slices


def pack_blocks(section: Section, blocks: list[Block], target_chars: int = TARGET_CHARS_PER_CHUNK) -> list[SectionSlice]:
    if not blocks:
        return []

    full_text = "\n\n".join(block.text for block in blocks)
    if len(full_text) <= target_chars:
        return [SectionSlice(label="section", text=full_text)]

    slices: list[SectionSlice] = []
    current_blocks: list[Block] = []
    current_len = 0

    for block in blocks:
        candidate_len = current_len + len(block.text) + (2 if current_blocks else 0)
        if current_blocks and candidate_len > target_chars and block.kind != "table":
            slices.append(
                SectionSlice(
                    label=f"section-part-{len(slices) + 1}",
                    text="\n\n".join(item.text for item in current_blocks),
                )
            )
            overlap = current_blocks[-OVERLAP_BLOCKS:] if OVERLAP_BLOCKS and len(current_blocks) > OVERLAP_BLOCKS else []
            current_blocks = list(overlap)
            current_len = sum(len(item.text) for item in current_blocks) + max(0, len(current_blocks) - 1) * 2
        current_blocks.append(block)
        current_len = current_len + len(block.text) + (2 if len(current_blocks) > 1 else 0)

    if current_blocks:
        slices.append(
            SectionSlice(
                label=f"section-part-{len(slices) + 1}",
                text="\n\n".join(item.text for item in current_blocks),
            )
        )
    return slices


def parse_markdown_table(table_text: str) -> tuple[list[str], list[list[str]]] | None:
    lines = [line.strip() for line in table_text.splitlines() if line.strip()]
    table_lines = [line for line in lines if TABLE_LINE_RE.match(line)]
    if len(table_lines) < 2:
        return None

    parsed_rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in table_lines]
    headers = parsed_rows[0]
    data_rows: list[list[str]] = []
    for row in parsed_rows[2:]:
        if len(row) != len(headers):
            continue
        data_rows.append(row)

    if not headers or not data_rows:
        return None
    return headers, data_rows


def humanize_slice_label(slice_label: str) -> str:
    mapping = {
        "sla-geral": "Subtema: SLAs para chamados gerais.",
        "sla-critico": "Subtema: SLAs para incidentes críticos.",
        "sla-complementar": "Subtema: Indicadores complementares de SLA.",
    }
    return mapping.get(slice_label, "")


def render_table_summary(headers: list[str], data_rows: list[list[str]], slice_label: str) -> str:
    intro = humanize_slice_label(slice_label)
    summary_lines: list[str] = []
    if intro:
        summary_lines.append(intro)

    if slugify(headers[0]) == "metrica" and len(headers) > 1:
        for column_index, column_name in enumerate(headers[1:], start=1):
            metrics = []
            for row in data_rows:
                metrics.append(f"{row[0]}: {row[column_index]}")
            summary_lines.append(f"- {column_name}: " + "; ".join(metrics) + ".")
        return "\n".join(summary_lines)

    for row in data_rows:
        pairs = [f"{headers[index]}: {cell}" for index, cell in enumerate(row)]
        summary_lines.append("- " + "; ".join(pairs) + ".")
    return "\n".join(summary_lines)


def build_embedding_body(body: str, slice_label: str) -> str:
    rendered_blocks: list[str] = []
    for block in extract_blocks(body):
        if block.kind != "table":
            rendered_blocks.append(block.text)
            continue
        parsed_table = parse_markdown_table(block.text)
        if parsed_table is None:
            rendered_blocks.append(block.text)
            continue
        rendered_blocks.append(render_table_summary(*parsed_table, slice_label))
    return "\n\n".join(item for item in rendered_blocks if item.strip()).strip()


def build_display_body(body: str, slice_label: str) -> str:
    rendered_blocks: list[str] = []
    for block in extract_blocks(body):
        if block.kind != "table":
            rendered_blocks.append(block.text)
            continue
        parsed_table = parse_markdown_table(block.text)
        if parsed_table is None:
            rendered_blocks.append(block.text)
            continue
        rendered_blocks.append("Tabela normalizada:\n" + render_table_summary(*parsed_table, slice_label))
        rendered_blocks.append("Tabela original markdown:\n" + block.text)
    return "\n\n".join(item for item in rendered_blocks if item.strip()).strip()


def infer_reference_ids(document_id: str, section_path: str, slice_label: str, chunk_text: str) -> tuple[str, ...]:
    normalized_path = slugify(section_path)
    normalized_text = slugify(chunk_text)

    if document_id == "POL-001":
        if "3-1" in normalized_path and "prazo-geral" in normalized_path:
            return ("POL-001-A",)
        if "3-2" in normalized_path and "exce" in normalized_path:
            return ("POL-001-B",)
        if "3-3" in normalized_path and "procedimento" in normalized_path:
            return ("POL-001-C",)
        if "3-5" in normalized_path and "custos" in normalized_path:
            return ("POL-001-D",)

    if document_id == "PROC-042":
        if "2-1" in normalized_path and "multiplicadores-regionais" in normalized_path:
            return ("PROC-042-B",)
        if normalized_path.endswith("2-formula-de-calculo"):
            return ("PROC-042-A",)
        if normalized_path.endswith("3-prazo-de-entrega-para-frete-especial"):
            return ("PROC-042-C",)

    if document_id == "PROC-042-v2":
        if "2-1" in normalized_path and "multiplicadores-regionais" in normalized_path:
            return ("PROC-042v2-B",)
        if normalized_path.endswith("2-formula-de-calculo"):
            return ("PROC-042v2-A",)
        if normalized_path.endswith("3-prazo-de-entrega-para-frete-especial"):
            return ("PROC-042v2-C",)
        if "descontos-de-volume" in normalized_text or "a-partir-de-8-fretes-especiais" in normalized_text:
            return ("PROC-042v2-D",)
        if normalized_path.endswith("5-disposicoes-transitorias"):
            return ("PROC-042v2-E",)

    if document_id == "SLA-2024":
        if normalized_path.endswith("1-classificacao-de-clientes"):
            return ("SLA-2024-A",)
        if normalized_path.endswith("2-tabela-de-slas") and slice_label == "sla-geral":
            return ("SLA-2024-B",)
        if normalized_path.endswith("2-tabela-de-slas") and slice_label == "sla-critico":
            return ("SLA-2024-C",)
        if normalized_path.endswith("3-definicao-de-incidente-critico"):
            return ("SLA-2024-D",)
        if normalized_path.endswith("4-penalidades-por-descumprimento"):
            return ("SLA-2024-E",)

    if document_id == "FAQ-ATENDIMENTO":
        item_match = re.search(r"item-(\d+)", normalized_path)
        if item_match:
            return (f"FAQ-{int(item_match.group(1)):02d}",)

    return ()


class MarkdownChunker:
    def __init__(self, target_chars: int = TARGET_CHARS_PER_CHUNK) -> None:
        self.target_chars = target_chars

    def chunk_document(self, document: SourceDocument) -> list[Chunk]:
        sections = parse_sections(document.text)
        chunks: list[Chunk] = []
        for section in sections:
            if section.level < 2 or not section.content.strip():
                continue
            slices = self._split_section(document, section)
            if not slices:
                continue
            for index, section_slice in enumerate(slices, start=1):
                section_path = " > ".join(section.path[1:]) if len(section.path) > 1 else section.path[0]
                heading_label = slugify(section_path or section.heading) or "chunk"
                suffix = slugify(section_slice.label) if section_slice.label and section_slice.label != "section" else f"part-{index:02d}"
                chunk_id = f"{slugify(document.spec.document_id)}__{heading_label}__{suffix}"
                reference_ids = infer_reference_ids(
                    document_id=document.spec.document_id,
                    section_path=section_path,
                    slice_label=section_slice.label,
                    chunk_text=section_slice.text,
                )
                text = self._build_chunk_text(
                    document,
                    section_path,
                    section_slice.text,
                    section_slice.label,
                    include_raw_tables=True,
                )
                embedding_text = self._build_chunk_text(
                    document,
                    section_path,
                    section_slice.text,
                    section_slice.label,
                    include_raw_tables=False,
                )
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        document_id=document.spec.document_id,
                        document_title=document.spec.title,
                        authority=document.spec.authority,
                        source_priority=document.spec.source_priority,
                        source_path=str(document.path),
                        section_path=section_path,
                        reference_ids=reference_ids,
                        version_family=document.spec.version_family,
                        version_label=document.metadata.get("Versão")
                        or document.metadata.get("Última atualização")
                        or document.metadata.get("Data de emissão")
                        or "n/d",
                        preferred_version=document.spec.preferred_version,
                        text=text,
                        embedding_text=embedding_text,
                    )
                )
        return chunks

    def _split_section(self, document: SourceDocument, section: Section) -> list[SectionSlice]:
        if document.spec.document_id == "SLA-2024" and "tabela de slas" in section.heading.lower():
            special_slices = split_sla_table_section(section)
            if special_slices:
                return special_slices
        blocks = extract_blocks(section.content)
        return pack_blocks(section, blocks, target_chars=self.target_chars)

    @staticmethod
    def _build_chunk_text(
        document: SourceDocument,
        section_path: str,
        body: str,
        slice_label: str,
        *,
        include_raw_tables: bool,
    ) -> str:
        header = f"Documento: {document.spec.document_id} | Tipo: {document.spec.authority} | Seção: {section_path}"
        rendered_body = build_display_body(body, slice_label) if include_raw_tables else build_embedding_body(body, slice_label)
        return f"{header}\n{rendered_body.strip()}".strip()
