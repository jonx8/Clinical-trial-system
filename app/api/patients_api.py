from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models import PatientStatus
from app.schemes import PatientSummary, Patient, PatientCreate, PatientUpdate
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("", response_model=List[PatientSummary])
async def get_patients(skip: int = 0, limit: int = 50,
                       patient_service: PatientService = Depends()):
    patients = await patient_service.list_patients(skip, limit)
    return [PatientSummary.model_validate(p) for p in patients]


@router.get("/{patient_id}", response_model=Patient)
async def get_patient_by_id(patient_id: int,
                            patient_service: PatientService = Depends()):
    patient = await patient_service.get_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return Patient.model_validate(patient)


@router.get("/code/{patient_code}", response_model=Patient)
async def get_patient_by_code(patient_code: str,
                              patient_service: PatientService = Depends()):
    patient = await patient_service.get_by_code(patient_code)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return Patient.model_validate(patient)


@router.post("", response_model=Patient, status_code=201)
async def create_patient(patient_data: PatientCreate,
                         patient_service: PatientService = Depends()):
    patient = await patient_service.create_patient(patient_data)
    return Patient.model_validate(patient)


@router.put("/{patient_id}", response_model=Patient)
async def update_patient(patient_id: int,
                         patient_data: PatientUpdate,
                         patient_service: PatientService = Depends()):
    patient = await patient_service.update_patient(patient_id, patient_data)
    return Patient.model_validate(patient)


@router.patch("/{patient_id}/status", response_model=Patient)
async def update_patient_status(patient_id: int, status: PatientStatus,
                                patient_service: PatientService = Depends()):
    patient = await patient_service.update_patient_status(patient_id, status)
    return Patient.model_validate(patient)


@router.delete("/{patient_id}", status_code=204)
async def delete_patient(patient_id: int,
                         patient_service: PatientService = Depends()):
    await patient_service.delete_patient(patient_id)
