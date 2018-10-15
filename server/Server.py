import DB
import pytz
import datetime
from datetime import timedelta
from flask import Flask, jsonify
from flask_compress import Compress


app = Flask(__name__)

def get_UTC_now():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

def datetime_to_epoch(timestamp):
    """Convert datetime timestamp to epoch seconds(double). Miliseconds comes as decimal.
    Return example:
    >>> datetime_to_epoch(x)
    1479730200.0"""
    epoch = datetime.datetime(1970, 1, 1)
    result = (timestamp - epoch).total_seconds()
    return result

def get_data(table, delta=24):
    result = []
    query = table.select(table.c.time > get_UTC_now() - timedelta(hours=delta))
    cursor = query.execute()
    resultProxy = cursor.fetchall()
    for row in resultProxy:
        temp = dict(row.items())
        data_time = int(datetime_to_epoch(temp['time'])*1000)
        result.append([data_time, temp['value']])
    return result

db_handler = DB.DBHandler()
table_names =  db_handler.get_table_names()
print table_names
# ['01_01', '01_02']

get_data(db_handler.getTable('01_01'))

@app.route('/tables')
def give_tables():
    response = jsonify(table_names)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/<table_name>')
def give_data(table_name):
    if table_name not in table_names:
        return '{}'
    data = get_data(db_handler.getTable(table_name),1000)
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

Compress(app)
app.run(host='159.93.221.24', port=5001)

