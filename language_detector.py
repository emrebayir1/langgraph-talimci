from state import GraphState
from lingua import Language, LanguageDetectorBuilder
from typing import Dict, Any

# Most used languages are selected for better performance.
langs = [Language.ENGLISH, Language.CHINESE, Language.HINDI, Language.TURKISH, Language.SPANISH, Language.FRENCH, Language.ARABIC, Language.BENGALI, Language.PORTUGUESE, Language.RUSSIAN, Language.URDU, Language.INDONESIAN, Language.GERMAN, Language.JAPANESE, Language.VIETNAMESE, Language.TAGALOG, Language.KOREAN, Language.PERSIAN]
detector = LanguageDetectorBuilder.from_languages(*langs).build()

def detect_language(state:GraphState) -> Dict[str,Any]:
    """
    Detect the language of user question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates language key with users language.
    """
    question = state["question"]
    language = detector.detect_language_of(question)
    language = str(language.iso_code_639_1.name).lower()
    return {"question":question, "language":language}