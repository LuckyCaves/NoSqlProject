import time_uuid
import logging
import datetime
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
        account_id, username, first_name, last_name, registration_date, role
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
"""

SELECT_APPOINTMENTS_BY_PATIENT_DATE = """
    SELECT
        appointment_id, appointment_date, patient_id, doctor_id, status, notes
    FROM appointments_by_patient
        WHERE patient_id = ?
        AND appointment_date = ?
"""

SELECT_APPOINTMENTS_BY_DOCTOR = """
    SELECT
        appointment_id, appointment_date, patient_id, doctor_id, status, notes
    FROM appointments_by_doctor
        WHERE doctor_id = ?
"""

SELECT_APPOINTMENTS_BY_DOCTOR_DATE = """
    SELECT
        appointment_id, appointment_date, patient_id, doctor_id, status, notes
    FROM appointments_by_doctor
        WHERE doctor_id = ?
        AND appointment_date = ?
"""

SELECT_ALERTS_BY_ACCOUNT = """
    SELECT
        alert_id, account_id, date, alert_type, alert_message
    FROM alerts_by_account_date
        WHERE account_id = ?
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

UPDATE_APPOINTMENT_DATE = """
    UPDATE appointments_by_date
        SET status = ?,
            notes = ?
        WHERE appointment_id = ?
"""

