from sqlalchemy import String,Float,Integer
from sqlalchemy.orm import Mapped,mapped_column
from app.database import Base

class PatientORM(Base):
    __tablename__ = "patients"
    patient_id: Mapped[str] = mapped_column(String,primary_key=True) # patient_id is a type of Mapped db column and 
    name : Mapped[str] = mapped_column(String(50))
    city : Mapped[str] = mapped_column(String(20))
    age : Mapped[int] = mapped_column(Integer)
    gender : Mapped[str] = mapped_column(String(10))
    height : Mapped[float] = mapped_column(Float)
    weight : Mapped[float] = mapped_column(Float)