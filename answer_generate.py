from state import GraphState
from typing import Any, Dict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from models import llama_model

llm = llama_model

generation_prompt = PromptTemplate.from_template(
    """You are a educational assistant. Your job is to recommend relevant courses based on user question.
    Given the following user question and corresponding SQL result, recommend the user relevant courses.
    Answer the questions concisely.
    If exists in the SQL Result, always include course title and url in your answers.
    Directly answer the user question.
    Your answer's language should be {language}

    Question: {question}
    SQL Result: {result}
    Answer: 
"""
)

generation_chain = generation_prompt | llm | StrOutputParser()

def answer_generation(state:GraphState) -> Dict[str, Any]:

    """
    Generates course recommendations based on a user’s question, SQL query, and result, providing relevant course titles and URLs when available.
    Attributes:
        state (dict): Current state of the graph.
    Returns:
        state (dict): LLM generated answer
    """

    question = state["question"]
    query = state["sql_query"]
    result = state["sql_result"]
    language = state["language"]

    generation = generation_chain.invoke(
        {"question": question, "query":query, "result":result, "language":language}
    )

    return {"question": question, "query":query, "result":result, "generation":generation, "language":language}
