from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_groq import ChatGroq
import os

load_dotenv()

huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

qwen_model = HuggingFaceEndpoint(
    repo_id="Qwen/QwQ-32B-Preview",
    temperature=0.1,
    huggingfacehub_api_token=huggingface_api_key,
    model_kwargs={
        "max_length": 128}
)

llama_model = ChatGroq(
    temperature=0.7,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)