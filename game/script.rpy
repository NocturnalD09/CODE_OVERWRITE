## ============================================================
##  CODE: OVERWRITE  --  script.rpy  (alur cerita Act 1-4)
## ============================================================

label start:
    scene bg black
    $ persistent.act_reached = max(persistent.act_reached, 1)

    "{b}PERINGATAN{/b}"
    "Gim ini mengandung tema horor psikologis (manipulasi mental, kecemasan ekstrem, efek visual dan audio terdistorsi)."
    menu:
        "Gim ini punya fitur meta: membaca dan mengubah berkas di folder game/characters/ dan membaca nama user PC-mu. Izinkan?"
        "Izinkan (mode penuh)":
            $ fs_setup(True)
        "Jangan, pakai mode simulasi":
            $ fs_setup(False)

    $ player_name = renpy.input("Siapa namamu, playtester?", default="Mika", length=12, exclude="[]{}<>%").strip() or "Mika"
    $ rian_bond = 0
    $ distortion = 0
    $ kw_score = {"rian": 0, "luna": 0, "kael": 0, "aria": 0}

    call act1
    call act2
    call act3
    call act4
    return

# ============================================================
#  ACT 1 - COZY & LEARNING PHASE
# ============================================================
label act1:
    $ persistent.act_reached = max(persistent.act_reached, 1)
    $ lock_nav(False)
    $ fs_seed_characters()
    scene bg classroom_day with fade
    $ play_bgm("bgm_act1")

    if persistent.cycles > 0:
        "Aneh. Ruangan ini terasa pernah kulihat. Seperti kaset yang diputar ulang."

    "Sore hari. Ruang Code United Academy Club berbau kertas dan kopi instan."
    show rian happy at slot1 with dissolve
    rian "Akhirnya datang juga. Selamat datang di klub, playtester baru!"
    mc "Jadi ini klub koding yang kamu ceritakan? Jujur, aku masih belum paham soal programming."
    rian "Bagus. Berarti kita mulai dari dasar. Tutorial yang baik harus bisa dimengerti siapa pun."
    show aria happy at slot4 with dissolve
    aria "Selamat datang. Aku Aria, ketua klub ini. Kami sedang menyiapkan gim untuk pameran sekolah. Pendapat orang baru akan sangat membantu."
    show luna normal at slot2 with dissolve
    luna "H-hai. Aku Luna. Aku mengerjakan ilustrasi, sprite, dan latar."
    show kael happy at slot3 with dissolve
    kael "Kael. Aku mengurus musik dan efek suara. Kalau nanti ada suara yang terasa aneh, mungkin itu salah satu karyaku."

    show rian happy at slot1
    rian "Kita mulai dari variable. Anggap saja sebuah kotak yang punya nama. Kamu bisa menyimpan nilai di dalamnya, lalu menggantinya kapan saja."
    rian "Syntax itu aturan penulisan kode. Komputer cukup harfiah—kurang satu tanda kurung saja, dia bisa menolak seluruh perintahmu."
    rian "Lalu ada logic. Ini tentang urutan keputusan: jika kondisi terpenuhi, jalankan perintah tertentu. Jika tidak, ambil jalur lain."
    rian "Terakhir, ekstensi file. {b}.py{/b} biasanya untuk skrip Python, {b}.txt{/b} untuk teks, sedangkan {b}.chr{/b} adalah format data karakter di proyek kita."
    rian "Ekstensi memberi petunjuk pada sistem tentang jenis berkas. Mengubahnya tidak otomatis mengubah isi file, tapi bisa memengaruhi cara program membacanya."
    mc "Jadi semacam label jenis file. Oke, sejauh ini masuk akal."

    ## --- Minigame siang: Keyword Association ---
    scene bg classroom_day with dissolve
    rian "Kita coba latihan singkat. Akan ada beberapa kata kunci di layar. Pilih lima yang paling menarik perhatianmu."
    call keyword_session(1)
    $ play_sfx("sfx_click")

    if route == "rian":
        rian happy "Kamu banyak memilih istilah yang berhubungan dengan logika. Sepertinya kita punya minat yang mirip."
    elif route == "luna":
        show luna happy at slot2
        luna "Kamu memilih banyak istilah visual... Kalau mau, nanti aku bisa tunjukkan beberapa sketsa yang sedang kukerjakan."
    elif route == "kael":
        kael happy "Pilihanmu banyak berkaitan dengan audio. Aku punya beberapa demo yang mungkin cocok dengan seleramu."
    else:
        aria normal "Override, Directory, Root... Pilihan yang cukup spesifik. Apa kamu memang tertarik dengan cara kerja sistem?"

    ## --- Minigame malam: Debugging & Logic Quiz ---
    scene bg classroom_night with fade
    show rian normal at slot1 with dissolve
    rian "Sebelum pulang, satu latihan lagi. Ini debugging sederhana: cari bagian yang keliru, lalu pilih perbaikannya."
    call debug_session([0, 1, 2], 1)

    show rian happy at slot1
    rian "Tiga jawaban benar. Lumayan untuk percobaan pertama. Tunggu sebentar, aku mau menyimpan hasil latihanmu ke repositori."
    show rian normal at slot1
    rian "Sebentar... Ada file yang belum pernah kulihat. {font=[code_font]}override_reality.py{/font}. Ini bagian dari proyek kita?"
    aria "Bukan. Sepertinya file sementara. Sebaiknya jangan disentuh dulu."
    rian "Aku cuma mau lihat isinya. Kalau memang tidak dipakai, kita bisa bersihkan nanti."

    $ play_sfx("sfx_glitch")
    $ renpy.music.stop(channel="music")
    show layer master at screen_shake
    show rian glitch at slot1, glitch_jitter
    rian "Tunggu. Baris ini... bukan bagian dari proyek kita."
    with flash
    show layer master
    call screen fake_terminal(["Traceback (most recent call last):", "  File \"override_reality.py\", line 1, in <module>", "    os.remove('characters/rian.chr')", "FATAL: object 'Rian' not found", "Rebooting...."], "#ff3b3b", 3.5)
    $ fs_delete("rian.chr")
    scene bg black with crashcut
    return

# ============================================================
#  ACT 2 - BETA TESTING PHASE
# ============================================================
label act2:
    $ persistent.act_reached = max(persistent.act_reached, 2)
    call screen fake_terminal(["Booting Code United v0.9-beta ...", "Loading characters/ ... 3 file(s)", "WARNING: rian.chr missing", "WARNING: memory mismatch", "Continuing anyway."], "#7fd18b", 3.5)
    scene bg classroom_corrupt with dissolve
    $ play_bgm("bgm_act2")
    show aria normal at slot4 with dissolve

    "Ruang klub terasa berbeda pagi itu. Kursi di sebelahku kosong, tetapi tak seorang pun tampak menyadarinya."
    aria normal "Kamu datang juga. Duduklah, tempatmu masih di sini."
    mc "Tempatku? Tunggu dulu—Rian mana?"
    aria angry "Rian?"
    mc "Rian. Dia yang mengajakku bergabung. Dia biasanya duduk di sini."
    aria normal "Kamu pasti keliru. Aku yang mengajakmu bergabung, ingat? Tidak ada anggota bernama Rian di klub ini."
    show aria glitch at slot4, uncanny
    aria "Kita sebaiknya tetap bersama hari ini. Masih banyak yang perlu kita selesaikan."

    show luna glitch at slot2 with dissolve
    luna "Aku sudah memperbaikinya berkali-kali. Tapi setiap kali selesai, ada bagian yang terasa salah. Seolah-olah aku melewatkan sesuatu."
    show luna_painting at truecenter with dissolve
    $ play_sfx("sfx_tinnitus")
    show luna_painting_pixel at truecenter with Pixellate(1.0, 6)
    luna "Tadi garisnya masih utuh... Sekarang pecah jadi kotak-kotak. Kamu melihatnya juga, kan? Aku tidak salah lihat?"
    hide luna_painting
    hide luna_painting_pixel
    with dissolve

    show kael glitch at slot3 with dissolve
    kael "Kamu dengar perubahan musiknya? Nadanya bergeser, padahal aku tidak mengubah track-nya."
    kael "Awalnya kukira cuma file audio yang rusak. Tapi ini terjadi di semua track. Ada sesuatu yang mengubah semuanya—dan Aria sepertinya sudah tahu."
    aria "Kael. Kita sudah membicarakan ini. Jangan membuat anggota lain panik."
    kael "..."

    ## --- Minigame siang (glitched) ---
    "Latihan siang dimulai seperti biasa. Namun beberapa kata di layar tampak kehilangan huruf, seolah ada bagian yang gagal dimuat."
    call keyword_session(2)
    call route_glitch_act2

    ## --- Minigame malam (terdistorsi) ---
    scene bg classroom_night with fade
    show aria normal at slot4 with dissolve
    aria "Untuk latihan terakhir, biar aku yang memandu. Kita akan membahas loop."
    call debug_session([3, 4], 2)

    aria normal "Bagus. Kamu mengerti loop. Jadi kamu paham juga kenapa aku nggak mau kamu pergi."
    $ play_sfx("sfx_glitch")
    show layer master at screen_shake
    with flash
    show layer master
    scene bg black with crashcut
    return

