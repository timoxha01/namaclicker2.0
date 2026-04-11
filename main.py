import random
import pygame
import os
import datasave
from vars import *
from funcs import *

pygame.init()
pygame.mixer.init()

MUSIC_END_EVENT = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

pygame.display.set_caption("NamaClicker 2.0")
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("assets/images/tamas/classic.png"))

def draw_loading_screen(message):
    loading_font = pygame.font.SysFont("arial", 28)
    screen.fill((18, 18, 18))
    title = loading_font.render("NamaClicker 2.0", True, (230, 230, 230))
    text = loading_font.render(message, True, (180, 180, 180))
    screen.blit(title, (vars.W // 2 - title.get_width() // 2, vars.H // 2 - 36))
    screen.blit(text, (vars.W // 2 - text.get_width() // 2, vars.H // 2 + 8))
    pygame.display.flip()
    pygame.event.pump()
    print(message)

font_40 = pygame.font.Font(GAME_FONT, 40)
font_30 = pygame.font.Font(GAME_FONT, 30)
font_25 = pygame.font.Font(GAME_FONT, 25)
font_20 = pygame.font.Font(GAME_FONT, 20)

vars.font_40 = font_40
vars.font_30 = font_30
vars.font_25 = font_25
vars.font_20 = font_20

SAVE_PATH = os.path.join(os.path.dirname(__file__), "data.json")
save_system = datasave.SaveSystem(
    pygame=pygame,
    update_volume_cb=update_volume,
    save_path=SAVE_PATH,
    autosave_every_ms=3000,
    save_version=1,
)

draw_loading_screen("Инициализация мира...")
from classes import *
from assets_loading import *
save_system.load(vars.__dict__)


play_next_soundtrack()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_system.save(vars.__dict__)
            pygame.mixer.music.stop()
            byebye_nama_sound.play()
            pygame.time.delay(int(byebye_nama_sound.get_length() * 1000))
            running = False
        if event.type == MUSIC_END_EVENT:
            play_next_soundtrack()

            # MouseButton действия:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_to_game_from_menu.rect.collidepoint(event.pos) and vars.mode == "menu":
                load_mode("game")
            if button_to_menu_from_game.rect.collidepoint(event.pos) and vars.mode == "game":
                load_mode("menu")
            if (
                button_to_credits_from_menu.rect.collidepoint(event.pos)
                and vars.mode == "menu"
            ):
                load_mode("credits")
            if credits_back_button.rect.collidepoint(event.pos) and vars.mode == "credits":
                load_mode("menu")
            if (
                button_to_achievements_from_menu.rect.collidepoint(event.pos)
                and vars.mode == "menu"
            ):
                load_mode("achievements")
            if (
                achievements_back_button.rect.collidepoint(event.pos)
                and vars.mode == "achievements"
            ):
                load_mode("menu")
            if (
                button_to_settings_from_menu.rect.collidepoint(event.pos)
                and vars.mode == "menu"
            ):
                load_mode("settings")
            if (
                settings_back_button.rect.collidepoint(event.pos)
                and vars.mode == "settings"
            ):
                load_mode("menu")
            if (
                sfx_button_plus.rect.collidepoint(event.pos)
                and vars.mode == "settings"
            ):
                vars.VOLUME = min(1.0, vars.VOLUME + VOLUME_STEP)
                update_volume()
                volume_changing_sound.play()
            if (
                sfx_button_minus.rect.collidepoint(event.pos)
                and vars.mode == "settings"
            ):
                vars.VOLUME = max(0.0, vars.VOLUME - VOLUME_STEP)
                update_volume()
                volume_changing_sound.play()
            if (
                sdtrack_button_plus.rect.collidepoint(event.pos)
                and vars.mode == "settings"
            ):
                vars.VOLUME_SDTRACK = min(1.0, vars.VOLUME_SDTRACK + VOLUME_STEP)
                pygame.mixer.music.set_volume(vars.VOLUME_SDTRACK)
                volume_changing_sound.play()
            if (
                sdtrack_button_minus.rect.collidepoint(event.pos)
                and vars.mode == "settings"
            ):
                vars.VOLUME_SDTRACK = max(0.0, vars.VOLUME_SDTRACK - VOLUME_STEP)
                pygame.mixer.music.set_volume(vars.VOLUME_SDTRACK)
                volume_changing_sound.play()
            if (
                button_to_minigame_from_game.rect.collidepoint(event.pos)
                and vars.mode == "game"
            ):
                if vars.total_clicks >= 1000 or vars.isReached1000clicks:
                    vars.isLoading = True
                    if vars.isTutorialWatched:
                        vars.next_mode = "minigame"
                    else:
                        vars.next_mode = "tutorial_gfield"
                    cooldown_timer.reset()
            if (
                button_back_from_minigame.rect.collidepoint(event.pos)
                and vars.mode == "minigame"
            ):
                load_mode("game")
            if (
                button_to_shelf_from_game.rect.collidepoint(event.pos)
                and vars.mode == "game"
            ):
                load_mode("shelf")
            if (
                button_back_from_shelf.rect.collidepoint(event.pos)
                and vars.mode == "shelf"
            ):
                load_mode("game")
            if (
                button_back_from_shop.rect.collidepoint(event.pos)
                and vars.mode == "shop"
            ):
                load_mode("shelf")
            if (
                button_boost.rect.collidepoint(event.pos)
                and vars.mode == "game"
            ):
                if vars.total_clicks >= vars.required_clicks_for_boost and vars.boost < 50:
                    vars.total_clicks -= vars.required_clicks_for_boost
                    vars.boost += 1
                    vars.required_clicks_for_boost *= 1.5
                    purchase_success.play()
                else:
                    purchase_failed.play()
            if (
                button_to_shop_from_shelf.rect.collidepoint(event.pos)
                and vars.mode == "shelf"
            ):
                load_mode("shop")
            if vars.tama_on_screen.rect.collidepoint(event.pos) and vars.mode == "game":
                add_clicks()
            if (
                button_back_from_shelf.rect.collidepoint(event.pos)
                and vars.mode == "shelf"
            ):
                load_mode("game")
            if (
                banner.rect.collidepoint(event.pos)
                and vars.mode == "game"
            ):
                load_mode("NamaPass")
            if (
                button_back_from_battle_pass.rect.collidepoint(event.pos)
                and vars.mode == "NamaPass"
            ):
                load_mode("game")
            if (
                button_got_it.rect.collidepoint(event.pos)
                and vars.mode == "tutorial_gfield"
            ):
                load_mode("minigame")
                vars.isTutorialWatched = True

            if (
                button_exchanging.rect.collidepoint(event.pos)
                and vars.mode == "shop"
                and vars.isReached1000clicks
            ):
                load_mode("exchanger")

            if (
                button_exchanging_back_to_shop.rect.collidepoint(event.pos)
                and vars.mode == "exchanger"
            ):
                load_mode("shop")

            # обменник
            if (
                button_exchange_to_coins.rect.collidepoint(event.pos)
                and vars.mode == "exchanger"
            ):
                if vars.total_clicks > 0:
                    gained_coins = int(vars.total_clicks // EXCHANGE_CLICKS_PER_NAMACOIN)
                    if gained_coins > 0:
                        vars.NamaCoins += gained_coins
                        vars.total_clicks = int(vars.total_clicks % EXCHANGE_CLICKS_PER_NAMACOIN)
                        coins_collecting.play()
                else:
                    purchase_failed.play()

            if (
                button_exchange_to_clicks.rect.collidepoint(event.pos)
                and vars.mode == "exchanger"
            ):
                if vars.NamaCoins > 0:
                    gained_clicks = int(vars.NamaCoins * EXCHANGE_CLICKS_PER_NAMACOIN)
                    if gained_clicks > 0:
                        vars.total_clicks += gained_clicks
                        vars.NamaCoins = 0
                        coins_collecting.play()
                else:
                    purchase_failed.play()
       

            #namapass
            if (
                namapass_100_coins.rect.collidepoint(event.pos)
                and vars.mode == "NamaPass"
                and namapass_100_coins.isCountdownDone
            ):
                if not namapass_100_coins.isCollected:
                    namapass_100_coins.buy()
                    vars.NamaCoins += 100
            if (
                namapass_200_coins.rect.collidepoint(event.pos)
                and vars.mode == "NamaPass"
                and namapass_200_coins.isCountdownDone
            ):
                if not namapass_200_coins.isCollected:
                    namapass_200_coins.buy()
                    vars.NamaCoins += 200
            if (
                namapass_500_coins.rect.collidepoint(event.pos)
                and vars.mode == "NamaPass"
                and namapass_500_coins.isCountdownDone
            ):
                if not namapass_500_coins.isCollected:
                    namapass_500_coins.buy()
                    vars.NamaCoins += 500
            if (
                namapass_trentila_reward.rect.collidepoint(event.pos)
                and vars.mode == "NamaPass"
                and namapass_trentila_reward.isCountdownDone
            ):
                if not namapass_trentila_reward.isCollected:
                    namapass_trentila_reward.buy()
                    tiger_fruit.isBought = True
            if (
                namapass_ospuze_reward.rect.collidepoint(event.pos)
                and vars.mode == "NamaPass"
                and namapass_ospuze_reward.isCountdownDone
            ):
                if not namapass_ospuze_reward.isCollected:
                    namapass_ospuze_reward.buy()
                    energy_drink.isBought = True
            if (
                namapass_minigun_reward.rect.collidepoint(event.pos)
                and vars.mode == "NamaPass"
                and namapass_minigun_reward.isCountdownDone
            ):
                if not namapass_minigun_reward.isCollected:
                    namapass_minigun_reward.buy()
                    minigun.isBought = True

            #покупка
            if (
                button_buy_bear.rect.collidepoint(event.pos)
                and vars.mode == "teddy_bear_preview"
                and not teddy_bear.isBought
            ):
                teddy_bear.buy()

            if (
                button_buy_beluash.rect.collidepoint(event.pos)
                and vars.mode == "beluash_preview"
                and not beluash.isBought
            ):
                beluash.buy()

            if (
                button_buy_contestant.rect.collidepoint(event.pos)
                and vars.mode == "contestant_preview"
                and not contestant.isBought
            ):
                contestant.buy()

            # магазин - isPreview
            if (
                teddy_bear.rect.collidepoint(event.pos)
                and vars.mode == "shop"
            ):
                load_mode("teddy_bear_preview")
            if (
                beluash.rect.collidepoint(event.pos)
                and vars.mode == "shop"
            ):
                load_mode("beluash_preview")
            if (
                energy_drink.rect.collidepoint(event.pos)
                and vars.mode == "shop"
            ):
                load_mode("energy_drink_preview")
            if (
                tiger_fruit.rect.collidepoint(event.pos)
                and vars.mode == "shop"
            ):
                load_mode("tiger_fruit_preview")
            if (
                minigun.rect.collidepoint(event.pos)
                and vars.mode == "shop"
            ):
                load_mode("minigun_preview")
            if (
                contestant.rect.collidepoint(event.pos)
                and vars.mode == "shop" 
            ):
                load_mode("contestant_preview")
            if (
                button_to_sponsors_from_NamaPass.rect.collidepoint(event.pos)
                and vars.mode == "NamaPass"
            ):
                load_mode("sponsors_choice")
            if (
                button_back_from_sponsors_choice.rect.collidepoint(event.pos)
                and vars.mode == "sponsors_choice"
            ):
                load_mode("NamaPass")
            if (
                trentila_button.rect.collidepoint(event.pos)
                and vars.mode == "sponsors_choice"
            ):
                load_mode("trentila_sponsor_quote")
            if (
                ospuze_button.rect.collidepoint(event.pos)
                and vars.mode == "sponsors_choice"
            ):
                load_mode("ospuze_sponsor_quote")
            if (
                alfa_acta_button.rect.collidepoint(event.pos)
                and vars.mode == "sponsors_choice"
            ):
                load_mode("alfa_acta_sponsor_quote")
            if (
                vaiiya_button.rect.collidepoint(event.pos)
                and vars.mode == "sponsors_choice"
            ):
                load_mode("vaiiya_sponsor_quote")
            

            if (
                back_button_from_preview.rect.collidepoint(event.pos)
                and vars.mode in ["teddy_bear_preview", "beluash_preview", 
                        "energy_drink_preview", "tiger_fruit_preview",
                            "minigun_preview", "contestant_preview"]
                ):
                load_mode("shop")

            if (
                button_back_from_sponsors_quotes.rect.collidepoint(event.pos)
                and vars.mode in ["ospuze_sponsor_quote", "trentila_sponsor_quote", 
                        "alfa_acta_sponsor_quote", "vaiiya_sponsor_quote"]
                ):
                load_mode("sponsors_choice")
            
            if (
                button_back_from_backgrounds_shop.rect.collidepoint(event.pos)
                and vars.mode == "backgrounds_shop"
            ):
                load_mode("game")

            #buff machine
            if (
                button_machine.rect.collidepoint(event.pos)
                and vars.mode == "game"
            ):
                if buffm_intermission_timer.done():
                    buffm.shuffle()
                    buffm.apply_instant_effects(vars.__dict__)
                    buffm_intermission_timer.reset()
                    inserted_coin.play()
            #ФОНЫ
            if (
                button_to_backgrounds_shop.rect.collidepoint(event.pos)
                and vars.mode == "game"
            ):
                load_mode("backgrounds_shop")
            
            if (seoul_bg.button_rect.collidepoint(event.pos) and vars.mode == "backgrounds_shop"):
                if not seoul_bg.isBought:
                    seoul_bg.buy()
                else:
                    bernal_bg.equipped = False
                    kyoto_bg.equipped = False
                    seoul_bg.equip()

            if (kyoto_bg.button_rect.collidepoint(event.pos) and vars.mode == "backgrounds_shop"):
                if not kyoto_bg.isBought:
                    kyoto_bg.buy()
                else:
                    bernal_bg.equipped = False
                    seoul_bg.equipped = False
                    kyoto_bg.equip()
                
            if (bernal_bg.button_rect.collidepoint(event.pos) and vars.mode == "backgrounds_shop"):
                if not bernal_bg.isBought:
                    bernal_bg.buy()
                else:
                    seoul_bg.equipped = False
                    kyoto_bg.equipped = False
                    bernal_bg.equip()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and vars.mode == "game":
                add_clicks()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a] and vars.mode == "minigame":
        namaPlayer.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d] and vars.mode == "minigame":
        namaPlayer.x += 5
    if keys[pygame.K_UP] or keys[pygame.K_w] and vars.mode == "minigame":
        namaPlayer.y -= 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s] and vars.mode == "minigame":
        namaPlayer.y += 5

    namaPlayer.x = max(0, min(1000 - namaPlayer.rect.width, namaPlayer.x))
    namaPlayer.y = max(0, min(800 - namaPlayer.rect.height, namaPlayer.y))

    if namapass_5min_timer.done() and not vars.notif_5_shown:
        vars.notif_5_shown = True
        nofitication_sound.play()
        TriggerNotification()
    if namapass_10min_timer.done() and not vars.notif_10_shown:
        vars.notif_10_shown = True
        nofitication_sound.play()
        TriggerNotification()
    if namapass_15min_timer.done() and not vars.notif_15_shown:
        vars.notif_15_shown = True
        nofitication_sound.play()
        TriggerNotification()
    if namapass_20min_timer.done() and not vars.notif_20_shown:
        vars.notif_20_shown = True
        nofitication_sound.play()
        TriggerNotification()
    if namapass_25min_timer.done() and not vars.notif_25_shown:
        vars.notif_25_shown = True
        nofitication_sound.play()
        TriggerNotification()
    if namapass_30min_timer.done() and not vars.notif_30_shown:
        vars.notif_30_shown = True
        nofitication_sound.play()
        TriggerNotification()

    had_active_timed_effect = (
        buffm.active_effect_id is not None and buffm.active_effect_timer is not None
    )
    buffm.update_timed_effects(vars.__dict__)
    if had_active_timed_effect and buffm.active_effect_id is None:
        vars.show_buff_effect_end_notice = True
        buff_effect_end_notice_timer.reset()
    if vars.show_buff_effect_end_notice and buff_effect_end_notice_timer.done():
        vars.show_buff_effect_end_notice = False

    # DRAW MODE
    if vars.mode == "game":
        screen.fill(GREY)

        if seoul_bg.equipped:
            screen.blit(seoul_bg.bg_image, (0, 0))
        if kyoto_bg.equipped:
            screen.blit(kyoto_bg.bg_image, (0, 0))
        if bernal_bg.equipped:
            screen.blit(bernal_bg.bg_image, (0, 0))

        button_boost.draw(screen)

        button_to_shelf_from_game.draw(screen)

        button_to_backgrounds_shop.draw(screen)
        screen.blit(
            font_30.render("Фоны", True, BLACK),
            (button_to_backgrounds_shop.x + 52.5, button_to_backgrounds_shop.y + 12)
        )

        banner.change_banner()
        banner.update()
        banner.draw(screen)

        ShowNofitication(screen)
        
        #Buff Machine:
        screen.blit(buff_machine_image, (BUFF_MACHINE_X, BUFF_MACHINE_Y))

        if buffm_intermission_timer.done():
            machine_timer_text = "Таймер: готово"
        else:
            machine_timer_text = f"Таймер: {buffm_intermission_timer.time_format()}"
        screen.blit(
            font_25.render(machine_timer_text, True, WHITE),
            (button_machine.x + 15, BUFF_MACHINE_Y + buff_machine_image.get_height() + 8)
        )

        button_machine.draw(screen)
        screen.blit(
            font_25.render("INSERT COIN", True, BLACK),
            (button_machine.x + 22, button_machine.y + 15)
        )

        effect_color = WHITE
        effect_title = "Эффект:"
        effect_text = buffm.last_result_text if buffm.last_result_text else "Пока нет эффекта"

        current_effect_kind = buffm.last_effect_kind
        if buffm.active_effect_id is not None:
            _, current_effect_kind, _, _, _, _ = buffm.EFFECTS[buffm.active_effect_id]

        if current_effect_kind == "buff":
            effect_color = (140, 255, 140)
            effect_title = "Бафф:"
        elif current_effect_kind == "debuff":
            effect_color = (255, 140, 140)
            effect_title = "Дебафф:"

        effect_y = button_machine.y + 70
        screen.blit(font_25.render(effect_title, True, effect_color), (BUFF_MACHINE_TEXT_X, effect_y))
        if vars.show_buff_effect_end_notice:
            screen.blit(
                font_20.render("Эффект кончился", True, (255, 245, 140)),
                (BUFF_MACHINE_TEXT_X + 112, effect_y + 4)
            )
        effect_y += 24
        effect_y = draw_wrapped_text(
            screen,
            effect_text,
            font_20,
            WHITE,
            BUFF_MACHINE_TEXT_X,
            effect_y,
            BUFF_MACHINE_TEXT_W,
            20
        )

        if buffm.active_effect_id is not None and buffm.active_effect_timer is not None:
            screen.blit(
                font_20.render(f"До конца: {buffm.active_effect_timer.time_format()}", True, effect_color),
                (BUFF_MACHINE_TEXT_X, effect_y + 8)
            )

        button_to_minigame_from_game.draw(screen)
        screen.blit(
            font_30.render("Полка", True, BLACK),
            (850, 730)
        ) 
        screen.blit(
            font_25.render("Зелёное поле", True, BLACK),
            (button_to_minigame_from_game.x + 16, button_to_minigame_from_game.y + 15)
        )
        if vars.total_clicks < 1000 and not vars.isReached1000clicks:
            screen.blit(
                locked_button_gfield,
                (button_to_minigame_from_game.x, button_to_minigame_from_game.y)
            )
        
        if vars.boost >= 50:
            screen.blit(
            font_30.render("Буст: Макс.", True, BLACK),
            (55, 650)
        )
        else:
            screen.blit(
                font_30.render(f"Буст: x{vars.boost + 1}", True, BLACK),
                (55, 650)
            )

        screen.blit(
            font_25.render(f"Цена: {int(vars.required_clicks_for_boost)}", True, BLACK),
            (56, 676)
        )
        button_to_menu_from_game.draw(screen)
        screen.blit(
            font_30.render("Меню", True, BLACK),
            (button_to_menu_from_game.x + 52.5, button_to_menu_from_game.y + 10.5),
        )
        vars.tama_on_screen.update()
        vars.tama_on_screen.draw(screen)
        if vars.tama_on_screen.name == "glitch" and not cfa_IT.unlocked:
            cfa_IT.unlocked = True
            cfa_IT.show_popup = True
            cfa_IT.timer.reset()
            glitch_sound.play()
        if vars.tama_on_screen.name == "sanic" and not cfa_sanic_popout.unlocked:
            cfa_sanic_popout.unlocked = True
            cfa_sanic_popout.show_popup = True
            cfa_sanic_popout.timer.reset()
            sanic_sound.play()
        if vars.show_boost and vars.mode == "game":
            shake_x = random.randint(-2, 2)
            shake_y = random.randint(-2, 2)
            boost_pos_shaken = (vars.boost_pos[0] + shake_x, vars.boost_pos[1] + shake_y)
            screen.blit(
                font_30.render(f"+{vars.boost}", True, WHITE),
                boost_pos_shaken,
            )
            if clicking_text_timer.done() and vars.mode == "game":
                vars.show_boost = False
        if vars.show_intro_game_text:
            screen.blit(
                font_25.render("Namatama меняется каждый клик", True, WHITE),
                (300, 700),
            )
        if vars.total_clicks >= 1000 and not cfa_1000_clicks.unlocked:
            cfa_1000_clicks.unlocked = True
            cfa_1000_clicks.show_popup = True
            cfa_1000_clicks.timer.reset()
        if vars.total_clicks >= 10000 and not cfa_10000_clicks.unlocked:
            cfa_10000_clicks.unlocked = True
            cfa_10000_clicks.show_popup = True
            cfa_1000_clicks.timer.reset()   
        if vars.total_clicks >= 100000 and not cfa_1000000_clicks.unlocked:
            cfa_1000000_clicks.unlocked = True
            cfa_1000000_clicks.show_popup = True
            cfa_1000_clicks.timer.reset()
                
        cfa_1000_clicks.pop_out(screen)
        cfa_10000_clicks.pop_out(screen)
        cfa_1000000_clicks.pop_out(screen)

        cfa_IT.pop_out(screen)
        cfa_sanic_popout.pop_out(screen)

    if vars.mode == "menu":
        screen.blit(menu_screen, (0, 0))
        button_to_achievements_from_menu.draw(screen)
        button_to_game_from_menu.draw(screen)
        button_to_settings_from_menu.draw(screen)
        screen.blit(
            font_30.render("Настройки", True, BLACK),
            (button_to_settings_from_menu.x + 20, button_to_settings_from_menu.y + 10),
        )
        screen.blit( 
            font_25.render("Достижения", True, BLACK),
            (button_to_game_from_menu.x + 18, button_to_game_from_menu.y + 85.5),
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
    if vars.mode == "achievements":
        screen.blit(achievements_bg_ru, (0, 0)) 
        achievements_back_button.draw(screen)
        cfa_collect_all_tamas.draw(screen)
        cfa_sanic_popout.draw(screen)
        cfa_IT.draw(screen)
        cfa_1000_clicks.draw(screen)
        cfa_10000_clicks.draw(screen)
        cfa_1000000_clicks.draw(screen)
        draw_button_text(
            screen,
            "Нажмите чтобы вернуться в Меню",
            font_25,
            BLACK,
            achievements_back_button,
            (12, 14),
        )
    if vars.mode == "credits":
        screen.blit(credits_bg_ru, (0, 0))
        credits_back_button.draw(screen)
        draw_button_text(
            screen,
            "Нажмите чтобы вернуться в Меню",
            font_25,
            BLACK,
            credits_back_button,
            (15, 14),
        )
    if vars.mode == "settings":
        screen.blit(settings_bg, (0, 0))
        settings_back_button.draw(screen)
        screen.blit(volume_icon, (420 + 20, 57))
        screen.blit(volume_icon, (400 + 20, 218))
        draw_button_text(
            screen,
            "Нажмите чтобы вернуться в Меню",
            font_25,
            BLACK,
            settings_back_button,
            (16, 14),
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
    if vars.mode == "minigame" and vars.isTutorialWatched:
        screen.blit(field_bg, (0, 0))
        button_back_from_minigame.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_minigame.x + 52.5, button_back_from_minigame.y + 10.5),)
        )
        namaPlayer.draw(screen)

        for coin in coins:
            coin.draw(screen)

        if coin_spawn_timer.done() and len(coins) < MAX_COINS:
            if random.random() < 0.2:
                    coins.append(BoostCoin())
            else:
                coins.append(Coin())
            coin_spawn_timer.reset()

        for coin in coins[:]:
            if namaPlayer.rect.colliderect(coin.rect):
                coins.remove(coin)

                if isinstance(coin, BoostCoin):
                    vars.boost_coin = 2
                    vars.coin_boost_active = True
                    coin_boost_timer.reset()
                else:
                    farm_mult = buffm.get_farm_coin_multiplier() if buffm else 1
                    vars.NamaCoins += 1 * vars.boost_coin * farm_mult

                coins_collecting.play()

    if vars.coin_boost_active and coin_boost_timer.done():
        vars.boost_coin = 1
        vars.coin_boost_active = False
    
    if vars.mode == "shelf":
        screen.blit(shelf_bg, (0, 0))
        button_back_from_shelf.draw(screen)
        button_to_shop_from_shelf.draw(screen)
        
        if teddy_bear.isBought:
            teddy_bear.draw(screen)
        
        if beluash.isBought:
            beluash.draw(screen)

        if contestant.isBought:
            contestant.draw(screen)

        if tiger_fruit.isBought:
            tiger_fruit.draw(screen)
        
        if energy_drink.isBought:
            energy_drink.draw(screen)
        
        if minigun.isBought:
            minigun.draw(screen)

        screen.blit(
            font_30.render("В магазин", True, BLACK),
            ((button_to_shop_from_shelf.x + 20.5, button_to_shop_from_shelf.y + 10.5),)
        )
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_shelf.x + 52.5, button_back_from_shelf.y + 10.5),)
        )
        
    if vars.mode == "shop":
        screen.blit(shop_bg, (0, 0))
        button_back_from_shop.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            (button_back_from_shop.x + 52.5, button_back_from_shop.y + 10.5)
        )
        if vars.isReached1000clicks:
            button_exchanging.draw(screen)
            screen.blit(
                font_30.render("Обменник", True, BLACK),
                (button_exchanging.x + 25, button_exchanging.y + 10.5)
            )
        else:
            screen.blit(locked_exchange_button, (button_exchanging.x, button_exchanging.y))
        beluash.draw(screen)
        energy_drink.draw(screen)
        minigun.draw(screen)
        contestant.draw(screen)
        tiger_fruit.draw(screen)
        teddy_bear.draw(screen)
    
    if vars.mode == "teddy_bear_preview":
        screen.blit(teddy_bear_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
        if not teddy_bear.isBought:
            button_buy_bear.draw(screen) 
            screen.blit(
                font_30.render("Купить", True, BLACK),
                ((button_buy_bear.x + 45, button_buy_bear.y + 10.5),)
            )
    if vars.mode == "beluash_preview":
        screen.blit(beluash_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
        if not beluash.isBought:
            button_buy_beluash.draw(screen)
            screen.blit(
                font_30.render("Купить", True, BLACK),
                ((button_buy_beluash.x + 45, button_buy_beluash.y + 10.5),)
            )
        
    if vars.mode == "contestant_preview":
        screen.blit(contestant_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
        if not contestant.isBought:
            button_buy_contestant.draw(screen)
            screen.blit(
                font_30.render("Купить", True, BLACK),
                ((button_buy_contestant.x + 45, button_buy_contestant.y + 10.5),)
            )

    if vars.mode == "energy_drink_preview":
        screen.blit(energy_drink_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
    
    if vars.mode == "tiger_fruit_preview":
        screen.blit(tiger_fruit_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
    
    if vars.mode == "minigun_preview":
        screen.blit(minigun_preview, (0, 0))
        back_button_from_preview.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((back_button_from_preview.x + 52.5, back_button_from_preview.y + 10.5),)
        )
    
    if vars.mode == "NamaPass":
        screen.blit(namapass_bg, (0, 0))
        button_back_from_battle_pass.draw(screen)
        button_to_sponsors_from_NamaPass.draw(screen)
        screen.blit(
            font_30.render("Спонсоры", True, BLACK),
            ((button_to_sponsors_from_NamaPass.x + 30, button_to_sponsors_from_NamaPass.y + 10.5),)
        )
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_battle_pass.x + 52.5, button_back_from_battle_pass.y + 10.5),)
        )

        if namapass_5min_timer.done():
            namapass_100_coins.isCountdownDone = True
            namapass_100_coins.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_5min_timer.time_format()}", True, WHITE),
                (198 - 12, 472)
            )
        if namapass_100_coins.isCollected:
            screen.blit(namapass_100_coins.collected_item, namapass_100_coins.rect)

        if namapass_10min_timer.done():
            namapass_200_coins.isCountdownDone = True
            namapass_200_coins.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_10min_timer.time_format()}", True, WHITE),
                (490 - 12, 472)
            )
        if namapass_200_coins.isCollected:
            screen.blit(namapass_200_coins.collected_item, namapass_200_coins.rect)

        if namapass_15min_timer.done():
            namapass_500_coins.isCountdownDone = True
            namapass_500_coins.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_15min_timer.time_format()}", True, WHITE),
                (782 - 12, 472)
            )
        if namapass_500_coins.isCollected:
            screen.blit(namapass_500_coins.collected_item, namapass_500_coins.rect)

        if namapass_20min_timer.done():
            namapass_trentila_reward.isCountdownDone = True
            namapass_trentila_reward.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_20min_timer.time_format()}", True, WHITE),
                (782 - 12, 204)
            )
        if namapass_trentila_reward.isCollected:
            screen.blit(
                namapass_trentila_reward.collected_item,
                namapass_trentila_reward.rect
            )

        if namapass_25min_timer.done():
            namapass_ospuze_reward.isCountdownDone = True
            namapass_ospuze_reward.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_25min_timer.time_format()}", True, WHITE),
                (489 - 12, 204)
            )
        if namapass_ospuze_reward.isCollected:
            screen.blit(
                namapass_ospuze_reward.collected_item,
                namapass_ospuze_reward.rect
            )

        if namapass_30min_timer.done():
            namapass_minigun_reward.isCountdownDone = True
            namapass_minigun_reward.draw(screen)
        else:
            screen.blit(
                font_25.render(f"{namapass_30min_timer.time_format()}", True, WHITE),
                (195 - 12, 204)
            )
        if namapass_minigun_reward.isCollected:
            screen.blit(
                namapass_minigun_reward.collected_item,
                namapass_minigun_reward.rect
            )
            
    if vars.mode == "sponsors_choice":
        screen.fill(GREY)
        button_back_from_sponsors_choice.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_sponsors_choice.x + 52.5, button_back_from_sponsors_choice.y + 10.5),)
        )

        trentila_button.draw(screen)
        ospuze_button.draw(screen)
        alfa_acta_button.draw(screen)
        vaiiya_button.draw(screen)

    #sponsors_quotes
    if vars.mode == "trentila_sponsor_quote":
        screen.fill(GREY)
        button_back_from_sponsors_quotes.draw(screen)
        screen.blit(trentila_quote, (50, 65))
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_sponsors_quotes.x + 52.5, button_back_from_sponsors_quotes.y + 10.5),)
        )
    
    if vars.mode == "ospuze_sponsor_quote":
        screen.fill(GREY)
        button_back_from_sponsors_quotes.draw(screen)
        screen.blit(ospuze_quote, (50, 65))
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_sponsors_quotes.x + 52.5, button_back_from_sponsors_quotes.y + 10.5),)
        )
    
    if vars.mode == "alfa_acta_sponsor_quote":
        screen.fill(GREY)
        button_back_from_sponsors_quotes.draw(screen)
        screen.blit(alfa_acta_quote, (50, 65))
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_sponsors_quotes.x + 52.5, button_back_from_sponsors_quotes.y + 10.5),)
        )
    
    if vars.mode == "vaiiya_sponsor_quote":
        screen.fill(GREY)
        button_back_from_sponsors_quotes.draw(screen)
        screen.blit(vaiiya_quote, (50, 65))
        screen.blit(
            font_30.render("Назад", True, BLACK),
            ((button_back_from_sponsors_quotes.x + 52.5, button_back_from_sponsors_quotes.y + 10.5),)
        )
    if not vars.isTutorialWatched and vars.mode == "tutorial_gfield":
        screen.blit(tutorial_gfield, (0, 0))
        button_got_it.draw(screen)
        screen.blit(
            font_30.render("Понятно", True, BLACK),
            ((button_got_it.x + 42.5, button_got_it.y + 10.5),)
        )

    if vars.mode == "exchanger":
        screen.blit(exchanger_bg, (0, 0))
        button_exchanging_back_to_shop.draw(screen)
        button_exchange_to_coins.draw(screen)
        button_exchange_to_clicks.draw(screen)

        screen.blit(
            font_30.render("Назад", True, BLACK),
            (button_exchanging_back_to_shop.x + 52.5, button_exchanging_back_to_shop.y + 10.5)
        )
        screen.blit(
            font_40.render("Клики → NamaCoins", True, BLACK),
            (320, 230)
        )
        screen.blit(
            font_40.render("NamaCoins → Клики", True, BLACK),
            (320, 400)
        )
        screen.blit(
            font_30.render("Обменять", True, BLACK),
            (button_exchange_to_coins.x + 25, button_exchange_to_coins.y + 10.5)
        )
        screen.blit(
            font_30.render("Обменять", True, BLACK),
            (button_exchange_to_clicks.x + 25, button_exchange_to_clicks.y + 10.5)
        )

    if vars.mode == "backgrounds_shop":
        screen.fill(GREY)
        button_back_from_backgrounds_shop.draw(screen)
        screen.blit(
            font_30.render("Назад", True, BLACK),
            (button_back_from_backgrounds_shop.x + 52.5, button_back_from_backgrounds_shop.y + 10.5)
        )
        seoul_bg.draw_button(screen)
        if seoul_bg.isBought:
            status_text_seoul = "Надеть" if not seoul_bg.equipped else "Надет"
            screen.blit(
                font_25.render(f"Куплено. {status_text_seoul}", True, BLACK),
                (seoul_bg.button_rect.x, seoul_bg.button_rect.bottom + 10)
            )
        else:
            screen.blit(
                font_25.render(f"Цена: {seoul_bg.price} NamaCoins", True, BLACK),
                (seoul_bg.button_rect.x, seoul_bg.button_rect.bottom + 10)
            )

        kyoto_bg.draw_button(screen)
        if kyoto_bg.isBought:
            status_text_kyoto = "Надеть" if not kyoto_bg.equipped else "Надет"
            screen.blit(
                font_25.render(f"Куплено. {status_text_kyoto}", True, BLACK),
                (kyoto_bg.button_rect.x, kyoto_bg.button_rect.bottom + 10)
            )
        else:
            screen.blit(
                font_25.render(f"Цена: {kyoto_bg.price} NamaCoins", True, BLACK),
                (kyoto_bg.button_rect.x, kyoto_bg.button_rect.bottom + 10)
            )

        bernal_bg.draw_button(screen)
        if bernal_bg.isBought:
            status_text_bernal = "Надеть" if not bernal_bg.equipped else "Надет"
            screen.blit(
                font_25.render(f"Куплено. {status_text_bernal}", True, BLACK),
                (bernal_bg.button_rect.x, bernal_bg.button_rect.bottom + 10)
            )
        else:
            screen.blit(
                font_25.render(f"Цена: {bernal_bg.price} NamaCoins", True, BLACK),
                (bernal_bg.button_rect.x, bernal_bg.button_rect.bottom + 10)
            )

    for pop in song_popouts.values():
        pop.update()
        pop.draw(screen)

    # Загрузка
    if vars.isLoading:
        screen.fill(GREY)
        if vars.cooldown_timer.done():
            mouse_click_sound.play()
            vars.mode = vars.next_mode
            vars.isLoading = False
    
    if vars.total_clicks != vars.last_total_clicks_for_shake:
        vars.last_total_clicks_for_shake = vars.total_clicks
        clicks_shake_timer.reset()

    if vars.NamaCoins != vars.last_nama_coins_for_shake:
        vars.last_nama_coins_for_shake = vars.NamaCoins
        nama_shake_timer.reset()

    if vars.total_clicks >= 1000:
        vars.isReached1000clicks = True

    if vars.total_clicks > 0:
        vars.show_intro_game_text = False

    if (
        vars.mode != "menu"
        and vars.mode != "credits"
        and vars.mode != "settings"
        and vars.mode != "achievements"
        and vars.mode != "NamaPass"
        and vars.mode != "tutorial_gfield"
    ):
        screen.blit(angle_frame, (776, 0))
        screen.blit(NamaCoin_image, (792, 0))
        screen.blit(click_image, (792, 47))

        coins_text = font_30.render(f": {vars.NamaCoins}", True, BLACK)
        if not nama_shake_timer.done():
            shake_x = random.randint(-1, 1)
            shake_y = random.randint(-1, 1)
            screen.blit(coins_text, (860 + shake_x, 13 + shake_y))
        else:
            screen.blit(coins_text, (860, 13))

        clicks_text = font_30.render(f": {int(vars.total_clicks)}", True, BLACK)
        if not clicks_shake_timer.done():
            shake_x = random.randint(-1, 1)
            shake_y = random.randint(-1, 1)
            screen.blit(clicks_text, (860 + shake_x, 60 + shake_y))
        else:
            screen.blit(clicks_text, (860, 60))

    save_system.maybe_autosave(vars.__dict__)
    pygame.display.flip()
    clock.tick(vars.FPS)

pygame.quit()