import random, ctypes, json
from tkinter import *
from PIL import ImageTk, Image
user32 = ctypes.windll.user32
screensize_x, screensize_y = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

root = Tk()
root.title("Kockapóker")  # cím
root.attributes('-fullscreen', True)
root.configure(bg="white")  # háttérszín
root.grid_columnconfigure(1, minsize=1600)

img = ImageTk.PhotoImage(Image.open("bg_car.jpg"))
l=Label(image=img).place(x=2, y=2)

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
    for gomb in gombok:
        if str(gomb['text']).isdigit():
            szum_ellenseg += gomb['text']
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


def be_ir(button, ertek):
    button['text'], button['state'] = ertek, DISABLED


def kilep():
    root.destroy()

def close():
    root.iconify()

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


def jobb_oldal():
    egyik_par, ertekek, k_sor, n_sor, lista, dolgok = 0, [0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 3, 4, 5], [2, 3, 4, 5, 6], dobas(jobb_dobasok, jobb_label_dobasok), ["szemet", "par", "ket_par", "drill", "full", "kis_sor", "nagy_sor", "kis_poker", "nagy_poker"]

    for szam in lista:
        if jobb_button_1['state'] != DISABLED:  # szemét
            ertekek[0] += szam
        if jobb_button_6['state'] != DISABLED:  # kis sor
            if szam in k_sor:
                k_sor.remove(szam)
        if jobb_button_7['state'] != DISABLED:  # nagy sor
            if szam in n_sor:
                n_sor.remove(szam)
    if len(k_sor) == 0:
        ertekek[5] = 15
    if len(n_sor) == 0:
        ertekek[6] = 20

    for szam in range(1, 7):
        if jobb_button_9['state'] != DISABLED:  # nagy póker
            if lista.count(szam) >= 5:
                ertekek[8] = 50
        if jobb_button_8['state'] != DISABLED:  # kis póker
            if lista.count(szam) >= 4:
                ertekek[7] = szam * 4
        if jobb_button_4['state'] != DISABLED:  # drill
            if lista.count(szam) >= 3:
                ertekek[3] = szam * 3
        if jobb_button_2['state'] != DISABLED:  # pár
            if lista.count(szam) >= 2:
                ertekek[1] = szam * 2
        if jobb_button_5['state'] != DISABLED:  # full
            if egyik_par != 0 and egyik_par != szam and lista.count(szam) >= 3:
                ertekek[4] = (egyik_par + szam) * 2 + szam
            elif ertekek[3] != 0 and (ertekek[3] / 3) != szam and lista.count(szam) >= 2:
                ertekek[4] = ertekek[3] + (szam * 2)
        if jobb_button_3['state'] != DISABLED:  # két pár
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


def ravisz_1(e):
    def szemet2():
        szum = 0
        for kocka in dobasok:
            szum += kocka
        return szum
    if button_1['state'] == NORMAL:
        button_1['text'] = szemet2()

def ravisz_2(e):
    def par2():
        eredmeny = 0
        for sorszam in dobasok:
            if dobasok.count(sorszam) >= 2:
                eredmeny = sorszam * 2
        return eredmeny
    if button_2['state'] == NORMAL:
        button_2['text'] = par2()

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

def ravisz_4(e):
    def drill2():
        eredmeny=0
        for sorszam in dobasok:
            if dobasok.count(sorszam) >= 3:
                eredmeny = sorszam * 3
        return eredmeny
    if button_4['state'] == NORMAL:
        button_4['text'] = drill2()

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

def ravisz_8(e):
    def kis_poker2():
        eredmeny = 0
        for sorszam in dobasok:
            if dobasok.count(sorszam) >= 4:
                eredmeny = sorszam * 4
        return eredmeny
    if button_8['state'] == NORMAL:
        button_8['text'] = kis_poker2()

def ravisz_9(e):
    def nagy_poker2():
        eredmeny = 0
        for sorszam in dobasok:
            if dobasok.count(sorszam) >= 5:
                eredmeny = 50
        return eredmeny
    if button_9['state'] == NORMAL:
        button_9['text'] = nagy_poker2()

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


def fajlba_ir(player_or_enemy, index, ertek, score_type):
    file = open('data.json', 'tr', encoding="UTF-8")
    data = json.load(file)
    file.close()
    data[player_or_enemy][index].append(ertek)
    #data[player_or_enemy][score_type] += ertek
    file = open('data.json', 'tw', encoding="UTF-8")
    json.dump(data, file, indent=4)
    file.close()

def ellenorzes(player_or_enemy, lista, score):
    file = open('data.json', 'tr', encoding="UTF-8")
    data = json.load(file)
    file.close()
    round = data['round']
    for index in range(len(lista)):
        if len(data[player_or_enemy][index]) == round:
            lista[index]['state'] = DISABLED
    return data[score]



