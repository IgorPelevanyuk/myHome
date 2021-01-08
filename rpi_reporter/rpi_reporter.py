#!/usr/bin/python
import psutil
import zmq
import time
import json
import datetime
import logging
from subprocess import PIPE, Popen

LOG_LEVEL = logging.DEBUG

logger = logging.getLogger('RadioListner')
logger.setLevel(LOG_LEVEL)
fh = logging.FileHandler('/var/log/radio_listner.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

DEVICE_ID = "00"
TEMP_ID = "90"
CPU_ID = "91"
MEM_ID = "92"

DELIEVERY_PERIOD = 600
SLEEP_TIME = 10

def send(data, device_id, check_id):
    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    sender.connect('tcp://159.93.221.24:5555')
    zmq_packet = {'data': device_id + check_id + str(data), 'time': time.time()}
    sender.send(json.dumps(zmq_packet))
    logger.debug(str(zmq_packet));

def get_cpu_temperature():
    """get cpu temperature using vcgencmd"""
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

context = zmq.Context()
sender = context.socket(zmq.PUSH)
sender.connect('tcp://159.93.221.24:5555')

time_elapsed = 0
temp_integral = 0
cpu_integral = 0
mem_integral = 0
checks = 0
logger.info("Initialized RPI reporter")
while True:
    try:
        if time_elapsed >= DELIEVERY_PERIOD:
            temp = int(1.0 * temp_integral / checks)
            cpu = int(1.0 * cpu_integral / checks)
            mem = int(1.0 * mem_integral / checks)
            send(temp, DEVICE_ID, TEMP_ID)
            send(cpu, DEVICE_ID, CPU_ID)
            send(mem, DEVICE_ID, MEM_ID)
            time_elapsed = 0
            temp_integral = 0
            cpu_integral = 0
            mem_integral = 0
            checks = 0
        temp_integral += get_cpu_temperature()
        cpu_integral += psutil.cpu_percent()
        mem_integral += psutil.virtual_memory().percent
        checks += 1
        time_elapsed += SLEEP_TIME
        #logger.debug('Temp: ' + str(temp_integral))
    except Exception, e:
        logger.error('ERROR')
        logger.error(str(e))
    time.sleep(SLEEP_TIME)
    
