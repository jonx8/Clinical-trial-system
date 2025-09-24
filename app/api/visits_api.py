from fastapi import Depends, APIRouter

from app.schemes import Visit, VisitCreate, VisitUpdate
from app.services.visit_service import VisitService

router = APIRouter(prefix="/patients", tags=["visits"])


@router.get("/{patient_id}/visits", response_model=list[Visit])
async def get_visits_for_patient(
        patient_id: int,
        offset: int = 0,
        limit: int = 50,
        visit_service: VisitService = Depends()
):
    visits = await visit_service.list_visits_for_patient(patient_id, offset, limit)
    return [Visit.model_validate(v) for v in visits]


@router.get("/{patient_id}/visits/{visit_id}", response_model=Visit)
async def get_visit(
        patient_id: int,
        visit_id: int,
        visit_service: VisitService = Depends()
):
    visit = await visit_service.get_visit_for_patient(patient_id, visit_id)
    return Visit.model_validate(visit)


@router.post("/{patient_id}/visits", response_model=Visit, status_code=201)
async def create_visit_for_patient(
        patient_id: int,
        visit_data: VisitCreate,
        visit_service: VisitService = Depends()
):
    visit = await visit_service.create_visit_for_patient(patient_id, visit_data)
    return Visit.model_validate(visit)


@router.put("/{patient_id}/visits/{visit_id}", response_model=Visit, status_code=200)
async def update_visit_for_patient(
        patient_id: int,
        visit_id: int,
        update_data: VisitUpdate,
        visit_service: VisitService = Depends()
):
    visit = await visit_service.update_visit_for_patient(patient_id, visit_id, update_data)
    return Visit.model_validate(visit)

@router.delete("/{patient_id}/visits/{visit_id}", status_code=204)
async def delete_visit_for_patient(patient_id: int, visit_id: int, visit_service: VisitService = Depends()):
    await visit_service.delete_visit_for_patient(patient_id, visit_id)