#!/usr/bin/env python3
import os

import pydgraph

import model

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def print_menu():
    mm_options = {
        1: "Set schema",
        2: "Load data",
        3: "Get doctors for patient",
        4: "Get patients for doctor",
        5: "Get patient health summary",
        6: "Get doctors by specialty",
        7: "Get treatments and medications for disease",
        8: "Get side effects for medication",
        9: "Get team composition and patients",
        10: "Check family hereditary disease risk",
        11: "Get medication interactions",
        12: "Get treatment effectiveness",
        13: "Get diseases for symptom",
        14: "Get doctors recommended by doctor",
        15: "Get treatment rehabilitation info",
        0: "Exit",
    }
    print("\n===== Medical Database System =====")
    for key in mm_options.keys():
        print(f"{key} -- {mm_options[key]}")
    print("==================================")


def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)


def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)


def close_client_stub(client_stub):
    client_stub.close()


def main():
    client_stub = create_client_stub()
    client = create_client(client_stub)

    while True:
        print_menu()
        try:
            option = int(input('Enter your choice: '))
            
            if option == 0:
                print("Exiting program. Goodbye!")
                break
                
            elif option == 1:
                print("Setting schema...")
                model.set_schema(client)
                print("Schema set successfully.")
                
            elif option == 2:
                print("Loading data...")
                model.load_data(client)
                print("Data loaded successfully.")
                
            elif option == 3:
                patient_id = input("Enter patient ID: ")
                model.get_doctors_for_patient(client, patient_id)
                
            elif option == 4:
                doctor_id = input("Enter doctor ID: ")
                model.get_patients_for_doctor(client, doctor_id)
                
            elif option == 5:
                patient_id = input("Enter patient ID: ")
                model.get_patient_health_summary(client, patient_id)
                
            elif option == 6:
                specialty_id = input("Enter specialty name: ")
                model.get_doctors_by_specialty_name(client, specialty_id)
                
            elif option == 7:
                disease_id = input("Enter disease name: ")
                model.get_treatments_and_medications_for_disease_by_name(client, disease_id)
                
            elif option == 8:
                medication_id = input("Enter medication NAME: ")
                model.get_side_effects_for_medication_by_name(client, medication_id)
                
            elif option == 9:
                team_id = input("Enter team name: ")
                model.get_team_composition_and_patients_by_name(client, team_id)
                
            elif option == 10:
                patient_id = input("Enter patient ID: ")
                model.check_family_hereditary_disease_risk(client, patient_id)
                
            elif option == 11:
                medication_id = input("Enter medication name: ")
                model.get_medication_interactions_by_name(client, medication_id)
                
            elif option == 12:
                treatment_id = input("Enter treatment ID: ")
                model.get_treatment_effectiveness(client, treatment_id)
                
            elif option == 13:
                symptom_id = input("Enter symptom name: ")
                model.get_diseases_for_symptom_by_name(client, symptom_id)
                
            elif option == 14:
                doctor_id = input("Enter doctor ID: ")
                model.get_doctors_recommended_by_doctor(client, doctor_id)
                
            elif option == 15:
                treatment_id = input("Enter treatment ID: ")
                model.get_treatment_rehabilitation_info(client, treatment_id)
                
            else:
                print("Invalid option. Please try again.")
                
            input("\nPress Enter to continue...")
            
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error: {e}")
            
    close_client_stub(client_stub)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')