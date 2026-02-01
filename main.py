import random
import pygame

pygame.init()
pygame.mixer.init()

print("Loading...")

W, H = 1000, 800
FPS = 60
mode = "menu"
lang = ""

GAME_FONT = "assets/fonts/Tiny5-Regular.ttf"
VOLUME = 1.0
VOLUME_SDTRACK = 1.0
VOLUME_STEP = 0.05
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SOUNDTRACKS = [

    "assets/sounds/osts/GoldStandard_ost.mp3",
    "assets/sounds/osts/Stardust_ost.mp3",
    "assets/sounds/osts/Syntax_CNS_ost.mp3",
    "assets/sounds/osts/TheDivide_ost.mp3",
    "assets/sounds/osts/TheWorld'sGreatestGameShow2_ost.mp3"
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

credits_bg_en = pygame.image.load("assets/images/UI/credits_en.png")
credits_bg_ru = pygame.image.load("assets/images/UI/credits_ru.png")
menu_screen = pygame.image.load("assets/images/UI/menu_screen.png")

settings_bg = pygame.image.load("assets/images/UI/settings_bg.png")

achievements_bg_ru = pygame.image.load("assets/images/UI/achievements_ru.png")
achievements_bg_en = pygame.image.load("assets/images/UI/achievements_en.png")

volume_icon = pygame.image.load("assets/images/UI/volume_icon.png")

credits_back_button = pygame.image.load("assets/images/UI/button_long.png")
achievements_back_button = pygame.image.load("assets/images/UI/button_long.png")

settings_back_button = pygame.image.load("assets/images/UI/button_long.png")
settings_back_button_rect = settings_back_button.get_rect(
    center=(W // 2, H - 40)
)
achievements_back_button_rect = achievements_back_button.get_rect(
    center=(W // 2, H - 55)
)
credits_back_button_rect = credits_back_button.get_rect(center=(W // 2, H - 40))
achievements_back_button_rect = achievements_back_button.get_rect(
    center=(W // 2, H - 55)
)

byebye_nama_sound = pygame.mixer.Sound("assets/sounds/sfxes/namatama_byebye.mp3")
click_sound = pygame.mixer.Sound("assets/sounds/sfxes/click_sound.mp3")
mouse_click_sound = pygame.mixer.Sound("assets/sounds/sfxes/mouse_click.mp3")
glitch_sound = pygame.mixer.Sound("assets/sounds/sfxes/screamer_glitch.mp3")
sanic_sound = pygame.mixer.Sound("assets/sounds/sfxes/screamer_sanic.mp3")
volume_changing_sound = pygame.mixer.Sound("assets/sounds/sfxes/volume_change_sound.mp3")

class Namas:
    def __init__(self, name, path, chance):
        self.name = name
        self.pos = (W // 2, 300)
        self.original_image = pygame.image.load(path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.pos)
        self.chance = chance
        self.boost = 1
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


class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start = pygame.time.get_ticks()

    def done(self):
        return pygame.time.get_ticks() - self.start >= self.duration

    def reset(self):
        self.start = pygame.time.get_ticks()

class SongsPopouts:
    def __init__(self, image_path, x=11, y=614):
        self.base_image = pygame.image.load(image_path).convert_alpha()
        self.x = x
        self.y = y

        self.scale = 0.0
        self.target_scale = 1.0
        self.speed = 0.15

        self.visible = False
        self.hiding = False
        self.timer = Timer(3500)

    def show(self):
        self.scale = 0.0
        self.visible = True
        self.hiding = False
        self.timer.reset()

    def update(self):
        if not self.visible:
            return

        # Появление
        if not self.hiding and self.scale < self.target_scale:
            self.scale += self.speed
            if self.scale >= self.target_scale:
                self.scale = self.target_scale
                self.timer.reset()
            return

        # Переход в скрытие
        if not self.hiding and self.timer.done():
            self.hiding = True

        # Исчезновение
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
        self.image = pygame.image.load("assets/images/UI/button.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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
            "assets/sounds/sfxes/announcement.mp3"
            )
        self.image = pygame.image.load(
            "assets/images/UI/hidden_achi_ru.png"
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


        
cfa_collect_all_tamas = Achievements("Собрать все NamaTama", 64, 80)
cfa_sanic_popout = Achievements("Встретить Sanic", 372, 80)
cfa_IT = Achievements("Встретить ...", 679, 80)
cfa_1000_clicks = Achievements("Набрать 1000 кликов", 65, 382)
cfa_10000_clicks = Achievements("Набрать 10000 кликов", 372, 382)
cfa_1000000_clicks = Achievements("Набрать 1000000 кликов", 679, 382)

song_popouts = {
    "GoldStandard_ost.mp3": SongsPopouts("assets/images/UI/GoldStandard_SongCard.png"),
    "Stardust_ost.mp3": SongsPopouts("assets/images/UI/Stardust_SongCard.png"),
    "Syntax_CNS_ost.mp3": SongsPopouts("assets/images/UI/SyntaxCNS_SongCard.png"),
    "TheDivide_ost.mp3": SongsPopouts("assets/images/UI/TheDivide_SongCard.png"),
    "TheWorld'sGreatestGameShow2.mp3": SongsPopouts("assets/images/UI/TheWorld'sGreatestGameShow2_SongCard.png")
}



tamas = [
    Namas("classic", "assets/images/tamas/classic.png", 1.0),
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

def add_clicks():
    global \
        tama_on_screen, \
        total_clicks, \
        show_boost, \
        clicking_text_timer, \
        seen_tamas, \
        boost_pos
    total_clicks += 1 * tama_on_screen.boost
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
    ]:
        sound.set_volume(VOLUME)

def play_random_soundtrack():
    track = random.choice(SOUNDTRACKS)
    pygame.mixer.music.load(track)
    pygame.mixer.music.set_volume(VOLUME_SDTRACK)
    pygame.mixer.music.play()

    filename = track.split("/")[-1]
    if filename in song_popouts:
        song_popouts[filename].show()

button_to_menu_from_game = Button(20, 720)
button_to_game_from_menu = Button((W // 2) - (183 // 2), (H // 2) - (58 // 2))
button_to_credits_from_menu = Button(800, 730)
button_to_achievements_from_menu = Button((W // 2) - (183 // 2), (H // 2) + 40)
button_to_settings_from_menu = Button((W // 2) - (183 // 2), (H // 2) + 110)
sfx_button_plus = Button(289, 114)
sfx_button_minus = Button(527, 114)
sdtrack_button_plus = Button(289, 275)
sdtrack_button_minus = Button(527, 275)

clicking_text_timer = Timer(200)
cooldown_timer = Timer(1)

current_music_credits = None
isLoading = False
seen_tamas = set()
tama_on_screen = tamas[0]
total_clicks = 0
show_boost = False
next_mode = ""

print("Game Loaded, Booting up...")
running = True
play_random_soundtrack()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            byebye_nama_sound.play()
            pygame.time.delay(int(byebye_nama_sound.get_length() * 1000))
            running = False
        if event.type == MUSIC_END_EVENT:
            play_random_soundtrack()
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

            if credits_back_button_rect.collidepoint(event.pos) and mode == "credits":
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
                achievements_back_button_rect.collidepoint(event.pos)
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
                settings_back_button_rect.collidepoint(event.pos)
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
            if tama_on_screen.rect.collidepoint(event.pos) and mode == "game":
                add_clicks()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and mode == "game":
                add_clicks()

    if mode == "game":
        screen.fill(GREY)
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
                font_30.render(f"+{tama_on_screen.boost}", True, WHITE), boost_pos
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
            font_30.render("Достижения", True, BLACK),
            (button_to_game_from_menu.x + 5, button_to_game_from_menu.y + 80.5),
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
        screen.blit(achievements_back_button, achievements_back_button_rect)
        cfa_collect_all_tamas.draw(screen)
        cfa_sanic_popout.draw(screen)
        cfa_IT.draw(screen)
        cfa_1000_clicks.draw(screen)
        cfa_10000_clicks.draw(screen)
        cfa_1000000_clicks.draw(screen)
        screen.blit(
            font_25.render("Нажмите чтобы вернуться в Меню", True, BLACK),
            (
                achievements_back_button_rect.x + 12,
                achievements_back_button_rect.y + 14,
            ),
        )
    if mode == "credits":
        screen.blit(credits_bg_ru, (0, 0))
        screen.blit(credits_back_button, credits_back_button_rect)
        screen.blit(
            font_25.render("Нажмите чтобы вернуться в Меню", True, BLACK),
            (credits_back_button_rect.x + 15, credits_back_button_rect.y + 14),
        )
    if mode == "settings":
        screen.blit(settings_bg, (0, 0))
        screen.blit(settings_back_button, settings_back_button_rect)
        screen.blit(volume_icon, (420 + 20, 57))
        screen.blit(volume_icon, (400 + 20, 218))
        screen.blit(
            font_25.render("Нажмите чтобы вернуться в Меню", True, BLACK),
            (credits_back_button_rect.x + 15, credits_back_button_rect.y + 14),
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

    pygame.display.flip()
    clock.tick(FPS)

print("Game is quitting")
pygame.quit()
