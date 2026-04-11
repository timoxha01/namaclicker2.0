from assets_loading import *
import pygame
import math
import random
import vars

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

class Namas:

    def __init__(self, name, path, chance):
        self.name = name
        self.clicks = 0
        self.base_pos = (vars.W // 2, vars.H // 2)
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
            self.sway_time -= 1.0 / vars.FPS
            t = max(0.0, self.sway_time / self.sway_duration)
            offset = math.sin((1.0 - t) * math.pi * 4) * self.sway_amplitude * t
            self.pos = (self.base_pos[0] + offset, self.base_pos[1])
        else:
            self.pos = self.base_pos

        self.rect = self.image.get_rect(center=self.pos)

    def pulse(self):
        self.sway_time = self.sway_duration

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
        if not self.isCollected and self.isCountdownDone:
            self.isCollected = True
            coins_collecting.play()

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
        if vars.NamaCoins >= self.price:
            self.isBought = True
            vars.NamaCoins -= self.price
            purchase_success.play()
        else:
            purchase_failed.play()

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
            midtop=(vars.W // 2, - self.pop_out_label.get_height())
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
            vars.font_40.render("Новое достижение!", True, vars.BLACK),
            (self.pop_rect.x + 40, self.pop_rect.y + 25),
        )
        screen.blit(
            vars.font_30.render(self.pop_out_text, True, vars.BLACK),
            (self.pop_rect.x + ((vars.font_30.size(self.pop_out_text)[0] // 4) - 30),
             self.pop_rect.y + 70),
        )
    def reset_popup(self):
        self.y_pop_out = -137
        self.sound_played = False 
        self.timer.reset()

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
        if vars.NamaCoins >= self.price:
            if not self.isBought:
                purchase_success.play()
                self.isBought = True
                vars.NamaCoins -= self.price
        else:
            purchase_failed.play()

    def equip(self):
        if self.isBought:
            self.equipped = True
            volume_changing_sound.play()


class BuffMachine:
    EFFECTS = {
        "buff1": ("x1.1 кликов каждые 10 секунд на протяжении минуты!", "buff", 60000, 10000, 1.1, "clicks"),
        "buff2": ("Буст увеличивается на 2 на 10 секунд!", "buff", 10000, 0, 2, "boost_bonus"),
        "buff3": ("x3 NamaCoins на ферме!", "buff", 60000, 0, 3, "farm_coins"),
        "debuff1": ("-10 кликов каждые 3 секунды на протяжении 30 секунд!", "debuff", 30000, 3000, -10, "clicks"),
        "debuff2": ("В NamaPass к текущему оставшемуся времени добавляется 30 секунд!", "debuff", 0, 0, 30000, "namapass_delay"),
        "debuff3": ("NamaCoins делятся на 2", "debuff", 0, 0, 0, "halve_coins"),
    }

    def __init__(self) -> None:
        self.shuffle_result = None
        self.last_result_text = None
        self.last_effect_kind = None
        self.active_effect_id = None
        self.active_effect_timer = None
        self.active_effect_tick_timer = None
        self.active_effect_tick_value = 0

    def shuffle(self):
        self.active_effect_id = random.choice(list(self.EFFECTS.keys()))
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
        """Применяет мгновенные эффекты (debuff2, debuff3)."""
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
        """Обновляет эффекты с таймером (buff1, buff2, buff3, debuff1)."""
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
                pass  # обрабатывается в add_clicks через buff_boost_bonus

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

class Coin:
    def __init__(self):
        self.image = pickable_namacoin
        self.rect = self.image.get_rect(
            center=(
                random.randint(50, vars.W - 50),
                random.randint(50, vars.H - 50),
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
                random.randint(50, vars.W - 50),
                random.randint(50, vars.H - 50),
            )
        )

