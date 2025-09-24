from typing import Optional, List

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import PatientModel
from app.schemes import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_patient_by_id(self, patient_id: int) -> Optional[PatientModel]:
        return await self.db.get(PatientModel, patient_id)

    async def get_by_code(self, patient_code: str) -> Optional[PatientModel]:
        stmt = select(PatientModel).where(PatientModel.patient_code == patient_code)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_patients(self, offset: int = 0, limit: int = 50) -> List[PatientModel]:
        stmt = select(PatientModel).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_patient(self, patient_data: PatientCreate) -> PatientModel:
        async with self.db.begin():
            stmt = select(PatientModel).where(PatientModel.patient_code == patient_data.patient_code)
            existing_patient = await self.db.execute(stmt)
            if existing_patient.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="Patient code already exists")

            patient = PatientModel(**patient_data.model_dump())
            self.db.add(patient)
            await self.db.flush()
            await self.db.refresh(patient)
        return patient

    async def update_patient(self, patient_id: int, patient_data: PatientUpdate) -> PatientModel:
        async with self.db.begin():
            patient = await self._get_patient_or_404(patient_id)

            for field, value in patient_data.model_dump(exclude_unset=True).items():
                setattr(patient, field, value)

            await self.db.flush()
            await self.db.refresh(patient)
        return patient

    async def update_patient_status(self, patient_id: int, status: str) -> PatientModel:
        async with self.db.begin():
            patient = await self._get_patient_or_404(patient_id)
            patient.status = status
            await self.db.flush()
            await self.db.refresh(patient)
        return patient

    async def delete_patient(self, patient_id: int):
        async with self.db.begin():
            patient = await self._get_patient_or_404(patient_id)
            await self.db.delete(patient)

    async def _get_patient_or_404(self, patient_id: int) -> PatientModel:
        patient = await self.get_patient_by_id(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
