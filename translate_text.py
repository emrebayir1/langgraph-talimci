from deep_translator import GoogleTranslator
from state import GraphState
from typing import Dict, Any

def translate_text(state:GraphState) -> Dict[str,Any]:
    """
    Translate pre defined text to user's language.
    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates generation key with translation.
    """
    question = state["question"]
    text = "I couldn't find the details you're searching for. Can you rephrase or ask about something else?"
    language_code = state["language"]
    translation = GoogleTranslator(source="en", target=language_code).translate(text)
    return {"question":question, "generation":translation}

