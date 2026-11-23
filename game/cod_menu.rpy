## ============================================================
##  cod_menu.rpy -- Menu utama yang berubah seiring Act.
##  Satu-satunya definisi screen main_menu di project ini.
##  Tombol: Start, Load, Settings, Exit.
## ============================================================


screen main_menu():
    tag menu
    $ act = persistent.act_reached
    $ bg_col = "#f3e3c3" if act <= 1 else ("#8a7f78" if act == 2 else "#1a1a1a")
    $ txt_col = "#3a2e22" if act <= 1 else ("#b5a89e" if act == 2 else "#6a6a6a")
    add Solid(bg_col)

    ## 4 anggota klub (Rian hilang setelah Act 1)
    if act <= 1:
        add Transform("rian normal", zoom=0.55) pos (260, 500)
    add Transform("luna " + ("normal" if act <= 1 else "glitch"), zoom=0.55) pos (520, 500)
    add Transform("kael " + ("normal" if act <= 1 else "glitch"), zoom=0.55) pos (780, 500)
    add Transform("aria " + ("happy" if act <= 1 else "glitch"), zoom=0.55) pos (1040, 500)

    text ("CODE: OVERWRITE" if act <= 1 else "{zalgo=3}CODE: OVERWRITE{/zalgo}"):
        xalign 0.5 ypos 60 size 90 color txt_col
        at (menu_jitter if act >= 2 else menu_still)

    vbox:
        xpos 1500 ypos 380 spacing 24
        at (menu_jitter if act >= 2 else menu_still)
        textbutton _("Start") action Start() text_size 60 text_color txt_col text_hover_color "#c2415d"
        textbutton _("Load") action ShowMenu("load") text_size 60 text_color txt_col text_hover_color "#c2415d"
        textbutton _("Settings") action ShowMenu("preferences") text_size 60 text_color txt_col text_hover_color "#c2415d"
        textbutton _("Exit") action Quit(confirm=False) text_size 60 text_color txt_col text_hover_color "#c2415d"

