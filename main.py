import random
import pygame

pygame.init()
pygame.mixer.init()

print("Loading...")

W, H = 1000, 800
FPS = 50
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
pygame.display.set_icon(pygame.image.load("assets/images/tamas/classic.png"))
font_40 = pygame.font.Font(GAME_FONT, 40)
font_30 = pygame.font.Font(GAME_FONT, 30)
font_25 = pygame.font.Font(GAME_FONT, 25)
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

credits_bg_ru = pygame.image.load("assets/images/UI/credits.png")
menu_screen = pygame.image.load("assets/images/UI/menu_screen.png")

settings_bg = pygame.image.load("assets/images/UI/settings_bg.png")

achievements_bg_ru = pygame.image.load("assets/images/UI/achievements.png")

volume_icon = pygame.image.load("assets/images/UI/volume_icon.png")

long_button_img = pygame.image.load(
    "assets/images/UI/button_long.png"
).convert_alpha()



NamaCoin_image = pygame.image.load("assets/images/UI/NamaCoin.png")
angle_frame = pygame.image.load("assets/images/UI/angle_frame.png").convert_alpha()

field_bg = pygame.image.load("assets/images/UI/greenfield.png")

pickable_namacoin = pygame.image.load("assets/images/UI/NamaCoin.png").convert_alpha()

locked_button_gfield = pygame.image.load("assets/images/UI/locked_button_1000.png").convert_alpha()

shelf_bg = pygame.image.load("assets/images/UI/shelf_bg.png")

shop_bg = pygame.image.load("assets/images/UI/shop_bg.png")

namapass_bg = pygame.image.load("assets/images/UI/namapass_bg.png")

tutorial_gfield = pygame.image.load("assets/images/UI/tutorial_gfield.png")

exc_mark = pygame.image.load("assets/images/UI/exc_mark.png")

beluash_preview = pygame.image.load("assets/images/UI/beluash_preview.png").convert_alpha()
contestant_preview = pygame.image.load("assets/images/UI/contestant_preview.png").convert_alpha()
tiger_fruit_preview = pygame.image.load("assets/images/UI/tiger_fruit_preview.png").convert_alpha()
energy_drink_preview = pygame.image.load("assets/images/UI/energy_drink_preview.png").convert_alpha()
minigun_preview = pygame.image.load("assets/images/UI/minigun_preview.png").convert_alpha()
teddy_bear_preview = pygame.image.load("assets/images/UI/teddy_bear_preview.png").convert_alpha()

namapass_banner_alfa_acta = pygame.image.load("assets/images/UI/namapass_banner_alfa_acta.png").convert_alpha()
namapass_banner_ospuze = pygame.image.load("assets/images/UI/namapass_banner_ospuze.png").convert_alpha()
namapass_banner_trentila = pygame.image.load("assets/images/UI/namapass_banner_trentila.png").convert_alpha()
namapass_banner_vaiiya = pygame.image.load("assets/images/UI/namapass_banner_vaiiya.png").convert_alpha()

trentila_button_img = pygame.image.load(
    "assets/images/UI/trentila_button.png"
).convert_alpha()
vaiiya_button_img = pygame.image.load(
    "assets/images/UI/vaiiya_button.png"
).convert_alpha()
ospuze_button_img = pygame.image.load(
    "assets/images/UI/ospuze_button.png"
).convert_alpha()
alfa_acta_button_img = pygame.image.load(
    "assets/images/UI/alfa_acta_button.png"
).convert_alpha()

vaiiya_quote = pygame.image.load("assets/images/UI/vaiiya_info.png").convert_alpha()
trentila_quote = pygame.image.load("assets/images/UI/trentila_info.png").convert_alpha()
ospuze_quote = pygame.image.load("assets/images/UI/ospuze_info.png").convert_alpha()
alfa_acta_quote = pygame.image.load("assets/images/UI/alfa_acta_info.png").convert_alpha()

