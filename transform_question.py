from question_rewriter import question_chain
from state import GraphState
from typing import Dict, Any

def transform_question(state: GraphState) -> Dict[str, Any]:
    """
    Transform the question to produce a better query.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """

    question = state["question"]
    better_question = question_chain.invoke({"question": question})
    return {"question": better_question}