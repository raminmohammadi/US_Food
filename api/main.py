from fastapi import FastAPI, Response, status, HTTPException
from typing import List, Union
from api.schemas import PredictionRequest, PredictionResponse
from services.predictors import prepare_inference_data
import pandas as pd
from middlewares.logger_middleware import LoggingMiddleware
import lightgbm as lgb
from config.settings import settings
import uvicorn
from services.logger import create_tables
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context to initialize resources at startup and cleanup at shutdown.
    """
    global model

    # Startup logic
    model = lgb.Booster(model_file=settings.MODEL_PATH)
    print("✅ Model loaded successfully.")

    create_tables()
    print("✅ Database tables created successfully.")

    yield

# FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan 
)

# Middleware
app.add_middleware(LoggingMiddleware)

@app.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns basic information if API is running.
    """
    return {"status": "Model API is running"}

@app.get("/status", tags=["Health"])
async def get_status():
    """
    Status endpoint.
    Returns 200 OK if API server is healthy.
    Useful for load balancers and health checks.
    """
    return Response(status_code=status.HTTP_200_OK)

@app.post("/predict", tags=["Prediction"])
async def predict_endpoint(request: Union[PredictionRequest, List[PredictionRequest]]):
    """
    Predict sales based on input features.

    Args:
        request (PredictionRequest or List[PredictionRequest]): Single or multiple prediction inputs.

    Returns:
        PredictionResponse or list of PredictionResponses.
    """
    global model

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet. Please try again later.")


    if isinstance(request, list):
        # Batch input
        features_list = [prepare_inference_data(req) for req in request]
        features_df = pd.DataFrame(features_list)
        preds = model.predict(features_df)

        return [PredictionResponse(sales=int(round(pred))) for pred in preds]
    else:
        # Single input
        features = prepare_inference_data(request)
        features_df = pd.DataFrame([features])
        sales = model.predict(features_df)[0]

        return PredictionResponse(sales=int(sales))


if __name__ == '__main__':
    uvicorn.run("api.main:app", host=settings.HOST, port=settings.PORT, reload=True)