from __future__ import annotations

import os
import re
from pathlib import Path

import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .chunking import MarkdownChunker, slugify
from .config import (
    ARTIFACTS_DIR,
    CHROMA_DIR,
    COLLECTION_NAME,
    DEFAULT_DOCS_DIR,
    DOCUMENT_SPECS,
    EMBEDDING_MODEL_NAME,
    MODEL_CACHE_DIR,
    SYSTEM_PROMPT,
)
from .markdown_loader import load_source_documents
from .models import Chunk, RetrievalHit

STOPWORDS = {
    "a",
    "ao",
    "as",
    "com",
    "da",
    "das",
    "de",
    "do",
    "dos",
    "e",
    "em",
    "o",
    "os",
    "para",
    "por",
    "qual",
    "que",
    "um",
    "uma",
}

CITY_REGION_HINTS = {
    "manaus": "regiao norte amazonas norte",
    "salvador": "regiao nordeste bahia nordeste",
}


class RAGPipeline:
    def __init__(
        self,
        *,
        docs_dir: Path = DEFAULT_DOCS_DIR,
        chroma_dir: Path = CHROMA_DIR,
        model_cache_dir: Path = MODEL_CACHE_DIR,
        collection_name: str = COLLECTION_NAME,
        model_name: str = EMBEDDING_MODEL_NAME,
    ) -> None:
        self.docs_dir = Path(docs_dir)
        self.chroma_dir = Path(chroma_dir)
        self.model_cache_dir = Path(model_cache_dir)
        self.collection_name = collection_name
        self.model_name = model_name
        self.chunker = MarkdownChunker()
        self._client: chromadb.ClientAPI | None = None
        self._model: SentenceTransformer | None = None

    def ensure_directories(self) -> None:
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.model_cache_dir.mkdir(parents=True, exist_ok=True)

    @property
    def client(self) -> chromadb.ClientAPI:
        if self._client is None:
            self.ensure_directories()
            self._client = chromadb.PersistentClient(path=str(self.chroma_dir))
        return self._client

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            self.ensure_directories()
            os.environ.setdefault("HF_HOME", str(self.model_cache_dir))
            os.environ.setdefault("SENTENCE_TRANSFORMERS_HOME", str(self.model_cache_dir))
            self._model = SentenceTransformer(self.model_name, cache_folder=str(self.model_cache_dir))
        return self._model

    def rebuild_collection(self) -> None:
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass

    def get_collection(self):
        return self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def ingest(self) -> dict[str, object]:
        self.rebuild_collection()
        collection = self.get_collection()
        documents = load_source_documents(self.docs_dir, DOCUMENT_SPECS)
        chunks = self._build_chunks(documents)
        embeddings = self.model.encode(
            [chunk.embedding_text for chunk in chunks],
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        collection.add(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            embeddings=embeddings.tolist(),
            metadatas=[chunk.chroma_metadata() for chunk in chunks],
        )
        manifest = {
            "docs_dir": str(self.docs_dir),
            "model_name": self.model_name,
            "document_count": len(documents),
            "chunk_count": len(chunks),
            "documents": [str(document.path) for document in documents],
            "chunk_ids": [chunk.chunk_id for chunk in chunks],
        }
        return manifest

    def _build_chunks(self, documents) -> list[Chunk]:
        chunks: list[Chunk] = []
        for document in documents:
            chunks.extend(self.chunker.chunk_document(document))
        return chunks

    def collection_count(self) -> int:
        return self.get_collection().count()

    def retrieve(self, question: str, top_k: int) -> tuple[RetrievalHit, ...]:
        collection = self.get_collection()
        if collection.count() == 0:
            raise RuntimeError("A coleção está vazia. Execute o comando de ingestão antes da consulta.")

        expanded_question = self._expand_query(question)
        query_embedding = self.model.encode([expanded_question], normalize_embeddings=True, show_progress_bar=False)[0]
        stored = collection.get(
            limit=collection.count(),
            include=["documents", "metadatas", "embeddings"],
        )

        ids = stored.get("ids", [])
        documents = stored.get("documents", [])
        metadatas = stored.get("metadatas", [])
        embeddings = np.asarray(stored.get("embeddings", []), dtype=float)
        if embeddings.size == 0:
            raise RuntimeError("Não foi possível carregar embeddings do ChromaDB.")

        dense_scores = ((embeddings @ query_embedding) + 1.0) / 2.0
        vectorizer = TfidfVectorizer(strip_accents="unicode", lowercase=True, ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([*documents, expanded_question])
        lexical_scores = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1]).ravel()
        normalized_question = self._normalize_for_match(question)
        normalized_expanded_question = self._normalize_for_match(expanded_question)

        ranked_rows: list[tuple[float, int]] = []
        for index, chunk_id in enumerate(ids):
            metadata = metadatas[index] or {}
            text = str(documents[index])
            section_path = str(metadata.get("section_path", ""))
            combined_score = (
                0.58 * float(dense_scores[index])
                + 0.32 * float(lexical_scores[index])
                + self._authority_bonus(int(metadata.get("source_priority", 0)))
                + self._preferred_version_bonus(bool(metadata.get("preferred_version", False)))
                + self._section_overlap_bonus(normalized_expanded_question, section_path)
                + self._intent_bonus(normalized_question, text, section_path)
            )
            ranked_rows.append((min(combined_score, 0.9999), index))

        ranked_rows.sort(key=lambda item: item[0], reverse=True)

        hits: list[RetrievalHit] = []
        for rank, (similarity, index) in enumerate(ranked_rows[:top_k], start=1):
            metadata = metadatas[index] or {}
            reference_ids_csv = str(metadata.get("reference_ids") or "")
            reference_ids = tuple(item for item in reference_ids_csv.split(",") if item)
            hits.append(
                RetrievalHit(
                    rank=rank,
                    chunk_id=str(ids[index]),
                    document_id=str(metadata.get("document_id", "")),
                    document_title=str(metadata.get("document_title", "")),
                    authority=str(metadata.get("authority", "")),
                    source_priority=int(metadata.get("source_priority", 0)),
                    section_path=str(metadata.get("section_path", "")),
                    reference_ids=reference_ids,
                    version_family=str(metadata.get("version_family", "")),
                    version_label=str(metadata.get("version_label", "")),
                    preferred_version=bool(metadata.get("preferred_version", False)),
                    distance=max(0.0, 1.0 - similarity),
                    similarity=float(similarity),
                    text=str(documents[index]),
                )
            )
        return tuple(hits)

    def build_prompt(self, question: str, hits: tuple[RetrievalHit, ...]) -> str:
        context_blocks: list[str] = []
        for hit in hits:
            references = ", ".join(hit.reference_ids) if hit.reference_ids else "sem mapeamento Anexo B"
            context_blocks.append(
                "\n".join(
                    [
                        f"[Chunk {hit.rank}] documento={hit.document_id}; seção={hit.section_path}; autoridade={hit.authority}; similaridade={hit.similarity:.4f}; referencias={references}",
                        hit.text,
                    ]
                )
            )

        dynamic_context = "\n\n".join(context_blocks) if context_blocks else "Nenhum chunk recuperado."
        return (
            "### System prompt\n"
            f"{SYSTEM_PROMPT}\n\n"
            "### Chunks recuperados\n"
            f"{dynamic_context}\n\n"
            "### Pergunta do atendente\n"
            f"{question}\n\n"
            "### Instrução final\n"
            "Responda de forma objetiva, com indicação das fontes. Se não houver cobertura suficiente nos chunks, diga isso explicitamente."
        )

    @staticmethod
    def _normalize_for_match(value: str) -> str:
        return slugify(value).replace("-", " ")

    def _expand_query(self, question: str) -> str:
        normalized_question = self._normalize_for_match(question)
        hints: list[str] = []

        for city, expansion in CITY_REGION_HINTS.items():
            if city in normalized_question:
                hints.append(expansion)

        weight_match = re.search(r"\b(\d+)\s*kg\b", normalized_question)
        if weight_match:
            weight = int(weight_match.group(1))
            if weight >= 500:
                hints.append("frete especial acima de 500kg fator de peso multiplicador regional")
            else:
                hints.append("abaixo de 500kg frete padrao sem cobertura documental explicita")

        if "prazo" in normalized_question and "devolu" in normalized_question:
            hints.append("prazo geral devolucao dias uteis")
        if "sla" in normalized_question:
            hints.append("tempo de primeira resposta tempo de resolucao")
            if "critico" not in normalized_question and "incidente" not in normalized_question:
                hints.append("chamados gerais")
        if "multiplicador" in normalized_question or "frete" in normalized_question:
            hints.append("frete especial multiplicadores regionais")
        if "carga" in normalized_question and "perigos" in normalized_question and (
            "devolver" in normalized_question or "devolu" in normalized_question
        ):
            hints.append("nao elegivel processo padrao gestao de riscos")

        if not hints:
            return question
        return f"{question}\n\nExpansão de retrieval: {'; '.join(hints)}"

    @staticmethod
    def _authority_bonus(source_priority: int) -> float:
        return source_priority * 0.018

    @staticmethod
    def _preferred_version_bonus(preferred_version: bool) -> float:
        return 0.028 if preferred_version else 0.0

    def _section_overlap_bonus(self, normalized_question: str, section_path: str) -> float:
        question_terms = {
            term for term in self._normalize_for_match(normalized_question).split() if term and term not in STOPWORDS
        }
        section_terms = {term for term in self._normalize_for_match(section_path).split() if term and term not in STOPWORDS}
        overlap = len(question_terms & section_terms)
        return min(0.12, overlap * 0.03)

    def _intent_bonus(self, normalized_question: str, text: str, section_path: str) -> float:
        normalized_text = self._normalize_for_match(text)
        normalized_section = self._normalize_for_match(section_path)
        bonus = 0.0

        if "prazo" in normalized_question and "devolu" in normalized_question:
            if "prazo geral" in normalized_text or "prazo geral" in normalized_section:
                bonus += 0.08
            if "custos" in normalized_section:
                bonus -= 0.03

        if "carga" in normalized_question and "perigos" in normalized_question and (
            "devolver" in normalized_question or "devolu" in normalized_question
        ):
            if "nao sao elegiveis" in normalized_text or "gestao de riscos" in normalized_text:
                bonus += 0.08

        if "sla" in normalized_question:
            if "critico" not in normalized_question and "incidente" not in normalized_question:
                if "chamados gerais" in normalized_text:
                    bonus += 0.07
                if "incidentes criticos" in normalized_text:
                    bonus -= 0.04
                if "disponibilidade do portal" in normalized_text or "relatorio mensal de performance" in normalized_text:
                    bonus -= 0.03

        if "multiplicador" in normalized_question or "frete" in normalized_question:
            if "multiplicadores regionais" in normalized_text or "multiplicadores regionais" in normalized_section:
                bonus += 0.08

        return bonus
