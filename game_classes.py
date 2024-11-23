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
        
        self.angle_filter = LowPassAngleFilter(cutoff_frequency, sampling_time)
        
        self.current_led_state = -1 # unknown
        self.glove.set_power_led(0, OFF)
        
    def update(self):
        self.shield.update()
        
        if self.button_pressed():
            self.shield.activate()
    
        self.update_position()
        
    def update_position(self):
        # Lê os dados do MPU6050
        new_angle = self.glove.get_angle()
        
        if self.invert_controls:
            new_angle = - new_angle
            
        angle = self.angle_filter.filter(new_angle)
        self.pad.update(angle)
    
    def button_pressed(self):
        return self.glove.get_button_state(3) == 1

    def draw(self, fbuf):
        self.pad.draw(fbuf)
        self.shield.draw(fbuf)
        
        if self.shield.available():
            self.glove.set_power_led(0, ON)
        else:
            self.glove.set_power_led(0, OFF)
    
    def reset(self):
        self.shield.reset()
        self.pad.reset()
        self.glove.set_power_led(0, OFF)
    
    def show_ready(self, fbuf):
        if not self.button_pressed():
            return

        if self.side == UP:
            y = HEIGHT//4
        else:
            y = HEIGHT - HEIGHT//4 - 8
        
        text_width = 5*8
        
        fbuf.text("READY", (WIDTH - text_width)//2, y, st7789.WHITE)
    
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
        pad1 = player1.pad
        pad2 = player2.pad
        
        if player1.shield.activated and self.y < BALL_RADIUS:
            player1.shield.deactivate()
            self.y = BALL_RADIUS + SHIELD_WEIGHT
            self.vy = -self.vy
            return True
        
        if player2.shield.activated and self.y > HEIGHT - BALL_RADIUS:
            player2.shield.deactivate()
            self.y = HEIGHT - (BALL_RADIUS + SHIELD_WEIGHT)
            self.vy = -self.vy
            return True
        
        # Colisão com o pad do player 1
        if self.vy < 0 and abs(self.y - PAD_WEIGHT - pad1.y) < BALL_RADIUS and abs(self.x - pad1.x) <= BALL_RADIUS + PAD_WIDTH // 2 :
            self.vy = -self.vy
            
            hs = PAD_WIDTH // 2
            dir = self.x - pad1.x
            dir /= hs
            dir *= 1.25
            
            self.vx = dir * self.vmax
            
            self.y = pad1.y + PAD_WEIGHT + BALL_RADIUS
            return True
            
        # Colisão com o pad do player 2
        if self.vy > 0 and abs(self.y - pad2.y) < BALL_RADIUS and abs(self.x - pad2.x) <= BALL_RADIUS + PAD_WIDTH // 2 :
            self.vy = -self.vy
            
            hs = PAD_WIDTH // 2
            dir = self.x - pad2.x
            dir /= hs
            dir *= 1.25
            
            self.vx = dir * self.vmax
            
            self.y = pad2.y - BALL_RADIUS
            return True
            
        # Colisões com as bordas
        if self.x - BALL_RADIUS <= 0:
            self.vx = -self.vx
            self.x = BALL_RADIUS
            return True
        
        if self.x + BALL_RADIUS >= WIDTH:
            self.vx = -self.vx
            self.x = WIDTH - BALL_RADIUS
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