label_dobasok = Label(root, width=20, padx=41, pady=30, bg="gray", fg="white", borderwidth=4, relief="sunken")
button_1 = Button(root, text="Szemét", width=20, padx=41, pady=30, bg="gray", fg="yellow", command=lambda: [szemet(), dobas(dobasok, label_dobasok)])
button_2 = Button(root, text="Pár", width=20, padx=41, pady=30, bg="gray", fg="yellow", command=lambda: [par(), dobas(dobasok, label_dobasok)])
button_3 = Button(root, text="Két pár", width=20, padx=41, pady=30, bg="gray", fg="yellow", command=lambda: [ket_par(), dobas(dobasok, label_dobasok)])
button_4 = Button(root, text="Drill", width=20, padx=41, pady=30, bg="gray", fg="yellow", command=lambda: [drill(), dobas(dobasok, label_dobasok)])
button_5 = Button(root, text="Full", width=20, padx=41, pady=30, bg="gray", fg="yellow", command=lambda: [full(), dobas(dobasok, label_dobasok)])
button_6 = Button(root, text="Kis sor", width=20, padx=41, pady=30, bg="gray", fg="yellow", command=lambda: [kis_sor(), dobas(dobasok, label_dobasok)])
button_7 = Button(root, text="Nagy sor", width=20, padx=41, pady=30, bg="gray", fg="yellow", command=lambda: [nagy_sor(), dobas(dobasok, label_dobasok)])
button_8 = Button(root, text="Kis póker", width=20, padx=41, pady=30, bg="gray", fg="yellow", command=lambda: [kis_poker(), dobas(dobasok, label_dobasok)])
button_9 = Button(root, text="Nagy póker", width=20, padx=41, pady=30, bg="gray", fg="yellow", command=lambda: [nagy_poker(), dobas(dobasok, label_dobasok)])
button_ujra = Button(root, text="R", width=5, height=1, padx=5, pady=5, bg="green", fg="white", command=lambda: ujra(jatekos_gombok, gombok, szovegek))
button_kilep = Button(root, text="X", width=5, height=1, padx=5, pady=5, bg="red", fg="white", command=kilep)
button_lecsuk = Button(root, text="__", width=5, height=1, padx=5, pady=5, bg="blue", fg="white", command=close)

jobb_label_dobasok = Label(root, width=10, padx=40, pady=20, bg="gray", fg="white", borderwidth=4, relief="sunken")
jobb_button_1 = Button(root, text="Szemét", width=10, padx=40, pady=20, bg="gray", fg="yellow")
jobb_button_2 = Button(root, text="Pár", width=10, padx=40, pady=20, bg="gray", fg="yellow")
jobb_button_3 = Button(root, text="Két pár", width=10, padx=40, pady=20, bg="gray", fg="yellow")
jobb_button_4 = Button(root, text="Drill", width=10, padx=40, pady=20, bg="gray", fg="yellow")
jobb_button_5 = Button(root, text="Full", width=10, padx=40, pady=20, bg="gray", fg="yellow")
jobb_button_6 = Button(root, text="Kis sor", width=10, padx=40, pady=20, bg="gray", fg="yellow")
jobb_button_7 = Button(root, text="Nagy sor", width=10, padx=40, pady=20, bg="gray", fg="yellow")
jobb_button_8 = Button(root, text="Kis póker", width=10, padx=40, pady=20, bg="gray", fg="yellow")
jobb_button_9 = Button(root, text="Nagy póker", width=10, padx=40, pady=20, bg="gray", fg="yellow")

space1 = Label(root, width=250, text="adaawdawddawawddaw", height=1, padx=4, pady=7, bg="white", fg="white")
space1.place(x=0, y=0)
label_pontszam = Label(root, width=10, text="almafafafa", pady=7, bg="#FFFFFF", fg="black")
label_pontszam.place(x=screensize_x/2-100, y=50)
label_pontszam.config(font=("Arial", 44))

button_kilep.place(x=screensize_x-53, y=0)
button_ujra.place(x=screensize_x-106, y=0)
button_lecsuk.place(x=screensize_x-159, y=0)
label_dobasok.grid(row=1, column=0)
button_1.grid(row=2, column=0)
button_2.grid(row=3, column=0)
button_3.grid(row=4, column=0)
button_4.grid(row=5, column=0)
button_5.grid(row=6, column=0)
button_6.grid(row=7, column=0)
button_7.grid(row=8, column=0)
button_8.grid(row=9, column=0)
button_9.grid(row=10, column=0)
button_1.bind("<Enter>", ravisz_1)
button_1.bind("<Leave>", levesz)
button_2.bind("<Enter>", ravisz_2)
button_2.bind("<Leave>", levesz)
button_3.bind("<Enter>", ravisz_3)
button_3.bind("<Leave>", levesz)
button_4.bind("<Enter>", ravisz_4)
button_4.bind("<Leave>", levesz)
button_5.bind("<Enter>", ravisz_5)
button_5.bind("<Leave>", levesz)
button_6.bind("<Enter>", ravisz_6)
button_6.bind("<Leave>", levesz)
button_7.bind("<Enter>", ravisz_7)
button_7.bind("<Leave>", levesz)
button_8.bind("<Enter>", ravisz_8)
button_8.bind("<Leave>", levesz)
button_9.bind("<Enter>", ravisz_9)
button_9.bind("<Leave>", levesz)

jobb_label_dobasok.place(x=screensize_x-158, y=34)
jobb_button_1.place(x=screensize_x-158, y=97)
jobb_button_2.place(x=screensize_x-158, y=160)
jobb_button_3.place(x=screensize_x-158, y=223)
jobb_button_4.place(x=screensize_x-158, y=286)
jobb_button_5.place(x=screensize_x-158, y=349)
jobb_button_6.place(x=screensize_x-158, y=412)
jobb_button_7.place(x=screensize_x-158, y=475)
jobb_button_8.place(x=screensize_x-158, y=538)
jobb_button_9.place(x=screensize_x-158, y=601)

gombok, jatekos_gombok, szovegek = [jobb_button_1, jobb_button_2, jobb_button_3, jobb_button_4, jobb_button_5, jobb_button_6, jobb_button_7, jobb_button_8, jobb_button_9], [button_1, button_2, button_3, button_4,button_5, button_6, button_7, button_8,button_9], ["Szemét", "Pár", "Két pár","Drill", "Full", "Kis sor","Nagy sor", "Kis póker","Nagy póker"]


dobas(dobasok, label_dobasok)
root.mainloop()
