from __future__ import annotations

from pathlib import Path

from .models import DocumentSpec

DELIVERABLE_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = DELIVERABLE_ROOT.parents[1]
DEFAULT_DOCS_DIR = REPOSITORY_ROOT / "Prática 1"
ARTIFACTS_DIR = DELIVERABLE_ROOT / "artifacts"
CHROMA_DIR = ARTIFACTS_DIR / "chroma_db"
MODEL_CACHE_DIR = ARTIFACTS_DIR / "model_cache"
COLLECTION_NAME = "novatech_rag_chunks"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K_DEFAULT = 5
TARGET_CHARS_PER_CHUNK = 1100
OVERLAP_BLOCKS = 1

DOCUMENT_SPECS = (
    DocumentSpec(
        file_name="POL-001-politica-devolucao.md",
        document_id="POL-001",
        title="Política de Devolução de Mercadorias",
        authority="normativo",
        source_priority=4,
        version_family="POL-001",
        preferred_version=True,
    ),
    DocumentSpec(
        file_name="PROC-042-frete-especial-v1.md",
        document_id="PROC-042",
        title="Procedimento de Cálculo de Frete Especial",
        authority="procedimento",
        source_priority=3,
        version_family="PROC-042",
        preferred_version=False,
    ),
    DocumentSpec(
        file_name="PROC-042-v2-frete-especial-revisado.md",
        document_id="PROC-042-v2",
        title="Procedimento de Cálculo de Frete Especial (Revisado)",
        authority="procedimento",
        source_priority=3,
        version_family="PROC-042",
        preferred_version=True,
    ),
    DocumentSpec(
        file_name="SLA-2024-tabela-sla-clientes.md",
        document_id="SLA-2024",
        title="Tabela de SLA por Tipo de Cliente",
        authority="contratual",
        source_priority=4,
        version_family="SLA-2024",
        preferred_version=True,
    ),
    DocumentSpec(
        file_name="FAQ-atendimento.md",
        document_id="FAQ-ATENDIMENTO",
        title="FAQ do Atendimento",
        authority="informal",
        source_priority=1,
        version_family="FAQ-ATENDIMENTO",
        preferred_version=True,
    ),
)

SYSTEM_PROMPT = """Você é o assistente interno da NovaTech para o time de atendimento.

Regras obrigatórias:
1. Responda em português do Brasil.
2. Use somente informações presentes nos chunks recuperados.
3. Cite a fonte no corpo da resposta em formato [documento | seção].
4. Se a informação não estiver coberta pelos chunks, diga explicitamente que a base recuperada não cobre a resposta.
5. Se houver conflito entre fontes, explique o conflito e aplique esta prioridade:
   - documentos normativos/contratuais;
   - procedimento mais recente quando houver múltiplas versões da mesma PROC;
   - FAQ apenas como complemento operacional, nunca como fonte única para regra crítica.
6. Não invente prazos, tiers, multiplicadores, regras comerciais ou exceções.
7. Quando a pergunta exigir decisão de negócio ou tratamento especial, indique o encaminhamento encontrado nos chunks."""
