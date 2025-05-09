import falcon
from bson.objectid import ObjectId
from datetime import datetime
from typing import List, Dict, Union

class PatientResource:
    def __init__(self, db):
        self.collection = db.patients

    async def on_get(self, req, resp, patient_id):
        """Handles GET requests to retrieve a patient by ID."""
        patient = self.collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient["_id"] = str(patient["_id"])
            resp.media = patient
            resp.status = falcon.HTTP_200
        else:
            resp.media = {"error": "Patient not found"}
            resp.status = falcon.HTTP_404

    async def on_put(self, req, resp, patient_id):
        """Handles PUT requests to update a patient by ID."""
        data = await req.media
        result = self.collection.update_one({"_id": ObjectId(patient_id)}, {"$set": data})
        if result.modified_count > 0:
            resp.media = {"message": "Patient updated successfully"}
            resp.status = falcon.HTTP_200
        else:
            resp.media = {"error": "Patient not found or no changes made"}
            resp.status = falcon.HTTP_404
    
    async def on_delete(self, req, resp, patient_id):
        """Handles DELETE requests to remove a patient by ID."""
        result = self.collection.delete_one({"_id": ObjectId(patient_id)})
        if result.deleted_count > 0:
            resp.media = {"message": "Patient deleted successfully"}
            resp.status = falcon.HTTP_200
        else:
            resp.media = {"error": "Patient not found"}
            resp.status = falcon.HTTP_404

class PatientsResource:
    def __init__(self, db):
        self.collection = db.patients

    async def on_get(self, req, resp):
        """Handles GET requests to retrieve all patients."""
        patients = list(self.collection.find())
        for patient in patients:
            patient["_id"] = str(patient["_id"])
        resp.media = patients
        resp.status = falcon.HTTP_200

    async def on_post(self, req, resp):
        """Handles POST requests to create a new patient."""
        data = await req.media
        data = validate_patient_data(data)
        result = self.collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        resp.media = data
        resp.status = falcon.HTTP_201

class DoctorResource:
    def __init__(self, db):
        self.collection = db.doctors

    async def on_get(self, req, resp, doctor_id):
        """Handles GET requests to retrieve a doctor by ID."""
        doctor = self.collection.find_one({"_id": ObjectId(doctor_id)})
        if doctor:
            doctor["_id"] = str(doctor["_id"])
            resp.media = doctor
            resp.status = falcon.HTTP_200
        else:
            resp.media = {"error": "Doctor not found"}
            resp.status = falcon.HTTP_404
    
    async def on_put(self, req, resp, doctor_id):
        """Handles PUT requests to update a doctor by ID."""
        data = await req.media
        result = self.collection.update_one({"_id": ObjectId(doctor_id)}, {"$set": data})
        if result.modified_count > 0:
            resp.media = {"message": "Doctor updated successfully"}
            resp.status = falcon.HTTP_200
        else:
            resp.media = {"error": "Doctor not found or no changes made"}
            resp.status = falcon.HTTP_404
    
    async def on_delete(self, req, resp, doctor_id):
        """Handles DELETE requests to remove a doctor by ID."""
        result = self.collection.delete_one({"_id": ObjectId(doctor_id)})
        if result.deleted_count > 0:
            resp.media = {"message": "Doctor deleted successfully"}
            resp.status = falcon.HTTP_200
        else:
            resp.media = {"error": "Doctor not found"}
            resp.status = falcon.HTTP_404

class DoctorsResource:
    def __init__(self, db):
        self.collection = db.doctors

    async def on_get(self, req, resp):
        """Handles GET requests to retrieve all doctors."""
        doctors = list(self.collection.find())
        for doctor in doctors:
            doctor["_id"] = str(doctor["_id"])
        resp.media = doctors
        resp.status = falcon.HTTP_200

    async def on_post(self, req, resp):
        """Handles POST requests to create a new doctor."""
        data = await req.media
        result = self.collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        resp.media = data
        resp.status = falcon.HTTP_201

class FormTemplateResource:
    def __init__(self, db):
        self.collection = db.form_templates

 
# Definición de tipos (schemas)
patient_types = {
    "patient_id": str,
    "full_name": str,
    "dob": datetime,
    "gender": str,
    "mail": str,
    "blood_type": str,
    "phone": str,
    "medical_history": str,
    "emergency_contact": {
        "name": str,
        "phone": str,
        "relationship": str
    },
    "comorbidities": [str], ## enfermedades que tiene el paciente
    "consultations": [
        {
            "doctor_id": str,
            "date": datetime,
            "reason": str,
            "notes": str
        }
    ],
    "lab_results": [
        {
            "test_name": str,
            "date": str,
            "values": (str, float, int),
            "notes": str
        }
    ],
    "prescriptions": [ ## Este se hará desde la app de dgraph y to tomaré los atributos de la app de dgraph
        {
            "medication": str,
            "dosage": str,
            "frequency": str,
            "doctor_id": str,
            "route": str,
            "date_prescribed": datetime
        }
    ],
    "forms_filled": [
        {
            "template_id": str,
            "storage_reference": {
                "cabinet_number": str,
                "file_url": str
            },
            "date_filled": datetime
        }
    ],
    "allergies": [
        {
            "substance": str, ## a qué es alergico
            "reaction": str, ## reacción que tiene
            "severity": str ## mild, moderate, severe
        }
    ]
}

doctor_types = {
    "doctor_id": str,
    "full_name": str,
    "specialty": str,
    "license_number": str,
    "phone_number": str,
    "email": str,
    "university": str,
    "graduation_year": int,
    "rfc" : str,
    "address": str,
    "dob": datetime,
}

form_template_types = {
    "template_id": str,
    "template_name": str,
    "form_fields": list,
    "created_at": datetime
}

def validate_patient_data(data):
    """Validates the patient data against the defined schema."""
    for property in patient_types:
        if property not in data:
            raise ValueError(f"Missing required field: {property}")
        if patient_types[property] != str:
            try:
                data[property] = patient_types[property](data[property])
            except ValueError:
                raise falcon.HTTPBadRequest(f"Invalid type for field: {property} must be {patient_types[property]}")