from langchain_core.prompts import PromptTemplate

scoring_prompt = PromptTemplate(
    input_variables=["match_result"],
    template="""
Based on this matching result:

{match_result}

Assign a FINAL SCORE (0-100).

Rules:
- Be strict
- No assumptions
- Only based on given data

Return JSON ONLY:

{{
  "score": number,
  "reason": "short explanation"
}}
"""
)