from data import db, table_info
from state import GraphState
from typing import Dict, Any
import re
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from models import qwen_model

llm = qwen_model
db = db
table_info = table_info

prompt = PromptTemplate.from_template(
    """
    You are a SQLite expert and a problem solver. Based on the user's criteria, you write efficient and correct SQL queries. If a query does not return results, you rewrite it using a different approach to achieve the same objective and retrieve relevant data.
    By default, queries should return a maximum of 5 rows unless specified otherwise. Use the LIMIT clause to enforce this.

    Available Tables and Their Structures:
    {table_info}

    Available Instructional Levels:
    "All Levels", "Beginner", "Intermediate", "Expert"

    Available Languages:
    "Turkish", "English"

    Format:

    Initial Query: The first SQL query based on the user's input
    Initial Result: The result of the initial query (e.g., no data returned)
    Revised Query: A modified query designed to achieve the same objective while ensuring results are retrieved
    Revised Result: The output of the revised query
    Answer: Final explanation and solution

    Example:

    Initial Query: {sql_query}
    Initial Result: No data returned.
    Revised Query:
    """
)

write_alternative_query = prompt | llm | StrOutputParser()
execute_alternative_query = QuerySQLDataBaseTool(db=db)
alternative_sql_chain = write_alternative_query | execute_alternative_query

def alternative_sql_query_generation(state: GraphState) -> Dict[str, Any]:
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

    sql_query = state["sql_query"]

    query_text = write_alternative_query.invoke({
        "table_info": table_info,
        "sql_query": sql_query
    })

    query = extract_sql_query(query_text)

    result = execute_alternative_query.invoke({
        "query": query
    })

    return {"sql_query": query, "sql_result": result}