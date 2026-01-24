import random

import pygame

pygame.init()

W, H = 800, 600
FPS = 50
mode = "game"

GREY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)

pygame.display.set_caption("NamaClicker 2.0 | Prototype")
pygame.display.set_icon(pygame.image.load("assets/images/tamas/classic.png"))
font = pygame.font.Font("assets/fonts/PixelifySans-Medium.ttf", 40)
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()


class Namas:
    def __init__(self, name, path, chance):
        self.name = name
        self.pos = (W // 2, H // 2)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.chance = chance
        self.clicks = 0
        self.boost = 1
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def add_clicks(self, amount, boost):
        self.clicks += amount * boost


tamas = [
    Namas("classic", "assets/images/tamas/classic.png", 0.9),
    Namas("like", "assets/images/tamas/like.png", 0.6),
    Namas("bob", "assets/images/tamas/bob.png", 0.5),
    Namas("builder", "assets/images/tamas/builder.png", 0.4),
    Namas("gun", "assets/images/tamas/gun.png", 0.3),
    Namas("kinger", "assets/images/tamas/kinger.png", 0.2),
    Namas("vibe", "assets/images/tamas/vibe.png", 0.1),
    Namas("evil", "assets/images/tamas/evil.png", 0.01),
    Namas("demon", "assets/images/tamas/demon.png", 0.001),
]

def choose_tama(tamas):
    total_chance = sum(t.chance for t in tamas)
    roll = random.uniform(0, total_chance)

    current = 0
    for tama in tamas:
        current += tama.chance
        if roll <= current:
            return tama


seen_tamas = set()
tama_on_screen = tamas[0]
total_clicks = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and mode == "game"
            and tama_on_screen is not None
            and event.button == 1
        ):
            if tama_on_screen.rect.collidepoint(event.pos):
                tama_on_screen.add_clicks(1, tama_on_screen.boost)
                total_clicks += 1 * tama_on_screen.boost
                if total_clicks % 10 == 0:
                    tama_on_screen = choose_tama(tamas)
                
                #Достижение: Собрать все виды tamas
                seen_tamas.add(tama_on_screen.name)
                if len(seen_tamas) == len(tamas):
                    pass

    if mode == "game" and tama_on_screen is not None:
        screen.fill(GREY)
        tama_on_screen.draw(screen)
        
        clicks_text = font.render(str(total_clicks), True, WHITE)
        screen.blit(clicks_text, (W // 2 - clicks_text.get_width() // 2, 450))

    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()