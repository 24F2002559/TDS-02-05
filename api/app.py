import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allow all origins (so the browser grader can call us)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your assigned API key (get it from the environment for security)
API_KEY = os.environ.get("API_KEY")
MY_EMAIL = "24f2002559@ds.study.iitm.ac.in"

# Model for incoming events
class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsRequest(BaseModel):
    events: List[Event]

@app.post("/analytics")
async def analytics(request: Request, body: AnalyticsRequest):
    # ---- Authentication ----
    api_key = request.headers.get("X-API-Key")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    # ---- Aggregation ----
    events = body.events
    total_events = len(events)

    # Unique users (using a set)
    unique_users = len({event.user for event in events})

    # Revenue: sum of positive amounts
    revenue = sum(event.amount for event in events if event.amount > 0)

    # Top user: highest total positive amount
    user_totals = {}
    for event in events:
        if event.amount > 0:
            user_totals[event.user] = user_totals.get(event.user, 0) + event.amount
    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    # Return response
    return {
        "email": MY_EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }
