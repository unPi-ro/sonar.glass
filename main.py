import utime
import uos

from sonar import Ultrasonic
from buzzer import Buzzer
from temperature import celsius


# our Reset/s Time Clock at boot
with open('main.txt', 'w') as f:
    f.write("{} at main.py said Hello World on {}".format(uos.uname().machine, utime.localtime()))

# take ur time
#utime.sleep(5)

# surpise! boot.py globals are visible in main (too)
# reconfigure the timer, hence led to flash a bit less
timer.init(freq=1, mode=Timer.PERIODIC, callback=tick)

# instantiate all (3) distance sensors
uLeft = Ultrasonic(triggerPin=3, echoPin=2)
uRight = Ultrasonic(triggerPin=7, echoPin=6)
uCenter = Ultrasonic(triggerPin=11, echoPin=10)

hLeft = Buzzer(signalPin=18)
hRight = Buzzer(signalPin=13)

while True:

    # start measuring
    utime.sleep(0.100)
    uCenter.measure()
    utime.sleep(0.100)
    uLeft.measure()
    utime.sleep(0.100)
    uRight.measure()
    utime.sleep(0.100)
    # sonars are ready
        
    ucm = min(uLeft.cm, uCenter.cm, uRight.cm)
    if ucm == uLeft.cm: hLeft.beep(ucm)
    if ucm == uRight.cm: hRight.beep(ucm)
    if ucm == uCenter.cm:           
        hLeft.alert(ucm)
        hRight.alert(ucm)
        # a bit longer beep
        utime.sleep(0.200)
        hLeft.stop()
        hRight.stop()

    print("nearest obstacle detected at", ucm, "cm, air temperature cca", celsius(), "C")
    print("measurements [in cm] from all existing sonars were", uLeft.cm, uCenter.cm, uRight.cm)
    #utime.sleep(0.2)
