from langgraph.graph import StateGraph, END

from workflow.state import GraphState
from workflow.nodes import (
    process_query,
    human_node,
    output_node
)

from workflow.router import route_query

def build_graph(vectordb):

    workflow = StateGraph(GraphState)

    workflow.add_node(
        "process",
        lambda state: process_query(state, vectordb)
    )

    workflow.add_node(
        "human",
        human_node
    )

    workflow.add_node(
        "output",
        output_node
    )

    workflow.set_entry_point("process")

    workflow.add_conditional_edges(
        "process",
        route_query,
        {
            "human": "human",
            "answer": "output"
        }
    )

    workflow.add_edge("human", "output")

    workflow.add_edge("output", END)

    app = workflow.compile()

    return app