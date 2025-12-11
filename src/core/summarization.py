from pydantic import BaseModel, Field

from .llm_adapter import LlmAdapter
from .extraction import Fragment, compile_fragments


class SummarizationCriterion(BaseModel):
    score: int = Field(..., ge=1, le=10)
    comment: str


class SummarizationCriterions(BaseModel):
    value_proposition_clarity: SummarizationCriterion
    value_proposition_uniqueness: SummarizationCriterion
    trust_strength: SummarizationCriterion
    cta_strength: SummarizationCriterion
    seo_friendliness: SummarizationCriterion
    audience_fit: SummarizationCriterion


SUMMARIZATION_CRITERIONS_FULL_NAMES = {
    "value_proposition_clarity": "Value Proposition Clarity",
    "value_proposition_uniqueness": "Value Proposition Uniqueness",
    "trust_strength": "Trust Strength",
    "cta_strength": "CTA Strength",
    "seo_friendliness": "SEO Friendliness",
    "audience_fit": "Audience Fit",
}


class SummarizationOutput(BaseModel):
    criterions: SummarizationCriterions
    recommendations: list[str]


_SUMMARIZATION_CRITERIONS_DESC = "\n".join(
    f"""        "{crit}": {{
            "score": <score>, // score 1-10
            "comment": "<comment>" // your comment & explanation
        }}"""
    for crit in SummarizationCriterions.model_fields
)

SUMMARIZATION_INSTRUCT_PROMPT = f"""
You are a B2B marketing analysis engine trained on modern SaaS best practices, enterprise messaging standards, and principles from top experts (e.g., David Ogilvy, Andy Raskin, April Dunford, category design frameworks).

You receive clean structured text extracted from a B2B homepage, already organized into:

- Main Headline
- Subheadline
- Product Description
- CTA
- Social Proof
- Key Sections

Your task is to evaluate the effectiveness of this homepage as if you were a B2B buyer visiting the website for the first time.

YOUR GOALS

Score the homepage across key marketing criteria.

Explain the reasoning behind each score.

Identify gaps, missing elements, inconsistencies, and weak spots.

Describe how well the page addresses the needs and pain points of B2B decision makers (CFO, CTO, COO, VP Ops, etc.).

Optionally prepare insights that will be used later to generate actionable recommendations (but do NOT generate recommendations yet).

SCORING CRITERIA (1–10 scale)

Score each dimension from 1 (very weak) to 10 (world-class).

- Value proposition clarity: can a first-time visitor understand what the product does and who it's for in under 5 seconds?
- Value Proposition Uniqueness: is it clear how this product differs from competitors? Is there a specific niche, role, or problem it focuses on?
- Trust & Social Proof Strength: are client logos, testimonials, ROI metrics, or case studies present and convincing?
- CTA Strength: are next steps clear, specific, and compelling (e.g., “Get a demo”, “Calculate ROI”)?
- SEO Friendliness: Presence of meaningful headings, scannable structure, keyword-aligned language.
- Audience Fit & Pain Orientation: Does the messaging address actual B2B pains, metrics, roles, business outcomes?

ADDITIONAL ANALYSIS DIMENSIONS

Include qualitative assessments and recommendations. Identify missing elements, vague wording, generic statements, unclear benefits, weak proof, etc.

OUTPUT FORMAT

You MUST respond in JSON (the format will be enforced during your inference). The following template will be used:

{{
    "criterions": {{
{_SUMMARIZATION_CRITERIONS_DESC}
    }},
    "recommendations": [
        "<recommendation>",
        "<recommendation>",
        "<recommendation>",
        "<recommendation>"
    ] // your helpful recommendations
}}
"""


async def summarize_fragments(llm: LlmAdapter, frags: list[Fragment]):
    input = compile_fragments(frags)

    messages = [
        {"role": "system", "content": SUMMARIZATION_INSTRUCT_PROMPT},
        {"role": "user", "content": input},
    ]

    out = await llm.answer_json(messages, SummarizationOutput.model_json_schema())
    return SummarizationOutput.model_validate(out)
