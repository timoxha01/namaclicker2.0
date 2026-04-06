import math
import random


_deps = {}


def configure(**kwargs):
    _deps.update(kwargs)


def _dep(name):
    return _deps[name]


class NamaPassbanner:
    def __init__(self):
        self.x = 20
        self.y = 210

        self.banners = [
            _dep("namapass_banner_alfa_acta"),
            _dep("namapass_banner_ospuze"),
            _dep("namapass_banner_trentila"),
            _dep("namapass_banner_vaiiya"),
        ]

        self.index = 0
        self.current_image = self.banners[self.index]
        self.next_image = None

        self.alpha_current = 255
        self.alpha_next = 0

        self.fade_speed = 8
        self.is_fading = False

        self.change_delay = 3000
        self.timer = _dep("pygame").time.get_ticks()

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
            self.timer = _dep("pygame").time.get_ticks()

    def change_banner(self):
        now = _dep("pygame").time.get_ticks()

        if not self.is_fading and now - self.timer >= self.change_delay:
            self.is_fading = True

            next_index = (self.index + 1) % len(self.banners)
            self.next_image = self.banners[next_index]

            self.alpha_current = 255
            self.alpha_next = 0

    def draw(self, screen):
        mouse_pos = _dep("pygame").mouse.get_pos()
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
        img = _dep("pygame").transform.smoothscale(self.current_image, (w, h))
        self.rect = img.get_rect(center=self.base_rect.center)
        screen.blit(img, self.rect)

        if self.is_fading and self.next_image:
            w = int(self.next_image.get_width() * self.scale)
            h = int(self.next_image.get_height() * self.scale)
            img_next = _dep("pygame").transform.smoothscale(self.next_image, (w, h))
            img_next.set_alpha(self.alpha_next)
            rect_next = img_next.get_rect(center=self.base_rect.center)
            screen.blit(img_next, rect_next)


