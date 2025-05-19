#!/usr/bin/env python3
import datetime
import json
import csv


import pydgraph

def set_schema(client):
    schema = """
    patient_id: string @index(exact) .
    name: string @index(term) .
    date_of_birth: datetime .
    gender: string .
    blood_type: string @index(exact) .

    doctor_id: string @index(exact) .
    license_number: string .
    years_experience: int @index(int) .

    specialty_id: string @index(exact) .
    description: string .

    treatment_id: string @index(exact) .
    start_date: datetime .
    end_date: datetime .
    effectiveness_score: float @index(float) .

    medication_id: string @index(exact) .
    dosage: string .
    frequency: string .
    route: string .

    effect_id: string @index(exact) .
    severity: string @index(exact) .

    team_id: string @index(exact) .
    formation_date: datetime .
    purpose: string .

    disease_id: string @index(exact) .
    hereditary_risk: float @index(float) .

    symptom_id: string @index(exact) .

    rehabilitation_id: string @index(exact) .
    rehabilitation_duration: int @index(int) .
    condition_severity: string @index(exact) .

    
    family_relation: [uid] @reverse .
    has_symptom: [uid] .
    attends: [uid] @reverse .
    recomends: [uid] @reverse .
    specializes: [uid] @reverse .
    part_of: [uid] @reverse .
    cure: [uid] @reverse .
    has_medication: [uid] .
    interact_with: [uid] @reverse .
    cause: [uid] .
    treats: [uid] .
    diagnosed: [uid] .
    require: [uid] .
  

    
    type Patient {
      patient_id
      name
      date_of_birth
      gender
      blood_type
    }

    type Doctor {
      doctor_id
      name
      license_number
      years_experience


    }

    type Specialty {
      specialty_id
      name
      description
    }

    type Treatment {
      treatment_id
      name
      description
      start_date
      end_date
      effectiveness_score
    }

    type Medication {
      medication_id
      name
      dosage
      frequency
      route

    }

    type SideEffect {
      effect_id
      name
      description
      severity
    }

    type TreatmentTeam {
      team_id
      name
      formation_date
      purpose

    }

    type Disease {
      disease_id
      name
      hereditary_risk
      description
    }

    type Symptom {
      symptom_id
      name
      description
      severity

    }

    type RehabilitationTime {
      rehabilitation_id
      rehabilitation_duration
      condition_severity
    }
    """
    return client.alter(pydgraph.Operation(schema=schema))

#load data from csvs

def load_patients(client):
    txn = client.txn()
    try:
        patients = []
        with open('csvs/nodes/patients_Dgraph.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                patients.append({
                    'uid': f'_:{row["patient_id"]}',
                    'dgraph.type': 'Patient',
                    'patient_id': row['patient_id'],
                    'name': row['name'],
                    'date_of_birth': row['date_of_birth'],
                    'gender': row['gender'],
                    'blood_type': row['blood_type']
                })
        assigned = txn.mutate(set_obj=patients)
        print(f"Loaded {len(patients)} patients. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
        return assigned.uids

def load_doctors(client):
    txn = client.txn()
    try:
        doctors = []
        with open('csvs/nodes/doctors_Dgraph.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                doctors.append({
                    'uid': f'_:{row["doctor_id"]}',
                    'dgraph.type': 'Doctor',
                    'doctor_id': row['doctor_id'],
                    'name': row['name'],
                    'license_number': row['license_number'],
                    'years_experience': int(row['years_experience'])
                })
        assigned = txn.mutate(set_obj=doctors)
        txn.commit()
        print(f"Loaded {len(doctors)} doctors.")
        return assigned.uids
    finally:
        txn.discard()

def load_specialties(client):
    txn = client.txn()
    try:
        specialties = []
        with open('csvs/nodes/specialty.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                specialties.append({
                    'uid': f'_:{row["specialty_id"]}',
                    'dgraph.type': 'Specialty',
                    'specialty_id': row['specialty_id'],
                    'name': row['name'],
                    'description': row['description']
                })
        assigned = txn.mutate(set_obj=specialties)
        txn.commit()
        print(f"Loaded {len(specialties)} specialties.")
        return assigned.uids
    finally:
        txn.discard()

def load_treatments(client):
    txn = client.txn()
    try:
        treatments = []
        with open('csvs/nodes/treatments.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                treatments.append({
                    'uid': f'_:{row["treatment_id"]}',
                    'dgraph.type': 'Treatment',
                    'treatment_id': row['treatment_id'],
                    'name': row['name'],
                    'description': row['description'],
                    'start_date': row['start_date'],
                    'end_date': row['end_date'],
                    'effectiveness_score': float(row['effectiveness_score'])
                })
        assigned = txn.mutate(set_obj=treatments)
        txn.commit()
        print(f"Loaded {len(treatments)} treatments.")
        return assigned.uids
    finally:
        txn.discard()

def load_medications(client):
    txn = client.txn()
    try:
        medications = []
        with open('csvs/nodes/medication.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                medications.append({
                    'uid': f'_:{row["medication_id"]}',
                    'dgraph.type': 'Medication',
                    'medication_id': row['medication_id'],
                    'name': row['name'],
                    'dosage': row['dosage'],
                    'frequency': row['frequency'],
                    'route': row['route']
                })
        assigned = txn.mutate(set_obj=medications)
        txn.commit()
        print(f"Loaded {len(medications)} medications.")
        return assigned.uids
    finally:
        txn.discard()

