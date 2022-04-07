import random, ctypes, json
from tkinter import *
from PIL import ImageTk, Image
user32 = ctypes.windll.user32
screensize_x, screensize_y = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
import tkinter.font as font

root = Tk()
root.title("Kockapóker")  # cím
root.attributes('-fullscreen', True)
root.grid_columnconfigure(1, minsize=1600)
root.configure(bg="black")

img = ImageTk.PhotoImage(Image.open("23138.jpg"))
l=Label(image=img).place(x=175, y=-40)

dobasok, jobb_dobasok = [], []  # kockákat tárolja, a másik meg a bot kockáit

# "dob" a kockákkal
def dobas(lista, label):
    lista.clear()  # lista kiürítése
    for dobas in range(5):
        dobas = random.randint(1, 6)
        lista.append(dobas)
    label['text'] = lista

    szum=0
    szum_ellenseg = 0


    for gomb in jatekos_gombok:
        if str(gomb['text']).isdigit():
            szum += gomb['text']
        if gomb['state'] == DISABLED:
            gomb['cursor'] = "arrow"
        else:
            gomb['cursor'] = CURSOR

    for gomb in gombok:
        if str(gomb['text']).isdigit():
            szum_ellenseg += gomb['text']
        if gomb['state'] == DISABLED:
            gomb['cursor'] = "arrow"
        else:
            gomb['cursor'] = CURSOR
    label_pontszam['text'] = ellenorzes('player', jatekos_gombok, 'player_score'), ':', ellenorzes('enemy', gombok, 'enemy_score')


    return lista


# szemét
def szemet():
    szum = 0
    for kocka in dobasok:
        szum += kocka
    fajlba_ir('player', 0, szum, 'player_score')
    button_1['state'], button_1['text'] = DISABLED, szum
    jobb_oldal()


# pár
def par():
    dobasok.sort()
    szum = 0
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 2:
            szum, button_2['text'] = sorszam * 2, sorszam * 2
    if button_2['text'] == "Pár":
        szum, button_2['text'] = 0, 0
    fajlba_ir('player', 1, szum, 'player_score')
    button_2['state'] = DISABLED
    jobb_oldal()


# két pár
def ket_par():
    dobasok.sort()
    parok = []
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 2:
            parok.append(sorszam)
    parok = sorted(parok)

    try:
        szum = parok[-1] * 2 + parok[-3] * 2
    except:
        szum = 0
    fajlba_ir('player', 2, szum, 'player_score')
    button_3['text'], button_3['state'] = szum, DISABLED
    jobb_oldal()


# drill
def drill():
    dobasok.sort()
    szum = 0
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 3:
            szum, button_4['text'] = sorszam * 3, sorszam * 3
    if button_4['text'] == "Drill":
        szum, button_4['text'] = 0, 0
    fajlba_ir('player', 3, szum, 'player_score')
    button_4['state'] = DISABLED
    jobb_oldal()


# full house
def full():
    dobasok.sort()
    par, drill = 0, 0
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 3:
            drill = sorszam * 3
    for x in range(dobasok.count(drill / 3)):
        dobasok.remove(drill / 3)
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 2:
            par = sorszam * 2
    szum = drill + par
    if drill == 0 or par == 0:
        szum = 0
    button_5['text'] = szum
    if button_5['text'] == "Full":
        button_5['text'] = 0
    fajlba_ir('player', 4, szum, 'player_score')
    button_5['state'] = DISABLED
    jobb_oldal()


# kis sor
def kis_sor():
    dobasok.sort()
    seged, kis_sor = 1, True
    while seged != 6:
        if dobasok.count(seged) == 0:
            kis_sor = False
        seged += 1
    if kis_sor:
        szum, button_6['text'] = 15, 15
    else:
        szum, button_6['text'] = 0, 0
    fajlba_ir('player', 5, szum, 'player_score')
    button_6['state'] = DISABLED
    jobb_oldal()


