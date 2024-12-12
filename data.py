from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os

load_dotenv()

db_path = ("courses.db")

db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
table_info = db.get_table_info()
