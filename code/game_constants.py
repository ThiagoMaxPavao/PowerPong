# Estados do Programa
GAME_RUNNING = 0
GAME_BREAK = 1
MENU = 2
CHOOSE_SETS = 3
END = 4

# Constantes de Jogo
BALL_VMAX = 2
BALL_RADIUS = 3
PAD_WIDTH = 50
PAD_WEIGHT = 6
SHIELD_WEIGHT = 2
SPEED_INCREMENT = 0.1

# Liga/Desliga
OFF = 0
ON = 1

# Lados
RIGHT = 0
LEFT = 1
TOP = 2
BOTTOM = 3

# Opcoes de numero de SETs
n_sets_options = [1, 3, 5]

# Matriz de LEDs
NUM_LEDS = 25
ON_BRIGHTNESS = 35 # Brilho padrão dos LEDs

# Configuracões para o filtro do sensor MPU6050
cutoff_frequency = 60.0  # frequência de corte em Hz
sampling_time = 0.001    # intervalo de amostragem em segundos

# Display 
WIDTH = 128
HEIGHT = 160

# Poderes
INVISIBILITY_POWER_INCREMENT = 3 # Em quanto incrementar o contador de invisibilidade quando um jogador utiliza o poder 
BUFFED_PAD_DURATION_MS = 5000 # Duração do pad buffado
