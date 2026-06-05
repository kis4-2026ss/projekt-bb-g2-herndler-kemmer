[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/5deAuAXI)

# KIS4-AI-Project - an AI-Powered Query System

## Goal of the Project
- What is the high-level goal of your project and how to validate it?

  In our SWK4 Project we created a REST Api for a Restaurant Service.

  The goal of this project is to allow non-technical persons to easily query the database for data
  by asking a LLM and receive the output in a understandable natural language format.

  Validation will be done by:
    - Comparing generated answers with actual SQL query results
    - Testing usability with non-technical users
 
  We will analyze the correctness of the output, based on the used LLM.

- What system, feature or workflow will you develop or analyze?

  We plan on implementing a RAG system that connects the database and an LLM. 

- How does AI assistance contribute to the development process?
  (which tools or models at which stages of the development are used?)
  
  We will use AI to research on the topic, then decide on what RAG/LLM to use.
  We will use LMStudio with a local llm aswell as a OpenAPI compatible provider.
  Code will be in Python and IDE is Visual Studio Code.
  
- Provide development/architecture diagram illustrating the project idea
  (software components, roles and use of AI tools, interaction between human and AI)
  
  The system consists of a web frontend where users input natural language queries.
  These queries are sent to a REST API, processed in a RAG pipeline, and answered using an LLM
  based on data retrieved from a SQL database.
  
  Flow:
  User → Web Frontend → REST API → RAG Pipeline → (SQL Database + LLM) → Answer → Web Frontend

  See Diagram in docs Folder.

## Project plan
- Break down the project into tasks, including team-internal deadlines
  - Research
  - Docker container for database
  - Backend RAG/LLM implementation
  - Testing for correct results
  - Frontend

## Teamwork and responsibilities
  - Research - Both
  - RAG - Christoph
  - LLM - Both
  - Testing - Both
  - Frontend - Lucas
