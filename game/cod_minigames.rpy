## ============================================================
##  cod_minigames.rpy
##  1) Debugging & Logic Quiz (malam)
##  2) Keyword Association (siang)
## ============================================================

init python:
    DEBUG_QUESTIONS = [
        {   # 0 - assignment vs comparison
            "title": "Level 1 - Assignment vs Comparison", "file": "skor.py",
            "code": ["skor = 10", "if skor = 10:", "    print(\"Sempurna!\")"], "bug": 2,
            "choices": ["if skor == 10:", "if skor = 10:", "if skor === 10:"], "answer": 0,
            "explain": "Satu tanda sama dengan itu assignment, memberi nilai. Untuk membandingkan, pakai dua tanda sama dengan."},
        {   # 1 - if/else syntax
            "title": "Level 2 - If / Else", "file": "nyawa.py",
            "code": ["nyawa = 0", "if nyawa > 0:", "    print(\"Lanjut main\")", "else", "    print(\"Game Over\")"], "bug": 4,
            "choices": ["else if:", "else:", "elseif:"], "answer": 1,
            "explain": "Blok else harus diakhiri titik dua, sama seperti if."},
        {   # 2 - loop indentation
            "title": "Level 3 - Looping", "file": "sapa.py",
            "code": ["for i in range(3):", "print(\"Halo klub!\")"], "bug": 2,
            "choices": ["print(\"Halo klub!\");", "    print(\"Halo klub!\")", "print(\"Halo klub!\") # ulang"], "answer": 1,
            "explain": "Isi loop harus menjorok. Di Python, indentasi adalah bagian dari sintaks."},
        {   # 3 - variable naming
            "title": "Level 4 - Variable", "file": "klub.py",
            "code": ["nama_klub = \"Code United\"", "print(nama klub)"], "bug": 2,
            "choices": ["print(nama-klub)", "print(nama_klub)", "print(\"nama klub\")"], "answer": 1,
            "explain": "Nama variabel tidak boleh mengandung spasi. Pakai garis bawah, dan tulis persis sama."},
        {   # 4 - infinite loop
            "title": "Level 5 - Loop Tak Berhingga", "file": "bertahan.py",
            "code": ["hp = 3", "while hp > 0:", "    print(\"Bertahan...\")"], "bug": 3,
            "choices": ["    hp += 1", "    hp -= 1", "    print(hp > 0)"], "answer": 1,
            "explain": "Kondisi loop harus bisa berubah menjadi False. Kurangi hp di dalam loop supaya berhenti."},
    ]

    KEYWORDS = {
        "rian": ["Variable", "Function", "Syntax", "Array", "Loop", "Debugging"],
        "luna": ["Canvas", "Palette", "Sprite", "Plot", "Branching", "Atmosphere"],
        "kael": ["Waveform", "Pitch", "Bitrate", "BGM", "Echo", "Sample"],
        "aria": ["Override", "Execute", "Memory", "Directory", "Root", "User"],
    }
    KEYWORD_OWNER = {}
    for _k, _ws in KEYWORDS.items():
        for _w in _ws:
            KEYWORD_OWNER[_w] = _k

    def build_word_layout():
        words = list(KEYWORD_OWNER.keys())
        random.shuffle(words)
        layout = []
        for i, w in enumerate(words):
            c, r = i % 6, i // 6
            x = 120 + c * 290 + random.randint(-40, 40)
            y = 230 + r * 170 + random.randint(-30, 30)
            layout.append((w, x, y, round(random.random() * 2, 2)))
        return layout

    def score_keywords(picked):
        res = {"rian": 0, "luna": 0, "kael": 0, "aria": 0}
        for w in picked:
            res[KEYWORD_OWNER[w]] += 1
        return res

    def pick_route(scores):
        best, best_v = "rian", -1
        for k in ("rian", "luna", "kael", "aria"):   # urutan = prioritas bila seri
            if scores[k] > best_v:
                best, best_v = k, scores[k]
        return best

    def code_line(s):
        return esc(s).replace("    ", "\u00a0\u00a0\u00a0\u00a0")