# nagy sor
def nagy_sor():
    dobasok.sort()
    seged, nagy_sor = 2, True
    while seged != 7:
        if dobasok.count(seged) == 0:
            nagy_sor = False
        seged += 1
    if nagy_sor:
        szum, button_7['text'] = 20, 20
    else:
        szum, button_7['text'] = 0, 0
    fajlba_ir('player', 6, szum, 'player_score')
    button_7['state'] = DISABLED
    jobb_oldal()


# kis póker
def kis_poker():
    dobasok.sort()
    szum = 0
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 4:
            szum, button_8['text'] = sorszam * 4, sorszam * 4
    if button_8['text'] == "Kis póker":
        szum, button_8['text'] = 0, 0
    fajlba_ir('player', 7, szum, 'player_score')
    button_8['state'] = DISABLED
    jobb_oldal()


# nagy póker
def nagy_poker():
    dobasok.sort()
    szum = 0
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 5:
            szum, button_9['text'] = 50, 50
    if button_9['text'] == "Nagy póker":
        szum, button_9['text'] = 0, 0
    fajlba_ir('player', 8, szum, 'player_score')
    button_9['state'] = DISABLED
    jobb_oldal()

# átírja a gombok szövegét és állapotát disabled-re
def be_ir(button, ertek):
    button['text'], button['state'] = ertek, DISABLED

# lecsukja az ablakot
def close():
    root.iconify()

# Újraindítja a játékot, kitölti a fájlt nullásokkal az üres helyeken, visszaállítja pontszámokat és gombokat
def ujra(gomb_lista, ellenseg_gombok, szoveg):
    for (gomb, gomb2, szo) in zip(gomb_lista, ellenseg_gombok, szoveg): gomb['state'], gomb2['state'], gomb['text'], gomb2['text'] = NORMAL, NORMAL, szo, szo
    dobas(dobasok, label_dobasok)
    file = open('data.json', 'tr', encoding="UTF-8")
    data = json.load(file)
    file.close()
    file = open('data.json', 'tw', encoding="UTF-8")
    for index in range(9):
        if len(data['player'][index]) < data['round']:
            data['player'][index].append(0)
        if len(data['enemy'][index]) < data['round']:
            data['enemy'][index].append(0)
    data['round'] += 1
    data['player_score'], data['enemy_score'] = 0, 0
    json.dump(data, file, indent=4)
    file.close()
    label_jatek_vege.place(x=10000, y=screensize_y / 3 + screensize_y / 24, width=screensize_x / 4,height=screensize_y / 4)
    label_jatek_vege_alap.place(x=10000, y=screensize_y / 3 + screensize_y / 24, width=screensize_x / 4,height=screensize_y / 4)
    button_vege.place(x=10000, y=screensize_y / 2 + 100)

# bezárja az ablakot, ha a játék vége után történik, akkor előtte újraindítja  ajátékot és csak utána lép ki
def kilep():
    if not vege_van():
        root.destroy()
    else:
        ujra(jatekos_gombok, gombok, szovegek)
        root.destroy()