def load_side_effects(client):
    txn = client.txn()
    try:
        effects = []
        with open('csvs/nodes/sideEffect.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                effects.append({
                    'uid': f'_:{row["effect_id"]}',
                    'dgraph.type': 'SideEffect',
                    'effect_id': row['effect_id'],
                    'name': row['name'],
                    'description': row['description'],
                    'severity': row['severity']
                })
        assigned = txn.mutate(set_obj=effects)
        txn.commit()
        print(f"Loaded {len(effects)} side effects.")
        return assigned.uids
    finally:
        txn.discard()

def load_treatment_teams(client):
    txn = client.txn()
    try:
        teams = []
        with open('csvs/nodes/treatmentTeam.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                teams.append({
                    'uid': f'_:{row["team_id"]}',
                    'dgraph.type': 'TreatmentTeam',
                    'team_id': row['team_id'],
                    'name': row['name'],
                    'formation_date': row['formation_date'],
                    'purpose': row['purpose']
                })
        assigned = txn.mutate(set_obj=teams)
        txn.commit()
        print(f"Loaded {len(teams)} treatment teams.")
        return assigned.uids
    finally:
        txn.discard()

def load_diseases(client):
    txn = client.txn()
    try:
        diseases = []
        with open('csvs/nodes/diseases.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                diseases.append({
                    'uid': f'_:{row["disease_id"]}',
                    'dgraph.type': 'Disease',
                    'disease_id': row['disease_id'],
                    'name': row['name'],
                    'hereditary_risk': float(row['hereditary_risk']),
                    'description': row['description']
                })
        assigned = txn.mutate(set_obj=diseases)
        txn.commit()
        print(f"Loaded {len(diseases)} diseases.")
        return assigned.uids
    finally:
        txn.discard()

def load_symptoms(client):
    txn = client.txn()
    try:
        symptoms = []
        with open('csvs/nodes/symptoms.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                symptoms.append({
                    'uid': f'_:{row["symptom_id"]}',
                    'dgraph.type': 'Symptom',
                    'symptom_id': row['symptom_id'],
                    'name': row['name'],
                    'description': row['description'],
                    'severity': row['severity']
                })
        assigned = txn.mutate(set_obj=symptoms)
        txn.commit()
        print(f"Loaded {len(symptoms)} symptoms.")
        return assigned.uids
    finally:
        txn.discard()

def load_rehabilitations(client):
    txn = client.txn()
    try:
        rehabilitations = []
        with open('csvs/nodes/rehabilitationTime.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                rehabilitations.append({
                    'uid': f'_:{row["rehabilitation_id"]}',
                    'dgraph.type': 'RehabilitationTime',
                    'rehabilitation_id': row['rehabilitation_id'],
                    'rehabilitation_duration': int(row['rehabilitation_duration']),
                    'condition_severity': row['condition_severity']
                })
        assigned = txn.mutate(set_obj=rehabilitations)
        txn.commit()
        print(f"Loaded {len(rehabilitations)} rehabilitations.")
        return assigned.uids
    finally:
        txn.discard()


#load relations 

def load_family_relation(client, patient_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/family_relation.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = patient_uids.get(row['uid'])
                uid2 = patient_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in family_relation row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'family_relation': [{'uid': uid2}]})
        txn.commit()
        print("Loaded family_relation relationships.")
    finally:
        txn.discard()


def load_has_symptom(client, patient_uids, symptom_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/has_symptom.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = patient_uids.get(row['uid'])
                uid2 = symptom_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in has_symptom row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'has_symptom': [{'uid': uid2}]})
        txn.commit()
        print("Loaded has_symptom relationships.")
    finally:
        txn.discard()


def load_attends(client, patient_uids, doctor_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/attends.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = doctor_uids.get(row['uid'])
                uid2 = patient_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in attends row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'attends': [{'uid': uid2}]})
        txn.commit()
        print("Loaded attends relationships.")
    finally:
        txn.discard()


def load_recomends(client, doctor_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/recomends.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = doctor_uids.get(row['uid'])
                uid2 = doctor_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in recomends row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'recomends': [{'uid': uid2}]})
        txn.commit()
        print("Loaded recomends relationships.")
    finally:
        txn.discard()


def load_specializes(client, doctor_uids, specialty_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/specializes.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = doctor_uids.get(row['uid'])
                uid2 = specialty_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in specializes row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'specializes': [{'uid': uid2}]})
        txn.commit()
        print("Loaded specializes relationships.")
    finally:
        txn.discard()


def load_part_of(client, doctor_uids, team_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/part_of.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = doctor_uids.get(row['uid'])
                uid2 = team_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in part_of row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'part_of': [{'uid': uid2}]})
        txn.commit()
        print("Loaded part_of relationships.")
    finally:
        txn.discard()


def load_treats(client, team_uids, patient_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/treats.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = team_uids.get(row['uid'])
                uid2 = patient_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in treats row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'treats': [{'uid': uid2}]})
        txn.commit()
        print("Loaded treats relationships.")
    finally:
        txn.discard()


def load_cure(client, treatment_uids, disease_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/cure.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = treatment_uids.get(row['uid'])
                uid2 = disease_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in cure row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'cure': [{'uid': uid2}]})
        txn.commit()
        print("Loaded cure relationships.")
    finally:
        txn.discard()


def load_has_medication(client, treatment_uids, medication_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/has_medication.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = treatment_uids.get(row['uid'])
                uid2 = medication_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in has_medication row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'has_medication': [{'uid': uid2}]})
        txn.commit()
        print("Loaded has_medication relationships.")
    finally:
        txn.discard()


