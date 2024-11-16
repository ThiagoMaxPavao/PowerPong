import utime
import math
import random
import st7789

from game_constants import *
from game_classes import *
from game_routines import *
from util import *
from peripherals import Peripherals

# ---------------------------------------- Inicializacão e loop do programa ----------------------------------------

# Inicializa todos os periféricos e armazena neste objeto
peripherals = Peripherals()

# Inicializa os pads e a bola
pad1 = PlayerPad(WIDTH // 2, 0 + 10 - PAD_WEIGHT, st7789.RED)
pad2 = PlayerPad(WIDTH // 2, HEIGHT - 10, st7789.BLUE)
ball = Ball(WIDTH // 2, HEIGHT // 2, st7789.WHITE)

# Cria os escudos
shield1 = Shield(0, st7789.YELLOW)
shield2 = Shield(WIDTH-1, st7789.YELLOW)

# Cria os jogadores
player1 = Player(peripherals.glove1, pad1, shield1, False, UP)
player2 = Player(peripherals.glove2, pad2, shield2, False, DOWN)

# Cria o placar
score = Score(peripherals.np)
score.draw()

# Cria gerenciador do jogo
game = Game(player1, player2, score, ball)

# Loop principal - lógica de estados
while True:
    
    if game.state == MENU:
        menu_routine(game, peripherals)
    elif game.state == CHOOSE_SETS:
        choose_sets_routine(game, peripherals)
    elif game.state == GAME_RUNNING:
        game_running_routine(game, peripherals)
    elif game.state == GAME_BREAK:
        game_break_routine(game, peripherals)
    elif game.state == END:
        end_routine(game, peripherals)
    