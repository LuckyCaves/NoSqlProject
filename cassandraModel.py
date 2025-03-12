import time_uuid
import logging
from cassandra.query import BatchStatement

log = logging.getLogger()

CREATE_KEYSPACE ="""
    CREATE KEYSPACE IF NOT EXISTS {}
    WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': {}}};
"""

CREATE_PATIENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS patients (
        patient_id UUID,
        first_name TEXT,
        last_name TEXT,
        dob DATE
        PRIMARY KEY (patient_id)
    );
"""

CREATE_DOCTORS_TABLE = """
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id UUID,
        first_name TEXT,
        last_name TEXT,
        specialty TEXT,
        PRIMARY KEY (doctor_id)
    );
"""

CREATE_APPOINTMENTS_BY_PATIENT_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS appointments_by_patient (
        appointment_id TIMEUUID,
        appointment_date DATE,
        patient_id UUID,
        doctor_id UUID,
        status TEXT,
        notes TEXT,
        PRIMARY KEY (patient_id, appointment_id)
    )WITH CLUSTERING ORDER BY (appointment_id DESC);
"""

CREATE_APPOINTMENTS_BY_DOCTOR_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS appointments_by_doctor (
        appointment_id TIMEUUID,
        appointment_date DATE,
        patient_id UUID,
        doctor_id UUID,
        status TEXT,
        notes TEXT,
        PRIMARY KEY (doctor_name, appointment_id)
    )WITH CLUSTERING ORDER BY (appointment_id DESC);
"""

CREATE_APPOINTMENTS_BY_DATE_PD_TABLE = """
    CREATE TABLE IF NOT EXISTS appointments_by_pd (
        appointment_id TIMEUUID,
        appointment_date DATE,
        patient_id UUID,
        doctor_id UUID,
        status TEXT,
        notes TEXT,
        PRIMARY KEY ((patient_id, doctor_id), appointment_id)
    )WITH CLUSTERING ORDER BY (appointment_id DESC);
"""

CREATE_ACCOUNTS_BY_PATIENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS accounts_by_patient (
        account_id UUID,
        patient_id UUID,
        registration_date TIMEUUID,
        PRIMARY KEY (patient_id, account_id)
    );
"""

CREATE_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS vital_signs_by_type_date (
        vital_sign_id TIMEUUID,
        account_id UUID,
        type TEXT,
        value DOUBLE,
        date DATE,
        PRIMARY KEY (account_id, type, vital_sign_id)
    )WITH CLUSTERING ORDER BY (vital_sign_id DESC);
"""

CREATE_ACTIONS_BY_ACCOUNT_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS actions_by_account_date (
        action_id TIMEUUID,
        account_id UUID,
        date DATE,
        action_type TEXT,
        PRIMARY KEY (account_id, date, action_id)
"""

CREATE_ALERTS_BY_ACCOUNT_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS alerts_by_account_date (
        alert_id TIMEUUID,
        account_id UUID,
        date DATE,
        alert_type TEXT,
        alert_message TEXT,
        PRIMARY KEY (account_id, date, alert_id)
    );
"""

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor: {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

def create_schema(session):
    log.info("Creating Cassandra model schema")
    session.execute(CREATE_PATIENTS_TABLE)
    session.execute(CREATE_DOCTORS_TABLE)
    session.execute(CREATE_APPOINTMENTS_BY_PATIENT_DATE_TABLE)
    session.execute(CREATE_APPOINTMENTS_BY_DOCTOR_DATE_TABLE)
    session.execute(CREATE_APPOINTMENTS_BY_DATE_PD_TABLE)
    session.execute(CREATE_VITAL_SIGNS_BY_ACCOUNT_TYPE_DATE_TABLE)
    session.execute(CREATE_ACCOUNTS_BY_PATIENTS_TABLE)
    session.execute(CREATE_ACTIONS_BY_ACCOUNT_DATE_TABLE)
    session.execute(CREATE_ALERTS_BY_ACCOUNT_DATE_TABLE)

def exeute_batch(session, stmt, data):
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
    acc_stmt = session.prepare("INSERT INTO accounts_by_patient(account_id, patient_id, registration_date) VALUES (?, ?, ?)")
    vs_stmt = session.prepare("INSERT INTO vital_signs_by_type_date(vital_sign_id, account_id, type, value, date) VALUES (?, ?, ?, ?, ?)")
    act_stmt = session.prepare("INSERT INTO actions_by_account_date(action_id, account_id, date, action_type) VALUES (?, ?, ?, ?)")
    alert_stmt = session.prepare("INSERT INTO alerts_by_account_date(alert_id, account_id, date, alert_type, alert_message) VALUES (?, ?, ?, ?, ?)")

    

    # Generate trades by account
    data = []
    for i in range(trades_by_account):
        trade_id = random_date(datetime.datetime(2020, 1, 1), datetime.datetime(2025, 2, 28))
        acc = random.choice(accounts)
        sym = random.choice(INSTRUMENTS)
        trade_type = random.choice(['buy', 'sell'])
        shares = random.randint(1, 5000)
        price = random.uniform(0.1, 100000.0)
        amount = shares * price
        data.append((acc, trade_id, trade_type, sym, shares, price, amount))
    execute_batch(session, tad_stmt, data)
    execute_batch(session, tatd_stmt, data)
    execute_batch(session, tastd_stmt, data)
    execute_batch(session, tasd_stmt, data)