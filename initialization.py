import pygame


W = 1000
H = 800
FPS = 60
DEFAULT_MODE = "menu"

GAME_FONT = "assets/fonts/Tiny5-Regular.ttf"

DEFAULT_VOLUME = 0.5
DEFAULT_SOUNDTRACK_VOLUME = 0.5
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
    "assets/sounds/osts/ElIndomable_ost.mp3",
]

MUSIC_END_EVENT = pygame.USEREVENT + 1

EXCHANGE_CLICKS_PER_NAMACOIN = 50

VALID_MODES = {
    "game",
    "menu",
    "credits",
    "achievements",
    "settings",
    "minigame",
    "shelf",
    "shop",
    "beluash_preview",
    "contestant_preview",
    "energy_drink_preview",
    "tiger_fruit_preview",
    "minigun_preview",
    "teddy_bear_preview",
    "NamaPass",
    "sponsors_choice",
    "trentila_sponsor_quote",
    "ospuze_sponsor_quote",
    "alfa_acta_sponsor_quote",
    "vaiiya_sponsor_quote",
    "tutorial_gfield",
    "exchanger",
    "backgrounds_shop",
}
