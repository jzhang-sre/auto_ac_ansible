from classes.dht_sensor import dht_sensor
import sqlite3
import time
import sys

if __name__ == "__main__":
  db_path = "/var/opt/sensor_server/sensor_logger.db"
  conn = sqlite3.connect(db_path)
  cur = conn.cursor()

  sensor_reading = dht_sensor()
  time.sleep(2)
  sensor_reading.poll_sensor()

  timestamp = int(time.time())
  temp_f = round(sensor_reading.get_temp('f'), 2)
  temp_c = round(sensor_reading.get_temp('c'), 2)
  humidity = round(sensor_reading.get_humidity())

  cur.execute(" CREATE TABLE IF NOT EXISTS SENSOR_LOG ([unix_time] INTEGER PRIMARY KEY,[temp_c] real, [temp_f] real, [humidity] real) ")
  cur.execute(" INSERT INTO SENSOR_LOG VALUES ('{time}','{c}','{f}','{rh}') ".format(time = str(timestamp), f = temp_f, c = temp_c, rh = humidity))
  conn.commit()

  if len(sys.argv) > 1:
    cur.execute(" SELECT * FROM SENSOR_LOG WHERE unix_time = (SELECT MAX(unix_time) FROM SENSOR_LOG); ")

    rows = cur.fetchall()

    for row in rows:
      print(list(row))

  conn.close()