from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.retrieval import search_assessments
from app.chatbot import generate_response

app = FastAPI(
    title="SHL AI Assessment Recommender",
    description="AI-powered SHL Assessment Recommendation API",
    version="1.0.0"
)


# ---------------- Request Models ---------------- #

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# ---------------- Home Endpoint ---------------- #

@app.get("/")
def home():
    return {
        "message": "Welcome to the SHL AI Assessment Recommendation API",
        "status": "running",
        "health": "/health",
        "documentation": "/docs"
    }


# ---------------- Health Endpoint ---------------- #

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# ---------------- Chat Endpoint ---------------- #

@app.post("/chat")
def chat(request: ChatRequest):

    # Validate request
    if not request.messages:
        raise HTTPException(
            status_code=400,
            detail="No messages provided."
        )

    # Get latest user message
    query = request.messages[-1].content.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    try:

        # Retrieve assessments
        results = search_assessments(query)

        # Generate Gemini response
        answer = generate_response(query, results)

        # -------- Clarification Detection -------- #

        clarification_phrases = [
            "what role are you hiring for",
            "what role",
            "what is the experience level",
            "experience level",
            "could you tell me",
            "could you please provide",
            "can you provide more information",
            "before i recommend",
            "i need a little more information",
            "to help me recommend",
            "to better recommend",
            "please provide more information"
        ]

        is_clarification = any(
            phrase in answer.lower()
            for phrase in clarification_phrases
        )

        # If clarification is needed,
        # DO NOT return recommendations yet.
        if is_clarification:
            return {
                "reply": answer,
                "recommendations": [],
                "end_of_conversation": False
            }

        # -------- Recommendation Response -------- #

        recommendations = []

        for item in results:
            recommendations.append({
                "name": item.get("name", ""),
                "url": item.get("url", "")
            })

        return {
            "reply": answer,
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )