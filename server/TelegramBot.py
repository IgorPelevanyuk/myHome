import DB
from Schemas import types as TYPES

import datetime
import telepot
import pytz
from pprint import pprint as pp

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

token = "612727621:AAE3UH9w_70cAq9YKFCJr7_L2edjRwja5CY"

TelegramBot = telepot.Bot(token)
print TelegramBot.getMe()
db_handler = DB.DBHandler()
for table in db_handler.get_table_names():
    data = get_data(table, delta=1)
    type_id = table.split('_')[1]
    if len(data) != 0:
        last_val = max(data, key=lambda x: x[0])
        pp(TYPES[type_id]['name'] + ": " + str(last_val[1]))
 
    
TelegramBot.sendMessage(404763289, str(db_handler.get_table_names()))
#pp(TelegramBot.getUpdates())

