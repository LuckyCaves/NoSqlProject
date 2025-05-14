import time_uuid
import logging
from datetime import datetime
import datetime as dt
import random
import uuid
from cassandra.query import BatchStatement

log = logging.getLogger()

'''
========================================================
==        Cassandra create keyspace and tables        ==
========================================================
'''

CREATE_KEYSPACE ="""
    CREATE KEYSPACE IF NOT EXISTS {}
    WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': {}}};
"""

CREATE_PATIENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT,
        first_name TEXT,
        last_name TEXT,
        dob DATE,
        PRIMARY KEY (patient_id)
    );
"""

CREATE_DOCTORS_TABLE = """
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id TEXT,
        first_name TEXT,
        last_name TEXT,
        specialty TEXT,
        PRIMARY KEY (doctor_id)
    );
"""

CREATE_ACCOUNTS_TABLE = """
    CREATE TABLE IF NOT EXISTS accounts (
        account_id TEXT,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        registration_date TIMEUUID,
        role TEXT,  
        PRIMARY KEY (account_id)
    );
"""

CREATE_APPOINTMENTS_BY_PATIENT_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS appointments_by_patient (
        appointment_id TIMEUUID,
        appointment_date DATE,
        patient_id TEXT,
        doctor_id TEXT,
        status TEXT,
        notes TEXT,
        PRIMARY KEY (patient_id, appointment_id)
    )WITH CLUSTERING ORDER BY (appointment_id DESC);
"""

CREATE_APPOINTMENTS_BY_DOCTOR_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS appointments_by_doctor (
        appointment_id TIMEUUID,
        appointment_date DATE,
        patient_id TEXT,
        doctor_id TEXT,
        status TEXT,
        notes TEXT,
        PRIMARY KEY (doctor_id, appointment_id)
    )WITH CLUSTERING ORDER BY (appointment_id DESC);
"""

CREATE_APPOINTMENTS_BY_DATE_PD_TABLE = """
    CREATE TABLE IF NOT EXISTS appointments_by_pd (
        appointment_id TIMEUUID,
        appointment_date DATE,
        patient_id TEXT,
        doctor_id TEXT,
        status TEXT,
        notes TEXT,
        PRIMARY KEY ((patient_id, doctor_id), appointment_id)
    )WITH CLUSTERING ORDER BY (appointment_id DESC);
"""

CREATE_APPOINTMENTS_BY_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS appointments_by_date (
        appointment_id TIMEUUID,
        appointment_date DATE,
        patient_id TEXT,
        doctor_id TEXT,
        status TEXT,
        notes TEXT,
        PRIMARY KEY (appointment_id)
    )WITH CLUSTERING ORDER BY (appointment_id DESC);
"""

CREATE_VITAL_SIGNS_BY_ACCOUNT_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS vital_signs_by_account_date (
        vital_sign_id TIMEUUID,
        account_id TEXT,
        type TEXT,
        value DOUBLE,
        date DATE,
        PRIMARY KEY (account_id, vital_sign_id)
    )WITH CLUSTERING ORDER BY (vital_sign_id DESC);
"""

CREATE_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS vital_signs_by_account_type_date (
        vital_sign_id TIMEUUID,
        account_id TEXT,
        type TEXT,
        value DOUBLE,
        date DATE,
        PRIMARY KEY (account_id, type, vital_sign_id)
    )WITH CLUSTERING ORDER BY (type DESC, vital_sign_id DESC);
"""

CREATE_ALERTS_BY_ACCOUNT_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS alerts_by_account_date (
        alert_id TIMEUUID,
        account_id TEXT,
        date DATE,
        alert_type TEXT,
        alert_message TEXT,
        PRIMARY KEY (account_id, alert_id)
    );
"""

CREATE_ACTIONS_BY_ACCOUNT_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS actions_by_account_date (
        action_id TIMEUUID,
        account_id TEXT,
        date DATE,
        action_type TEXT,
        PRIMARY KEY (account_id, date, action_id)
    );
"""

'''
========================================================
==               Cassandra Queries                    ==
========================================================
'''

SELECT_ACCOUNTS = """
    SELECT 
        account_id, username, role, first_name, last_name, registration_date
    FROM accounts
        WHERE account_id = ?
"""

