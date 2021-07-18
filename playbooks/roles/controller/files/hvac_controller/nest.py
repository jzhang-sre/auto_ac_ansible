from classes.hvac_controller import hvac_controller
from datetime import datetime
import time
import requests
import json

SENSOR_SERVER = "172.16.32.27"
SENSOR_SERVER_PORT = 8080
SENSOR_SERVER_ADDRESS = "http://" + SENSOR_SERVER + ":" + str(SENSOR_SERVER_PORT)
TEMPERATURE_SETTING = "/var/opt/hvac_controller/set_temp.txt"

def poll_sensor():
  r = requests.get(SENSOR_SERVER_ADDRESS)
  return json.loads(r.text)

def sensor_data_stale(timestamp):
  dt_now = datetime.fromtimestamp(int(time.time()))
  dt_timestamp = datetime.fromtimestamp(timestamp)

  dt_diff = dt_now - dt_timestamp

  if int(dt_diff.seconds) > 120:
    print("Temp sensor data stale, %i seconds old!" % dt_diff.seconds)
    return True
  else:
    return False

if __name__ == '__main__':
  nest_ctl = hvac_controller()

  while True:
    try:
      with open(TEMPERATURE_SETTING) as f:
        temperature_setting = float(f.read())
    except:
      temperature_setting = 77.25

    data = poll_sensor()

    print("Temperature (F): %.2f" % data["temperature_f"])
    print("Humidity: %.2f" % data["humidity"])

    if sensor_data_stale(data['timestamp']):
      nest_ctl.ac_off()
      exit(1)

    if data["temperature_f"] > (temperature_setting + .9):
      print("Turning AC ON for 15 minutes.")
      nest_ctl.ac_on()
      time.sleep(60*15)
      after_cooling_data = poll_sensor()
      print("Temperature (F): %.2f" % after_cooling_data["temperature_f"])
      print("Humidity: %.2f" % after_cooling_data["humidity"])
      while after_cooling_data["temperature_f"] > (temperature_setting + .9):
        time.sleep(60)
        after_cooling_data = poll_sensor()
        print("Temperature (F): %.2f" % after_cooling_data["temperature_f"])
        print("Humidity: %.2f" % after_cooling_data["humidity"])

      print("Turning AC OFF")
      nest_ctl.ac_off()
    time.sleep(60)