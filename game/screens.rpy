## ============================================================
##  screens.rpy -- Screen dasar (tanpa aset gui, pakai warna polos)
##  Screen main_menu ada di cod_menu.rpy
## ============================================================

init offset = -1

style default:
    font "DejaVuSans.ttf"
    size 36

## ---------- SAY ----------
screen say(who, what):
    style_prefix "say"
    window:
        id "window"
        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who"
        text what id "what"

style window:
    xfill True
    yalign 1.0
    ysize 300
    background Solid("#000000c0")

style namebox:
    xpos 280
    ypos -30
    xminimum 260
    padding (24, 8)
    background Solid("#222233")

style say_label:
    size 42
    bold True

style say_dialogue:
    xpos 300
    ypos 80
    xsize 1320
    size 38

## ---------- INPUT ----------
screen input(prompt):
    style_prefix "input"
    window:
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 30
            text prompt xalign 0.5
            input id "input" xalign 0.5

## ---------- CHOICE ----------
screen choice(items):
    style_prefix "choice"
    vbox:
        xalign 0.5
        yalign 0.45
        spacing 22
        for i in items:
            textbutton i.caption action i.action

style choice_button:
    xsize 1100
    padding (20, 16)
    background Solid("#222233dd")
    hover_background Solid("#c2415d")

style choice_button_text:
    xalign 0.5
    color "#ffffff"

## ---------- QUICK MENU ----------
default quick_menu = True

screen quick_menu():
    zorder 100
    if quick_menu:
        hbox:
            xalign 0.5
            yalign 0.995
            spacing 40
            textbutton _("Back") action Rollback() text_size 26
            textbutton _("Auto") action Preference("auto-forward", "toggle") text_size 26
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True) text_size 26
            textbutton _("Save") action ShowMenu("save") text_size 26
            textbutton _("Load") action ShowMenu("load") text_size 26
            textbutton _("Prefs") action ShowMenu("preferences") text_size 26

init python:
    config.overlay_screens.append("quick_menu")

## ---------- GAME MENU ----------
screen game_menu_base(title):
    tag menu
    add Solid("#101018")
    vbox:
        xpos 70
        ypos 120
        spacing 20
        textbutton _("Save") action ShowMenu("save")
        textbutton _("Load") action ShowMenu("load")
        textbutton _("Preferences") action ShowMenu("preferences")
        if not main_menu:
            textbutton _("Main Menu") action MainMenu()
        textbutton _("Return") action Return()
        textbutton _("Quit") action Quit(confirm=not main_menu)
    text title xpos 500 ypos 40 size 60
    frame:
        xpos 480
        ypos 150
        xsize 1360
        ysize 850
        background None
        transclude
    key "game_menu" action Return()

screen save():
    tag menu
    use file_slots(_("Save"))

screen load():
    tag menu
    use file_slots(_("Load"))

screen file_slots(title):
    use game_menu_base(title):
        vbox:
            spacing 24
            hbox:
                spacing 30
                textbutton _("<") action FilePagePrevious()
                text _("Page {}").format(FileCurrentPage())
                textbutton _(">") action FilePageNext()
            grid 3 2:
                spacing 24
                for i in range(1, 7):
                    $ slot = i
                    button:
                        xsize 430
                        ysize 260
                        background Solid("#1d2230")
                        hover_background Solid("#2d3550")
                        action FileAction(slot)
                        vbox:
                            add FileScreenshot(slot)
                            text FileTime(slot, format=_("{#file_time}%Y-%m-%d %H:%M"), empty=_("empty slot")) size 24

## ---------- PREFERENCES ----------
screen preferences():
    tag menu
    use game_menu_base(_("Preferences")):
        vbox:
            spacing 30
            hbox:
                spacing 40
                textbutton _("Window") action Preference("display", "window")
                textbutton _("Fullscreen") action Preference("display", "fullscreen")
            text _("Text speed")
            bar value Preference("text speed") xsize 700 ysize 26 left_bar Solid("#c2415d") right_bar Solid("#444455")
            text _("Music volume")
            bar value Preference("music volume") xsize 700 ysize 26 left_bar Solid("#c2415d") right_bar Solid("#444455")
            text _("Sound volume")
            bar value Preference("sound volume") xsize 700 ysize 26 left_bar Solid("#c2415d") right_bar Solid("#444455")
            textbutton _("Mute all") action Preference("all mute", "toggle")

## ---------- CONFIRM / NOTIFY / SKIP ----------
screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#000000b0")
    frame:
        xalign 0.5
        yalign 0.5
        padding (60, 50)
        background Solid("#1d2230")
        vbox:
            spacing 40
            text message xalign 0.5 text_align 0.5
            hbox:
                xalign 0.5
                spacing 120
                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action
    key "game_menu" action no_action

screen notify(message):
    zorder 100
    frame:
        xpos 40
        ypos 40
        padding (24, 12)
        background Solid("#000000c0")
        text message size 28
    timer 3.25 action Hide("notify")

screen skip_indicator():
    zorder 100
    text _("Skipping") xpos 40 ypos 40 size 28

init offset = 0
