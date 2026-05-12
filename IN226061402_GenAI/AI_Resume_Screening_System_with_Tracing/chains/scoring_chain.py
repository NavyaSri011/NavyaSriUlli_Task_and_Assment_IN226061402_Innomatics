from llm import llm
from prompts.scoring_prompt import scoring_prompt

scoring_chain = scoring_prompt | llm