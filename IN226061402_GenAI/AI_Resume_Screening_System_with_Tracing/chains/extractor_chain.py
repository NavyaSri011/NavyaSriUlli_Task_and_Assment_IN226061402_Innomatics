from llm import llm
from prompts.skill_extraction_prompt import skill_extraction_prompt

extractor_chain = skill_extraction_prompt | llm