import random
from tkinter import *

root = Tk()
root.title("Kockapóker")  # cím
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.configure(bg="white")  # háttérszín

dobasok, bal_dobasok = [], []  # kockákat tárolja, a másik meg a bot kockáit


# "dob" a kockákkal
def dobas(lista, label):
    lista.clear()  # lista kiürítése
    for dobas in range(5):
        dobas = random.randint(1, 6)
        lista.append(dobas)
    label['text'] = lista
    return lista


# szemét
def szemet():
    szum = 0
    for kocka in dobasok:
        szum += kocka
    button_1['state'], button_1['text'] = DISABLED, szum
    bal_oldal()


# pár
def par():
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 2:
            button_2['text'] = sorszam * 2
    if button_2['text'] == "Pár":
        button_2['text'] = 0
    button_2['state'] = DISABLED
    bal_oldal()


# két pár
def ket_par():
    parok = []
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 2:
            parok.append(sorszam)
    parok = sorted(parok)

    try:
        szum = parok[-1] * 2 + parok[-3] * 2
    except:
        szum = 0
    button_3['text'], button_3['state'] = szum, DISABLED
    bal_oldal()


# drill
def drill():
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 3:
            button_4['text'] = sorszam * 3
    if button_4['text'] == "Drill":
        button_4['text'] = 0
    button_4['state'] = DISABLED
    bal_oldal()


# full house
def full():
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
    button_5['state'] = DISABLED
    bal_oldal()


# kis sor
def kis_sor():
    seged, kis_sor = 1, True
    while seged != 6:
        if dobasok.count(seged) == 0:
            kis_sor = False
        seged += 1
    if kis_sor:
        button_6['text'] = 15
    else:
        button_6['text'] = 0
    button_6['state'] = DISABLED
    bal_oldal()


# nagy sor
def nagy_sor():
    seged, nagy_sor = 2, True
    while seged != 7:
        if dobasok.count(seged) == 0:
            nagy_sor = False
        seged += 1
    if nagy_sor:
        button_7['text'] = 20
    else:
        button_7['text'] = 0
    button_7['state'] = DISABLED
    bal_oldal()


# kis póker
def kis_poker():
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 4:
            button_8['text'] = sorszam * 4
    if button_8['text'] == "Kis póker":
        button_8['text'] = 0
    button_8['state'] = DISABLED
    bal_oldal()


# nagy póker
def nagy_poker():
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 5:
            button_9['text'] = sorszam * 5
    if button_9['text'] == "Nagy póker":
        button_9['text'] = 0
    button_9['state'] = DISABLED
    bal_oldal()


def be_ir(button, ertek):
    button['text'], button['state'] = ertek, DISABLED


def kilep():
    root.destroy()


def ujra(gomb_lista, ellenseg_gombok, szoveg):
    for (gomb, gomb2, szo) in zip(gomb_lista, ellenseg_gombok, szoveg): gomb['state'], gomb2['state'], gomb['text'], gomb2['text'] = NORMAL, NORMAL, szo, szo


def bal_oldal():
    egyik_par, ertekek, k_sor, n_sor, lista = 0, [0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 3, 4, 5], [2, 3, 4, 5, 6], dobas(bal_dobasok, bal_label_dobasok)

    for szam in lista:
        if bal_button_1['state'] != DISABLED:   # szemét
            ertekek[0] += szam
        if bal_button_6['state'] != DISABLED:   # kis sor
            if szam in k_sor:
                k_sor.remove(szam)
        if bal_button_7['state'] != DISABLED:   # nagy sor
            if szam in n_sor:
                n_sor.remove(szam)
    if len(k_sor) == 0:
        ertekek[5] = 15
    if len(n_sor) == 0:
        ertekek[6] = 20

    for szam in range(1, 7):
        if bal_button_9['state'] != DISABLED:   # nagy póker
            if lista.count(szam) >= 5:
                ertekek[8] = szam * 5
        if bal_button_8['state'] != DISABLED:   # kis póker
            if lista.count(szam) >= 4:
                ertekek[7] = szam * 4
        if bal_button_4['state'] != DISABLED:   # drill
            if lista.count(szam) >= 3:
                ertekek[3] = szam * 3
        if bal_button_2['state'] != DISABLED:   # pár
            if lista.count(szam) >= 2:
                ertekek[1] = szam * 2
        if bal_button_5['state'] != DISABLED:   # full
            if egyik_par != 0 and egyik_par != szam and lista.count(szam) >= 3:
                ertekek[4] = (egyik_par + szam) * 2 + szam
            elif ertekek[3] != 0 and (ertekek[3] / 3) != szam and lista.count(szam) >= 2:
                ertekek[4] = ertekek[3] + (szam * 2)
        if bal_button_3['state'] != DISABLED:   # két pár
            if egyik_par != 0 and egyik_par != szam and lista.count(szam) == 2:
                ertekek[2] = (egyik_par + szam) * 2
        if lista.count(szam) >= 2:
            egyik_par = szam

    if ertekek.count(0) == 9:
        for index in range(9):
            if gombok[index]['state'] != DISABLED:
                be_ir(gombok[index], ertekek[index])
                break
    else:
        for index in range(9):
            if ertekek.index(max(ertekek)) == index:
                be_ir(gombok[index], ertekek[index])
                break