SELECT_VITAL_SIGNS_BY_ACCOUNT_DATE = """
    SELECT
        vital_sign_id, account_id, type, value, date
    FROM vital_signs_by_account_date
        WHERE account_id = ?
        AND VITAL_SIGN_ID >= minTimeuuid(?)
        AND VITAL_SIGN_ID <= maxTimeuuid(?)
"""

SELECT_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE = """
    SELECT
        vital_sign_id, account_id, type, value, date
    FROM vital_signs_by_account_type_date
        WHERE account_id = ?
        AND type = ?
        AND VITAL_SIGN_ID >= minTimeuuid(?)
        AND VITAL_SIGN_ID <= maxTimeuuid(?)
"""

SELECT_APPOINTMENTS_BY_PATIENT = """
    SELECT
        appointment_id, appointment_date, patient_id, doctor_id, status, notes
    FROM appointments_by_patient
        WHERE patient_id = ?
        AND appointment_id >= minTimeuuid(?)
"""

SELECT_APPOINTMENTS_BY_PATIENT_DATE = """
    SELECT
        appointment_id, appointment_date, patient_id, doctor_id, status, notes
    FROM appointments_by_patient
        WHERE patient_id = ?
        AND appointment_id  >= minTimeuuid(?)
        AND appointment_id <= maxTimeuuid(?)
"""

SELECT_APPOINTMENTS_BY_DOCTOR = """
    SELECT
        appointment_id, appointment_date, patient_id, doctor_id, status, notes
    FROM appointments_by_doctor
        WHERE doctor_id = ?
        AND appointment_id >= minTimeuuid(?)
"""

SELECT_APPOINTMENTS_BY_DOCTOR_DATE = """
    SELECT
        appointment_id, appointment_date, patient_id, doctor_id, status, notes
    FROM appointments_by_doctor
        WHERE doctor_id = ?
        AND appointment_id >= minTimeuuid(?)
        AND appointment_id <= maxTimeuuid(?)
"""

SELECT_APPOINTMENTS_BY_PATIENT_DOCTOR = """
    SELECT
        appointment_id, appointment_date, patient_id, doctor_id, status, notes
    FROM appointments_by_pd
        WHERE patient_id = ?
        AND doctor_id = ?
        AND appointment_id >= minTimeuuid(?)
"""

SELECT_APPOINTMENTS_BY_PATIENT_DOCTOR_DATE = """
    SELECT
        appointment_id, appointment_date, patient_id, doctor_id, status, notes
    FROM appointments_by_pd
        WHERE patient_id = ?
        AND doctor_id = ?
        AND appointment_id >= minTimeuuid(?)
        AND appointment_id <= maxTimeuuid(?)
"""

SELECT_ALERTS_BY_ACCOUNT = """
    SELECT
        alert_id, account_id, date, alert_type, alert_message
    FROM alerts_by_account_date
        WHERE account_id = ?
        AND alert_id >= minTimeuuid(?)
"""

INSERT_APPOINTMENT_BY_PATIENT = """
    INSERT INTO appointments_by_patient(appointment_id, appointment_date, patient_id, doctor_id, status, notes)
    VALUES (?, ?, ?, ?, ?, ?)
"""

INSERT_APPOINTMENT_BY_DOCTOR = """
    INSERT INTO appointments_by_doctor(appointment_id, appointment_date, patient_id, doctor_id, status, notes)
    VALUES (?, ?, ?, ?, ?, ?)
"""

INSERT_APPOINTMENT_BY_DATE = """
    INSERT INTO appointments_by_date(appointment_id, appointment_date, patient_id, doctor_id, status, notes)
    VALUES (?, ?, ?, ?, ?, ?)
"""

INSERT_APPOINTMENT_BY_PD = """
    INSERT INTO appointments_by_pd(appointment_id, appointment_date, patient_id, doctor_id, status, notes)
    VALUES (?, ?, ?, ?, ?, ?)
"""

UPDATE_APPOINTMENT_PATIENT = """
    UPDATE appointments_by_patient
        SET status = ?,
            notes = ?
        WHERE appointment_id = ?
        AND patient_id = ?
"""

UPDATE_APPOINTMENT_DOCTOR = """
    UPDATE appointments_by_doctor
        SET status = ?,
            notes = ?
        WHERE appointment_id = ?
        AND doctor_id = ?
"""

UPDATE_APPOINTMENT_PATIENT_DOCTOR = """
    UPDATE appointments_by_pd
        SET status = ?,
            notes = ?
        WHERE appointment_id = ?
        AND patient_id = ?
        AND doctor_id = ?
"""
UPDATE_APPOINTMENT_PATIENT_S = """
    UPDATE appointments_by_patient
        SET status = ?
        WHERE appointment_id = ?
        AND patient_id = ?
"""