def load_require(client, treatment_uids, rehabilitation_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/require.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = treatment_uids.get(row['uid'])
                uid2 = rehabilitation_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in requires row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'require': [{'uid': uid2}]})
        txn.commit()
        print("Loaded require relationships.")
    finally:
        txn.discard()


def load_cause(client, medication_uids, effect_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/cause.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = medication_uids.get(row['uid'])
                uid2 = effect_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in causes row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'cause': [{'uid': uid2}]})
        txn.commit()
        print("Loaded cause relationships.")
    finally:
        txn.discard()


def load_interacts_with(client, medication_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/interacts_with.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = medication_uids.get(row['uid'])
                uid2 = medication_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in interacts_with row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'interact_with': [{'uid': uid2}]})
        txn.commit()
        print("Loaded interact_with relationships.")
    finally:
        txn.discard()


def load_diagnosed(client, symptom_uids, disease_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/diagnosed.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                uid1 = symptom_uids.get(row['uid'])
                uid2 = disease_uids.get(row['uid2'])
                if not uid1 or not uid2:
                    print(f"Warning: Missing UID(s) in diagnosed row: {row}")
                    continue
                txn.mutate(set_obj={'uid': uid1, 'diagnosed': [{'uid': uid2}]})
        txn.commit()
        print("Loaded diagnosed relationships.")
    finally:
        txn.discard()



def load_data(client):
    # Load nodes
    patient_uids = load_patients(client)
    doctor_uids = load_doctors(client)
    specialty_uids = load_specialties(client)
    treatment_uids = load_treatments(client)
    medication_uids = load_medications(client)
    side_effects_uids = load_side_effects(client)
    treatment_teams_uids = load_treatment_teams(client)
    diseases_uids = load_diseases(client)
    symptoms_uids = load_symptoms(client)
    rehabilitation_uids = load_rehabilitations(client)

    # Load relations
    load_family_relation(client, patient_uids)
    load_has_symptom(client, patient_uids, symptoms_uids)
    load_attends(client, patient_uids, doctor_uids)
    load_recomends(client, doctor_uids)
    load_specializes(client, doctor_uids, specialty_uids)
    load_part_of(client, doctor_uids, treatment_teams_uids)
    load_treats(client, treatment_teams_uids, patient_uids)
    load_cure(client, treatment_uids, diseases_uids)
    load_has_medication(client, treatment_uids, medication_uids)
    load_require(client, treatment_uids, rehabilitation_uids)
    load_cause(client, medication_uids, side_effects_uids)
    load_interacts_with(client, medication_uids)
    load_diagnosed(client, symptoms_uids, diseases_uids)
    print("Data loaded successfully.")
    
#querys
def get_doctors_for_patient(client, patient_id_value):
    query = """
    query getDoctors($patient_id: string) {
      patient(func: eq(patient_id, $patient_id)) {
        uid
        patient_id
        name
        ~attends { 
          uid
          doctor_id
          name
          license_number
          years_experience
        }
      }
    }
    """
    variables = {'$patient_id': patient_id_value}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(f"\n--- Reporte de Médicos para el Paciente ID: {patient_id_value} ---")

    if not data.get('patient'):
        print("No se encontró información para el paciente especificado.")
        print("--- Fin del Reporte ---")
        return

    patient_list = data['patient']

    if not patient_list:
        print(f"Paciente con ID '{patient_id_value}' no encontrado.")
        print("--- Fin del Reporte ---")
        return

    patient_data = patient_list[0]
    
    print("\nInformación del Paciente:")
    print(f"  ID del Paciente: {patient_data.get('patient_id', 'N/A')}")
    print(f"  Nombre: {patient_data.get('name', 'N/A')}")

    doctors_list = patient_data.get('~attends', []) 

    if not doctors_list:
        print("\nEste paciente no tiene médicos asignados actualmente.")
    else:
        print("\nMédicos que atienden al paciente:")
        for i, doctor in enumerate(doctors_list, 1):
            print(f"\n  Médico {i}:")
            print(f"    ID del Doctor: {doctor.get('doctor_id', 'N/A')}")
            print(f"    Nombre: {doctor.get('name', 'N/A')}")
            print(f"    Número de Licencia: {doctor.get('license_number', 'N/A')}")
            print(f"    Años de Experiencia: {doctor.get('years_experience', 'N/A')}")

    print("\n--- Fin del Reporte ---")


def get_patients_for_doctor(client, doctor_id_value):
    query = """
    query getPatients($doctor_id: string) {
      doctor(func: eq(doctor_id, $doctor_id)) {
        uid
        doctor_id
        name
        attends { 
          uid
          patient_id
          name
          gender
          blood_type
        }
      }
    }
    """
    variables = {'$doctor_id': doctor_id_value}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(f"\n--- Reporte de Pacientes para el Doctor ID: {doctor_id_value} ---")

    if not data.get('doctor'):
        print("No se encontró información para el doctor especificado.")
        print("--- Fin del Reporte ---")
        return

    doctor_list = data['doctor']

    if not doctor_list:
        print(f"Doctor con ID '{doctor_id_value}' no encontrado.")
        print("--- Fin del Reporte ---")
        return

    doctor_data = doctor_list[0]
    
    print("\nInformación del Doctor:")
    print(f"  ID del Doctor: {doctor_data.get('doctor_id', 'N/A')}")
    print(f"  Nombre: {doctor_data.get('name', 'N/A')}")

    patients_list = doctor_data.get('attends', [])

    if not patients_list:
        print("\nEste doctor no tiene pacientes asignados actualmente.")
    else:
        print("\nPacientes atendidos por este doctor:")
        for i, patient in enumerate(patients_list, 1):
            print(f"\n  Paciente {i}:")
            print(f"    ID del Paciente: {patient.get('patient_id', 'N/A')}")
            print(f"    Nombre: {patient.get('name', 'N/A')}")
            print(f"    Género: {patient.get('gender', 'N/A')}")
            print(f"    Tipo de Sangre: {patient.get('blood_type', 'N/A')}")

    print("\n--- Fin del Reporte ---")



def get_patient_health_summary(client, patient_id_value):
    query = """
    query getPatientSummary($patient_id: string) {
      patient(func: eq(patient_id, $patient_id)) {
        uid
        patient_id
        name
        
        has_symptom { 
          uid
          symptom_id
          name
          description
          severity
          
          diagnosed { 
            uid
            disease_id
            name
            hereditary_risk
            description
            
            ~cure { 
              uid
              treatment_id
              name
              description
              effectiveness_score
              
              has_medication { 
                uid
                medication_id
                name
                dosage
                frequency
                route
              }
            }
          }
        }
      }
    }
    """
    variables = {'$patient_id': patient_id_value}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(f"\n--- Resumen de Salud para el Paciente ID: {patient_id_value} ---")

    if not data.get('patient'):
        print("No se encontró información para el paciente especificado.")
        print("--- Fin del Reporte ---")
        return

    patient_data = data['patient'][0]
    
    print("\nInformación del Paciente:")
    print(f"  ID del Paciente: {patient_data.get('patient_id', 'N/A')}")
    print(f"  Nombre: {patient_data.get('name', 'N/A')}")

    symptoms = patient_data.get('has_symptom', [])
    if not symptoms:
        print("\nNo se encontraron síntomas registrados para este paciente.")
    else:
        print("\nSíntomas registrados:")
        for i, symptom in enumerate(symptoms, 1):
            print(f"\n  Síntoma {i}:")
            print(f"    ID: {symptom.get('symptom_id', 'N/A')}")
            print(f"    Nombre: {symptom.get('name', 'N/A')}")
            print(f"    Descripción: {symptom.get('description', 'N/A')}")
            print(f"    Severidad: {symptom.get('severity', 'N/A')}")
            
            diagnoses = symptom.get('diagnosed', [])
            if not diagnoses:
                print("    → No se encontraron diagnósticos para este síntoma.")
            else:
                print("    Diagnósticos:")
                for j, diagnosis in enumerate(diagnoses, 1):
                    print(f"      Diagnóstico {j}:")
                    print(f"        ID de Enfermedad: {diagnosis.get('disease_id', 'N/A')}")
                    print(f"        Nombre: {diagnosis.get('name', 'N/A')}")
                    print(f"        Descripción: {diagnosis.get('description', 'N/A')}")
                    print(f"        Riesgo Hereditario: {diagnosis.get('hereditary_risk', 'N/A')}")
                    
                    cures = diagnosis.get('~cure', [])
                    if not cures:
                        print("        → No se encontraron tratamientos para esta enfermedad.")
                    else:
                        print("        Tratamientos:")
                        for k, cure in enumerate(cures, 1):
                            print(f"          Tratamiento {k}:")
                            print(f"            ID: {cure.get('treatment_id', 'N/A')}")
                            print(f"            Nombre: {cure.get('name', 'N/A')}")
                            print(f"            Descripción: {cure.get('description', 'N/A')}")
                            print(f"            Efectividad: {cure.get('effectiveness_score', 'N/A')}")
                            
                            meds = cure.get('has_medication', [])
                            if not meds:
                                print("            → No se encontraron medicamentos asociados.")
                            else:
                                print("            Medicamentos:")
                                for m, med in enumerate(meds, 1):
                                    print(f"              Medicamento {m}:")
                                    print(f"                ID: {med.get('medication_id', 'N/A')}")
                                    print(f"                Nombre: {med.get('name', 'N/A')}")
                                    print(f"                Dosis: {med.get('dosage', 'N/A')}")
                                    print(f"                Frecuencia: {med.get('frequency', 'N/A')}")
                                    print(f"                Vía de Administración: {med.get('route', 'N/A')}")

    print("\n--- Fin del Reporte ---")



def get_doctors_by_specialty_name(client, specialty_name_value):
    query = """
    query FindDoctorsBySpecialtyName($specialtyName: string!) {
      specialty_doctors(func: eq(name, $specialtyName)) {
        uid
        specialty_id
        name_of_specialty: name 
        
        doctors_in_specialty: ~specializes @filter(has(doctor_id)) { 
          uid
          doctor_id
          name
          license_number
          years_experience
        }
      }
    }
    """
    variables = {
        '$specialtyName': specialty_name_value
    }
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(f"\n--- Reporte de Doctores para la Especialidad: \"{specialty_name_value}\" ---")

    if not data.get('specialty_doctors'):
        print("No se encontró información para la especialidad especificada.")
        print("--- Fin del Reporte ---")
        return

    specialty_list = data['specialty_doctors']

    if not specialty_list:
        print(f"Especialidad con nombre '{specialty_name_value}' no encontrada.")
        print("--- Fin del Reporte ---")
        return

    specialty_data = specialty_list[0]
    
    print("\nInformación de la Especialidad:")
    print(f"  ID de la Especialidad: {specialty_data.get('specialty_id', 'N/A')}")
    print(f"  Nombre: {specialty_data.get('name_of_specialty', 'N/A')}")

    doctors_list = specialty_data.get('doctors_in_specialty', [])

    if not doctors_list:
        print("\nNo hay doctores registrados con esta especialidad actualmente.")
    else:
        print("\nDoctores que tienen esta especialidad:")
        for i, doctor in enumerate(doctors_list, 1):
            print(f"\n  Doctor {i}:")
            print(f"    ID del Doctor: {doctor.get('doctor_id', 'N/A')}")
            print(f"    Nombre: {doctor.get('name', 'N/A')}")
            print(f"    Número de Licencia: {doctor.get('license_number', 'N/A')}")
            print(f"    Años de Experiencia: {doctor.get('years_experience', 'N/A')}")

    print("\n--- Fin del Reporte ---")




def get_treatments_and_medications_for_disease_by_name(client, disease_name_value):
    query = """
    query FindTreatmentsForDiseaseByName($diseaseName: string!) {
      disease_treatment_info(func: eq(name, $diseaseName)) { 
        uid
        disease_id
        name_of_disease: name 
        description_of_disease: description 

        recommended_treatments: ~cure @filter(has(treatment_id)) {
          uid
          treatment_id
          name_of_treatment: name
          description_of_treatment: description
          start_date
          end_date
          effectiveness_score

          medications_in_treatment: has_medication @filter(has(medication_id)) {
            uid
            medication_id
            name_of_medication: name
            dosage
            frequency
            route
          }
        }
      }
    }
    """
    variables = {'$diseaseName': disease_name_value}
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)

    print(f"\n--- Reporte de Tratamientos y Medicamentos para la Enfermedad: \"{disease_name_value}\" ---")

    if not data.get('disease_treatment_info'):
        print("No se encontró información para la enfermedad especificada.")
        print("--- Fin del Reporte ---")
        return

    disease_list = data['disease_treatment_info']

    if not disease_list:
        print(f"Enfermedad con nombre '{disease_name_value}' no encontrada.")
        print("--- Fin del Reporte ---")
        return

    disease_data = disease_list[0]

    print("\nInformación de la Enfermedad:")
    print(f"  ID de la Enfermedad: {disease_data.get('disease_id', 'N/A')}")
    print(f"  Nombre: {disease_data.get('name_of_disease', 'N/A')}")
    print(f"  Descripción: {disease_data.get('description_of_disease', 'N/A')}")

    treatments = disease_data.get('recommended_treatments', [])

    if not treatments:
        print("\nNo hay tratamientos registrados para esta enfermedad.")
    else:
        print("\nTratamientos recomendados:")
        for i, treatment in enumerate(treatments, 1):
            print(f"\n  Tratamiento {i}:")
            print(f"    ID del Tratamiento: {treatment.get('treatment_id', 'N/A')}")
            print(f"    Nombre: {treatment.get('name_of_treatment', 'N/A')}")
            print(f"    Descripción: {treatment.get('description_of_treatment', 'N/A')}")
            print(f"    Fecha de Inicio: {treatment.get('start_date', 'N/A')}")
            print(f"    Fecha de Fin: {treatment.get('end_date', 'N/A')}")
            print(f"    Efectividad: {treatment.get('effectiveness_score', 'N/A')}")

            medications = treatment.get('medications_in_treatment', [])
            if not medications:
                print("    No hay medicamentos registrados para este tratamiento.")
            else:
                print("    Medicamentos en este tratamiento:")
                for j, medication in enumerate(medications, 1):
                    print(f"      Medicamento {j}:")
                    print(f"        ID: {medication.get('medication_id', 'N/A')}")
                    print(f"        Nombre: {medication.get('name_of_medication', 'N/A')}")
                    print(f"        Dosis: {medication.get('dosage', 'N/A')}")
                    print(f"        Frecuencia: {medication.get('frequency', 'N/A')}")
                    print(f"        Vía de Administración: {medication.get('route', 'N/A')}")

    print("\n--- Fin del Reporte ---")


