import logging
import sqlite3
from providers.karvi import Karvi

def register_car(conn, car):
    stmt = 'INSERT INTO properties (internal_id, provider, url) VALUES (:internal_id, :provider, :url)'
    try:
        conn.execute(stmt, car)
    except Exception as e:
        print(e)

def process_cars(provider_name, provider_data):
    provider = get_instance(provider_name, provider_data)
    new_cars = []

    # db connection
    conn = sqlite3.connect('cars.db')

    # Check to see if we know it
    stmt = 'SELECT * FROM cars WHERE internal_id=:internal_id AND provider=:provider'

    with conn:
        for car in provider.next_car():
            cur = conn.cursor()
            logging.info(f"Processing car {car['internal_id']}")
            cur.execute(stmt, {'internal_id': car['internal_id'], 'provider': car['provider']})
            result = cur.fetchone()
            cur.close()
            if result == None:
                # Insert and save for notification
                logging.info('It is a new one')
                register_car(conn, car)
                new_cars.append(car)
                    
    return new_cars

def get_instance(provider_name, provider_data):
    if provider_name == 'karvi':
        return Karvi(provider_name, provider_data)
    elif provider_name == 'kabak':
        return Kabak(provider_name, provider_data)
    else:
        raise Exception('Unrecognized provider')