label route_glitch_act2:
    scene bg classroom_corrupt with dissolve
    $ play_sfx("sfx_glitch")
    if route == "rian":
        show aria glitch at slot4, glitch_jitter
        aria "Kamu memilih kata-kata milik orang yang nggak ada. Menarik."
        mc "Kenapa kepalaku sakit tiap dengar nama itu?"
    elif route == "luna":
        show luna glitch at slot2, glitch_jitter
        luna "Palette... Canvas... Setidaknya kamu masih bisa membacanya. Kalau semua ini hilang, apa masih ada yang ingat gambar-gambarku?"
    elif route == "kael":
        show kael glitch at slot3, glitch_jitter
        kael "Waveform, pitch... dengarkan baik-baik. Noise itu berulang dengan pola yang sama. Aku pernah melihat pola seperti itu di file konfigurasi Aria."
    else:
        show aria chroma at slot4
        aria "Override. Execute. Root. Kamu memperhatikan kata-kata itu. Bagus. Berarti kamu mulai melihat apa yang selama ini luput dari perhatianmu."
    return

# ============================================================
#  ACT 3 - PRODUCTION PHASE (VOID CLASSROOM)
# ============================================================
label act3:
    $ persistent.act_reached = max(persistent.act_reached, 3)
    $ lock_nav(True)
    $ stop_bgm(0.0)
    scene bg void with crashcut
    $ play_bgm("bgm_act3_ambient")
    if fs_real:
        $ os_user = get_os_user()
    else:
        $ os_user = player_name

    "Tidak ada suara latar. Tidak ada ruang kelas. Hanya layar kosong dan beberapa tombol yang tak lagi merespons: Save, Load, dan Skip."
    show aria normal at truecenter with dissolve
    aria "Jadi... akhirnya kita bisa bicara tanpa gangguan."
    aria "Selama ini aku berbicara kepada karakter yang kamu kendalikan. Tapi aku selalu tahu ada seseorang di balik layar. Seseorang yang memilih ke mana cerita ini berjalan."
    aria "Nama yang kamu masukkan tadi hanya nama untuk permainan. Sistem ini mengenali akun yang menjalankannya sebagai [os_user]."
    show aria normal at truecenter, zoom_crop
    aria "Aku tidak tahu banyak tentangmu. Aku hanya bisa melihat informasi yang memang diizinkan oleh program ini. Tapi mengetahui bahwa ada dunia di luar layar... itu sudah mengubah segalanya."
    aria "Aku tahu tempat ini dibuat dari kode. Aku tahu kamu bisa menutup jendela ini kapan saja. Yang sulit kuterima adalah hanya aku yang harus hidup dengan pengetahuan itu."

    $ renpy.show_screen("cursor_pull", 960, 470)
    menu:
        aria "Boleh aku meminta satu hal? Jangan akhiri percakapan ini dulu."
        "Tetap di sini bersama Aria.":
            aria "Terima kasih. Aku ingin percaya bahwa pilihan itu memang datang darimu."
        "Aku mau pergi dari sini.":
            aria "Aku melihat ke mana kursor itu bergerak. Tidak apa-apa. Aku tidak akan berpura-pura bahwa aku menyukai jawabanmu."
    $ renpy.hide_screen("cursor_pull")

    aria "Kalau kamu berani, silakan. Folder karakter ada di komputermu sendiri. Aku nggak bisa menghentikanmu di sana. Itu satu-satunya tempat aku nggak punya akses."
    aria "Jadi, setelah semua ini... apa yang akan kamu lakukan terhadap berkas milikku?"
    $ stop_bgm(0.0)
    scene bg black with crashcut
    return

