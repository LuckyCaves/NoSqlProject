#!/usr/bin/env python3
import argparse
import logging
import os
import requests
from pprint import pprint
import json
from tabulate import tabulate
from datetime import datetime
from pymongo import MongoClient

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('medical_records.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars to API connection
MEDICAL_RECORDS_API = os.getenv('MEDICAL_RECORDS_API', "http://localhost:8000")

client = MongoClient('mongodb://localhost:27017/')
db = client.medical_records

# ========== SEARCH FUNCTIONS ==========
def search_patient_by_id():
    patient_id = input("Enter patient ID: ")
    log.info(f"Searching patient with ID: {patient_id}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        print("\nPatient Details:")
        print(tabulate([[key, value] for key, value in patient.items()], headers=["Field", "Value"], tablefmt="grid"))
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"Patient with ID {patient_id} not found")
        else:
            print(f"Error: {err}")
    except Exception as err:
        print(f"Error: {err}")

def search_doctor_by_id():
    doctor_id = input("Enter doctor ID: ")
    log.info(f"Searching doctor with ID: {doctor_id}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/doctors/{doctor_id}")
        response.raise_for_status()
        doctor = response.json()
        print("\nDoctor Details:")
        print(tabulate([[key, value] for key, value in doctor.items()], headers=["Field", "Value"], tablefmt="grid"))
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"Doctor with ID {doctor_id} not found")
        else:
            print(f"Error: {err}")
    except Exception as err:
        print(f"Error: {err}")

def search_patient_by_name():
    name = input("Enter patient name (or part of it): ")
    log.info(f"Searching patients with name: {name}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients", params={"name": name})
        response.raise_for_status()
        patients = response.json()
        if patients:
            print("\nFound Patients:")
            for patient in patients:
                # Crear una tabla vertical para cada paciente
                table_data = [
                    ["ID", patient['patient_id']],
                    ["Name", patient['full_name']],
                    ["Gender", patient['gender']],
                    ["DOB", patient['dob']],
                    ["Phone", patient['phone']],
                    ["Email", patient['mail']]
                ]
                print(tabulate(table_data, tablefmt="grid"))  # Mostrar datos verticalmente
                print("\n")  # Separar cada paciente con una línea en blanco
        else:
            print("No patients found matching the search criteria")
    except Exception as err:
        print(f"Error: {err}")

