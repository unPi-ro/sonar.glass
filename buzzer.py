import utime
from machine import Pin, PWM


class Buzzer():
    
    SCALE = [5, 3, 2, 1, 1, 0]
    
    def __init__(self, signalPin):
        self.signal = PWM(Pin(signalPin))
        self.signal.freq(1000)
        self.signal.duty_u16(0)
        
    def multiplier(self, cm):
        if cm < 101: return self.SCALE[0]
        if cm < 201: return self.SCALE[1]
        if cm < 301: return self.SCALE[2]
        if cm < 401: return self.SCALE[3]
        if cm < 501: return self.SCALE[4]
        return self.SCALE[5]

    def stop(self):
        self.signal.duty_u16(0)
        
    def beep(self, cm):
        self.signal.freq(110 * (2 ** self.multiplier(cm)))
        self.signal.duty_u16(10000) #* self.multiplier(cm))
        utime.sleep(0.100)
        self.stop()

    def alert(self, cm):
        self.signal.freq(110 * (2 ** self.multiplier(cm)))
        self.signal.duty_u16(10000) #* self.multiplier(cm))


class Haptic(Buzzer): pass