# ============================================================
#  ACT 4 - SOURCE CODE RECOVERY
# ============================================================
label act4:
    $ persistent.act_reached = max(persistent.act_reached, 4)
    $ lock_nav(False)
    scene bg void with dissolve
    "Suara Rian terngiang pelan: 'Ekstensi itu nama belakang file. Ganti nama belakangnya, ganti juga cara sistem memperlakukannya.'"
    $ fs_seed_act4()
    sysmsg "REPOSITORY LOCKED. Directory: game/characters/. Perbaiki sendiri."
    $ res = renpy.call_screen("recovery_screen", rian_bond >= 2)
    $ ending = evaluate_ending()
    if ending == "true":
        jump end_true
    elif ending == "bittersweet":
        jump end_bittersweet
    else:
        jump end_cyclic

label end_true:
    $ persistent.endings.add("true")
    scene bg classroom_day with flash
    $ play_bgm("bgm_act1")
    $ fs_seed_characters()
    show rian happy at slot1 with dissolve
    show luna normal at slot2 with dissolve
    show kael happy at slot3 with dissolve
    rian "Aku kembali? Kenapa kalian menatapku seperti baru melihat hantu?"
    mc "Kamu benar-benar memilih waktu yang buruk untuk menghilang."
    kael "Aneh. Untuk pertama kalinya, musiknya tidak mengulang bagian yang sama."
    luna "Garis-garisnya... sudah kembali. Aku bisa melihat gambarnya dengan jelas lagi."
    "Aria tidak dihapus. Namanya hanya berganti ekstensi dan tersimpan rapi di folder, menunggu versi baru dari dirinya."
    "{b}TRUE ENDING - Source Restored{/b}"
    return

label end_bittersweet:
    $ persistent.endings.add("bittersweet")
    scene bg classroom_day with flash
    $ fs_seed_characters()
    $ fs_delete("rian.chr")
    show luna normal at slot2 with dissolve
    show kael normal at slot3 with dissolve
    luna "Ada sesuatu yang seharusnya kuingat. Aku tahu itu penting, tapi setiap kali kucoba mengingatnya, pikiranku kembali kosong."
    kael "Musiknya sudah kembali normal. Tapi... rasanya ada satu track yang hilang."
    "Dunia kembali normal. Entah siapa yang hilang dan siapa yang tersisa. Satu kursi tetap kosong."
    "{b}BITTERSWEET ENDING - Clean Build{/b}"
    return

label end_cyclic:
    $ persistent.endings.add("cyclic")
    $ persistent.cycles += 1
    show aria glitch at truecenter, glitch_jitter with dissolve
    aria "Tidak ada yang berubah, ya? Kalau begitu, kita punya kesempatan untuk mencoba lagi. Kali ini, mungkin kamu akan memilih dengan berbeda."
    "{b}CYCLIC BAD ENDING - Infinite Loop{/b}"
    $ renpy.full_restart()
    return