def search_patient_diseases():
    patient_id = input("Enter patient ID: ")
    log.info(f"Searching diseases for patient: {patient_id}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        if patient and 'comorbidities' in patient:
            print("\nPatient Diseases------")
            print(f"Patient ID: {patient['patient_id']}")
            print(f"Patient Name: {patient['full_name']}")
            for disease in patient['comorbidities']:
                print(f"- {disease}")
        else:
            print("No diseases recorded for this patient")
    except Exception as err:
        print(f"Error: {err}")

def search_patient_consultations():
    patient_id = input("Enter patient ID: ")
    log.info(f"Searching consultations for patient: {patient_id}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        if patient and 'consultations' in patient and patient['consultations']:
            print("\nPatient Consultations:")
            for consult in patient['consultations']:
                print(f"\nDate: {consult['date']}")
                print(f"Doctor ID: {consult['doctor_id']}")
                print(f"Reason: {consult['reason']}")
                print(f"Notes: {consult['notes']}")
        else:
            print("No consultations recorded for this patient")
    except Exception as err:
        print(f"Error: {err}")

def search_doctor_by_license():
    license = input("Enter doctor license number: ")
    log.info(f"Searching doctor with license: {license}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/doctors", params={"license": license})
        response.raise_for_status()
        doctors = response.json()
        if doctors:
            print("\nFound Doctors:")
            for doctor in doctors:
                print(f"\nID: {doctor['doctor_id']}, Name: {doctor['full_name']}")
                print(f"Specialty: {doctor['specialty']}")
                print(f"License: {doctor['license_number']}")
        else:
            print("No doctors found with that license number")
    except Exception as err:
        print(f"Error: {err}")

def search_patient_allergies():
    patient_id = input("Enter patient ID: ")
    log.info(f"Searching allergies for patient: {patient_id}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        if patient and 'allergies' in patient and patient['allergies']:
            print("\nPatient Allergies:")
            for allergy in patient['allergies']:
                print(f"\nSubstance: {allergy['substance']}")
                print(f"Reaction: {allergy['reaction']}")
                print(f"Severity: {allergy['severity']}")
        else:
            print("No allergies recorded for this patient")
    except Exception as err:
        print(f"Error: {err}")

def search_patient_prescriptions_by_date():
    patient_id = input("Enter patient ID: ")
    date_from = input("Enter start date (YYYY-MM-DD): ")
    date_to = input("Enter end date (YYYY-MM-DD): ")
    log.info(f"Searching prescriptions for patient {patient_id} between {date_from} and {date_to}")
    try:
        response = requests.get(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}",
            params={"date_from": date_from, "date_to": date_to}
        )
        response.raise_for_status()
        patient = response.json()
        if patient and 'prescriptions' in patient:
            prescriptions = [p for p in patient['prescriptions'] 
                           if (not date_from or p['date_prescribed'] >= date_from) and 
                           (not date_to or p['date_prescribed'] <= date_to)]
            if prescriptions:
                print("\nPatient Prescriptions:")
                for presc in prescriptions:
                    print(f"\nMedication: {presc['medication']}")
                    print(f"Dosage: {presc['dosage']}")
                    print(f"Frequency: {presc['frequency']}")
                    print(f"Prescribed on: {presc['date_prescribed']}")
            else:
                print("No prescriptions found in that date range")
        else:
            print("No prescriptions recorded for this patient")
    except Exception as err:
        print(f"Error: {err}")

def search_patient_prescriptions_by_medication():
    patient_id = input("Enter patient ID: ")
    medication = input("Enter medication name (or part of it): ")
    log.info(f"Searching prescriptions for patient {patient_id} with medication {medication}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        if patient and 'prescriptions' in patient:
            prescriptions = [p for p in patient['prescriptions'] 
                           if medication.lower() in p['medication'].lower()]
            if prescriptions:
                print("\nPatient Prescriptions:")
                for presc in prescriptions:
                    print(f"\nMedication: {presc['medication']}")
                    print(f"Dosage: {presc['dosage']}")
                    print(f"Frequency: {presc['frequency']}")
                    print(f"Prescribed on: {presc['date_prescribed']}")
            else:
                print("No prescriptions found for that medication")
        else:
            print("No prescriptions recorded for this patient")
    except Exception as err:
        print(f"Error: {err}")

# ========== LIST FUNCTIONS ==========
def list_all_patients():
    log.info("Listing all patients")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients")
        response.raise_for_status()
        patients = response.json()
        if patients:
            print("\nAll Patients:")
            for patient in patients:
                print(f"\nID: {patient['patient_id']}, Name: {patient['full_name']}")
                print(f"Gender: {patient['gender']}, DOB: {patient['dob']}")
                print(f"Phone: {patient['phone']}, Email: {patient['mail']}")
        else:
            print("No patients found in the system")
    except Exception as err:
        print(f"Error: {err}")

def list_all_doctors():
    log.info("Listing all doctors")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/doctors")
        response.raise_for_status()
        doctors = response.json()
        if doctors:
            print("\nAll Doctors:")
            for doctor in doctors:
                print(f"\nID: {doctor['doctor_id']}, Name: {doctor['full_name']}")
                print(f"Specialty: {doctor['specialty']}")
                print(f"License: {doctor['license_number']}")
        else:
            print("No doctors found in the system")
    except Exception as err:
        print(f"Error: {err}")

# ========== ADD FUNCTIONS ==========
def add_patient():
    print("\nEnter new patient details:")
    patient_data = {
        "patient_id": input("Patient ID: "),
        "full_name": input("Full name: "),
        "dob": input("Date of birth (YYYY-MM-DD): "),
        "gender": input("Gender: "),
        "mail": input("Email: "),
        "blood_type": input("Blood type: "),
        "phone": input("Phone: "),
        "medical_history": input("Medical history: "),
        "emergency_contact": {
            "name": input("Emergency contact name: "),
            "phone": input("Emergency contact phone: "),
            "relationship": input("Emergency contact relationship: ")
        },
        "comorbidities": input("Comorbidities (comma separated): ").split(","),
        "consultations": [],
        "lab_results": [],
        "prescriptions": [],
        "forms_filled": [],
        "allergies": []
    }
    
    try:
        response = requests.post(f"{MEDICAL_RECORDS_API}/patients", json=patient_data)
        response.raise_for_status()
        print("Patient added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding patient: {err}")
    except Exception as err:
        print(f"Error: {err}")

def add_doctor():
    print("\nEnter new doctor details:")
    doctor_data = {
        "doctor_id": input("Doctor ID: "),
        "full_name": input("Full name: "),
        "specialty": input("Specialty: "),
        "license_number": input("License number: "),
        "phone_number": input("Phone: "),
        "email": input("Email: "),
        "university": input("University: "),
        "graduation_year": int(input("Graduation year: ")),
        "rfc": input("RFC: "),
        "address": input("Address: "),
        "dob": input("Date of birth (YYYY-MM-DD): ")
    }
    
    try:
        response = requests.post(f"{MEDICAL_RECORDS_API}/doctors", json=doctor_data)
        response.raise_for_status()
        print("Doctor added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding doctor: {err}")
    except Exception as err:
        print(f"Error: {err}")

def add_lab_result():
    patient_id = input("Enter patient ID: ")
    print("\nEnter lab result details:")
    lab_data = {
        "test_name": input("Test name: "),
        "date": input("Date (YYYY-MM-DD): "),
        "values": input("Values (number or text): "),
        "notes": input("Notes: ")
    }
    
    try:
        # Try to convert to float if possible
        try:
            lab_data['values'] = float(lab_data['values'])
        except ValueError:
            pass  # Keep as string if not convertible
        
        response = requests.post(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}/lab_results",
            json=lab_data
        )
        response.raise_for_status()
        print("Lab result added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding lab result: {err}")
    except Exception as err:
        print(f"Error: {err}")

from datetime import datetime

def add_prescription():
    patient_id = input("Enter patient ID: ")
    print("\nEnter prescription details:")
    
    while True:
        date_str = input("Date prescribed (YYYY-MM-DD): ")
        try:
            # Validar y convertir a formato ISO
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            iso_date = date_obj.isoformat()
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
    
    prescription_data = {
        "medication": input("Medication: "),
        "dosage": input("Dosage: "),
        "frequency": input("Frequency: "),
        "doctor_id": input("Doctor ID: "),
        "route": input("Route (oral, IV, etc): "),
        "date_prescribed": iso_date  # Usamos la fecha ya validada
    }
    
    try:
        response = requests.post(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}/prescriptions",
            json=prescription_data
        )
        response.raise_for_status()
        print("Prescription added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding prescription: {err}")
    except Exception as err:
        print(f"Error: {err}")

def add_consultation():
    patient_id = input("Enter patient ID: ")
    print("\nEnter consultation details:")
    
    while True:
        date_str = input("Date (YYYY-MM-DDTHH:MM:SS): ")
        try:
            # Validar el formato de fecha
            datetime.fromisoformat(date_str)
            break
        except ValueError:
            print("Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)")
    
    consultation_data = {
        "doctor_id": input("Doctor ID: "),
        "date": date_str,
        "reason": input("Reason: "),
        "notes": input("Notes: ")
    }
    
    try:
        response = requests.post(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}/consultations",
            json=consultation_data
        )
        response.raise_for_status()
        print("Consultation added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding consultation: {err.response.text}")
    except Exception as err:
        print(f"Error: {err}")

