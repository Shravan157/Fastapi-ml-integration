from sqlalchemy import Integer,String,Float,ForeignKey,Boolean
from sqlalchemy.orm import Mapped,mapped_column 
from app.database import Base
from datetime import date

class PredictionORM(Base):
    __tablename__ = "predictions"
    
    id : Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    patient_id : Mapped[str | None] = mapped_column(String,ForeignKey("patients.patient_id",ondelete='SET NULL'),nullable=True)
    age : Mapped[int] = mapped_column(Integer)
    weight : Mapped[float] = mapped_column(Float)
    height : Mapped[float] = mapped_column(Float)
    smoker : Mapped[bool] = mapped_column(Boolean)
    children : Mapped[int] = mapped_column(Integer)
    predicted_premium : Mapped[float] = mapped_column(Float)
    created_at : Mapped[date] = mapped_column(default=date.today)
    