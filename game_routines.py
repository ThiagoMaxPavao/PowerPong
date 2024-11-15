import utime
from util import *
import st7789

import vga1_8x8 as small_font
import vga1_16x32 as big_font
import vga1_bold_16x32 as big_bold_font

# ---------------------------------------- Rotinas de tratamento dos estados ----------------------------------------

# -------------------- MENU --------------------

def menu_routine(game, peripherals):
    clear_oled_screen(peripherals.oled)

    peripherals.display.fill(st7789.BLACK)
    
    # Título
    print_x_centered_text(peripherals.display, big_bold_font, "Power", 30, st7789.CYAN)
    print_x_centered_text(peripherals.display, big_bold_font, "Pong",  56, st7789.CYAN)
    
    blink = False  # Estado inicial do texto piscante
    blink_period_ms = 750
    last_update = utime.ticks_ms() - blink_period_ms  # Marca o tempo inicial
    
    while peripherals.button_a.value() == 1:
        now = utime.ticks_ms()
        if utime.ticks_diff(now, last_update) >= blink_period_ms:
            last_update = now
            blink = not blink
            if blink:
                print_x_centered_text(peripherals.display, small_font, "Press A", 110, st7789.YELLOW)
                print_x_centered_text(peripherals.display, small_font, "to start", 120, st7789.YELLOW)
            else:
                peripherals.display.fill_rect(30, 110, WIDTH-30*2, 20, st7789.BLACK)
        
        utime.sleep_ms(50)

    while peripherals.button_a.value() == 0:
        utime.sleep_ms(100)
    
    # Feedback sonoro
    beep_beep(peripherals.buzzer)
    
    game.state = CHOOSE_SETS


# -------------------- CHOOSE SETS --------------------

def choose_sets_routine(game, peripherals):
    
    changed = False
    changed_time_ms = 0
    selected = 0
    
    peripherals.display.fill(st7789.BLACK)

    print_x_centered_text(peripherals.display, big_font, "Number",  5, st7789.WHITE)
    print_x_centered_text(peripherals.display, big_font, "of Sets", 31, st7789.WHITE)

    instruction_text = False
    instruction_text_period_ms = 2500
    instruction_text_last_update = utime.ticks_ms() - instruction_text_period_ms  # Marca o tempo inicial

    text1_line1 = "Press A"
    text1_line2 = "to confirm"

    text2_line1 = "Up/down joystick"
    text2_line2 = "to select"

    # Desenha opções
    draw_options(peripherals.display, selected, 10)

    while True:
        game.player1.update_position()
        game.player2.update_position()

        # Mostra instrucao
        now = utime.ticks_ms()
        if utime.ticks_diff(now, instruction_text_last_update) >= instruction_text_period_ms:
            instruction_text_last_update = now
            instruction_text = not instruction_text

            peripherals.display.fill_rect(0, 130, WIDTH, 20, st7789.BLACK)
            if instruction_text:
                print_x_centered_text(peripherals.display, small_font, text1_line1, 130, st7789.YELLOW)
                print_x_centered_text(peripherals.display, small_font, text1_line2, 140, st7789.YELLOW)
            else:
                print_x_centered_text(peripherals.display, small_font, text2_line1, 130, st7789.YELLOW)
                print_x_centered_text(peripherals.display, small_font, text2_line2, 140, st7789.YELLOW)
            
        # Atualiza a seleção de acordo com a posição do joystick
        adc_value_y = peripherals.joystick_y.read_u16()
        y = (adc_value_y) / 2**15 - 1
        
        trigger = abs(y) > 0.7
        if not changed and trigger:
            selected -= int(signal(y))
            
            if selected < 0:
                selected = 0
                
                # error sound
                peripherals.buzzer.freq(330)
                peripherals.buzzer.duty_u16(2000)
            elif selected > len(n_sets_options) - 1:
                selected = len(n_sets_options) - 1
                
                # error sound
                peripherals.buzzer.freq(330)
                peripherals.buzzer.duty_u16(2000)
            else:
                # ok sound
                peripherals.buzzer.freq(440)
                peripherals.buzzer.duty_u16(2000)

            draw_options(peripherals.display, selected, 10)
                
            changed_time_ms = utime.ticks_ms()
            changed = True
        elif not trigger or utime.ticks_diff(now, changed_time_ms) > 500:
            changed = False
        
        if utime.ticks_diff(now, changed_time_ms) > 50:
            peripherals.buzzer.duty_u16(0)
        
        # Verifica confirmação da escolha
        if peripherals.button_a.value() == 0:
            beep_beep(peripherals.buzzer)
            break
        
        utime.sleep_ms(50)
    
    game.n_sets = n_sets_options[selected]
    game.score.reset(game.n_sets)
    game.ball.randomize_direction()
    
    game.state = GAME_BREAK

# -------------------- GAME RUNNING --------------------

def game_running_routine(game, peripherals):
    display.set_pen(st7789.BLACK)
    display.clear()
    
    # Atualiza o pad e a bola
    player1.update()
    player2.update()
    ball.update(player1, player2)

    # Desenha o pad e a bola
    player1.draw()
    player2.draw()
    ball.draw()
    
    # Atualiza o display
    display_draw_fbuf()
    
    utime.sleep(sampling_time)
    
    if ball.out():
        game_over = score.point(ball.out_side())
        player1.reset()
        player2.reset()
        ball.reset(game_over)
        
        if game_over:
            game.winner = score.get_game_winner()
            game.state = END
        else:
            game.state = GAME_BREAK
    else:
        game.state = GAME_RUNNING

# -------------------- GAME BREAK --------------------

def game_break_routine(game, peripherals):
    draw_oled_set_info(len(score.set_wins) + 1, game.n_sets)
    
    time_start_us = 0
    starting = False
    
    while True:
        display.set_pen(st7789.BLACK)
        display.clear()
        
        player1.update_position()
        player2.update_position()

        player1.draw()
        player2.draw()
        ball.draw()
        
        # Atualiza o display
        display_draw_fbuf()
        
        if not starting and player1.button_pressed() and player2.button_pressed():
            starting = True
            time_start_us = utime.ticks_us()
            buzzer.freq(440)
            buzzer.duty_u16(2000)
        
        if starting and utime.ticks_us() - time_start_us > 500000:
            buzzer.duty_u16(0)
            
        if starting and utime.ticks_us() - time_start_us > 1000000:
            break
        
        utime.sleep(sampling_time)
        
    game.state = GAME_RUNNING
    
# -------------------- END --------------------

def end_routine(game, peripherals):
    if game.winner == 1:
        pad = player1.pad
    elif game.winner == 2:
        pad = player2.pad
    
    animate_pad_to_center(pad, WIDTH // 2 - PAD_WEIGHT // 2, 170, 0.5)
    
    display.set_font("large_font")
    
    if game.winner == 1:
        display.set_pen(st7789.RED)
        text_width = display.measure_text("RED", 7)
        display.text("RED", (WIDTH - text_width) // 2, 10, 255, 7)
    elif game.winner == 2:
        display.set_pen(st7789.BLUE)
        text_width = display.measure_text("BLUE", 7)
        display.text("BLUE", (WIDTH - text_width) // 2, 10, 255, 7)
        
    display.set_pen(st7789.WHITE)
    text_width = display.measure_text("WINS!", 7)
    display.text("WINS!", (WIDTH - text_width) // 2, 60, 255, 7)
    display_draw_fbuf()
    
    # Música de vitoria do jogo
    end_song()
    
    player1.reset()
    player2.reset()
    
    score.reset()
    score.draw()
    
    # Limpa a tela
    display.set_pen(st7789.BLACK)
    display.clear()
    display_draw_fbuf()
        
    utime.sleep_ms(1000)
    
    game.state = MENU
