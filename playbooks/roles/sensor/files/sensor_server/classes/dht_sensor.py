import adafruit_dht
import time
import board

class dht_sensor:
  def __init__(self):
    self.__sensor = adafruit_dht.DHT22(board.D4)
    self.temp_c = 0
    self.temp_f = 0
    self.humidity = 0

    self.poll_sensor()

  def __get_temp_reading(self):
    while True:
      try:
        temp_c = self.__sensor.temperature

        if temp_c is not None:
          temp_c = self.__sensor.temperature
          break

      except RuntimeError:
        continue

    return temp_c

  def __get_humidity_reading(self):
    while True:
      try:
        humidity = self.__sensor.temperature

        if humidity is not None:
          humidity = self.__sensor.humidity
          break

      except RuntimeError:
        continue

    return humidity

  def poll_sensor(self):
    self.temp_c = self.__get_temp_reading()
    self.temp_f = self.temp_c * 9.0 / 5.0 + 32.0
    self.humidity = self.__get_humidity_reading()

  def get_temp(self, scale):
    if str(scale).lower() == 'c':
      return self.temp_c
    else:
      return self.temp_f

  def get_humidity(self):
    return self.humidity

if __name__ == "__main__":
  sensor_reading = dht_sensor()
  time.sleep(2)
  sensor_reading.poll_sensor()
  
  print("Temp(F): %.2f" % sensor_reading.get_temp('f'))
  print("Temp(C): %.2f" % sensor_reading.get_temp('c'))
  print("Humidity: %.2f" % sensor_reading.get_humidity())