import falcon
from bson.objectid import ObjectId


class PatientResource:
    def __init__(self, db):
        self.db = db

class PatientsResource:
    def __init__(self, db):
        self.db = db

class FormTemplateResource:
    def __init__(self, db):
        self.db = db

patient_types = {
    "patient_id": str,  # ID de 6 dígitos (validar longitud por separado si lo deseas)
    "full_name": str,
    "dob": str,  # Fecha en formato ISO: 'YYYY-MM-DD'
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
    "prescriptions": [
        {
            "medication": str,
            "dosage": str,
            "frequency": str,
            "doctor_id": str,
            "date_prescribed": str
        }
    ],
    "forms_filled": [
        {
            "template_id": str,
            "storage_reference": {
                "cabinet_number": str,     # Número del archivero físico
                "file_url": str            # Ruta o enlace del archivo en el servidor
            },
            "date_filled": str
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
    "created_at": str  # Fecha en formato ISO: 'YYYY-MM-DD'
}