byebye_nama_sound = pygame.mixer.Sound("assets/sounds/sfxes/namatama_byebye.mp3")
click_sound = pygame.mixer.Sound("assets/sounds/sfxes/click_sound.mp3")
mouse_click_sound = pygame.mixer.Sound("assets/sounds/sfxes/mouse_click.mp3")
glitch_sound = pygame.mixer.Sound("assets/sounds/sfxes/screamer_glitch.mp3")
sanic_sound = pygame.mixer.Sound("assets/sounds/sfxes/screamer_sanic.mp3")
volume_changing_sound = pygame.mixer.Sound("assets/sounds/sfxes/volume_change_sound.mp3")
purchase_success = pygame.mixer.Sound("assets/sounds/sfxes/purchase_success.mp3")
purchase_failed = pygame.mixer.Sound("assets/sounds/sfxes/purchase_failed.mp3")
coins_collecting = pygame.mixer.Sound("assets/sounds/sfxes/NamaCoins_collecting.mp3")
nofitication_sound = pygame.mixer.Sound("assets/sounds/sfxes/announcement.mp3")

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
        self.pos = (W // 2, 300)
        self.original_image = pygame.image.load(path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.pos)
        self.chance = chance
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.15
        self.pulsing = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def add_clicks(self, amount, boost):
        self.clicks += amount * boost

    def update(self):
        if self.scale != self.target_scale:
            self.scale += (self.target_scale - self.scale) * self.scale_speed

            if abs(self.scale - self.target_scale) < 0.01:
                self.scale = self.target_scale
                if self.pulsing:
                    self.target_scale = 1.0
                    self.pulsing = False

            size = (
                int(self.original_image.get_width() * self.scale),
                int(self.original_image.get_height() * self.scale),
            )
            self.image = pygame.transform.smoothscale(self.original_image, size)
            self.rect = self.image.get_rect(center=self.pos)

    def pulse(self):
        self.scale = 0.85
        self.target_scale = 1.0 
        self.pulsing = True

class NamaPlayer():
    def __init__(self):
        self.x = 25
        self.y = 523
        self.original_image = pygame.image.load("assets/images/tamas/classic.png")
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
        self.image = pygame.image.load(image_path).convert_alpha()
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

class NamaPassItemsCollect:
    def __init__(self, button_x, button_y):
        self.button_x = button_x
        self.button_y = button_y
        self.button_image = pygame.image.load("assets/images/UI/collect_button.png")
        self.collected_item = pygame.image.load("assets/images/UI/namapass_collected.png")
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
        self.base_image = pygame.image.load(image_path).convert_alpha()
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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_image = pygame.image.load(
            "assets/images/UI/button.png"
        ).convert_alpha()
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
    def __init__(self, pop_out_text, x, y):
        self.x_pop_out = 500 
        self.target_y = 30
        self.speed = 7
        self.pop_out_text = pop_out_text
        self.sound_played = False
        self.pop_out_label = pygame.image.load(
            "assets/images/UI/pop_out_label.png"
        ).convert_alpha()
        self.pop_rect = self.pop_out_label.get_rect(
            midtop=(W // 2, - self.pop_out_label.get_height())
        )
        self.y_pop_out = self.pop_rect.y
        self.achievement_sound = pygame.mixer.Sound(
            "assets/sounds/sfxes/nofitication_sound.mp3"
            )
        self.image = pygame.image.load(
            "assets/images/UI/hidden_achi.png"
        ).convert_alpha()
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
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            "assets/images/UI/NamaCoin_boost.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(
            center=(
                random.randint(50, W - 50),
                random.randint(50, H - 50),
            )
        )

def add_clicks():
    global \
        tama_on_screen, \
        total_clicks, \
        show_boost, \
        clicking_text_timer, \
        seen_tamas, \
        boost_pos, \
        boost
    total_clicks += 1 * boost
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
    Namas("sanic", "assets/images/tamas/sanic_ee.png", 0.001),
    Namas("glitch", "assets/images/tamas/glitch_ee.png", 0.001),
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

sfx_button_plus = Button(527, 114)
sfx_button_minus = Button(289, 114)
sdtrack_button_plus = Button(527, 275)
sdtrack_button_minus = Button(289, 275)

button_got_it = Button(471 - (183 // 2) + 45, 730)

button_buy_bear = Button((W // 2) - (183 // 2), 550)
button_buy_beluash = Button((W // 2) - (183 // 2), 550)
button_buy_contestant = Button((W // 2) - (183 // 2), 550)

clicking_text_timer = Timer(200)
cooldown_timer = Timer(1)
coin_spawn_timer = Timer(2000)
coin_boost_timer = Timer(5000)

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

coins = []
MAX_COINS = 5
required_clicks_for_boost = 200
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
seen_tamas = set()
tama_on_screen = tamas[0]

boost_coin = 1
coin_boost_active = False

total_clicks = 0
boost = 1
NamaCoins = 0

show_boost = False
next_mode = ""

play_next_soundtrack()
print("Game Loaded, Booting up...")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            byebye_nama_sound.play()
            pygame.time.delay(int(byebye_nama_sound.get_length() * 1000))
            running = False
        if event.type == MUSIC_END_EVENT:
            play_next_soundtrack()
            # MouseButton действия:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_to_game_from_menu.rect.collidepoint(event.pos) and mode == "menu":
                isLoading = True
                next_mode = "game"
                cooldown_timer.reset()
            if button_to_menu_from_game.rect.collidepoint(event.pos) and mode == "game":
                isLoading = True
                next_mode = "menu"
                cooldown_timer.reset()
            if (
                button_to_credits_from_menu.rect.collidepoint(event.pos)
                and mode == "menu"
            ):
                isLoading = True
                next_mode = "credits"
                cooldown_timer.reset()
            if credits_back_button.rect.collidepoint(event.pos) and mode == "credits":
                isLoading = True
                next_mode = "menu"
                cooldown_timer.reset()
            if (
                button_to_achievements_from_menu.rect.collidepoint(event.pos)
                and mode == "menu"
            ):
                isLoading = True
                next_mode = "achievements"
                cooldown_timer.reset()
            if (
                achievements_back_button.rect.collidepoint(event.pos)
                and mode == "achievements"
            ):
                isLoading = True
                next_mode = "menu"
                cooldown_timer.reset()
            if (
                button_to_settings_from_menu.rect.collidepoint(event.pos)
                and mode == "menu"
            ):
                isLoading = True
                next_mode = "settings"
                cooldown_timer.reset()
            if (
                settings_back_button.rect.collidepoint(event.pos)
                and mode == "settings"
            ):
                isLoading = True
                next_mode = "menu"
                cooldown_timer.reset()
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
                isLoading = True
                next_mode = "game"
                cooldown_timer.reset()
            if (
                button_to_shelf_from_game.rect.collidepoint(event.pos)
                and mode == "game"
            ):
                isLoading = True
                next_mode = "shelf"
                cooldown_timer.reset()
            if (
                button_back_from_shelf.rect.collidepoint(event.pos)
                and mode == "shelf"
            ):
                isLoading = True
                next_mode = "game"
                cooldown_timer.reset()
            if (
                button_back_from_shop.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                isLoading = True
                next_mode = "shelf"
                cooldown_timer.reset()
            if (
                button_boost.rect.collidepoint(event.pos)
                and mode == "game"
            ):
                if total_clicks >= required_clicks_for_boost:
                    total_clicks -= required_clicks_for_boost
                    boost += 1
                    required_clicks_for_boost *= 2
                    purchase_success.play()
                else:
                    purchase_failed.play()
            if (
                button_to_shop_from_shelf.rect.collidepoint(event.pos)
                and mode == "shelf"
            ):
                isLoading = True
                next_mode = "shop"
                cooldown_timer.reset()
            if tama_on_screen.rect.collidepoint(event.pos) and mode == "game":
                add_clicks()
            if (
                button_back_from_shelf.rect.collidepoint(event.pos)
                and mode == "shelf"
            ):
                isLoading = True
                next_mode = "game"
                cooldown_timer.reset()
            if (
                banner.rect.collidepoint(event.pos)
                and mode == "game"
            ):
                isLoading = True
                next_mode = "NamaPass"
                cooldown_timer.reset()
            if (
                button_back_from_battle_pass.rect.collidepoint(event.pos)
                and mode == "NamaPass"
            ):
                isLoading = True
                next_mode = "game"
                cooldown_timer.reset()
            if (
                button_got_it.rect.collidepoint(event.pos)
                and mode == "tutorial_gfield"
            ):
                isLoading = True
                isTutorialWatched = True
                next_mode = "minigame"
                cooldown_timer.reset()

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
                isLoading = True
                next_mode = "teddy_bear_preview"
                cooldown_timer.reset()
            if (
                beluash.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                isLoading = True
                next_mode = "beluash_preview"
                cooldown_timer.reset()
            if (
                energy_drink.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                isLoading = True
                next_mode = "energy_drink_preview"
                cooldown_timer.reset()
            if (
                tiger_fruit.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                isLoading = True
                next_mode = "tiger_fruit_preview"
                cooldown_timer.reset()
            if (
                minigun.rect.collidepoint(event.pos)
                and mode == "shop"
            ):
                isLoading = True
                next_mode = "minigun_preview"
                cooldown_timer.reset()
            if (
                contestant.rect.collidepoint(event.pos)
                and mode == "shop" 
            ):
                isLoading = True
                next_mode = "contestant_preview"
                cooldown_timer.reset()
            if (
                button_to_sponsors_from_NamaPass.rect.collidepoint(event.pos)
                and mode == "NamaPass"
            ):
                isLoading = True
                next_mode = "sponsors_choice"
                cooldown_timer.reset()
            if (
                button_back_from_sponsors_choice.rect.collidepoint(event.pos)
                and mode == "sponsors_choice"
            ):
                isLoading = True
                next_mode = "NamaPass"
                cooldown_timer.reset()
            if (
                trentila_button.rect.collidepoint(event.pos)
                and mode == "sponsors_choice"
            ):
                isLoading = True
                next_mode = "trentila_sponsor_quote"
                cooldown_timer.reset()
            if (
                ospuze_button.rect.collidepoint(event.pos)
                and mode == "sponsors_choice"
            ):
                isLoading = True
                next_mode = "ospuze_sponsor_quote"
                cooldown_timer.reset()
            if (
                alfa_acta_button.rect.collidepoint(event.pos)
                and mode == "sponsors_choice"
            ):
                isLoading = True
                next_mode = "alfa_acta_sponsor_quote"
                cooldown_timer.reset()
            if (
                vaiiya_button.rect.collidepoint(event.pos)
                and mode == "sponsors_choice"
            ):
                isLoading = True
                next_mode = "vaiiya_sponsor_quote"
                cooldown_timer.reset()
            

            if (
                back_button_from_preview.rect.collidepoint(event.pos)
                and mode in ["teddy_bear_preview", "beluash_preview", 
                        "energy_drink_preview", "tiger_fruit_preview",
                            "minigun_preview", "contestant_preview"]
                ):
                isLoading = True
                next_mode = "shop"
                cooldown_timer.reset()

            if (
                button_back_from_sponsors_quotes.rect.collidepoint(event.pos)
                and mode in ["ospuze_sponsor_quote", "trentila_sponsor_quote", 
                        "alfa_acta_sponsor_quote", "vaiiya_sponsor_quote"]
                ):
                isLoading = True
                next_mode = "sponsors_choice"
                cooldown_timer.reset()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and mode == "game":
                add_clicks()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a] and mode == "minigame":
        namaPlayer.x -= 3
    if keys[pygame.K_RIGHT] or keys[pygame.K_d] and mode == "minigame":
        namaPlayer.x += 3
    if keys[pygame.K_UP] or keys[pygame.K_w] and mode == "minigame":
        namaPlayer.y -= 3
    if keys[pygame.K_DOWN] or keys[pygame.K_s] and mode == "minigame":
        namaPlayer.y += 3

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

    # DRAW MODE
    if mode == "game":
        screen.fill(GREY)
        button_boost.draw(screen)

        button_to_shelf_from_game.draw(screen)

        banner.change_banner()
        banner.update()
        banner.draw(screen)

        ShowNofitication(screen)
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
        screen.blit(
            font_30.render(f"Буст: +{boost + 1}", True, BLACK),
            (55, 650)
        )
        screen.blit(
            font_25.render(f"Цена: {required_clicks_for_boost}", True, BLACK),
            (56, 676)
        )
        button_to_menu_from_game.draw(screen)
        screen.blit(
            font_30.render("Меню", True, BLACK),
            (button_to_menu_from_game.x + 52.5, button_to_menu_from_game.y + 10.5),
        )
        tama_on_screen.update()
        tama_on_screen.draw(screen)
        clicks_text = font_40.render(str(total_clicks), True, WHITE)
        screen.blit(clicks_text, (W // 2 - clicks_text.get_width() // 2, 440))
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
            screen.blit(
                font_30.render(f"+{boost}", True, WHITE), boost_pos
            )
            if clicking_text_timer.done() and mode == "game":
                show_boost = False
        if total_clicks == 0 and mode == "game":
            screen.blit(
                font_25.render("Namatama меняется каждый клик", True, WHITE),
                (300, 500),
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
                    NamaCoins += 1 * boost_coin

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
            ((button_back_from_shop.x + 52.5, button_back_from_shop.y + 10.5),)
        )
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
    
    if total_clicks >= 1000:
        isReached1000clicks = True

    if (
        mode != "menu"
        and mode != "credits"
        and mode != "settings"
        and mode != "achievements"
    ):
        screen.blit(angle_frame, (781, 0))
        screen.blit(NamaCoin_image, (792, 7))
        screen.blit(
            font_30.render(f": {NamaCoins}", True, BLACK),
            (865, 20)
        )

    pygame.display.flip()
    clock.tick(FPS)

print("Game is quitting")
pygame.quit()