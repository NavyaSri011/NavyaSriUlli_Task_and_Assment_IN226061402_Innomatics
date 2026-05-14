from typing import TypedDict

class GraphState(TypedDict):

    query: str
    context: str
    response: str
    route: str