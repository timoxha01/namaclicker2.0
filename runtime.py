from collections import OrderedDict

import pygame


class CachedFont:
    def __init__(self, font, max_cache=512):
        self._font = font
        self._cache = OrderedDict()
        self._max_cache = max_cache

    def render(self, text, antialias, color):
        key = (text, antialias, color)
        cached = self._cache.get(key)
        if cached is not None:
            self._cache.move_to_end(key)
            return cached
        surface = self._font.render(text, antialias, color)
        self._cache[key] = surface
        if len(self._cache) > self._max_cache:
            self._cache.popitem(last=False)
        return surface

    def size(self, text):
        return self._font.size(text)

    def __getattr__(self, name):
        return getattr(self._font, name)


def create_runtime(*, width, height, caption, icon_path, font_path, music_end_event):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_endevent(music_end_event)

    pygame.display.set_caption(caption)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load(icon_path))

    fonts = {
        40: CachedFont(pygame.font.Font(font_path, 40)),
        30: CachedFont(pygame.font.Font(font_path, 30)),
        25: CachedFont(pygame.font.Font(font_path, 25)),
        20: CachedFont(pygame.font.Font(font_path, 20)),
    }

    image_cache = {}
    sound_cache = {}

    def draw_loading_screen(message):
        screen.fill((18, 18, 18))
        title = fonts[30].render("NamaClicker 2.0", True, (230, 230, 230))
        text = fonts[30].render(message, True, (180, 180, 180))
        screen.blit(title, (width // 2 - title.get_width() // 2, height // 2 - 36))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 + 8))
        pygame.display.flip()
        pygame.event.pump()

    def load_image(path, *, alpha=True):
        key = (path, alpha)
        cached = image_cache.get(key)
        if cached is not None:
            return cached
        image = pygame.image.load(path)
        image = image.convert_alpha() if alpha else image.convert()
        image_cache[key] = image
        return image

    def load_sound(path):
        cached = sound_cache.get(path)
        if cached is not None:
            return cached
        sound = pygame.mixer.Sound(path)
        sound_cache[path] = sound
        return sound

    return {
        "screen": screen,
        "clock": clock,
        "fonts": fonts,
        "draw_loading_screen": draw_loading_screen,
        "load_image": load_image,
        "load_sound": load_sound,
    }
