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
    has_symptom: [uid] .
    attends: [uid] @reverse .
    recomends: [uid] @reverse .
    specializes: [uid] .
    part_of: [uid] .
    cure: [uid] .
    has_medication: [uid] .
    interact_with: [uid] @reverse .
    cause: [uid] .
    treats: [uid] .
    diagnosed: uid .
    require: [uid] .
  

    
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

      interact_with
      cause
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

#load data from csvs

def load_patients(client):
    txn = client.txn()
    try:
        patients = []
        with open('csvs/nodes/patients.csv', mode='r') as csv_file:
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
        with open('csvs/nodes/doctors.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                doctors.append({
                    'uid': f'_:{row["doctor_id"]}',
                    'dgraph.type': 'Doctor',
                    'doctor_id': row['doctor_id'],
                    'name': row['name'],
                    'license_number': row['license_number'],
                    'years_experience': int(row['years_experience'])
                })
        assigned = txn.mutate(set_obj=doctors)
        print(f"Loaded {len(doctors)} doctors. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
    return assigned.uids


def load_specialties(client):
    txn = client.txn()
    try:
        specialties = []
        with open('csvs/nodes/specialties.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                specialties.append({
                    'uid': f'_:{row["specialty_id"]}',
                    'dgraph.type': 'Specialty',
                    'specialty_id': row['specialty_id'],
                    'name': row['name'],
                    'description': row['description']
                })
        assigned = txn.mutate(set_obj=specialties)
        print(f"Loaded {len(specialties)} specialties. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
    return assigned.uids


def load_treatments(client):
    txn = client.txn()
    try:
        treatments = []
        with open('csvs/nodes/treatments.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
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
        print(f"Loaded {len(treatments)} treatments. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
    return assigned.uids


def load_medications(client):
    txn = client.txn()
    try:
        medications = []
        with open('csvs/nodes/medications.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
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
        print(f"Loaded {len(medications)} medications. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
    return assigned.uids




def load_side_effects(client):
    txn = client.txn()
    try:
        effects = []
        with open('csvs/nodes/side_effects.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                effects.append({
                    'uid': f'_:{row["effect_id"]}',
                    'dgraph.type': 'SideEffect',
                    'effect_id': row['effect_id'],
                    'name': row['name'],
                    'description': row['description'],
                    'severity': row['severity']
                })
        assigned = txn.mutate(set_obj=effects)
        print(f"Loaded {len(effects)} side effects. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
    return assigned.uids


def load_treatment_teams(client):
    txn = client.txn()
    try:
        teams = []
        with open('csvs/nodes/treatment_teams.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                teams.append({
                    'uid': f'_:{row["team_id"]}',
                    'dgraph.type': 'TreatmentTeam',
                    'team_id': row['team_id'],
                    'name': row['name'],
                    'formation_date': row['formation_date'],
                    'lead_doctor_id': row['lead_doctor_id'],
                    'purpose': row['purpose']
                })
        assigned = txn.mutate(set_obj=teams)
        print(f"Loaded {len(teams)} treatment teams. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
    return assigned.uids


def load_diseases(client):
    txn = client.txn()
    try:
        diseases = []
        with open('csvs/nodes/diseases.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                diseases.append({
                    'uid': f'_:{row["disease_id"]}',
                    'dgraph.type': 'Disease',
                    'disease_id': row['disease_id'],
                    'name': row['name'],
                    'hereditary_risk': float(row['hereditary_risk']),
                    'description': row['description']
                })
        assigned = txn.mutate(set_obj=diseases)
        print(f"Loaded {len(diseases)} diseases. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
    return assigned.uids

def load_symptoms(client):
    txn = client.txn()
    try:
        symptoms = []
        with open('csvs/nodes/symptoms.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                symptoms.append({
                    'uid': f'_:{row["symptom_id"]}',
                    'dgraph.type': 'Symptom',
                    'symptom_id': row['symptom_id'],
                    'name': row['name'],
                    'description': row['description'],
                    'severity': row['severity'],
                    'diagnosed': {'uid': f'_:{row["diagnosed"]}'}
                })
        assigned = txn.mutate(set_obj=symptoms)
        print(f"Loaded {len(symptoms)} symptoms. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
    return assigned.uids

def load_rehabilitations(client):
    txn = client.txn()
    try:
        rehabilitations = []
        with open('csvs/nodes/rehabilitations.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                rehabilitations.append({
                    'uid': f'_:{row["rehabilitation_id"]}',
                    'dgraph.type': 'RehabilitationTime',
                    'rehabilitation_id': row['rehabilitation_id'],
                    'rehabilitation_duration': int(row['rehabilitation_duration']),
                    'condition_severity': row['condition_severity'],
                    'completion_status': row['completion_status']
                })
        assigned = txn.mutate(set_obj=rehabilitations)
        print(f"Loaded {len(rehabilitations)} rehabilitations. UIDs: {assigned.uids}")
        txn.commit()
    finally:
        txn.discard()
    return assigned.uids


#load relations 
def load_family_relation(client, patient_uids):
    txn = client.txn()
    try:
        with open('csvs/relations/family_relation.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': patient_uids[row['uid']],
                    'family_relation': [{'uid': patient_uids[row['uid2']]}]
                })
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
                txn.mutate(set_obj={
                    'uid': patient_uids[row['uid']],
                    'has_symptom': [{'uid': symptom_uids[row['uid2']]}]
                })
        txn.commit()
        print("Loaded has_symptom relationships.")
    finally:
        txn.discard()


def load_attends(client, patient_uids, doctor_uids):
    txn = client.txn()
    try:
        with open('csvs/attends.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': doctor_uids[row['uid2']],
                    'attends': [{'uid': patient_uids[row['uid']]}]
                })
        txn.commit()
        print("Loaded attends relationships.")
    finally:
        txn.discard()


def load_recomends(client, doctor_uids, doctor_uids_2):
    txn = client.txn()
    try:
        with open('csvs/recomends.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': doctor_uids[row['uid']],
                    'recomends': [{'uid': doctor_uids_2[row['uid2']]}]
                })
        txn.commit()
        print("Loaded recomends relationships.")
    finally:
        txn.discard()


def load_specializes(client, doctor_uids, specialty_uids):
    txn = client.txn()
    try:
        with open('csvs/specializes.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': doctor_uids[row['uid']],
                    'specializes': [{'uid': specialty_uids[row['uid2']]}]
                })
        txn.commit()
        print("Loaded specializes relationships.")
    finally:
        txn.discard()


