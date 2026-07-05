# AiAgent - Autonomous Agent Challenge

An autonomous AI agent built with FastAPI and Ollama for generating business documents.

## Engineering Improvement Implemented: **Tool Calling**
For the mandatory engineering improvement, this project implements native **Tool Calling** (Function Calling) using the Ollama Python SDK. 

**Why it was chosen:** Rather than relying on fragile regex or parsing standard text responses to generate documents, we give the LLM a rigid `generate_docx` tool schema. 
**How it improves the agent:** It forces deterministic execution. The agent is forced to structure its output into strict JSON arguments (`title` and `sections_json_string`), which the FastAPI backend then extracts and passes to `python-docx`. This guarantees that the final document is always formatted correctly and eliminates hallucinated paths.

## Test Inputs for Evaluation

You can test the agent using the following `curl` commands (ensure `uvicorn main:app` and `ollama run llama3.1` are running).

### 1. Standard Business Request
A straightforward request with a clear objective.
```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"request":"Create a meeting minutes document for today'\''s Q3 marketing planning meeting."}'
```

### 2. Complex / Ambiguous Request
A request that requires the agent to make assumptions, structure a multi-step plan, and figure out the missing details autonomously.
```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"request":"I need a technical design document for migrating our legacy on-premise SQL database to AWS RDS. I dont know the specifics, just make reasonable assumptions for the architecture and steps."}'
```
