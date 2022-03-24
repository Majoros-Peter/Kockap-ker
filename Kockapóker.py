import random
from tkinter import *

root = Tk()
root.title("Kockapóker")  # cím
root.geometry("1000x1000")  # ablak mérete

dobasok = []  # kockákat tárolja


# "dob" a kockákkal
def dobas(lista):
    lista.clear()  # lista kiürítése
    '''try:
        if int(entry_kockak_szama.get()) < 10 and int(entry_kockak_szama.get()) > 4:
            for dobas in range(int(entry_kockak_szama.get())):
                dobas = random.randint(1, 6)
                lista.append(dobas)
        else:
            for dobas in range(5):
                dobas = random.randint(1, 6)
                lista.append(dobas)
    except:'''
    for dobas in range(5):
        dobas = random.randint(1, 6)
        lista.append(dobas)
    label_dobasok['text'] = lista
    return lista


# szemét
def megnyom_1():
    szum = 0
    for kocka in dobasok:
        szum += kocka
    button_1['state'] = DISABLED
    button_1['text'] = szum
    dobas(dobasok)


# pár
def megnyom_2():
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 2:
            button_2['text'] = sorszam * 2
    if button_2['text'] == "Pár":
        button_2['text'] = 0
    button_2['state'] = DISABLED
    dobas(dobasok)


# két pár
def megnyom_3():
    parok = []
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 2:
            parok.append(sorszam)
    parok = sorted(parok)

    try:
        szum = parok[-1] * 2 + parok[-3] * 2
    except:
        szum = 0
    button_3['text'] = szum
    button_3['state'] = DISABLED
    dobas(dobasok)


# drill
def megnyom_4():
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 3:
            button_4['text'] = sorszam * 3
    if button_4['text'] == "Drill":
        button_4['text'] = 0
    button_4['state'] = DISABLED
    dobas(dobasok)


# full house
def megnyom_5():
    par = 0
    drill = 0
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
    dobas(dobasok)


# kis sor
def megnyom_6():
    seged = 1
    kis_sor = True
    while seged != 6:
        if dobasok.count(seged) == 0:
            kis_sor = False
        seged += 1
    if kis_sor:
        button_6['text'] = 15
    else:
        button_6['text'] = 0
    button_6['state'] = DISABLED
    dobas(dobasok)


# nagy sor
def megnyom_7():
    seged = 2
    nagy_sor = True
    while seged != 7:
        if dobasok.count(seged) == 0:
            nagy_sor = False
        seged += 1
    if nagy_sor:
        button_7['text'] = 20
    else:
        button_7['text'] = 0
    button_7['state'] = DISABLED
    dobas(dobasok)


# kis póker
def megnyom_8():
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 4:
            button_8['text'] = sorszam * 4
    if button_8['text'] == "Kis póker":
        button_8['text'] = 0
    button_8['state'] = DISABLED
    dobas(dobasok)


# nagy póker
def megnyom_9():
    for sorszam in dobasok:
        if dobasok.count(sorszam) >= 5:
            button_9['text'] = sorszam * 5
    if button_9['text'] == "Nagy póker":
        button_9['text'] = 0
    button_9['state'] = DISABLED
    dobas(dobasok)


def kilep():
    root.destroy()


label_dobasok = Label(root, width=10, padx=40, pady=20, bg="gray", fg="white", borderwidth=4, relief="sunken")
#entry_kockak_szama = Entry(root, width=10, bg="gray", fg="white", borderwidth=4, relief="sunken")                  W.I.P.
button_1 = Button(root, text="Szemét", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=megnyom_1)
button_2 = Button(root, text="Pár", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=megnyom_2)
button_3 = Button(root, text="Két pár", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=megnyom_3)
button_4 = Button(root, text="Drill", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=megnyom_4)
button_5 = Button(root, text="Full", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=megnyom_5)
button_6 = Button(root, text="Kis sor", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=megnyom_6)
button_7 = Button(root, text="Nagy sor", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=megnyom_7)
button_8 = Button(root, text="Kis póker", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=megnyom_8)
button_9 = Button(root, text="Nagy póker", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=megnyom_9)
button_kilep = Button(root, text="Kilépés", width=10, padx=40, pady=20, bg="gray", fg="yellow", command=kilep)

#entry_kockak_szama.grid(row=0, column=2)   W.I.P.
label_dobasok.grid(row=0, column=1)
button_1.grid(row=1, column=1)
button_2.grid(row=2, column=1)
button_3.grid(row=3, column=1)
button_4.grid(row=4, column=1)
button_5.grid(row=5, column=1)
button_6.grid(row=6, column=1)
button_7.grid(row=7, column=1)
button_8.grid(row=8, column=1)
button_9.grid(row=9, column=1)
button_kilep.grid(row=10, column=1)

dobas(dobasok)
root.attributes('-fullscreen', True)
root.mainloop()
