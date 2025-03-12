import falcon.asgi
from pymongo import MongoClient
import logging

from mongoResources import PatientResource, PatientsResource, LabResultResource, LabResultsResource, PrescriptionResource, PrescriptionsResource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware:
    async def process_request(self, req, resp):
        logger.info(f"Request: {req.method} {req.uri}")

    async def process_response(self, req, resp, resource, req_succeeded):
        logger.info(f"Response: {resp.status} for {req.method} {req.uri}")

# Initialize MongoDB client and database
client = MongoClient('mongodb://localhost:27017/')
db = client.HealthCare

app = falcon.asgi.App(middleware=[LoggingMiddleware()])

patient_resource = PatientResource(db)
patients_resource = PatientsResource(db)
lab_result_resource = LabResultResource(db)
lab_results_resource = LabResultsResource(db)
prescription_resource = PrescriptionResource(db)
prescriptions_resource = PrescriptionsResource(db)

# Add routes to serve the resources
app.add_route('/patients', patients_resource)
app.add_route('/patients/{patient_id}', patient_resource)
app.add_route('/lab_results', lab_results_resource)
app.add_route('/lab_results/{result_id}', lab_result_resource)
app.add_route('/prescriptions', prescriptions_resource)
app.add_route('/prescriptions/{prescription_id}', prescription_resource)