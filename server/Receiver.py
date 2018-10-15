#!/usr/bin/python

import datetime
import json
import sys
import time
import zmq
import Schemas
import DB
import logging

LOG_LEVEL = logging.DEBUG

logger = logging.getLogger('ZMQ_listner')
logger.setLevel(LOG_LEVEL)
fh = logging.FileHandler('/var/log/zmq_listner.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


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
            logger.error('Packet came: ' + str(zmq_packet))
        logger.error('ERROR: JSON load problem')
        logger.error('Error_text: ' + str(e))
        logger.error('Message: ' + str(s))
        continue
        

    logger.info(zmq_packet)
    if len(zmq_packet['data']) < 4:
        continue
    sensor_id = zmq_packet['data'][:2]
    sensor_type = zmq_packet['data'][2:4]
    sensor_data = zmq_packet['data'][4:]
    sensor_value = get_value(sensor_type, sensor_data)
    if not sensor_value:
        logger.error('Value is not good')
        logger.error(str(sensor_value) + " " + repr(sensor_value))
    sensor_time = datetime.datetime.utcfromtimestamp(zmq_packet['time'])
    if sensor_value:
        try:
            db_handler.writeValue(sensor_id, sensor_type, sensor_value, sensor_time)
        except Exception, e:
            logger.error('ERROR: DB insert problem')
            logger.error('Error_text: ' + str(e))
            
            

