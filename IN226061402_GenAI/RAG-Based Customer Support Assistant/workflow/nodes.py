import os
import requests

from dotenv import load_dotenv

from retrieval.retriever import retrieve_context
from prompts.support_prompt import SUPPORT_PROMPT
from hitl.escalation import escalate_to_human

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

def process_query(state, vectordb):

    query = state["query"]

    context = retrieve_context(vectordb, query)

    if len(context.strip()) < 30:

        return {
            "query": query,
            "context": context,
            "response": "ESCALATE_TO_HUMAN"
        }

    prompt = SUPPORT_PROMPT.format(
        context=context,
        query=query
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    try:

        response = requests.post(
            LM_STUDIO_URL,
            json=payload
        )

        answer = response.json()["choices"][0]["message"]["content"]

    except Exception:

        answer = "ESCALATE_TO_HUMAN"

    return {
        "query": query,
        "context": context,
        "response": answer
    }

def human_node(state):

    query = state["query"]

    human_response = escalate_to_human(query)

    return {
        "query": query,
        "context": state["context"],
        "response": human_response
    }

def output_node(state):

    return state