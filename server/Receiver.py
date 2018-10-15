import datetime
import json
import sys
import time
import zmq


import Schemas
import DB

ALLOWED_SYMBOLS = "0123456789"

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5555")

db_handler = DB.DBHandler()

def get_value(sensor_type, value_str):
    if sensor_type in Schemas.types:
        value = Schemas.types[sensor_type]['read'](value_str)
        if value < Schemas.types[sensor_type]['min']:
            return None
        if value > Schemas.types[sensor_type]['max']:
            return None
    else:
        return None
    return value

while True:
    s = receiver.recv()
    try:
        zmq_packet = json.loads(s)
    except Exception, e:
        if zmq_packet:
            print 'Packet came: ', zmq_packet
        print 'ERROR: JSON load problem'
        print 'Error_text: ', e
        print 'Message: ', s
        continue
        

    print zmq_packet
    if len(zmq_packet['data']) < 4:
        continue
    sensor_id = zmq_packet['data'][:2]
    sensor_type = zmq_packet['data'][2:4]
    sensor_data = zmq_packet['data'][4:]
    sensor_value = get_value(sensor_type, sensor_data)
    if not sensor_value:
        print 'Value is not good'
        print sensor_value, repr(sensor_value)
    sensor_time = datetime.datetime.utcfromtimestamp(zmq_packet['time'])
    if sensor_value:
        try:
            db_handler.writeValue(sensor_id, sensor_type, sensor_value, sensor_time)
        except Exception, e:
            print 'ERROR: DB insert problem'
            print 'Error_text: ', e
            
            

