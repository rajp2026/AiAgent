from fastapi import FastAPI
from pydantic import BaseModel
from agent import process_request

app = FastAPI(title="Autonomous AI Agent API")

class AgentRequest(BaseModel):
    request: str

class AgentResponse(BaseModel):
    agent_message: str
    document_url: str | None = None

@app.post("/agent", response_model=AgentResponse)
async def handle_agent_request(payload: AgentRequest):
    # Call the core agent logic
    result = process_request(payload.request)
    
    return AgentResponse(
        agent_message=result["agent_message"],
        document_url=result.get("document_url")
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
