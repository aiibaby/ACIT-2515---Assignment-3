import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE temperature_reading
          (id INTEGER PRIMARY KEY ASC,
           timestamp DATETIME NOT NULL,
           model VARCHAR(250) NOT NULL,
           min_reading NUMBER NOT NULL,
           avg_reading NUMBER NOT NULL,
           max_reading NUMBER NOT NULL,
           status VARCHAR(250) NOT NULL
          )
          ''')
c.execute('''
          CREATE TABLE pressure_reading
          (id INTEGER PRIMARY KEY ASC,
           timestamp DATETIME NOT NULL,
           model VARCHAR(250) NOT NULL,
           min_reading NUMBER NOT NULL,
           avg_reading NUMBER NOT NULL,
           max_reading NUMBER NOT NULL,
           status VARCHAR(250) NOT NULL
          )
          ''')

conn.commit()
conn.close()
