from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
import joblib
import pandas as pd
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Configure CORS to allow frontend requests
origins = ["*"]  # In production, restrict this to your frontend's domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model pipeline
try:
    model = joblib.load(r"C:\Users\sahil\OneDrive\Naresh IT Class\ML_End_To_End_Projects\Internship Projects\AI Lead Scoring Dashboard Prototype\Backend\model.pkl")
except FileNotFoundError:
    raise RuntimeError("Model file not found. Please run train_model.py first.")

# In-memory storage for leads
scored_leads_db = []

# Pydantic model for input data validation
class LeadInput(BaseModel):
    Email: EmailStr
    CreditScore: int = Field(..., gt=0)
    AgeGroup: str
    FamilyBackground: str
    Income: int = Field(..., gt=0)
    Comments: str = ""

# Re-ranker logic
def re_rank_score(initial_score: int, comments: str) -> int:
    score_adjustment = 0
    lower_comments = comments.lower()
    
    # Positive keywords
    if any(keyword in lower_comments for keyword in ["urgent", "asap", "immediate", "ready"]):
        score_adjustment += 15
    if any(keyword in lower_comments for keyword in ["interested", "quote", "call me"]):
        score_adjustment += 10

    # Negative keywords
    if any(keyword in lower_comments for keyword in ["not interested", "unsubscribe", "spam"]):
        score_adjustment -= 20
    if any(keyword in lower_comments for keyword in ["wrong number", "not me", "mistake"]):
        score_adjustment -= 15

    reranked_score = initial_score + score_adjustment
    # Cap the score between 0 and 100
    return max(0, min(100, reranked_score))


@app.post("/score")
def score_lead(lead: LeadInput):
    try:
        # Create a DataFrame from the input data
        input_data = pd.DataFrame([lead.dict(exclude={'Comments', 'Email'})])
        print("testing", input_data)
        
        # Predict probability of high intent (class 1)
        # model.predict_proba returns [[prob_class_0, prob_class_1]]
        intent_probability = model.predict_proba(input_data)[:, 1][0]
        
        # Scale probability to an initial score of 0-100
        initial_score = int(np.round(intent_probability * 100))
        
        # Apply the rule-based re-ranker
        reranked_score = re_rank_score(initial_score, lead.Comments)
        
        # Store the result
        result = {
            "Email": lead.Email,
            "InitialScore": initial_score,
            "RerankedScore": reranked_score,
            "Comments": lead.Comments
        }
        scored_leads_db.append(result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leads")
def get_leads():
    # Return all scored leads
    return scored_leads_db


# To run the app: uvicorn main:app --reload --host 0.0.0.0 --port 800