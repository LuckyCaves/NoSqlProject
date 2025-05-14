#!/usr/bin/env python3
import argparse
import logging
import os
import requests
from pprint import pprint
import json
from tabulate import tabulate
from datetime import datetime

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('medical_records.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars to API connection
MEDICAL_RECORDS_API = os.getenv('MEDICAL_RECORDS_API', "http://localhost:8000")

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
        
        # Get current patient data
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        
        # Add the new lab result
        if 'lab_results' not in patient:
            patient['lab_results'] = []
        patient['lab_results'].append(lab_data)
        
        # Update the patient
        update_response = requests.put(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}",
            json=patient
        )
        update_response.raise_for_status()
        print("Lab result added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding lab result: {err}")
    except Exception as err:
        print(f"Error: {err}")

def add_prescription():
    patient_id = input("Enter patient ID: ")
    print("\nEnter prescription details:")
    prescription_data = {
        "medication": input("Medication: "),
        "dosage": input("Dosage: "),
        "frequency": input("Frequency: "),
        "doctor_id": input("Doctor ID: "),
        "route": input("Route (oral, IV, etc): "),
        "date_prescribed": input("Date prescribed (YYYY-MM-DD): ")
    }
    
    try:
        # Get current patient data
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        
        # Add the new prescription
        if 'prescriptions' not in patient:
            patient['prescriptions'] = []
        patient['prescriptions'].append(prescription_data)
        
        # Update the patient
        update_response = requests.put(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}",
            json=patient
        )
        update_response.raise_for_status()
        print("Prescription added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding prescription: {err}")
    except Exception as err:
        print(f"Error: {err}")

def add_consultation():
    patient_id = input("Enter patient ID: ")
    print("\nEnter consultation details:")
    consultation_data = {
        "doctor_id": input("Doctor ID: "),
        "date": input("Date (YYYY-MM-DDTHH:MM:SS): "),
        "reason": input("Reason: "),
        "notes": input("Notes: ")
    }
    
    try:
        # Get current patient data
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        
        # Add the new consultation
        if 'consultations' not in patient:
            patient['consultations'] = []
        patient['consultations'].append(consultation_data)
        
        # Update the patient
        update_response = requests.put(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}",
            json=patient
        )
        update_response.raise_for_status()
        print("Consultation added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding consultation: {err}")
    except Exception as err:
        print(f"Error: {err}")
    
    try:
        # First get the current patient data
        patient_response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        patient_response.raise_for_status()
        patient = patient_response.json()
        
        # Add the new consultation
        patient['consultations'].append(consultation_data)
        
        # Update the patient
        update_response = requests.put(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}",
            json=patient
        )
        update_response.raise_for_status()
        print("Consultation added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding consultation: {err}")
    except Exception as err:
        print(f"Error: {err}")

def add_disease():
    patient_id = input("Enter patient ID: ")
    disease = input("Enter disease to add: ")
    
    try:
        # Get current patient data
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        
        # Add the new disease if not already present
        if 'comorbidities' not in patient:
            patient['comorbidities'] = []
        
        if disease.strip() and disease not in patient['comorbidities']:
            patient['comorbidities'].append(disease.strip())
            
            # Update the patient
            update_response = requests.put(
                f"{MEDICAL_RECORDS_API}/patients/{patient_id}",
                json=patient
            )
            update_response.raise_for_status()
            print("Disease added successfully!")
        else:
            print("Disease already exists for this patient or is empty")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding disease: {err}")
    except Exception as err:
        print(f"Error: {err}")

def add_filled_form():
    patient_id = input("Enter patient ID: ")
    print("\nEnter filled form details:")
    form_data = {
        "template_id": input("Template ID: "),
        "storage_reference": {
            "cabinet_number": input("Cabinet number: "),
            "file_url": input("File URL: ")
        },
        "date_filled": input("Date filled (YYYY-MM-DD): ")
    }
    
    try:
        # Get current patient data
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        
        # Add the new form
        if 'forms_filled' not in patient:
            patient['forms_filled'] = []
        patient['forms_filled'].append(form_data)
        
        # Update the patient
        update_response = requests.put(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}",
            json=patient
        )
        update_response.raise_for_status()
        print("Filled form added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding filled form: {err}")
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
        # Get current patient data
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        
        # Add the new allergy
        if 'allergies' not in patient:
            patient['allergies'] = []
        patient['allergies'].append(allergy_data)
        
        # Update the patient
        update_response = requests.put(
            f"{MEDICAL_RECORDS_API}/patients/{patient_id}",
            json=patient
        )
        update_response.raise_for_status()
        print("Allergy added successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"Error adding allergy: {err}")
    except Exception as err:
        print(f"Error: {err}")

# ========== DELETE FUNCTIONS ==========
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

def search_last_consultation_doctor():
    patient_id = input("Enter patient ID: ")
    log.info(f"Searching last consultation doctor for patient: {patient_id}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        patient = response.json()
        
        if patient and 'consultations' in patient and patient['consultations']:
            # Ordenar consultas por fecha (más reciente primero)
            sorted_consults = sorted(
                patient['consultations'], 
                key=lambda x: x['date'], 
                reverse=True
            )
            last_consult = sorted_consults[0]
            doctor_id = last_consult['doctor_id']
            
            # Obtener información del doctor
            doctor_response = requests.get(f"{MEDICAL_RECORDS_API}/doctors/{doctor_id}")
            doctor_response.raise_for_status()
            doctor = doctor_response.json()
            
            print("\nDoctor from last consultation:")
            print(f"Name: {doctor['full_name']}")
            print(f"Specialty: {doctor['specialty']}")
            print(f"License: {doctor['license_number']}")
            print(f"Contact: {doctor['phone_number']}")
        else:
            print("No consultations recorded for this patient")
    except Exception as err:
        print(f"Error: {err}")

# ========== MAIN MENU ==========
def print_menu():
    print("\n=== Medical Records System ===")
    print("1. Search")
    print("2. See All Data")
    print("3. Add")
    print("4. Delete")
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
    print("11. Back to Main Menu")

def print_add_menu():
    print("\n=== Add Options ===")
    print("1. Register Patient")
    print("2. Register Doctor")
    print("3. Add Lab Result")
    print("4. Add Prescription")
    print("5. Add Consultation")
    print("6. Add Disease")
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
            print("Invalid input. Please enter a number between 1 and 5.")
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
                    search_last_consultation_doctor()
                elif search_choice == 11:
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
                    add_disease()
                elif add_choice == 7:
                    add_filled_form()
                elif add_choice == 8:
                    add_allergy()
                elif add_choice == 9:
                    break
                else:
                    print("Invalid choice. Please select a valid option.")

        elif choice == 4:  # Delete
            print("\n=== Delete Options ===")
            print("1. Delete Patient")
            print("2. Delete Doctor")
            print("3. Back to Main Menu")
            
            try:
                delete_choice = int(input("Select option (1-3): "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 3.")
                continue
            
            if delete_choice == 1:
                delete_patient()
            elif delete_choice == 2:
                delete_doctor()
            elif delete_choice == 3:
                continue
            else:
                print("Invalid choice. Please select a valid option.")

        elif choice == 5:  # Exit
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
    