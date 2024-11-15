"""TTGO T-Display RP2040 display"""

from machine import Pin, SPI
from time import sleep
import st7789

def config():
    spi = SPI(0,
        baudrate=62500000,
        polarity=0,
        phase=0,
        sck=Pin(18, Pin.OUT),
        mosi=Pin(19, Pin.OUT),
        miso=None)

    return st7789.ST7789(
        spi,
        128,
        160,
        cs=Pin(17, Pin.OUT),
        dc=Pin(16, Pin.OUT),
        reset=Pin(20, Pin.OUT),
        backlight=Pin(8, Pin.OUT),
        rotation=2,
        buffer_size=0,
        color_order=st7789.RGB,
        inversion=False)
