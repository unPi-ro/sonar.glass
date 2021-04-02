import micropython
# sets? __debug__ False
micropython.opt_level(1)

# early work on https://glass.unpi.ro for unPi Sonar Glass
# our PINs might/will change, so please double check yours

import _thread as experiment
from machine import Pin, PWM
import utime, gc

# a HC-SR04P to look left
trigLeft = Pin(3, Pin.OUT)
echoLeft = Pin(2, Pin.IN)
# a HC-SR04P to look right
trigRight = Pin(7, Pin.OUT)
echoRight = Pin(6, Pin.IN)
# a HC-SR04P to look center
trigCenter = Pin(11, Pin.OUT)
echoCenter = Pin(10, Pin.IN)
# a lucky SparkFun RedBot Buzzer
pwm = PWM(Pin(13))

def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        if __debug__: print('*** Function {}() ran for {:3} ms'.format(myname, int(delta/1000)))
        return result
    return new_func

#@timed_function #OR
@micropython.native
def ultra(direction, trigger, echo):
    # inspired from https://www.tomshardware.com/how-to/raspberry-pi-pico-ultrasonic-sensor
    
    trigger.low()
    utime.sleep_us(2)
    
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    
    while echo.value() == 0: signaloff = utime.ticks_us()
    while echo.value() == 1: signalon = utime.ticks_us()
    
    timepassed = utime.ticks_diff(signalon, signaloff)
    
    distance = timepassed * 0.0343 / 2
    
    if __debug__: print("The distance from {} object is {:3} cm".format(direction,int(distance)))

def runLeft():
    while True:
        ultra("left", trigLeft, echoLeft)
        utime.sleep(1)
        
def runRight():
    while True:
        ultra("right", trigRight, echoRight)
        utime.sleep(1)

def runCenter():
    while True:
        ultra("center", trigCenter, echoCenter)
        utime.sleep(1)

def runTweet():
    # in a previous life it was a LED
    # https://github.com/raspberrypi/pico-micropython-examples/blob/master/pwm/pwm_fade.py
    
    # now it's a mosquito, by the sounds coming out from the SparkFun RedBot Buzzer
    
    pwm.freq(1000)

    duty = 0
    direction = 1
    for _ in range(8 * 256):
        duty += direction
        if duty > 255:
            duty = 255
            direction = -1
        elif duty < 0:
            duty = 0
            direction = 1
        pwm.duty_u16(duty * duty)
        utime.sleep(0.002)
        
experiment.start_new_thread(runCenter,())

runLeft()