def get_side_effects_for_medication_by_name(client, medication_name_value):
    query = """
    query FindSideEffects($med_name: string!) {
      medication_info(func: eq(name, $med_name)) {
        uid
        medication_id
        name_of_medication: name 
        dosage
        frequency
        route
        reported_side_effects: cause @filter(has(effect_id)) { 
          uid
          effect_id
          name_of_side_effect: name
          description_of_side_effect: description
          severity
        }
      }
    }
    """
    variables = {'$med_name': medication_name_value}
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)

    print(f"\n--- Reporte de Efectos Secundarios para el Medicamento: {medication_name_value} ---")

    if not data.get('medication_info'):
        print("No se encontró información para el medicamento especificado.")
        print("--- Fin del Reporte ---")
        return

    medication_list = data['medication_info']

    if not medication_list:
        print(f"Medicamento con nombre '{medication_name_value}' no encontrado.")
        print("--- Fin del Reporte ---")
        return

    medication_data = medication_list[0]

    print("\nInformación del Medicamento:")
    print(f"  ID del Medicamento: {medication_data.get('medication_id', 'N/A')}")
    print(f"  Nombre: {medication_data.get('name_of_medication', 'N/A')}")
    print(f"  Dosis: {medication_data.get('dosage', 'N/A')}")
    print(f"  Frecuencia: {medication_data.get('frequency', 'N/A')}")
    print(f"  Vía de Administración: {medication_data.get('route', 'N/A')}")

    side_effects = medication_data.get('reported_side_effects', [])

    if not side_effects:
        print("\nEste medicamento no tiene efectos secundarios reportados.")
    else:
        print("\nEfectos Secundarios Reportados:")
        for i, effect in enumerate(side_effects, 1):
            print(f"\n  Efecto Secundario {i}:")
            print(f"    ID: {effect.get('effect_id', 'N/A')}")
            print(f"    Nombre: {effect.get('name_of_side_effect', 'N/A')}")
            print(f"    Descripción: {effect.get('description_of_side_effect', 'N/A')}")
            print(f"    Severidad: {effect.get('severity', 'N/A')}")

    print("\n--- Fin del Reporte ---")



