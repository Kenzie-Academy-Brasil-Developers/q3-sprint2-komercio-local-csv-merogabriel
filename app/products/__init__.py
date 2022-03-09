from csv import DictReader, DictWriter

import os 

FILEPATH = os.getenv('FILEPATH')


def read_events_from_csv():
    with open(FILEPATH, "r") as csv_file:
        reader = DictReader(csv_file)
        events = list(reader)

        return events


def write_event_in_csv(payload: dict):
    with open (FILEPATH, 'a') as csv_file:
        fieldnames = ['id', 'name', 'price']
        writer = DictWriter(csv_file, fieldnames)
    
        writer.writerow(payload)

        return payload


def validate_keys(payload: dict, expected_keys: set):
    body_keys_set = set(payload.keys())

    invalid_keys = body_keys_set - expected_keys

    if invalid_keys:
        raise KeyError( {
                "error": "invalid_keys",
                "expected": list(expected_keys),
                "received": list(body_keys_set),
            }
        )


def update_event_in_csv(payload):
    with open (FILEPATH, 'w') as csv_file:
        fieldnames = ["id", "name", "price"]

        writer = DictWriter(csv_file, fieldnames)

        writer.writeheader()
        writer.writerows(payload)


def normalize_variables(payload:dict):
    payload['id'] = int(payload['id'])
    payload['price'] = float(payload['price'])

    return payload