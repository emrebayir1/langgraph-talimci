# Talimci

Talimci is a Python-based project designed to recommend online courses to users based on their questions. By leveraging natural language processing (NLP), Talimci generates SQL queries from user input, executes these queries on a course database, and provides relevant course recommendations.
Features

- **SQL Query Generation**: Transforms user questions into SQL queries.
- **Course Recommendation**: Executes SQL queries to fetch and recommend relevant courses from the database.
- **Dynamic Question Answering**: Provides personalized recommendations based on query results.
- **LLM Integration**: Enhances query generation and interpretation using LLM models.

# Requirements

To run this project, you need the following:

    Python 3.10 or higher
    pandas
    langchain-huggingface
    langchain-community
    langgraph
    streamlit
    deep_translator
    lingua-language-detector
    langchain-groq
    huggingface-hub
    python-dotenv

Install the required dependencies with:
    
    pip install -r requirements.txt

# Setup

Clone this repository to your local machine:

    git clone https://github.com/emrebayir1/talimci.git
    cd talimci

Install the required dependencies:

    pip install -r requirements.txt

Create a .env file in the project root and add the following information:

    HUGGINGFACE_API_KEY = huggingface_api
    GROQ_API_KEY = grog_api

Run the project:

    streamlit run talimci.py

Go to your browser and navigate to the URL provided by Streamlit (e.g., http://localhost:8501). Use the interface to input your questions and receive course recommendations.

# Usage

## Input Questions:
The user inputs a question in natural language (e.g., "What are the best Python courses?").

## SQL Query Generation:
Talimci interprets the question and generates the corresponding SQL query to search for relevant courses.

## Course Recommendation:
The generated SQL query is executed on the course database to fetch matching courses.

## Answer Delivery:
Talimci presents the recommended courses to the user in a clear and concise format.

# Used LLMs and Technologies

## LLMs

**LLama**: Utilized for generating answers to user queries based on the data retrieved from the database.
**Qwen**: Used for writing SQL queries and validating the results of these queries.

## Orchestration

**Langchain**: Manages the interaction between the user, the NLP models, and the database.
**Langgraph**: Structures and optimizes the flow of data and logic within the application.

## Frontend

**Streamlit**: Delivers an intuitive and user-friendly interface for interacting with the application.

# Contributing

Contributions are welcome! To contribute:

Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes and push them to your fork.
Submit a pull request.

For issues and suggestions, please use the GitHub Issues section.

# License

This project is licensed under the MIT License.

# Contact

For questions or suggestions, please contact via GitHub or email: emre.bayir@windowslive.com.
