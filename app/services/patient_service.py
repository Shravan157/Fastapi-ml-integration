from sqlalchemy.orm import Session
from app.models.patient import PatientORM
from app.schemas.patient import PatientCreate, PatientUpdate

def get_all(db: Session, limit: int, offset: int):
    return db.query(PatientORM).offset(offset).limit(limit).all()

def get_by_id(db: Session, patient_id: str):
    return db.query(PatientORM).filter(PatientORM.patient_id == patient_id).first()

def create(db: Session, patient: PatientCreate):
    db_patient = PatientORM(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def update(db: Session, patient_id: str, update_data: PatientUpdate):
    db_patient = get_by_id(db, patient_id)
    if not db_patient:
        return None
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_patient, field, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete(db: Session, patient_id: str):
    db_patient = get_by_id(db, patient_id)
    if not db_patient:
        return None
    db.delete(db_patient)
    db.commit()
    return db_patient

def sort(db: Session, sort_by: str, order: str):
    columns = {
        "height": PatientORM.height,
        "weight": PatientORM.weight,
        "age": PatientORM.age,
    }
    column = columns[sort_by]
    column = column.desc() if order == "desc" else column.asc()
    return db.query(PatientORM).order_by(column).all()