UPDATE_APPOINTMENT_DOCTOR_S = """
    UPDATE appointments_by_doctor
        SET status = ?
        WHERE appointment_id = ?
        AND doctor_id = ?
"""

UPDATE_APPOINTMENT_PATIENT_DOCTOR_S = """
    UPDATE appointments_by_pd
        SET status = ?
        WHERE appointment_id = ?
        AND patient_id = ?
        AND doctor_id = ?
"""
UPDATE_APPOINTMENT_PATIENT_N = """
    UPDATE appointments_by_patient
        SET notes = ?
        WHERE appointment_id = ?
        AND patient_id = ?
"""

UPDATE_APPOINTMENT_DOCTOR_N = """
    UPDATE appointments_by_doctor
        SET notes = ?
        WHERE appointment_id = ?
        AND doctor_id = ?
"""

UPDATE_APPOINTMENT_PATIENT_DOCTOR_N = """
    UPDATE appointments_by_pd
        SET notes = ?
        WHERE appointment_id = ?
        AND patient_id = ?
        AND doctor_id = ?
"""

INSERT_DOCTOR = """
    INSERT INTO doctors(doctor_id, first_name, last_name, specialty)
    VALUES (?, ?, ?, ?)
"""

INSERT_PATIENT = """
    INSERT INTO patients(patient_id, first_name, last_name, dob)
    VALUES (?, ?, ?, ?)
"""

INSERT_ACCOUNT = """
    INSERT INTO accounts(account_id, username, first_name, last_name, registration_date, role)
    VALUES (?, ?, ?, ?, ?, ?)
"""

INSERT_ALERT_BY_ACCOUNT_DATE = """
    INSERT INTO alerts_by_account_date(alert_id, account_id, date, alert_type, alert_message)
    VALUES (?, ?, ?, ?, ?)
"""

INSERT_VITAL_SIGN_BY_ACCOUNT_DATE = """
    INSERT INTO vital_signs_by_account_date(vital_sign_id, account_id, type, value, date)
    VALUES (?, ?, ?, ?, ?)
"""

INSERT_VITAL_SIGN_BY_ACCOUNT_TYPE_DATE = """
    INSERT INTO vital_signs_by_account_type_date(vital_sign_id, account_id, type, value, date)
    VALUES (?, ?, ?, ?, ?)
"""

DELETE_VITAL_SIGNS_BY_ACCOUNT_DATE = """
    DELETE FROM vital_signs_by_account_date
    WHERE account_id = ?
    AND vital_sign_id >= minTimeuuid(?)
    AND vital_sign_id <= maxTimeuuid(?)
"""

DELETE_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE = """
    DELETE FROM vital_signs_by_account_type_date
    WHERE account_id = ?
    AND type = ?
    AND vital_sign_id >= minTimeuuid(?)
    AND vital_sign_id <= maxTimeuuid(?)
"""

def random_dateUUID(dateUUID):
        return time_uuid.TimeUUID.with_timestamp(time_uuid.mkutime(dateUUID))

