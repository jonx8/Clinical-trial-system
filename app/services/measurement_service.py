from typing import Optional, List
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import MeasurementModel, PatientModel
from app.database import get_db
from app.schemes import MeasurementCreate, MeasurementUpdate
from app.services.visit_service import VisitService


class MeasurementService:
    def __init__(self, db: AsyncSession = Depends(get_db), visit_service: VisitService = Depends()):
        self.db = db
        self.visit_service = visit_service

    async def get_measurement(self, measurement_id: int) -> Optional[MeasurementModel]:
        return await self.db.get(MeasurementModel, measurement_id)

    async def list_measurements_for_patient(
            self, patient_id: int, offset: int = 0, limit: int = 50
    ) -> List[MeasurementModel]:
        stmt = select(MeasurementModel).where(MeasurementModel.patient_id == patient_id).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_measurement_for_patient(
            self, patient_id: int, measurement_data: MeasurementCreate
    ) -> MeasurementModel:
        async with self.db.begin():
            data = measurement_data.model_dump()
            data["patient_id"] = patient_id

            patient = await self.db.get(PatientModel, patient_id)
            if not patient:
                raise HTTPException(status_code=409, detail="Patient not found")

            visit_id = data.get("visit_id")
            if visit_id is not None:
                visit = await self.visit_service.get_visit_for_patient(patient_id, visit_id)
                if not visit:
                    raise HTTPException(status_code=409, detail="Visit not found for patient")

            measurement = MeasurementModel(**data)
            self.db.add(measurement)
            await self.db.flush()
            await self.db.refresh(measurement)
        return measurement

    async def update_measurement_for_patient(
            self, patient_id: int, measurement_id: int, update_data: MeasurementUpdate
    ) -> MeasurementModel:
        async with self.db.begin():
            measurement = await self.get_measurement(measurement_id)
            if not measurement or measurement.patient_id != patient_id:
                raise HTTPException(status_code=404, detail="Measurement not found")
            update_dict = update_data.model_dump(exclude_unset=True)
            for k, v in update_dict.items():
                setattr(measurement, k, v)
            await self.db.flush()
            await self.db.refresh(measurement)
        return measurement

    async def delete_measurement_for_patient(self, patient_id: int, measurement_id: int):
        async with self.db.begin():
            measurement = await self.get_measurement(measurement_id)
            if not measurement or measurement.patient_id != patient_id:
                raise HTTPException(status_code=404, detail="Measurement not found")
            await self.db.delete(measurement)
