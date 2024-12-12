from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from models import qwen_model
from langchain_core.prompts import PromptTemplate

class AnswerGrader(BaseModel):
    """
    Binary score for LLM answer adresses the user's question.
    """

    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )


llm = qwen_model

pydantic_parser = PydanticOutputParser(pydantic_object=AnswerGrader)

answer_prompt = PromptTemplate.from_template(
    """
    You are a grader assessing whether an answer addresses / resolves a question.
    Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."

    Question: {question}
    Answer: {answer}

    Answer only using expected JSON format.
    Give your response with just one word. All other information will be ignored.

    Expected format:
    {{"binary_score":"yes"}} or {{"binary_score":"no"}}

    Answer:
    """
)

answer_chain = answer_prompt | llm | pydantic_parser