def get_team_composition_and_patients_by_name(client, team_name_value):
    query = """
    query GetTeamInfoByName($team_name_filter: string!) {
      team_details(func: eq(name, $team_name_filter)) {
        uid
        team_id
        name_of_team: name
        formation_date
        purpose

        patients_treated_by_team: treats @filter(has(patient_id)) {
          uid
          patient_id
          name_of_patient: name
        }

        doctors_in_team: ~part_of @filter(has(doctor_id)) {
          uid
          doctor_id
          name_of_doctor: name
        }
      }
    }
    """
    variables = {'$team_name_filter': team_name_value}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)

    print(f"\n--- Reporte de Composición del Equipo: \"{team_name_value}\" ---")

    if not data.get('team_details'):
        print("No se encontró información para el equipo especificado.")
        print("--- Fin del Reporte ---")
        return

    team_list = data['team_details']

    if not team_list:
        print(f"Equipo con nombre '{team_name_value}' no encontrado.")
        print("--- Fin del Reporte ---")
        return

    team_data = team_list[0]

    print("\nInformación del Equipo Médico:")
    print(f"  ID del Equipo: {team_data.get('team_id', 'N/A')}")
    print(f"  Nombre del Equipo: {team_data.get('name_of_team', 'N/A')}")
    print(f"  Fecha de Formación: {team_data.get('formation_date', 'N/A')}")
    print(f"  Propósito: {team_data.get('purpose', 'N/A')}")

    doctors = team_data.get('doctors_in_team', [])
    patients = team_data.get('patients_treated_by_team', [])

    if not doctors:
        print("\nEste equipo no tiene doctores asignados actualmente.")
    else:
        print("\nDoctores en el Equipo:")
        for i, doctor in enumerate(doctors, 1):
            print(f"\n  Doctor {i}:")
            print(f"    ID del Doctor: {doctor.get('doctor_id', 'N/A')}")
            print(f"    Nombre: {doctor.get('name_of_doctor', 'N/A')}")

    if not patients:
        print("\nEste equipo no tiene pacientes asignados actualmente.")
    else:
        print("\nPacientes Tratados por el Equipo:")
        for i, patient in enumerate(patients, 1):
            print(f"\n  Paciente {i}:")
            print(f"    ID del Paciente: {patient.get('patient_id', 'N/A')}")
            print(f"    Nombre: {patient.get('name_of_patient', 'N/A')}")

    print("\n--- Fin del Reporte ---")



