import random


def choose_tama(tamas):
    total_chance = sum(t.chance for t in tamas)
    roll = random.uniform(0, total_chance)

    current = 0
    for tama in tamas:
        current += tama.chance
        if roll <= current:
            return tama

    return tamas[-1]


def update_volume(volume, sounds):
    for sound in sounds:
        sound.set_volume(volume)


def get_next_track(music_loop, soundtracks):
    if not music_loop:
        music_loop = soundtracks.copy()
        random.shuffle(music_loop)
    return music_loop.pop(), music_loop


def play_next_soundtrack(*, pygame, volume, soundtracks, music_loop, song_popouts):
    track, music_loop = get_next_track(music_loop, soundtracks)
    pygame.mixer.music.load(track)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()

    filename = track.split("/")[-1]
    if filename in song_popouts:
        song_popouts[filename].show()

    return music_loop
