#!/usr/bin/python
import serial
import zmq
import time
import json
import datetime
import logging

LOG_LEVEL = logging.DEBUG

logger = logging.getLogger('RadioListner')
logger.setLevel(LOG_LEVEL)
fh = logging.FileHandler('/var/log/radio_listner.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

ALLOWED_CHARS = '0123456789'

count = 0
timestamp = 0
ser = serial.Serial('/dev/ttyUSB0',9600)

context = zmq.Context()
sender = context.socket(zmq.PUSH)
sender.connect('tcp://159.93.221.24:5555')

logger.info("Initialized. Listening...")
while True:
    try:
        data = ""

        raw_data = ser.readline()
        # logger.debug(str(raw_data))
        temp_time = time.time()
        for i in range(0, len(raw_data)):
            if raw_data[i] in ALLOWED_CHARS:
                data += raw_data[i]

        key = data[0:3]
        encoded = data[3:]
        decoded = ""
        for i in range(0, len(encoded)):
            decoded += str((int(encoded[i]) + 10 - int(key[i % 3])) % 10)
        logger.debug(str(key) + " "  + str(decoded))
        zmq_packet = {'data': decoded, 'time': time.time()}
        sender.send(json.dumps(zmq_packet))

    except Exception, e:
        logger.error('ERROR')
        logger.error(str(e))
    
