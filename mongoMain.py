#!/usr/bin/env python3
import falcon.asgi
from pymongo import MongoClient
import logging

from resources import PatientResource, PatientsResource, FormTemplateResource

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
patients_resource = PatientsResource(db)
patient_resource = PatientResource(db)
form_template_resource = FormTemplateResource(db)

# Add routes to serve the resources
app.add_route('/patients', patients_resource)
app.add_route('/patients/{patient_id}', patient_resource)
app.add_route('/form-templates', form_template_resource)