UPDATE_APPOINTMENT_PATIENT_DOCTOR = """
    UPDATE appointments_by_pd
        SET status = ?,
            notes = ?
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
    rand_date = start_date + datetime.timedelta(days=random_number_of_days)
    return rand_date

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor: {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

def create_schema(session):
    log.info("Creating Cassandra model schema")
    session.execute(CREATE_PATIENTS_TABLE)
    session.execute(CREATE_DOCTORS_TABLE)
    session.execute(CREATE_APPOINTMENTS_BY_DATE_TABLE)
    session.execute(CREATE_APPOINTMENTS_BY_PATIENT_DATE_TABLE)
    session.execute(CREATE_APPOINTMENTS_BY_DOCTOR_DATE_TABLE)
    session.execute(CREATE_APPOINTMENTS_BY_DATE_PD_TABLE)
    session.execute(CREATE_ACCOUNTS_TABLE)
    session.execute(CREATE_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE_TABLE)
    session.execute(CREATE_VITAL_SIGNS_BY_ACCOUNT_DATE_TABLE)
    session.execute(CREATE_ALERTS_BY_ACCOUNT_DATE_TABLE)
    session.execute(CREATE_ACTIONS_BY_ACCOUNT_DATE_TABLE) #Probalemente no se necesite

patientsData = [
    {"first_name": "John", "last_name": "Doe", "username": "jdoe"},
    {"first_name": "Alice", "last_name": "Smith", "username": "asmith"},
    {"first_name": "Bob", "last_name": "Johnson", "username": "bjohnson"},
    {"first_name": "Emma", "last_name": "White", "username": "ewhite"},
    {"first_name": "David", "last_name": "Martinez", "username": "dmartinez"},
    {"first_name": "Sophia", "last_name": "Brown", "username": "sbrown"},
    {"first_name": "Michael", "last_name": "Anderson", "username": "manderson"},
    {"first_name": "Olivia", "last_name": "Thomas", "username": "othomas"},
    {"first_name": "James", "last_name": "Harris", "username": "jharris"},
    {"first_name": "Charlotte", "last_name": "Wilson", "username": "cwilson"}
]

doctorsData = [
    {"first_name": "Liam", "last_name": "Davis", "username": "ldavis"},
    {"first_name": "Sophia", "last_name": "Miller", "username": "smiller"},
    {"first_name": "Noah", "last_name": "Garcia", "username": "ngarcia"},
    {"first_name": "Amelia", "last_name": "Rodriguez", "username": "arodriguez"},
    {"first_name": "Ethan", "last_name": "Lopez", "username": "elopez"},
    {"first_name": "Isabella", "last_name": "Gonzalez", "username": "igonzalez"},
    {"first_name": "Mason", "last_name": "Perez", "username": "mperez"},
    {"first_name": "Mia", "last_name": "Taylor", "username": "mtaylor"},
    {"first_name": "Lucas", "last_name": "Clark", "username": "lclark"},
    {"first_name": "Harper", "last_name": "Walker", "username": "hwalker"}
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
    appbt_stmt = session.prepare("INSERT INTO appointments_by_date(appointment_id, appointment_date, patient_id, doctor_id, status, notes) VALUES (?, ?, ?, ?, ?, ?)")
    appbpt_stmt = session.prepare("INSERT INTO appointments_by_patient(appointment_id, appointment_date, patient_id, doctor_id, status, notes) VALUES (?, ?, ?, ?, ?, ?)")
    appbdt_stmt = session.prepare("INSERT INTO appointments_by_doctor(appointment_id, appointment_date, patient_id, doctor_id, status, notes) VALUES (?, ?, ?, ?, ?, ?)")
    appbpd_stmt = session.prepare("INSERT INTO appointments_by_pd(appointment_id, appointment_date, patient_id, doctor_id, status, notes) VALUES (?, ?, ?, ?, ?, ?)")
    acc_stmt = session.prepare("INSERT INTO accounts(account_id, username, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)")
    vs_stmt = session.prepare("INSERT INTO vital_signs_by_type_date(vital_sign_id, account_id, type, value, date) VALUES (?, ?, ?, ?, ?)")
    vsad_stmt = session.prepare("INSERT INTO vital_signs_by_account_date(vital_sign_id, account_id, type, value, date) VALUES (?, ?, ?, ?, ?)")
    alert_stmt = session.prepare("INSERT INTO alerts_by_account_date(alert_id, account_id, date, alert_type, alert_message) VALUES (?, ?, ?, ?, ?)")
    act_stmt = session.prepare("INSERT INTO actions_by_account_date(action_id, account_id, date, action_type) VALUES (?, ?, ?, ?)")

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
        patient_uuid = str(uuid.uuid4())
        patients.append(patient_uuid)
        dob = random_date(datetime.datetime(1950, 1, 1), datetime.datetime(2008, 1, 1))
        data.append((patient_uuid, patient["first_name"], patient["last_name"], dob))
    execute_batch(session, pat_stmt, data)

    # Generate doctors
    data = []
    for index, doctor in enumerate(doctorsData):
        doctor_uuid = str(uuid.uuid4())
        doctors.append(doctor_uuid)
        data.append((doctor_uuid, doctor["first_name"], doctor["last_name"], specialists[index]))
    execute_batch(session, doc_stmt, data)

    # Generate appointments
    data = []
    for i in range(appointments):
        app_date = random_date(datetime.datetime(2020, 1, 1), datetime.datetime(2025, 2, 28))
        app_id = random_dateUUID(app_date)
        patient = random.choice(patients)
        doctor = random.choice(doctors)

        status = random.choice(['scheduled', 'completed', 'cancelled'])
        notes = random.choice(['', 'Patient needs to fast before the appointment', 'Patient needs to bring a urine sample'])
        data.append((app_id, app_date, patient, doctor, status, notes))
    execute_batch(session, appbt_stmt, data)
    execute_batch(session, appbpt_stmt, data)
    execute_batch(session, appbdt_stmt, data)
    execute_batch(session, appbpd_stmt, data)

    #Generate accounts doctors
    data = []
    for index, patient in enumerate(patients):
        account_id = patients[index]
        patientsAcc.append(account_id)
        registration_date = random_date(datetime.datetime(2020, 1, 1), datetime.datetime(2021, 1, 1))
        registration_date = random_dateUUID(registration_date)
        data.append((account_id, patientsData[index]["username"], patientsData[index]["first_name"], patientsData[index]["last_name"], registration_date, 'patient'))
    execute_batch(session, acc_stmt, data)
    
    # Generate accounts doctors
    data = []
    for index, doctor in enumerate(doctors):
        account_id = doctors[index]
        doctorsAcc.append(account_id)
        registration_date = random_date(datetime.datetime(2020, 1, 1), datetime.datetime(2021, 1, 1))
        registration_date = random_dateUUID(registration_date)
        data.append((account_id, doctorsData[index]["username"], doctorsData[index]["first_name"], doctorsData[index]["last_name"], registration_date, 'doctor'))
    execute_batch(session, acc_stmt, data)

    # Generate vital signs
    data = []
    for i in range(vital_signs):
        account = random.choice(patientsAcc)
        vital_sign_type = random.choice(['blood pressure', 'heart rate', 'temperature', 'weight', 'height'])
        vital_sign_value = random.uniform(0, 100)
        vital_sign_date = random_date(datetime.datetime(2020, 1, 1), datetime.datetime(2025, 1, 1))
        vital_sign_id = random_dateUUID(vital_sign_date)
        data.append((vital_sign_id, account, vital_sign_type, vital_sign_value, vital_sign_date))
    execute_batch(session, vs_stmt, data)
    execute_batch(session, vsad_stmt, data)

    # Generate actions
    data = []
    for i in range(actions):
        account = random.choice(patientsAcc)
        action_date = random_date(datetime.datetime(2020, 1, 1), datetime.datetime(2025, 1, 1))
        action_id = random_dateUUID(action_date)
        action_type = random.choice(['appointment', 'vital_sign', 'alert'])
        data.append((action_id, account, action_date, action_type))
    execute_batch(session, act_stmt, data)

    # Generate alerts
    data = []
    for i in range(alerts):
        account = random.choice(patientsAcc)
        alert_date = random_date(datetime.datetime(2020, 1, 1), datetime.datetime(2025, 1, 1))
        alert_id = random_dateUUID(alert_date)
        alert_type = random.choice(['appointment', 'vital_sign', 'alert'])
        alert_message = random.choice(['Appointment scheduled', 'Vital sign out of range', 'New alert'])
        data.append((alert_id, account, alert_date, alert_type, alert_message))
    execute_batch(session, alert_stmt, data)

def create_account(session, accountData):
    stmt = session.prepare(INSERT_ACCOUNT)
    session.execute(stmt, (accountData["account_id"], accountData["username"], 
                           accountData["first_name"], accountData["last_name"], 
                           accountData["registration_date"], accountData["role"]))

def insert_patient(session, patientData):
    stmt = session.prepare(INSERT_PATIENT)
    session.execute(stmt, (patientData["patient_id"], patientData["first_name"], 
                           patientData["last_name"], patientData["dob"]))

def insert_doctor(session, doctorData):
    stmt = session.prepare(INSERT_DOCTOR)
    session.execute(stmt, (doctorData["doctor_id"], doctorData["first_name"], 
                           doctorData["last_name"], doctorData["specialty"]))

def insert_appointment(session, appointmentData):

    appbt_stmt = session.prepare(INSERT_APPOINTMENT_BY_DATE)
    appbpt_stmt = session.prepare(INSERT_APPOINTMENT_BY_PATIENT)
    appbdt_stmt = session.prepare(INSERT_APPOINTMENT_BY_DOCTOR)
    appbpd_stmt = session.prepare(INSERT_APPOINTMENT_BY_PD)

    execute_batch(session, appbt_stmt, [appointmentData])
    execute_batch(session, appbpt_stmt, [appointmentData])
    execute_batch(session, appbdt_stmt, [appointmentData])
    execute_batch(session, appbpd_stmt, [appointmentData])

def update_appointment(session, appointmentData):
    appbt_stmt = session.prepare(UPDATE_APPOINTMENT_DATE)
    appbpt_stmt = session.prepare(UPDATE_APPOINTMENT_PATIENT)
    appbdt_stmt = session.prepare(UPDATE_APPOINTMENT_DOCTOR)
    appbpd_stmt = session.prepare(UPDATE_APPOINTMENT_PATIENT_DOCTOR)

    execute_batch(session, appbt_stmt, [appointmentData])
    execute_batch(session, appbpt_stmt, [appointmentData])
    execute_batch(session, appbdt_stmt, [appointmentData])
    execute_batch(session, appbpd_stmt, [appointmentData])

def get_appointments_by_patient(session, patient_id, appointment_date=None):

    if appointment_date:
        stmt = session.prepare(SELECT_APPOINTMENTS_BY_PATIENT)
        rows = session.execute(stmt, [patient_id, appointment_date])
    else:
        stmt = session.prepare(SELECT_APPOINTMENTS_BY_PATIENT_DATE)
        rows = session.execute(stmt, [patient_id, appointment_date])
    
    return rows if rows else None

def get_appointments_by_doctor(session, doctor_id, appointment_date=None):
    if appointment_date:
        stmt = session.prepare(SELECT_APPOINTMENTS_BY_DOCTOR)
        rows = session.execute(stmt, [doctor_id, appointment_date])
    else:
        stmt = session.prepare(SELECT_APPOINTMENTS_BY_DOCTOR_DATE)
        rows = session.execute(stmt, [doctor_id, appointment_date])
    
    return rows if rows else None

def insert_vital_sign(session, vitalSignData):
    vs_stmt = session.prepare(INSERT_VITAL_SIGN_BY_ACCOUNT_DATE)
    vsad_stmt = session.prepare(INSERT_VITAL_SIGN_BY_ACCOUNT_TYPE_DATE)

    execute_batch(session, vs_stmt, [vitalSignData])
    execute_batch(session, vsad_stmt, [vitalSignData])

def delete_vital_signs(session, account_id, start_date, end_date):
    vs_stmt = session.prepare(DELETE_VITAL_SIGNS_BY_ACCOUNT_DATE)
    vsad_stmt = session.prepare(DELETE_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE)

    execute_batch(session, vs_stmt, [account_id, start_date, end_date])
    execute_batch(session, vsad_stmt, [account_id, start_date, end_date])

def get_vital_signs(session, account_id, start_date=None, end_date=None, vital_sign_type=None):

    if not start_date:
        start_date = datetime.date.today() - datetime.timedelta(days=30)
    if not end_date:
        end_date = datetime.date.today()

    if vital_sign_type:
        stmt = session.prepare(SELECT_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE)
        rows = session.execute(stmt, [account_id, vital_sign_type, start_date, end_date])
    else:
        stmt = session.prepare(SELECT_VITAL_SIGNS_BY_ACCOUNT_DATE)
        rows = session.execute(stmt, [account_id, start_date, end_date])

    return rows if rows else None

def insert_alert(session, alertData):

    stmt = session.prepare(INSERT_ALERT_BY_ACCOUNT_DATE)
    session.execute(stmt, (alertData["alert_id"], alertData["account_id"], 
                           alertData["date"], alertData["alert_type"], 
                           alertData["alert_message"]))

def get_alerts(session, account_id):
    stmt = session.prepare(SELECT_ALERTS_BY_ACCOUNT)
    rows = session.execute(stmt, [account_id])
    return rows if rows else None

def get_user(session, account_id):
    stmt = session.prepare(SELECT_ACCOUNTS)
    rows = session.execute(stmt, [account_id])
    return rows[0] if rows else None