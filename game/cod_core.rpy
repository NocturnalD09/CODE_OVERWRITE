## ============================================================
##  CODE: OVERWRITE  --  cod_core.rpy
##  Karakter, gambar placeholder, audio helper, variabel global.
##  Target: Ren'Py 8.x (Python 3)
## ============================================================

init -3 python:
    import os
    import random
    import getpass

    def esc(s):
        """Escape [ dan { supaya aman dipakai di text Ren'Py."""
        return s.replace("[", "[[]]") .replace("{}", "{{}}")

init -2 python:
    # ---------- AUDIO (aman walau file belum ada) ----------
    def play_bgm(name, fadein=1.0):
        path = "audio/%s.ogg" % name
        if renpy.loadable(path):
            renpy.music.play(path, channel="music", loop=True, fadein=fadein)
        else:
            renpy.music.stop(channel="music", fadeout=0.5)

    def stop_bgm(fadeout=0.0):
        renpy.music.stop(channel="music", fadeout=fadeout)

    def play_sfx(name):
        path = "audio/%s.ogg" % name
        if renpy.loadable(path):
            renpy.sound.play(path)

    def type_callback(event, interact=True, **kwargs):
        """Typewriter sound pada dialog."""
        if not interact:
            return
        if event == "show" and renpy.loadable("audio/sfx_type.ogg"):
            renpy.music.play("audio/sfx_type.ogg", channel="sound", loop=True)
        elif event in ("slow_done", "end"):
            renpy.music.stop(channel="sound")

    # ---------- KUNCI NAVIGASI (Act 3) ----------
    def lock_nav(flag):
        """flag=True  -> matikan Save/Load/Skip/Rollback/Menu.
           flag=False -> kembalikan seperti semula."""
        if flag:
            if not getattr(store, "nav_locked", False):
                store._saved_game_menu = getattr(store, "_game_menu_screen", "save")
            store.nav_locked = True
            store._game_menu_screen = None
            store.quick_menu = False
            store._skipping = False
            config.allow_skipping = False
            config.rollback_enabled = False
            config.has_autosave = False
            config.has_quicksave = False
        else:
            if getattr(store, "nav_locked", False):
                store._game_menu_screen = getattr(store, "_saved_game_menu", "save")
            store.nav_locked = False
            store.quick_menu = True
            config.allow_skipping = True
            config.rollback_enabled = True
            config.has_autosave = True
            config.has_quicksave = True

    def get_os_user():
        try:
            return getpass.getuser()
        except Exception:
            return os.environ.get("USERNAME") or os.environ.get("USER") or "Player"

# ---------- DATA GLOBAL ----------
default persistent.act_reached = 1
default persistent.cycles = 0
default persistent.endings = set()

default player_name = "Mika"
default os_user = "Player"
default rian_bond = 0
default distortion = 0
default route = "rian"
default kw_score = {"rian": 0, "luna": 0, "kael": 0, "aria": 0}
default nav_locked = False

define code_font = "fonts/mono.ttf" if renpy.loadable("fonts/mono.ttf") else "DejaVuSans.ttf"

# ---------- KARAKTER ----------
define mc   = Character("[player_name]", color="#9ad1ff", callback=type_callback)
define rian = Character("Rian", color="#7fd18b", callback=type_callback)
define luna = Character("Luna", color="#c79bff", callback=type_callback)
define kael = Character("Kael", color="#ffcf6b", callback=type_callback)
define aria = Character("Aria", color="#ff6b8b", callback=type_callback)
define sysmsg = Character(None, what_color="#ff4040", what_font=code_font, callback=type_callback)

# ---------- TRANSISI ----------
define flash = Fade(0.1, 0.0, 0.4, color="#ffffff")
define crashcut = Fade(0.0, 0.0, 0.3, color="#000000")

# ---------- GAMBAR (otomatis pakai file asli bila ada di game/images/) ----------
# Sprite : images/rian normal.png, images/luna glitch.png, dst. (lihat images/README_IMAGES.txt)
# Latar  : images/bg classroom_day.png, dst.
# Kalau file belum ada, dipakai kotak placeholder berlabel.
init python:
    def _sprite(name, expr, color):
        return Fixed(
            Solid(color, xsize=360, ysize=720),
            Text("{size=44}%s{/size}\n{size=28}(%s){/size}" % (name, expr),
                 color="#ffffff", xalign=0.5, yalign=0.12, text_align=0.5),
            xsize=360, ysize=720)

    def _bg(color, label):
        return Fixed(Solid(color),
                     Text("BG: %s" % label, color="#00000066", size=36, xalign=0.5, yalign=0.03))

    def _use_file_or(name, fallback):
        path = "images/%s.png" % name
        if renpy.loadable(path):
            renpy.image(name, path)
        else:
            renpy.image(name, fallback)

    for _n, _c in (("rian", "#2e8b57"), ("luna", "#7b4fb8"),
                   ("kael", "#c58f1a"), ("aria", "#c2415d")):
        for _e in ("normal", "happy", "sad", "angry", "glitch"):
            _use_file_or("%s %s" % (_n, _e), _sprite(_n.capitalize(), _e, _c))

    _use_file_or("bg classroom_day", _bg("#e8d7ae", "ruang kelas sore"))
    _use_file_or("bg classroom_night", _bg("#1d2240", "ruang kelas malam"))
    _use_file_or("bg classroom_corrupt", _bg("#6e5f58", "kelas corrupted"))
    _use_file_or("bg void", Solid("#050505"))
    _use_file_or("bg black", Solid("#000000"))
    _use_file_or("luna_painting", Fixed(Solid("#a8d0e6"), Text("Lukisan Luna", color="#00000088", size=48, xalign=0.5, yalign=0.5), xsize=720, ysize=480))
    _use_file_or("luna_painting_pixel", Fixed(Solid("#400010"), Text("L U K I S A N", color="#ff0044", size=48, xalign=0.5, yalign=0.5), xsize=720, ysize=480))
