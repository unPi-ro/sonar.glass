from machine import Pin, Timer

# Red on the tiny Pico
rgbRed = Pin(18, Pin.OUT)
# Green on the tiny Pico
rgbGreen = Pin(19, Pin.OUT)
# Blue on the tiny Pico
rgbBlue = Pin(20, Pin.OUT)

# from https://github.com/raspberrypi/pico-micropython-examples/blob/master/blink/blink.py

# always Green on the (standard) Pico
led = Pin(25, Pin.OUT)

timer = Timer()
def tick(timer):
    global led
    led.toggle()

timer.init(freq=1, mode=Timer.PERIODIC, callback=tick)
