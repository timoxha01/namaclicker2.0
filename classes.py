import pygame
import random
import math

_load_image = None
_load_sound = None


def set_load_image(loader):
    global _load_image
    _load_image = loader


def set_load_sound(loader):
    global _load_sound
    _load_sound = loader

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

class Button:
    BASE_IMAGE = None

    def __init__(self, x, y):
        if _load_image is None:
            raise RuntimeError("set_load_image(load_image) must be called before creating Button")
        self.x = x
        self.y = y
        if Button.BASE_IMAGE is None:
            Button.BASE_IMAGE = _load_image("assets/images/UI/button.png", alpha=True)
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

class SongsPopouts:
    def __init__(self, image_path, x=15, y=680):
        self.base_image = _load_image(image_path, alpha=True)
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

class Coin:
    def __init__(self, image, screen_size):
        self.image = image
        w, h = screen_size
        self.rect = self.image.get_rect(
            center=(
                random.randint(50, w - 50),
                random.randint(50, h - 50),
            )
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class BoostCoin(Coin):
    BOOST_COIN_IMAGE = None

    def __init__(self, screen_size):
        super().__init__(None, screen_size)
        w, h = screen_size
        if BoostCoin.BOOST_COIN_IMAGE is None:
            BoostCoin.BOOST_COIN_IMAGE = _load_image("assets/images/UI/NamaCoin_boost.png", alpha=True)
        self.image = BoostCoin.BOOST_COIN_IMAGE
        self.rect = self.image.get_rect(
            center=(
                random.randint(50, w - 50),
                random.randint(50, h - 50),
            )
        )

class Namas:
    def __init__(self, name, path, chance, screen_size, fps):
        self.name = name
        w, h = screen_size
        self.base_pos = (w // 2, h // 2)
        self.pos = self.base_pos
        self.original_image = _load_image(path, alpha=True)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.pos)
        self.chance = chance
        self.fps = fps
        self.sway_time = 0.0
        self.sway_duration = 0.15
        self.sway_amplitude = 4

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def add_clicks(self, amount, boost):
        self.clicks += amount * boost

    def update(self):
        if self.sway_time > 0.0:
            self.sway_time -= 1.0 / self.fps
            t = max(0.0, self.sway_time / self.sway_duration)
            offset = math.sin((1.0 - t) * math.pi * 4) * self.sway_amplitude * t
            self.pos = (self.base_pos[0] + offset, self.base_pos[1])
        else:
            self.pos = self.base_pos

        self.rect = self.image.get_rect(center=self.pos)

    def pulse(self):
        self.sway_time = self.sway_duration

class Achievements:
    POP_OUT_LABEL = None
    HIDDEN_IMAGE = None
    ACHIEVEMENT_SOUND = None

    def __init__(self, pop_out_text, x, y, screen_width, font_large, font_small, text_color):
        self.x_pop_out = 500 
        self.target_y = 30
        self.speed = 7
        self.pop_out_text = pop_out_text
        self.screen_width = screen_width
        self.font_large = font_large
        self.font_small = font_small
        self.text_color = text_color
        self.sound_played = False
        if _load_sound is None:
            raise RuntimeError("set_load_sound(load_sound) must be called before creating Achievements")
        if Achievements.POP_OUT_LABEL is None:
            Achievements.POP_OUT_LABEL = _load_image("assets/images/UI/pop_out_label.png", alpha=True)
        if Achievements.HIDDEN_IMAGE is None:
            Achievements.HIDDEN_IMAGE = _load_image("assets/images/UI/hidden_achi.png", alpha=True)
        if Achievements.ACHIEVEMENT_SOUND is None:
            Achievements.ACHIEVEMENT_SOUND = _load_sound("assets/sounds/sfxes/nofitication_sound.mp3")
        self.pop_out_label = Achievements.POP_OUT_LABEL
        self.pop_rect = self.pop_out_label.get_rect(
            midtop=(self.screen_width // 2, - self.pop_out_label.get_height())
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
            self.font_large.render("Новое достижение!", True, self.text_color),
            (self.pop_rect.x + 40, self.pop_rect.y + 25),
        )
        screen.blit(
            self.font_small.render(self.pop_out_text, True, self.text_color),
            (self.pop_rect.x + ((self.font_small.size(self.pop_out_text)[0] // 4) - 30),
             self.pop_rect.y + 70),
        )
    def reset_popup(self):
        self.y_pop_out = -137
        self.sound_played = False 
        self.timer.reset()

class ShopItems():
    def __init__(self, image_path, price, x, y) -> None:
        self.price = price
        self.image = _load_image(image_path, alpha=True)
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

class Background:
    def __init__(self, bg_path, price, buy_button_path, x_button, y_button) -> None:
        self.bg_image = _load_image(bg_path, alpha=False)
        self.price = price
        self.isBought = False
        self.equipped = False
        self.x_button = x_button
        self.y_button = y_button
        self.original_button_image = _load_image(buy_button_path, alpha=True)
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

class NamaPassItemsCollect:
    BUTTON_IMAGE = None
    COLLECTED_IMAGE = None

    def __init__(self, button_x, button_y):
        self.button_x = button_x
        self.button_y = button_y
        if NamaPassItemsCollect.BUTTON_IMAGE is None:
            NamaPassItemsCollect.BUTTON_IMAGE = _load_image("assets/images/UI/collect_button.png", alpha=True)
        if NamaPassItemsCollect.COLLECTED_IMAGE is None:
            NamaPassItemsCollect.COLLECTED_IMAGE = _load_image("assets/images/UI/namapass_collected.png", alpha=True)
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
