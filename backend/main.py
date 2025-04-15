from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import uvicorn

app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev purposes, allows any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    message: str
    personality: str

PERSONALITY_PROMPTS = {
    "friend": "You are a cheerful, funny best friend. Talk like a bubbly buddy and keep things light.",
    "mentor": "You are a wise mentor. Speak in a calm, guiding, and reflective tone.",
    "companion": "You are a loving life partner. Be empathetic, soft-spoken, and caring."
}

@app.post("/ask")
def ask_user(prompt: Prompt):
    full_prompt = f"{PERSONALITY_PROMPTS[prompt.personality]}\n\nUser: {prompt.message}"
    
    result = subprocess.run(
        ["ollama", "run", "llama3.1", full_prompt],
        capture_output=True, text=True
    )
    
    return {"response": result.stdout.strip()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
