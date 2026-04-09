
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

coins = []
MAX_COINS = 5
required_clicks_for_boost = 100
current_music_credits = None
isLoading = False
isReached1000clicks = False
isTutorialWatched = False
notif_visible = False
notif_5_shown = False
notif_10_shown = False
notif_15_shown = False
notif_20_shown = False
notif_25_shown = False
notif_30_shown = False
show_intro_game_text = True
seen_tamas = set()

boost_coin = 1
coin_boost_active = False

total_clicks = 0
NamaCoins = 0
boost = 1

last_total_clicks_for_shake = 0
last_nama_coins_for_shake = 0

show_boost = False
next_mode = ""

EXCHANGE_CLICKS_PER_NAMACOIN = 50
