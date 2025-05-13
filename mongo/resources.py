#!/usr/bin/env python3
import falcon
from bson.objectid import ObjectId
from datetime import datetime
from pymongo import errors

# Helper functions
def validate_data(data, schema):
    for field, field_type in schema.items():
        if field not in data:
            raise falcon.HTTPBadRequest(f"Missing required field: {field}")
        
        if isinstance(field_type, type):
            try:
                # Special handling for datetime fields
                if field_type == datetime and isinstance(data[field], str):
                    data[field] = datetime.fromisoformat(data[field])
                else:
                    data[field] = field_type(data[field])
            except (ValueError, TypeError):
                raise falcon.HTTPBadRequest(f"Invalid type for field {field}. Expected {field_type}")
        
        elif isinstance(field_type, dict):
            validate_data(data[field], field_type)
        
        elif isinstance(field_type, list) and data[field]:
            if isinstance(field_type[0], dict):
                for item in data[field]:
                    validate_data(item, field_type[0])
    return data

# Schemas
patient_schema = {
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
    "comorbidities": [str],
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
    "prescriptions": [
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
            "substance": str,
            "reaction": str,
            "severity": str
        }
    ]
}

doctor_schema = {
    "doctor_id": str,
    "full_name": str,
    "specialty": str,
    "license_number": str,
    "phone_number": str,
    "email": str,
    "university": str,
    "graduation_year": int,
    "rfc": str,
    "address": str,
    "dob": datetime
}

form_template_types = {
    "template_id": str,
    "template_name": str,
    "form_fields": list,
    "created_at": datetime
}


# Resources
class PatientResource:
    def __init__(self, db):
        self.db = db

    def _convert_datetimes(self, data):
        """Helper method to convert datetime objects to ISO format strings"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                elif isinstance(value, dict):
                    self._convert_datetimes(value)
                elif isinstance(value, list):
                    for item in value:
                        self._convert_datetimes(item)
        return data

    async def on_get(self, req, resp, patient_id):
        """Get patient by ID"""
        patient = self.db.patients.find_one({"patient_id": patient_id})
        if patient:
            patient['_id'] = str(patient['_id'])
            # Convert datetime objects to strings
            self._convert_datetimes(patient)
            resp.media = patient
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

    async def on_put(self, req, resp, patient_id):
        """Update patient information"""
        data = await req.media
        try:
            data = validate_data(data, patient_schema)
            result = self.db.patients.update_one(
                {"patient_id": patient_id},
                {"$set": data}
            )
            if result.modified_count > 0:
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        except falcon.HTTPBadRequest as e:
            raise e
        except Exception as e:
            raise falcon.HTTPInternalServerError(description=str(e))

    async def on_delete(self, req, resp, patient_id):
        """Delete a patient record"""
        result = self.db.patients.delete_one({"patient_id": patient_id})
        if result.deleted_count > 0:
            resp.status = falcon.HTTP_204
        else:
            resp.status = falcon.HTTP_404

class PatientsResource:
    def __init__(self, db):
        self.db = db

    def _convert_datetimes(self, data):
        """Helper method to convert datetime objects to ISO format strings"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                elif isinstance(value, dict):
                    self._convert_datetimes(value)
                elif isinstance(value, list):
                    for item in value:
                        self._convert_datetimes(item)
        return data

    async def on_get(self, req, resp):
        """Get all patients or search by name"""
        name = req.get_param('name')
        query = {}
        if name:
            query['full_name'] = {'$regex': name, '$options': 'i'}
        
        patients = self.db.patients.find(query)
        patients_list = []
        for patient in patients:
            patient['_id'] = str(patient['_id'])
            # Convert datetime objects to strings
            self._convert_datetimes(patient)
            patients_list.append(patient)
        resp.media = patients_list
        resp.status = falcon.HTTP_200

    async def on_post(self, req, resp):
        """Create a new patient"""
        data = await req.media
        try:
            data = validate_data(data, patient_schema)
            # Check if patient already exists
            if self.db.patients.find_one({"patient_id": data['patient_id']}):
                raise falcon.HTTPBadRequest("Patient with this ID already exists")
            
            result = self.db.patients.insert_one(data)
            data['_id'] = str(result.inserted_id)
            resp.media = data
            resp.status = falcon.HTTP_201
        except falcon.HTTPBadRequest as e:
            raise e
        except Exception as e:
            raise falcon.HTTPInternalServerError(description=str(e))

