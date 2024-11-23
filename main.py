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
pad1 = PlayerPad(WIDTH // 2, 0 + 10 - PAD_WEIGHT, swap_rgb565(st7789.RED))
pad2 = PlayerPad(WIDTH // 2, HEIGHT - 10, swap_rgb565(st7789.BLUE))
ball = Ball(WIDTH // 2, HEIGHT // 2, swap_rgb565(st7789.WHITE))

# Cria os escudos
shield1 = Shield(0, swap_rgb565(st7789.YELLOW))
shield2 = Shield(HEIGHT-SHIELD_WEIGHT, swap_rgb565(st7789.YELLOW))

# Cria os jogadores
player1 = Player(peripherals.glove1, pad1, shield1, False, TOP)
player2 = Player(peripherals.glove2, pad2, shield2, True, BOTTOM)

player1.set_enemy_player(player2)
player2.set_enemy_player(player1)

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
    