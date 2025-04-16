import datetime

records = []

def record_progress(message):
    records.append((datetime.datetime.now(), message))

def get_records():
    return records
