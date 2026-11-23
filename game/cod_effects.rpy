## ============================================================
##  cod_effects.rpy  --  Efek glitch: ATL, Zalgo, Chromatic, dll.
## ============================================================

init -1 python:
    ZALGO_MARKS = [chr(c) for c in list(range(0x0300, 0x0315)) + list(range(0x0316, 0x0320))]

    def zalgo(text, level=3):
        rng = random.Random(text)   # seed = teks, supaya stabil tiap redraw
        out = []
        for ch in text:
            out.append(ch)
            if ch.strip():
                for _ in range(rng.randint(0, level)):
                    out.append(rng.choice(ZALGO_MARKS))
        return "".join(out)

    def zalgo_tag(tag, argument, contents):
        try:
            lvl = int(argument) if argument else 3
        except ValueError:
            lvl = 3
        new = []
        for kind, text in contents:
            if kind == renpy.TEXT_TEXT:
                text = zalgo(text, lvl)
            new.append((kind, text))
        return new

    config.custom_text_tags["zalgo"] = zalgo_tag   # pakai: {zalgo}teks{/zalgo}  atau {zalgo=5}

    def ChromaAberration(d, offset=5):
        """Tiga salinan R/G/B bergeser = chromatic aberration (butuh Ren'Py 8)."""
        return Fixed(
            Transform(d, matrixcolor=TintMatrix("#ff0000"), xoffset=-offset),
            Transform(d, matrixcolor=TintMatrix("#00ff00"), blend="add"),
            Transform(d, matrixcolor=TintMatrix("#0000ff"), xoffset=offset, blend="add"),
            fit_first=True)

image aria chroma = ChromaAberration("aria glitch")
image luna chroma = ChromaAberration("luna glitch")
image kael chroma = ChromaAberration("kael glitch")

# ---------- POSISI 4 SLOT ----------
transform slot1:
    xalign 0.08 yalign 1.0
transform slot2:
    xalign 0.36 yalign 1.0
transform slot3:
    xalign 0.64 yalign 1.0
transform slot4:
    xalign 0.92 yalign 1.0

# ---------- ATL GLITCH ----------
transform glitch_jitter:
    block:
        linear 0.04 xoffset 6
        linear 0.04 xoffset -8 yoffset 3
        linear 0.04 xoffset 0 yoffset 0
        pause 1.2
        linear 0.03 xoffset -14 alpha 0.7
        linear 0.03 xoffset 0 alpha 1.0
        pause 2.0
        repeat

transform uncanny:
    # sprite sedikit melar/menyusut = uncanny valley
    block:
        ease 2.5 xzoom 1.04 yzoom 0.97
        ease 2.5 xzoom 0.97 yzoom 1.04
        repeat

transform screen_shake(amp=14):
    # pakai: show layer master at screen_shake   |   hapus: show layer master
    block:
        linear 0.04 xoffset amp yoffset -amp
        linear 0.04 xoffset -amp yoffset amp
        linear 0.04 xoffset amp yoffset amp
        linear 0.04 xoffset -amp yoffset -amp
        repeat 6
    xoffset 0 yoffset 0

transform zoom_crop:
    # Crop/Zoom pada wajah saat adegan menegangkan
    xalign 0.5 yalign 0.0
    ease 1.5 zoom 1.8 yalign 0.1

transform menu_still:
    xoffset 0

transform menu_jitter:
    block:
        linear 0.05 xoffset 3
        linear 0.05 xoffset -3
        pause renpy.random.random() * 1.5 + 0.5
        repeat

transform text_flicker:
    block:
        alpha 1.0
        pause 1.3
        alpha 0.15
        pause 0.06
        alpha 1.0
        pause 0.9
        repeat

transform floaty(d=0.0, amp=8):
    pause d
    block:
        ease 2.0 yoffset -amp
        ease 2.0 yoffset amp
        repeat

# ---------- LAYAR CRASH / BOOT PALSU ----------
screen fake_terminal(lines, col="#ff3b3b", secs=4.0):
    modal True
    add Solid("#000000")
    vbox:
        xpos 80 ypos 70 spacing 6
        for l in lines:
            text esc(l) color col size 28 font code_font
    timer secs action Return()