# ---------- SCREEN: DEBUGGING QUIZ ----------
screen debug_quiz(q, distortion=0):
    modal True
    add Solid("#1e1e2e")
    $ stability = max(0, 100 - distortion * 12)
    frame:
        background Solid("#11111b")
        xalign 0.5 yalign 0.5 xsize 1400 ysize 900 padding (40, 30)
        vbox:
            spacing 16
            hbox:
                spacing 30
                text "[[IDE]  %s" % q["file"] size 34 color "#89b4fa" font code_font
                text "Stabilitas program: %d%%" % stability size 30 font code_font color ("#a6e3a1" if stability > 60 else "#f38ba8")
            text q["title"] size 34 color "#f9e2af"
            null height 8
            for i, line in enumerate(q["code"], 1):
                hbox:
                    spacing 24
                    text "%02d" % i size 30 color "#6c7086" font code_font min_width 50
                    text code_line(line) size 32 font code_font color ("#f38ba8" if i == q["bug"] else "#cdd6f4")
            null height 6
            if distortion >= 3:
                text "{zalgo=4}ERROR: variable corrupted at 0x00FF{/zalgo}" size 28 color "#ff4040" at text_flicker
            text "Pilih perbaikan yang benar untuk baris yang ditandai:" size 30 color "#cdd6f4"
            for idx, c in enumerate(q["choices"]):
                textbutton code_line(c):
                    action [Function(play_sfx, "sfx_click"), Return(idx)]
                    text_font code_font text_size 32 text_color "#cdd6f4" text_hover_color "#a6e3a1"
                    background Solid("#1e1e2e") hover_background Solid("#313244")
                    padding (24, 12) xfill True

# ---------- SCREEN: KEYWORD ASSOCIATION ----------
screen keyword_pick(layout, corrupt=False):
    modal True
    default picked = []
    add Solid("#1b1f3a")
    text "Pilih 5 kata kunci yang menarik perhatianmu" xalign 0.5 ypos 60 size 48 color "#ffffff"
    for (w, x, y, d) in layout:
        textbutton esc(zalgo(w, 2) if (corrupt and len(w) % 3 == 0) else w):
            pos (x, y)
            at floaty(d)
            action [Function(play_sfx, "sfx_click"),
                    If(w in picked or len(picked) < 5, ToggleSetMembership(picked, w), NullAction())]
            background Solid("#2a2f55") selected_background Solid("#6b4fbb")
            text_color "#ffffff" text_selected_color "#ffd166" text_size 34
            padding (24, 12)
    textbutton "Konfirmasi (%d/5)" % len(picked):   
        xalign 0.5 ypos 960
        sensitive len(picked) == 5
        action Return(list(picked))
        text_size 42 text_color "#ffffff" text_insensitive_color "#555577" text_hover_color "#7fd18b"

# ---------- SCREEN: CURSOR DITARIK (Act 2 & 3) ----------
screen cursor_pull(x, y):
    timer 0.4 action Function(renpy.set_mouse_pos, x, y, 0.8)

# ---------- LABEL: DEBUG SESSION ----------
label debug_session(ids, act=1):
    $ qi = 0
    while qi < len(ids):
        $ q = DEBUG_QUESTIONS[ids[qi]]
        $ pick = renpy.call_screen("debug_quiz", q, distortion)
        $ explain = q["explain"]
        if pick == q["answer"]:
            $ rian_bond += 1
            $ play_sfx("sfx_click")
            if act == 1:
                rian happy "Tepat! [explain]"
            else:
                aria normal "Benar. [explain] Kamu belajar cepat... sayang bukan dari orang yang tepat."
        else:
            $ distortion += 1
            $ play_sfx("sfx_glitch")
            if act == 1:
                show rian glitch at slot1, glitch_jitter
                rian "Eh? Barusan nilai variabelnya berubah sendiri... Hmm. [explain]"
                show rian normal at slot1
            else:
                show aria glitch at slot4, glitch_jitter
                aria "Salah. Dan sistem mencatatnya. [explain]"
                show aria normal at slot4
        $ qi += 1
    return

# ---------- LABEL: KEYWORD SESSION ----------
label keyword_session(act=1):
    $ kw_layout = build_word_layout()
    if act == 2:
        $ renpy.show_screen("cursor_pull", 960, 600)
    $ picked_words = renpy.call_screen("keyword_pick", kw_layout, act >= 2)
    if act == 2:
        $ renpy.hide_screen("cursor_pull")
    python:
        res = score_keywords(picked_words)
        for k, v in res.items():
            kw_score[k] += v
        route = pick_route(kw_score)
    return
