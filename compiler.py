from hallucination_grader import hallucination_chain
from answer_grader import answer_chain
from answer_generate import answer_generation
from sql_query_generate import sql_query_generation
from alternative_sql_query_generate import alternative_sql_query_generation
from translate_text import translate_text
from language_detector import detect_language
from transform_question import transform_question
from state import GraphState
from langgraph.graph import END, StateGraph, START

# CONDITIONAL EDGE FUNCTIONS
def generation_check(state: GraphState):
    """
    Determines whether the generation is grounded and answers user's question.
    Attributes:
        state (dict): Current state of the graph.
    Returns:
        str: Next node to call.
    """
    question = state["question"]
    sql_result = state["sql_result"]
    generation = state["generation"]
    score = hallucination_chain.invoke({"generation":generation, "sql_result":sql_result})
    grade = score.binary_score
    if grade == "yes":
        score = answer_chain.invoke({"question": question, "answer": generation})
        grade = score.binary_score
        if grade == "yes":
            return "useful"
        else:
            return "not_useful"
    else:
        return "not_supported"

def sql_query_result_check(state: GraphState):
    """
    Checks if the SQL query result is empty or an error.
    Attributes:
        state (dict): Current state of the graph.
    Returns:
        str: Next node to call.
    """
    sql_result = state.get("sql_result")  # state.get() ile hata kontrolü yapıyoruz
    if sql_result is None or sql_result == "" or isinstance(sql_result,
                                                            str) and "No SQL query found in the text" in sql_result:
        return "empty_sql_result"
    else:
        return "not_empty_sql_result"

workflow = StateGraph(GraphState)

# NODES
workflow.add_node("sql_query_generator", sql_query_generation)
workflow.add_node("final_sql_query_generator", sql_query_generation)
workflow.add_node("alternative_sql_query_generator", alternative_sql_query_generation)
workflow.add_node("answer_generate", answer_generation)
workflow.add_node("final_answer_generate", answer_generation)
workflow.add_node("translate_text", translate_text)
workflow.add_node("transform_question", transform_question)
workflow.add_node("detect_language", detect_language)

# EDGES
workflow.add_edge(START, "detect_language")
workflow.add_edge("detect_language", "sql_query_generator")
workflow.add_conditional_edges("sql_query_generator", sql_query_result_check,
                               {
                                   "empty_sql_result": "alternative_sql_query_generator",
                                    "not_empty_sql_result": "answer_generate"}
                               )
workflow.add_conditional_edges("alternative_sql_query_generator", sql_query_result_check,
                  {"empty_sql_result": "transform_question",
                   "not_empty_sql_result": "answer_generate"
                  })
workflow.add_conditional_edges("answer_generate", generation_check,
    {
        "useful": END,
        "not_useful": "transform_question",
        "not_supported" : "final_answer_generate"
    }
)
workflow.add_edge("transform_question", "final_sql_query_generator")
workflow.add_conditional_edges("final_sql_query_generator", sql_query_result_check,
                               {
                                   "empty_sql_result":"translate_text",
                                   "not_empty_sql_result":"final_answer_generate"
                               }
                               )
workflow.add_conditional_edges("final_answer_generate", generation_check,
    {
        "useful": END,
        "not_useful": "translate_text",
        "not_supported" : "translate_text"
    }
)
workflow.add_edge("translate_text", END)
app = workflow.compile()

def process_question(input_question):
    """
    Process the input question through the `app.invoke` function and return the final generation.

    Args:
        input_question (str): The question input provided by the user.

    Returns:
        str: The final generation result, or an error message if not found.
    """
    inputs = {"question": input_question}

    output = app.invoke(inputs)  # Assuming invoke returns a dictionary-like structure

    # Ensure the output is a dictionary and contains the 'generation' key
    if isinstance(output, dict) and "generation" in output:
        return output["generation"]
    else:
        raise KeyError("The 'generation' key is missing in the output or output is not a dictionary.")
