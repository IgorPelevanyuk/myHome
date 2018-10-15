from DB import Column, Integer, String, DateTime

types = {
    # Temperature DHT11 - Int Celsius
    '01': {'schema': (Column('time', DateTime, primary_key=True),
                      Column('value', Integer)),
           'read': int,
           'min': 0, 'max': 60,
           'name': 'Teperature, C',
    },
    # Humidity DHT11 - Int Percent
    '02': {'schema': (Column('time', DateTime, primary_key=True),
                      Column('value', Integer)),
           'read': int,
           'min': 0, 'max': 100,
           'name': 'Humidity, %',
    },
    # Leakage detector - 0 if OK, not 0 if LEAK
    '04': {'schema': (Column('time', DateTime, primary_key=True),
                      Column('value', Integer)),
          'read': int,
          'min': 0, 'max':1000,
          'name': 'Leak',
    },
    # PIR detector - 1 when move existed
    '05': {'schema': (Column('time', DateTime, primary_key=True),
                      Column('value', Integer)),
          'read': int,
          'min': 0, 'max':100,
          'name': 'Movement',
    },
    # Temperature - Int Percent
    '90': {'schema': (Column('time', DateTime, primary_key=True),
                      Column('value', Integer)),
          'read': int,
          'min': 0, 'max':100,
          'name': 'CPU Temperature, C',
    },
    # CPU load - Int Percent
    '91': {'schema': (Column('time', DateTime, primary_key=True),
                      Column('value', Integer)),
          'read': int,
          'min': 0, 'max':100,
          'name': 'CPU Load, %',
    },
    # MEM load - Int Percent
    '92': {'schema': (Column('time', DateTime, primary_key=True),
                      Column('value', Integer)),
          'read': int,
          'min': 0, 'max':100,
          'name': 'Memory Load, %',
    },
    
}

