from typing import Optional

from app.models.models import Application, Job

class JobRepository:
  def __init__(self):
    self.jobs: dict[int, Job] = {}
    self.applications: dict[int, Application] = {}

    self.next_job_id = 1
    self.next_application_id = 1

  def create_job(self, job: Job) -> Job:
    self.jobs[job.id] = job
    return job

  def get_job(self, job_id: int) -> Optional[Job]:
    return self.jobs.get(job_id)

  def get_jobs(self) -> list[Job]:
    return list(self.jobs.values())

  def update_job(self, job: Job) -> Job:
    self.jobs[job.id] = job
    return job

  def create_application(self, application: Application) -> Application:
    self.applications[application.id] = application
    return application

  def get_applications_by_job(self, job_id: int) -> list[Application]:
    return [
      application
      for application in self.applications.values()
      if application.job_id == job_id
    ]