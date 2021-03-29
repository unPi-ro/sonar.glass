from machine import Pin, Timer
import utime

# TODO: booting preparation [code]

# Pico's onboard Green
led = Pin(25, Pin.OUT)
LED_state = True
timer = Timer()

def tick(timer):
    global led, LED_state
    LED_state = not LED_state
    led.value(LED_state)

# start flashing onboard led as a booting / setup hint
timer.init(freq=2, mode=Timer.PERIODIC, callback=tick)

# be fast! or your IDE will be slow to connect to Pico if:
#utime.sleep(5)

# our Reset/s Time Clock at boot
with open('boot.txt', 'w') as f:
    f.write("Pico's boot.py said Hello World on {}".format(utime.localtime()))