label_dobasok = Label(root, width=10, padx=40, pady=20, bg="gray", fg="white", borderwidth=4, relief="sunken")
button_1 = Button(root, text="Szemét", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=lambda: [szemet(), dobas(dobasok, label_dobasok)])
button_2 = Button(root, text="Pár", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=lambda: [par(), dobas(dobasok, label_dobasok)])
button_3 = Button(root, text="Két pár", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=lambda: [ket_par(), dobas(dobasok, label_dobasok)])
button_4 = Button(root, text="Drill", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=lambda: [drill(), dobas(dobasok, label_dobasok)])
button_5 = Button(root, text="Full", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=lambda: [full(), dobas(dobasok, label_dobasok)])
button_6 = Button(root, text="Kis sor", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=lambda: [kis_sor(), dobas(dobasok, label_dobasok)])
button_7 = Button(root, text="Nagy sor", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=lambda: [nagy_sor(), dobas(dobasok, label_dobasok)])
button_8 = Button(root, text="Kis póker", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=lambda: [kis_poker(), dobas(dobasok, label_dobasok)])
button_9 = Button(root, text="Nagy póker", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=lambda: [nagy_poker(), dobas(dobasok, label_dobasok)])
button_kilep = Button(root, text="Kilépés", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=kilep)
button_ujra = Button(root, text="Újrakezdés", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=lambda: ujra(jatekos_gombok, gombok, szovegek))

space = Label(root, width=230, bg="white", fg="white")

bal_label_dobasok = Label(root, width=10, padx=40, pady=20, bg="gray", fg="white", borderwidth=4, relief="sunken")
bal_button_1 = Button(root, text="Szemét", width=10, padx=40, pady=20, bg="gray", fg="yellow")
bal_button_2 = Button(root, text="Pár", width=10, padx=40, pady=20, bg="gray", fg="yellow")
bal_button_3 = Button(root, text="Két pár", width=10, padx=40, pady=20, bg="gray", fg="yellow")
bal_button_4 = Button(root, text="Drill", width=10, padx=40, pady=20, bg="gray", fg="yellow")
bal_button_5 = Button(root, text="Full", width=10, padx=40, pady=20, bg="gray", fg="yellow")
bal_button_6 = Button(root, text="Kis sor", width=10, padx=40, pady=20, bg="gray", fg="yellow")
bal_button_7 = Button(root, text="Nagy sor", width=10, padx=40, pady=20, bg="gray", fg="yellow")
bal_button_8 = Button(root, text="Kis póker", width=10, padx=40, pady=20, bg="gray", fg="yellow")
bal_button_9 = Button(root, text="Nagy póker", width=10, padx=40, pady=20, bg="gray", fg="yellow")

label_dobasok.grid(row=0, column=0)
button_1.grid(row=1, column=0)
button_2.grid(row=2, column=0)
button_3.grid(row=3, column=0)
button_4.grid(row=4, column=0)
button_5.grid(row=5, column=0)
button_6.grid(row=6, column=0)
button_7.grid(row=7, column=0)
button_8.grid(row=8, column=0)
button_9.grid(row=9, column=0)
button_kilep.grid(row=10, column=0)
button_ujra.grid(row=11, column=0)
space.grid(row=0, column=1)
bal_label_dobasok.grid(row=0, column=2)
bal_button_1.grid(row=1, column=2)
bal_button_2.grid(row=2, column=2)
bal_button_3.grid(row=3, column=2)
bal_button_4.grid(row=4, column=2)
bal_button_5.grid(row=5, column=2)
bal_button_6.grid(row=6, column=2)
bal_button_7.grid(row=7, column=2)
bal_button_8.grid(row=8, column=2)
bal_button_9.grid(row=9, column=2)

gombok, jatekos_gombok, szovegek = [bal_button_1, bal_button_2, bal_button_3, bal_button_4, bal_button_5, bal_button_6, bal_button_7, bal_button_8, bal_button_9], [button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9], ["Szemét", "Pár", "Két pár", "Drill", "Full", "Kis sor", "Nagy sor", "Kis póker", "Nagy póker"]

dobas(dobasok, label_dobasok)
root.mainloop()
