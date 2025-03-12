import time_uuid
from cassandra.query import BatchStatement

CREATE_KEYSPACE ="""
    CREATE KEYSPACE IF NOT EXISTS {}
    WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': {}}};
"""

def create_keyspace(session, keyspace, replication_factor):
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

