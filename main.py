import os
import time
import uuid
from typing import Any
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

APP_VERSION = "0.1.0"
MODEL_STATUS = "ready"
MAX_TEXT_CHARS = 512
SERVICE_NAME = "classroom-model-api"
app = FastAPI(title="Classroom Model API v2", version=APP_VERSION)
POSITIVE_WORDS = {"love", "great", "excellent", "fast", "helpful", "good"}
NEGATIVE_WORDS = {"hate", "bad", "slow", "broken", "wrong", "terrible"}
# API_KEY = '1234567890'

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_TEXT_CHARS)
    request_id: str = Field(default=None, max_length=63)
    language: str = Field(default=None, max_length=16)

class PredictResponse(BaseModel):
    request_id: str
    label: str
    score: float = Field(..., ge=0.0, le=1.0)
    model: str
    latency_ms: float = Field(..., ge=0.0)

def run_local_text_model(text: str) -> dict[str, Any]:
    normalized = text.lower()
    if "[model_down]" in normalized:
        raise RuntimeError("simulated local model outage")
    tokens = set(normalized.replace(".", " ").replace(",", " ").split())
    positive_hits = len(tokens & POSITIVE_WORDS)
    negative_hits = len(tokens & NEGATIVE_WORDS)
    raw_score = 0.5 + 0.15 * (positive_hits - negative_hits)
    score = min(0.95, max(0.05, raw_score))
    label = "positive" if score >= 0.5 else "negative"
    return {
        "label": label,
        "score": round(score, 3),
        "model": "demo-sentiment-v1",
    }

@app.middleware("http")
async def add_version_header(request: Request, call_next):
    print('IN THE MIDDLE OF THE REQUEST/RESPONSE')
    response = await call_next(request)
    response.headers["X-Service-Version"] = APP_VERSION

    # simple authorization middleware
    # print(request.url.path)

    # if request.url.path in ['/docs', '/', '/openapi.json']:
    #     pass

    # elif request.headers.get("X-API-KEY") != API_KEY :
    #     raise HTTPException(
    #         status_code=401,
    #         detail="Invalid API key",
    #     )
    
    return response


@app.get("/test", )
async def test():
    return {
        "status": "ok",
        "message": "Hello, World!",
    }


@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "version": APP_VERSION,
        "environment": os.getenv("APP_ENV", "local"),
    }


@app.get("/readyz")
async def readyz():
    if MODEL_STATUS != "ready":
        raise HTTPException(
            status_code=503,
            detail="model dependencies are not ready",
        )
    
    return {
        "status": "ready",
        "model_status": MODEL_STATUS,
        "version": APP_VERSION,
    }


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    started = time.perf_counter()
    request_id = request.request_id or f"req-{uuid.uuid4().hex[:10]}"
    if not request.text.strip():
        raise HTTPException(
            status_code=422,
            detail="text must contain a non-whitespace character",
            )
    
    print(f"predict request_id={request_id} text_len={len(request.text)}")

    try:
     result = run_local_text_model(request.text)
    except RuntimeError:
        raise HTTPException(status_code=503, detail="model is temporarily unavailable")
    except Exception:
        raise HTTPException(status_code=500, detail="prediction failed")

    latency_ms = round((time.perf_counter() - started) * 1000, 3)
    return PredictResponse(
        request_id=request_id,
        latency_ms=latency_ms,
        **result,
    )