class DoctorResource:
    def __init__(self, db):
        self.db = db

    def _convert_datetimes(self, data):
        """Helper method to convert datetime objects to ISO format strings"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                elif isinstance(value, dict):
                    self._convert_datetimes(value)
                elif isinstance(value, list):
                    for item in value:
                        self._convert_datetimes(item)
        return data

    async def on_get(self, req, resp, doctor_id):
        """Get doctor by ID"""
        doctor = self.db.doctors.find_one({"doctor_id": doctor_id})
        if doctor:
            doctor['_id'] = str(doctor['_id'])
            self._convert_datetimes(doctor)
            resp.media = doctor
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

    async def on_put(self, req, resp, doctor_id):
        """Update doctor information"""
        data = await req.media
        try:
            data = validate_data(data, doctor_schema)
            result = self.db.doctors.update_one(
                {"doctor_id": doctor_id},
                {"$set": data}
            )
            if result.modified_count > 0:
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        except falcon.HTTPBadRequest as e:
            raise e
        except Exception as e:
            raise falcon.HTTPInternalServerError(description=str(e))

    async def on_delete(self, req, resp, doctor_id):
        """Delete a doctor record"""
        result = self.db.doctors.delete_one({"doctor_id": doctor_id})
        if result.deleted_count > 0:
            resp.status = falcon.HTTP_204
        else:
            resp.status = falcon.HTTP_404

class DoctorsResource:
    def __init__(self, db):
        self.db = db

    def _convert_datetimes(self, data):
        """Helper method to convert datetime objects to ISO format strings"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                elif isinstance(value, dict):
                    self._convert_datetimes(value)
                elif isinstance(value, list):
                    for item in value:
                        self._convert_datetimes(item)
        return data

    async def on_get(self, req, resp):
        """Search doctors by license or name"""
        license = req.get_param('license')
        name = req.get_param('name')
        query = {}
        if license:
            query['license_number'] = license
        if name:
            query['full_name'] = {'$regex': name, '$options': 'i'}
        
        doctors = self.db.doctors.find(query)
        doctors_list = []
        for doctor in doctors:
            doctor['_id'] = str(doctor['_id'])
            self._convert_datetimes(doctor)
            doctors_list.append(doctor)
        resp.media = doctors_list
        resp.status = falcon.HTTP_200

    async def on_post(self, req, resp):
        """Create a new doctor"""
        data = await req.media
        try:
            data = validate_data(data, doctor_schema)
            # Check if doctor already exists
            if self.db.doctors.find_one({"doctor_id": data['doctor_id']}):
                raise falcon.HTTPBadRequest(
                    title="Duplicate doctor ID",
                    description="A doctor with this ID already exists in the database."
                )
            
            result = self.db.doctors.insert_one(data)
            data['_id'] = str(result.inserted_id)
            resp.media = data
            resp.status = falcon.HTTP_200
        except falcon.HTTPBadRequest as e:
            raise e
        except Exception as e:
            raise falcon.HTTPInternalServerError(description=str(e))

class LabResultResource:
    def __init__(self, db):
        self.db = db

    async def on_get(self, req, resp, patient_id):
        """Get all lab results for a patient"""
        lab_results = self.db.patients.find_one(
            {"patient_id": patient_id},
            {"lab_results": 1}
        )
        if lab_results and 'lab_results' in lab_results:
            resp.media = lab_results['lab_results']
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

    async def on_post(self, req, resp, patient_id):
        """Add lab results for a patient"""
        data = await req.media
        try:
            # Validate lab result structure
            if not isinstance(data, list):
                data = [data]
            
            for result in data:
                validate_data(result, {
                    "test_name": str,
                    "date": str,
                    "values": (str, float, int),
                    "notes": str
                })
            
            update_result = self.db.patients.update_one(
                {"patient_id": patient_id},
                {"$push": {"lab_results": {"$each": data}}}
            )
            
            if update_result.modified_count > 0:
                resp.status = falcon.HTTP_201
            else:
                resp.status = falcon.HTTP_404
        except falcon.HTTPBadRequest as e:
            raise e
        except Exception as e:
            raise falcon.HTTPInternalServerError(description=str(e))

