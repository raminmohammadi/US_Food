from pydantic import BaseModel
from typing import List, Optional

class PredictionRequest(BaseModel):
    date: str
    store: int
    item: int

class PredictionResponse(BaseModel):
    sales: int

