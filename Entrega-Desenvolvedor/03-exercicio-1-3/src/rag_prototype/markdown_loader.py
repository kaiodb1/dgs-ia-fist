from __future__ import annotations

import re
from pathlib import Path

from .models import DocumentSpec, Section, SourceDocument

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
METADATA_RE = re.compile(r"^\*\*(.+?)\*\*\s*:?\s*(.+)$")


def parse_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        match = METADATA_RE.match(line.strip())
        if match:
            metadata[match.group(1).strip().rstrip(":")] = match.group(2).strip()
    return metadata


def load_source_documents(docs_dir: Path, specs: tuple[DocumentSpec, ...]) -> list[SourceDocument]:
    documents: list[SourceDocument] = []
    for spec in specs:
        path = docs_dir / spec.file_name
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado para ingestão: {path}")
        text = path.read_text(encoding="utf-8")
        documents.append(
            SourceDocument(
                spec=spec,
                path=path,
                text=text,
                metadata=parse_metadata(text),
            )
        )
    return documents


def parse_sections(text: str) -> list[Section]:
    sections: list[Section] = []
    heading_stack: list[str] = []
    current_heading = ""
    current_level = 0
    current_lines: list[str] = []

    def flush_current() -> None:
        if not current_heading:
            return
        content = "\n".join(current_lines).strip()
        sections.append(
            Section(
                level=current_level,
                heading=current_heading,
                path=tuple(heading_stack),
                content=content,
            )
        )

    for raw_line in text.splitlines():
        match = HEADING_RE.match(raw_line)
        if match:
            flush_current()
            current_level = len(match.group(1))
            current_heading = match.group(2).strip()
            while len(heading_stack) >= current_level:
                heading_stack.pop()
            heading_stack.append(current_heading)
            current_lines = []
            continue
        current_lines.append(raw_line)

    flush_current()
    return [section for section in sections if section.path]
