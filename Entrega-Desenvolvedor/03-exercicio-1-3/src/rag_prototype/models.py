from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DocumentSpec:
    file_name: str
    document_id: str
    title: str
    authority: str
    source_priority: int
    version_family: str
    preferred_version: bool = True


@dataclass(frozen=True)
class SourceDocument:
    spec: DocumentSpec
    path: Path
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class Section:
    level: int
    heading: str
    path: tuple[str, ...]
    content: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    document_title: str
    authority: str
    source_priority: int
    source_path: str
    section_path: str
    reference_ids: tuple[str, ...]
    version_family: str
    version_label: str
    preferred_version: bool
    text: str
    embedding_text: str

    def chroma_metadata(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "document_title": self.document_title,
            "authority": self.authority,
            "source_priority": self.source_priority,
            "source_path": self.source_path,
            "section_path": self.section_path,
            "reference_ids": ",".join(self.reference_ids),
            "version_family": self.version_family,
            "version_label": self.version_label,
            "preferred_version": self.preferred_version,
        }


@dataclass(frozen=True)
class RetrievalHit:
    rank: int
    chunk_id: str
    document_id: str
    document_title: str
    authority: str
    source_priority: int
    section_path: str
    reference_ids: tuple[str, ...]
    version_family: str
    version_label: str
    preferred_version: bool
    distance: float
    similarity: float
    text: str


@dataclass(frozen=True)
class Scenario:
    slug: str
    question: str
    must_have: tuple[str, ...]
    optional: tuple[str, ...] = ()
    no_answer_expected: bool = False


@dataclass(frozen=True)
class ScenarioResult:
    scenario: Scenario
    verdict: str
    recovered_reference_ids: tuple[str, ...]
    missing_reference_ids: tuple[str, ...]
    optional_reference_ids_found: tuple[str, ...]
    observations: tuple[str, ...]
    hits: tuple[RetrievalHit, ...]
    prompt: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario": {
                "slug": self.scenario.slug,
                "question": self.scenario.question,
                "must_have": list(self.scenario.must_have),
                "optional": list(self.scenario.optional),
                "no_answer_expected": self.scenario.no_answer_expected,
            },
            "verdict": self.verdict,
            "recovered_reference_ids": list(self.recovered_reference_ids),
            "missing_reference_ids": list(self.missing_reference_ids),
            "optional_reference_ids_found": list(self.optional_reference_ids_found),
            "observations": list(self.observations),
            "hits": [
                {
                    "rank": hit.rank,
                    "chunk_id": hit.chunk_id,
                    "document_id": hit.document_id,
                    "document_title": hit.document_title,
                    "authority": hit.authority,
                    "source_priority": hit.source_priority,
                    "section_path": hit.section_path,
                    "reference_ids": list(hit.reference_ids),
                    "version_family": hit.version_family,
                    "version_label": hit.version_label,
                    "preferred_version": hit.preferred_version,
                    "distance": hit.distance,
                    "similarity": hit.similarity,
                    "text": hit.text,
                }
                for hit in self.hits
            ],
            "prompt": self.prompt,
        }
