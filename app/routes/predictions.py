from fastapi import APIRouter,Depends,Query,Path,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import prediction_service,patient_service
from app.schemas.prediction import PatientPredictionInput,PredictionHistory,PredictionInput,PredictionOutput
from app.config import MODEL_PATH
import joblib
from typing import List

router = APIRouter(
    prefix='/predictions',
    tags=['Prediction Endpoints']
)

model = joblib.load(MODEL_PATH)

@router.post('/premium',response_model=PredictionOutput)
def predict_premium(
    user_input : PredictionInput,
    db:Session = Depends(get_db),
):
    return prediction_service.predict_and_log(db,model=model,raw=user_input.model_dump(),patient_id=None)

@router.post('/patients/{patient_id}',response_model=PredictionOutput)
def predict_patient_premium(
    additional_details : PatientPredictionInput,
    db : Session = Depends(get_db),
    patient_id : str = Path(...,description='id of the patient',examples=['P001']),
):
    
    patient = patient_service.get_by_id(db,patient_id)
    
    if not patient:
        raise HTTPException(status_code=404,detail='patient not found')
    
    if not 18 <= patient.age <= 64:
        raise HTTPException(status_code=422, detail="Model supports ages 18-64 only")
    raw = {
        "age" : patient.age,
        "weight" : patient.weight,
        "height" : patient.height,
        "smoker" : additional_details.smoker,
        "children" : additional_details.children
    }
    
    return prediction_service.predict_and_log(db,raw,model,patient_id)
    
@router.get('/history',response_model=List[PredictionHistory])
def get_history(
    db:Session = Depends(get_db),
    limit : int = Query(default=10,ge=0,le=50),
    offset : int = Query(default=0,ge=0),
):
    
    return prediction_service.history(db,limit,offset)