# számítógép lépése lépése, összehasonlítja az összes értéket és az alapján dönt. Ez írja le az ellenség működését/gondolkodását
def jobb_oldal():
    egyik_par, ertekek, k_sor, n_sor, lista, dolgok = 0, [0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 3, 4, 5], [2, 3, 4, 5, 6], dobas(jobb_dobasok, jobb_label_dobasok), ["szemet", "par", "ket_par", "drill", "full", "kis_sor", "nagy_sor", "kis_poker", "nagy_poker"]

    for szam in lista:
        if gombok[0]['state'] != DISABLED:  # szemét
            ertekek[0] += szam
        if gombok[5]['state'] != DISABLED:  # kis sor
            if szam in k_sor:
                k_sor.remove(szam)
        if gombok[6]['state'] != DISABLED:  # nagy sor
            if szam in n_sor:
                n_sor.remove(szam)
    if len(k_sor) == 0:
        ertekek[5] = 15
    if len(n_sor) == 0:
        ertekek[6] = 20

    for szam in range(1, 7):
        if gombok[8]['state'] != DISABLED:  # nagy póker
            if lista.count(szam) >= 5:
                ertekek[8] = 50
        if gombok[7]['state'] != DISABLED:  # kis póker
            if lista.count(szam) >= 4:
                ertekek[7] = szam * 4
        if gombok[3]['state'] != DISABLED:  # drill
            if lista.count(szam) >= 3:
                ertekek[3] = szam * 3
        if gombok[1]['state'] != DISABLED:  # pár
            if lista.count(szam) >= 2:
                ertekek[1] = szam * 2
        if gombok[4]['state'] != DISABLED:  # full
            if egyik_par != 0 and egyik_par != szam and lista.count(szam) >= 3:
                ertekek[4] = (egyik_par + szam) * 2 + szam
            elif ertekek[3] != 0 and (ertekek[3] / 3) != szam and lista.count(szam) >= 2:
                ertekek[4] = ertekek[3] + (szam * 2)
        if gombok[2]['state'] != DISABLED:  # két pár
            if egyik_par != 0 and egyik_par != szam and lista.count(szam) == 2:
                ertekek[2] = (egyik_par + szam) * 2
        if lista.count(szam) >= 2:
            egyik_par = szam

    if ertekek.count(0) == 9:
        for index in range(9):
            if gombok[index]['state'] != DISABLED:
                be_ir(gombok[index], ertekek[index])
                fajlba_ir('enemy', index, ertekek[index], 'enemy_score')
                break
    else:
        for index in range(9):
            if ertekek.index(max(ertekek)) == index:
                be_ir(gombok[index], ertekek[index])
                fajlba_ir('enemy', index, ertekek[index], 'enemy_score')
                break

    if vege_van():
        eredmeny_hirdetes()

# Hover effekt az 1-es gombon
def ravisz_1(e):
    def szemet2():
        szum = 0
        for kocka in dobasok:
            szum += kocka
        return szum
    if button_1['state'] == NORMAL:
        button_1['text'] = szemet2()

# Hover effekt az 2-es gombon
def ravisz_2(e):
    def par2():
        eredmeny = 0
        for sorszam in dobasok:
            if dobasok.count(sorszam) >= 2:
                eredmeny = sorszam * 2
        return eredmeny
    if button_2['state'] == NORMAL:
        button_2['text'] = par2()

# Hover effekt az 3-as gombon
def ravisz_3(e):
    def ket_par2():
        parok = []
        for sorszam in dobasok:
            if dobasok.count(sorszam) == 2 or dobasok.count(sorszam) == 3:
                parok.append(sorszam)
            if dobasok.count(sorszam) == 4 or dobasok.count(sorszam) == 5:
                parok.append(sorszam)
                parok.append(sorszam)
        parok = sorted(parok)
        if len(parok) == 3:
            parok.pop(0)
        try:
            szum = parok[-1] * 2 + parok[-3] * 2
        except:
            szum = 0
        return szum
    if button_3['state'] == NORMAL:
        button_3['text'] = ket_par2()

# Hover effekt az 4-es gombon
def ravisz_4(e):
    def drill2():
        eredmeny=0
        for sorszam in dobasok:
            if dobasok.count(sorszam) >= 3:
                eredmeny = sorszam * 3
        return eredmeny
    if button_4['state'] == NORMAL:
        button_4['text'] = drill2()

