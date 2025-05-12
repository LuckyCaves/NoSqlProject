#!/usr/bin/env python3
import argparse
import logging
import os
import requests
from datetime import datetime

# Configuration
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('medical_records.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

API_URL = os.getenv("MEDICAL_API_URL", "http://localhost:8000")

def print_record(record):
    for k, v in record.items():
        if isinstance(v, dict):
            print(f"{k}:")
            for sk, sv in v.items():
                print(f"  {sk}: {sv}")
        elif isinstance(v, list):
            print(f"{k}:")
            for item in v:
                if isinstance(item, dict):
                    for sk, sv in item.items():
                        print(f"  - {sk}: {sv}")
                else:
                    print(f"  - {item}")
        else:
            print(f"{k}: {v}")
    print("="*50)

def register_patient():
    """Register a new patient"""
    print("Enter patient details:")
    data = {
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
        "comorbidities": input("Comorbidities (comma separated): ").split(",")
    }
    
    response = requests.post(f"{API_URL}/patients", json=data)
    if response.ok:
        print("Patient registered successfully")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def search_patient():
    """Search for patients"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="Patient ID")
    parser.add_argument("--name", help="Patient name")
    args = parser.parse_args()
    
    if args.id:
        response = requests.get(f"{API_URL}/patients/{args.id}")
        if response.ok:
            print_record(response.json())
        else:
            print(f"Error: {response.status_code}")
    elif args.name:
        response = requests.get(f"{API_URL}/patients", params={"name": args.name})
        if response.ok:
            for patient in response.json():
                print_record(patient)
        else:
            print(f"Error: {response.status_code}")
    else:
        print("Please specify --id or --name")

def add_lab_results():
    """Add lab results for a patient"""
    patient_id = input("Patient ID: ")
    test_name = input("Test name: ")
    values = input("Test values: ")
    notes = input("Notes: ")
    
    data = {
        "test_name": test_name,
        "date": datetime.now().isoformat(),
        "values": values,
        "notes": notes
    }
    
    response = requests.post(f"{API_URL}/patients/{patient_id}/lab_results", json=data)
    if response.ok:
        print("Lab results added successfully")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def get_prescriptions():
    """Get prescriptions for a patient"""
    parser = argparse.ArgumentParser()
    parser.add_argument("patient_id", help="Patient ID")
    parser.add_argument("--medication", help="Filter by medication")
    parser.add_argument("--date_from", help="Filter from date (YYYY-MM-DD)")
    parser.add_argument("--date_to", help="Filter to date (YYYY-MM-DD)")
    args = parser.parse_args()
    
    params = {}
    if args.medication:
        params['medication'] = args.medication
    if args.date_from:
        params['date_from'] = args.date_from
    if args.date_to:
        params['date_to'] = args.date_to
    
    response = requests.get(f"{API_URL}/patients/{args.patient_id}/prescriptions", params=params)
    if response.ok:
        for prescription in response.json():
            print_record(prescription)
    else:
        print(f"Error: {response.status_code}")

def register_doctor():
    """Register a new doctor"""
    print("Enter doctor details:")
    data = {
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
    
    response = requests.post(f"{API_URL}/doctors", json=data)
    if response.ok:
        print("Doctor registered successfully")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def search_doctor():
    """Search for doctors"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="Doctor ID")
    parser.add_argument("--license", help="License number")
    parser.add_argument("--name", help="Doctor name")
    args = parser.parse_args()
    
    if args.id:
        response = requests.get(f"{API_URL}/doctors/{args.id}")
        if response.ok:
            print_record(response.json())
        else:
            print(f"Error: {response.status_code}")
    elif args.license or args.name:
        params = {}
        if args.license:
            params['license'] = args.license
        if args.name:
            params['name'] = args.name
        
        response = requests.get(f"{API_URL}/doctors", params=params)
        if response.ok:
            for doctor in response.json():
                print_record(doctor)
        else:
            print(f"Error: {response.status_code}")
    else:
        print("Please specify --id, --license or --name")

def add_allergy():
    """Add allergy for a patient"""
    patient_id = input("Patient ID: ")
    substance = input("Substance: ")
    reaction = input("Reaction: ")
    severity = input("Severity (mild/moderate/severe): ")
    
    data = {
        "substance": substance,
        "reaction": reaction,
        "severity": severity
    }
    
    response = requests.post(f"{API_URL}/patients/{patient_id}/allergies", json=data)
    if response.ok:
        print("Allergy recorded successfully")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    log.info("Medical Records Management System")
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Patient commands
    patient_parser = subparsers.add_parser('patient')
    patient_subparsers = patient_parser.add_subparsers(dest='patient_cmd', required=True)
    
    register_patient_parser = patient_subparsers.add_parser('register')
    search_patient_parser = patient_subparsers.add_parser('search')
    search_patient_parser.add_argument("--id", help="Patient ID")
    search_patient_parser.add_argument("--name", help="Patient name")
    
    # Doctor commands
    doctor_parser = subparsers.add_parser('doctor')
    doctor_subparsers = doctor_parser.add_subparsers(dest='doctor_cmd', required=True)
    
    register_doctor_parser = doctor_subparsers.add_parser('register')
    search_doctor_parser = doctor_subparsers.add_parser('search')
    search_doctor_parser.add_argument("--id", help="Doctor ID")
    search_doctor_parser.add_argument("--license", help="License number")
    search_doctor_parser.add_argument("--name", help="Doctor name")
    
    # Medical records commands
    records_parser = subparsers.add_parser('records')
    records_subparsers = records_parser.add_subparsers(dest='records_cmd', required=True)
    
    add_lab_parser = records_subparsers.add_parser('add_lab')
    prescriptions_parser = records_subparsers.add_parser('prescriptions')
    prescriptions_parser.add_argument("patient_id", help="Patient ID")
    prescriptions_parser.add_argument("--medication", help="Filter by medication")
    prescriptions_parser.add_argument("--date_from", help="Filter from date (YYYY-MM-DD)")
    prescriptions_parser.add_argument("--date_to", help="Filter to date (YYYY-MM-DD)")
    
    # Allergy commands
    allergy_parser = subparsers.add_parser('allergy')
    allergy_subparsers = allergy_parser.add_subparsers(dest='allergy_cmd', required=True)
    add_allergy_parser = allergy_subparsers.add_parser('add')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'patient':
            if args.patient_cmd == 'register':
                register_patient()
            elif args.patient_cmd == 'search':
                search_patient()
        
        elif args.command == 'doctor':
            if args.doctor_cmd == 'register':
                register_doctor()
            elif args.doctor_cmd == 'search':
                search_doctor()
        
        elif args.command == 'records':
            if args.records_cmd == 'add_lab':
                add_lab_results()
            elif args.records_cmd == 'prescriptions':
                get_prescriptions()
        
        elif args.command == 'allergy':
            if args.allergy_cmd == 'add':
                add_allergy()
    
    except Exception as e:
        log.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()