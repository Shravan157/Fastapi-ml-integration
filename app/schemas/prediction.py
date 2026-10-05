from datetime import date
from pydantic import BaseModel, Field, ConfigDict

class PatientPredictionInput(BaseModel):
    """If a user has an account already, they only pass children and smoker fields."""
    smoker: bool
    children: int = Field(ge=0, le=10) 
    
class PredictionInput(PatientPredictionInput):
    """If the patient does not have an account, accept all features."""
    age: int = Field(gt=0, le=120)
    height: float = Field(gt=0, le=2.5, description='meters')
    weight: float = Field(gt=0, le=300, description='kg')
    
class PredictionOutput(BaseModel):
    annual_premium: float

class PredictionHistory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(gt=0)
    patient_id: str | None
    age: int 
    weight: float 
    height: float 
    smoker: bool 
    children: int 
    predicted_premium: float 
    created_at: date 