# Hover effekt az 1-ös gombon
def ravisz_5(e):
    def full2():
        par, drill, eredmeny, dobasok_clone = 0, 0, 0, []
        for tag in dobasok:
            dobasok_clone.append(tag)
        for sorszam in dobasok_clone:
            if dobasok_clone.count(sorszam) >= 3:
                drill = sorszam * 3
        for x in range(dobasok_clone.count(drill / 3)):
            dobasok_clone.remove(drill / 3)
        for sorszam in dobasok_clone:
            if dobasok_clone.count(sorszam) >= 2:
                par = sorszam * 2
        eredmeny = drill + par
        if drill == 0 or par == 0:
            eredmeny = 0
        return eredmeny
    if button_5['state'] == NORMAL:
        button_5['text'] = full2()

# Hover effekt az 6-os gombon
def ravisz_6(e):
    def kis_sor2():
        seged, kis_sor = 1, True
        while seged != 6:
            if dobasok.count(seged) == 0:
                kis_sor = False
            seged += 1
        if kis_sor:
            eredmeny = 15
        else:
            eredmeny = 0
        return eredmeny
    if button_6['state'] == NORMAL:
        button_6['text'] = kis_sor2()

# Hover effekt az 7-es gombon
def ravisz_7(e):
    def nagy_sor2():
        seged, nagy_sor = 2, True
        while seged != 7:
            if dobasok.count(seged) == 0:
                nagy_sor = False
            seged += 1
        if nagy_sor:
            eredmeny = 20
        else:
            eredmeny = 0
        return eredmeny
    if button_7['state'] == NORMAL:
        button_7['text'] = nagy_sor2()

# Hover effekt az 8-as gombon
def ravisz_8(e):
    def kis_poker2():
        eredmeny = 0
        for sorszam in dobasok:
            if dobasok.count(sorszam) >= 4:
                eredmeny = sorszam * 4
        return eredmeny
    if button_8['state'] == NORMAL:
        button_8['text'] = kis_poker2()

# Hover effekt az 9-es gombon
def ravisz_9(e):
    def nagy_poker2():
        eredmeny = 0
        for sorszam in dobasok:
            if dobasok.count(sorszam) >= 5:
                eredmeny = 50
        return eredmeny
    if button_9['state'] == NORMAL:
        button_9['text'] = nagy_poker2()

# Hover effekt eltűnése a gombról
def levesz(e):
        if button_1['state'] == NORMAL:
            button_1['text'] = "Szemét"
        if button_2['state'] == NORMAL:
            button_2['text'] = "Pár"
        if button_3['state'] == NORMAL:
            button_3['text'] = "Két pár"
        if button_4['state'] == NORMAL:
            button_4['text'] = "Drill"
        if button_5['state'] == NORMAL:
            button_5['text'] = "Full"
        if button_6['state'] == NORMAL:
            button_6['text'] = "Kis sor"
        if button_7['state'] == NORMAL:
            button_7['text'] = "Nagy sor"
        if button_8['state'] == NORMAL:
            button_8['text'] = "Kis póker"
        if button_9['state'] == NORMAL:
            button_9['text'] = "Nagy póker"

# beírja a fájlba az értékeket
def fajlba_ir(player_or_enemy, index, ertek, score_type):
    file = open('data.json', 'tr', encoding="UTF-8")
    data = json.load(file)
    file.close()
    data[player_or_enemy][index].append(ertek)
    data[score_type] += ertek
    file = open('data.json', 'tw', encoding="UTF-8")
    json.dump(data, file, indent=4)
    file.close()

# kikapcsolja a gombokat és visszaadja a pont értékét
def ellenorzes(player_or_enemy, lista, score):
    file = open('data.json', 'tr', encoding="UTF-8")
    data = json.load(file)
    file.close()
    for index in range(len(lista)):
        if len(data[player_or_enemy][index]) == data['round']:
            lista[index]['text'] = data[player_or_enemy][index][-1]
            lista[index]['state'] = DISABLED
        else:
            lista[index]['text'] = szovegek[index]
            lista[index]['state'] = NORMAL
    return data[score]

