#!/usr/bin/env python3
import argparse
import logging
import os
import requests
from pprint import pprint
import json
from tabulate import tabulate

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
                pprint(patient)
                print("="*40)
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
        pprint(response.json())
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"Patient with ID {patient_id} not found")
        else:
            log.error(f"HTTP error occurred: {err}")
            print(f"Error: {err}")
    except Exception as err:
        log.error(f"Other error occurred: {err}")
        print(f"Error: {err}")


def list_doctors():
    log.info("Listing all doctors...")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/doctors")
        response.raise_for_status()
        doctors = response.json()
        if doctors:
            for doctor in doctors:
                pprint(doctor)
                print("="*40)
        else:
            print("No doctors found")
    except requests.exceptions.HTTPError as err:
        log.error(f"HTTP error occurred: {err}")
        print(f"Error: {err}")
    except Exception as err:
        log.error(f"Other error occurred: {err}")
        print(f"Error: {err}")

def get_doctor_by_id(doctor_id):
    log.info(f"Getting doctor with ID: {doctor_id}")
    try:
        response = requests.get(f"{MEDICAL_RECORDS_API}/doctors/{doctor_id}")
        response.raise_for_status()
        doctor = response.json()
        print("Doctor details:")
        table = [[key, value] for key, value in doctor.items()]
        print(tabulate(table, headers=["Field", "Value"], tablefmt="grid"))
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"Doctor with ID {doctor_id} not found")
        else:
            log.error(f"HTTP error occurred: {err}")
            print(f"Error: {err}")
    except Exception as err:
        log.error(f"Other error occurred: {err}")
        print(f"Error: {err}")

def main():
    log.info(f"Welcome to the Medical Records API client!")
    log.info(f"Connecting to API at {MEDICAL_RECORDS_API}")

    while True:
        print("\n=== Medical Records API Client ===")
        print("1. List all patients")
        print("2. Get patient by ID")
        print("3. List all doctors")
        print("4. Get doctor by ID")
        print("5. Exit")
        
        try:
            choice = int(input("Select an option (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        if choice == 1:
            list_patients()
        elif choice == 2:
            patient_id = input("Enter the patient ID: ")
            get_patient_by_id(patient_id)
        elif choice == 3:
            list_doctors()
        elif choice == 4:
            doctor_id = input("Enter the doctor ID: ")
            get_doctor_by_id(doctor_id)
        elif choice == 5:
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()