def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    rand_date = start_date + dt.timedelta(days=random_number_of_days)
    return rand_date

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor: {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

def create_schema(session):
    log.info("Creating Cassandra model schema")
    session.execute(CREATE_PATIENTS_TABLE)
    session.execute(CREATE_DOCTORS_TABLE)
    # session.execute(CREATE_APPOINTMENTS_BY_DATE_TABLE)
    session.execute(CREATE_APPOINTMENTS_BY_PATIENT_DATE_TABLE)
    session.execute(CREATE_APPOINTMENTS_BY_DOCTOR_DATE_TABLE)
    session.execute(CREATE_APPOINTMENTS_BY_DATE_PD_TABLE)
    session.execute(CREATE_ACCOUNTS_TABLE)
    session.execute(CREATE_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE_TABLE)
    session.execute(CREATE_VITAL_SIGNS_BY_ACCOUNT_DATE_TABLE)
    session.execute(CREATE_ALERTS_BY_ACCOUNT_DATE_TABLE)
    session.execute(CREATE_ACTIONS_BY_ACCOUNT_DATE_TABLE) #Probalemente no se necesite

patientsData = [
    {"id": "P0001", "first_name": "John", "last_name": "Doe", "username": "jdoe"},
    {"id": "P0002", "first_name": "Alice", "last_name": "Smith", "username": "asmith"},
    {"id": "P0003", "first_name": "Bob", "last_name": "Johnson", "username": "bjohnson"},
    {"id": "P0004", "first_name": "Emma", "last_name": "White", "username": "ewhite"},
    {"id": "P0005", "first_name": "David", "last_name": "Martinez", "username": "dmartinez"},
    {"id": "P0006", "first_name": "Sophia", "last_name": "Brown", "username": "sbrown"},
    {"id": "P0007", "first_name": "Michael", "last_name": "Anderson", "username": "manderson"},
    {"id": "P0008", "first_name": "Olivia", "last_name": "Thomas", "username": "othomas"},
    {"id": "P0009", "first_name": "James", "last_name": "Harris", "username": "jharris"},
    {"id": "P0010", "first_name": "Charlotte", "last_name": "Wilson", "username": "cwilson"}
]

doctorsData = [
    {"id": "D0001", "first_name": "Liam", "last_name": "Davis", "username": "ldavis"},
    {"id": "D0002", "first_name": "Sophia", "last_name": "Miller", "username": "smiller"},
    {"id": "D0003", "first_name": "Noah", "last_name": "Garcia", "username": "ngarcia"},
    {"id": "D0004", "first_name": "Amelia", "last_name": "Rodriguez", "username": "arodriguez"},
    {"id": "D0005", "first_name": "Ethan", "last_name": "Lopez", "username": "elopez"},
    {"id": "D0006", "first_name": "Isabella", "last_name": "Gonzalez", "username": "igonzalez"},
    {"id": "D0007", "first_name": "Mason", "last_name": "Perez", "username": "mperez"},
    {"id": "D0008", "first_name": "Mia", "last_name": "Taylor", "username": "mtaylor"},
    {"id": "D0009", "first_name": "Lucas", "last_name": "Clark", "username": "lclark"},
    {"id": "D0010", "first_name": "Harper", "last_name": "Walker", "username": "hwalker"}
]

specialists = [
    "Cardiologist",
    "Dermatologist",
    "Neurologist",
    "Orthopedic Surgeon",
    "Pediatrician",
    "Oncologist",
    "Ophthalmologist",
    "Psychiatrist",
    "Endocrinologist",
    "Gastroenterologist" 
]

def execute_batch(session, stmt, data):
    batch_size = 10
    for i in range(0, len(data), batch_size):
        batch = BatchStatement()
        for item in data[i : i+batch_size]:
            batch.add(stmt, item)
        session.execute(batch)
    session.execute(batch)

def bulk_insert(session):
    pat_stmt = session.prepare("INSERT INTO patients(patient_id, first_name, last_name, dob) VALUES (?, ?, ?, ?)")
    doc_stmt = session.prepare("INSERT INTO doctors(doctor_id, first_name, last_name, specialty) VALUES (?, ?, ?, ?)")
    appbpt_stmt = session.prepare("INSERT INTO appointments_by_patient(appointment_id, appointment_date, patient_id, doctor_id, status, notes) VALUES (?, ?, ?, ?, ?, ?)")
    appbdt_stmt = session.prepare("INSERT INTO appointments_by_doctor(appointment_id, appointment_date, patient_id, doctor_id, status, notes) VALUES (?, ?, ?, ?, ?, ?)")
    appbpd_stmt = session.prepare("INSERT INTO appointments_by_pd(appointment_id, appointment_date, patient_id, doctor_id, status, notes) VALUES (?, ?, ?, ?, ?, ?)")
    acc_stmt = session.prepare("INSERT INTO accounts(account_id, username, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)")
    vs_stmt = session.prepare("INSERT INTO vital_signs_by_account_type_date(vital_sign_id, account_id, type, value, date) VALUES (?, ?, ?, ?, ?)")
    vsad_stmt = session.prepare("INSERT INTO vital_signs_by_account_date(vital_sign_id, account_id, type, value, date) VALUES (?, ?, ?, ?, ?)")
    alert_stmt = session.prepare("INSERT INTO alerts_by_account_date(alert_id, account_id, date, alert_type, alert_message) VALUES (?, ?, ?, ?, ?)")

    patients = []
    patientsAcc = []
    doctors = []
    doctorsAcc = []

    patients_num=10
    doctor_num=10
    appointments=50
    vital_signs=1000
    actions=100
    alerts=100

    # Generate patients
    data = []
    for patient in patientsData:
        patient_uuid = patient["id"]
        patients.append(patient_uuid)
        dob = random_date(datetime(1950, 1, 1), datetime(2008, 1, 1))
        data.append((patient_uuid, patient["first_name"], patient["last_name"], dob))
    execute_batch(session, pat_stmt, data)

    # Generate doctors
    data = []
    for index, doctor in enumerate(doctorsData):
        doctor_uuid = doctor["id"]
        doctors.append(doctor_uuid)
        data.append((doctor_uuid, doctor["first_name"], doctor["last_name"], specialists[index]))
    execute_batch(session, doc_stmt, data)

    # Generate appointments
    data = []
    for i in range(appointments):
        app_date = random_date(datetime(2025, 1, 1), datetime(2025, 12, 31))
        app_id = random_dateUUID(app_date)
        patient = random.choice(patients)
        doctor = random.choice(doctors)

        status = random.choice(['scheduled', 'completed', 'cancelled'])
        notes = random.choice(['', 'Patient needs to fast before the appointment', 'Patient needs to bring a urine sample'])
        data.append((app_id, app_date, patient, doctor, status, notes))
    execute_batch(session, appbpt_stmt, data)
    execute_batch(session, appbdt_stmt, data)
    execute_batch(session, appbpd_stmt, data)

    #Generate accounts doctors
    data = []
    for index, patient in enumerate(patients):
        account_id = patients[index]
        patientsAcc.append(account_id)
        registration_date = random_date(datetime(2024, 1, 1), datetime(2025, 1, 1))
        registration_date = random_dateUUID(registration_date)
        data.append((account_id, patientsData[index]["username"], patientsData[index]["first_name"], patientsData[index]["last_name"], registration_date, 'patient'))
    execute_batch(session, acc_stmt, data)
    
    # Generate accounts doctors
    data = []
    for index, doctor in enumerate(doctors):
        account_id = doctors[index]
        doctorsAcc.append(account_id)
        registration_date = random_date(datetime(2024, 1, 1), datetime(2025, 1, 1))
        registration_date = random_dateUUID(registration_date)
        data.append((account_id, doctorsData[index]["username"], doctorsData[index]["first_name"], doctorsData[index]["last_name"], registration_date, 'doctor'))
    execute_batch(session, acc_stmt, data)

    # Generate vital signs
    data = []
    for i in range(vital_signs):
        account = random.choice(patientsAcc)
        vital_sign_type = random.choice(['blood pressure', 'heart rate', 'steps', 'oxygenation', 'temperature'])
        if vital_sign_type == 'blood pressure':
            vital_sign_value = random.uniform(60, 200)
        elif vital_sign_type == 'heart rate':
            vital_sign_value = random.uniform(30, 250)
        elif vital_sign_type == 'steps':
            vital_sign_value = random.uniform(0, 20000)
        elif vital_sign_type == 'oxygenation':
            vital_sign_value = random.uniform(75, 100)
        elif vital_sign_type == 'temperature':
            vital_sign_value = random.uniform(35, 39)
        vital_sign_date = random_date(datetime(2020, 1, 1), datetime(2025, 1, 1))
        vital_sign_id = random_dateUUID(vital_sign_date)
        data.append((vital_sign_id, account, vital_sign_type, vital_sign_value, vital_sign_date))
    execute_batch(session, vs_stmt, data)
    execute_batch(session, vsad_stmt, data)

    # Generate alerts
    data = []
    for i in range(alerts):
        account = random.choice(patientsAcc)
        alert_date = random_date(datetime(2020, 1, 1), datetime(2025, 1, 1))
        alert_id = random_dateUUID(alert_date)
        alert_type = random.choice(['appointment', 'vital_sign', 'alert'])
        alert_message = random.choice(['Appointment scheduled', 'Vital sign out of range', 'New alert'])
        data.append((alert_id, account, alert_date, alert_type, alert_message))
    execute_batch(session, alert_stmt, data)

def create_account(session, accountData):
    stmt = session.prepare(INSERT_ACCOUNT)

    insertAccountData = [accountData[0], accountData[4], accountData[1], 
                            accountData[2], accountData[5], accountData[6]]
    session.execute(stmt, insertAccountData)

def insert_patient(session, patientData):
    stmt = session.prepare(INSERT_PATIENT)
    insertPatientData = [patientData[0], patientData[1], patientData[2], patientData[3]]
    print(insertPatientData)
    session.execute(stmt, insertPatientData)
    create_account(session, patientData)

def insert_doctor(session, doctorData):
    stmt = session.prepare(INSERT_DOCTOR)
    insertDoctorData = [doctorData[0], doctorData[1], doctorData[2], doctorData[3]]
    session.execute(stmt, insertDoctorData)
    create_account(session, doctorData)

def insert_appointment(session, appointmentData):

    appbpt_stmt = session.prepare(INSERT_APPOINTMENT_BY_PATIENT)
    appbdt_stmt = session.prepare(INSERT_APPOINTMENT_BY_DOCTOR)
    appbpd_stmt = session.prepare(INSERT_APPOINTMENT_BY_PD)

    execute_batch(session, appbpt_stmt, [appointmentData])
    execute_batch(session, appbdt_stmt, [appointmentData])
    execute_batch(session, appbpd_stmt, [appointmentData])

def update_appointment(session, appointmentData):

    if appointmentData[3] == "":
        appbpt_stmt = session.prepare(UPDATE_APPOINTMENT_PATIENT_N)
        appbdt_stmt = session.prepare(UPDATE_APPOINTMENT_DOCTOR_N)
        appbpd_stmt = session.prepare(UPDATE_APPOINTMENT_PATIENT_DOCTOR_N)
    elif appointmentData[4] == "":
        appbpt_stmt = session.prepare(UPDATE_APPOINTMENT_PATIENT_S)
        appbdt_stmt = session.prepare(UPDATE_APPOINTMENT_DOCTOR_S)
        appbpd_stmt = session.prepare(UPDATE_APPOINTMENT_PATIENT_DOCTOR_S)
    else:
        appbpt_stmt = session.prepare(UPDATE_APPOINTMENT_PATIENT)
        appbdt_stmt = session.prepare(UPDATE_APPOINTMENT_DOCTOR)
        appbpd_stmt = session.prepare(UPDATE_APPOINTMENT_PATIENT_DOCTOR)


    updateByPatient = [appointmentData[3], appointmentData[4], appointmentData[0], appointmentData[1]]
    updateByDoctor = [appointmentData[3], appointmentData[4], appointmentData[0], appointmentData[2]]
    updateByPatientDoctor = [appointmentData[3], appointmentData[4], appointmentData[0], appointmentData[1], appointmentData[2]]

    execute_batch(session, appbpt_stmt, [updateByPatient])
    execute_batch(session, appbdt_stmt, [updateByDoctor])
    execute_batch(session, appbpd_stmt, [updateByPatientDoctor])

def get_appointments_by_patient(session, patient_id, appointment_date=None):

    if appointment_date:
        stmt = session.prepare(SELECT_APPOINTMENTS_BY_PATIENT_DATE)
        endDate = appointment_date + dt.timedelta(days=1)
        rows = session.execute(stmt, [patient_id, appointment_date, endDate])
    else:
        stmt = session.prepare(SELECT_APPOINTMENTS_BY_PATIENT)
        rows = session.execute(stmt, [patient_id, appointment_date])

    if rows is None:
        print("You have no appointments.")
        return

    for row in rows:
        print(" ")
        print("**** Appointment ****")
        doctorData = get_user(session, row.doctor_id)
        date = time_uuid.TimeUUID.get_timestamp(row.appointment_id)
        date = datetime.fromtimestamp(date)
        print(f"=== Date: {date}")
        print(f"=== Doctor: {doctorData[3]} {doctorData[4]}")
        print(f"=== Status: {row.status}")
        print(f"=== Notes: {row.notes}")


def get_appointments_by_doctor(session, doctor_id, appointment_date=None):
    if appointment_date:
        stmt = session.prepare(SELECT_APPOINTMENTS_BY_DOCTOR_DATE)
        endDate = appointment_date + dt.timedelta(days=1)
        rows = session.execute(stmt, [doctor_id, appointment_date, endDate])
    else:
        stmt = session.prepare(SELECT_APPOINTMENTS_BY_DOCTOR)
        rows = session.execute(stmt, [doctor_id, appointment_date])

    if rows is None:
        print("You have no appointments.")
        return

    for row in rows:
        patientData = get_user(session, row.patient_id)
        print(" ")
        print("**** Appointment ****")
        date = time_uuid.TimeUUID.get_timestamp(row.appointment_id)
        date = datetime.fromtimestamp(date)
        print(f"=== Date: {date}")
        print(f"=== Patient: {patientData[3]} {patientData[4]}")
        print(f"=== Status: {row.status}")
        print(f"=== Notes: {row.notes}")

def get_appointments_by_patient_doctor(session, patient_id, doctor_id, appointment_date=None):
    if appointment_date:
        stmt = session.prepare(SELECT_APPOINTMENTS_BY_PATIENT_DOCTOR_DATE)
        endDate = appointment_date + dt.timedelta(days=1)
        rows = session.execute(stmt, [patient_id, doctor_id, appointment_date, endDate])
    else:
        appointment_date = datetime.datetime.now()
        stmt = session.prepare(SELECT_APPOINTMENTS_BY_PATIENT_DOCTOR)
        rows = session.execute(stmt, [patient_id, doctor_id, appointment_date])

    if rows is None:
        print("You have no appointments.")
        return

    for row in rows:
        patientData = get_user(session, row.patient_id)
        doctorData = get_user(session, row.doctor_id)
        print(" ")
        print("**** Appointment ****")
        date = time_uuid.TimeUUID.get_timestamp(row.appointment_id)
        date = datetime.fromtimestamp(date)
        print(f"=== Date: {date}")
        print(f"=== Doctor: {doctorData[3]} {doctorData[4]}")
        print(f"=== Patient: {patientData[3]} {patientData[4]}")
        print(f"=== Status: {row.status}")
        print(f"=== Notes: {row.notes}")

def insert_vital_sign(session, vitalSignData):
    vs_stmt = session.prepare(INSERT_VITAL_SIGN_BY_ACCOUNT_DATE)
    vsad_stmt = session.prepare(INSERT_VITAL_SIGN_BY_ACCOUNT_TYPE_DATE)

    execute_batch(session, vs_stmt, [vitalSignData])
    execute_batch(session, vsad_stmt, [vitalSignData])

def delete_vital_signs(session, account_id, start_date, end_date):
    vs_stmt = session.prepare(DELETE_VITAL_SIGNS_BY_ACCOUNT_DATE)
    vsad_stmt = session.prepare(DELETE_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE)

    if not start_date:
        start_date = datetime.now() - dt.timedelta(days=30)
    if not end_date:
        end_date = datetime.now()

    deleteVitalSigns = [account_id, start_date, end_date]
    execute_batch(session, vs_stmt, [deleteVitalSigns])

    vitalSignsTypes = ['blood pressure', 'heart rate', 'temperature', 'weight', 'height']
    for vitalSignType in vitalSignsTypes:
        deleteVitalSignsType = [account_id, vitalSignType, start_date, end_date]
        execute_batch(session, vsad_stmt, [deleteVitalSignsType])

def get_vital_signs(session, account_id, start_date=None, end_date=None, vital_sign_type=None):

    if vital_sign_type:
        stmt = session.prepare(SELECT_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE)
        rows = session.execute(stmt, [account_id, vital_sign_type, start_date, end_date])
    else:
        stmt = session.prepare(SELECT_VITAL_SIGNS_BY_ACCOUNT_DATE)
        rows = session.execute(stmt, [account_id, start_date, end_date])

    if rows is None:
        print("You have no vital signs registered.")
        return

    for row in rows:
        print(" ")
        print("**** Vital Sign ****")
        print(f"=== Date: {row.date}")
        print(f"=== Type: {row.type}")
        print(f"=== Value: {row.value}")


def insert_alert(session, alertData):

    stmt = session.prepare(INSERT_ALERT_BY_ACCOUNT_DATE)
    session.execute(stmt, alertData)

def get_alerts(session, account_id):
    date = datetime.now() - dt.timedelta(days=760)
    stmt = session.prepare(SELECT_ALERTS_BY_ACCOUNT)
    rows = session.execute(stmt, [account_id, date])

    if rows is None:
        print("You have no alerts in the last 30 days.")
        return

    for row in rows:
        print(" ")
        print("**** Alert ****")
        date = time_uuid.TimeUUID.get_timestamp(row.alert_id)
        date = datetime.fromtimestamp(date)
        print(f"=== Date: {date}")
        print(f"=== Type: {row.alert_type}")
        print(f"=== Message: {row.alert_message}")

def get_user(session, account_id):
    stmt = session.prepare(SELECT_ACCOUNTS)
    rows = session.execute(stmt, [account_id])
    return rows[0] if rows else None