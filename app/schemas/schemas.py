from pydantic import BaseModel, EmailStr

# Validate only these can be sent from client
class CreateJobRequest(BaseModel):
  title: str
  description: str
  location: str

class CreateApplicationRequest(BaseModel):
  candidateName: str
  candidateEmail: EmailStr