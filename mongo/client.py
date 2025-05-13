#!/usr/bin/env python3
import argparse
import logging
import os
import requests

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('medical_records.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars to API connection
MEDICAL_RECORDS_API = os.getenv('MEDICAL_RECORDS_API', "http://localhost:8000")


def list_patients():
    log.info("Listing all patients...")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients")
        response.raise_for_status()  # Esto lanzará una excepción para códigos 4XX/5XX
        patients = response.json()
        if patients:
            for patient in patients:
                print(patient)
        else:
            print("No patients found")
    except requests.exceptions.HTTPError as err:
        log.error(f"HTTP error occurred: {err}")
        print(f"Error: {err}")
    except Exception as err:
        log.error(f"Other error occurred: {err}")
        print(f"Error: {err}")

def get_patient_by_id(patient_id):
    log.info(f"Getting patient with ID: {patient_id}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/patients/{patient_id}")
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"Patient with ID {patient_id} not found")
        else:
            log.error(f"HTTP error occurred: {err}")
            print(f"Error: {err}")
    except Exception as err:
        log.error(f"Other error occurred: {err}")
        print(f"Error: {err}")


def get_doctor_by_id(doctor_id):
    log.info(f"Getting doctor with ID: {doctor_id}")
    response = requests.get(f"{MEDICAL_RECORDS_API}/doctors/{doctor_id}")
    if response.status_code == 200:
        print(response.json())
    elif response.status_code == 404:
        print(f"Doctor with ID {doctor_id} not found")
    else:
        log.error(f"Failed to get doctor: {response.status_code} - {response.text}")
        print(f"Error: {response.status_code} - {response.text}")


def main():
    log.info(f"Welcome to the Medical Records API client!")
    log.info(f"Connecting to API at {MEDICAL_RECORDS_API}")

    parser = argparse.ArgumentParser(description='Medical Records API Client')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Patient commands
    patient_parser = subparsers.add_parser('patient', help='Patient operations')
    patient_subparsers = patient_parser.add_subparsers(dest='patient_command')

    # List patients
    list_patients_parser = patient_subparsers.add_parser('list', help='List all patients')

    # Get patient by ID
    get_patient_parser = patient_subparsers.add_parser('get', help='Get patient by ID')
    get_patient_parser.add_argument('id', help='Patient ID')

    # Doctor commands
    doctor_parser = subparsers.add_parser('doctor', help='Doctor operations')
    doctor_subparsers = doctor_parser.add_subparsers(dest='doctor_command')

    # Get doctor by ID
    get_doctor_parser = doctor_subparsers.add_parser('get', help='Get doctor by ID')
    get_doctor_parser.add_argument('id', help='Doctor ID')

    args = parser.parse_args()

    if args.command == 'patient':
        if args.patient_command == 'list':
            list_patients()
        elif args.patient_command == 'get':
            get_patient_by_id(args.id)
    elif args.command == 'doctor':
        if args.doctor_command == 'get':
            get_doctor_by_id(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()