class Namas:
    def __init__(self, name, path, chance):
        self.name = name
        self.base_pos = (_dep("W") // 2, _dep("H") // 2)
        self.pos = self.base_pos
        self.original_image = _dep("load_image")(path, alpha=True)
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
            self.sway_time -= 1.0 / _dep("FPS")
            t = max(0.0, self.sway_time / self.sway_duration)
            offset = math.sin((1.0 - t) * math.pi * 4) * self.sway_amplitude * t
            self.pos = (self.base_pos[0] + offset, self.base_pos[1])
        else:
            self.pos = self.base_pos

        self.rect = self.image.get_rect(center=self.pos)

    def pulse(self):
        self.sway_time = self.sway_duration


class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start = _dep("pygame").time.get_ticks()

    def done(self):
        return _dep("pygame").time.get_ticks() - self.start >= self.duration

    def reset(self):
        self.start = _dep("pygame").time.get_ticks()

    def time_left(self):
        return max(0, self.duration - (_dep("pygame").time.get_ticks() - self.start))

    def time_format(self):
        total_sec = self.time_left() // 1000
        minutes = total_sec // 60
        seconds = total_sec % 60
        return f"{minutes:02d}:{seconds:02d}"


class BuffMachine:
    EFFECTS = {
        "buff1": ("x1.1 РєР»РёРєРѕРІ РєР°Р¶РґС‹Рµ 10 СЃРµРєСѓРЅРґ РЅР° РїСЂРѕС‚СЏР¶РµРЅРёРё РјРёРЅСѓС‚С‹!", "buff", 60000, 10000, 1.1, "clicks"),
        "buff2": ("Р‘СѓСЃС‚ СѓРІРµР»РёС‡РёРІР°РµС‚СЃСЏ РЅР° 2 РЅР° 10 СЃРµРєСѓРЅРґ!", "buff", 10000, 0, 2, "boost_bonus"),
        "buff3": ("x3 NamaCoins РЅР° С„РµСЂРјРµ!", "buff", 60000, 0, 3, "farm_coins"),
        "debuff1": ("-10 РєР»РёРєРѕРІ РєР°Р¶РґС‹Рµ 3 СЃРµРєСѓРЅРґС‹ РЅР° РїСЂРѕС‚СЏР¶РµРЅРёРё 30 СЃРµРєСѓРЅРґ!", "debuff", 30000, 3000, -10, "clicks"),
        "debuff2": ("Р’ NamaPass Рє С‚РµРєСѓС‰РµРјСѓ РѕСЃС‚Р°РІС€РµРјСѓСЃСЏ РІСЂРµРјРµРЅРё РґРѕР±Р°РІР»СЏРµС‚СЃСЏ 30 СЃРµРєСѓРЅРґ!", "debuff", 0, 0, 30000, "namapass_delay"),
        "debuff3": ("NamaCoins РґРµР»СЏС‚СЃСЏ РЅР° 2", "debuff", 0, 0, 0, "halve_coins"),
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
                for name in [
                    "namapass_5min_timer",
                    "namapass_10min_timer",
                    "namapass_15min_timer",
                    "namapass_20min_timer",
                    "namapass_25min_timer",
                    "namapass_30min_timer",
                ]:
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
        self.image_path = _dep("load_image")(image_path, alpha=True)
        self.image_path_x = int(image_path_x)
        self.image_path_y = int(image_path_y)
        self.rect = self.image_path.get_rect()
        self.dialogueWindow = _dep("load_image")(dialogueWindow_path, alpha=True)
        self.isTriggered = False
        self.dialogueText = ""
        self.visible_chars = 0
        self.char_delay_ms = 35
        self.last_char_tick = _dep("pygame").time.get_ticks()
        self.dialogue_sound_delay_ms = 70
        self.last_dialogue_sound_tick = 0
        self.isEntered = False
        self.eButton_image = _dep("load_image")("assets/images/UI/eButton.png")
        self.button_x = button_x
        self.button_y = button_y

    def shufflePhrases(self):
        self.dialogueText = random.choice(self.phrases)
        self.visible_chars = 0
        self.last_char_tick = _dep("pygame").time.get_ticks()

    def update_typing_effect(self):
        if not self.isTriggered:
            return
        if self.visible_chars >= len(self.dialogueText):
            return

        now = _dep("pygame").time.get_ticks()
        elapsed = now - self.last_char_tick
        if elapsed < self.char_delay_ms:
            return

        chars_to_add = max(1, elapsed // self.char_delay_ms)
        self.visible_chars = min(len(self.dialogueText), self.visible_chars + chars_to_add)
        self.last_char_tick += chars_to_add * self.char_delay_ms
        if now - self.last_dialogue_sound_tick >= self.dialogue_sound_delay_ms:
            _dep("text_dialogue_sound").play()
            self.last_dialogue_sound_tick = now

    def drawDialogueWindow(self, screen):
        if self.isTriggered:
            self.update_typing_effect()
            screen.blit(self.dialogueWindow, (0, 662))
            screen.blit(_dep("font_30").render(self.name, True, _dep("BLACK")), (43, 662))
            typed_text = self.dialogueText[:self.visible_chars]
            screen.blit(_dep("font_30").render(typed_text, True, _dep("BLACK")), (30, 750))

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
        self.bg_image = _dep("load_image")(bg_path, alpha=False)
        self.price = price
        self.isBought = False
        self.equipped = False
        self.x_button = x_button
        self.y_button = y_button
        self.original_button_image = _dep("load_image")(buy_button_path, alpha=True)
        self.buy_button_image = self.original_button_image
        self.button_base_rect = self.original_button_image.get_rect(topleft=(x_button, y_button))
        self.button_rect = self.button_base_rect.copy()
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.15

    def draw_button(self, screen):
        mouse_pos = _dep("pygame").mouse.get_pos()
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
            self.buy_button_image = _dep("pygame").transform.smoothscale(self.original_button_image, size)
            self.button_rect = self.buy_button_image.get_rect(center=self.button_base_rect.center)

        screen.blit(self.buy_button_image, self.button_rect)

    def buy(self, nama_coins):
        if nama_coins >= self.price:
            if not self.isBought:
                _dep("purchase_success").play()
                self.isBought = True
                nama_coins -= self.price
        else:
            _dep("purchase_failed").play()
        return nama_coins

    def equip(self):
        if self.isBought:
            self.equipped = True
            _dep("volume_changing_sound").play()


class NamaPlayer:
    def __init__(self):
        self.x = 25
        self.y = 523
        self.original_image = _dep("load_image")("assets/images/tamas/classic.png", alpha=True)
        self.image = _dep("pygame").transform.scale(self.original_image, (144, 144))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, self.rect)


class ShopItems:
    def __init__(self, image_path, price, x, y) -> None:
        self.price = price
        self.image = _dep("load_image")(image_path, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.isBought = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def buy(self, nama_coins):
        if nama_coins >= self.price:
            self.isBought = True
            nama_coins -= self.price
            _dep("purchase_success").play()
        else:
            _dep("purchase_failed").play()
        return nama_coins


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
            NamaPassItemsCollect.BUTTON_IMAGE = _dep("load_image")("assets/images/UI/collect_button.png", alpha=True)
        if NamaPassItemsCollect.COLLECTED_IMAGE is None:
            NamaPassItemsCollect.COLLECTED_IMAGE = _dep("load_image")("assets/images/UI/namapass_collected.png", alpha=True)
        self.button_image = NamaPassItemsCollect.BUTTON_IMAGE
        self.collected_item = NamaPassItemsCollect.COLLECTED_IMAGE
        self.rect = self.button_image.get_rect(topleft=(button_x, button_y))
        self.isCountdownDone = False
        self.isCollected = False

    def draw(self, screen):
        screen.blit(self.button_image, self.rect)

    def buy(self):
        if not self.isCollected and self.isCountdownDone:
            self.isCollected = True
            _dep("coins_collecting").play()


class SongsPopouts:
    def __init__(self, image_path, x=15, y=680):
        self.base_image = _dep("load_image")(image_path, alpha=True)
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

        img = _dep("pygame").transform.smoothscale(self.base_image, (w, h))
        screen.blit(img, (self.x, self.y))


class Button:
    BASE_IMAGE = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        if Button.BASE_IMAGE is None:
            Button.BASE_IMAGE = _dep("load_image")("assets/images/UI/button.png", alpha=True)
        self.original_image = Button.BASE_IMAGE
        self.image = self.original_image
        self.base_rect = self.original_image.get_rect(topleft=(self.x, self.y))
        self.rect = self.base_rect.copy()
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.15

    def draw(self, screen):
        mouse_pos = _dep("pygame").mouse.get_pos()
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
            self.image = _dep("pygame").transform.smoothscale(self.original_image, size)
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
        mouse_pos = _dep("pygame").mouse.get_pos()
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
            self.image = _dep("pygame").transform.smoothscale(self.original_image, size)
            self.rect = self.image.get_rect(center=self.base_rect.center)

        screen.blit(self.image, self.rect)


def draw_button_text(screen, text, font, color, button, offset):
    text_surface = font.render(text, True, color)
    scale = button.scale
    if scale != 1.0:
        w = max(1, int(text_surface.get_width() * scale))
        h = max(1, int(text_surface.get_height() * scale))
        text_surface = _dep("pygame").transform.smoothscale(text_surface, (w, h))
    x = button.rect.x + int(offset[0] * scale)
    y = button.rect.y + int(offset[1] * scale)
    screen.blit(text_surface, (x, y))


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
            Achievements.POP_OUT_LABEL = _dep("load_image")("assets/images/UI/pop_out_label.png", alpha=True)
        if Achievements.HIDDEN_IMAGE is None:
            Achievements.HIDDEN_IMAGE = _dep("load_image")("assets/images/UI/hidden_achi.png", alpha=True)
        if Achievements.ACHIEVEMENT_SOUND is None:
            Achievements.ACHIEVEMENT_SOUND = _dep("load_sound")("assets/sounds/sfxes/nofitication_sound.mp3")
        self.pop_out_label = Achievements.POP_OUT_LABEL
        self.pop_rect = self.pop_out_label.get_rect(midtop=(_dep("W") // 2, -self.pop_out_label.get_height()))
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
            _dep("font_40").render("РќРѕРІРѕРµ РґРѕСЃС‚РёР¶РµРЅРёРµ!", True, _dep("BLACK")),
            (self.pop_rect.x + 40, self.pop_rect.y + 25),
        )
        screen.blit(
            _dep("font_30").render(self.pop_out_text, True, _dep("BLACK")),
            (self.pop_rect.x + ((_dep("font_30").size(self.pop_out_text)[0] // 4) - 30), self.pop_rect.y + 70),
        )

    def reset_popup(self):
        self.y_pop_out = -137
        self.sound_played = False
        self.timer.reset()


class Coin:
    def __init__(self):
        self.image = _dep("pickable_namacoin")
        self.rect = self.image.get_rect(
            center=(
                random.randint(50, _dep("W") - 50),
                random.randint(50, _dep("H") - 50),
            )
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class BoostCoin(Coin):
    BOOST_COIN_IMAGE = None

    def __init__(self):
        super().__init__()
        if BoostCoin.BOOST_COIN_IMAGE is None:
            BoostCoin.BOOST_COIN_IMAGE = _dep("load_image")("assets/images/UI/NamaCoin_boost.png", alpha=True)
        self.image = BoostCoin.BOOST_COIN_IMAGE
        self.rect = self.image.get_rect(
            center=(
                random.randint(50, _dep("W") - 50),
                random.randint(50, _dep("H") - 50),
            )
        )


class Course:
    def __init__(self, exchange_clicks_per_namacoin) -> None:
        self.course_clicks = float(exchange_clicks_per_namacoin)
        self.course_coins = round(1.0 / exchange_clicks_per_namacoin, 6)