def load_part_of(client, doctor_uids, team_uids):
    txn = client.txn()
    try:
        with open('csvs/part_of.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': doctor_uids[row['uid']],
                    'part_of': [{'uid': team_uids[row['uid2']]}]
                })
        txn.commit()
        print("Loaded part_of relationships.")
    finally:
        txn.discard()


def load_treats(client, team_uids, patient_uids):
    txn = client.txn()
    try:
        with open('csvs/treats.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': team_uids[row['uid']],
                    'treats': [{'uid': patient_uids[row['uid2']]}]
                })
        txn.commit()
        print("Loaded treats relationships.")
    finally:
        txn.discard()


def load_cure(client, treatment_uids, disease_uids):
    txn = client.txn()
    try:
        with open('csvs/cure.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': treatment_uids[row['uid']],
                    'cure': [{'uid': disease_uids[row['uid2']]}]
                })
        txn.commit()
        print("Loaded cure relationships.")
    finally:
        txn.discard()


def load_has_medication(client, treatment_uids, medication_uids):
    txn = client.txn()
    try:
        with open('csvs/has_medication.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': treatment_uids[row['uid']],
                    'has_medication': [{'uid': medication_uids[row['uid2']]}]
                })
        txn.commit()
        print("Loaded has_medication relationships.")
    finally:
        txn.discard()


def load_require(client, treatment_uids, rehabilitation_uids):
    txn = client.txn()
    try:
        with open('csvs/requires.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': treatment_uids[row['uid']],
                    'require': [{'uid': rehabilitation_uids[row['uid2']]}]
                })
        txn.commit()
        print("Loaded require relationships.")
    finally:
        txn.discard()


def load_cause(client, medication_uids, effect_uids):
    txn = client.txn()
    try:
        with open('csvs/causes.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': medication_uids[row['uid']],
                    'cause': [{'uid': effect_uids[row['uid2']]}]
                })
        txn.commit()
        print("Loaded cause relationships.")
    finally:
        txn.discard()


def load_interacts_with(client, medication_uids):
    txn = client.txn()
    try:
        with open('csvs/interacts_with.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': medication_uids[row['uid']],
                    'interact_with': [{'uid': medication_uids[row['uid2']]}]
                })
        txn.commit()
        print("Loaded interact_with relationships.")
    finally:
        txn.discard()


def load_diagnosed(client, symptom_uids, disease_uids):
    txn = client.txn()
    try:
        with open('csvs/diagnosed.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                txn.mutate(set_obj={
                    'uid': symptom_uids[row['uid']],
                    'diagnosed': {'uid': disease_uids[row['uid2']]}
                })
        txn.commit()
        print("Loaded diagnosed relationships.")
    finally:
        txn.discard()


def load_data(client):
    patients_uids = load_patients(client)
    doctors_uids = load_doctors(client)
    specialties_uids = load_specialties(client)
    treatments_uids = load_treatments(client)
    medications_uids = load_medications(client)
    side_effects_uids = load_side_effects(client)
    treatment_teams_uids = load_treatment_teams(client)
    diseases_uids = load_diseases(client)
    symptoms_uids = load_symptoms(client)
    rehabilitations_uids = load_rehabilitations(client)


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
