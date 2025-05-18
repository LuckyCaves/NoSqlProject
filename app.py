import os
from datetime import datetime
import datetime as dt
from uuid import UUID

from cassandra.cluster import Cluster

from Cass import cassandraModel
from Cass import cassandraApp

CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'healthcare')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

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
            #Open Mongo
            pass
        elif option == 2:
            #open dgraph
            pass
        elif option == 3:
            #Load data
            load_data(cassandraSession)
            pass
        elif option == 4:
            print("*** Exiting ****")
            break
        else:
            print("Invalid option. Please try again.")
        
    # while True:

if __name__ == '__main__':
    main()