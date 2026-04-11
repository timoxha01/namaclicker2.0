import assets_loading
import random
import vars
import pygame


def load_mode(mode):
    vars.isLoading = True
    vars.next_mode = mode
    vars.cooldown_timer.reset()

def draw_wrapped_text(surface, text, font, color, x, y, max_width, line_height):
    words = text.split()
    if not words:
        return y

    line = words[0]
    lines = []

    for word in words[1:]:
        candidate = f"{line} {word}"
        if font.size(candidate)[0] <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    lines.append(line)

    for row in lines:
        surface.blit(font.render(row, True, color), (x, y))
        y += line_height
    return y

def ShowNofitication(sc):
    if not vars.notif_visible:
        return
    if vars.notif_timer.done():
        vars.notif_visible = False
        return
    sc.blit(assets_loading.exc_mark, (144, 196))

def TriggerNotification():
    vars.notif_visible = True
    vars.notif_timer.reset()

def draw_button_text(screen, text, font, color, button, offset):
    text_surface = font.render(text, True, color)
    scale = button.scale
    if scale != 1.0:
        w = max(1, int(text_surface.get_width() * scale))
        h = max(1, int(text_surface.get_height() * scale))
        text_surface = pygame.transform.smoothscale(text_surface, (w, h))
    x = button.rect.x + int(offset[0] * scale)
    y = button.rect.y + int(offset[1] * scale)
    screen.blit(text_surface, (x, y))

def add_clicks():
    vars.total_clicks = int(vars.total_clicks)
    boost_bonus = vars.buffm.get_boost_bonus() if vars.buffm else 0
    vars.total_clicks += 1 * (vars.boost + boost_bonus)
    vars.show_boost = True
    vars.clicking_text_timer.reset()
    vars.tama_on_screen = choose_tama(vars.tamas)
    vars.tama_on_screen.pulse()
    assets_loading.click_sound.play()
    # Достижение: Собрать все виды tamas
    vars.seen_tamas.add(vars.tama_on_screen.name)
    if len(vars.seen_tamas) == len(vars.tamas):
        vars.cfa_collect_all_tamas.unlocked = True
        vars.cfa_collect_all_tamas.show_popup = True
        vars.cfa_collect_all_tamas.timer.reset()
    vars.boost_pos = (
        random.randint(0, vars.W - 50),
        random.randint(0, vars.H - 50),
    )

def choose_tama(tamas):
    total_chance = sum(t.chance for t in tamas)
    roll = random.uniform(0, total_chance)

    current = 0
    for tama in tamas:
        current += tama.chance
        if roll <= current:
            return tama
    return tamas[0]

def update_volume():
    for sound in [
        assets_loading.click_sound,
        assets_loading.mouse_click_sound,
        assets_loading.glitch_sound,
        assets_loading.sanic_sound,
        vars.cfa_collect_all_tamas.achievement_sound,
        vars.cfa_sanic_popout.achievement_sound,
        vars.cfa_IT.achievement_sound,
        vars.cfa_1000_clicks.achievement_sound,
        vars.cfa_10000_clicks.achievement_sound,
        vars.cfa_1000000_clicks.achievement_sound,
        assets_loading.volume_changing_sound,
        assets_loading.byebye_nama_sound,
    ]:
        sound.set_volume(vars.VOLUME)

def play_next_soundtrack():
    track = get_next_track()
    pygame.mixer.music.load(track)
    pygame.mixer.music.set_volume(vars.VOLUME_SDTRACK)
    pygame.mixer.music.play()

    filename = track.split("/")[-1]
    if filename in vars.song_popouts:
        vars.song_popouts[filename].show()

def get_next_track():
    if not vars.music_loop:
        vars.music_loop = vars.SOUNDTRACKS.copy()
        random.shuffle(vars.music_loop)
    return vars.music_loop.pop()