import utime

# just a placeholder / demo code

# our Reset/s Time Clock at boot
with open('main.txt', 'w') as f:
    f.write("Pico's main.py said Hello World on {}".format(utime.localtime()))

# take ur time
utime.sleep(5)

# surpise! boot.py globals are visible in main (too)
# lets turn off the timer, then led, if we got here
timer.deinit()
led.off()
