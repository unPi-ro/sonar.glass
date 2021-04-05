import micropython
import temperature

# irq ISRs won't produce error reports unless
micropython.alloc_emergency_exception_buf(100)

from machine import Pin
import utime

INFINITY = micropython.const(float('inf'))

@micropython.native
class Ultrasonic():
    # supports (only) the low voltage (simple, standard, non i2c breakouts) HC-SR04+ or HC-SR04p sensor
    # https://shop.4tronix.co.uk/collections/sensors/products/hc-sr04p-low-voltage-ultrasonic-distance-sensor
    
    RANGE = 450 # max range of this ultrasonic sensor in centimeters
    # give it a name, vertical and horizontal field of view in degrees
    (name, orientation, verticalFoV, horizontalFoV) = ("", {}, 15, 30)
    # records stop/start micro ticks, plus last distance calculated
    (start, stop, distance, calculated) = (0.0, 0.0, INFINITY, True)
    
    @property
    def cm(self):
        # show all cases
        if self.ranging:
            return INFINITY
        else:
            if self.calculated:
                return self.distance
            else:
                # time in microseconds spent by our ultrasound signal in the air
                uticks = utime.ticks_diff(self.stop, self.start)
                # speed of sound adjusted to (estimated) environment's temperature
                speed = 331.3 + 0.606 * self.temperature
                # overwrite previously calculated distance only after doing ranging
                # microseconds to seconds is / 1000000, then meters into cm is *100
                # uticks could be a small number, better doing math * before / 10^4
                self.distance = uticks * speed / 10000 / 2
                self.calculated = True
                return self.distance
                
    @property
    def mm(self): return self.cm * 10
    
    @property
    def temperature(self):
        # leave room for improvement
        return temperature.celsius()
        
    def __init__(self, triggerPin, echoPin):
        # just being verbose
        self.ranging = False
        # serving infinity 1st
        self.calculated = True
        
        self.echo = Pin(echoPin, Pin.IN, Pin.PULL_DOWN)
        self.trigger = Pin(triggerPin, Pin.OUT, Pin.PULL_DOWN)

        # following the ISR rules for writting IRQ (class) handlers for MicroPython
        # https://docs.micropython.org/en/latest/reference/isr_rules.html#isr-rules
        self.refStop = self.handlerStop
        self.refStart = self.handlerStart
        
        # make sure is low
        self.trigger.low()
        utime.sleep_us(2)
        
        # arming the IRQ (class) handlers
        self.trigger.irq(self.handlerRanging, Pin.IRQ_RISING)
        self.echo.irq(self.handlerStart, Pin.IRQ_RISING)
    
    def measure(self):
        if not self.ranging:           
            self.trigger.high()
            utime.sleep_us(5)
            self.trigger.low()
            # now let the IRQs do the work

    def handlerRanging(self, pin):
        self.ranging = True
        
    def handlerStart(self, pin):
        # will NOT trigger unless all PINs are connected
        if self.ranging:
            self.start = utime.ticks_us()
            # re-arm the irq handling for next iteration
            # passing a handler* would be bad/allocation
            self.echo.irq(self.refStop, Pin.IRQ_FALLING)
            # ignore the previously (calculated) distance
            self.calculated = False

    def handlerStop(self, pin):
        # will NOT trigger unless all PINs are connected
        if self.ranging:
            self.stop = utime.ticks_us()
            self.ranging = False
            # re-arm the irq handling for next iteration
            # passing a handler* would be bad/allocation
            self.echo.irq(self.refStart, Pin.IRQ_RISING)


if __name__ == '__main__':
    # change to your actual HC-SR04p pins
    uLeft=Ultrasonic(triggerPin=3, echoPin=2)
    uRight=Ultrasonic(triggerPin=7, echoPin=6)
    uCenter=Ultrasonic(triggerPin=11, echoPin=10)

    # trigger
    uLeft.measure()
    uRight.measure()
    uCenter.measure()
    
    # wait for sonar
    utime.sleep(0.5)
    ucm = min(uLeft.cm, uCenter.cm, uRight.cm)
    print("nearest obstacle detected at", ucm, "cm, air temperature cca", temperature.celsius(), "C")
    print("measurements [in cm] from all existing sonars were", uLeft.cm, uCenter.cm, uRight.cm)