def get_team_composition_and_patients(client, team_id_value):
    query = """
    query GetTeamInfo($team_id_filter: string!) {
      team_details(func: eq(team_id, $team_id_filter)) {
        uid
        team_id
        name_of_team: name
        formation_date
        purpose

        patients_treated_by_team: treats @filter(has(patient_id)) {
          uid
          patient_id
          name_of_patient: name
        }

        doctors_in_team: ~part_of @filter(has(doctor_id)) {
          uid
          doctor_id
          name_of_doctor: name
        }
      }
    }
    """
    variables = {'$team_id_filter': team_id_value}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)

    print(f"\n--- Reporte de Composición del Equipo ID: {team_id_value} ---")

    if not data.get('team_details'):
        print("No se encontró información para el equipo especificado.")
        print("--- Fin del Reporte ---")
        return

    team_list = data['team_details']

    if not team_list:
        print(f"Equipo con ID '{team_id_value}' no encontrado.")
        print("--- Fin del Reporte ---")
        return

    team_data = team_list[0]

    print("\nInformación del Equipo Médico:")
    print(f"  ID del Equipo: {team_data.get('team_id', 'N/A')}")
    print(f"  Nombre del Equipo: {team_data.get('name_of_team', 'N/A')}")
    print(f"  Fecha de Formación: {team_data.get('formation_date', 'N/A')}")
    print(f"  Propósito: {team_data.get('purpose', 'N/A')}")

    doctors = team_data.get('doctors_in_team', [])
    patients = team_data.get('patients_treated_by_team', [])

    if not doctors:
        print("\nEste equipo no tiene doctores asignados actualmente.")
    else:
        print("\nDoctores en el Equipo:")
        for i, doctor in enumerate(doctors, 1):
            print(f"\n  Doctor {i}:")
            print(f"    ID del Doctor: {doctor.get('doctor_id', 'N/A')}")
            print(f"    Nombre: {doctor.get('name_of_doctor', 'N/A')}")

    if not patients:
        print("\nEste equipo no tiene pacientes asignados actualmente.")
    else:
        print("\nPacientes Tratados por el Equipo:")
        for i, patient in enumerate(patients, 1):
            print(f"\n  Paciente {i}:")
            print(f"    ID del Paciente: {patient.get('patient_id', 'N/A')}")
            print(f"    Nombre: {patient.get('name_of_patient', 'N/A')}")

    print("\n--- Fin del Reporte ---")


