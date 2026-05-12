from llm import llm
from prompts.matching_prompt import matching_prompt

matcher_chain = matching_prompt | llm