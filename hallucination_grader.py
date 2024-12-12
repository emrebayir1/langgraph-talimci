from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from models import qwen_model
from langchain_core.prompts import PromptTemplate

class HallucinationGrader(BaseModel):
    """
    Binary score for hallucination present in the generated answer.
    """

    binary_score: str = Field(
        description="Answer is grounded in the facts. 'yes' or 'no'."
    )

llm = qwen_model

pydantic_parser = PydanticOutputParser(pydantic_object=HallucinationGrader)

hallucination_prompt = PromptTemplate.from_template(
    """
    You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
    Give a binary score 'yes' or 'no'. 
    'yes' means that the answer is grounded.

    LLM Generation: {generation}
    Facts: {sql_result}

    Answer only using expected JSON format.
    Give your response with just one word. All other information will be ignored.

    Expected format:
    {{"binary_score":"yes"}} or {{"binary_score":"no"}}

    Answer:
    """
)

hallucination_chain = hallucination_prompt | llm | pydantic_parser

