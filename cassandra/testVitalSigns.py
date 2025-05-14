import random
import os
from datetime import datetime

from cassandra.cluster import Cluster

import cassandraModel as model


CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'healthcare')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

cluster = Cluster(CLUSTER_IPS.split(','))
session = cluster.connect()

model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
session.set_keyspace(KEYSPACE)

data = []

patientsAcc = ["P0006","P0004","P0005","P0001","P0007","P0003","P0002","P0008","P0009","P0010"]
for i in range(10):
    account = "P0001"
    vital_sign_type = random.choice(['blood pressure', 'heart rate', 'oxygenation', 'temperature'])
    if vital_sign_type == 'blood pressure':
        vital_sign_value = random.uniform(80, 150)
    elif vital_sign_type == 'heart rate':
        vital_sign_value = random.uniform(50, 110)
    elif vital_sign_type == 'oxygenation':
        vital_sign_value = random.uniform(85, 100)
    elif vital_sign_type == 'temperature':
        vital_sign_value = random.uniform(35, 39)
    vital_sign_date = datetime.now()
    vital_sign_id = model.random_dateUUID(vital_sign_date)
    data.extend([vital_sign_id, account, vital_sign_type, vital_sign_value, vital_sign_date])
    model.insert_vital_sign(session, data)
    data = []