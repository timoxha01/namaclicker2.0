import random
import pygame

pygame.init()

W, H = 1000, 800
FPS = 60
mode = "menu"
lang = "ru"

GAME_FONT = "assets/fonts/Tiny5-Regular.ttf"
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.display.set_caption("NamaClicker 2.0")
pygame.display.set_icon(pygame.image.load("assets/images/tamas/classic.png"))
font_40 = pygame.font.Font(GAME_FONT, 40)
font_30 = pygame.font.Font(GAME_FONT, 30)
font_25 = pygame.font.Font(GAME_FONT, 25)
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

inc = pygame.image.load("assets/images/UI/loading_logo.png")
credits_bg_en = pygame.image.load("assets/images/UI/credits_en.png")
credits_bg_ru = pygame.image.load("assets/images/UI/credits_ru.png")

credits_back_button = pygame.image.load("assets/images/UI/button_long.png")
credits_back_button_rect = credits_back_button.get_rect(center=(W // 2, H - 40))

class Namas:
    def __init__(self, name, path, chance):
        self.name = name
        self.pos = (W // 2, 300)
        self.original_image = pygame.image.load(path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.pos)
        self.chance = chance
        self.clicks = 0
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


class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/images/UI/button.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

tamas = [
    Namas("classic", "assets/images/tamas/classic.png", 1.5), 
    Namas("search", "assets/images/tamas/search.png", 0.5),
    Namas("tea", "assets/images/tamas/tea.png", 0.3),
    Namas("bob", "assets/images/tamas/bob.png", 0.2),
    Namas("builder", "assets/images/tamas/builder.png", 0.1),
    Namas("birthday", "assets/images/tamas/birthday.png", 0.1),
    Namas("stone", "assets/images/tamas/stone.png", 0.1),
    Namas("gun", "assets/images/tamas/gun.png", 0.05),
    Namas("galaxy", "assets/images/tamas/galaxy.png", 0.05),
    Namas("vibe", "assets/images/tamas/vibe.png", 0.03),
    Namas("evil", "assets/images/tamas/evil.png", 0.001),
    Namas("demon", "assets/images/tamas/demon.png", 0.001),
]

def add_clicks():
    global tama_on_screen, total_clicks, show_boost, clicking_text_timer, seen_tamas, boost_pos
    tama_on_screen.add_clicks(1, tama_on_screen.boost)
    total_clicks += 1 * tama_on_screen.boost
    show_boost = True
    clicking_text_timer.reset()
    tama_on_screen = choose_tama(tamas)
    tama_on_screen.pulse()
    # Достижение: Собрать все виды tamas
    seen_tamas.add(tama_on_screen.name)
    if len(seen_tamas) == len(tamas):
        pass
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

button_to_menu_from_game = Button(20, 720)
button_to_game_from_menu = Button((W // 2) - (183 // 2), (H // 2) - (58 // 2))
button_to_credits_from_menu = Button((W // 2) - (183 // 2), (H // 2) + 40)

clicking_text_timer = Timer(200)
loading_timer = Timer(1)

isLoading = False
seen_tamas = set()
tama_on_screen = tamas[0]
total_clicks = 0
show_boost = False
next_mode = ""

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #перед закрытием добавить звук намы "byebye!"
            running = False

            # MouseButton действия:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and button_to_game_from_menu.rect.collidepoint(event.pos)
                and mode == "menu"
            ):
                isLoading = True
                next_mode = "game"
                loading_timer.reset()
            if button_to_menu_from_game.rect.collidepoint(event.pos) and mode == "game":
                isLoading = True
                next_mode = "menu"
                loading_timer.reset()
            if button_to_credits_from_menu.rect.collidepoint(event.pos) and mode == "menu":
                isLoading = True
                next_mode = "credits"
                loading_timer.reset()
            if credits_back_button_rect.collidepoint(event.pos) and mode == "credits":
                isLoading = True
                next_mode = "menu"
                loading_timer.reset()
            if tama_on_screen.rect.collidepoint(event.pos) and mode == "game":
                add_clicks()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                add_clicks()

    if mode == "game" and tama_on_screen is not None:
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
        if show_boost and mode == "game":
            screen.blit(
                font_30.render(f"+{tama_on_screen.boost}", True, WHITE),
                boost_pos
            )
            if clicking_text_timer.done() and mode == "game":
                show_boost = False
        if total_clicks == 0 and mode == "game":
            screen.blit(
                font_25.render("Namatama меняется каждый клик", True, WHITE),
                (300, 500),
            )
    if mode == "menu":
        screen.fill(GREY)
        button_to_game_from_menu.draw(screen)
        screen.blit(
            font_30.render("Играть", True, BLACK),
            (button_to_game_from_menu.x + 50, button_to_game_from_menu.y + 10.5),
        )
        button_to_credits_from_menu.draw(screen)
        screen.blit(
            font_25.render("Информация", True, BLACK),
            (button_to_credits_from_menu.x + 20, button_to_credits_from_menu.y + 14),
        )
    if mode == "credits":
        screen.blit(credits_bg_ru, (0, 0))
        screen.blit(credits_back_button, credits_back_button_rect)
        screen.blit(
            font_25.render("Нажмите чтобы вернуться в Меню", True, BLACK),
            (credits_back_button_rect.x + 15, credits_back_button_rect.y + 14),
        )
    #Загрузка
    if isLoading:
        screen.fill(GREY)
        if loading_timer.done():
            mode = next_mode
            isLoading = False
            
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()