from langchain_core.prompts import PromptTemplate

skill_extraction_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
You are an expert HR assistant.

Extract structured information ONLY from the resume below.

Resume:
{resume}

Return JSON with:
- skills
- experience
- tools

Rules:
- Do NOT assume missing information
- Do NOT add external knowledge
"""
)