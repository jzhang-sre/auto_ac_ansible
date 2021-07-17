import adafruit_dht
import time
import board

if __name__ == "__main__":

  # --------- User Settings ---------
  METRIC_UNITS = False
  # ---------------------------------

  dhtSensor = adafruit_dht.DHT22(board.D4)

  try:
    humidity = dhtSensor.humidity
    temp_c = dhtSensor.temperature

  except RuntimeError:
    print("RuntimeError, trying again...")
          
  if METRIC_UNITS:
    print('Temperature(C): {0} - RH: {1}'.format(temp_c, humidity))
  else:
    temp_f = format((temp_c * 9.0 / 5.0) + 32.0, ".2f")
    print('Temperature(F): {0} - RH: {1}'.format(temp_f, humidity))