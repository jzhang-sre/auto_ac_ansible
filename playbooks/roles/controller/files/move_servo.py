import pi_servo_hat
import time
import sys

ON_POSITION = 95
OFF_POSITION = -8

if __name__ == "__main__":
  args = sys.argv
  mySensor = pi_servo_hat.PiServoHat()

  try:
    mySensor.restart()
  except:
    print("The Qwiic PCA9685 device isn't connected to the system. Please check your connection", file=sys.stderr)

  if str(args[1]).lower() == "on":
    mySensor.move_servo_position(0, ON_POSITION) #ON
  else:
    mySensor.move_servo_position(0, OFF_POSITION) #OFF
