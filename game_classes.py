from game_constants import *
from util import *
import math
import random

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
    def __init__(self, x, pen):
        self.x = x
        self.pen = pen
        
        self.activate_time_us = 0
        self.activated = False
        self.used = False
    
    # Desativa após 5 segundos
    def update(self):
        if utime.ticks_us() - self.activate_time_us > 5000000:
            self.activated = False
    
    def draw(self):
        if self.activated:
            display.set_pen(self.pen)
            display.rectangle(self.x - 2, 0, 5, HEIGHT-1)
    
    def activate(self):
        if self.used: # Ativa apenas se não foi utilizado ainda
            return
        
        self.used = True
        self.activate_time_us = utime.ticks_us()
        self.activated = True
    
    def deactivate(self):
        self.activated = False
    
    def available(self):
        return game.state == GAME_RUNNING and not self.used
    
    def reset(self):
        self.activate_time_us = 0
        self.activated = False
        self.used = False

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
    def point(self, player):
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
            self.announce_set_victory(set_winner)
            
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
    def announce_set_victory(self, player):
        play_tone(523, 200, 50)
        play_tone(659, 200, 50)
        play_tone(784, 300, 200)
        
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
    def __init__(self, glove, pad, shield, invert_controls, ready_text_side):
        self.glove = glove
        self.pad = pad
        self.shield = shield
        self.invert_controls = invert_controls
        self.ready_text_side = ready_text_side
        
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
            new_angle = math.pi - new_angle
            
        angle = self.angle_filter.filter(new_angle)
        self.pad.update(angle)
    
    def button_pressed(self):
        return self.glove.get_button_state(6) == 1

    def draw(self):
        self.pad.draw()
        self.shield.draw()
        
        if self.shield.available():
            self.glove.set_power_led(0, ON)
        else:
            self.glove.set_power_led(0, OFF)
        
        if game.state == GAME_BREAK:
            self.show_ready()
    
    def reset(self):
        self.shield.reset()
        self.pad.reset()
        self.glove.set_power_led(0, OFF)
    
    def show_ready(self):
        if not self.button_pressed():
            return
        
        display.set_pen(st7789.WHITE)
        display.set_font("small_font")
        text = "ready"
        text_width = display.measure_text(text, 2)
        
        if self.ready_text_side == LEFT:
            text_x = 0 + 10
        else:
            text_x = WIDTH - 10 - text_width
            
        display.text(text, text_x, 10, 255, 2)
    
# -------------------- Pad do Jogador --------------------

# Inicializa o pad e a bola
class PlayerPad:
    def __init__(self, x, y, pen):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.pen = pen
        
    def update(self, angle):
        if angle < 0:
            return
        
        self.y = map_value(angle, 0 + math.pi/4, math.pi - math.pi/4, PAD_WIDTH//2, WIDTH - PAD_WIDTH//2)
        
        # Limita a movimentação do pad
        if self.y < PAD_WIDTH // 2:
            self.y = PAD_WIDTH // 2
        elif self.y + PAD_WIDTH // 2 > WIDTH:
            self.y = WIDTH - PAD_WIDTH // 2

    def draw(self):
        display.set_pen(self.pen)
        display.rectangle(int(self.x), int(self.y) - PAD_WIDTH//2, PAD_WEIGHT, PAD_WIDTH)
    
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        
# -------------------- Bola --------------------

class Ball:
    def __init__(self, x, y, pen):
        self.vmax = BALL_VMAX
        self.x = x
        self.y = y
        self.vx = -self.vmax
        self.vy = 0
        self.pen = pen
        
        self.sound_freq = 0
        self.sound_on = False
        self.start_sound_us = 0
        
    def collision_check(self, player1, player2):
        pad1 = player1.pad
        pad2 = player2.pad
        
        if player1.shield.activated and self.x < BALL_RADIUS:
            player1.shield.deactivate()
            self.x = BALL_RADIUS
            self.vx = -self.vx
            return True
        
        if player2.shield.activated and self.x > WIDTH - BALL_RADIUS:
            player2.shield.deactivate()
            self.x = WIDTH - BALL_RADIUS
            self.vx = -self.vx
            return True
        
        # Colisão com o pad do player 1
        if self.vx < 0 and abs(self.x - PAD_WEIGHT - pad1.x) < BALL_RADIUS and abs(self.y - pad1.y) <= BALL_RADIUS + PAD_WIDTH // 2 :
            self.vx = -self.vx
            
            hs = PAD_WIDTH // 2
            dir = self.y - pad1.y
            dir /= hs
            dir *= 1.1
            
            self.vy = dir * self.vmax
            
            self.x = pad1.x + PAD_WEIGHT + BALL_RADIUS
            return True
            
        # Colisão com o pad do player 2
        if self.vx > 0 and abs(self.x - pad2.x) < BALL_RADIUS and abs(self.y - pad2.y) <= BALL_RADIUS + PAD_WIDTH // 2 :
            self.vx = -self.vx
            
            hs = PAD_WIDTH // 2
            dir = self.y - pad2.y
            dir /= hs
            dir *= 1.25
            
            self.vy = dir * self.vmax
            
            self.x = pad2.x - BALL_RADIUS
            return True
            
        # Colisões com as bordas
        if self.y - BALL_RADIUS <= 0:
            self.vy = -self.vy
            self.y = BALL_RADIUS
            return True
        
        if self.y + BALL_RADIUS >= WIDTH:
            self.vy = -self.vy
            self.y = WIDTH - BALL_RADIUS
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
    
    def update(self, player1, player2):
        prev_vx = self.vx
        
        self.update_position(player1, player2)
        
        if prev_vx != self.vx:
            self.vmax += 0.3
            self.vx = signal(self.vx) * self.vmax
            
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

    def draw(self):
        display.set_pen(self.pen)
        display.circle(int(self.x), int(self.y), BALL_RADIUS)
    
    def out(self):
        return self.out_side() != 0
        
    def out_side(self):
        if self.x < 0 - BALL_RADIUS:
            return 2
        elif self.x > WIDTH + BALL_RADIUS:
            return 1
        return 0
    
    # hard reset -> volta p/ vmax = BALL_VMAX, caso contrario, pode voltar menos
    def reset(self, hard):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.vy = 0
       
        if hard:
            self.vmax = BALL_VMAX
        else:
            self.vmax = max(BALL_VMAX, self.vmax * 0.7)
            
        self.vx = signal(self.vx) * self.vmax
        
    def randomize_direction(self):
        self.vx *= random.choice([-1, 1])

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
