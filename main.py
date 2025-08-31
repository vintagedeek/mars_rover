#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Button, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# -------- Hardware --------
ev3 = EV3Brick()
left = Motor(Port.B)
right = Motor(Port.C)
arm = Motor(Port.A)
eyes = UltrasonicSensor(Port.S4)

WHEEL_DIAMETER = 55.5   # mm
AXLE_TRACK = 110        # mm
robot = DriveBase(left, right, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)

# -------- Arm positions (deg) --------
UP_POS = 90
ARM_SPEED = 300  # deg/s for moves

# -------- Distance thresholds (mm) --------
DROP_MM = 40     # 4 cm
BLIND_MM = 30    # ~3 cm blind zone

# -------- Init --------
arm.run_target(ARM_SPEED, UP_POS, Stop.HOLD)
ev3.speaker.say("Arms up. Driving.")

DRIVE_SPEED = 120  # mm/s
robot.drive(DRIVE_SPEED, 0)

while True:
    d = eyes.distance()  # mm

    # Display distance
    ev3.screen.clear()
    ev3.screen.print("Dist:" if d >= BLIND_MM else "Dist: too close",
                     d // 10 if d >= BLIND_MM else "")

    # Trigger at 4 cm or closer
    if d <= DROP_MM:
        robot.stop(Stop.BRAKE)
        ev3.speaker.beep()

        # Lower until stall = gently to the ground, then hold.
        # Use a slow speed and low duty_limit so it doesn't grind.
        arm.run_until_stalled(-120, then=Stop.HOLD, duty_limit=30)

        ev3.speaker.say("Rock reached. Reversing.")
        # Reverse ~3 feet (3 ft ≈ 914 mm)
        robot.straight(-914)
        break

    # Manual abort
    if Button.CENTER in ev3.buttons.pressed():
        robot.stop(Stop.BRAKE)
        break

    wait(50)  # ~20 Hz loop

ev3.speaker.say("Done")