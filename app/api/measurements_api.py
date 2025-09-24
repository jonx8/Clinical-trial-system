from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.schemes import Measurement, MeasurementCreate, MeasurementUpdate
from app.services.measurement_service import MeasurementService

router = APIRouter(prefix="/patients", tags=["measurements"])


@router.get("/{patient_id}/measurements", response_model=List[Measurement])
async def list_measurements(
    patient_id: int, offset: int = 0, limit: int = 50,
    service: MeasurementService = Depends()
):
    measurements = await service.list_measurements_for_patient(patient_id, offset, limit)
    return [Measurement.model_validate(m) for m in measurements]


@router.get("/{patient_id}/measurements/{measurement_id}", response_model=Measurement)
async def get_measurement(
    patient_id: int, measurement_id: int,
    service: MeasurementService = Depends()
):
    measurement = await service.get_measurement(measurement_id)
    if not measurement or measurement.patient_id != patient_id:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return Measurement.model_validate(measurement)


@router.post("/{patient_id}/measurements", response_model=Measurement, status_code=201)
async def create_measurement(
    patient_id: int, measurement_data: MeasurementCreate,
    service: MeasurementService = Depends()
):
    measurement = await service.create_measurement_for_patient(patient_id, measurement_data)
    return Measurement.model_validate(measurement)


@router.put("/{patient_id}/measurements/{measurement_id}", response_model=Measurement)
async def update_measurement(
    patient_id: int, measurement_id: int, update_data: MeasurementUpdate,
    service: MeasurementService = Depends()
):
    measurement = await service.update_measurement_for_patient(patient_id, measurement_id, update_data)
    return Measurement.model_validate(measurement)


@router.delete("/{patient_id}/measurements/{measurement_id}", status_code=204)
async def delete_measurement(
    patient_id: int, measurement_id: int,
    service: MeasurementService = Depends()
):
    await service.delete_measurement_for_patient(patient_id, measurement_id)