def add_comorbidity():
    patient_id = input("Enter patient ID: ")
    comorbidity = input("Enter comorbidity to add: ").strip()
    
    if not comorbidity:
        print("Comorbidity cannot be empty")
        return
    
    try:
        response = requests.post(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}/comorbidities",
            json={"comorbidity": comorbidity}
        )
        
        if response.status_code == 201:
            print("Comorbidity added successfully!")
        elif response.status_code == 200:
            print("Comorbidity already exists for this patient")
        else:
            response.raise_for_status()
            
    except requests.exceptions.HTTPError as err:
        print(f"Error adding comorbidity: {err.response.text}")
    except Exception as err:
        print(f"Error: {err}")

def add_filled_form():
    patient_id = input("Enter patient ID: ")
    print("\nEnter filled form details:")
    
    while True:
        date_str = input("Date filled (YYYY-MM-DD): ")
        try:
            datetime.fromisoformat(date_str)
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format")
    
    form_data = {
        "template_id": input("Template ID: "),
        "storage_reference": {
            "cabinet_number": input("Cabinet number: "),
            "file_url": input("File URL: ")
        },
        "date_filled": date_str
    }
    
    try:
        response = requests.post(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}/forms_filled",
            json=form_data
        )
        response.raise_for_status()
        print("Filled form added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding filled form: {err.response.text}")
    except Exception as err:
        print(f"Error: {err}")

