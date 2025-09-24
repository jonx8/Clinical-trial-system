from typing import Optional

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import VisitModel
from app.schemes import VisitCreate, VisitUpdate
from app.services.patient_service import PatientService


class VisitService:
    def __init__(self, db: AsyncSession = Depends(get_db),
                 patient_service: PatientService = Depends()):
        self.db = db
        self.patient_service = patient_service

    async def get_visit(self, visit_id: int) -> Optional[VisitModel]:
        return await self.db.get(VisitModel, visit_id)

    async def create_visit_for_patient(self, patient_id: int, visit_data: VisitCreate) -> VisitModel:
        async with self.db.begin():
            if not await self.patient_service.get_patient_by_id(patient_id):
                raise HTTPException(status_code=404, detail="Patient not found")
            visit_dict = visit_data.model_dump()
            visit_dict["patient_id"] = patient_id
            visit = VisitModel(**visit_dict)
            self.db.add(visit)
            await self.db.flush()
            await self.db.refresh(visit)
        return visit

    async def list_visits_for_patient(self, patient_id: int, offset: int = 0, limit: int = 50) -> list[VisitModel]:
        stmt = select(VisitModel).where(VisitModel.patient_id == patient_id).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update_visit_for_patient(self, patient_id: int, visit_id: int, update_data: VisitUpdate) -> VisitModel:
        async with self.db.begin():
            visit = await self.get_visit_for_patient(patient_id, visit_id)

            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(visit, field, value)

            await self.db.flush()
            await self.db.refresh(visit)
        return visit

    async def delete_visit_for_patient(self, patient_id: int, visit_id: int):
        async with self.db.begin():
            visit = await self.get_visit_for_patient(patient_id, visit_id)
            await self.db.delete(visit)

    async def get_visit_for_patient(self, patient_id: int, visit_id: int) -> VisitModel:
        visit = await self.get_visit(visit_id)
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")

        if visit.patient_id != patient_id:
            raise HTTPException(status_code=409, detail="Visit does not belong to this patient")

        return visit
