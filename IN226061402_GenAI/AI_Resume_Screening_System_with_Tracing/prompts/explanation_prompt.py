from langchain_core.prompts import PromptTemplate

explanation_prompt = PromptTemplate(
    input_variables=["score", "match_result"],
    template="""
You are an AI recruiter.

Score: {score}
Match Details: {match_result}

Explain:
- Strengths
- Weaknesses
- Why this score was given
"""
)