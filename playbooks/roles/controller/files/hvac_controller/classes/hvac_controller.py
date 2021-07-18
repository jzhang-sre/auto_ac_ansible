import pi_servo_hat
import time
import sys

class hvac_controller:
  def __init__(self):
    self.mySensor = pi_servo_hat.PiServoHat()
    self.on_position = 95
    self.off_position = -8
    self.servo_channel = 0
    self.last_command_timestamp = int(time.time())

    try:
      self.mySensor.restart()
    except:
      print("The Qwiic PCA9685 device isn't connected to the system. Please check your connection", file=sys.stderr)
    
  def ac_on(self):
    self.mySensor.move_servo_position(self.servo_channel, self.on_position)
    self.last_command_timestamp = int(time.time())

  def ac_off(self):
    self.mySensor.move_servo_position(self.servo_channel, self.off_position)
    self.last_command_timestamp = int(time.time())

  def get_last_command(self):
    return self.last_command_timestamp

if __name__ == "__main__":
  args = sys.argv

  hvac_ctl = hvac_controller()

  if str(args[1]).lower() == "on":
    hvac_ctl.ac_on()
  else:
    hvac_ctl.ac_off()
