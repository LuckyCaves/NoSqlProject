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
    specializes: [uid] .
    part_of: [uid] .
    cure: [uid] .
    has_medication: [uid] .
    interact_with: [uid] @reverse .
    cause: [uid] .
    treats: [uid] @reverse .
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
    print(json.dumps(data, indent=2)) 


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
          date_of_birth
          gender
          blood_type
        }
      }
    }
    """
    variables = {'$doctor_id': doctor_id_value}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2)) 



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
              start_date
              end_date
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
    print(json.dumps(data, indent=2)) 



def get_doctors_by_specialty(client, specialty_id_value):
    query = """
    query FindDoctorsBySpecialty($specialty_id: string!) {
      specialty_doctors(func: eq(specialty_id, $specialty_id)) {
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
        '$specialty_id': specialty_id_value
    }
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2)) # Opcional: para depuración



def get_treatments_and_medications_for_disease_by_id(client, disease_id_value):
    query = """
    query FindTreatmentsForDiseaseById($diseaseId: string!) {
      disease_treatment_info(func: eq(disease_id, $diseaseId)) { 
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
    variables = {
        '$diseaseId': disease_id_value 
    }
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2)) 


def get_side_effects_for_medication(client, medication_id_value):
    query = """
    query FindSideEffects($med_id: string!) {
      medication_info(func: eq(medication_id, $med_id)) {
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
    variables = {
        '$med_id': medication_id_value
    }
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2)) 


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
    variables = {
        '$team_id_filter': team_id_value
    }
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2)) # Opcional: para depuración


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
    variables = {
        '$patientId': patient_id_value
    }
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2)) 


def get_medication_interactions(client, medication_id_value):
    query = """
    query FindMedicationInteractions($medId: string!) {
      medication_interaction_details(func: eq(medication_id, $medId)) {
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
    variables = {
        '$medId': medication_id_value
    }
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2)) 



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
    variables = {
        '$treatId': treatment_id_value
    }
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2)) 


def get_diseases_for_symptom(client, symptom_id_value):
    query = """
    query FindDiseasesForSymptom($symptomId: string!) {
      symptom_details(func: eq(symptom_id, $symptomId)) {
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
    variables = {
        '$symptomId': symptom_id_value
    }
    
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2)) 


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
    print(json.dumps(data, indent=2)) 


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
    print(json.dumps(data, indent=2))
