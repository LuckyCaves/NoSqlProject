import logging
import os
import random
from datetime import datetime
import datetime as dt
from uuid import UUID

from cassandra.cluster import Cluster

from Cass import cassandraModel as model

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
    print("*** To exit write 'EXIT' ***")

    accountData  = check_login(session)

    if accountData:
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
    elif account_id.upper() == "EXIT":
        return {"account_id": "exit"}
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


def createAppointment(session):
    print("**** Create appointment ****")
    os.system("cls")

    appointmentData = [""] * 6
    
    appointmentData[2] = input("Enter patient ID:")
    appointmentData[3] = input("Enter doctor ID:")
    strDate = input("Enter date [yyyy-mm-dd hh:mm:ss]: ")
    appointmentData[5] = input("Enter notes (leave empty for no notes):")
    date = datetime.strptime(strDate, '%Y-%m-%d %H:%M:%S') + dt.timedelta(hours=6)
    appointmentData[1] = date
    appointmentData[0] = model.random_dateUUID(date)
    appointmentData[4] = "Scheduled"

    alertData = ['']*5
    alertData[0] = appointmentData[0] #date uuid
    alertData[1] = appointmentData[2] #patientID
    alertData[2] = appointmentData[1].date() #date
    alertData[3] = "Appointment"
    alertData[4] = f"You have an appointment scheduled with doctor {appointmentData[3]}"

    model.insert_appointment(session, appointmentData)
    model.insert_alert(session, alertData)

    print("**** Appointment created ****")

def updateAppointment(session, accountData):
    os.system("cls")
    print("**** Update appointment ****")
    doctorId = accountData['account_id']

    appointmentData = ['']*5
    appointmentData[0] = UUID(input("Enter appointment ID: "))
    appointmentData[1] = input("Enter patient ID: ")
    appointmentData[2] = doctorId
    appointmentData[3] = input("Enter status (leave empty for no changes): ")
    appointmentData[4] = input("Enter notes (leave empty for no changes): ")

    model.update_appointment(session, appointmentData)

    print("**** Appointment updated ****")

def viewAppointmentsDoctor(session, accountData):
    os.system("cls")
    print("**** View appointments ****")
    date = input("Enter date [yyyy-mm-dd] (leave empty for today):")
    patientId = input("Enter patient ID (leave empty for all):")

    if date:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        date = datetime.now()

    if patientId:
        model.get_appointments_by_patient_doctor(session, patientId, accountData['account_id'], date)
    else:
        model.get_appointments_by_doctor(session, accountData['account_id'], date)

def viewVitalSignsbyPatient(session):
    os.system("cls")
    print("**** View vital signs ****")
    patientId = input("Enter patient ID:")
    dateRange = handle_date_ranges()
    vitalSignType = input("Enter vital sign type (leave empty for all):")

    if vitalSignType:
        vitalSignType = vitalSignType.lower()
        model.get_vital_signs(session, patientId, dateRange[0], dateRange[1], vitalSignType)
    else:
        model.get_vital_signs(session, patientId, dateRange[0], dateRange[1])

def deleteVitalSignsDoctor(session):
    os.system("cls")
    print("**** Delete vital signs ****")
    dateRange = handle_date_ranges()
    patientId = input("Enter patient ID: ")
    model.delete_vital_signs(session, patientId, dateRange[0], dateRange[1])

    print("*** Vital signs deleted ***")

def viewAppointmentsPatient(session, accountData):
    os.system("cls")
    print("**** View appointments ****")
    date = input("Enter date [yyyy-mm-dd] (leave empty for today):")
    doctorId = input("Enter doctor ID (leave empty for all):")
    if date:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        date = datetime.now()
    
    if doctorId:
        model.get_appointments_by_patient_doctor(session, accountData['account_id'], doctorId, date)
    else:
        model.get_appointments_by_patient(session, accountData['account_id'], date)

def viewVitalSignsPatient(session, accountData):
    os.system("cls")
    print("**** View vital signs ****")
    dateRange = handle_date_ranges()
    vitalSignType = input("Enter vital sign type (leave empty for all):")

    if vitalSignType:
        vitalSignType = vitalSignType.lower()
        model.get_vital_signs(session, accountData['account_id'], dateRange[0], dateRange[1], vitalSignType)
    else:
        model.get_vital_signs(session, accountData['account_id'], dateRange[0], dateRange[1])

def viewAlertsPatient(session, accountData):
    os.system("cls")
    print("**** View alerts ****")
    model.get_alerts(session, accountData['account_id'])
