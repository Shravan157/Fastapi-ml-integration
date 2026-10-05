from pydantic import BaseModel,Field,computed_field,ConfigDict
from typing import Literal,Optional

class PatientBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    city: str = Field(min_length=2, max_length=20)
    age: int = Field(gt=0, le=120)
    gender: Literal['male', 'female', 'other']
    height: float = Field(gt=0, le=2.5, description="Height in meters")
    weight: float = Field(gt=0, le=300, description="Weight in kilograms")
    
    
class PatientCreate(PatientBase):
    patient_id : str = Field(description='id of the patient')


class PatientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    city: Optional[str] = Field(None, min_length=2, max_length=20)
    age: Optional[int] = Field(None, gt=0, le=120)
    gender: Optional[Literal['male', 'female', 'other']] = None
    height: Optional[float] = Field(None, gt=0, le=2.5)
    weight: Optional[float] = Field(None, gt=0, le=300)
    

class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    patient_id: str

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        return "Obese"