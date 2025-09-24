from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.api.patients_api import router as patient_router
from app.api.visits_api import router as visits_router
from app.api.measurements_api import router as measurements_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    except Exception:
        raise
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patient_router, prefix="/api/v1", tags=["patients"])
app.include_router(visits_router, prefix="/api/v1", tags=["visits"])
app.include_router(measurements_router, prefix="/api/v1", tags=["measurements"])