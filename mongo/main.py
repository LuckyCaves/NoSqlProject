#!/usr/bin/env python3
import falcon.asgi
from pymongo import MongoClient
import logging
from datetime import datetime
from resources import (
    PatientResource,
    PatientsResource,
    DoctorResource,
    DoctorsResource,
    LabResultResource,
    PrescriptionResource,
    AllergyResource
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware:
    async def process_request(self, req, resp):
        logger.info(f"Request: {req.method} {req.uri}")

    async def process_response(self, req, resp, resource, req_succeeded):
        logger.info(f"Response: {resp.status} for {req.method} {req.uri}")

# Initialize MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.medical_records

# Create Falcon app
app = falcon.asgi.App(middleware=[LoggingMiddleware()])

# Instantiate resources
patient_resource = PatientResource(db)
patients_resource = PatientsResource(db)
doctor_resource = DoctorResource(db)
doctors_resource = DoctorsResource(db)
lab_result_resource = LabResultResource(db)
prescription_resource = PrescriptionResource(db)
allergy_resource = AllergyResource(db)

# Add routes
app.add_route('/patients', patients_resource)
app.add_route('/patients/{patient_id}', patient_resource)
app.add_route('/patients/{patient_id}/lab_results', lab_result_resource)
app.add_route('/patients/{patient_id}/prescriptions', prescription_resource)
app.add_route('/patients/{patient_id}/allergies', allergy_resource)
app.add_route('/doctors', doctors_resource)
app.add_route('/doctors/{doctor_id}', doctor_resource)