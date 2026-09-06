from fastapi import FastAPI

from app.routers.jobs import router as jobs_router

app = FastAPI(
  title="Job Marketplace API",
  version='1.0.0',
)

app.include_router(jobs_router)