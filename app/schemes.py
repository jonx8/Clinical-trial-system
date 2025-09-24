from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, EmailStr, ConfigDict

from app.models import Gender, PatientStatus, VisitType


class PatientBase(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    birth_date: datetime = Field(..., description="Date of birth")
    gender: Gender = Field(..., description="Patient gender")
    status: PatientStatus = Field(..., description="Patient status in study")
    email: Optional[EmailStr] = Field(None, description="Patient email address")
    phone: Optional[str] = Field(None, max_length=20, description="Patient phone number")


class Patient(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_code: str
    medical_history: Optional[Dict[str, Any]]
    baseline_data: Optional[Dict[str, Any]]
    enrollment_date: Optional[datetime]
    completion_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]


class PatientSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_code: str
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Gender
    status: PatientStatus


class PatientCreate(PatientBase):
    patient_code: str = Field(..., min_length=1, max_length=50, description="Unique patient code")
    medical_history: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Medical history")
    baseline_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Baseline data")
    enrollment_date: Optional[datetime] = Field(..., description="Enrollment date")
    completion_date: Optional[datetime] = Field(..., description="Completion date")


class PatientUpdate(PatientBase):
    medical_history: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Medical history")
    baseline_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Baseline data")
    enrollment_date: Optional[datetime] = Field(..., description="Enrollment date")
    completion_date: Optional[datetime] = Field(..., description="Completion date")


class VisitBase(BaseModel):
    visit_date: datetime = Field(..., description="Visit date")
    visit_type: VisitType = Field(..., description="Visit type")
    notes: Optional[str] = Field(None, description="Notes about visit")


class VisitCreate(VisitBase):
    pass


class VisitUpdate(VisitBase):
    pass


class Visit(VisitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    created_at: datetime
    updated_at: Optional[datetime]

class MeasurementBase(BaseModel):
    metric_name: str = Field(..., description="Metric name")
    metric_code: Optional[str] = Field(None, description="Metric code")
    value_numeric: Optional[float] = None
    value_text: Optional[str] = None
    value_json: Optional[Dict[str, Any]] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    measured_at: Optional[datetime] = None


class MeasurementCreate(MeasurementBase):
    visit_id: Optional[int] = Field(None, description="Visit ID if applicable")


class MeasurementUpdate(MeasurementBase):
    pass


class Measurement(MeasurementBase):
    id: int
    patient_id: int
    visit_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
