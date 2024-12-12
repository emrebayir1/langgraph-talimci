from typing import TypedDict

class GraphState(TypedDict):
    """
    Represents the state of a graph.
    Attributes:
        question: User question.
        generation: LLM generation.
        sql_query: SQL query written by LLM.
        sql_result: SQL result.
        language: Langugage of the user question.

    """
    question: str
    generation: str
    sql_query: str
    sql_result: str
    language: str