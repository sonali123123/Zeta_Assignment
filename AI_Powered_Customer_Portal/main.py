# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from json import JSONDecoder
from ollama import chat

app = FastAPI()

class ScoreRequest(BaseModel):
    record_id: str
    amount: float

class ScoreResponse(BaseModel):
    score: int
    advice: str

SYSTEM_PROMPT = {
  "role": "system",
  "content": (
    "You are a financial underwriter. Evaluate the requested loan amount and "
    "OUTPUT **ONLY** a JSON object with exactly these two keys:\n"
    '  "score": integer 0–100,\n'
    '  "advice": string (1–2 sentences)\n'
    "Do not include any additional text or formatting."
  )
}

@app.post("/score", response_model=ScoreResponse)
async def score_loan(req: ScoreRequest):
    # Build messages
    messages = [
      SYSTEM_PROMPT,
      {"role":"user", "content": f"Requested amount: ₹{req.amount:.2f}"}
    ]

    # Call the model
    resp = chat(model="llama3.1:8b", messages=messages, stream=False)
    raw = resp.message.content.strip()

    # Attempt to decode just the JSON substring
    decoder = JSONDecoder()
    try:
        obj, idx = decoder.raw_decode(raw)             # find JSON at start or inside
    except json.JSONDecodeError:
        # Fallback: try to locate braces and load
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        if start == -1 or end == 0:
            raise HTTPException(502, detail=f"Invalid JSON from model:\n{raw}")
        obj = json.loads(raw[start:end])               # :contentReference[oaicite:1]{index=1}

    # Validate and return
    try:
        return ScoreResponse(score=int(obj["score"]), advice=obj["advice"])
    except (KeyError, TypeError, ValueError):
        raise HTTPException(502, detail=f"Malformed JSON keys:\n{json.dumps(obj)}")
    
    
@app.get("/health")
async def health():
    return {"status": "ok"}
