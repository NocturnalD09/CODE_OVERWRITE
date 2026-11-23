## ============================================================
##  cod_meta.rpy  --  Source Code Recovery (Meta-File Minigame)
##
##  Memantau folder  game/characters/  di PC pemain memakai `os`.
##  Mode REAL      : pemain minimize gim & ubah file lewat File Explorer.
##  Mode SIMULASI  : (web / mobile / pemain tidak setuju) file palsu
##                   yang dikelola di dalam gim lewat tombol.
## ============================================================

default fs_real = False
default sim_files = {}

init -1 python:
    CHR_TEMPLATE = "[character]\nname={name}\nstatus={status}\nrole={role}\n"

    CHR_DATA = [
        ("aria.chr", "Aria", "active", "club_president"),
        ("luna.chr", "Luna", "active", "artist"),
        ("kael.chr", "Kael", "active", "sound_designer"),
        ("rian.chr", "Rian", "active", "programmer"),
    ]

    def fs_dir():
        return os.path.join(config.gamedir, "characters")

    def fs_setup(want_real=True):
        """Tentukan mode REAL / SIMULASI. Aman untuk web & mobile."""
        real = False
        if want_real and not (renpy.emscripten or renpy.mobile):
            try:
                if not os.path.isdir(fs_dir()):
                    os.makedirs(fs_dir())
                probe = os.path.join(fs_dir(), ".probe")
                with open(probe, "w") as f:
                    f.write("ok")
                os.remove(probe)
                real = True
            except Exception:
                real = False
        store.fs_real = real

    def fs_list():
        if store.fs_real:
            try:
                return sorted(n for n in os.listdir(fs_dir()) if not n.startswith("."))
            except Exception:
                return []
        return sorted(store.sim_files.keys())

    def fs_write(name, content):
        if store.fs_real:
            try:
                with open(os.path.join(fs_dir(), name), "w") as f:
                    f.write(content)
            except Exception:
                pass
        else:
            store.sim_files[name] = content

    def fs_read(name):
        if store.fs_real:
            try:
                with open(os.path.join(fs_dir(), name), "r") as f:
                    return f.read()
            except Exception:
                return ""
        return store.sim_files.get(name, "")

    def fs_delete(name):
        if store.fs_real:
            try:
                os.remove(os.path.join(fs_dir(), name))
            except Exception:
                pass
        else:
            store.sim_files.pop(name, None)

    def fs_rename(old, new):
        if store.fs_real:
            try:
                os.rename(os.path.join(fs_dir(), old), os.path.join(fs_dir(), new))
            except Exception:
                pass
        else:
            if old in store.sim_files:
                store.sim_files[new] = store.sim_files.pop(old)

    def fs_clear():
        for n in list(fs_list()):
            fs_delete(n)

    def fs_seed_characters():
        """Isi awal folder characters/ (Act 1)."""
        fs_clear()
        for fn, name, status, role in CHR_DATA:
            fs_write(fn, CHR_TEMPLATE.format(name=name, status=status, role=role))

    def fs_status(name):
        for line in fs_read(name).splitlines():
            if line.strip().lower().startswith("status="):
                return line.split("=", 1)[1].strip().lower()
        return ""

    def fs_set_status(name, status):
        text = fs_read(name)
        lines = []
        for line in text.splitlines():
            if line.strip().lower().startswith("status="):
                line = "status=" + status
            lines.append(line)
        fs_write(name, "\n".join(lines) + "\n")

    def fs_seed_act4():
        """Kondisi folder saat Act 4 dimulai."""
        fs_write("rian.chr.bak", "[fragment]\nname=Rian\nstatus=recovered\nnote=ganti ekstensi untuk memulihkan\n")
        fs_write("aria.chr", CHR_TEMPLATE.format(name="Aria", status="active", role="OVERRIDE"))
        fs_write("README_RECOVERY.txt", "Ekstensi adalah nama belakang sebuah berkas.\nMengubahnya mengubah cara sistem memperlakukan berkas itu.\n")

    def evaluate_ending():
        names = [n.lower() for n in fs_list()]
        rian_ok = "rian.chr" in names
        aria_any = [n for n in names if n.startswith("aria")]
        aria_deleted = len(aria_any) == 0
        if "aria.chr" in names:
            aria_isolated = fs_status("aria.chr") not in ("active", "")
        else:
            aria_isolated = not aria_deleted        # di-rename (mis. aria.bak)
        if aria_deleted:
            return "bittersweet"
        if aria_isolated and rian_ok:
            return "true"
        if aria_isolated:
            return "bittersweet"
        return "cyclic"

# ---------- LAYAR PEMULIHAN ----------
screen recovery_screen(show_extra_hint=False):
    modal True
    default hint = False
    timer 1.0 repeat True action Function(renpy.restart_interaction)

    add Solid("#0b0f14")
    frame:
        background Solid("#111a24")
        xalign 0.5 yalign 0.5 xsize 1500 ysize 900 padding (40, 30)
        vbox:
            spacing 14
            text "SOURCE CODE RECOVERY" size 52 color "#7fd18b" font code_font
            text "Folder: game/characters/" size 30 color "#9fb3c8" font code_font
            if fs_real:
                text "Minimize gim, buka File Explorer, lalu ubah isi folder ini secara langsung." size 28 color "#ffd166"
                textbutton "Buka folder" action OpenDirectory(fs_dir(), absolute=True) text_size 28 text_color "#ffffff" text_hover_color "#7fd18b"
            else:
                text "Mode simulasi: kelola file lewat tombol di bawah." size 28 color "#ffd166"

            null height 10
            for f in fs_list():
                hbox:
                    spacing 24
                    text esc(f) size 34 color ("#ff6b8b" if f.lower().startswith("aria") else "#ffffff") font code_font min_width 520
                    if not fs_real:
                        textbutton "[[Hapus]" action Function(fs_delete, f) text_size 28 text_color "#ff8080"
                        if f.lower().endswith(".chr"):
                            textbutton "[[ke .bak]" action Function(fs_rename, f, f[:-4] + ".bak") text_size 28 text_color "#9ad1ff"
                        if f.lower().endswith(".bak"):
                            textbutton "[[ke .chr]" action Function(fs_rename, f, f[:-4] + ".chr") text_size 28 text_color "#9ad1ff"
                        if f.lower() == "aria.chr":
                            textbutton "[[status=inactive]" action Function(fs_set_status, f, "inactive") text_size 28 text_color "#ffd166"

            null height 10
            if hint:
                text "Petunjuk: berkas yang dihapus tidak bisa kembali. Berkas yang hanya diganti ekstensinya masih bisa dipulihkan." size 26 color "#9fb3c8"
                if show_extra_hint:
                    text "Kenangan Rian: 'Isolasi itu bukan hapus. Ganti nama belakangnya, jangan buang isinya.'" size 26 color "#7fd18b"
            hbox:
                spacing 40
                textbutton "Petunjuk" action ToggleScreenVariable("hint") text_size 30 text_color "#ffffff" text_hover_color "#ffd166"
                textbutton "Selesai - jalankan ulang repositori" action Return("done") text_size 30 text_color "#ffffff" text_hover_color "#7fd18b"
