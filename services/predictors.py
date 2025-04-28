from datetime import datetime
from api.schemas import PredictionRequest

def prepare_inference_data(inference_data: PredictionRequest) -> dict:
    """
    Prepares inference data for model prediction.

    Args:
        inference_data (PredictionRequest): Input data with fields like 'date', 'item', 'store'.

    Returns:
        dict: Processed feature dictionary ready for model prediction.
    """
    # Extract fields safely
    if not hasattr(inference_data, 'date') or inference_data.date is None:
        raise ValueError("Input data must contain 'date' field.")

    # Parse date
    if isinstance(inference_data.date, str):
        try:
            parsed_date = datetime.strptime(inference_data.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in format 'YYYY-MM-DD'.")
    elif isinstance(inference_data.date, datetime):
        parsed_date = inference_data.date
    else:
        raise TypeError("Invalid type for 'date'. Must be string or datetime.")

    # Feature engineering
    month = parsed_date.month
    dayofweek = parsed_date.weekday()  # Monday=0
    year = parsed_date.year

    # Construct feature dictionary
    features = {
        "store": inference_data.store,
        "item": inference_data.item,
        "month": month,
        "dayofweek": dayofweek,
        "year": year
    }

    return features