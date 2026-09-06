from datetime import datetime, UTC

from fastapi import HTTPException

from app.models.models import Application, Job, JobStatus
from app.repositories.repository import JobRepository
from app.schemas.schemas import(
  CreateApplicationRequest,
  CreateJobRequest,
)

class JobService:
  def __init__(self, repository: JobRepository):
    self.repository = repository

  def create_job(self, request: CreateJobRequest) -> Job:
    job = Job(
      id=self.repository.next_job_id,
      title=request.title,
      description=request.description,
      location=request.location,
      created_at=datetime.now(UTC),
      status=JobStatus.OPEN
    )

    self.repository.next_job_id += 1

    return self.repository.create_job(job)

  def get_job(self, job_id: int) -> Job:
    job = self.repository.get_job(job_id)

    if job is None:
      raise HTTPException(
        status_code=404,
        detail="Job not found",
      )

    return job

  def list_jobs(self, status: JobStatus | None = None) -> list[Job]:
    jobs = self.repository.get_jobs()

    if status is not None:
      jobs = [
        job
        for job in jobs
        if job.status == status
      ]

    return jobs

  def close_job(self, job_id: int) -> Job:
    job = self.get_job(job_id)

    if job.status == JobStatus.CLOSED:
      raise HTTPException(
        status_code=400,
        detail="Job is already closed",
      )

    job.status = JobStatus.CLOSED

    return self.repository.update_job(job)

  def create_application(
      self,
      job_id: int,
      request: CreateApplicationRequest,
  ) -> Application:
    job = self.get_job(job_id)

    if job.status == JobStatus.CLOSED:
      raise HTTPException(
        status_code=400,
        detail="Cannot apply for a closed job",
      )

    application = Application(
      id=self.repository.next_application_id,
      job_id=job_id,
      candidateName=request.candidateName,
      candidateEmail=request.candidateEmail,
      submitted_at=datetime.now(UTC)
    )

    self.repository.next_application_id += 1

    return self.repository.create_application(application)

  def list_applications(self, job_id: int) -> list[Application]:
    self.get_job(job_id)

    return self.repository.get_applications_by_job(job_id)