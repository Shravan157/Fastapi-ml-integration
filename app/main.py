from fastapi import FastAPI
from app.routes import generals,predictions,patients
from app.database import Base,engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(generals.router)
app.include_router(predictions.router)
app.include_router(patients.router)