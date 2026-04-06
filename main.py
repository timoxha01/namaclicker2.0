import random
import math
import pygame
import os
import datasave
from collections import OrderedDict


class CachedFont:
    def __init__(self, font, max_cache=512):
        self._font = font
        self._cache = OrderedDict()
        self._max_cache = max_cache

    def render(self, text, antialias, color):
        key = (text, antialias, color)
        cached = self._cache.get(key)
        if cached is not None:
            self._cache.move_to_end(key)
            return cached
        surface = self._font.render(text, antialias, color)
        self._cache[key] = surface
        if len(self._cache) > self._max_cache:
            self._cache.popitem(last=False)
        return surface

    def size(self, text):
        return self._font.size(text)

    def __getattr__(self, name):
        return getattr(self._font, name)

pygame.init()
pygame.mixer.init()

print("Loading...")

W, H = 1000, 800
FPS = 60
mode = "menu"

GAME_FONT = "assets/fonts/Tiny5-Regular.ttf"

VOLUME = 0.5
VOLUME_SDTRACK = 0.5
VOLUME_STEP = 0.05
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SOUNDTRACKS = [
    "assets/sounds/osts/GoldStandard_ost.mp3",
    "assets/sounds/osts/Stardust_ost.mp3",
    "assets/sounds/osts/Syntax_CNS_ost.mp3",
    "assets/sounds/osts/TheDivide_ost.mp3",
    "assets/sounds/osts/TheWorldsGreatestGameShow2_ost.mp3",
    "assets/sounds/osts/IntoTheUnknown_ost.mp3",
    "assets/sounds/osts/TheNextStage_ost.mp3",
    "assets/sounds/osts/ElIndomable_ost.mp3"
]

MUSIC_END_EVENT = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

pygame.display.set_caption("NamaClicker 2.0")
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("assets/images/tamas/classic.png"))
font_40 = CachedFont(pygame.font.Font(GAME_FONT, 40))
font_30 = CachedFont(pygame.font.Font(GAME_FONT, 30))
font_25 = CachedFont(pygame.font.Font(GAME_FONT, 25))
font_20 = CachedFont(pygame.font.Font(GAME_FONT, 20))

_image_cache = {}
_sound_cache = {}


