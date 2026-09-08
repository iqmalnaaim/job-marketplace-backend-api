from datetime import datetime
from enum import Enum

from pydantic import BaseModel

# To ensure the JobStatus can only be OPEN or CLOSED
class JobStatus(str, Enum):
  OPEN = "OPEN"
  CLOSED = "CLOSED"

class Job(BaseModel):
  id: int
  title: str
  description: str
  location: str
  created_at: datetime
  status: JobStatus

class Application(BaseModel):
  id: int
  job_id: int
  candidateName: str
  candidateEmail: str
  submitted_at: datetime

