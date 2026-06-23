from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True)
    role = Column(String)


class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name = Column(String)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_image = Column(String)
    prediction = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_url = Column(String)
    model_name = Column(String)
    generated_at = Column(DateTime, default=datetime.utcnow)
