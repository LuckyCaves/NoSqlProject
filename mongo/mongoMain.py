#!/usr/bin/env python3
import falcon.asgi
from pymongo import MongoClient
import logging

from mongoResources import PatientResource, PatientsResource, DoctorResource, DoctorsResource, FormTemplateResource

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware:
    async def process_request(self, req, resp):
        logger.info(f"Request: {req.method} {req.uri}")

    async def process_response(self, req, resp, resource, req_succeeded):
        logger.info(f"Response: {resp.status} for {req.method} {req.uri}")


# Initialize MongoDB client and database
client = MongoClient('mongodb://localhost:27017/')
db = client.projectmongodb

# Create the Falcon application
app = falcon.asgi.App(middleware=[LoggingMiddleware()])

# Instantiate the resources
patient_resource = PatientResource(db)
patinets_resource = PatientsResource(db)
doctor_resource = DoctorResource(db)
doctors_resource = DoctorsResource(db)
form_template_resource = FormTemplateResource(db)

# Add routes to serve the resources
app.add_route('/patients', patinets_resource)
app.add_route('/patients/{patient_id}', patient_resource)
app.add_route('/doctors', doctors_resource)
app.add_route('/doctors/{doctor_id}', doctor_resource)
app.add_route('/form-templates', form_template_resource)