from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Test case create job
def test_create_job():
  response = client.post(
    "/jobs",
    json={
      "title": "Data Analyst",
      "description": "Analyse data.",
      "location": "Kuala Lumpur",
    },
  )

  assert response.status_code == 201

  data = response.json()

  assert data["title"] == "Data Analyst"
  assert data["location"] == "Kuala Lumpur"
  assert data["status"] == "OPEN"

# Test case getting nonexistent job
def test_get_nonexistent_job():
  response = client.get("/jobs/999999")

  assert response.status_code == 404

# Test case send application for a closed job
def test_closed_job_cannot_accept_application():
  job_response = client.post(
    "/jobs",
    json={
      "title": "Backend Developer",
      "description": "Build APIs",
      "location": "Cyberjaya",
    },
  )

  job_id = job_response.json()["id"]

  close_response = client.post(
    f"/jobs/{job_id}/close"
  )

  assert close_response.status_code == 200

  application_response = client.post(
    f"/jobs/{job_id}/applications",
    json={
      "candidateName": "Ali",
      "candidateEmail": "ali@yahoo.com",
    },
  )

  assert application_response.status_code == 400
  assert(
    application_response.json()["detail"] == "Cannot apply for a closed job"
  )

# Test case create application
def test_create_application_for_open_job():
  job_response = client.post(
    "/jobs",
    json={
      "title": "Data Engineer",
      "description": "Build data pipeline",
      "location": "Kuala Lumpur",
    },
  )

  job_id = job_response.json()["id"]

  response = client.post(
    f"/jobs/{job_id}/applications",
    json={
      "candidateName": "Ahmad",
      "candidateEmail": "ahmad@gmail.com",
    },
  )

  assert response.status_code == 201

  data = response.json()

  assert data["job_id"] == job_id
  assert data["candidateName"] == "Ahmad"

# Test case listing applications for a particular job
def test_list_applications_for_job():
  job_response = client.post(
    "/jobs",
    json={
      "title": "Software Engineer",
      "description": "Develop applications",
      "location": "Remote",
    },
  )

  job_id = job_response.json()["id"]

  client.post(
    f"/jobs/{job_id}/applications",
    json={
      "candidateName": "Ali",
      "candidateEmail": "ali@example.com",
    },
  )

  response = client.get(
    f"/jobs/{job_id}/applications"
  )

  assert response.status_code == 200

  applications = response.json()

  assert len(applications) == 1
  assert applications[0]["candidateName"] == "Ali"