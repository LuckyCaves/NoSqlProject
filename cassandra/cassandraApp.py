import logging
import os
import random
from datetime import datetime

from cassandra.cluster import Cluster

import cassandraModel as model

#Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('healthcare.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'healthcare')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

def print_log(session):
    print("*** Welcome to the Healthcare App ***")
    print("**** Log in to your account using your account_id ****")

    accountData  = check_login(session)

    if accountData:
        print(f"Welcome back {accountData['role']}, {accountData['username']}!")
        return accountData

    print("Account not found. Please create a new account.")
    return None

def check_login(session):
    account_id = input('**** Account ID: ')
    log.info(f"Account ID set to {account_id}")

    row = model.get_user(session, account_id)

    if row:
        accountData = {"account_id": row[0], "username": row[1], "role": row[2]}
        return accountData
    else:
        print("Account not found.")
        return None

def handle_date_ranges():

    start_date = input('Enter the starting date [yyyy-mm-dd] (leave empty for 30 days from today):')
    end_date = input('Enter the ending date [yyyy-mm-dd] (leave empty for today):')

    date_range = [None, None]
    if len(start_date):
        date_range[0] = datetime.strptime(start_date, '%Y-%m-%d').date()
    if len(end_date):
        date_range[1] = datetime.strptime(end_date, '%Y-%m-%d').date()

    return date_range

def printMenuDoctor():
    mm_options = {
        0: "Create a new patient",
        1: "View appointments",
        2: "Update appointment",
        3: "Create appointment",
        4: "View vital signs",
        5: "Delete vital signs"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def printMenuPatient():
    mm_options = {
        0: "View appointments",
        1: "View vital signs",
        2: "View alerts"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def createAppointment(session):
    appointmentData = {}
    appointmentData['patient_id'] = input("Enter patient ID:")
    appointmentData['doctor_id'] = input("Enter doctor ID:")
    appointmentData['date'] = input("Enter date [yyyy-mm-dd hh:mm:ss]:")
    appointmentData['id'] = model.random_dateUUID(appointmentData['date'])
    appointmentData['status'] = "Scheduled"
    appointmentData['notes'] = input("Enter notes (leave empty for no notes):")

    model.insert_appointment(session, appointmentData)

def updateAppointment(session):
    appointmentData = {}
    appointmentData['appointment_id'] = input("Enter appointment ID:")
    appointmentData['status'] = input("Enter status (leave empty for no changes):")
    appointmentData['notes'] = input("leave empty for no changes):")

    model.update_appointment(session, appointmentData)

    print("**** Appointment updated ****")

def appDoctor(session, accountData):
    while True:
        print("")
        printMenuDoctor()
        print("**** Select an option ****")
        option = int(input("Option: "))
        if option == 0:
            # Create a new patient
            pass
        elif option == 1:
            # View appointments
            print("**** View appointments ****")
            date = input("Enter date [yyyy-mm-dd] (leave empty for today):")
            patientId = input("Enter patient ID (leave empty for all):")

            if date:
                date = datetime.strptime(date, '%Y-%m-%d').date()
            else:
                date = datetime.datetime.now()

            if patientId:
                model.get_appointments_by_patient_doctor(session, patientId, accountData['account_id'], date)
            else:
                model.get_appointments_by_doctor(session, accountData['account_id'], date)
            pass
        elif option == 2:
            # Update appointment
            print("**** Update appointment ****")
            updateAppointment(session)
            pass
        elif option == 3:
            print("**** Create appointment ****")
            createAppointment(session)
            # Create appointment
            pass
        elif option == 4:
            # View vital signs
            print("**** View vital signs ****")
            dateRange = handle_date_ranges()
            vitalSignType = input("Enter vital sign type (leave empty for all):")
            patientId = input("Enter patient ID:")

            if vitalSignType:
                vitalSignType = vitalSignType.lower()
                model.get_vital_signs(session, patientId, dateRange[0], dateRange[1], vitalSignType)
            else:
                model.get_vital_signs(session, patientId, dateRange[0], dateRange[1])
            pass
        elif option == 5:
            # Delete vital signs
            print("**** Delete vital signs ****")
            dateRange = handle_date_ranges()
            model.delete_vital_signs(session, accountData['account_id'], dateRange[0], dateRange[1])
            pass
        else:
            print("Invalid option. Please try again.")

def appPatient(session, accountData):
    while True:
        print("")
        printMenuPatient()
        print("**** Select an option ****")
        option = int(input("Option: "))
        if option == 0:
            print("**** View appointments ****")
            date = input("Enter date [yyyy-mm-dd] (leave empty for today):")
            doctorId = input("Enter doctor ID (leave empty for all):")
            if date:
                date = datetime.strptime(date, '%Y-%m-%d').date()
            else:
                date = datetime.datetime.now()
            
            if doctorId:
                model.get_appointments_by_patient_doctor(session, accountData['account_id'], doctorId, date)
            else:
                model.get_appointments_by_patient(session, accountData['account_id'], date)
            # View appointments
            pass
        elif option == 1:
            # View vital signs
            print("**** View vital signs ****")
            dateRange = handle_date_ranges()
            vitalSignType = input("Enter vital sign type (leave empty for all):")

            if vitalSignType:
                vitalSignType = vitalSignType.lower()
                model.get_vital_signs(session, accountData['account_id'], dateRange[0], dateRange[1], vitalSignType)
            else:
                model.get_vital_signs(session, accountData['account_id'], dateRange[0], dateRange[1])
            pass
        elif option == 2:
            # View alerts
            print("**** View alerts ****")


        else:
            print("Invalid option. Please try again.")

def main():
    log.info("Connecting to Cassandra Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)

    # Insert data
    # model.bulk_insert(session)

    accountData = print_log(session)

    if not accountData:
        print("**** No account found. Exiting...")
        return

    if accountData['role'] == 'doctor':
        appDoctor(session, accountData)
    if accountData['role'] == 'patient':
        appPatient(session, accountData)

    # while True:

if __name__ == '__main__':
    main()