from game_constants import *
from util import *
import math
import random

import vga1_8x8 as small_font
import vga1_16x32 as big_font
import vga1_bold_16x32 as big_bold_font

# ---------------------------------------- Classes ----------------------------------------

# -------------------- Jogo --------------------

# Variáveis de um jogo
class Game:
    def __init__(self, player1, player2, score, ball):
        self.state = MENU
        self.n_sets = 0
        self.winner = 0
        self.player1 = player1
        self.player2 = player2
        self.score = score
        self.ball = ball

# -------------------- Escudo --------------------

# Poder de escudo
class Shield:
    def __init__(self, y, color):
        self.y = y
        self.color = color
        self.activated = False
    
    def draw(self, fbuf):
        if self.activated:
            fbuf.rect(0, self.y, WIDTH, SHIELD_WEIGHT, self.color, True)
    
    def activate(self):
        self.activated = True
    
    def deactivate(self):
        self.activated = False
    
    def reset(self):
        self.activated = False

# -------------------- Placar --------------------

# Placar, gerencia a matriz de LEDs para mostrar pontuações do Set e do Jogo
class Score:
    def __init__(self, np):
        self.points1 = 0
        self.points2 = 0
        self.match_point = 2
        self.n_sets = 0
        self.set_wins = []
        self.np = np
    
    # Retorna True se o jogo tiver terminado, False caso contrário
    def point(self, buzzer, player):
        if self.points1 == 4 and self.points2 == 4: # logica "vai a dois"
            if player == 1:
                self.match_point += -1
            elif player == 2:
                self.match_point += 1
            
            if self.match_point == 0:
                self.points1 += 1
            if self.match_point == 4:
                self.points2 += 1
                
        else: # logica padrao
            if player == 1:
                self.points1 += 1
            elif player == 2:
                self.points2 += 1
            
        self.draw()
        
        set_winner = -1
        
        if self.points1 == 5:
            set_winner = 1
        elif self.points2 == 5:
            set_winner = 2
        
        if set_winner != -1: # Verifica se o set terminou
            self.announce_set_victory(buzzer, set_winner)
            
            self.set_wins.append(set_winner)
            self.points1 = 0
            self.points2 = 0
            
            self.draw()
            
            if self.get_game_winner() != -1: # Verifica se o jogo terminou
                return True
        
        return False
            
    def draw(self):
        # Apaga a tela
        for i in range(NUM_LEDS):
            self.np[i] = (0, 0, 0)
        
        # Desenha pontos do vermelho (jogador 1)
        for i in range(self.points1):
            led = led_index(0, i)
            self.np[led] = (ON_BRIGHTNESS, 0, 0)
            
        # Desenha pontos do vermelho (jogador 2)
        for i in range(self.points2):
            led = led_index(4, i)
            self.np[led] = (0, 0, ON_BRIGHTNESS)
        
        # Desenha ponto do vai a dois
        if self.points1 == 4 and self.points2 == 4:
            led = led_index(self.match_point, 4)
            
            if self.match_point == 1:
                r = ON_BRIGHTNESS
                g = ON_BRIGHTNESS//4
                b = ON_BRIGHTNESS//4
            elif self.match_point == 2:
                r = ON_BRIGHTNESS
                g = ON_BRIGHTNESS
                b = ON_BRIGHTNESS
            elif self.match_point == 3:
                r = 0
                g = int(ON_BRIGHTNESS/1.5)
                b = ON_BRIGHTNESS
            
            self.np[led] = (r, g, b)
        
        # Desenha vitórias dos sets
        for i in range(len(self.set_wins)):
            led = led_index(2, i)
    
            if self.set_wins[i] == 1:
                color = (ON_BRIGHTNESS, 0, 0)
            elif self.set_wins[i] == 2:
                color = (0, 0, ON_BRIGHTNESS)
            
            self.np[led] = color
            
        self.np.write()
    
    # Animação de fim de Set
    def announce_set_victory(self, buzzer, player):
        play_tone(buzzer, 523, 200, 50)
        play_tone(buzzer, 659, 200, 50)
        play_tone(buzzer, 784, 300, 200)
        
        while self.points1 > 0 or self.points2 > 0:
            
            if self.points1 > 0:
                self.points1 -= 1
            
            if self.points2 > 0:
                self.points2 -= 1
            
            self.draw()
            
            utime.sleep_ms(150)
        
        for i in range(2):
            self.set_wins.append(player)
            self.draw()
            utime.sleep_ms(250)
            self.set_wins.pop()
            self.draw()
            utime.sleep_ms(250)
    
    def reset(self, n_sets=0):
        self.points1 = 0
        self.points2 = 0
        self.match_point = 2
        self.n_sets = n_sets
        self.set_wins = []
    
    # Retorna -1 se o jogo ainda não terminou, ou 1/2 se algum jogador venceu
    def get_game_winner(self):
        player1_set_wins = self.set_wins.count(1)
        player2_set_wins = self.set_wins.count(2)

        game_winner = -1
        required_wins = self.n_sets // 2 + 1
        
        if player1_set_wins >= required_wins:
            game_winner = 1
        elif player2_set_wins >= required_wins:
            game_winner = 2
        
        return game_winner
        
