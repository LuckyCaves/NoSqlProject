#!/usr/bin/env python3
import argparse
import logging
import os
import requests
import json


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('clinic.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
BOOKS_API_URL = os.getenv("CLINIC_API_URL", "http://localhost:8000")

def print_patient(patient):
    for k in patient.keys():
        print(f"{k}: {patient[k]}")
    print("=" * 20)
    print("\n")

def print_doctor(doctor):
    for k in doctor.keys():
        print(f"{k}: {doctor[k]}")
    print("=" * 20)
    print("\n")

def print_form_template(form_template):
    for k in form_template.keys():
        print(f"{k}: {form_template[k]}")
    print("=" * 20)
    print("\n")

def list_patients():
    log.info("Listing all patients")
    resp = requests.get(f"{BOOKS_API_URL}/patients")
    if resp.status_code == 200:
        patients = resp.json()
        for patient in patients:
            print_patient(patient)
    else:
        log.error(f"Failed to list patients: {resp.status_code} - {resp.text}")


def main():
    log.info(f"Welcome to books catalog. App requests to: {BOOKS_API_URL}")

    parser = argparse.ArgumentParser()

    parser.add_argument("resource", choices=["patients", "doctors", "form_templates"], help="Resource to interact with (patients, doctors, form-templates)")
    parser.add_argument("action", choices=["get", "update", "delete", "create", "search"])
    parser.add_argument("-i", "--id", help="ID of the resource")
    parser.add_argument("-d", "--data", help="Data to send in JSON format")

    args = parser.parse_args()
    url = f"{BOOKS_API_URL}/{args.resource}"
    if args.id:
        url += f"/{args.id}"

    try:
        if args.action == "get":
            resp = requests.get(url)
        elif args.action == "delete":
            resp = requests.delete(url)
        elif args.action == "create":
            if not args.data:
                raise ValueError("Missing JSON data for creation")
            resp = requests.post(url, json=json.loads(args.data))
        elif args.action == "update":
            if not args.data:
                raise ValueError("Missing JSON data for update")
            resp = requests.put(url, json=json.loads(args.data))
        elif args.action == "search":
            resp = requests.get(url)
        else:
            raise ValueError("Unknown action")

        print(f"Status: {resp.status_code}")
        try:
            print(json.dumps(resp.json(), indent=2))
        except Exception:
            print(resp.text)

    except Exception as e:
        log.error(f"Error: {e}")
        print("Failed to perform request. Check logs for details.")

if __name__ == "__main__":
    main()