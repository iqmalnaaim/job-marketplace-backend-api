from pydantic import BaseModel, EmailStr

class CreateJobRequest(BaseModel):
  title: str
  description: str
  location: str

class CreateApplicationRequest(BaseModel):
  candidateName: str
  candidateEmail: EmailStr