# megnézi, hogy minden gom ki van-e kapcsolva, azaz vége van-e a játéknak
def vege_van():
    van_enable_gomb = True
    for gomb in gombok:
        if gomb['state'] == NORMAL:
            van_enable_gomb = False
    return van_enable_gomb

# eredményjelző képernyő
def eredmeny_hirdetes():
    label_jatek_vege_alap.place(x=screensize_x / 3, y=screensize_y / 3, width=screensize_x / 3, height=screensize_y / 3)
    label_jatek_vege.place(x=screensize_x / 3 + screensize_x / 24, y=screensize_y / 3 + screensize_y / 24, width=screensize_x / 4, height=screensize_y / 4)
    button_vege.place(x=screensize_x / 2 - screensize_x / 150 - 50, y=screensize_y / 2 + 100)
    if ellenorzes('player', jatekos_gombok, 'player_score') > ellenorzes('enemy', gombok, 'enemy_score'):
        label_jatek_vege['text'] = "Győztél!"
    elif ellenorzes('player', jatekos_gombok, 'player_score') < ellenorzes('enemy', gombok, 'enemy_score'):
        label_jatek_vege['text'] = "Vesztettél!"
    else:
        label_jatek_vege['text'] = "Döntetlen!"

# változók a gombokhoz és szövegekhez, egyszerűsítik a kinézet változtatását
PADX=41
PADY=10
BG="white"
FG="lime"
FONT = font.Font(size=25, family="Courier", weight="bold")
FONT_eredmeny = font.Font(size=50, family="Arial")
DISFG="black"
CURSOR= "X_cursor"
ACTBG="lime"
ACTFG="black"
MAGASSAG=(screensize_y-33)//9
SZELESSEG=250

# gombok és szövegek meghívása és elhelyezése
button_1 = Button(root, text="Szemét", padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, disabledforeground=DISFG, cursor=CURSOR, activebackground=ACTBG, activeforeground=ACTFG, command=lambda: [szemet(), dobas(dobasok, label_dobasok)])
button_2 = Button(root, text="Pár", padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, disabledforeground=DISFG, cursor=CURSOR, activebackground=ACTBG, activeforeground=ACTFG, command=lambda: [par(), dobas(dobasok, label_dobasok)])
button_3 = Button(root, text="Két pár", padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, disabledforeground=DISFG, cursor=CURSOR, activebackground=ACTBG, activeforeground=ACTFG, command=lambda: [ket_par(), dobas(dobasok, label_dobasok)])
button_4 = Button(root, text="Drill", padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, disabledforeground=DISFG, cursor=CURSOR, activebackground=ACTBG, activeforeground=ACTFG, command=lambda: [drill(), dobas(dobasok, label_dobasok)])
button_5 = Button(root, text="Full", padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, disabledforeground=DISFG, cursor=CURSOR, activebackground=ACTBG, activeforeground=ACTFG, command=lambda: [full(), dobas(dobasok, label_dobasok)])
button_6 = Button(root, text="Kis sor", padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, disabledforeground=DISFG, cursor=CURSOR, activebackground=ACTBG, activeforeground=ACTFG, command=lambda: [kis_sor(), dobas(dobasok, label_dobasok)])
button_7 = Button(root, text="Nagy sor", padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, disabledforeground=DISFG, cursor=CURSOR, activebackground=ACTBG, activeforeground=ACTFG, command=lambda: [nagy_sor(), dobas(dobasok, label_dobasok)])
button_8 = Button(root, text="Kis póker", padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, disabledforeground=DISFG, cursor=CURSOR, activebackground=ACTBG, activeforeground=ACTFG, command=lambda: [kis_poker(), dobas(dobasok, label_dobasok)])
button_9 = Button(root, text="Nagy póker", padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, disabledforeground=DISFG, cursor=CURSOR, activebackground=ACTBG, activeforeground=ACTFG, command=lambda: [nagy_poker(), dobas(dobasok, label_dobasok)])
button_ujra = Button(root, text="↺", width=5, height=1, padx=5, pady=5, bg="green", fg="white", command=lambda: [ujra(jatekos_gombok, gombok, szovegek), dobas(dobasok, label_dobasok)])
button_kilep = Button(root, text="X", width=5, height=1, padx=5, pady=5, bg="red", fg="white" , command=kilep)
button_lecsuk = Button(root, text="__", width=5, height=1, padx=5, pady=5, bg="blue", fg="white", command=close)

