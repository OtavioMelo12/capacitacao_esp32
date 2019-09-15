import time
from machine import Pin

blue_led = Pin(23, Pin.OUT)
red_led = Pin(22, Pin.OUT)

def purple_rain():
    print("INICIOU O CODIGO")
    while True:
        print("PISCANDO LED...")
        blue_led.on()
        red_led.on()
        time.sleep(1)
        blue_led.off()
        red_led.off()
        time.sleep(1)