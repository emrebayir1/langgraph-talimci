from state import GraphState
from typing import Dict, Any
import re
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.prompts import PromptTemplate
from models import qwen_model
from data import db

llm = qwen_model

prompt = PromptTemplate(
    input_variables=["table_info", "input", "top_k"],
    template="""
    You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
    Unless the user specifies in the question a specific language, do not include "language" column in your queries.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question, but always include "platform_id", "title", and "url" in the query. Wrap each column name in double quotes (") to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Available instructional levels are: "All Levels", "Beginner", "Intermediate", "Expert". Only use one of these categories in the query.
    Available languages are: "English", "Turkish". Only use one of these languages in the query.

    Use the following format:

    Question: Question here
    SQLQuery: SQL Query to run
    SQLResult: Result of the SQLQuery
    Answer: Final answer here

    Only use the following tables:
    {table_info}

    Question: {input}
    """
)

write_query = create_sql_query_chain(llm, db, prompt=prompt)
execute_query = QuerySQLDataBaseTool(db=db)
sql_chain = write_query | execute_query

def sql_query_generation(state: GraphState) -> Dict[str, Any]:
    """
    Generates an alternative SQL query based on the user's question, extracts the valid SQL query,
    and executes it to retrieve results.

    Args:
        state (GraphState): Current state of the graph containing the question and initial SQL query.

    Returns:
        Dict[str, Any]: A dictionary containing the generated SQL query and its execution result.
    """
    def extract_sql_query(text: str) -> str:
        """
        Extracts the first SQL query from the provided text.

        Args:
            text (str): The input text containing an SQL query.

        Returns:
            str: The extracted SQL query, or a message indicating no query was found.
        """
        # Regular expression to identify SQL queries
        sql_pattern = re.compile(
            r"SELECT\s+.+?\s+FROM\s+\w+(?:\s+WHERE\s+.+?)?(?:\s+LIMIT\s+\d+)?;",
            re.IGNORECASE | re.DOTALL
        )

        # Search for the first match
        match = sql_pattern.search(text)

        if match:
            return match.group(0).strip()
        else:
            return "No SQL query found in the text."

    question = state["question"]

    query_text = write_query.invoke({
        "question": question
    })

    query = extract_sql_query(query_text)
    result = execute_query.invoke({
        "query": query
    })

    return {"sql_query": query, "sql_result": result}