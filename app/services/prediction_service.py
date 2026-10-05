import pandas as pd
from sqlalchemy.orm import Session

from app.features import add_features
from app.models.prediction import PredictionORM

def predict_and_log(db:Session,raw:dict,model,patient_id:str | None):
    features = add_features(pd.DataFrame([raw]))
    premium =  round(model.predict(features)[0],2)
    
    db.add(PredictionORM(patient_id=patient_id,**raw,predicted_premium=premium))
    db.commit()
    return {'annual_premium':premium}

def history(db:Session,limit:int,offset:int):
    return db.query(PredictionORM).order_by(PredictionORM.created_at.desc()).offset(offset).limit(limit).all()