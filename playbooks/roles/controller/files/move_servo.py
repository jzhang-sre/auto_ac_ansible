import pi_servo_hat
import time
import sys

if __name__ == "__main__":
  mySensor = pi_servo_hat.PiServoHat()

  try:
    mySensor.restart()
  except:
    print("The Qwiic PCA9685 device isn't connected to the system. Please check your connection", file=sys.stderr)

  for i in range(0,30):
    mySensor.move_servo_position(0, -8)
    print("ON %i" % mySensor.get_servo_position(0))
    time.sleep(1)
    mySensor.move_servo_position(0, 90)
    print("OFF %i" % mySensor.get_servo_position(0))
    time.sleep(1)
