from fastapi import APIRouter, Query

from app.models.models import Application, Job, JobStatus
from app.repositories.repository import JobRepository
from app.schemas.schemas import (
  CreateApplicationRequest,
  CreateJobRequest,
)
from app.services.service import JobService

router = APIRouter(prefix="/jobs", tags=["Jobs"])

repository = JobRepository()
service = JobService(repository)

@router.post("", response_model=Job, status_code=201)
def create_job(request: CreateJobRequest):
  return service.create_job(request)

@router.get("", response_model=list[Job])
def list_jobs(
  status: JobStatus | None = Query(default=None)
):
  return service.list_jobs(status)

@router.get("/{job_id}", response_model=Job)
def get_job(job_id: int):
  return service.get_job(job_id)

@router.post("/{job_id}/close", response_model=Job)
def close_job(job_id: int):
  return service.close_job(job_id)

@router.post(
  "/{job_id}/applications",
  response_model=Application,
  status_code=201,
)
def create_application(
  job_id: int,
  request: CreateApplicationRequest,
):
  return service.create_application(
    job_id,
    request,
  )

@router.get(
  "/{job_id}/applications",
  response_model=list[Application],
)
def list_applications(job_id: int):
  return service.list_applications(job_id)