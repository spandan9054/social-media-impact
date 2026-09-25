import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.Pipeline.predict_pipeline import PredictPipeline


# -----------------------------------
# FastAPI Application
# -----------------------------------

app = FastAPI(
    title="Social Media Impact Prediction API",
    description="API for predicting the impact of social media on life",
    version="1.0.0"
)


# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# Prediction Pipeline
# -----------------------------------

predictor = PredictPipeline()


# -----------------------------------
# Input Data Schema
# -----------------------------------

class SocialMediaData(BaseModel):

    Age: int
    Gender: str
    Academic_Level: str
    Primary_Platform: str

    Daily_Usage_Hours: float
    Weekend_Extra_Hours: float

    Device_Type: str

    Sleep_Duration_Hours: float
    Sleep_Quality_Score: int

    Late_Night_Usage: bool

    Social_Comparison_Frequency: str

    Perceived_Stress_Score: float
    Mental_Health_Index: int
    Academic_Performance_GPA: float


# -----------------------------------
# Prediction Response
# -----------------------------------

class PredictionResponse(BaseModel):

    predicted_classification: str


# -----------------------------------
# Home Endpoint
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": "Social Media Impact Prediction API is running"
    }


# -----------------------------------
# Prediction Endpoint
# -----------------------------------

@app.post("/", response_model=PredictionResponse)
def predict(data: SocialMediaData):

    input_row = pd.DataFrame([{

        "Age": data.Age,
        "Gender": data.Gender,
        "Academic_Level": data.Academic_Level,
        "Primary_Platform": data.Primary_Platform,

        "Daily_Usage_Hours": data.Daily_Usage_Hours,
        "Weekend_Extra_Hours": data.Weekend_Extra_Hours,

        "Device_Type": data.Device_Type,

        "Sleep_Duration_Hours": data.Sleep_Duration_Hours,
        "Sleep_Quality_Score": data.Sleep_Quality_Score,

        "Late_Night_Usage": data.Late_Night_Usage,

        "Social_Comparison_Frequency":
            data.Social_Comparison_Frequency,

        "Perceived_Stress_Score":
            data.Perceived_Stress_Score,

        "Mental_Health_Index":
            data.Mental_Health_Index,

        "Academic_Performance_GPA":
            data.Academic_Performance_GPA
    }])


    prediction = predictor.predict(
        input_row
    )


    return PredictionResponse(
        predicted_classification=prediction
    )