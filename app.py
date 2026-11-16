from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import asyncio
import random

app = FastAPI(title="ParallelPrompt Demo API", version="0.1.0")


@app.get("/health")
async def health() -> Dict[str, str]:
    """Simple health check."""
    return {"status": "ok"}


class PromptRequest(BaseModel):
    """Incoming request payload."""
    prompt: str = Field(..., min_length=1, description="User prompt to send to both models")
    max_tokens: int = Field(150, ge=1, le=1024, description="Maximum tokens for each response")
    temperature: float = Field(0.7, ge=0.0, le=1.0, description="Sampling temperature")


class ModelResponse(BaseModel):
    """Individual model response."""
    model: str
    response: str
    tokens_used: int


class ParallelResponse(BaseModel):
    """Combined response from both models."""
    prompt: str
    results: List[ModelResponse]


async def mock_claude(prompt: str, max_tokens: int, temperature: float) -> ModelResponse:
    """Simulate a Claude response."""
    await asyncio.sleep(random.uniform(0.1, 0.3))  # pretend network latency
    text = f"Claude says: {prompt[:max_tokens//2]}..."
    return ModelResponse(
        model="claude",
        response=text,
        tokens_used=min(len(text.split()), max_tokens),
    )


async def mock_codex(prompt: str, max_tokens: int, temperature: float) -> ModelResponse:
    """Simulate a Codex response."""
    await asyncio.sleep(random.uniform(0.1, 0.3))
    text = f"Codex suggests: {prompt[:max_tokens//2]}..."
    return ModelResponse(
        model="codex",
        response=text,
        tokens_used=min(len(text.split()), max_tokens),
    )


@app.post("/compare", response_model=ParallelResponse)
async def compare_prompt(request: PromptRequest) -> ParallelResponse:
    """
    Send the same prompt to Claude and Codex (mocked) and return side‑by‑side results.
    """
    try:
        claude_task = asyncio.create_task(
            mock_claude(request.prompt, request.max_tokens, request.temperature)
        )
        codex_task = asyncio.create_task(
            mock_codex(request.prompt, request.max_tokens, request.temperature)
        )
        results = await asyncio.gather(claude_task, codex_task)
        return ParallelResponse(prompt=request.prompt, results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
