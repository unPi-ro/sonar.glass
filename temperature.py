import micropython
import machine
import utime

# inspired from https://github.com/raspberrypi/pico-micropython-examples/blob/master/adc/temperature.py

onboard_temperature_sensor = machine.ADC(4)
conversion_factor = micropython.const(3.3 / 65535)

def raw():
    reading = onboard_temperature_sensor.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706) / 0.001721
    
    return temperature
 
def celsius():
    return raw()-5
    # environment's temperature should be about temperature-5, see https://www.youtube.com/watch?v=rU381A-b79c

    
if __name__ == '__main__':
    print("estimated", celsius(), "C degrees at", utime.localtime())
