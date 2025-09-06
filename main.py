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

# Measure from outermost edges of a tire (i.e., measure from outer edge of black
# tire across to the other outer edge )
WHEEL_DIAMETER = 55.5   # mm

# Measure from center of left tire to center of right tire
AXLE_TRACK = 110        # mm
robot = DriveBase(left, right, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)

# -------- Arm positions (deg) --------
UP_POS = 90
ARM_SPEED = 300  # deg/s for moves

# -------- Distance thresholds (mm) --------
DROP_MM = 40     # 4 cm
BLIND_MM = 30    # ~3 cm blind zone

# -------- Init --------
arm.run_target(speed=ARM_SPEED, target_angle=UP_POS, then=Stop.HOLD)
ev3.speaker.say("Arms up. Driving.")

DRIVE_SPEED = 120  # mm/s
robot.drive(drive_speed=DRIVE_SPEED, turn_rate=0)

# https://pybricks.com/ev3-micropython/robotics.html
# https://pybricks.com/ev3-micropython/ev3devices.html
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
        # duty_limit This sets the max torque/power level the motor is allowed 
        # to use (as % of full duty cycle).Lower numbers (e.g. 20–30) = gentler
        # push, stops earlier. Higher numbers (like 50+) = pushes harder before 
        # declaring “stall,” which could stress the mechanism or scrape the ground.

        # then options
        # Stop.COAST → motor powers off, free to move. # Stop.BRAKE → motor 
        # resists movement a little. Stop.HOLD → motor locks position and keeps 
        # holding it (best for arms that you want to stay down).
        arm.run_until_stalled(speed=-120, then=Stop.HOLD, duty_limit=30)

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