def check_family_hereditary_disease_risk(client, patient_id_value):
    query = """
    query CheckFamilyRiskSimple($patientId: string!) {
      initial_patient_data(func: eq(patient_id, $patientId)) {
        uid
        patient_id
        name_patient: name
        
        family_members_with_hereditary_risk: family_relation @filter(has(patient_id)) @cascade {
          uid
          patient_id_family: patient_id
          name_family: name
          
          symptoms_of_family_member: has_symptom @filter(has(symptom_id)) @cascade {
            diseases_with_hereditary_risk: diagnosed 
                @filter(has(disease_id) AND gt(hereditary_risk, 0.0)) { 
              uid
              disease_id
              name_disease: name
              hereditary_risk
              description_disease: description
            }
          }
        }
      }
    }
    """
    variables = {'$patientId': patient_id_value}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)

    print(f"\n--- Reporte de Enfermedades Hereditarias en Familiares del Paciente ID: {patient_id_value} ---")

    patient_data = data.get('initial_patient_data', [])
    if not patient_data:
        print("No se encontró información del paciente especificado.")
        print("--- Fin del Reporte ---")
        return

    patient = patient_data[0]
    print("\nInformación del Paciente:")
    print(f"  ID del Paciente: {patient.get('patient_id', 'N/A')}")
    print(f"  Nombre: {patient.get('name_patient', 'N/A')}")

    family_members = patient.get('family_members_with_hereditary_risk', [])

    if not family_members:
        print("\nNo se encontraron familiares con enfermedades hereditarias registradas.")
    else:
        print("\nFamiliares con Enfermedades Hereditarias Detectadas:")
        for i, member in enumerate(family_members, 1):
            print(f"\n  Familiar {i}:")
            print(f"    ID del Familiar: {member.get('patient_id_family', 'N/A')}")
            print(f"    Nombre: {member.get('name_family', 'N/A')}")
            symptoms = member.get('symptoms_of_family_member', [])

            if not symptoms:
                print("    No se encontraron síntomas relacionados.")
                continue

            for j, symptom in enumerate(symptoms, 1):
                diseases = symptom.get('diseases_with_hereditary_risk', [])
                if diseases:
                    for k, disease in enumerate(diseases, 1):
                        print(f"    Enfermedad Hereditaria {k}:")
                        print(f"      ID de la Enfermedad: {disease.get('disease_id', 'N/A')}")
                        print(f"      Nombre: {disease.get('name_disease', 'N/A')}")
                        print(f"      Riesgo Hereditario: {disease.get('hereditary_risk', 'N/A')}")
                        print(f"      Descripción: {disease.get('description_disease', 'N/A')}")
                else:
                    print("    No se encontraron enfermedades hereditarias en este familiar.")

    print("\n--- Fin del Reporte ---")




def get_medication_interactions_by_name(client, medication_name_value):
    query = """
    query FindMedicationInteractions($medName: string!) {
      medication_interaction_details(func: eq(name, $medName)) {
        uid
        medication_id
        name_of_source_medication: name 
        dosage
        frequency
        route

        interacts_with: interact_with @filter(has(medication_id)) { 
          uid
          medication_id
          name_of_interacting_medication: name
        }
      }
    }
    """
    variables = {'$medName': medication_name_value}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)

    print(f"\n--- Reporte de Interacciones del Medicamento: \"{medication_name_value}\" ---")

    med_data = data.get('medication_interaction_details', [])
    if not med_data:
        print("No se encontró información para el medicamento especificado.")
        print("--- Fin del Reporte ---")
        return

    medication = med_data[0]
    print("\nInformación del Medicamento:")
    print(f"  ID: {medication.get('medication_id', 'N/A')}")
    print(f"  Nombre: {medication.get('name_of_source_medication', 'N/A')}")
    print(f"  Dosis: {medication.get('dosage', 'N/A')}")
    print(f"  Frecuencia: {medication.get('frequency', 'N/A')}")
    print(f"  Vía de Administración: {medication.get('route', 'N/A')}")

    interactions = medication.get('interacts_with', [])
    if not interactions:
        print("\nEste medicamento no tiene interacciones registradas con otros medicamentos.")
    else:
        print("\nInteracciones con otros medicamentos:")
        for i, inter in enumerate(interactions, 1):
            print(f"\n  Medicamento Interactuante {i}:")
            print(f"    ID: {inter.get('medication_id', 'N/A')}")
            print(f"    Nombre: {inter.get('name_of_interacting_medication', 'N/A')}")

    print("\n--- Fin del Reporte ---")






def get_treatment_effectiveness(client, treatment_id_value):
    query = """
    query FindTreatmentEffectiveness($treatId: string!) {
      treatment_effectiveness_info(func: eq(treatment_id, $treatId)) {
        uid
        treatment_id
        name_of_treatment: name 
        effectiveness_score     
      }
    }
    """
    variables = {'$treatId': treatment_id_value}
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)

    print(f"\n--- Reporte de Efectividad del Tratamiento ID: {treatment_id_value} ---")

    treatment_data = data.get('treatment_effectiveness_info', [])
    if not treatment_data:
        print("No se encontró información para el tratamiento especificado.")
        print("--- Fin del Reporte ---")
        return

    treatment = treatment_data[0]
    print("\nInformación del Tratamiento:")
    print(f"  ID: {treatment.get('treatment_id', 'N/A')}")
    print(f"  Nombre: {treatment.get('name_of_treatment', 'N/A')}")

    score = treatment.get('effectiveness_score', None)
    if score is not None:
        try:
            percentage = f"{float(score) * 100:.0f}%"
        except (ValueError, TypeError):
            percentage = "Formato inválido"
    else:
        percentage = "N/A"

    print(f"  Puntaje de Efectividad: {percentage}")

    print("\n--- Fin del Reporte ---")




