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
    FormTemplateResource,
    FormTemplatesResource
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
form_template_resource = FormTemplateResource(db)
form_templates_resource = FormTemplatesResource(db)

# Add routes
app.add_route('/patients', patients_resource)
app.add_route('/patients/{patient_id}', patient_resource)
app.add_route('/doctors', doctors_resource)
app.add_route('/doctors/{doctor_id}', doctor_resource)
app.add_route('/form_templates', form_templates_resource)
app.add_route('/form_templates/{template_id}', form_template_resource)