# -------------------- Jogador --------------------

class Player:
    def __init__(self, glove, pad, shield, invert_controls, side):
        self.glove = glove
        self.pad = pad
        self.shield = shield
        self.invert_controls = invert_controls
        self.side = side
        self.power = 0
        
        self.angle_filter = LowPassAngleFilter(cutoff_frequency, sampling_time)
        self.glove.set_power_leds(4*[OFF])

        self.enemy_player = None
        self.invisibility_counter = 0 # if > 0, invisble. Decrements each time player hits the ball.

        self.button_states = {0: 0, 1: 0, 2: 0, 3: 0}  # Estado inicial dos botões (todos soltos)
        self.powers = {
            0: {"cost": 1, "action": lambda: self.enemy_player.increment_invisiblity_counter(INVISIBILITY_POWER_INCREMENT)},
            1: {"cost": 2, "action": self.shield.activate},
            2: {"cost": 3, "action": lambda: print("Poder com custo 3 ativado!")},
            3: {"cost": 4, "action": lambda: print("Poder com custo 4 ativado!")}
        }
        
    def update(self):
        # Calcula posição baseado no acelerômetro
        self.update_position()

        # Verifica pressionamentos dos botões para utilizar os poderes
        for button, power_info in self.powers.items():
            current_state = self.glove.get_button_state(button)
            if current_state == 1 and self.button_states[button] == 0:  # Botão passou de solto para pressionado
                if self.power >= power_info["cost"]:
                    self.spend_power(power_info["cost"])
                    power_info["action"]()
            self.button_states[button] = current_state  # Atualiza o estado do botão
        
    def update_position(self):
        # Lê os dados do MPU6050
        new_angle = self.glove.get_angle()
        
        if self.invert_controls:
            new_angle = - new_angle
            
        angle = self.angle_filter.filter(new_angle)
        self.pad.update(angle)

    def draw(self, fbuf):
        if self.invisibility_counter == 0:
            self.pad.draw(fbuf)
        else:
            self.draw_invisibility_count(fbuf)
        
        self.shield.draw(fbuf)
    
    def draw_invisibility_count(self, fbuf):
        # Determina a posição Y com base no lado
        if self.side == TOP:
            y = HEIGHT // 4
        else:
            y = HEIGHT - HEIGHT // 4 - 8

        # Converte o contador para string
        string = str(self.invisibility_counter)

        # Calcula a largura do texto
        text_width = len(string) * 8  # Assume que cada caractere tem 8 pixels de largura

        # Desenha o texto centralizado
        fbuf.text(string, (WIDTH - text_width) // 2, y, st7789.WHITE)

    def reset(self):
        self.shield.reset()
        self.pad.reset()
        self.deactivate_invisibility()
    
    def update_power(self, new_value):
        self.power = new_value
        self.update_power_leds()
        
    def add_power(self):
        if self.power == 4:
            for _ in range(2):  # Repetir duas vezes
                self.glove.set_power_leds(4*[OFF])
                self.glove.buzz(True)  # Ativa o buzzer
                utime.sleep_ms(100)
                self.glove.set_power_leds(4*[ON])
                self.glove.buzz(False)  # Desativa o buzzer
                utime.sleep_ms(100)
        else:
            self.update_power(self.power + 1)
        
    def spend_power(self, amount):
        self.update_power(self.power - amount)
    
    def reset_power(self):
        self.update_power(0)
    
    def ready_button_pressed(self):
        return self.glove.get_button_state(0) == 1
    
    def show_ready(self, fbuf):
        if not self.ready_button_pressed():
            return

        if self.side == TOP:
            y = HEIGHT//4
        else:
            y = HEIGHT - HEIGHT//4 - 8
        
        text_width = 5*8
        
        fbuf.text("READY", (WIDTH - text_width)//2, y, st7789.WHITE)
    
    def update_power_leds(self):
        for i in range(4):
            self.glove.set_power_led(3-i, ON if i < self.power else OFF)

    def set_enemy_player(self, player):
        self.enemy_player = player

    def increment_invisiblity_counter(self, amount):
        self.invisibility_counter += amount

    def decrement_invisibility_counter(self):
        if self.invisibility_counter == 0:
            return
        self.invisibility_counter -= 1
    
    def deactivate_invisibility(self):
        self.invisibility_counter = 0

    def round_init(self):
        # Inicializa estado dos botões, caso algum jogador comece pressionando algum botão
        for button, power_info in self.powers.items():
            current_state = self.glove.get_button_state(button)
            self.button_states[button] = current_state

    
# -------------------- Pad do Jogador --------------------

# Inicializa o pad e a bola
class PlayerPad:
    def __init__(self, x, y, color):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.color = color
        self.left_angle = math.pi/4
        self.right_angle = - math.pi/4
        
    def update(self, angle):
        self.x = map_value(angle, self.left_angle, self.right_angle, PAD_WIDTH//2, WIDTH - PAD_WIDTH//2)
        
        # Limita a movimentação do pad
        if self.x < PAD_WIDTH // 2:
            self.x = PAD_WIDTH // 2
        elif self.x + PAD_WIDTH // 2 > WIDTH:
            self.x = WIDTH - PAD_WIDTH // 2

    def draw(self, fbuf):
        fbuf.rect(int(self.x) - PAD_WIDTH//2, int(self.y), PAD_WIDTH, PAD_WEIGHT, self.color, True)
    
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        
# -------------------- Bola --------------------

class Ball:
    def __init__(self, x, y, color):
        self.vmax = BALL_VMAX
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = self.vmax
        self.color = color
        
        self.sound_freq = 0
        self.sound_on = False
        self.start_sound_us = 0
        
    def collision_check(self, player1, player2):
        # Verifica colisão com o shield
        if self.check_shield_collision(player1):
            return True
        if self.check_shield_collision(player2):
            return True

        # Verifica colisão com os pads dos jogadores
        if self.check_pad_collision(player1):
            return True
        if self.check_pad_collision(player2):
            return True

        # Verifica colisões com as bordas horizontais
        if self.x - BALL_RADIUS <= 0:
            self.vx = -self.vx
            self.x = BALL_RADIUS
            return True

        if self.x + BALL_RADIUS >= WIDTH:
            self.vx = -self.vx
            self.x = WIDTH - BALL_RADIUS
            return True

        # colisão vertical antes do jogador vermelho, PARA TESTES, REMOVER QUANDO NÃO PRECISAR MAIS
        if self.y - BALL_RADIUS < 20:
            self.vy = -self.vy
            self.y = 20 + BALL_RADIUS
            return True

        return False

    def check_shield_collision(self, player):
        if player.shield.activated and (
            (player.side == TOP and self.y < BALL_RADIUS) or 
            (player.side == BOTTOM and self.y > HEIGHT - BALL_RADIUS)
        ):
            player.shield.deactivate()
            self.vy = -self.vy
            self.y = BALL_RADIUS + SHIELD_WEIGHT if player.side == TOP else HEIGHT - (BALL_RADIUS + SHIELD_WEIGHT)
            return True
        return False

    def check_pad_collision(self, player):
        pad = player.pad
        if (
            (self.vy < 0 and player.side == TOP and abs(self.y - PAD_WEIGHT - pad.y) < BALL_RADIUS) or
            (self.vy > 0 and player.side == BOTTOM and abs(self.y - pad.y) < BALL_RADIUS)
        ) and abs(self.x - pad.x) <= BALL_RADIUS + PAD_WIDTH // 2:
            self.vy = -self.vy

            # Ajusta a direção horizontal com base na posição da colisão no pad
            hs = PAD_WIDTH // 2
            dir = (self.x - pad.x) / hs * 1.25
            self.vx = dir * self.vmax

            # Reposiciona a bola para fora do pad
            self.y = pad.y + PAD_WEIGHT + BALL_RADIUS if player.side == "top" else pad.y - BALL_RADIUS

            # Decrementa contador de invisibilidade, para deixar o jogador mais próximo de restaurar sua visão
            player.decrement_invisibility_counter()
            return True
        return False

    def update_position(self, player1, player2):
        MOVE_LIMIT = 1
        
        # Calcula a distância a ser movida em x e y
        distance_x = self.vx
        distance_y = self.vy

        # Calcula o número de passos a serem dados
        steps_x = max(1, abs(distance_x) // MOVE_LIMIT)
        steps_y = max(1, abs(distance_y) // MOVE_LIMIT)

        # Define o incremento para cada passo
        step_x = distance_x / steps_x
        step_y = distance_y / steps_y

        # Move a bolinha em pequenos passos
        for step in range(int(max(steps_x, steps_y))):
            if step < steps_x:
                self.x += step_x
            if step < steps_y:
                self.y += step_y
            
            # Verifica colisão após cada incremento
            if self.collision_check(player1, player2):
                break
    
    def update(self, player1, player2, buzzer):
        prev_vy = self.vy
        
        self.update_position(player1, player2)
        
        if prev_vy != self.vy:
            self.vmax += SPEED_INCREMENT
            self.vy = signal(self.vy) * self.vmax
            
            if self.sound_freq == 0:
                buzzer.freq(880)
            if self.sound_freq == 1:
                buzzer.freq(440)
            
            self.sound_freq = 1 - self.sound_freq
                
            buzzer.duty_u16(2000)
            self.start_sound_us = utime.ticks_us()
            self.sound_on = True
        
        if self.sound_on and utime.ticks_us() - self.start_sound_us > 100000: # 100 ms duration
            buzzer.duty_u16(0)
            self.sound_on = False

    def draw(self, fbuf):
        fbuf.ellipse(int(self.x), int(self.y), BALL_RADIUS, BALL_RADIUS, self.color, True)
    
    def out(self):
        return self.out_side() != 0
        
    def out_side(self):
        if self.y < 0 - BALL_RADIUS:
            return 2
        elif self.y > HEIGHT + BALL_RADIUS:
            return 1
        return 0
    
    # hard reset -> volta p/ vmax = BALL_VMAX, caso contrario, pode voltar menos
    def reset(self, hard):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.vx = 0
       
        if hard:
            self.vmax = BALL_VMAX
        else:
            self.vmax = max(BALL_VMAX, self.vmax * 0.7)
            
        self.vy = signal(self.vy) * self.vmax
        
    def randomize_direction(self):
        self.vy *= random.choice([-1, 1])

# -------------------- Filtro passa baixa para ângulo --------------------

class LowPassAngleFilter:
    def __init__(self, cutoff_frequency, sampling_time):
        self.a = 1 / (1 + 1 / (2 * math.pi * cutoff_frequency * sampling_time))
        self.previous_output = 0

    def unwrap_angle(self, angle):
        delta = angle - self.previous_output
        if delta > math.pi:
            angle -= 2 * math.pi
        elif delta < -math.pi:
            angle += 2 * math.pi
        return angle

    def wrap_angle(self, angle):
        return (angle + math.pi) % (2 * math.pi) - math.pi

    def filter(self, input_signal):
        unwrapped_input = self.unwrap_angle(input_signal)
        current_output = self.a * unwrapped_input + (1 - self.a) * self.previous_output
        self.previous_output = current_output
        return self.wrap_angle(current_output)