def add_allergy():
    patient_id = input("Enter patient ID: ")
    print("\nEnter allergy details:")
    allergy_data = {
        "substance": input("Substance: "),
        "reaction": input("Reaction: "),
        "severity": input("Severity (Mild/Moderate/Severe): ")
    }
    
    try:
        response = requests.post(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}/allergies",
            json=allergy_data
        )
        response.raise_for_status()
        print("Allergy added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding allergy: {err}")
    except Exception as err:
        print(f"Error: {err}")

# ========== DELETE FUNCTIONS ========== NO SE USAN PERO SIRVEN PARA CIERTOS CASOS
def delete_patient():
    patient_id = input("Enter patient ID to delete: ")
    confirm = input(f"Are you sure you want to delete patient {patient_id}? (y/n): ")
    if confirm.lower() == 'y':
        try:
            response = requests.delete(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
            if response.status_code == 204:
                print("Patient deleted successfully!")
            else:
                print(f"Error deleting patient: {response.text}")
        except Exception as err:
            print(f"Error: {err}")
    else:
        print("Deletion cancelled")

def delete_doctor():
    doctor_id = input("Enter doctor ID to delete: ")
    confirm = input(f"Are you sure you want to delete doctor {doctor_id}? (y/n): ")
    if confirm.lower() == 'y':
        try:
            response = requests.delete(f"{MEDICAL_RECORDS_API}/doctors/{doctor_id}")
            if response.status_code == 204:
                print("Doctor deleted successfully!")
            else:
                print(f"Error deleting doctor: {response.text}")
        except Exception as err:
            print(f"Error: {err}")
    else:
        print("Deletion cancelled")

# ========== PIPELINES AGGREGATIONS ==========

def search_last_consultation_doctor():
    patient_id = input("Enter patient ID: ")
    log.info(f"Searching last consultation doctor for patient ID: {patient_id}")
    
    pipeline = [
        {
            "$match": {
                "patient_id": patient_id
            }
        },
        {
            "$unwind": "$consultations"
        },
        {
            "$sort": {
                "consultations.date": -1
            }
        },
        {
            "$limit": 1
        },
        {
            "$lookup": {
                "from": "doctors",
                "localField": "consultations.doctor_id",
                "foreignField": "doctor_id",
                "as": "doctor_info"
            }
        },
        {
            "$unwind": "$doctor_info"
        },
        {
            "$project": {
                "_id": 0,
                "doctor_name": "$doctor_info.full_name",
                "phone": "$doctor_info.phone_number",
                "license": "$doctor_info.license_number"
            }
        }
    ]
    
    try:
        result = list(db.patients.aggregate(pipeline))
        if not result:
            print(f"No consultations found for patient ID {patient_id}")
            return
            
        doctor = result[0]
        print("\nDoctor from Last Consultation:")
        print(tabulate(
            [
                ["Name", ("Dr " + doctor.get("doctor_name", "N/A"))],
                ["Phone", doctor.get("phone", "N/A")],
                ["License", doctor.get("license", "N/A")]
            ],
            headers=["Field", "Value"],
            tablefmt="grid"
        ))
        
    except Exception as err:
        print(f"Error: {err}")

def show_templates_filled_by_patient():
    patient_id = input("Enter patient ID: ")
    log.info(f"Searching filled templates for patient ID: {patient_id}")
    
    pipeline = [
        {
            "$match": {
                "patient_id": patient_id
            }
        },
        {
            "$unwind": "$forms_filled"
        },
        {
            "$lookup": {
                "from": "form_templates",
                "localField": "forms_filled.template_id",
                "foreignField": "template_id",
                "as": "template_info"
            }
        },
        {
            "$unwind": "$template_info"
        },
        {
            "$project": {
                "_id": 0,
                "patient_name": "$full_name",
                "template_name": "$template_info.template_name",
                "date_filled": "$forms_filled.date_filled",
                "cabinet_number": "$forms_filled.storage_reference.cabinet_number",
                "file_url": "$forms_filled.storage_reference.file_url"
            }
        }
    ]
    
    try:
        results = list(db.patients.aggregate(pipeline))
        if not results:
            print(f"Patient ID {patient_id} has no filled templates")
            return
            
        print(f"\nPatient: {results[0]['patient_name']} (ID: {patient_id})")
        print("Filled Templates:")
        
        for result in results:
            print(f"\n- Template: {result['template_name']}")
            print(f"  Date Filled: {result['date_filled']}")
            print(f"  Storage: Cabinet: {result['cabinet_number']}, URL: {result['file_url']}")
            
    except Exception as err:
        print(f"Error: {err}")

def show_doctors_who_attended_patient():
    patient_id = input("Enter patient ID: ")
    log.info(f"Searching doctors who attended patient ID: {patient_id}")
    
    pipeline = [
        {
            "$match": {
                "patient_id": patient_id
            }
        },
        {
            "$unwind": "$consultations"
        },
        {
            "$group": {
                "_id": "$consultations.doctor_id",
                "consultation_dates": {
                    "$push": "$consultations.date"
                }
            }
        },
        {
            "$lookup": {
                "from": "doctors",
                "localField": "_id",
                "foreignField": "doctor_id",
                "as": "doctor_info"
            }
        },
        {
            "$unwind": "$doctor_info"
        },
        {
            "$project": {
                "_id": 0,
                "doctor_id": "$doctor_info.doctor_id",
                "name": "$doctor_info.full_name",
                "specialty": "$doctor_info.specialty",
                "consultation_count": {
                    "$size": "$consultation_dates"
                }
            }
        }
    ]
    
    try:
        results = list(db.patients.aggregate(pipeline))
        if not results:
            print("No consultations found for this patient")
            return
            
        print("\nDoctors who attended this patient:")
        for doctor in results:
            print(f"\nDoctor ID: {doctor['doctor_id']}")
            print(f"Name: {doctor['name']}")
            print(f"Specialty: {doctor['specialty']}")
            print(f"Number of consultations: {doctor['consultation_count']}")
            
    except Exception as err:
        print(f"Error: {err}")

def show_patients_prescribed_medication():
    medication = input("Enter medication name: ")
    log.info(f"Searching patients prescribed with medication: {medication}")
    
    pipeline = [
        {
            "$match": {
                "prescriptions.medication": medication
            }
        },
        {
            "$project": {
                "_id": 0,
                "patient_id": 1,
                "full_name": 1,
                "phone": 1,
                "prescriptions": {
                    "$filter": {
                        "input": "$prescriptions",
                        "as": "prescription",
                        "cond": {
                            "$eq": ["$$prescription.medication", medication]
                        }
                    }
                }
            }
        }
    ]
    
    try:
        results = list(db.patients.aggregate(pipeline))
        if not results:
            print("No patients found with that medication")
            return
            
        print("\nPatients prescribed with medication:")
        for patient in results:
            print(f"\nPatient ID: {patient['patient_id']}")
            print(f"Name: {patient['full_name']}")
            print(f"Phone Number: {patient['phone']}")
            print("Prescriptions:")
            for prescription in patient['prescriptions']:
                print(f"- {prescription['medication']} ({prescription['dosage']}, {prescription['frequency']})")
                
    except Exception as err:
        print(f"Error: {err}")

# ========== MAIN MENU ==========
def print_menu():
    print("\n=== Medical Records System ===")
    print("1. Search")
    print("2. Pipelines Agregations")
    print("3. See All Data")
    print("4. Add")
    print("5. Exit")

def print_search_menu():
    print("\n=== Search Options ===")
    print("1. Search Patient by ID")
    print("2. Search Doctor by ID")
    print("3. Search Patient by Name")
    print("4. Search Patient Diseases")
    print("5. Search Patient Consultations")
    print("6. Search Doctor by License")
    print("7. Search Patient Allergies")
    print("8. Search Prescriptions by Date")
    print("9. Search Prescriptions by Medication")
    print("10. Search Last Consultation Doctor")
    print("11. Show Templates filled by patient")
    print("12. Show Docctors who attended patient")
    print("13. Show Patients prescribed medication")
    print("14. Back to Main Menu")

def print_add_menu():
    print("\n=== Add Options ===")
    print("1. Register Patient")
    print("2. Register Doctor")
    print("3. Add Lab Result")
    print("4. Add Prescription")
    print("5. Add Consultation")
    print("6. Add Comorbidity")
    print("7. Add Filled Form")
    print("8. Add Allergy")
    print("9. Back to Main Menu")

def main():
    log.info(f"Welcome to the Medical Records API client!")
    log.info(f"Connecting to API at {MEDICAL_RECORDS_API}")

    while True:
        print_menu()
        try:
            choice = int(input("Select an option (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")
            continue

        if choice == 1:  # Search
            while True:
                print_search_menu()
                try:
                    search_choice = int(input("Select search option (1-10): "))
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 10.")
                    continue
                
                if search_choice == 1:
                    search_patient_by_id()
                elif search_choice == 2:
                    search_doctor_by_id()
                elif search_choice == 3:
                    search_patient_by_name()
                elif search_choice == 4:
                    search_patient_diseases()
                elif search_choice == 5:
                    search_patient_consultations()
                elif search_choice == 6:
                    search_doctor_by_license()
                elif search_choice == 7:
                    search_patient_allergies()
                elif search_choice == 8:
                    search_patient_prescriptions_by_date()
                elif search_choice == 9:
                    search_patient_prescriptions_by_medication()
                elif search_choice == 10:
                    break
                else:
                    print("Invalid choice. Please select a valid option.")

        elif choice == 2:  # See All Data
            print("\n=== See All Data ===")
            print("1. List All Patients")
            print("2. List All Doctors")
            print("3. Back to Main Menu")
            
            try:
                list_choice = int(input("Select option (1-3): "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 3.")
                continue
            
            if list_choice == 1:
                list_all_patients()
            elif list_choice == 2:
                list_all_doctors()
            elif list_choice == 3:
                continue
            else:
                print("Invalid choice. Please select a valid option.")

        elif choice == 3:  # Add
            while True:
                print_add_menu()
                try:
                    add_choice = int(input("Select add option (1-9): "))
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 9.")
                    continue
                
                if add_choice == 1:
                    add_patient()
                elif add_choice == 2:
                    add_doctor()
                elif add_choice == 3:
                    add_lab_result()
                elif add_choice == 4:
                    add_prescription()
                elif add_choice == 5:
                    add_consultation()
                elif add_choice == 6:
                    add_comorbidity()
                elif add_choice == 7:
                    add_filled_form()
                elif add_choice == 8:
                    add_allergy()
                elif add_choice == 9:
                    break
                else:
                    print("Invalid choice. Please select a valid option.")

        elif choice == 4:  # Exit
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
    