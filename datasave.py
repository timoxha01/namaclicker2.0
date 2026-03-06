import json
import os


class SaveSystem:
    def __init__(
        self,
        *,
        pygame,
        update_volume_cb,
        save_path: str,
        autosave_every_ms: int = 3000,
        save_version: int = 1,
    ) -> None:
        self.pygame = pygame
        self.update_volume_cb = update_volume_cb
        self.save_path = save_path
        self.autosave_every_ms = int(autosave_every_ms)
        self.save_version = int(save_version)
        self._last_autosave_at = 0

    def _safe_int(self, value, default=0) -> int:
        try:
            return int(value)
        except Exception:
            return int(default)

    def _safe_float(self, value, default=0.0) -> float:
        try:
            return float(value)
        except Exception:
            return float(default)

    def _timer_remaining_ms(self, timer) -> int:
        try:
            return int(timer.time_left())
        except Exception:
            return 0

    def _timer_set_remaining_ms(self, timer, remaining_ms: int) -> None:
        try:
            duration = int(timer.duration)
        except Exception:
            return

        remaining_ms = int(max(0, min(duration, int(remaining_ms))))
        now = self.pygame.time.get_ticks()
        elapsed_ms = duration - remaining_ms
        timer.start = now - int(elapsed_ms)

    def build_state(self, ctx: dict) -> dict:
        seen_tamas = ctx.get("seen_tamas", set())
        if isinstance(seen_tamas, set):
            seen_tamas_list = sorted(list(seen_tamas))
        elif isinstance(seen_tamas, list):
            seen_tamas_list = [str(x) for x in seen_tamas]
        else:
            seen_tamas_list = []

        def _b(name: str, attr: str) -> bool:
            obj = ctx.get(name)
            return bool(getattr(obj, attr, False)) if obj is not None else False

        def _u(name: str) -> bool:
            obj = ctx.get(name)
            return bool(getattr(obj, "unlocked", False)) if obj is not None else False

        def _c(name: str) -> bool:
            obj = ctx.get(name)
            return bool(getattr(obj, "isCollected", False)) if obj is not None else False

        def _t(name: str) -> int:
            timer = ctx.get(name)
            return self._timer_remaining_ms(timer) if timer is not None else 0

        course = ctx.get("course")
        course_coins = getattr(course, "course_coins", 0.0) if course is not None else 0.0
        course_clicks = getattr(course, "course_clicks", 0.0) if course is not None else 0.0

        return {
            "version": self.save_version,
            "settings": {
                "VOLUME": self._safe_float(ctx.get("VOLUME", 0.5), 0.5),
                "VOLUME_SDTRACK": self._safe_float(ctx.get("VOLUME_SDTRACK", 0.5), 0.5),
            },
            "progress": {
                "total_clicks": self._safe_int(ctx.get("total_clicks", 0), 0),
                "NamaCoins": self._safe_int(ctx.get("NamaCoins", 0), 0),
                "boost": self._safe_int(ctx.get("boost", 1), 1),
                "required_clicks_for_boost": self._safe_int(ctx.get("required_clicks_for_boost", 100), 100),
                "isReached1000clicks": bool(ctx.get("isReached1000clicks", False)),
                "isTutorialWatched": bool(ctx.get("isTutorialWatched", False)),
                "seen_tamas": seen_tamas_list,
            },
            "shop": {
                "teddy_bear": _b("teddy_bear", "isBought"),
                "beluash": _b("beluash", "isBought"),
                "contestant": _b("contestant", "isBought"),
                "energy_drink": _b("energy_drink", "isBought"),
                "tiger_fruit": _b("tiger_fruit", "isBought"),
                "minigun": _b("minigun", "isBought"),
            },
            "achievements": {
                "cfa_collect_all_tamas": _u("cfa_collect_all_tamas"),
                "cfa_sanic_popout": _u("cfa_sanic_popout"),
                "cfa_IT": _u("cfa_IT"),
                "cfa_1000_clicks": _u("cfa_1000_clicks"),
                "cfa_10000_clicks": _u("cfa_10000_clicks"),
                "cfa_1000000_clicks": _u("cfa_1000000_clicks"),
            },
            "namapass": {
                "collected": {
                    "namapass_100_coins": _c("namapass_100_coins"),
                    "namapass_200_coins": _c("namapass_200_coins"),
                    "namapass_500_coins": _c("namapass_500_coins"),
                    "namapass_trentila_reward": _c("namapass_trentila_reward"),
                    "namapass_ospuze_reward": _c("namapass_ospuze_reward"),
                    "namapass_minigun_reward": _c("namapass_minigun_reward"),
                },
                "timers_remaining_ms": {
                    "namapass_5min_timer": _t("namapass_5min_timer"),
                    "namapass_10min_timer": _t("namapass_10min_timer"),
                    "namapass_15min_timer": _t("namapass_15min_timer"),
                    "namapass_20min_timer": _t("namapass_20min_timer"),
                    "namapass_25min_timer": _t("namapass_25min_timer"),
                    "namapass_30min_timer": _t("namapass_30min_timer"),
                },
            },
            "exchange": {
                "course": {
                    "course_coins": self._safe_float(course_coins, 0.0),
                    "course_clicks": self._safe_float(course_clicks, 0.0),
                },
                "course_timer_remaining_ms": _t("course_timer"),
            },
            "ui_flags": {
                "notif_5_shown": bool(ctx.get("notif_5_shown", False)),
                "notif_10_shown": bool(ctx.get("notif_10_shown", False)),
                "notif_15_shown": bool(ctx.get("notif_15_shown", False)),
                "notif_20_shown": bool(ctx.get("notif_20_shown", False)),
                "notif_25_shown": bool(ctx.get("notif_25_shown", False)),
                "notif_30_shown": bool(ctx.get("notif_30_shown", False)),
            },
        }

    def apply_state(self, ctx: dict, data: dict) -> None:
        if not isinstance(data, dict):
            return

        settings = data.get("settings", {}) if isinstance(data.get("settings", {}), dict) else {}
        ctx["VOLUME"] = float(max(0.0, min(1.0, self._safe_float(settings.get("VOLUME", ctx.get("VOLUME", 0.5)), 0.5))))
        ctx["VOLUME_SDTRACK"] = float(
            max(0.0, min(1.0, self._safe_float(settings.get("VOLUME_SDTRACK", ctx.get("VOLUME_SDTRACK", 0.5)), 0.5)))
        )
        try:
            self.update_volume_cb()
        except Exception:
            pass

        progress = data.get("progress", {}) if isinstance(data.get("progress", {}), dict) else {}
        ctx["total_clicks"] = max(0, self._safe_int(progress.get("total_clicks", ctx.get("total_clicks", 0)), 0))
        ctx["NamaCoins"] = max(0, self._safe_int(progress.get("NamaCoins", ctx.get("NamaCoins", 0)), 0))
        ctx["boost"] = max(1, self._safe_int(progress.get("boost", ctx.get("boost", 1)), 1))
        ctx["required_clicks_for_boost"] = max(
            1,
            self._safe_int(
                progress.get("required_clicks_for_boost", ctx.get("required_clicks_for_boost", 100)),
                100,
            ),
        )
        ctx["isReached1000clicks"] = bool(progress.get("isReached1000clicks", ctx.get("isReached1000clicks", False)))
        ctx["isTutorialWatched"] = bool(progress.get("isTutorialWatched", ctx.get("isTutorialWatched", False)))

        saved_seen = progress.get("seen_tamas", [])
        if isinstance(saved_seen, list):
            ctx["seen_tamas"] = set(str(x) for x in saved_seen)

        shop = data.get("shop", {}) if isinstance(data.get("shop", {}), dict) else {}
        for key in ["teddy_bear", "beluash", "contestant", "energy_drink", "tiger_fruit", "minigun"]:
            obj = ctx.get(key)
            if obj is not None and hasattr(obj, "isBought"):
                setattr(obj, "isBought", bool(shop.get(key, getattr(obj, "isBought", False))))

        ach = data.get("achievements", {}) if isinstance(data.get("achievements", {}), dict) else {}
        for key in [
            "cfa_collect_all_tamas",
            "cfa_sanic_popout",
            "cfa_IT",
            "cfa_1000_clicks",
            "cfa_10000_clicks",
            "cfa_1000000_clicks",
        ]:
            obj = ctx.get(key)
            if obj is not None and hasattr(obj, "unlocked"):
                obj.unlocked = bool(ach.get(key, getattr(obj, "unlocked", False)))
                if hasattr(obj, "show_popup"):
                    obj.show_popup = False
                if hasattr(obj, "sound_played"):
                    obj.sound_played = False

        namapass = data.get("namapass", {}) if isinstance(data.get("namapass", {}), dict) else {}
        collected = namapass.get("collected", {}) if isinstance(namapass.get("collected", {}), dict) else {}
        for key in [
            "namapass_100_coins",
            "namapass_200_coins",
            "namapass_500_coins",
            "namapass_trentila_reward",
            "namapass_ospuze_reward",
            "namapass_minigun_reward",
        ]:
            obj = ctx.get(key)
            if obj is not None and hasattr(obj, "isCollected"):
                obj.isCollected = bool(collected.get(key, getattr(obj, "isCollected", False)))

        timers_remaining = namapass.get("timers_remaining_ms", {}) if isinstance(namapass.get("timers_remaining_ms", {}), dict) else {}
        for timer_key in [
            "namapass_5min_timer",
            "namapass_10min_timer",
            "namapass_15min_timer",
            "namapass_20min_timer",
            "namapass_25min_timer",
            "namapass_30min_timer",
        ]:
            timer = ctx.get(timer_key)
            if timer is not None:
                self._timer_set_remaining_ms(timer, self._safe_int(timers_remaining.get(timer_key, self._timer_remaining_ms(timer))))

        exchange = data.get("exchange", {}) if isinstance(data.get("exchange", {}), dict) else {}
        course_data = exchange.get("course", {}) if isinstance(exchange.get("course", {}), dict) else {}
        course = ctx.get("course")
        if course is not None:
            try:
                course.course_coins = self._safe_float(course_data.get("course_coins", getattr(course, "course_coins", 0.0)), 0.0)
                course.course_clicks = self._safe_float(course_data.get("course_clicks", getattr(course, "course_clicks", 0.0)), 0.0)
            except Exception:
                pass
        course_timer = ctx.get("course_timer")
        if course_timer is not None:
            self._timer_set_remaining_ms(course_timer, self._safe_int(exchange.get("course_timer_remaining_ms", self._timer_remaining_ms(course_timer))))

        ui_flags = data.get("ui_flags", {}) if isinstance(data.get("ui_flags", {}), dict) else {}
        for flag in ["notif_5_shown", "notif_10_shown", "notif_15_shown", "notif_20_shown", "notif_25_shown", "notif_30_shown"]:
            if flag in ui_flags:
                ctx[flag] = bool(ui_flags.get(flag, ctx.get(flag, False)))

    def load(self, ctx: dict) -> bool:
        if not os.path.exists(self.save_path):
            return False
        try:
            with open(self.save_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.apply_state(ctx, data)
            return True
        except Exception:
            return False

    def save(self, ctx: dict) -> bool:
        try:
            state = self.build_state(ctx)
            tmp_path = self.save_path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.save_path)
            return True
        except Exception:
            return False

    def maybe_autosave(self, ctx: dict) -> None:
        now = self.pygame.time.get_ticks()
        if now - self._last_autosave_at >= self.autosave_every_ms:
            self.save(ctx)
            self._last_autosave_at = now

