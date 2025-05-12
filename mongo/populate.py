#!/usr/bin/env python3
import csv
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

import csv
import requests
import ast

API_URL = "http://localhost:8000"

def create_patients():
    with open("patients.csv", encoding="utf-8") as fd:
        patients_csv = csv.DictReader(fd)
        for patient in patients_csv:
            try:
                patient['full_name'] = patient['full_name'].strip()
                patient['dob'] = patient['dob'].strip()
                patient['gender'] = patient['gender'].strip()
                patient['mail'] = patient['mail'].strip()
                patient['blood_type'] = patient['blood_type'].strip()
                patient['phone'] = patient['phone'].strip()
                patient['medical_history'] = patient['medical_history'].strip()
                patient['comorbidities'] = patient['comorbidities'].split(',') if patient['comorbidities'] else []

                # Estructura anidada
                patient['emergency_contact'] = {
                    "name": patient.pop('emergency_name').strip(),
                    "phone": patient.pop('emergency_phone').strip(),
                    "relationship": patient.pop('emergency_relationship').strip()
                }

                # Campos con listas de objetos en formato texto
                json_fields = [
                    "consultations",
                    "lab_results",
                    "prescriptions",
                    "forms_filled",
                    "allergies"
                ]

                for field in json_fields:
                    try:
                        patient[field] = ast.literal_eval(patient[field])
                    except Exception as e:
                        print(f"⚠️ Error interpretando campo {field} del paciente {patient['patient_id']}: {e}")
                        patient[field] = []

                response = requests.post(f"{API_URL}/patients", json=patient)
                if response.status_code == 400 and "already exists" in response.text:
                    print(f"Paciente {patient['patient_id']} ya estaba registrado.")
                elif not response.ok:
                    print(f"❌ Error al crear paciente {patient['patient_id']}: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"🛑 Error procesando paciente {patient.get('patient_id', 'UNKNOWN')}: {e}")


def create_doctors():
    with open("doctors.csv", encoding="utf-8") as fd:
        doctors_csv = csv.DictReader(fd)
        for doctor in doctors_csv:
            # Asegúrate de conservar doctor_id si el backend lo requiere
            doctor['full_name'] = doctor['full_name'].strip()
            doctor['specialty'] = doctor['specialty'].strip()
            doctor["license_number"] = doctor["license_number"].strip()
            doctor["phone_number"] = doctor["phone_number"].strip()
            doctor["email"] = doctor["email"].strip()
            doctor["university"] = doctor["university"].strip()
            doctor["graduation_year"] = int(doctor["graduation_year"].strip())
            doctor["rfc"] = doctor["rfc"].strip()
            doctor["address"] = doctor["address"].strip()
            doctor["dob"] = doctor["dob"].strip()

            x = requests.post(f"{API_URL}/doctors", json=doctor)
            if not x.ok:
                print(f"Error al crear doctor {doctor['full_name']}: {x.status_code} - {x.text}")


def main():
    # Load patients
    create_patients();
    
    # Load doctors
    create_doctors();

if __name__ == "__main__":
    main()