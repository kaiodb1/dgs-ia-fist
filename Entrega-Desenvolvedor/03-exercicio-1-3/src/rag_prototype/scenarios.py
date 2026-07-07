from __future__ import annotations

from .models import RetrievalHit, Scenario, ScenarioResult

TEST_SCENARIOS = (
    Scenario(
        slug="prazo-devolucao",
        question="Qual o prazo de devolução?",
        must_have=("POL-001-A", "POL-001-B"),
        optional=("POL-001-C",),
    ),
    Scenario(
        slug="devolucao-carga-perigosa",
        question="Posso devolver carga perigosa?",
        must_have=("POL-001-B",),
        optional=("FAQ-03", "POL-001-A"),
    ),
    Scenario(
        slug="sla-cliente-gold",
        question="Qual o SLA do cliente Gold?",
        must_have=("SLA-2024-B",),
        optional=("SLA-2024-A", "SLA-2024-C"),
    ),
    Scenario(
        slug="frete-600kg-manaus",
        question="Frete para 600kg para Manaus?",
        must_have=("PROC-042v2-B", "PROC-042v2-A"),
        optional=("PROC-042-B",),
    ),
    Scenario(
        slug="multiplicador-sudeste",
        question="Qual o multiplicador para o Sudeste?",
        must_have=("PROC-042v2-B",),
        optional=("PROC-042-B",),
    ),
    Scenario(
        slug="frete-300kg-salvador",
        question="Frete para 300kg para Salvador?",
        must_have=(),
        optional=("PROC-042v2-B",),
        no_answer_expected=True,
    ),
    Scenario(
        slug="carga-danificada",
        question="O que acontece com carga danificada?",
        must_have=("FAQ-38",),
        optional=(),
    ),
)


def flatten_reference_ids(hits: tuple[RetrievalHit, ...]) -> tuple[str, ...]:
    ordered_ids: list[str] = []
    for hit in hits:
        for reference_id in hit.reference_ids:
            if reference_id and reference_id not in ordered_ids:
                ordered_ids.append(reference_id)
    return tuple(ordered_ids)


def evaluate_scenario(scenario: Scenario, hits: tuple[RetrievalHit, ...], prompt: str) -> ScenarioResult:
    recovered_reference_ids = flatten_reference_ids(hits)
    missing_reference_ids = tuple(reference_id for reference_id in scenario.must_have if reference_id not in recovered_reference_ids)
    optional_reference_ids_found = tuple(reference_id for reference_id in recovered_reference_ids if reference_id in scenario.optional)
    observations: list[str] = []

    if scenario.no_answer_expected:
        top_similarity = hits[0].similarity if hits else 0.0
        if top_similarity < 0.45:
            verdict = "Correto"
            observations.append("As similaridades ficaram baixas; o protótipo tende a sinalizar baixa cobertura documental.")
        elif optional_reference_ids_found:
            verdict = "Parcial"
            observations.append("A pergunta não tem cobertura formal; mesmo assim apareceram chunks parciais sobre frete especial (>500kg).")
        else:
            verdict = "Incorreto"
            observations.append("A pergunta não tem cobertura no Anexo B, mas o retriever retornou chunks fortes e potencialmente enganosos.")
    else:
        if not missing_reference_ids:
            verdict = "Correto"
        elif len(missing_reference_ids) < len(scenario.must_have):
            verdict = "Parcial"
        else:
            verdict = "Incorreto"

    if missing_reference_ids:
        observations.append(f"Chunks esperados ausentes: {', '.join(missing_reference_ids)}.")
    if optional_reference_ids_found:
        observations.append(f"Chunks opcionais/risco também apareceram: {', '.join(optional_reference_ids_found)}.")
    if any(hit.document_id == "FAQ-ATENDIMENTO" for hit in hits) and scenario.must_have and not scenario.must_have[0].startswith("FAQ"):
        observations.append("FAQ informal apareceu nos resultados; isso pede priorização por autoridade da fonte.")
    if any("PROC-042-B" in hit.reference_ids for hit in hits) and any("PROC-042v2-B" in hit.reference_ids for hit in hits):
        observations.append("Versões v1 e v2 da PROC-042 foram recuperadas juntas, criando risco real de contradição.")
    if not observations:
        observations.append("Sem ressalvas relevantes neste cenário.")

    return ScenarioResult(
        scenario=scenario,
        verdict=verdict,
        recovered_reference_ids=recovered_reference_ids,
        missing_reference_ids=missing_reference_ids,
        optional_reference_ids_found=optional_reference_ids_found,
        observations=tuple(observations),
        hits=hits,
        prompt=prompt,
    )
