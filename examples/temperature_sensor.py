import micropython
import machine
import utime

# from https://github.com/raspberrypi/pico-micropython-examples/blob/master/adc/temperature.py

temperature_sensor = machine.ADC(4)
conversion_factor = micropython.const(3.3 / 65535)

while True:
    reading = temperature_sensor.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706) / 0.001721
    
    # interesting, Pico has an reset-at-boot realtime clock
    print(temperature, "C degrees at", utime.localtime())
    
    # environment's temperature should be about temperature-5, see also https://www.youtube.com/watch?v=rU381A-b79c
    
    utime.sleep(2)
