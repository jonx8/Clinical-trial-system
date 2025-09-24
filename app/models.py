from enum import Enum

from sqlalchemy import Column, BigInteger, String, DateTime, func, ForeignKey, JSON, Text, Float
from sqlalchemy.orm import relationship

from app.database import Base


class Gender(str, Enum):
    Male = "Male"
    Female = "Female"
    OTHER = "Other"
    UNKNOWN = "Unknown"


class PatientStatus(str, Enum):
    SCREENING = "screening"
    ENROLLED = "enrolled"
    ACTIVE = "active"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"


class VisitType(str, Enum):
    SCREENING = "screening"
    BASELINE = "baseline"
    TREATMENT = "treatment"
    FOLLOW_UP = "follow_up"


class UserRole(str, Enum):
    ADMIN = "admin"
    RESEARCHER = "researcher"
    VIEWER = "viewer"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)

    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    full_name = Column(String(100), nullable=False)
    role = Column(String(50))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PatientModel(Base):
    __tablename__ = "patients"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    patient_code = Column(String(50), index=True, unique=True, nullable=False)

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    birth_date = Column(DateTime(timezone=True), nullable=False)
    gender = Column(String(20), nullable=False)

    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)

    medical_history = Column(JSON, default=dict())
    baseline_data = Column(JSON, default=dict())

    status = Column(String(20), default=PatientStatus.SCREENING.value)
    enrollment_date = Column(DateTime(timezone=True), nullable=True)
    completion_date = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    visits = relationship("VisitModel", back_populates="patient", cascade="all, delete-orphan")
    measurements = relationship("MeasurementModel", back_populates="patient", cascade="all, delete-orphan")


class VisitModel(Base):
    __tablename__ = "visits"

    id = Column(BigInteger, primary_key=True, index=True)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)

    visit_date = Column(DateTime(timezone=True), nullable=False)
    visit_type = Column(String(50), nullable=False)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    patient = relationship("PatientModel", back_populates="visits")
    measurements = relationship("MeasurementModel", back_populates="visit", cascade="all, delete-orphan")


class MeasurementModel(Base):
    __tablename__ = "measurements"

    id = Column(BigInteger, primary_key=True, index=True)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)
    visit_id = Column(BigInteger, ForeignKey("visits.id"), nullable=True)

    metric_name = Column(String(100), nullable=False)
    metric_code = Column(String(50), nullable=True)

    value_numeric = Column(Float, nullable=True)
    value_text = Column(Text, nullable=True)
    value_json = Column(JSON, nullable=True)

    unit = Column(String(50), nullable=True)

    notes = Column(Text, nullable=True)
    measured_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    patient = relationship("PatientModel", back_populates="measurements")
    visit = relationship("VisitModel", back_populates="measurements")