def draw_loading_screen(message):
    screen.fill((18, 18, 18))
    title = font_30.render("NamaClicker 2.0", True, (230, 230, 230))
    text = font_30.render(message, True, (180, 180, 180))
    screen.blit(title, (W // 2 - title.get_width() // 2, H // 2 - 36))
    screen.blit(text, (W // 2 - text.get_width() // 2, H // 2 + 8))
    pygame.display.flip()
    pygame.event.pump()


def load_image(path, *, alpha=True):
    key = (path, alpha)
    cached = _image_cache.get(key)
    if cached is not None:
        return cached
    image = pygame.image.load(path)
    image = image.convert_alpha() if alpha else image.convert()
    _image_cache[key] = image
    return image


def load_sound(path):
    cached = _sound_cache.get(path)
    if cached is not None:
        return cached
    sound = pygame.mixer.Sound(path)
    _sound_cache[path] = sound
    return sound


draw_loading_screen("Загрузка ассетов...")

credits_bg_ru = load_image("assets/images/UI/credits.png", alpha=False)
menu_screen = load_image("assets/images/UI/menu_screen.png", alpha=False)

settings_bg = load_image("assets/images/UI/settings_bg.png", alpha=False)

achievements_bg_ru = load_image("assets/images/UI/achievements.png", alpha=False)

volume_icon = load_image("assets/images/UI/volume_icon.png", alpha=True)

long_button_img = load_image("assets/images/UI/button_long.png", alpha=True)

NamaCoin_image = load_image("assets/images/UI/NamaCoin.png", alpha=True)
angle_frame = load_image("assets/images/UI/angle_frame.png", alpha=True)

field_bg = load_image("assets/images/UI/greenfield.png", alpha=False)

pickable_namacoin = NamaCoin_image

locked_button_gfield = load_image("assets/images/UI/locked_button_1000.png", alpha=True)

locked_exchange_button = locked_button_gfield

shelf_bg = load_image("assets/images/UI/shelf_bg.png", alpha=False)

shop_bg = load_image("assets/images/UI/shop_bg.png", alpha=False)

namapass_bg = load_image("assets/images/UI/namapass_bg.png", alpha=False)

tutorial_gfield = load_image("assets/images/UI/tutorial_gfield.png", alpha=False)

exc_mark = load_image("assets/images/UI/exc_mark.png", alpha=True)

exchanger_bg = load_image("assets/images/UI/exchanger_bg.png", alpha=False)

click_image = load_image("assets/images/UI/click_image.png", alpha=True)

beluash_preview = load_image("assets/images/UI/beluash_preview.png", alpha=True)
contestant_preview = load_image("assets/images/UI/contestant_preview.png", alpha=True)
tiger_fruit_preview = load_image("assets/images/UI/tiger_fruit_preview.png", alpha=True)
energy_drink_preview = load_image("assets/images/UI/energy_drink_preview.png", alpha=True)
minigun_preview = load_image("assets/images/UI/minigun_preview.png", alpha=True)
teddy_bear_preview = load_image("assets/images/UI/teddy_bear_preview.png", alpha=True)

namapass_banner_alfa_acta = load_image("assets/images/UI/namapass_banner_alfa_acta.png", alpha=True)
namapass_banner_ospuze = load_image("assets/images/UI/namapass_banner_ospuze.png", alpha=True)
namapass_banner_trentila = load_image("assets/images/UI/namapass_banner_trentila.png", alpha=True)
namapass_banner_vaiiya = load_image("assets/images/UI/namapass_banner_vaiiya.png", alpha=True)

buff_machine_image = load_image("assets/images/UI/buff_machine.png", alpha=True)

trentila_button_img = load_image("assets/images/UI/trentila_button.png", alpha=True)
vaiiya_button_img = load_image("assets/images/UI/vaiiya_button.png", alpha=True)
ospuze_button_img = load_image("assets/images/UI/ospuze_button.png", alpha=True)
alfa_acta_button_img = load_image("assets/images/UI/alfa_acta_button.png", alpha=True)

vaiiya_quote = load_image("assets/images/UI/vaiiya_info.png", alpha=True)
trentila_quote = load_image("assets/images/UI/trentila_info.png", alpha=True)
ospuze_quote = load_image("assets/images/UI/ospuze_info.png", alpha=True)
alfa_acta_quote = load_image("assets/images/UI/alfa_acta_info.png", alpha=True)

draw_loading_screen("Загрузка звуков...")
byebye_nama_sound = load_sound("assets/sounds/sfxes/namatama_byebye.mp3")
click_sound = load_sound("assets/sounds/sfxes/click_sound.mp3")
mouse_click_sound = load_sound("assets/sounds/sfxes/mouse_click.mp3")
glitch_sound = load_sound("assets/sounds/sfxes/screamer_glitch.mp3")
sanic_sound = load_sound("assets/sounds/sfxes/screamer_sanic.mp3")
volume_changing_sound = load_sound("assets/sounds/sfxes/volume_change_sound.mp3")
purchase_success = load_sound("assets/sounds/sfxes/purchase_success.mp3")
purchase_failed = load_sound("assets/sounds/sfxes/purchase_failed.mp3")
coins_collecting = load_sound("assets/sounds/sfxes/NamaCoins_collecting.mp3")
nofitication_sound = load_sound("assets/sounds/sfxes/announcement.mp3")
inserted_coin = load_sound("assets/sounds/sfxes/inserted_coin.mp3")
text_dialogue_sound = load_sound("assets/sounds/sfxes/text_dialogue.mp3")

class NamaPassbanner:
    def __init__(self):
        self.x = 20
        self.y = 210

        self.banners = [
            namapass_banner_alfa_acta,
            namapass_banner_ospuze,
            namapass_banner_trentila,
            namapass_banner_vaiiya
        ]

        self.index = 0
        self.current_image = self.banners[self.index]
        self.next_image = None

        self.alpha_current = 255
        self.alpha_next = 0

        self.fade_speed = 8
        self.is_fading = False

        self.change_delay = 3000
        self.timer = pygame.time.get_ticks()

        self.base_rect = self.current_image.get_rect(topleft=(self.x, self.y))
        self.rect = self.base_rect.copy()
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.15

    def update(self):
        if not self.is_fading:
            return

        self.alpha_current -= self.fade_speed
        self.alpha_next += self.fade_speed

        if self.alpha_current <= 0:
            self.alpha_current = 255
            self.alpha_next = 0

            self.index = (self.index + 1) % len(self.banners)
            self.current_image = self.banners[self.index]
            self.next_image = None

            self.is_fading = False
            self.timer = pygame.time.get_ticks()

    def change_banner(self):
        now = pygame.time.get_ticks()

        if not self.is_fading and now - self.timer >= self.change_delay:
            self.is_fading = True

            next_index = (self.index + 1) % len(self.banners)
            self.next_image = self.banners[next_index]

            self.alpha_current = 255
            self.alpha_next = 0

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.base_rect.collidepoint(mouse_pos):
            self.target_scale = 0.92
        else:
            self.target_scale = 1.0

        if self.scale != self.target_scale:
            self.scale += (self.target_scale - self.scale) * self.scale_speed
            if abs(self.scale - self.target_scale) < 0.01:
                self.scale = self.target_scale

        w = int(self.current_image.get_width() * self.scale)
        h = int(self.current_image.get_height() * self.scale)
        img = pygame.transform.smoothscale(self.current_image, (w, h))
        self.rect = img.get_rect(center=self.base_rect.center)
        screen.blit(img, self.rect)

        if self.is_fading and self.next_image:
            w = int(self.next_image.get_width() * self.scale)
            h = int(self.next_image.get_height() * self.scale)
            img_next = pygame.transform.smoothscale(self.next_image, (w, h))
            img_next.set_alpha(self.alpha_next)
            rect_next = img_next.get_rect(center=self.base_rect.center)
            screen.blit(img_next, rect_next)

class Namas:
    def __init__(self, name, path, chance):
        self.name = name
        self.base_pos = (W // 2, H // 2)
        self.pos = self.base_pos
        self.original_image = load_image(path, alpha=True)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.pos)
        self.chance = chance
        self.sway_time = 0.0
        self.sway_duration = 0.15
        self.sway_amplitude = 4

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def add_clicks(self, amount, boost):
        self.clicks += amount * boost

    def update(self):
        if self.sway_time > 0.0:
            self.sway_time -= 1.0 / FPS
            t = max(0.0, self.sway_time / self.sway_duration)
            offset = math.sin((1.0 - t) * math.pi * 4) * self.sway_amplitude * t
            self.pos = (self.base_pos[0] + offset, self.base_pos[1])
        else:
            self.pos = self.base_pos

        self.rect = self.image.get_rect(center=self.pos)

    def pulse(self):
        self.sway_time = self.sway_duration

class BuffMachine:
    EFFECTS = {
        "buff1": ("x1.1 кликов каждые 10 секунд на протяжении минуты!", "buff", 60000, 10000, 1.1, "clicks"),
        "buff2": ("Буст увеличивается на 2 на 10 секунд!", "buff", 10000, 0, 2, "boost_bonus"),
        "buff3": ("x3 NamaCoins на ферме!", "buff", 60000, 0, 3, "farm_coins"),
        "debuff1": ("-10 кликов каждые 3 секунды на протяжении 30 секунд!", "debuff", 30000, 3000, -10, "clicks"),
        "debuff2": ("В NamaPass к текущему оставшемуся времени добавляется 30 секунд!", "debuff", 0, 0, 30000, "namapass_delay"),
        "debuff3": ("NamaCoins делятся на 2", "debuff", 0, 0, 0, "halve_coins"),
    }
    EFFECT_KEYS = tuple(EFFECTS.keys())

    def __init__(self) -> None:
        self.shuffle_result = None
        self.last_result_text = None
        self.last_effect_kind = None
        self.active_effect_id = None
        self.active_effect_timer = None
        self.active_effect_tick_timer = None
        self.active_effect_tick_value = 0

    def shuffle(self):
        self.active_effect_id = random.choice(self.EFFECT_KEYS)
        text, etype, duration_ms, tick_ms, tick_val, _ = self.EFFECTS[self.active_effect_id]
        self.shuffle_result = text
        self.last_result_text = text
        self.last_effect_kind = etype

        if duration_ms > 0:
            self.active_effect_timer = Timer(duration_ms)
        else:
            self.active_effect_timer = None

        if tick_ms > 0:
            self.active_effect_tick_timer = Timer(tick_ms)
            self.active_effect_tick_value = tick_val
        else:
            self.active_effect_tick_timer = None
            self.active_effect_tick_value = tick_val

        return self.shuffle_result

    def apply_instant_effects(self, ctx):
        if self.active_effect_id is None:
            return
        _, _, duration_ms, _, tick_val, effect_type = self.EFFECTS[self.active_effect_id]
        if duration_ms == 0:
            if effect_type == "namapass_delay":
                for name in ["namapass_5min_timer", "namapass_10min_timer", "namapass_15min_timer",
                            "namapass_20min_timer", "namapass_25min_timer", "namapass_30min_timer"]:
                    t = ctx.get(name)
                    if t is not None and hasattr(t, "duration"):
                        t.duration += tick_val
            elif effect_type == "halve_coins":
                ctx["NamaCoins"] = max(0, ctx["NamaCoins"] // 2)
            self.active_effect_id = None

    def update_timed_effects(self, ctx):
        if self.active_effect_id is None or self.active_effect_timer is None:
            return
        if self.active_effect_timer.done():
            self.active_effect_id = None
            self.active_effect_timer = None
            self.active_effect_tick_timer = None
            self.active_effect_tick_value = 0
            return

        _, _, _, _, _, effect_type = self.EFFECTS[self.active_effect_id]
        if self.active_effect_tick_timer is not None and self.active_effect_tick_timer.done():
            self.active_effect_tick_timer.reset()
            if effect_type == "clicks":
                ctx["total_clicks"] = max(0, round(float(ctx["total_clicks"]) + self.active_effect_tick_value))
            elif effect_type == "boost_bonus":
                pass

    def get_boost_bonus(self):
        if self.active_effect_id is None:
            return 0
        _, _, _, _, _, effect_type = self.EFFECTS[self.active_effect_id]
        if effect_type == "boost_bonus":
            return self.active_effect_tick_value
        return 0

    def get_farm_coin_multiplier(self):
        if self.active_effect_id is None:
            return 1
        _, _, _, _, _, effect_type = self.EFFECTS[self.active_effect_id]
        if effect_type == "farm_coins":
            mult = int(self.active_effect_tick_value)
            return max(1, mult)
        return 1

class CharacterDialogues:
    def __init__(self, name, phrases, image_path, dialogueWindow_path, image_path_x, image_path_y, button_x, button_y) -> None:
        self.name = name
        self.phrases = phrases
        self.image_path = load_image(image_path, alpha=True)
        self.image_path_x = int(image_path_x)
        self.image_path_y = int(image_path_y)
        self.rect = self.image_path.get_rect()
        self.dialogueWindow = load_image(dialogueWindow_path, alpha=True)
        self.isTriggered = False
        self.dialogueText = ""
        self.visible_chars = 0
        self.char_delay_ms = 35
        self.last_char_tick = pygame.time.get_ticks()
        self.dialogue_sound_delay_ms = 70
        self.last_dialogue_sound_tick = 0
        self.isEntered = False
        self.eButton_image = load_image("assets/images/UI/eButton.png")
        self.button_x = button_x
        self.button_y = button_y

    def shufflePhrases(self):
        self.dialogueText = random.choice(self.phrases)
        self.visible_chars = 0
        self.last_char_tick = pygame.time.get_ticks()

    def update_typing_effect(self):
        if not self.isTriggered:
            return
        if self.visible_chars >= len(self.dialogueText):
            return

        now = pygame.time.get_ticks()
        elapsed = now - self.last_char_tick
        if elapsed < self.char_delay_ms:
            return

        chars_to_add = max(1, elapsed // self.char_delay_ms)
        self.visible_chars = min(len(self.dialogueText), self.visible_chars + chars_to_add)
        self.last_char_tick += chars_to_add * self.char_delay_ms
        if now - self.last_dialogue_sound_tick >= self.dialogue_sound_delay_ms:
            text_dialogue_sound.play()
            self.last_dialogue_sound_tick = now

    def drawDialogueWindow(self, screen):
        if self.isTriggered:
            self.update_typing_effect()
            screen.blit(self.dialogueWindow, (0, 662))
            screen.blit(font_30.render(self.name, True, BLACK), (43, 662))
            typed_text = self.dialogueText[:self.visible_chars]
            screen.blit(font_30.render(typed_text, True, BLACK), (30, 750))

    def draw(self, screen):
        self.rect.topleft = (self.image_path_x, self.image_path_y)
        screen.blit(self.image_path, (self.image_path_x, self.image_path_y))

    def draw_button(self, screen):
        screen.blit(self.eButton_image, (self.button_x, self.button_y))

    def activate(self):
        self.shufflePhrases()
        self.isTriggered = True

class Background:
    def __init__(self, bg_path, price, buy_button_path, x_button, y_button) -> None:
        self.bg_image = load_image(bg_path, alpha=False)
        self.price = price
        self.isBought = False
        self.equipped = False
        self.x_button = x_button
        self.y_button = y_button
        self.original_button_image = load_image(buy_button_path, alpha=True)
        self.buy_button_image = self.original_button_image
        self.button_base_rect = self.original_button_image.get_rect(topleft=(x_button, y_button))
        self.button_rect = self.button_base_rect.copy()
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.15

    def draw_button(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_base_rect.collidepoint(mouse_pos):
            self.target_scale = 0.92
        else:
            self.target_scale = 1.0

        if self.scale != self.target_scale:
            self.scale += (self.target_scale - self.scale) * self.scale_speed
            if abs(self.scale - self.target_scale) < 0.01:
                self.scale = self.target_scale
            size = (
                int(self.original_button_image.get_width() * self.scale),
                int(self.original_button_image.get_height() * self.scale),
            )
            self.buy_button_image = pygame.transform.smoothscale(self.original_button_image, size)
            self.button_rect = self.buy_button_image.get_rect(center=self.button_base_rect.center)

        screen.blit(self.buy_button_image, self.button_rect)

    def buy(self):
        global NamaCoins
        if NamaCoins >= self.price:
            if not self.isBought:
                purchase_success.play()
                self.isBought = True
                NamaCoins -= self.price
        else:
            purchase_failed.play()

    def equip(self):
        if self.isBought:
            self.equipped = True
            volume_changing_sound.play()


class NamaPlayer():
    def __init__(self):
        self.x = 25
        self.y = 523
        self.original_image = load_image("assets/images/tamas/classic.png", alpha=True)
        self.image = pygame.transform.scale(self.original_image, (144, 144))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
    def draw(self, screen):
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, self.rect)

namaPlayer = NamaPlayer()

class ShopItems():
    def __init__(self, image_path, price, x, y) -> None:
        self.price = price
        self.image = load_image(image_path, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.isBought = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def buy(self): 
        global NamaCoins        
        if NamaCoins >= self.price:
            self.isBought = True
            NamaCoins -= self.price
            purchase_success.play()
        else:
            purchase_failed.play()

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start = pygame.time.get_ticks()

    def done(self):
        return pygame.time.get_ticks() - self.start >= self.duration

    def reset(self):
        self.start = pygame.time.get_ticks()
    
    def time_left(self):
        return max(0, self.duration - (pygame.time.get_ticks() - self.start))

    def time_format(self):
        total_sec = self.time_left() // 1000
        minutes = total_sec // 60
        seconds = total_sec % 60
        return f"{minutes:02d}:{seconds:02d}"


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

class NamaPassItemsCollect:
    BUTTON_IMAGE = None
    COLLECTED_IMAGE = None

    def __init__(self, button_x, button_y):
        self.button_x = button_x
        self.button_y = button_y
        if NamaPassItemsCollect.BUTTON_IMAGE is None:
            NamaPassItemsCollect.BUTTON_IMAGE = load_image("assets/images/UI/collect_button.png", alpha=True)
        if NamaPassItemsCollect.COLLECTED_IMAGE is None:
            NamaPassItemsCollect.COLLECTED_IMAGE = load_image("assets/images/UI/namapass_collected.png", alpha=True)
        self.button_image = NamaPassItemsCollect.BUTTON_IMAGE
        self.collected_item = NamaPassItemsCollect.COLLECTED_IMAGE
        self.rect = self.button_image.get_rect(topleft=(button_x, button_y))
        self.isCountdownDone = False
        self.isCollected = False
    
    def draw(self, screen):
        screen.blit(self.button_image, self.rect)
    
    def buy(self):
        global NamaCoins, coins_collecting, purchase_failed
        if (
            self.rect.collidepoint(event.pos)
            and mode == "NamaPass"
        ):
            if not self.isCollected and self.isCountdownDone:
                self.isCollected = True
                coins_collecting.play()


class SongsPopouts:
    def __init__(self, image_path, x=15, y=680):
        self.base_image = load_image(image_path, alpha=True)
        self.x = x
        self.y = y

        self.scale = 0.0
        self.target_scale = 1.0
        self.speed = 0.15

        self.visible = False
        self.hiding = False
        self.timer = Timer(4000)

    def show(self):
        self.scale = 0.0
        self.visible = True
        self.hiding = False
        self.timer.reset()

    def update(self):
        if not self.visible:
            return

        if not self.hiding and self.scale < self.target_scale:
            self.scale += self.speed
            if self.scale >= self.target_scale:
                self.scale = self.target_scale
                self.timer.reset()
            return

        if not self.hiding and self.timer.done():
            self.hiding = True

        if self.hiding:
            self.scale -= self.speed
            if self.scale <= 0:
                self.scale = 0
                self.visible = False
                self.hiding = False

    def draw(self, screen):
        if not self.visible or self.scale <= 0:
            return

        w = int(self.base_image.get_width() * self.scale)
        h = int(self.base_image.get_height() * self.scale)

        img = pygame.transform.smoothscale(self.base_image, (w, h))
        screen.blit(img, (self.x, self.y))

class Button:
    BASE_IMAGE = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        if Button.BASE_IMAGE is None:
            Button.BASE_IMAGE = load_image("assets/images/UI/button.png", alpha=True)
        self.original_image = Button.BASE_IMAGE
        self.image = self.original_image
        self.base_rect = self.original_image.get_rect(topleft=(self.x, self.y))
        self.rect = self.base_rect.copy()
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.15

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.base_rect.collidepoint(mouse_pos):
            self.target_scale = 0.92
        else:
            self.target_scale = 1.0

        if self.scale != self.target_scale:
            self.scale += (self.target_scale - self.scale) * self.scale_speed
            if abs(self.scale - self.target_scale) < 0.01:
                self.scale = self.target_scale
            size = (
                int(self.original_image.get_width() * self.scale),
                int(self.original_image.get_height() * self.scale),
            )
            self.image = pygame.transform.smoothscale(self.original_image, size)
            self.rect = self.image.get_rect(center=self.base_rect.center)

        screen.blit(self.image, self.rect)

class HoverImage:
    def __init__(self, image, center):
        self.original_image = image
        self.image = self.original_image
        self.base_rect = self.original_image.get_rect(center=center)
        self.rect = self.base_rect.copy()
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.15

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.base_rect.collidepoint(mouse_pos):
            self.target_scale = 0.92
        else:
            self.target_scale = 1.0

        if self.scale != self.target_scale:
            self.scale += (self.target_scale - self.scale) * self.scale_speed
            if abs(self.scale - self.target_scale) < 0.01:
                self.scale = self.target_scale
            size = (
                int(self.original_image.get_width() * self.scale),
                int(self.original_image.get_height() * self.scale),
            )
            self.image = pygame.transform.smoothscale(self.original_image, size)
            self.rect = self.image.get_rect(center=self.base_rect.center)

        screen.blit(self.image, self.rect)

def ShowNofitication(sc):
    global notif_visible, notif_timer, exc_mark
    if not notif_visible:
        return
    if notif_timer.done():
        notif_visible = False
        return
    sc.blit(exc_mark, (144, 196))

def TriggerNotification():
    global notif_visible, notif_timer
    notif_visible = True
    notif_timer.reset()

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

credits_back_button = HoverImage(
    long_button_img,
    (W // 2, H - 42.5)
)
achievements_back_button = HoverImage(
    long_button_img,
    (W // 2, H - 50)
)
settings_back_button = HoverImage(
    long_button_img,
    (W // 2, H - 50)
)

trentila_button = HoverImage(
    trentila_button_img,
    (303 + (186 // 2), 270)
)
ospuze_button = HoverImage(
    ospuze_button_img,
    (509 + (186 // 2), 270)
)
alfa_acta_button = HoverImage(
    alfa_acta_button_img,
    (303 + (186 // 2), 430)
)
vaiiya_button = HoverImage(
    vaiiya_button_img,
    (511 + (186 // 2), 430)
)

class Achievements:
    POP_OUT_LABEL = None
    HIDDEN_IMAGE = None
    ACHIEVEMENT_SOUND = None

    def __init__(self, pop_out_text, x, y):
        self.x_pop_out = 500 
        self.target_y = 30
        self.speed = 7
        self.pop_out_text = pop_out_text
        self.sound_played = False
        if Achievements.POP_OUT_LABEL is None:
            Achievements.POP_OUT_LABEL = load_image("assets/images/UI/pop_out_label.png", alpha=True)
        if Achievements.HIDDEN_IMAGE is None:
            Achievements.HIDDEN_IMAGE = load_image("assets/images/UI/hidden_achi.png", alpha=True)
        if Achievements.ACHIEVEMENT_SOUND is None:
            Achievements.ACHIEVEMENT_SOUND = load_sound("assets/sounds/sfxes/nofitication_sound.mp3")
        self.pop_out_label = Achievements.POP_OUT_LABEL
        self.pop_rect = self.pop_out_label.get_rect(
            midtop=(W // 2, - self.pop_out_label.get_height())
        )
        self.y_pop_out = self.pop_rect.y
        self.achievement_sound = Achievements.ACHIEVEMENT_SOUND
        self.image = Achievements.HIDDEN_IMAGE
        self.rect = self.image.get_rect(topleft=(x, y))
        self.unlocked = False
        self.show_popup = False
        self.timer = Timer(2000)
        self.hiding = False

    def draw(self, screen):
        if not self.unlocked:
            screen.blit(self.image, self.rect)

    def pop_out(self, screen):
        if not self.show_popup:
            return
        if not self.sound_played:
            self.achievement_sound.play()
            self.sound_played = True
        if self.pop_rect.y < self.target_y and not self.timer.done():
            self.pop_rect.y += self.speed
            if self.pop_rect.y >= self.target_y:
                self.pop_rect.y = self.target_y
                self.timer.reset()

        if self.timer.done():
            self.pop_rect.y -= self.speed
            if self.pop_rect.y <= -self.pop_rect.height:
                self.reset_popup()
                self.show_popup = False
                return
    
        screen.blit(self.pop_out_label, self.pop_rect)
        screen.blit(
            font_40.render("Новое достижение!", True, BLACK),
            (self.pop_rect.x + 40, self.pop_rect.y + 25),
        )
        screen.blit(
            font_30.render(self.pop_out_text, True, BLACK),
            (self.pop_rect.x + ((font_30.size(self.pop_out_text)[0] // 4) - 30),
             self.pop_rect.y + 70),
        )
    def reset_popup(self):
        self.y_pop_out = -137
        self.sound_played = False 
        self.timer.reset()

class Coin:
    def __init__(self):
        self.image = pickable_namacoin
        self.rect = self.image.get_rect(
            center=(
                random.randint(50, W - 50),
                random.randint(50, H - 50),
            )
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class BoostCoin(Coin):
    BOOST_COIN_IMAGE = None

    def __init__(self):
        super().__init__()
        if BoostCoin.BOOST_COIN_IMAGE is None:
            BoostCoin.BOOST_COIN_IMAGE = load_image("assets/images/UI/NamaCoin_boost.png", alpha=True)
        self.image = BoostCoin.BOOST_COIN_IMAGE
        self.rect = self.image.get_rect(
            center=(
                random.randint(50, W - 50),
                random.randint(50, H - 50),
            )
        )

class Course:
    def __init__(self) -> None:
        self.course_clicks = float(EXCHANGE_CLICKS_PER_NAMACOIN)
        self.course_coins = round(1.0 / EXCHANGE_CLICKS_PER_NAMACOIN, 6)

def add_clicks():
    global \
        tama_on_screen, \
        total_clicks, \
        show_boost, \
        clicking_text_timer, \
        seen_tamas, \
        boost_pos, \
        boost
    total_clicks = int(total_clicks)
    boost_bonus = buffm.get_boost_bonus() if buffm else 0
    total_clicks += 1 * (boost + boost_bonus)
    show_boost = True
    clicking_text_timer.reset()
    tama_on_screen = choose_tama(tamas)
    tama_on_screen.pulse()
    click_sound.play()
    # Достижение: Собрать все виды tamas
    seen_tamas.add(tama_on_screen.name)
    if len(seen_tamas) == len(tamas):
        cfa_collect_all_tamas.unlocked = True
        cfa_collect_all_tamas.show_popup = True
        cfa_collect_all_tamas.timer.reset()
    boost_pos = (
        random.randint(0, W - 50),
        random.randint(0, H - 50),
    )


def choose_tama(tamas):
    total_chance = sum(t.chance for t in tamas)
    roll = random.uniform(0, total_chance)

    current = 0
    for tama in tamas:
        current += tama.chance
        if roll <= current:
            return tama

def update_volume():
    for sound in [
        click_sound,
        mouse_click_sound,
        glitch_sound,
        sanic_sound,
        cfa_collect_all_tamas.achievement_sound,
        cfa_sanic_popout.achievement_sound,
        cfa_IT.achievement_sound,
        cfa_1000_clicks.achievement_sound,
        cfa_10000_clicks.achievement_sound,
        cfa_1000000_clicks.achievement_sound,
        volume_changing_sound,
        byebye_nama_sound,
        text_dialogue_sound,
        purchase_success,
        purchase_failed,
        coins_collecting,
        nofitication_sound,
        inserted_coin
    ]:
        sound.set_volume(VOLUME)

def play_next_soundtrack():
    track = get_next_track()
    pygame.mixer.music.load(track)
    pygame.mixer.music.set_volume(VOLUME_SDTRACK)
    pygame.mixer.music.play()

    filename = track.split("/")[-1]
    if filename in song_popouts:
        song_popouts[filename].show()

music_loop = []
def get_next_track():
    global music_loop
    if not music_loop:
        music_loop = SOUNDTRACKS.copy()
        random.shuffle(music_loop)
    return music_loop.pop()

def load_mode(mode):
    global isLoading, next_mode, cooldown_timer
    isLoading = True
    next_mode = mode
    cooldown_timer.reset()

draw_loading_screen("Инициализация мира...")
seoul_bg = Background("assets/images/UI/seoul_bg.png", 100, "assets/images/UI/seoul_buy_button.png", 408, 246)
kyoto_bg = Background("assets/images/UI/kyoto_bg.png", 250, "assets/images/UI/kyoto_bg_button.png", 408, 351)
bernal_bg = Background("assets/images/UI/bernal_bg.png", 400, "assets/images/UI/bernal_bg_button.png", 408, 456)

cfa_collect_all_tamas = Achievements("Собрать все NamaTama", 64, 80)
cfa_sanic_popout = Achievements("Встретить Sanic", 372, 80)
cfa_IT = Achievements("Встретить ...", 679, 80)
cfa_1000_clicks = Achievements("Набрать 1000 кликов", 65, 382)
cfa_10000_clicks = Achievements("Набрать 10000 кликов", 372, 382)
cfa_1000000_clicks = Achievements("Набрать 1000000 кликов", 679, 382)

teddy_bear = ShopItems("assets/images/shop_items/teddy_bear.png", 250, 98, 173)
beluash = ShopItems("assets/images/shop_items/beluash.png", 500, 410, 173)
contestant = ShopItems("assets/images/shop_items/contestant.png", 1000, 722, 173)
energy_drink = ShopItems("assets/images/shop_items/energy_drink.png", None, 410, 430)
tiger_fruit = ShopItems("assets/images/shop_items/tiger_fruit.png", None, 98, 430)
minigun = ShopItems("assets/images/shop_items/minigun.png", None, 722, 430)

song_popouts = {
    "GoldStandard_ost.mp3": SongsPopouts("assets/images/UI/GoldStandard_SongCard.png"),
    "Stardust_ost.mp3": SongsPopouts("assets/images/UI/Stardust_SongCard.png"),
    "Syntax_CNS_ost.mp3": SongsPopouts("assets/images/UI/SyntaxCNS_SongCard.png"),
    "TheDivide_ost.mp3": SongsPopouts("assets/images/UI/TheDivide_SongCard.png"),
    "TheWorldsGreatestGameShow2_ost.mp3": SongsPopouts("assets/images/UI/TheWorldsGreatestGameShow2_SongCard.png"),
    "IntoTheUnknown_ost.mp3": SongsPopouts("assets/images/UI/IntoTheUnknown_SongCard.png"),
    "TheNextStage_ost.mp3": SongsPopouts("assets/images/UI/TheNextStage_SongCard.png"),
    "ElIndomable_ost.mp3": SongsPopouts("assets/images/UI/ElIndomable_SongCard.png")
}

tamas = [
    Namas("classic", "assets/images/tamas/classic.png", 1.0),
    Namas("like", "assets/images/tamas/like.png", 0.7),
    Namas("search", "assets/images/tamas/search.png", 0.5),
    Namas("tea", "assets/images/tamas/tea.png", 0.3),
    Namas("bob", "assets/images/tamas/bob.png", 0.2),
    Namas("builder", "assets/images/tamas/builder.png", 0.1),
    Namas("birthday", "assets/images/tamas/birthday.png", 0.1),
    Namas("stone", "assets/images/tamas/stone.png", 0.1),
    Namas("gun", "assets/images/tamas/gun.png", 0.05),
    Namas("galaxy", "assets/images/tamas/galaxy.png", 0.05),
    Namas("vibe", "assets/images/tamas/vibe.png", 0.03),
    Namas("evil", "assets/images/tamas/evil.png", 0.01),
    Namas("demon", "assets/images/tamas/demon.png", 0.01),
    Namas("boykisser", "assets/images/tamas/boykisser.png", 0.01),
    Namas("sanic", "assets/images/tamas/sanic_ee.png", 0.001),
    Namas("glitch", "assets/images/tamas/glitch_ee.png", 0.001)
]

banner = NamaPassbanner()
button_to_menu_from_game = Button(20, 720)
button_to_game_from_menu = Button((W // 2) - (183 // 2), (H // 2) - (58 // 2))
button_to_credits_from_menu = Button(800, 720)
button_to_achievements_from_menu = Button((W // 2) - (183 // 2), (H // 2) + 40)
button_to_settings_from_menu = Button((W // 2) - (183 // 2), (H // 2) + 110)
button_boost = Button(20, 650)
button_to_minigame_from_game = Button(20, 580)
button_back_from_minigame = Button(20, 720)
button_to_shelf_from_game = Button(800, 720)
button_back_from_shelf = Button(20, 720)
button_to_shop_from_shelf = Button(800, 720)
button_back_from_shop = Button(20, 720)
back_button_from_preview = Button(20, 720)
button_back_from_battle_pass = Button(20, 720)
button_to_sponsors_from_NamaPass = Button(800, 720)
button_back_from_sponsors_choice = Button(20, 720)
button_back_from_sponsors_quotes = Button(20, 720)
button_to_backgrounds_shop = Button(800, 650)
button_back_from_backgrounds_shop = Button(20, 720)

sfx_button_plus = Button(527, 114)
sfx_button_minus = Button(289, 114)
sdtrack_button_plus = Button(527, 275)
sdtrack_button_minus = Button(289, 275)

button_got_it = Button(471 - (183 // 2) + 45, 730)

button_buy_bear = Button((W // 2) - (183 // 2), 550)
button_buy_beluash = Button((W // 2) - (183 // 2), 550)
button_buy_contestant = Button((W // 2) - (183 // 2), 550)

button_exchanging = Button(408, 60)
button_exchanging_back_to_shop = Button(408, 60)

button_exchange_to_coins = Button(500 - (183 // 2), 310)
button_exchange_to_clicks = Button(500 - (183 // 2), 470)

clicking_text_timer = Timer(200)
cooldown_timer = Timer(1)
coin_spawn_timer = Timer(2000)
coin_boost_timer = Timer(5000)

EXCHANGE_CLICKS_PER_NAMACOIN = 50

namapass_5min_timer = Timer(300000)
namapass_10min_timer = Timer(600000)
namapass_15min_timer = Timer(900000)
namapass_20min_timer = Timer(1200000)
namapass_25min_timer = Timer(1500000)
namapass_30min_timer = Timer(1800000)

namapass_100_coins = NamaPassItemsCollect(139, 461)
namapass_200_coins = NamaPassItemsCollect(433, 461)
namapass_500_coins = NamaPassItemsCollect(726, 458)
namapass_trentila_reward = NamaPassItemsCollect(726, 194)
namapass_ospuze_reward = NamaPassItemsCollect(434, 194)
namapass_minigun_reward = NamaPassItemsCollect(142, 193)

BUFF_MACHINE_X = W - buff_machine_image.get_width() - 12
BUFF_MACHINE_Y = 100
BUFF_MACHINE_TEXT_X = BUFF_MACHINE_X + 8
BUFF_MACHINE_TEXT_W = buff_machine_image.get_width() - 16

button_machine = Button(
    BUFF_MACHINE_X + (buff_machine_image.get_width() - 183) // 2,
    BUFF_MACHINE_Y + buff_machine_image.get_height() + 48
)
buffm = BuffMachine()
buffm_intermission_timer = Timer(120000)
show_buff_effect_end_notice = False
buff_effect_end_notice_timer = Timer(2000)

course = Course()

coins = []
MAX_COINS = 5
required_clicks_for_boost = 100
current_music_credits = None
isLoading = False
isReached1000clicks = False
isTutorialWatched = False
notif_visible = False
notif_timer = Timer(1500)
notif_5_shown = False
notif_10_shown = False
notif_15_shown = False
notif_20_shown = False
notif_25_shown = False
notif_30_shown = False
show_intro_game_text = True
seen_tamas = set()
tama_on_screen = tamas[0]

boost_coin = 1
coin_boost_active = False

total_clicks = 0
NamaCoins = 0
boost = 1

last_total_clicks_for_shake = 0
clicks_shake_timer = Timer(200)
last_nama_coins_for_shake = 0
nama_shake_timer = Timer(200)

show_boost = False
next_mode = ""

SAVE_PATH = os.path.join(os.path.dirname(__file__), "data.json")
save_system = datasave.SaveSystem(
    pygame=pygame,
    update_volume_cb=update_volume,
    save_path=SAVE_PATH,
    autosave_every_ms=3000,
    save_version=1,
)
draw_loading_screen("Загрузка сохранения...")
save_system.load(globals())
VALID_MODES = {
    "game", "menu", "credits", "achievements", "settings", "minigame", "shelf",
    "shop", "beluash_preview", "contestant_preview", "energy_drink_preview",
    "tiger_fruit_preview", "minigun_preview", "teddy_bear_preview", "NamaPass",
    "sponsors_choice", "trentila_quote", "ospuze_quote", "alfa_acta_quote",
    "vaiiya_quote", "tutorial_gfield", "exchanger", "backgrounds_shop"
}
if mode not in VALID_MODES:
    mode = "menu"
play_next_soundtrack()
print("Game Loaded, Booting up...")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_system.save(globals())
            pygame.mixer.music.stop()
            byebye_nama_sound.play()
            pygame.time.delay(int(byebye_nama_sound.get_length() * 1000))
            running = False
        if event.type == MUSIC_END_EVENT:
            play_next_soundtrack()

            # MouseButton действия:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_to_game_from_menu.rect.collidepoint(event.pos) and mode == "menu":
                load_mode("game")
            if button_to_menu_from_game.rect.collidepoint(event.pos) and mode == "game":
                load_mode("menu")
            if (
                button_to_credits_from_menu.rect.collidepoint(event.pos)
                and mode == "menu"
            ):
                load_mode("credits")
            if credits_back_button.rect.collidepoint(event.pos) and mode == "credits":
                load_mode("menu")
            if (
                button_to_achievements_from_menu.rect.collidepoint(event.pos)
                and mode == "menu"
            ):
                load_mode("achievements")
            if (
                achievements_back_button.rect.collidepoint(event.pos)
                and mode == "achievements"
            ):
                load_mode("menu")
            if (
                button_to_settings_from_menu.rect.collidepoint(event.pos)
                and mode == "menu"
            ):
                load_mode("settings")
            if (
                settings_back_button.rect.collidepoint(event.pos)
                and mode == "settings"
            ):
                load_mode("menu")
            if (
                sfx_button_plus.rect.collidepoint(event.pos)
                and mode == "settings"
            ):
                VOLUME = min(1.0, VOLUME + VOLUME_STEP)
                update_volume()
                volume_changing_sound.play()
            if (
                sfx_button_minus.rect.collidepoint(event.pos)
                and mode == "settings"
            ):
                VOLUME = max(0.0, VOLUME - VOLUME_STEP)
                update_volume()
                volume_changing_sound.play()
            if (
                sdtrack_button_plus.rect.collidepoint(event.pos)
                and mode == "settings"
            ):
                VOLUME_SDTRACK = min(1.0, VOLUME_SDTRACK + VOLUME_STEP)
                pygame.mixer.music.set_volume(VOLUME_SDTRACK)
                volume_changing_sound.play()
            if (
                sdtrack_button_minus.rect.collidepoint(event.pos)
                and mode == "settings"
            ):
                VOLUME_SDTRACK = max(0.0, VOLUME_SDTRACK - VOLUME_STEP)
                pygame.mixer.music.set_volume(VOLUME_SDTRACK)
                volume_changing_sound.play()
            if (
                button_to_minigame_from_game.rect.collidepoint(event.pos)
                and mode == "game"
            ):
                if total_clicks >= 1000 or isReached1000clicks:
                    isLoading = True
                    if isTutorialWatched:
                        next_mode = "minigame"
                    else:
                        next_mode = "tutorial_gfield"
                    cooldown_timer.reset()
            if (
                button_back_from_minigame.rect.collidepoint(event.pos)
                and mode == "minigame"
            ):
                load_mode("game")
            if (
                button_to_shelf_from_game.rect.collidepoint(event.pos)
                and mode == "game"
            ):
                load_mode("shelf")
            if (
                button_back_from_shelf.rect.collidepoint(event.pos)
                and mode == "shelf"
            ):
                load_mode("game")
            if (
                button_back_from_shop.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                load_mode("shelf")
            if (
                button_boost.rect.collidepoint(event.pos)
                and mode == "game"
            ):
                if total_clicks >= required_clicks_for_boost and boost < 50:
                    total_clicks -= required_clicks_for_boost
                    boost += 1
                    required_clicks_for_boost *= 1.5
                    purchase_success.play()
                else:
                    purchase_failed.play()
            if (
                button_to_shop_from_shelf.rect.collidepoint(event.pos)
                and mode == "shelf"
            ):
                load_mode("shop")
            if tama_on_screen.rect.collidepoint(event.pos) and mode == "game":
                add_clicks()
            if (
                button_back_from_shelf.rect.collidepoint(event.pos)
                and mode == "shelf"
            ):
                load_mode("game")
            if (
                banner.rect.collidepoint(event.pos)
                and mode == "game"
            ):
                load_mode("NamaPass")
            if (
                button_back_from_battle_pass.rect.collidepoint(event.pos)
                and mode == "NamaPass"
            ):
                load_mode("game")
            if (
                button_got_it.rect.collidepoint(event.pos)
                and mode == "tutorial_gfield"
            ):
                load_mode("minigame")
                isTutorialWatched = True

            if (
                button_exchanging.rect.collidepoint(event.pos)
                and mode == "shop"
                and isReached1000clicks
            ):
                load_mode("exchanger")

            if (
                button_exchanging_back_to_shop.rect.collidepoint(event.pos)
                and mode == "exchanger"
            ):
                load_mode("shop")

            # обменник
            if (
                button_exchange_to_coins.rect.collidepoint(event.pos)
                and mode == "exchanger"
            ):
                if total_clicks > 0:
                    gained_coins = int(total_clicks // EXCHANGE_CLICKS_PER_NAMACOIN)
                    if gained_coins > 0:
                        NamaCoins += gained_coins
                        total_clicks = int(total_clicks % EXCHANGE_CLICKS_PER_NAMACOIN)
                        coins_collecting.play()
                else:
                    purchase_failed.play()

            if (
                button_exchange_to_clicks.rect.collidepoint(event.pos)
                and mode == "exchanger"
            ):
                if NamaCoins > 0:
                    gained_clicks = int(NamaCoins * EXCHANGE_CLICKS_PER_NAMACOIN)
                    if gained_clicks > 0:
                        total_clicks += gained_clicks
                        NamaCoins = 0
                        coins_collecting.play()
                else:
                    purchase_failed.play()
       

            #namapass
            if (
                namapass_100_coins.rect.collidepoint(event.pos)
                and mode == "NamaPass"
                and namapass_100_coins.isCountdownDone
            ):
                if not namapass_100_coins.isCollected:
                    namapass_100_coins.buy()
                    NamaCoins += 100
            if (
                namapass_200_coins.rect.collidepoint(event.pos)
                and mode == "NamaPass"
                and namapass_200_coins.isCountdownDone
            ):
                if not namapass_200_coins.isCollected:
                    namapass_200_coins.buy()
                    NamaCoins += 200
            if (
                namapass_500_coins.rect.collidepoint(event.pos)
                and mode == "NamaPass"
                and namapass_500_coins.isCountdownDone
            ):
                if not namapass_500_coins.isCollected:
                    namapass_500_coins.buy()
                    NamaCoins += 500
            if (
                namapass_trentila_reward.rect.collidepoint(event.pos)
                and mode == "NamaPass"
                and namapass_trentila_reward.isCountdownDone
            ):
                if not namapass_trentila_reward.isCollected:
                    namapass_trentila_reward.buy()
                    tiger_fruit.isBought = True
            if (
                namapass_ospuze_reward.rect.collidepoint(event.pos)
                and mode == "NamaPass"
                and namapass_ospuze_reward.isCountdownDone
            ):
                if not namapass_ospuze_reward.isCollected:
                    namapass_ospuze_reward.buy()
                    energy_drink.isBought = True
            if (
                namapass_minigun_reward.rect.collidepoint(event.pos)
                and mode == "NamaPass"
                and namapass_minigun_reward.isCountdownDone
            ):
                if not namapass_minigun_reward.isCollected:
                    namapass_minigun_reward.buy()
                    minigun.isBought = True

            #покупка
            if (
                button_buy_bear.rect.collidepoint(event.pos)
                and mode == "teddy_bear_preview"
                and not teddy_bear.isBought
            ):
                teddy_bear.buy()

            if (
                button_buy_beluash.rect.collidepoint(event.pos)
                and mode == "beluash_preview"
                and not beluash.isBought
            ):
                beluash.buy()

            if (
                button_buy_contestant.rect.collidepoint(event.pos)
                and mode == "contestant_preview"
                and not contestant.isBought
            ):
                contestant.buy()

            # магазин - isPreview
            if (
                teddy_bear.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                load_mode("teddy_bear_preview")
            if (
                beluash.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                load_mode("beluash_preview")
            if (
                energy_drink.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                load_mode("energy_drink_preview")
            if (
                tiger_fruit.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                load_mode("tiger_fruit_preview")
            if (
                minigun.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                load_mode("minigun_preview")
            if (
                contestant.rect.collidepoint(event.pos)
                and mode == "shop" 
            ):
                load_mode("contestant_preview")
            if (
                button_to_sponsors_from_NamaPass.rect.collidepoint(event.pos)
                and mode == "NamaPass"
            ):
                load_mode("sponsors_choice")
            if (
                button_back_from_sponsors_choice.rect.collidepoint(event.pos)
                and mode == "sponsors_choice"
            ):
                load_mode("NamaPass")
            if (
                trentila_button.rect.collidepoint(event.pos)
                and mode == "sponsors_choice"
            ):
                load_mode("trentila_sponsor_quote")
            if (
                ospuze_button.rect.collidepoint(event.pos)
                and mode == "sponsors_choice"
            ):
                load_mode("ospuze_sponsor_quote")
            if (
                alfa_acta_button.rect.collidepoint(event.pos)
                and mode == "sponsors_choice"
            ):
                load_mode("alfa_acta_sponsor_quote")
            if (
                vaiiya_button.rect.collidepoint(event.pos)
                and mode == "sponsors_choice"
            ):
                load_mode("vaiiya_sponsor_quote")
            

            if (
                back_button_from_preview.rect.collidepoint(event.pos)
                and mode in ["teddy_bear_preview", "beluash_preview", 
                        "energy_drink_preview", "tiger_fruit_preview",
                            "minigun_preview", "contestant_preview"]
                ):
                load_mode("shop")

            if (
                button_back_from_sponsors_quotes.rect.collidepoint(event.pos)
                and mode in ["ospuze_sponsor_quote", "trentila_sponsor_quote", 
                        "alfa_acta_sponsor_quote", "vaiiya_sponsor_quote"]
                ):
                load_mode("sponsors_choice")
            
            if (
                button_back_from_backgrounds_shop.rect.collidepoint(event.pos)
                and mode == "backgrounds_shop"
            ):
                load_mode("game")

            #buff machine
            if (
                button_machine.rect.collidepoint(event.pos)
                and mode == "game"
            ):
                if buffm_intermission_timer.done():
                    buffm.shuffle()
                    buffm.apply_instant_effects(globals())
                    buffm_intermission_timer.reset()
                    inserted_coin.play()
            #ФОНЫ
            if (
                button_to_backgrounds_shop.rect.collidepoint(event.pos)
                and mode == "game"
            ):
                load_mode("backgrounds_shop")
            
            if (seoul_bg.button_rect.collidepoint(event.pos) and mode == "backgrounds_shop"):
                if not seoul_bg.isBought:
                    seoul_bg.buy()
                else:
                    bernal_bg.equipped = False
                    kyoto_bg.equipped = False
                    seoul_bg.equip()

            if (kyoto_bg.button_rect.collidepoint(event.pos) and mode == "backgrounds_shop"):
                if not kyoto_bg.isBought:
                    kyoto_bg.buy()
                else:
                    bernal_bg.equipped = False
                    seoul_bg.equipped = False
                    kyoto_bg.equip()
                
            if (bernal_bg.button_rect.collidepoint(event.pos) and mode == "backgrounds_shop"):
                if not bernal_bg.isBought:
                    bernal_bg.buy()
                else:
                    seoul_bg.equipped = False
                    kyoto_bg.equipped = False
                    bernal_bg.equip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a] and mode == "minigame":
        namaPlayer.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d] and mode == "minigame":
        namaPlayer.x += 5
    if keys[pygame.K_UP] or keys[pygame.K_w] and mode == "minigame":
        namaPlayer.y -= 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s] and mode == "minigame":
        namaPlayer.y += 5

    namaPlayer.x = max(0, min(1000 - namaPlayer.rect.width, namaPlayer.x))
    namaPlayer.y = max(0, min(800 - namaPlayer.rect.height, namaPlayer.y))

    if namapass_5min_timer.done() and not notif_5_shown:
        notif_5_shown = True
        nofitication_sound.play()
        TriggerNotification()
    if namapass_10min_timer.done() and not notif_10_shown:
        notif_10_shown = True
        nofitication_sound.play()
        TriggerNotification()
    if namapass_15min_timer.done() and not notif_15_shown:
        notif_15_shown = True
        nofitication_sound.play()
        TriggerNotification()
    if namapass_20min_timer.done() and not notif_20_shown:
        notif_20_shown = True
        nofitication_sound.play()
        TriggerNotification()
    if namapass_25min_timer.done() and not notif_25_shown:
        notif_25_shown = True
        nofitication_sound.play()
        TriggerNotification()
    if namapass_30min_timer.done() and not notif_30_shown:
        notif_30_shown = True
        nofitication_sound.play()
        TriggerNotification()

    had_active_timed_effect = (
        buffm.active_effect_id is not None and buffm.active_effect_timer is not None
    )
    buffm.update_timed_effects(globals())
    if had_active_timed_effect and buffm.active_effect_id is None:
        show_buff_effect_end_notice = True
        buff_effect_end_notice_timer.reset()
    if show_buff_effect_end_notice and buff_effect_end_notice_timer.done():
        show_buff_effect_end_notice = False

    # DRAW MODE
    if mode == "game":
        screen.fill(GREY)

        if seoul_bg.equipped:
            screen.blit(seoul_bg.bg_image, (0, 0))
        if kyoto_bg.equipped:
            screen.blit(kyoto_bg.bg_image, (0, 0))
        if bernal_bg.equipped:
            screen.blit(bernal_bg.bg_image, (0, 0))

        button_boost.draw(screen)

        button_to_shelf_from_game.draw(screen)

        button_to_backgrounds_shop.draw(screen)
        screen.blit(
            font_30.render("Фоны", True, BLACK),
            (button_to_backgrounds_shop.x + 52.5, button_to_backgrounds_shop.y + 12)
        )

        banner.change_banner()
        banner.update()
        banner.draw(screen)

        ShowNofitication(screen)
        
        #Buff Machine:
        screen.blit(buff_machine_image, (BUFF_MACHINE_X, BUFF_MACHINE_Y))

        if buffm_intermission_timer.done():
            machine_timer_text = "Таймер: готово"
        else:
            machine_timer_text = f"Таймер: {buffm_intermission_timer.time_format()}"
        screen.blit(
            font_25.render(machine_timer_text, True, WHITE),
            (button_machine.x + 15, BUFF_MACHINE_Y + buff_machine_image.get_height() + 8)
        )

        button_machine.draw(screen)
        screen.blit(
            font_25.render("INSERT COIN", True, BLACK),
            (button_machine.x + 22, button_machine.y + 15)
        )

        effect_color = WHITE
        effect_title = "Эффект:"
        effect_text = buffm.last_result_text if buffm.last_result_text else "Пока нет эффекта"

        current_effect_kind = buffm.last_effect_kind
        if buffm.active_effect_id is not None:
            _, current_effect_kind, _, _, _, _ = buffm.EFFECTS[buffm.active_effect_id]

        if current_effect_kind == "buff":
            effect_color = (140, 255, 140)
            effect_title = "Бафф:"
        elif current_effect_kind == "debuff":
            effect_color = (255, 140, 140)
            effect_title = "Дебафф:"

        effect_y = button_machine.y + 70
        screen.blit(font_25.render(effect_title, True, effect_color), (BUFF_MACHINE_TEXT_X, effect_y))
        if show_buff_effect_end_notice:
            screen.blit(
                font_20.render("Эффект кончился", True, (255, 245, 140)),
                (BUFF_MACHINE_TEXT_X + 112, effect_y + 4)
            )
        effect_y += 24
        effect_y = draw_wrapped_text(
            screen,
            effect_text,
            font_20,
            WHITE,
            BUFF_MACHINE_TEXT_X,
            effect_y,
            BUFF_MACHINE_TEXT_W,
            20
        )

        if buffm.active_effect_id is not None and buffm.active_effect_timer is not None:
            screen.blit(
                font_20.render(f"До конца: {buffm.active_effect_timer.time_format()}", True, effect_color),
                (BUFF_MACHINE_TEXT_X, effect_y + 8)
            )

        button_to_minigame_from_game.draw(screen)
        screen.blit(
            font_30.render("Полка", True, BLACK),
            (850, 730)
        ) 
        screen.blit(
            font_25.render("Зелёное поле", True, BLACK),
            (button_to_minigame_from_game.x + 16, button_to_minigame_from_game.y + 15)
        )
        if total_clicks < 1000 and not isReached1000clicks:
            screen.blit(
                locked_button_gfield,
                (button_to_minigame_from_game.x, button_to_minigame_from_game.y)
            )
        
        if boost >= 50:
            screen.blit(
            font_30.render("Буст: Макс.", True, BLACK),
            (55, 650)
        )
        else:
            screen.blit(
                font_30.render(f"Буст: x{boost + 1}", True, BLACK),
                (55, 650)
            )

        screen.blit(
            font_25.render(f"Цена: {int(required_clicks_for_boost)}", True, BLACK),
            (56, 676)
        )
        button_to_menu_from_game.draw(screen)
        screen.blit(
            font_30.render("Меню", True, BLACK),
            (button_to_menu_from_game.x + 52.5, button_to_menu_from_game.y + 10.5),
        )
        tama_on_screen.update()
        tama_on_screen.draw(screen)
        if tama_on_screen.name == "glitch" and not cfa_IT.unlocked:
            cfa_IT.unlocked = True
            cfa_IT.show_popup = True
            cfa_IT.timer.reset()
            glitch_sound.play()
        if tama_on_screen.name == "sanic" and not cfa_sanic_popout.unlocked:
            cfa_sanic_popout.unlocked = True
            cfa_sanic_popout.show_popup = True
            cfa_sanic_popout.timer.reset()
            sanic_sound.play()
        if show_boost and mode == "game":
            shake_x = random.randint(-2, 2)
            shake_y = random.randint(-2, 2)
            boost_pos_shaken = (boost_pos[0] + shake_x, boost_pos[1] + shake_y)
            screen.blit(
                font_30.render(f"+{boost}", True, WHITE),
                boost_pos_shaken,
            )
            if clicking_text_timer.done() and mode == "game":
                show_boost = False
        if show_intro_game_text:
            screen.blit(
                font_25.render("Namatama меняется каждый клик", True, WHITE),
                (300, 700),
            )
        if total_clicks >= 1000 and not cfa_1000_clicks.unlocked:
            cfa_1000_clicks.unlocked = True
            cfa_1000_clicks.show_popup = True
            cfa_1000_clicks.timer.reset()
        if total_clicks >= 10000 and not cfa_10000_clicks.unlocked:
            cfa_10000_clicks.unlocked = True
            cfa_10000_clicks.show_popup = True
            cfa_1000_clicks.timer.reset()   
        if total_clicks >= 100000 and not cfa_1000000_clicks.unlocked:
            cfa_1000000_clicks.unlocked = True
            cfa_1000000_clicks.show_popup = True
            cfa_1000_clicks.timer.reset()
                
        cfa_1000_clicks.pop_out(screen)
        cfa_10000_clicks.pop_out(screen)
        cfa_1000000_clicks.pop_out(screen)

        cfa_IT.pop_out(screen)
        cfa_sanic_popout.pop_out(screen)

    if mode == "menu":
        screen.blit(menu_screen, (0, 0))
        button_to_achievements_from_menu.draw(screen)
        button_to_game_from_menu.draw(screen)
        button_to_settings_from_menu.draw(screen)
        screen.blit(
            font_30.render("Настройки", True, BLACK),
            (button_to_settings_from_menu.x + 20, button_to_settings_from_menu.y + 10),
        )
        screen.blit( 
            font_25.render("Достижения", True, BLACK),
            (button_to_game_from_menu.x + 18, button_to_game_from_menu.y + 85.5),
        )
        screen.blit(
            font_30.render("Играть", True, BLACK),
            (button_to_game_from_menu.x + 50, button_to_game_from_menu.y + 10.5),
        )
        button_to_credits_from_menu.draw(screen)
        screen.blit(
            font_25.render("Информация", True, BLACK),
            (button_to_credits_from_menu.x + 20, button_to_credits_from_menu.y + 14),
        )
    if mode == "achievements":
        screen.blit(achievements_bg_ru, (0, 0)) 
        achievements_back_button.draw(screen)
        cfa_collect_all_tamas.draw(screen)
        cfa_sanic_popout.draw(screen)
        cfa_IT.draw(screen)
        cfa_1000_clicks.draw(screen)
        cfa_10000_clicks.draw(screen)
        cfa_1000000_clicks.draw(screen)
        draw_button_text(
            screen,
            "Нажмите чтобы вернуться в Меню",
            font_25,
            BLACK,
            achievements_back_button,
            (12, 14),
        )
    if mode == "credits":
        screen.blit(credits_bg_ru, (0, 0))
        credits_back_button.draw(screen)
        draw_button_text(
            screen,
            "Нажмите чтобы вернуться в Меню",
            font_25,
            BLACK,
            credits_back_button,
            (15, 14),
        )
    if mode == "settings":
        screen.blit(settings_bg, (0, 0))
        settings_back_button.draw(screen)
        screen.blit(volume_icon, (420 + 20, 57))
        screen.blit(volume_icon, (400 + 20, 218))
        draw_button_text(
            screen,
            "Нажмите чтобы вернуться в Меню",
            font_25,
            BLACK,
            settings_back_button,
            (16, 14),
        )

        screen.blit(
            font_40.render("SFX", True, BLACK),
            (409 + 57.5 + 20, 50)
        )
        screen.blit(
            font_40.render("MUSIC", True, BLACK),
            (409 + 36 + 20, 210)
        )
        sfx_button_plus.draw(screen)
        screen.blit(
            font_40.render("+", True, BLACK),
            (sfx_button_plus.rect.x + 80, sfx_button_plus.rect.y + 6)
        )
        sfx_button_minus.draw(screen)
        screen.blit(
            font_40.render("-", True, BLACK),
            (sfx_button_minus.rect.x + 80, sfx_button_minus.rect.y + 6)
        )
        sdtrack_button_plus.draw(screen)
        screen.blit(
            font_40.render("+", True, BLACK),
            (sdtrack_button_plus.rect.x + 80, sdtrack_button_plus.rect.y + 6)
        )
        sdtrack_button_minus.draw(screen)
        screen.blit(
            font_40.render("-", True, BLACK),
            (sdtrack_button_minus.rect.x + 80, sdtrack_button_minus.rect.y + 6)
        )
    if mode == "minigame" and isTutorialWatched:
        screen.blit(field_bg, (0, 0))
        button_back_from_minigame.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_minigame.x + 52.5, button_back_from_minigame.y + 10.5),)
        )
        namaPlayer.draw(screen)

        for coin in coins:
            coin.draw(screen)

        if coin_spawn_timer.done() and len(coins) < MAX_COINS:
            if random.random() < 0.2:
                    coins.append(BoostCoin())
            else:
                coins.append(Coin())
            coin_spawn_timer.reset()

        for coin in coins[:]:
            if namaPlayer.rect.colliderect(coin.rect):
                coins.remove(coin)

                if isinstance(coin, BoostCoin):
                    boost_coin = 2
                    coin_boost_active = True
                    coin_boost_timer.reset()
                else:
                    farm_mult = buffm.get_farm_coin_multiplier() if buffm else 1
                    NamaCoins += 1 * boost_coin * farm_mult

                coins_collecting.play()

    if coin_boost_active and coin_boost_timer.done():
        boost_coin = 1
        coin_boost_active = False
    
    if mode == "shelf":
        screen.blit(shelf_bg, (0, 0))
        button_back_from_shelf.draw(screen)
        button_to_shop_from_shelf.draw(screen)
        
        if teddy_bear.isBought:
            teddy_bear.draw(screen)
        
        if beluash.isBought:
            beluash.draw(screen)

        if contestant.isBought:
            contestant.draw(screen)

        if tiger_fruit.isBought:
            tiger_fruit.draw(screen)
        
        if energy_drink.isBought:
            energy_drink.draw(screen)
        
        if minigun.isBought:
            minigun.draw(screen)

        screen.blit(
            font_30.render("В магазин", True, BLACK),
            ((button_to_shop_from_shelf.x + 20.5, button_to_shop_from_shelf.y + 10.5),)
        )
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_shelf.x + 52.5, button_back_from_shelf.y + 10.5),)
        )
        
    if mode == "shop":
        screen.blit(shop_bg, (0, 0))
        button_back_from_shop.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            (button_back_from_shop.x + 52.5, button_back_from_shop.y + 10.5)
        )
        if isReached1000clicks:
            button_exchanging.draw(screen)
            screen.blit(
                font_30.render("Обменник", True, BLACK),
                (button_exchanging.x + 25, button_exchanging.y + 10.5)
            )
        else:
            screen.blit(locked_exchange_button, (button_exchanging.x, button_exchanging.y))
        beluash.draw(screen)
        energy_drink.draw(screen)
        minigun.draw(screen)
        contestant.draw(screen)
        tiger_fruit.draw(screen)
        teddy_bear.draw(screen)
    
    if mode == "teddy_bear_preview":
        screen.blit(teddy_bear_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
        if not teddy_bear.isBought:
            button_buy_bear.draw(screen) 
            screen.blit(
                font_30.render("Купить", True, BLACK),
                ((button_buy_bear.x + 45, button_buy_bear.y + 10.5),)
            )
    if mode == "beluash_preview":
        screen.blit(beluash_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
        if not beluash.isBought:
            button_buy_beluash.draw(screen)
            screen.blit(
                font_30.render("Купить", True, BLACK),
                ((button_buy_beluash.x + 45, button_buy_beluash.y + 10.5),)
            )
        
    if mode == "contestant_preview":
        screen.blit(contestant_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
        if not contestant.isBought:
            button_buy_contestant.draw(screen)
            screen.blit(
                font_30.render("Купить", True, BLACK),
                ((button_buy_contestant.x + 45, button_buy_contestant.y + 10.5),)
            )

    if mode == "energy_drink_preview":
        screen.blit(energy_drink_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
    
    if mode == "tiger_fruit_preview":
        screen.blit(tiger_fruit_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
    
    if mode == "minigun_preview":
        screen.blit(minigun_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
    
    if mode == "NamaPass":
        screen.blit(namapass_bg, (0, 0))
        button_back_from_battle_pass.draw(screen)
        button_to_sponsors_from_NamaPass.draw(screen)
        screen.blit(
            font_30.render("Спонсоры", True, BLACK),
            ((button_to_sponsors_from_NamaPass.x + 30, button_to_sponsors_from_NamaPass.y + 10.5),)
        )
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_battle_pass.x + 52.5, button_back_from_battle_pass.y + 10.5),)
        )

        if namapass_5min_timer.done():
            namapass_100_coins.isCountdownDone = True
            namapass_100_coins.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_5min_timer.time_format()}", True, WHITE),
                (198 - 12, 472)
            )
        if namapass_100_coins.isCollected:
            screen.blit(namapass_100_coins.collected_item, namapass_100_coins.rect)

        if namapass_10min_timer.done():
            namapass_200_coins.isCountdownDone = True
            namapass_200_coins.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_10min_timer.time_format()}", True, WHITE),
                (490 - 12, 472)
            )
        if namapass_200_coins.isCollected:
            screen.blit(namapass_200_coins.collected_item, namapass_200_coins.rect)

        if namapass_15min_timer.done():
            namapass_500_coins.isCountdownDone = True
            namapass_500_coins.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_15min_timer.time_format()}", True, WHITE),
                (782 - 12, 472)
            )
        if namapass_500_coins.isCollected:
            screen.blit(namapass_500_coins.collected_item, namapass_500_coins.rect)

        if namapass_20min_timer.done():
            namapass_trentila_reward.isCountdownDone = True
            namapass_trentila_reward.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_20min_timer.time_format()}", True, WHITE),
                (782 - 12, 204)
            )
        if namapass_trentila_reward.isCollected:
            screen.blit(
                namapass_trentila_reward.collected_item,
                namapass_trentila_reward.rect
            )

        if namapass_25min_timer.done():
            namapass_ospuze_reward.isCountdownDone = True
            namapass_ospuze_reward.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_25min_timer.time_format()}", True, WHITE),
                (489 - 12, 204)
            )
        if namapass_ospuze_reward.isCollected:
            screen.blit(
                namapass_ospuze_reward.collected_item,
                namapass_ospuze_reward.rect
            )

        if namapass_30min_timer.done():
            namapass_minigun_reward.isCountdownDone = True
            namapass_minigun_reward.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_30min_timer.time_format()}", True, WHITE),
                (195 - 12, 204)
            )
        if namapass_minigun_reward.isCollected:
            screen.blit(
                namapass_minigun_reward.collected_item,
                namapass_minigun_reward.rect
            )
            
    if mode == "sponsors_choice":
        screen.fill(GREY)
        button_back_from_sponsors_choice.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_sponsors_choice.x + 52.5, button_back_from_sponsors_choice.y + 10.5),)
        )

        trentila_button.draw(screen)
        ospuze_button.draw(screen)
        alfa_acta_button.draw(screen)
        vaiiya_button.draw(screen)

    #sponsors_quotes
    if mode == "trentila_sponsor_quote":
        screen.fill(GREY)
        button_back_from_sponsors_quotes.draw(screen)
        screen.blit(trentila_quote, (50, 65))
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_sponsors_quotes.x + 52.5, button_back_from_sponsors_quotes.y + 10.5),)
        )
    
    if mode == "ospuze_sponsor_quote":
        screen.fill(GREY)
        button_back_from_sponsors_quotes.draw(screen)
        screen.blit(ospuze_quote, (50, 65))
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_sponsors_quotes.x + 52.5, button_back_from_sponsors_quotes.y + 10.5),)
        )
    
    if mode == "alfa_acta_sponsor_quote":
        screen.fill(GREY)
        button_back_from_sponsors_quotes.draw(screen)
        screen.blit(alfa_acta_quote, (50, 65))
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_sponsors_quotes.x + 52.5, button_back_from_sponsors_quotes.y + 10.5),)
        )
    
    if mode == "vaiiya_sponsor_quote":
        screen.fill(GREY)
        button_back_from_sponsors_quotes.draw(screen)
        screen.blit(vaiiya_quote, (50, 65))
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_sponsors_quotes.x + 52.5, button_back_from_sponsors_quotes.y + 10.5),)
        )
    if not isTutorialWatched and mode == "tutorial_gfield":
        screen.blit(tutorial_gfield, (0, 0))
        button_got_it.draw(screen)
        screen.blit(
            font_30.render("Понятно", True, BLACK),
            ((button_got_it.x + 42.5, button_got_it.y + 10.5),)
        )

    if mode == "exchanger":
        screen.blit(exchanger_bg, (0, 0))
        button_exchanging_back_to_shop.draw(screen)
        button_exchange_to_coins.draw(screen)
        button_exchange_to_clicks.draw(screen)

        screen.blit(
            font_30.render("Назад", True, BLACK),
            (button_exchanging_back_to_shop.x + 52.5, button_exchanging_back_to_shop.y + 10.5)
        )
        screen.blit(
            font_40.render("Клики → NamaCoins", True, BLACK),
            (320, 230)
        )
        screen.blit(
            font_40.render("NamaCoins → Клики", True, BLACK),
            (320, 400)
        )
        screen.blit(
            font_30.render("Обменять", True, BLACK),
            (button_exchange_to_coins.x + 25, button_exchange_to_coins.y + 10.5)
        )
        screen.blit(
            font_30.render("Обменять", True, BLACK),
            (button_exchange_to_clicks.x + 25, button_exchange_to_clicks.y + 10.5)
        )

    if mode == "backgrounds_shop":
        screen.fill(GREY)
        button_back_from_backgrounds_shop.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            (button_back_from_backgrounds_shop.x + 52.5, button_back_from_backgrounds_shop.y + 10.5)
        )
        seoul_bg.draw_button(screen)
        if seoul_bg.isBought:
            status_text_seoul = "Надеть" if not seoul_bg.equipped else "Надет"
            screen.blit(
                font_25.render(f"Куплено. {status_text_seoul}", True, BLACK),
                (seoul_bg.button_rect.x, seoul_bg.button_rect.bottom + 10)
            )
        else:
            screen.blit(
                font_25.render(f"Цена: {seoul_bg.price} NamaCoins", True, BLACK),
                (seoul_bg.button_rect.x, seoul_bg.button_rect.bottom + 10)
            )

        kyoto_bg.draw_button(screen)
        if kyoto_bg.isBought:
            status_text_kyoto = "Надеть" if not kyoto_bg.equipped else "Надет"
            screen.blit(
                font_25.render(f"Куплено. {status_text_kyoto}", True, BLACK),
                (kyoto_bg.button_rect.x, kyoto_bg.button_rect.bottom + 10)
            )
        else:
            screen.blit(
                font_25.render(f"Цена: {kyoto_bg.price} NamaCoins", True, BLACK),
                (kyoto_bg.button_rect.x, kyoto_bg.button_rect.bottom + 10)
            )

        bernal_bg.draw_button(screen)
        if bernal_bg.isBought:
            status_text_bernal = "Надеть" if not bernal_bg.equipped else "Надет"
            screen.blit(
                font_25.render(f"Куплено. {status_text_bernal}", True, BLACK),
                (bernal_bg.button_rect.x, bernal_bg.button_rect.bottom + 10)
            )
        else:
            screen.blit(
                font_25.render(f"Цена: {bernal_bg.price} NamaCoins", True, BLACK),
                (bernal_bg.button_rect.x, bernal_bg.button_rect.bottom + 10)
            )

    for pop in song_popouts.values():
        pop.update()
        pop.draw(screen)

    # Загрузка
    if isLoading:
        screen.fill(GREY)
        if cooldown_timer.done():
            mouse_click_sound.play()
            mode = next_mode
            isLoading = False
    
    if total_clicks != last_total_clicks_for_shake:
        last_total_clicks_for_shake = total_clicks
        clicks_shake_timer.reset()

    if NamaCoins != last_nama_coins_for_shake:
        last_nama_coins_for_shake = NamaCoins
        nama_shake_timer.reset()

    if total_clicks >= 1000:
        isReached1000clicks = True

    if total_clicks > 0:
        show_intro_game_text = False

    if (
        mode != "menu"
        and mode != "credits"
        and mode != "settings"
        and mode != "achievements"
        and mode != "NamaPass"
        and mode != "tutorial_gfield"
    ):
        screen.blit(angle_frame, (776, 0))
        screen.blit(NamaCoin_image, (792, 0))
        screen.blit(click_image, (792, 47))

        coins_text = font_30.render(f": {NamaCoins}", True, BLACK)
        if not nama_shake_timer.done():
            shake_x = random.randint(-1, 1)
            shake_y = random.randint(-1, 1)
            screen.blit(coins_text, (860 + shake_x, 13 + shake_y))
        else:
            screen.blit(coins_text, (860, 13))

        clicks_text = font_30.render(f": {int(total_clicks)}", True, BLACK)
        if not clicks_shake_timer.done():
            shake_x = random.randint(-1, 1)
            shake_y = random.randint(-1, 1)
            screen.blit(clicks_text, (860 + shake_x, 60 + shake_y))
        else:
            screen.blit(clicks_text, (860, 60))

    save_system.maybe_autosave(globals())
    pygame.display.flip()
    clock.tick(FPS)

print("Game is quitting")
pygame.quit()
