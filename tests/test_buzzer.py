from machine import PWM, Pin
import time

buzzer_pin = machine.PWM(machine.Pin(18))

def test_buzzer():
    buzzer_pin.freq(1000)
    buzzer_pin.duty_u16(32768)
    time.sleep(1)
    buzzer_pin.duty_u16(0)
    time.sleep(1)
    buzzer_pin.freq(2000)
    buzzer_pin.duty_u16(32768)
    time.sleep(1)
    buzzer_pin.duty_u16(0)
    time.sleep(1)
    buzzer_pin.freq(3000)
    buzzer_pin.duty_u16(32768)
    time.sleep(1)
    buzzer_pin.duty_u16(0)
    time.sleep(1)

    buzzer_pin.deinit()