label_dobasok = Label(root, padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, borderwidth=4, relief="sunken")
label_dobasok.place(x=250, y=33, width=SZELESSEG, height=MAGASSAG/2)
jobb_label_dobasok = Label(root, padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT,  borderwidth=4, relief="sunken")
jobb_label_dobasok.place(x=screensize_x-SZELESSEG*2, y=34, width=SZELESSEG, height=MAGASSAG/2)

label_jatek_vege_alap = Label(root, padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, borderwidth=10, relief="flat")
label_jatek_vege = Label(root, padx=PADX*3, pady=PADY*3, bg=BG, fg=FG, font=FONT_eredmeny, borderwidth=5, relief="sunken")
button_vege = Button(root, text="Újra", width=int(screensize_x/300), height=int(screensize_y/700), padx=0, pady=0, font=FONT, bg="green", fg="white", command=lambda: [ujra(jatekos_gombok, gombok, szovegek), dobas(dobasok, label_dobasok)])

gombok, jatekos_gombok, szovegek = [], [button_1, button_2, button_3, button_4,button_5, button_6, button_7, button_8, button_9], ["Szemét", "Pár", "Két pár", "Drill", "Full", "Kis sor", "Nagy sor", "Kis póker", "Nagy póker"]

pos_y = 33
for index in range(9):
    gomb = Button(root, text=szovegek[index], padx=PADX, pady=PADY, bg=BG, fg=FG, font=FONT, disabledforeground=DISFG, cursor=CURSOR, activebackground=BG, activeforeground=FG)
    gombok.append(gomb)
    gomb.place(x=screensize_x-SZELESSEG, y=pos_y, width=SZELESSEG, height=MAGASSAG)
    pos_y+=MAGASSAG

space1 = Label(root, width=250, text="", height=1, padx=4, pady=7, bg="white", fg="white")
space1.place(x=0, y=0)

label_pontszam = Label(root, width=10, text="", pady=7, bg="#FFFFFF", fg="black")
label_pontszam.place(x=screensize_x/2-175, y=50)
label_pontszam.config(font=("Arial", 44))

button_kilep.place(x=screensize_x-53, y=0)
button_ujra.place(x=screensize_x-106, y=0)
button_lecsuk.place(x=screensize_x-159, y=0)

pos_y = 33
for gomb in jatekos_gombok:
    gomb.place(x=0, y=pos_y, width=SZELESSEG, height=MAGASSAG)
    pos_y+=MAGASSAG
    gomb.bind("<Leave>", levesz)

button_1.bind("<Enter>", ravisz_1)
button_2.bind("<Enter>", ravisz_2)
button_3.bind("<Enter>", ravisz_3)
button_4.bind("<Enter>", ravisz_4)
button_5.bind("<Enter>", ravisz_5)
button_6.bind("<Enter>", ravisz_6)
button_7.bind("<Enter>", ravisz_7)
button_8.bind("<Enter>", ravisz_8)
button_9.bind("<Enter>", ravisz_9)

label_jatek_vege.place(x=10000, y=screensize_y / 3 + screensize_y / 24, width=screensize_x / 4, height=screensize_y / 4)
label_jatek_vege_alap.place(x=10000, y=screensize_y / 3, width=screensize_x / 3, height=screensize_y / 3)
button_vege.place(x=10000, y=screensize_y / 2 + 100)

# program elindítása
dobas(dobasok, label_dobasok)
root.mainloop()