class PrescriptionResource:
    def __init__(self, db):
        self.db = db

    async def on_get(self, req, resp, patient_id):
        """Get prescriptions for a patient with optional filters"""
        medication = req.get_param('medication')
        date_from = req.get_param('date_from')
        date_to = req.get_param('date_to')
        
        # Build query for array filtering
        array_filter = {}
        if medication:
            array_filter['prescriptions.medication'] = {'$regex': medication, '$options': 'i'}
        if date_from or date_to:
            date_query = {}
            if date_from:
                date_query['$gte'] = datetime.fromisoformat(date_from)
            if date_to:
                date_query['$lte'] = datetime.fromisoformat(date_to)
            array_filter['prescriptions.date_prescribed'] = date_query
        
        # Find patient with filtered prescriptions
        patient = self.db.patients.find_one(
            {"patient_id": patient_id},
            {"prescriptions": {
                "$elemMatch": array_filter
            }}
        )
        
        if patient and 'prescriptions' in patient:
            resp.media = patient['prescriptions']
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

class AllergyResource:
    def __init__(self, db):
        self.db = db

    async def on_get(self, req, resp, patient_id):
        """Get allergies for a patient"""
        patient = self.db.patients.find_one(
            {"patient_id": patient_id},
            {"allergies": 1}
        )
        if patient and 'allergies' in patient:
            resp.media = patient['allergies']
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

    async def on_post(self, req, resp, patient_id):
        """Add allergy for a patient"""
        data = await req.media
        try:
            validate_data(data, {
                "substance": str,
                "reaction": str,
                "severity": str
            })
            
            update_result = self.db.patients.update_one(
                {"patient_id": patient_id},
                {"$push": {"allergies": data}}
            )
            
            if update_result.modified_count > 0:
                resp.status = falcon.HTTP_201
            else:
                resp.status = falcon.HTTP_404
        except falcon.HTTPBadRequest as e:
            raise e
        except Exception as e:
            raise falcon.HTTPInternalServerError(description=str(e))
        
class FormTemplateResource:
    def __init__(self, db):
        self.db = db

    def _convert_datetimes(self, data):
        """Helper method to convert datetime objects to ISO format strings"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                elif isinstance(value, dict):
                    self._convert_datetimes(value)
                elif isinstance(value, list):
                    for item in value:
                        self._convert_datetimes(item)
        return data

    async def on_get(self, req, resp, template_id):
        """Get template by ID"""
        template = self.db.form_templates.find_one({"template_id": template_id})
        if template:
            template['_id'] = str(template['_id'])
            self._convert_datetimes(template)
            resp.media = template
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

class FormTemplatesResource:
    def __init__(self, db):
        self.db = db

    def _convert_datetimes(self, data):
        """Helper method to convert datetime objects to ISO format strings"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                elif isinstance(value, dict):
                    self._convert_datetimes(value)
                elif isinstance(value, list):
                    for item in value:
                        self._convert_datetimes(item)
        return data

    async def on_get(self, req, resp):
        """Get all templates or search by name"""
        name = req.get_param('name')
        query = {}
        if name:
            query['template_name'] = {'$regex': name, '$options': 'i'}
        
        templates = self.db.form_templates.find(query)
        templates_list = []
        for template in templates:
            template['_id'] = str(template['_id'])
            self._convert_datetimes(template)
            templates_list.append(template)
        resp.media = templates_list
        resp.status = falcon.HTTP_200

    async def on_post(self, req, resp):
        """Create a new template"""
        data = await req.media
        try:
            # Validación básica
            if not all(field in data for field in ['template_id', 'template_name', 'form_fields']):
                raise falcon.HTTPBadRequest("Missing required fields")
            
            # Verificar si el template ya existe
            if self.db.form_templates.find_one({"template_id": data['template_id']}):
                raise falcon.HTTPBadRequest("Template with this ID already exists")
            
            # Insertar en la base de datos
            result = self.db.form_templates.insert_one(data)
            data['_id'] = str(result.inserted_id)
            resp.media = data
            resp.status = falcon.HTTP_201
        except falcon.HTTPBadRequest as e:
            raise e
        except Exception as e:
            raise falcon.HTTPInternalServerError(description=str(e))