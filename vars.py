from classes import *

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

music_loop = []

EXCHANGE_CLICKS_PER_NAMACOIN = 50

BUFF_MACHINE_X = W - buff_machine_image.get_width() - 12
BUFF_MACHINE_TEXT_W = buff_machine_image.get_width() - 16
BUFF_MACHINE_TEXT_X = BUFF_MACHINE_X + 8

cooldown_timer = Timer(1)
clicking_text_timer = Timer(200)
coin_spawn_timer = Timer(2000)
coin_boost_timer = Timer(5000)
nama_shake_timer = Timer(200)
clicks_shake_timer = Timer(200)
notif_timer = Timer(1500)
buffm_intermission_timer = Timer(120000)
buff_effect_end_notice_timer = Timer(2000)
namapass_5min_timer = Timer(300000)
namapass_10min_timer = Timer(600000)
namapass_15min_timer = Timer(900000)
namapass_20min_timer = Timer(1200000)
namapass_25min_timer = Timer(1500000)
namapass_30min_timer = Timer(1800000)

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
button_to_backgrounds_shop = Button(800, 650)
button_back_from_backgrounds_shop = Button(20, 720)

sfx_button_plus = Button(527, 114)
sfx_button_minus = Button(289, 114)
sdtrack_button_plus = Button(527, 275)
sdtrack_button_minus = Button(289, 275)

button_got_it = Button(471 - (183 // 2) + 45, 730)

button_buy_bear = Button((W // 2) - (183 // 2), 550)
button_buy_beluash = Button((W // 2) - (183 // 2), 550)
button_buy_contestant = Button((W // 2) - (183 // 2), 550)

button_exchanging = Button(408, 60)
button_exchanging_back_to_shop = Button(408, 60)

button_exchange_to_coins = Button(500 - (183 // 2), 310)
button_exchange_to_clicks = Button(500 - (183 // 2), 470)

namapass_100_coins = NamaPassItemsCollect(139, 461)
namapass_200_coins = NamaPassItemsCollect(433, 461)
namapass_500_coins = NamaPassItemsCollect(726, 458)
namapass_trentila_reward = NamaPassItemsCollect(726, 194)
namapass_ospuze_reward = NamaPassItemsCollect(434, 194)
namapass_minigun_reward = NamaPassItemsCollect(142, 193)

teddy_bear = ShopItems("assets/images/shop_items/teddy_bear.png", 250, 98, 173)
beluash = ShopItems("assets/images/shop_items/beluash.png", 500, 410, 173)
contestant = ShopItems("assets/images/shop_items/contestant.png", 1000, 722, 173)
energy_drink = ShopItems("assets/images/shop_items/energy_drink.png", None, 410, 430)
tiger_fruit = ShopItems("assets/images/shop_items/tiger_fruit.png", None, 98, 430)
minigun = ShopItems("assets/images/shop_items/minigun.png", None, 722, 430)

BUFF_MACHINE_Y = 100
show_buff_effect_end_notice = False

banner = NamaPassbanner()
buffm = BuffMachine()
namaPlayer = NamaPlayer()

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
    Namas("boykisser", "assets/images/tamas/boykisser.png", 0.01),
    Namas("sanic", "assets/images/tamas/sanic_ee.png", 0.001),
    Namas("glitch", "assets/images/tamas/glitch_ee.png", 0.001)
]

tama_on_screen = tamas[0]

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

cfa_collect_all_tamas = Achievements("Собрать все NamaTama", 64, 80)
cfa_sanic_popout = Achievements("Встретить Sanic", 372, 80)
cfa_IT = Achievements("Встретить ...", 679, 80)
cfa_1000_clicks = Achievements("Набрать 1000 кликов", 65, 382)
cfa_10000_clicks = Achievements("Набрать 10000 кликов", 372, 382)
cfa_1000000_clicks = Achievements("Набрать 1000000 кликов", 679, 382)

seoul_bg = Background("assets/images/UI/seoul_bg.png", 100, "assets/images/UI/seoul_buy_button.png", 408, 246)
kyoto_bg = Background("assets/images/UI/kyoto_bg.png", 250, "assets/images/UI/kyoto_bg_button.png", 408, 351)
bernal_bg = Background("assets/images/UI/bernal_bg.png", 400, "assets/images/UI/kyoto_bg_button.png", 408, 456)

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

button_machine = Button(
    BUFF_MACHINE_X + (buff_machine_image.get_width() - 183) // 2,
    BUFF_MACHINE_Y + buff_machine_image.get_height() + 48
)