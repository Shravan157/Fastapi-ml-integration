from fastapi import APIRouter, Path, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import patient_service
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter(tags=["Patient Endpoints"], prefix="/patients")


@router.get("/", response_model=list[PatientResponse])
def read_all_patients(
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return patient_service.get_all(db, limit, offset)


@router.get("/sort", response_model=list[PatientResponse])
def sort_patients(
    sort_by: str = Query(examples="height"),
    order: str = Query(default="asc", examples="asc"),
    db: Session = Depends(get_db),
):
    VALID_SORT_OPTIONS = ["height", "weight", "age"]
    if sort_by not in VALID_SORT_OPTIONS:
        raise HTTPException(status_code=400, detail=f"select from {VALID_SORT_OPTIONS}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="select from ['asc','desc']")
    return patient_service.sort(db, sort_by, order)


@router.post("/create-patient", response_model=PatientResponse, status_code=201)
def create_patient_record(patient: PatientCreate, db: Session = Depends(get_db)):
    if patient_service.get_by_id(db, patient.patient_id):
        raise HTTPException(status_code=409, detail="patient with same patient_id already exists")
    return patient_service.create(db, patient)


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(update: PatientUpdate, patient_id: str = Path(..., example="P001"), db: Session = Depends(get_db)):
    updated = patient_service.update(db, patient_id, update)
    if not updated:
        raise HTTPException(status_code=404, detail="patient not found")
    return updated


@router.delete("/{patient_id}")
def delete_patient_record(patient_id: str = Path(...), db: Session = Depends(get_db)):
    deleted = patient_service.delete(db, patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="patient not found")
    return {"content": "patient data deleted"}


@router.get("/{patient_id}", response_model=PatientResponse)
def get_by_patientID(patient_id: str = Path(..., examples=["P001", "P002"]), db: Session = Depends(get_db)):
    patient = patient_service.get_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient