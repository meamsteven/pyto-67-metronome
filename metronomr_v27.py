import pyto_ui as ui
import sound
import os
import time
import threading

# Load audio files
six_path = os.path.join(os.path.expanduser('~'), 'Documents', '6.m4a')
seven_path = os.path.join(os.path.expanduser('~'), 'Documents', '7.m4a')

six_player_a = sound.AudioPlayer(six_path)
six_player_b = sound.AudioPlayer(six_path)
six_player_c = sound.AudioPlayer(six_path)
seven_player_a = sound.AudioPlayer(seven_path)
seven_player_b = sound.AudioPlayer(seven_path)
seven_player_c = sound.AudioPlayer(seven_path)

six_players = [six_player_a, six_player_b, six_player_c]
seven_players = [seven_player_a, seven_player_b, seven_player_c]

bpm = 67
running = False
metro_thread = None
reset_timing = False

def metronome_loop():
    global running, reset_timing
    toggle = True
    six_index = 0
    seven_index = 0
    next_beat = time.perf_counter()

    while running:
        global reset_timing
        if reset_timing:
            next_beat = time.perf_counter()
            reset_timing = False
        interval = 60 / bpm  # Recalculates on every beat
        if toggle:
            six_players[six_index].play()
            six_index = (six_index + 1) % 3
        else:
            seven_players[seven_index].play()
            seven_index = (seven_index + 1) % 3
        toggle = not toggle

        next_beat += interval
        while time.perf_counter() < next_beat:
            if not running or reset_timing:
                break
            time.sleep(0.05)

    for p in six_players + seven_players:
        p.stop()

def start_stop(sender):
    global running, metro_thread, bpm
    if not running:
        for p in six_players + seven_players:
            p.stop()
            p.current_time = 0
        running = True
        sender.title = '⏹ Stop'
        sender.background_color = ui.SystemColors.SYSTEM_GRAY
        metro_thread = threading.Thread(target=metronome_loop)
        metro_thread.start()
    else:
        running = False
        sender.title = '▶ Start'
        sender.background_color = ui.SystemColors.SYSTEM_GRAY

def increase_bpm(sender):
    global bpm, reset_timing
    bpm = min(500, bpm + 1)
    bpm_label.text = f'{bpm} BPM'
    if bpm <= 30:
        reset_timing = True

def decrease_bpm(sender):
    global bpm, reset_timing
    bpm = max(1, bpm - 1)
    bpm_label.text = f'{bpm} BPM'
    if bpm <= 30:
        reset_timing = True

def increase_bpm_10(sender):
    global bpm, reset_timing
    bpm = min(500, bpm + 10)
    bpm_label.text = f'{bpm} BPM'
    if bpm <= 30:
        reset_timing = True

def decrease_bpm_10(sender):
    global bpm, reset_timing
    bpm = max(1, bpm - 10)
    bpm_label.text = f'{bpm} BPM'
    if bpm <= 30:
        reset_timing = True

def set_bpm(sender):
    global bpm, reset_timing
    try:
        new_bpm = int(bpm_input.text)
        if 1 <= new_bpm <= 500:
            bpm = new_bpm
            bpm_label.text = f'{bpm} BPM'
            if bpm <= 30:
                reset_timing = True
        else:
            bpm_input.text = ''
    except:
        bpm_input.text = ''

# Build the UI
view = ui.View()
view.background_color = ui.SystemColors.SYSTEM_BACKGROUND
view.width = 430
view.height = 932

# Title
title = ui.Label()
title.text = '6 / 7 Metronome'
title.font = ui.Font.bold_system_font_of_size(32)
title.frame = (0, 80, 430, 60)
title.text_alignment = ui.TextAlignment.CENTER
view.add_subview(title)

# BPM display
bpm_label = ui.Label()
bpm_label.text = f'{bpm} BPM'
bpm_label.font = ui.Font.bold_system_font_of_size(80)
bpm_label.frame = (0, 180, 430, 100)
bpm_label.text_alignment = ui.TextAlignment.CENTER
view.add_subview(bpm_label)

# BPM text input
bpm_input = ui.TextField()
bpm_input.placeholder = 'Type BPM...'
bpm_input.frame = (10, 295, 300, 50)
bpm_input.keyboard_type = ui.KeyboardType.NUMBER_PAD
bpm_input.border_style = ui.TextFieldBorderStyle.ROUNDED_RECT
bpm_input.action = set_bpm
view.add_subview(bpm_input)

# Set BPM button
btn_set = ui.Button()
btn_set.title = 'Set'
btn_set.font = ui.Font.bold_system_font_of_size(22)
btn_set.frame = (320, 295, 100, 50)
btn_set.background_color = ui.SystemColors.SYSTEM_GRAY
btn_set.title_color = ui.SystemColors.SYSTEM_BACKGROUND
btn_set.corner_radius = 12
btn_set.action = set_bpm
view.add_subview(btn_set)

# -10 button
btn_minus10 = ui.Button()
btn_minus10.title = '-10'
btn_minus10.font = ui.Font.bold_system_font_of_size(28)
btn_minus10.frame = (10, 360, 200, 100)
btn_minus10.background_color = ui.SystemColors.SYSTEM_GRAY
btn_minus10.title_color = ui.SystemColors.SYSTEM_BACKGROUND
btn_minus10.corner_radius = 16
btn_minus10.action = decrease_bpm_10
view.add_subview(btn_minus10)

# +10 button
btn_plus10 = ui.Button()
btn_plus10.title = '+10'
btn_plus10.font = ui.Font.bold_system_font_of_size(28)
btn_plus10.frame = (220, 360, 200, 100)
btn_plus10.background_color = ui.SystemColors.SYSTEM_GRAY
btn_plus10.title_color = ui.SystemColors.SYSTEM_BACKGROUND
btn_plus10.corner_radius = 16
btn_plus10.action = increase_bpm_10
view.add_subview(btn_plus10)

# -1 button
btn_minus = ui.Button()
btn_minus.title = '-1'
btn_minus.font = ui.Font.bold_system_font_of_size(28)
btn_minus.frame = (10, 475, 200, 100)
btn_minus.background_color = ui.SystemColors.SYSTEM_GRAY
btn_minus.title_color = ui.SystemColors.SYSTEM_BACKGROUND
btn_minus.corner_radius = 16
btn_minus.action = decrease_bpm
view.add_subview(btn_minus)

# +1 button
btn_plus = ui.Button()
btn_plus.title = '+1'
btn_plus.font = ui.Font.bold_system_font_of_size(28)
btn_plus.frame = (220, 475, 200, 100)
btn_plus.background_color = ui.SystemColors.SYSTEM_GRAY
btn_plus.title_color = ui.SystemColors.SYSTEM_BACKGROUND
btn_plus.corner_radius = 16
btn_plus.action = increase_bpm
view.add_subview(btn_plus)

# Start/Stop button
btn_start = ui.Button()
btn_start.title = '▶ Start'
btn_start.font = ui.Font.bold_system_font_of_size(36)
btn_start.frame = (10, 620, 410, 120)
btn_start.background_color = ui.SystemColors.SYSTEM_GRAY
btn_start.title_color = ui.SystemColors.SYSTEM_BACKGROUND
btn_start.corner_radius = 20
btn_start.action = start_stop
view.add_subview(btn_start)

ui.show_view(view, ui.PresentationMode.SHEET)
