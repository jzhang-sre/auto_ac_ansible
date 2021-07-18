from datetime import datetime
import time
import requests
import json

if __name__ == '__main__':
  SENSOR_SERVER = "172.16.32.27"
  SENSOR_SERVER_PORT = 8080
  SENSOR_SERVER_ADDRESS = "http://" + SENSOR_SERVER + ":" + str(SENSOR_SERVER_PORT)
  r = requests.get(SENSOR_SERVER_ADDRESS)
  
  data = json.loads(r.text)
  dt_now = datetime.fromtimestamp(int(time.time()))
  dt_timestamp = datetime.fromtimestamp(data["timestamp"])

  dt_diff = dt_now - dt_timestamp

  print(dt_diff.seconds)
  print("Temperature (F): %.2f" % data["temperature_f"])
  print("Humidity: %.2f" % data["humidity"])