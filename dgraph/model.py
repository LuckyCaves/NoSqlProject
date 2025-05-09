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
    start_date: datetime @index(datetime) .
    end_date: datetime @index(datetime) .
    effectiveness_score: float @index(float) .

    medication_id: string @index(exact) .
    dosage: string .
    frequency: string .
    route: string .

    effect_id: string @index(exact) .
    severity: string @index(exact) .

    team_id: string @index(exact) .
    formation_date: datetime .
    lead_doctor_id: string @index(exact) .
    purpose: string .

    disease_id: string @index(exact) .
    hereditary_risk: float @index(float) .

    symptom_id: string @index(exact) .

    rehabilitation_id: string @index(exact) .
    rehabilitation_duration: int @index(int) .
    condition_severity: string @index(exact) .
    completion_status: string @index(exact) .


    family_relation: [uid] @reverse .
    interact_with: [uid] @reverse .
    has_symptom: [uid] .
    diagnosed: uid .
    cure: [uid] .
    has_medication: [uid] .
    require: [uid] .
    cause: [uid] .
    recomends: [uid] @reverse .
    specializes: [uid] .
    part_of: [uid] .
    attends: [uid] @reverse .
    treats: [uid] .

    
    type Patient {
      patient_id
      name
      date_of_birth
      gender
      blood_type
      family_relation
      has_symptom
      attends
    }

    type Doctor {
      doctor_id
      name
      license_number
      years_experience
      recomends
      specializes
      part_of
      attends
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
      cure
      has_medication
      require
    }

    type Medication {
      medication_id
      name
      dosage
      frequency
      route
      cause
      interacts_with
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
      lead_doctor_id
      purpose
      treats
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
      diagnosed
    }

    type RehabilitationTime {
      rehabilitation_id
      rehabilitation_duration
      condition_severity
      completion_status
    }


    """
    return client.alter(pydgraph.Operation(schema=schema))

def load_cosmetics(client):
    txn = client.txn()
    try:
        cosmetics = []
        with open('csvs/Cosmetic.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                cosmetics.append({
                    'uid': row['uid'],
                    'dgraph.type': 'Cosmetic',
                    'nombre': row['nombre'],
                    'category': row['category']
                })
        if cosmetics:
            assigned = txn.mutate(set_obj=cosmetics)
            print(f"Loaded {len(cosmetics)} cosmetics. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
    return assigned.uids

def load_levels(client):
    txn = client.txn()
    try:
        levels = []
        with open('csvs/Level.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # missions_uids = [{'uid': uid.strip()} for uid in row['missions'].split('|_|') if uid.strip()]
                levels.append({
                    'uid': row['uid'],
                    'dgraph.type': 'Level',
                    'dificultad': row['dificultad']
                })
        if levels:
            assigned = txn.mutate(set_obj=levels)
            print(f"Loaded {len(levels)} levels. UIDs: {assigned.uids}")
        txn.commit()

    finally:
        txn.discard()
    return assigned.uids

def load_missions(client):
    txn = client.txn()
    try:
        missions = []
        with open('csvs/Mission.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                missions.append({
                    'uid': row['uid'],
                    'dgraph.type': 'Mission',
                    'time': int(row['time']),
                    'objectives': row['objectives']
                })
        if missions:
            assigned = txn.mutate(set_obj=missions)
            print(f"Loaded {len(missions)} missions. UIDs: {assigned.uids}")
        txn.commit()

    finally:
        txn.discard()
    return assigned.uids

def load_players(client):
    txn = client.txn()
    try:
        players = []
        with open('csvs/Player.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:

                players.append({
                    'uid': row['uid'],
                    'dgraph.type': 'Player',
                    'username': row['username'],
                    'level': int(row['level']),
                    'location': {
                        'type': 'Point',
                        'coordinates': [float(row['longitude']), float(row['latitude'])] # Note the order: longitude then latitude
                    }
                })
        if players:
            assigned = txn.mutate(set_obj=players)
            print(f"Loaded {len(players)} players. UIDs: {assigned.uids}")
        txn.commit()

    finally:
        txn.discard()
    return assigned.uids

def load_buys(client, cosmetic_uids, player_uids):
    txn = client.txn()
    try:
        with open('csvs/buys.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                player = row['uid']
                cosmetic = row['uid2']
                txn.mutate(set_obj={
                    'uid': player_uids[player],
                    'buys': [{'uid': cosmetic_uids[cosmetic]}]
                })
        txn.commit()
        print("Loaded buys relationships.")
    finally:
        txn.discard()



def load_uses(client, cosmetic_uids, player_uids):
    txn = client.txn()
    try:
        with open('csvs/uses.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                player = row['uid']
                cosmetic = row['uid2']
                txn.mutate(set_obj={
                    'uid': player_uids[player],
                    'uses': [{'uid': cosmetic_uids[cosmetic]}]
                })
        txn.commit()
        print("Loaded uses relationships.")
    finally:
        txn.discard()

def load_friends_with(client, player_uids):
    txn = client.txn()
    try:
        with open('csvs/friends_with.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                player = row['uid']
                friend = row['uid2']
                txn.mutate(set_obj={
                    'uid': player_uids[player],
                    'friends_with': [{'uid': player_uids[friend]}]
                })
        txn.commit()
        print("Loaded friends_with relationships.")
    finally:
        txn.discard()

def load_plays(client, player_uids, level_uids):
    txn = client.txn()
    try:
        with open('csvs/plays.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                player = row['uid']
                level = row['uid2']
                txn.mutate(set_obj={
                    'uid': player_uids[player],
                    'plays': [{'uid': level_uids[level]}]
                })
        txn.commit()
        print("Loaded plays relationships.")
    finally:
        txn.discard()

def load_has(client, level_uids, mission_uids):
    txn = client.txn()
    try:
        with open('csvs/has.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                level = row['uid']
                mission = row['uid2']
                txn.mutate(set_obj={
                    'uid': level_uids[level],
                    'has': [{'uid': mission_uids[mission]}]
                })
        txn.commit()
        print("Loaded has relationships.")
    finally:
        txn.discard()

def load_rewards(client, mission_uids, cosmetic_uids):
    txn = client.txn()
    try:
        with open('csvs/rewards.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                mission = row['uid']
                cosmetic = row['uid2']
                txn.mutate(set_obj={
                    'uid': mission_uids[mission],
                    'rewards': [{'uid': cosmetic_uids[cosmetic]}]
                })
        txn.commit()
        print("Loaded rewards relationships.")
    finally:
        txn.discard()

def load_data(client):
    cosmetic_uids = load_cosmetics(client)
    level_uids = load_levels(client)
    mission_uids = load_missions(client)
    player_uids = load_players(client)


    load_buys(client, cosmetic_uids, player_uids)
    load_uses(client, cosmetic_uids, player_uids)
    load_plays(client, player_uids, level_uids)
    load_has(client, level_uids, mission_uids)
    load_rewards(client, mission_uids, cosmetic_uids)
    load_friends_with(client, player_uids)

def create_data(client):
    print("La función create_data original ha sido reemplazada por load_data.")
    load_data(client)



def get_patients_by_doctor_name(client, doctor_name):
    query = """
    query patientsByDoctor($name: string) {
        doctor(func: allofterms(name, $name)) {
            name
            attends {
                name
            }
        }
    }
    """
    variables = {'$name': doctor_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_doctors_by_patient_name(client, patient_name):
    query = """
    query doctorsByPatient($name: string) {
        patient(func: allofterms(name, $name)) {
            name
            ~attends {
                name
            }
        }
    }
    """
    variables = {'$name': patient_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_patient_symptoms_and_treatments(client, patient_name):
    query = """
    query patientSymptoms($name: string) {
        patient(func: allofterms(name, $name)) {
            name
            has_symptom {
                name
                description
                diagnosed {
                    name
                    description
                    cure {
                        name
                        start_date
                        end_date
                    }
                }
            }
        }
    }
    """
    variables = {'$name': patient_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_recommended_doctors_for_patient_diagnoses(client, patient_name):
    query = """
    query recommendedDoctors($name: string) {
        patient(func: allofterms(name, $name)) {
            name
            has_symptom {
                diagnosed {
                    name
                    ~recomends {
                        name
                        specializes {
                            name
                        }
                    }
                }
            }
        }
    }
    """
    variables = {'$name': patient_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_similar_diagnosis_treatments(client, diagnosis_name):
    query = """
    query similarDiagnosis($name: string) {
        similar_diagnoses(func: allofterms(name, $name)) @cascade {
            name
            cure {
                name
                start_date
                effectiveness_score
            }
        }
    }
    """
    variables = {'$name': diagnosis_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_medications_and_causes_for_treatment(client, treatment_name):
    query = """
    query treatmentMedications($name: string) {
        treatment(func: allofterms(name, $name)) {
            name
            has_medication {
                name
                cause {
                    name
                    severity
                }
            }
        }
    }
    """
    variables = {'$name': treatment_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_patient_medical_teams(client, patient_name):
    query = """
    query patientTeams($name: string) {
        patient(func: allofterms(name, $name)) {
            name
            ~treats {
                name
                purpose
                formation_date
                lead_doctor_id
                ~part_of {
                    name
                    specializes {
                        name
                    }
                }
            }
        }
    }
    """
    variables = {'$name': patient_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_family_hereditary_diseases(client, patient_name):
    query = """
    query familyDiseases($name: string) {
        patient(func: allofterms(name, $name)) {
            name
            family_relation {
                name
                has_symptom {
                    diagnosed {
                        name
                        hereditary_risk
                    }
                }
            }
        }
    }
    """
    variables = {'$name': patient_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_medication_interactions(client, medication_name):
    query = """
    query medicationInteractions($name: string) {
        medication(func: allofterms(name, $name)) {
            name
            interacts_with {
                name
            }
        }
    }
    """
    variables = {'$name': medication_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_effective_treatments(client):
    query = """
    query effectiveTreatments {
        treatments(func: type(Treatment)) @filter(gt(effectiveness_score, 0.7)) {
            name
            effectiveness_score
            cure {
                name
            }
        }
    }
    """
    res = client.txn(read_only=True).query(query)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_symptoms_and_related_cures(client):
    query = """
    query symptomsAndCures {
        symptoms(func: type(Symptom)) {
            name
            diagnosed {
                name
                cure {
                    name
                }
            }
        }
    }
    """
    res = client.txn(read_only=True).query(query)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_diagnoses_recommended_by_doctor(client, doctor_name):
    query = """
    query doctorRecommendations($name: string) {
        doctor(func: allofterms(name, $name)) {
            name
            recomends {
                name
            }
        }
    }
    """
    variables = {'$name': doctor_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))


def get_patient_rehabilitation_info(client, patient_name):
    query = """
    query patientRehabInfo($name: string) {
        patient(func: allofterms(name, $name)) {
            name
            has_symptom {
                diagnosed {
                    name
                    ~rehabilitation_id {
                        rehabilitation_duration
                        condition_severity
                        completion_status
                    }
                }
            }
        }
    }
    """
    variables = {'$name': patient_name}
    res = client.txn(read_only=True).query(query, variables=variables)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))
