from game_constants import *
import utime
import st7789

import vga1_8x8 as small_font
import vga1_16x32 as big_font
import vga1_bold_16x32 as big_bold_font

# ---------------------------------------- Funções auxiliares ----------------------------------------

# realiza troca de escala
def map_value(value, from_low, from_high, to_low, to_high):
    return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low

# retorna index de um led na matriz de acordo com a posição X, Y
def led_index(x, y, largura=5):
    if y % 2 == 1:
        return y * largura + x
    else:
        return y * largura + (largura - 1 - x)

# Retorna o sinal do número x, 1 para positivo e -1 para negativo
def signal(x):
    if x == 0:
        return 1
    return int(x / abs(x))

# Desenha opções de quantidade de Sets, selecionando a enviada em selected
def draw_options(display, selected, spacing):
    
    display.fill_rect(50, 80, WIDTH-50*2, spacing*len(n_sets_options), st7789.BLACK)

    # Desenho das opções
    for i, option in enumerate(n_sets_options):
        text = str(option)
        y_position = 80 + spacing * i

        if i == selected:
            # Setando o marcador para a opção selecionada
            print_x_centered_text(display, small_font, "> <", y_position, st7789.MAGENTA)

        print_x_centered_text(display, small_font, text, y_position, st7789.WHITE)
    
# Função para tocar uma nota de frequencia, duração e pausa dadas
def play_tone(frequency, duration, pause):
    buzzer.freq(frequency)
    buzzer.duty_u16(2000)
    utime.sleep_ms(duration)
    buzzer.duty_u16(0)
    utime.sleep_ms(pause)

# Função de animação do PAD do jogador vencedor para o centro da tela
def animate_pad_to_center(pad, target_x, target_y, duration=1.0):
    # Calcular a distância total que o pad deve percorrer
    start_x = pad.x
    start_y = pad.y
    distance_x = target_x - start_x
    distance_y = target_y - start_y
    
    # Obter o tempo de início da animação
    start_time = utime.ticks_ms()
    elapsed_time = 0

    while elapsed_time < duration * 1000:  # duração convertida para milissegundos
        # Calcular quanto tempo se passou desde o início
        current_time = utime.ticks_ms()
        elapsed_time = utime.ticks_diff(current_time, start_time)

        # Calcular a fração do caminho percorrido com base no tempo passado
        t = min(elapsed_time / (duration * 1000), 1.0)  # Garantir que t não exceda 1
        
        # Atualizar a posição do pad com base na fração do tempo
        pad.x = start_x + t * distance_x
        pad.y = start_y + t * distance_y

        # Limpa a tela
        display.set_pen(st7789.BLACK)
        display.clear()
        
        # Desenhar o pad
        pad.draw()
        
        # Atualiza o display
        display_draw_fbuf()
        
        # Pequena pausa para suavizar a animação (pode ser ajustado conforme necessário)
        utime.sleep(0.01)

    # Garantir que o pad chegue exatamente ao destino
    pad.x = target_x
    pad.y = target_y
    
    # Limpa a tela e desenha o pad na posição final
    display.set_pen(st7789.BLACK)
    display.clear()
    pad.draw()
    display_draw_fbuf()

# Música de finalizacão de um jogo
def end_song():
    play_tone(659, 200, 50)  # E5
    play_tone(784, 200, 50)  # G5
    play_tone(880, 200, 50)  # A5
    play_tone(988, 300, 100)  # B5 (nota mais longa)

    play_tone(1046, 150, 50)  # C6
    play_tone(988, 150, 50)  # B5
    play_tone(880, 150, 50)  # A5
    play_tone(784, 150, 50)  # G5

    play_tone(523, 250, 100)  # C5 (oitava baixa, um pouco de variação)
    play_tone(587, 250, 100)  # D5

    play_tone(659, 200, 50)  # E5
    play_tone(784, 200, 50)  # G5
    play_tone(880, 300, 100)  # A5 (com final destacado)

    play_tone(1046, 400, 200)  # C6 (nota final prolongada para o efeito de vitória)

# Apaga a tela OLED
def clear_oled_screen(oled):
    oled.fill(0)  # Limpa a tela preenchendo-a com preto
    oled.show()   # Atualiza o display

# Desenha um texto centralizado na tela OLED
def center_text(oled, text, y):
    """Calcula a posição x para centralizar o texto."""
    text_width = len(text) * 8   # Aproximando a largura do texto
    x = (128 - text_width) // 2  # Centraliza no display
    oled.text(text, x, y, 1)  # Desenha o texto

# Desenha Set atual na tela
def draw_oled_set_info(oled, set_number, total_sets):
    clear_oled_screen(oled)  # Limpa a tela antes de desenhar

    # Desenha "SET" centralizado no topo
    center_text(oled, f"SET {set_number} / {total_sets}", 32-4)

    oled.show()  # Atualiza o display

def print_x_centered_text(display, font, text, y, color):
    text_width = len(text) * font.WIDTH
    display.text(font, text, (WIDTH - text_width) // 2, y, color)
    
def clear_fbuf(fbuf):
    fbuf.fill(st7789.BLACK)

def display_draw_fbuf(display, fbuf):
    display.blit_buffer(fbuf, 0, 0, WIDTH, HEIGHT)

def beep_beep(buzzer):
    buzzer.freq(440)
    buzzer.duty_u16(2000)
    utime.sleep_ms(100)
    buzzer.duty_u16(0)
    utime.sleep_ms(50)
    buzzer.duty_u16(2000)
    utime.sleep_ms(100)
    buzzer.duty_u16(0)