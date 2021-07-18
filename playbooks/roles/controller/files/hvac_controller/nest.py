from classes.hvac_controller import hvac_controller
from datetime import datetime
import time
import requests
import json

CONFIG_FILE = "/var/opt/hvac_controller/hvac_controller.json"

def poll_sensor(sensor_address):
  r = requests.get(sensor_address)
  return json.loads(r.text)

def sensor_data_stale(timestamp):
  dt_now = datetime.fromtimestamp(int(time.time()))
  dt_timestamp = datetime.fromtimestamp(timestamp)

  dt_diff = dt_now - dt_timestamp

  if int(dt_diff.seconds) > 120:
    with open(configuration["Log File"],'a') as f:
      f.write("Temp sensor data stale, %i seconds old!\n" % dt_diff.seconds)
    return True
  else:
    return False

def read_config(config_path):
  try:
    with open(config_path) as f:
      config = json.load(f)
  except:
    print("Unable to load config file!")
    exit(1)

  return config

def get_log_timestamp():
  return str(datetime.fromtimestamp(int(time.time())))

def write_temp_data_to_log(log_path, temp_f, humidity):
  with open(log_path,'a') as f:
    f.write("%s: Temperature (F): %.2f\n" % (get_log_timestamp(), temp_f))
    f.write("%s: Humidity: %.2f\n" % (get_log_timestamp(), humidity))

if __name__ == '__main__':
  nest_ctl = hvac_controller() 
  
  while True:
    configuration = read_config(CONFIG_FILE)
    sensor_address = "http://" + str(configuration["Sensor Server"]) + ":" + str(configuration["Sensor Server Port"])

    with open(configuration["Log File"],'a') as f:
      f.write("%s: Getting sensor data from %s\n" % (get_log_timestamp(), sensor_address))

    data = poll_sensor(sensor_address)
    write_temp_data_to_log(configuration["Log File"], data["temperature_f"], data["humidity"])

    with open(configuration["Log File"],'a') as f:
      f.write("%s: Desired temperature set to %.2f degrees (F)\n" % (get_log_timestamp(), configuration["Temperature Setting"]))

    if sensor_data_stale(data['timestamp']):
      nest_ctl.ac_off()
      f.write("%s: ERROR sensor data is stale! (More than 2 minutes old)\n" % get_log_timestamp())
      exit(1)

    if data["temperature_f"] > (configuration["Temperature Setting"] + .9):
      with open(configuration["Log File"],'a') as f:
        f.write("%s: Turning AC ON for 15 minutes.\n" % get_log_timestamp())

      nest_ctl.ac_on()

      for i in range(15):
        time.sleep(60)
        active_cooling_data = poll_sensor(sensor_address)
        write_temp_data_to_log(configuration["Log File"], active_cooling_data["temperature_f"], active_cooling_data["humidity"])

      while active_cooling_data["temperature_f"] > (configuration["Temperature Setting"] + .9):
        with open(configuration["Log File"],'a') as f:
          f.write("%s: Target temp not yet reached, continue cooling for another minute before checking temp again.\n" % get_log_timestamp())
        time.sleep(60)
        active_cooling_data = poll_sensor(sensor_address)
        write_temp_data_to_log(configuration["Log File"], active_cooling_data["temperature_f"], active_cooling_data["humidity"])

      nest_ctl.ac_off()

      with open(configuration["Log File"],'a') as f:
        f.write("%s: Desired temp reached, turning AC off\n" % get_log_timestamp())

    time.sleep(60)