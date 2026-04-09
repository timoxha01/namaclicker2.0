import pygame

pygame.mixer.init()

_image_cache = {}
_sound_cache = {}

def load_image(path, *, alpha=True):
    key = (path, alpha)
    cached = _image_cache.get(key)
    if cached is not None:
        return cached

    image = pygame.image.load(path)
    display_surface = pygame.display.get_surface()
    if display_surface is not None:
        image = image.convert_alpha() if alpha else image.convert()

    _image_cache[key] = image
    return image

def load_sound(path):
    cached = _sound_cache.get(path)
    if cached is not None:
        return cached
    sound = pygame.mixer.Sound(path)
    _sound_cache[path] = sound
    return sound

credits_bg_ru = load_image("assets/images/UI/credits.png", alpha=False)
menu_screen = load_image("assets/images/UI/menu_screen.png", alpha=False)

settings_bg = load_image("assets/images/UI/settings_bg.png", alpha=False)

achievements_bg_ru = load_image("assets/images/UI/achievements.png", alpha=False)

volume_icon = load_image("assets/images/UI/volume_icon.png", alpha=True)

long_button_img = load_image("assets/images/UI/button_long.png", alpha=True)

NamaCoin_image = load_image("assets/images/UI/NamaCoin.png", alpha=True)
angle_frame = load_image("assets/images/UI/angle_frame.png", alpha=True)

field_bg = load_image("assets/images/UI/greenfield.png", alpha=False)

pickable_namacoin = NamaCoin_image

locked_button_gfield = load_image("assets/images/UI/locked_button_1000.png", alpha=True)

locked_exchange_button = locked_button_gfield

shelf_bg = load_image("assets/images/UI/shelf_bg.png", alpha=False)

shop_bg = load_image("assets/images/UI/shop_bg.png", alpha=False)

namapass_bg = load_image("assets/images/UI/namapass_bg.png", alpha=False)

tutorial_gfield = load_image("assets/images/UI/tutorial_gfield.png", alpha=False)

exc_mark = load_image("assets/images/UI/exc_mark.png", alpha=True)

exchanger_bg = load_image("assets/images/UI/exchanger_bg.png", alpha=False)

click_image = load_image("assets/images/UI/click_image.png", alpha=True)

beluash_preview = load_image("assets/images/UI/beluash_preview.png", alpha=True)
contestant_preview = load_image("assets/images/UI/contestant_preview.png", alpha=True)
tiger_fruit_preview = load_image("assets/images/UI/tiger_fruit_preview.png", alpha=True)
energy_drink_preview = load_image("assets/images/UI/energy_drink_preview.png", alpha=True)
minigun_preview = load_image("assets/images/UI/minigun_preview.png", alpha=True)
teddy_bear_preview = load_image("assets/images/UI/teddy_bear_preview.png", alpha=True)

namapass_banner_alfa_acta = load_image("assets/images/UI/namapass_banner_alfa_acta.png", alpha=True)
namapass_banner_ospuze = load_image("assets/images/UI/namapass_banner_ospuze.png", alpha=True)
namapass_banner_trentila = load_image("assets/images/UI/namapass_banner_trentila.png", alpha=True)
namapass_banner_vaiiya = load_image("assets/images/UI/namapass_banner_vaiiya.png", alpha=True)

buff_machine_image = load_image("assets/images/UI/buff_machine.png", alpha=True)

trentila_button_img = load_image("assets/images/UI/trentila_button.png", alpha=True)
vaiiya_button_img = load_image("assets/images/UI/vaiiya_button.png", alpha=True)
ospuze_button_img = load_image("assets/images/UI/ospuze_button.png", alpha=True)
alfa_acta_button_img = load_image("assets/images/UI/alfa_acta_button.png", alpha=True)

vaiiya_quote = load_image("assets/images/UI/vaiiya_info.png", alpha=True)
trentila_quote = load_image("assets/images/UI/trentila_info.png", alpha=True)
ospuze_quote = load_image("assets/images/UI/ospuze_info.png", alpha=True)
alfa_acta_quote = load_image("assets/images/UI/alfa_acta_info.png", alpha=True)

byebye_nama_sound = load_sound("assets/sounds/sfxes/namatama_byebye.mp3")
click_sound = load_sound("assets/sounds/sfxes/click_sound.mp3")
mouse_click_sound = load_sound("assets/sounds/sfxes/mouse_click.mp3")
glitch_sound = load_sound("assets/sounds/sfxes/screamer_glitch.mp3")
sanic_sound = load_sound("assets/sounds/sfxes/screamer_sanic.mp3")
volume_changing_sound = load_sound("assets/sounds/sfxes/volume_change_sound.mp3")
purchase_success = load_sound("assets/sounds/sfxes/purchase_success.mp3")
purchase_failed = load_sound("assets/sounds/sfxes/purchase_failed.mp3")
coins_collecting = load_sound("assets/sounds/sfxes/NamaCoins_collecting.mp3")
nofitication_sound = load_sound("assets/sounds/sfxes/announcement.mp3")
inserted_coin = load_sound("assets/sounds/sfxes/inserted_coin.mp3")