def get_diseases_for_symptom_by_name(client, symptom_name_value):
    query = """
    query FindDiseasesForSymptom($symptomName: string!) {
      symptom_details(func: eq(name, $symptomName)) {
        uid
        symptom_id
        name_of_symptom: name         
        description_of_symptom: description 

        diagnosed_diseases: diagnosed @filter(has(disease_id)) { 
          uid
          disease_id
          name_of_disease: name
          description_of_disease: description
        }
      }
    }
    """
    variables = {'$symptomName': symptom_name_value}

    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)

    print(f"\n--- Reporte de Enfermedades Relacionadas con el Síntoma: \"{symptom_name_value}\" ---")

    symptom_data_list = data.get('symptom_details', [])
    if not symptom_data_list:
        print("No se encontró información para el síntoma especificado.")
        print("--- Fin del Reporte ---")
        return

    symptom = symptom_data_list[0]

    print("\nInformación del Síntoma:")
    print(f"  ID del Síntoma: {symptom.get('symptom_id', 'N/A')}")
    print(f"  Nombre: {symptom.get('name_of_symptom', 'N/A')}")
    print(f"  Descripción: {symptom.get('description_of_symptom', 'N/A')}")

    diseases = symptom.get('diagnosed_diseases', [])

    if not diseases:
        print("\nNo se encontraron enfermedades asociadas a este síntoma.")
    else:
        print("\nEnfermedades diagnosticadas asociadas a este síntoma:")
        for i, disease in enumerate(diseases, 1):
            print(f"\n  Enfermedad {i}:")
            print(f"    ID: {disease.get('disease_id', 'N/A')}")
            print(f"    Nombre: {disease.get('name_of_disease', 'N/A')}")
            print(f"    Descripción: {disease.get('description_of_disease', 'N/A')}")

    print("\n--- Fin del Reporte ---")




def get_doctors_recommended_by_doctor(client, doctor_id_value):
    query = """
    query FindDoctorRecommendations($docId: string!) {
      recommending_doctor_details(func: eq(doctor_id, $docId)) {
        uid
        doctor_id
        name_of_recommending_doctor: name 

        recommended_doctors_list: recomends @filter(has(doctor_id)) {
          uid
          doctor_id
          name_of_recommended_doctor: name
          license_number
          years_experience
          specializes {
            uid
            specialty_id
            name_of_specialty: name
          }
        }
      }
    }
    """
    variables = {
        '$docId': doctor_id_value
    }

    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)

    print(f"\n--- Reporte de Recomendaciones del Doctor ID: {doctor_id_value} ---")

    recommending_list = data.get('recommending_doctor_details', [])
    if not recommending_list:
        print("No se encontró información para el doctor especificado.")
        print("--- Fin del Reporte ---")
        return

    recommending_doctor = recommending_list[0]
    print("\nInformación del Doctor que Recomienda:")
    print(f"  ID: {recommending_doctor.get('doctor_id', 'N/A')}")
    print(f"  Nombre: {recommending_doctor.get('name_of_recommending_doctor', 'N/A')}")

    recommended_doctors = recommending_doctor.get('recommended_doctors_list', [])

    if not recommended_doctors:
        print("\nEste doctor no ha recomendado a ningún otro doctor.")
    else:
        print(f"\nDoctores recomendados por {recommending_doctor.get('name_of_recommending_doctor', 'N/A')}:")
        for i, doc in enumerate(recommended_doctors, 1):
            print(f"\n  Doctor Recomendado {i}:")
            print(f"    ID: {doc.get('doctor_id', 'N/A')}")
            print(f"    Nombre: {doc.get('name_of_recommended_doctor', 'N/A')}")
            print(f"    Número de licencia: {doc.get('license_number', 'N/A')}")
            print(f"    Años de experiencia: {doc.get('years_experience', 'N/A')}")

            specialties = doc.get('specializes', [])
            if specialties:
                print("    Especialidades:")
                for spec in specialties:
                    print(f"      - {spec.get('name_of_specialty', 'N/A')} (ID: {spec.get('specialty_id', 'N/A')})")
            else:
                print("    Especialidades: No registradas")

    print("\n--- Fin del Reporte ---")



def get_treatment_rehabilitation_info(client, treatment_id_value):
    query = """
    query FindTreatmentRehabTime($treatId: string!) {
      treatment_rehab_details(func: eq(treatment_id, $treatId)) {
        uid
        treatment_id
        name_of_treatment: name 

        required_rehabilitation_time: require @filter(has(rehabilitation_id)) { 
          uid
          rehabilitation_id
          rehabilitation_duration
          condition_severity
        }
      }
    }
    """
    variables = {
        '$treatId': treatment_id_value
    }
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)

    print(f"\n--- Información de Rehabilitación para Tratamiento ID: {treatment_id_value} ---")

    treatment_data = data.get('treatment_rehab_details', [])
    if not treatment_data:
        print("No se encontró información de rehabilitación para el tratamiento indicado.")
        print("--- Fin del Reporte ---")
        return

    treatment = treatment_data[0]
    print(f"\nTratamiento:")
    print(f"  ID: {treatment.get('treatment_id', 'N/A')}")
    print(f"  Nombre: {treatment.get('name_of_treatment', 'N/A')}")

    rehab_times = treatment.get('required_rehabilitation_time', [])
    if not rehab_times:
        print("\nNo se encontró información de tiempo de rehabilitación.")
    else:
        print("\nTiempos de Rehabilitación Requeridos:")
        for i, rehab in enumerate(rehab_times, 1):
            print(f"\n  Rehabilitación {i}:")
            print(f"    ID: {rehab.get('rehabilitation_id', 'N/A')}")
            print(f"    Duración: {rehab.get('rehabilitation_duration', 'N/A')}")
            print(f"    Severidad de la condición: {rehab.get('condition_severity', 'N/A')}")

    print("\n--- Fin del Reporte ---")
