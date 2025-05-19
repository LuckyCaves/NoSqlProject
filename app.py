import os
from datetime import datetime
import datetime as dt
from uuid import UUID
import pydgraph

from cassandra.cluster import Cluster
from dgraph import model

from Cass import cassandraModel
from Cass import cassandraApp

from mongo import populate
from mongo import client

CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'healthcare')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')
# Configuración de Dgraph
DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

# Funciones de utilidad para Dgraph
def create_dgraph_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)

def create_dgraph_client(client_stub):
    return pydgraph.DgraphClient(client_stub)

def close_dgraph_client_stub(client_stub):
    client_stub.close()

def printMenuDoctor():
    mm_options = {
        0: "Create a new patient",
        1: "View appointments",
        2: "Update appointment",
        3: "Create appointment",
        4: "View vital signs",
        5: "Delete vital signs",
        6: "Create a new doctor",
        10: "Exit"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def printMenuPatient():
    mm_options = {
        0: "View appointments",
        1: "View vital signs",
        2: "View alerts",
        10: "Exit"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def print_menu():
    mm_options = {
        0: "Mobile App",
        1: "Mongo",
        2: "Dgraph",
        3: "Load data",
        4: "Exit"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def load_data(session): 
    cassandraApp.bulk_insert(session)

def createPatient(session):
    os.system("cls")
    print("**** Create a new patient ****")

    patientData = ['']*7
    patientData[0] = input("Enter patient ID: ")
    patientData[1] = input("Enter patient first name: ")
    patientData[2] = input("Enter patient last name: ")
    strDate = input("Enter patient date of birth [yyyy-mm-dd]: ")
    patientData[3] = datetime.strptime(strDate, '%Y-%m-%d').date()
    patientData[4] = patientData[1][0].lower() + patientData[2].lower()
    patientData[5] = cassandraModel.random_dateUUID(datetime.now())
    patientData[6] = "patient"

    cassandraModel.insert_patient(session, patientData)

    print("**** Patient created ****")

def createDoctor(session):

    os.system("cls")
    print("**** Create a new doctor ****")

    doctorData = ['']*7
    doctorData[0] = input("Enter doctor ID: ")
    doctorData[1] = input("Enter doctor first name: ")
    doctorData[2] = input("Enter doctor last name: ")
    doctorData[3] = input("Enter doctor specialty: ")
    doctorData[4] = doctorData[1][0].lower() + doctorData[2].lower()
    doctorData[5] = cassandraModel.random_dateUUID(datetime.now())
    doctorData[6] = "doctor"

    cassandraModel.insert_doctor(session, doctorData)

    print("**** Doctor created ****")


def appDoctor(session, accountData):
    while True:
        print("")
        printMenuDoctor()
        print("**** Select an option ****")
        option = int(input("Option: "))
        if option == 0:
            # Create a new patient
            createPatient(session)
            pass
        elif option == 1:
            cassandraApp.viewAppointmentsDoctor(session, accountData)
            pass
        elif option == 2:
            cassandraApp.updateAppointment(session, accountData)
            pass
        elif option == 3:
            cassandraApp.createAppointment(session)
            # Create appointment
            pass
        elif option == 4:
            # View vital signs
            cassandraApp.viewVitalSignsbyPatient(session)
            pass
        elif option == 5:
            # Delete vital signs
            cassandraApp.deleteVitalSignsDoctor(session)
            pass
        elif option == 6:
            # Create a new doctor
            createDoctor(session)
            pass
        elif option == 10:
            # Exit
            print("**** Exiting ****")
            break
        else:
            print("Invalid option. Please try again.")

def appPatient(session, accountData):
    while True:
        print("")
        printMenuPatient()
        print("**** Select an option ****")
        option = int(input("Option: "))
        if option == 0:
            cassandraApp.viewAppointmentsPatient(session, accountData)
            pass
        elif option == 1:
            cassandraApp.viewVitalSignsPatient(session, accountData)
            pass
        elif option == 2:
            # View alerts
            cassandraApp.viewAlertsPatient(session, accountData)
            pass
        elif option == 10:
            # Exit
            print("**** Exiting ****")
            break
        else:
            print("Invalid option. Please try again.")

def cassandraMain(session):
    while True:
        accountData = cassandraApp.print_log(session)
        if not accountData:
            print("*** Try again. ***")
            continue

        if accountData['account_id'] == 'exit':
            os.system("cls")
            break

        print(f"Welcome back {accountData['role']}, {accountData['username']}!")
        if accountData['role'] == 'doctor':
            appDoctor(session, accountData)
        if accountData['role'] == 'patient':
            appPatient(session, accountData)


def dgraph_main():
    client_stub = create_dgraph_client_stub()
    client = create_dgraph_client(client_stub)

    while True:
        print_menu_dgraph()
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
            
    close_dgraph_client_stub(client_stub)
def print_menu_dgraph():
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
    print("\n===== Dgraph Medical Database System =====")
    for key in mm_options.keys():
        print(f"{key} -- {mm_options[key]}")
    print("========================================")

def main():
    cluster = Cluster(CLUSTER_IPS.split(','))
    cassandraSession = cluster.connect()
    cassandraModel.create_keyspace(cassandraSession, KEYSPACE, REPLICATION_FACTOR)
    cassandraSession.set_keyspace(KEYSPACE)
    cassandraModel.create_schema(cassandraSession)

    while True:
        print_menu()
        print("**** Select an option ****")
        option = int(input("Option: "))
        if option == 0:
            cassandraMain(cassandraSession)
            #Open Cassandra
            pass
        elif option == 1:
            client.main()
            pass
        elif option == 2:
            dgraph_main()

            #open dgraph
            pass
        elif option == 3:
            #Load data
            load_data(cassandraSession)
            populate.main() ## Populate MongoDB
            pass
        elif option == 4:
            print("*** Exiting ****")
            break
        else:
            print("Invalid option. Please try again.")
        
    # while True:

if __name__ == '__main__':
    main()