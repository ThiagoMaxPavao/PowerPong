from machine import I2C, Pin
from mpu6050 import MPU6050
from pcf8575 import PCF8575
import utime
import math

class Glove:
    def __init__(self, i2c, mpu_address=0x68, pcf_address=0x20, buzzer_pin=17, power_led_pins=None, rgb_pins=None, button_pins=None):
        # Inicialização de I2C, MPU6050 e PCF8575
        self.i2c = i2c
        self.mpu = MPU6050(self.i2c, address=mpu_address)
        self.pcf = PCF8575(self.i2c, address=pcf_address)

        # Configuração dos componentes
        self.buzzer = buzzer_pin
        self.power_led_pins = power_led_pins or [10, 11, 12, 13]
        self.rgb_pins = rgb_pins or [1, 2, 3]
        self.button_pins = button_pins or [4, 5, 6, 7]

        # Estados atuais dos LEDs de power
        self.current_power_led_states = [0] * len(self.power_led_pins)

        # Inicializar os pinos dos LEDs e botões
        self._initialize_pcf_pins()

        # Inicializar o MPU6050
        self.mpu.write_accel_range(0)  # range de maior precisão
        self.mpu.wake()  # Despertar o MPU6050

    def _initialize_pcf_pins(self):
        """Configura os pinos do expansor de I/O como entrada ou saída."""
        # Inicializa LEDs de power como saída
        self.pcf.pin(self.buzzer, 1)  # Saída desligada
        
        for pin in self.power_led_pins:
            self.pcf.pin(pin, 1)  # Saída desligada
        
        for pin in self.rgb_pins:
            self.pcf.pin(pin, 1)  # Saída desligada

    def set_rgb_color(self, color):
        """Configura a cor RGB nos LEDs."""
        self.pcf.pin(self.rgb_pins[0], 1 - color[0])
        self.pcf.pin(self.rgb_pins[1], 1 - color[1])
        self.pcf.pin(self.rgb_pins[2], 1 - color[2])

    def buzz(self, state):
        """Ativa ou desativa o buzzer."""
        self.pcf.pin(self.buzzer, 0 if state else 1)

    def read_acceleration(self):
        """Lê os dados do acelerômetro (x, y, z)."""
        accel_data = self.mpu.read_accel_data()
        return accel_data

    def get_angle(self):
        """Calcula o ângulo de inclinação baseado no acelerômetro."""
        accel_data = self.read_acceleration()
        angle = math.atan2(accel_data[2], accel_data[1])  # Calcula o ângulo com base nos dados
        return angle

    def get_button_state(self, index):
        pin = self.button_pins[index]
        return self.pcf.pin(pin)
        
    def get_button_states(self):
        """Retorna o estado de todos os botões (0 ou 1)."""
        states = []
        for pin in self.button_pins:
            states.append(self.pcf.pin(pin))  # Retorna 0 (não pressionado) ou 1 (pressionado)
        return states

    def set_power_led(self, led, state):
        """Define o estado de um LED de power, enviando comando apenas se necessário."""
        if self.current_power_led_states[led] != state:
            self.pcf.pin(self.power_led_pins[led], 1 - state)
            self.current_power_led_states[led] = state

    def set_power_leds(self, states):
        """Configura o estado dos LEDs de power com base nos estados fornecidos (0 ou 1)."""
        for i, state in enumerate(states):
            self.set_power_led(i, state)
            

if __name__ == '__main__':
    # Inicialização da luva com os pinos de I2C e outros componentes
    i2c = I2C(0, scl=Pin(1), sda=Pin(0))
    glove = Glove(i2c)

    # **Piscar LEDs de power (com comportamento do teste inicial)**
    state = 1
    for _ in range(2):
        for led in range(4):
            glove.set_power_led(led, state)
            utime.sleep_ms(100)
    
        state = 1 - state
        
    utime.sleep_ms(1000)
    
    for _ in range(2):  # Repetir duas vezes
        glove.buzz(True)  # Ativa o buzzer
        utime.sleep_ms(100)
        glove.buzz(False)  # Desativa o buzzer
        utime.sleep_ms(100)

    # **Teste de LEDs RGB (com todas as cores possíveis)**
    colors = [
        (0, 0, 0),  # desligado
        (1, 0, 0),  # vermelho
        (0, 1, 0),  # verde
        (0, 0, 1),  # azul
        (1, 1, 0),  # amarelo
        (0, 1, 1),  # ciano
        (1, 0, 1),  # roxo
        (1, 1, 1),  # branco
    ]

    for color in colors:
        glove.set_rgb_color(color)  # Atualiza a cor RGB
        utime.sleep_ms(500)  # Atraso entre as cores

    # **Laço principal - Atualização contínua**
    while True:
        # **Atualizar a cor RGB com base no ângulo do acelerômetro**
        angle = glove.get_angle()
        index = math.floor(8 * ((angle) / (2 * math.pi) + 1.0 / 2))  # Calcula o índice baseado no ângulo
        
        glove.set_rgb_color(colors[index])  # Atualiza a cor com base no índice

        # **Ler os estados dos botões**
        button_states = glove.get_button_states()
        print("Estados dos botões:", button_states)

        # **Atualizar os LEDs de power com base nos estados dos botões**
        glove.set_power_leds(button_states)  # Liga os LEDs de power conforme o estado dos botões

        # Aguarda 100ms antes de ler novamente
        utime.sleep_ms(100)
