from machine import I2C, Pin, PWM, SoftI2C, ADC
from mpu6050 import MPU6050
from pcf8575 import PCF8575
from neopixel import NeoPixel
from ssd1306 import SSD1306_I2C
import tft_config
import framebuf
from glove import Glove

from game_constants import *

class Peripherals:
    def __init__(self):
        # Configurações do display SPI
        display = tft_config.config()
        display.init()
        display.on()
        self.display = display

        # Inicializa framebuffer
        self.fbuf = framebuf.FrameBuffer(bytearray(WIDTH * HEIGHT * 2), WIDTH, HEIGHT, framebuf.RGB565)

        # Barramentos I2C hardware
        I2C0 = I2C(0, scl=Pin(1), sda=Pin(0))
        I2C1 = I2C(1, scl=Pin(3), sda=Pin(2))

        # ----- Controle do Jogador 1 -----

        self.glove1 = Glove(I2C1)

        # ----- Controle do Jogador 2 -----

        self.glove2 = self.glove1 # Glove(I2C0)

        # Buzzer
        self.buzzer = PWM(Pin(10))

        # Joystick
        self.joystick_x = ADC(Pin(27))
        self.joystick_y = ADC(Pin(26))

        # Configuração Display OLED
        i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
        self.oled = SSD1306_I2C(128, 64, i2c)

        # Configuração Neopixel - Matriz de LEDs
        self.np = NeoPixel(Pin(7), NUM_LEDS)

        # Configuração dos botões da BitDogLab
        self.button_a = Pin(5, Pin.IN, Pin.PULL_UP)
        self.button_b = Pin(6, Pin.IN, Pin.PULL_UP)
