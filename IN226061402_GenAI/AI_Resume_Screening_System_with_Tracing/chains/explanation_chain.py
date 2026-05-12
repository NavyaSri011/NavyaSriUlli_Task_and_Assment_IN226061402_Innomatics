from llm import llm
from prompts.explanation_prompt import explanation_prompt

explanation_chain = explanation_prompt | llm