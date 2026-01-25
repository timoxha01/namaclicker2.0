import random

import pygame

pygame.init()

W, H = 1000, 800
FPS = 60
mode = "game"

GAME_FONT = "assets/fonts/Tiny5-Regular.ttf"
GREY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.display.set_caption("NamaClicker 2.0 | Prototype")
pygame.display.set_icon(pygame.image.load("assets/images/tamas/classic.png"))
font_40 = pygame.font.Font(GAME_FONT, 40)
font_30 = pygame.font.Font(GAME_FONT, 30)
font_25 = pygame.font.Font(GAME_FONT, 25)
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()


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


tamas = [
    Namas("classic", "assets/images/tamas/classic.png", 0.9),
    Namas("like", "assets/images/tamas/like.png", 0.6),
    Namas("bob", "assets/images/tamas/bob.png", 0.5),
    Namas("builder", "assets/images/tamas/builder.png", 0.4),
    Namas("gun", "assets/images/tamas/gun.png", 0.3),
    Namas("kinger", "assets/images/tamas/kinger.png", 0.2),
    Namas("vibe", "assets/images/tamas/vibe.png", 0.1),
    Namas("evil", "assets/images/tamas/evil.png", 0.01),
    Namas("demon", "assets/images/tamas/demon.png", 0.01),
]


def choose_tama(tamas):
    total_chance = sum(t.chance for t in tamas)
    roll = random.uniform(0, total_chance)

    current = 0
    for tama in tamas:
        current += tama.chance
        if roll <= current:
            return tama


button_to_menu_from_game = Button(20, 720)

clicking_text_timer = Timer(250)

seen_tamas = set()
tama_on_screen = tamas[0]
total_clicks = 0
show_boost = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # MouseButton действия:
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and mode == "game"
            and tama_on_screen is not None
            and event.button == 1
        ):
            if button_to_menu_from_game.rect.collidepoint(event.pos):
                mode = "menu"
            if tama_on_screen.rect.collidepoint(event.pos):
                tama_on_screen.add_clicks(1, tama_on_screen.boost)
                total_clicks += 1 * tama_on_screen.boost
                show_boost = True
                boost_pos = (
                    random.randint(0, W - 50),
                    random.randint(0, H - 50),
                )
                clicking_text_timer.reset()
                if total_clicks % 10 == 0:
                    tama_on_screen = choose_tama(tamas)
                    tama_on_screen.pulse()
                # Достижение: Собрать все виды tamas
                seen_tamas.add(tama_on_screen.name)
                if len(seen_tamas) == len(tamas):
                    pass

    if mode == "game" and tama_on_screen is not None:
        screen.fill(GREY)
        tama_on_screen.update()
        tama_on_screen.draw(screen)
        screen.blit(button_to_menu_from_game.image, button_to_menu_from_game.rect)
        screen.blit(font_30.render("Меню", True, BLACK), (button_to_menu_from_game.x + 52.5, button_to_menu_from_game.y + 10.5))

        clicks_text = font_40.render(str(total_clicks), True, WHITE)
        screen.blit(clicks_text, (W // 2 - clicks_text.get_width() // 2, 440))
        if show_boost:
            screen.blit(
                font_30.render(f"+{tama_on_screen.boost}", True, WHITE),
                boost_pos,
            )
            if clicking_text_timer.done():
                show_boost = False
        if total_clicks == 0:
            screen.blit(
                font_25.render("Namatama меняется каждые 10 кликов", True, WHITE),
                (270, 500),
            )
    if mode == "menu":
        screen.fill(BLACK)
        screen.blit(font_40.render("MENU", True, WHITE), (400, 290))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
