def route_query(state):

    response = state["response"]

    escalation_conditions = [
        "ESCALATE_TO_HUMAN",
        "not enough information",
        "cannot answer",
        "do not know"
    ]

    for item in escalation_conditions:

        if item.lower() in response.lower():

            return "human"

    return "answer"