from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from models import llama_model

llm = llama_model

question_prompt = PromptTemplate.from_template(
"""Provide a one-sentence rephrasing of the given question for SQL query generation.

Given: {question}

Rephrased:
"""
)

question_chain = question_prompt | llm | StrOutputParser()
