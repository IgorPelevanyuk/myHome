#!/usr/bin/python

import DB
from Schemas import types as TYPES

import datetime
import time
import telepot
import pytz
from pprint import pprint as pp

import logging

LOG_LEVEL = logging.DEBUG

logger = logging.getLogger('Telegram_Reporter')
logger.setLevel(LOG_LEVEL)
fh = logging.FileHandler('/var/log/telegram_reporter.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_UTC_now():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('Europe/Moscow'))

def datetime_to_epoch(timestamp):
    """Convert datetime timestamp to epoch seconds(double). Miliseconds comes as decimal.
    Return example:
    >>> datetime_to_epoch(x)
    1479730200.0"""
    epoch = datetime.datetime(1970, 1, 1)
    result = (timestamp - epoch).total_seconds()
    return result

def get_data(table_name, delta=24):
    result = []
    table = db_handler.getTable(table_name) 
    query = table.select(table.c.time > (get_UTC_now() - datetime.timedelta(hours=delta)))
    cursor = query.execute()
    resultProxy = cursor.fetchall()
    for row in resultProxy:
        temp = dict(row.items())
        data_time = int(datetime_to_epoch(temp['time'])*1000)
        result.append([data_time, temp['value']])
    return result

def get_overview_message():
    message = ""
    for table in db_handler.get_table_names():
        data = get_data(table, delta=1)
        type_id = table.split('_')[1]
        if len(data) != 0:
            last_val = max(data, key=lambda x: x[0])
            message += TYPES[type_id]['name'] + ": " + str(last_val[1]) + '\r\n'
    return message


token = "612727621:AAE3UH9w_70cAq9YKFCJr7_L2edjRwja5CY"

db_handler = DB.DBHandler()
TelegramBot = telepot.Bot(token)

from telepot.loop import MessageLoop
def handle(msg):
    TelegramBot.sendMessage(404763289, get_overview_message())

MessageLoop(TelegramBot, handle).run_as_thread()

while True:
    table = db_handler.getTable("02_04")
    query = table.select(table.c.time > (get_UTC_now() - datetime.timedelta(hours=50)))
    cursor = query.execute()
    resultProxy = cursor.fetchall()
    result = []
    for row in resultProxy:
        temp = dict(row.items())
        result.append(temp)
    last_val = result[-1]
    if last_val['value'] != 401:
        TelegramBot.sendMessage(404763289, "Warning, last value received: %s. Time: %s" % (last_val['value'], last_val['time'].strftime('%d %b %Y %H:%M:%S')))
    time.sleep(10)
