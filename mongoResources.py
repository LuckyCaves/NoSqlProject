import falcon
from bson.objectid import ObjectId
from datetime import datetime


class PatientResource:
    def __init__(self, db):
        self.db = db
    
    def on_get (self, req, resp, patient_id):
        # Obtener información de un paciente específico
        try:
            patient = self.db.patients.find_one({"patient_id": patient_id})
            if patient:
                resp.media = patient
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
                resp.media = {"error": "Patient not found"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"error": str(e)}

    def on_put(self, req, resp, patient_id, body):
        # Actualizar información de un paciente específico
        try:
            update_result = self.db.patients.update_one(
                {"patient_id": patient_id},
                {"$set": body}
            )
            if update_result.modified_count > 0:
                resp.status = falcon.HTTP_200
                resp.media = {"message": "Patient updated successfully"}
            else:
                resp.status = falcon.HTTP_404
                resp.media = {"error": "Patient not found"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"error": str(e)}
    
    def on_delete(self, req, resp, patient_id):
        # Eliminar un paciente específico
        try:
            result = self.db.patients.delete_one({"patient_id": patient_id})
            if result.deleted_count > 0:
                resp.status = falcon.HTTP_200
                resp.media = {"message": "Patient deleted successfully"}
            else:
                resp.status = falcon.HTTP_404
                resp.media = {"error": "Patient not found"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"error": str(e)}

    def add_allergy(self, req, resp, patient_id, allergy_data):
        # Agregar una alergia a un paciente específico
        try:
            result = self.db.patients.update_one(
                {"patient_id": patient_id},
                {"$push": {"allergies": allergy_data}}
            )
            if result.modified_count > 0:
                resp.status = falcon.HTTP_200
                resp.media = {"message": "Allergy added successfully"}
            else:
                resp.status = falcon.HTTP_404
                resp.media = {"error": "Patient not found"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"error": str(e)}

class PatientsResource:
    def __init__(self, db):
        self.db = db

    def on_post(self, req, resp):
        # Registrar un nuevo paciente
        try:
            data = req.media

            if self.db.patients.find_one({"patient_id": data["patient_id"]}):
                resp.status = falcon.HTTP_400
                resp.media = {"error": "Patient ID already exists"}
                return
            
            result = self.db.patients.insert_one(data)

            if result.inserted_id:
                resp.status = falcon.HTTP_201
                resp.media = {"message": "Patient registered successfully", "patient_id": str(result.inserted_id)}
            else:
                resp.status = falcon.HTTP_400
                resp.media = {"error": "Failed to register patient"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"error": str(e)}

class FormTemplateResource:
    def __init__(self, db):
        self.db = db

patient_types = {
    "patient_id": str,  # ID de 6 dígitos (validar longitud por separado si lo deseas)
    "full_name": str,
    "dob": datetime,  # Fecha en formato ISO: 'YYYY-MM-DD'
    "gender": str,  # "masculino", "femenino", "otro"
    "medical_history": str,
    "emergency_contact": {
        "name": str,
        "phone": str,
        "relationship": str
    },
    "lab_results": [  # Lista de subdocumentos
        {
            "test_name": str,
            "date": str,  # Fecha ISO
            "values": (str, float, int),  # Puede variar según el tipo de análisis
            "notes": str
        }
    ],
    "prescriptions": [ ## ESTO CHECAR CON DGRAPH MEDICACION
        {
            "medication": str,
            "dosage": str,
            "frequency": str,
            "doctor_id": str,
            "date_prescribed": datetime
        }
    ],
    "forms_filled": [
        {
            "template_id": str,
            "storage_reference": {
                "cabinet_number": str,     # Número del archivero físico
                "file_url": str            # Ruta o enlace del archivo en el servidor
            },
            "date_filled": datetime
        }
    ],
    "allergies": [
        {
            "substance": str,
            "reaction": str,
            "severity": str  # "leve", "moderada", "severa"
        }
    ]
}

form_template_types = {
    "template_id": str,
    "template_name": str,
    "form_fields": list,  # Lista de nombres de campos, ej. ["nombre", "firma", "fecha"]
    "created_at": datetime  # Fecha en formato ISO: 'YYYY-MM-DD'
}