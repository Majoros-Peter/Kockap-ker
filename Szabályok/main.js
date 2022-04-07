szovegek = [
    "A játék során a gép 5-5db 6 oldalú dobókockával dob neked is és az ellenfelednek is. A tieid bal oldalt, az ellenfélnek jobb oldalt lesznek kiírva ezekben a mezőben",
    "Minden dobás után a játékosnak rá kell kattintania a bal oldalon lévő gombok egyikére.",
    "Ha a dobás megfelel az adott mező szabályának, akkor a gombra rákattintva megváltozik a szövege a megfelelő értékre (pl. van 2 db 6-os, a párra kattintva 12 pontod lesz).",
    "Minden gombra csak egyszer lehet rákattintani, tehát ha már egy gombra már rákattintottál, azt már nem lehet megváltoztatni. Az ↺ gombra rányomva a jelenlegi játék véget ér, és egy új kezdődik.",
    "Ha a dobott eredmények több helyre is jók, akkor el kell dönteni, hogy melyik gombra fogsz kattintani (pl. 2db 6-ost és 2db 5-öst be lehet írni <b>12 pontért párnak</b>, vagy <b>22 pontért két párnak</b>).",
    "Előfordul, hogy dobott eredmények egyik helyre se jók. Ilyenkor rá kell kattintani az egyik gombra, attól, hogy 0 pontot fog érni.",
    "A játék akkor ér véget, ha minden gombra rákattintottál. Az nyer akinek a legtöbb pontja van.",
];

let body = document.getElementById('body');
let kep = document.getElementById('img');
let aproBetusResz = document.getElementById('aproBetusResz')
let text = document.getElementById('text');
let lista = document.getElementById('lista');
let nextGomb = document.getElementById('next');
let backGomb = document.getElementById('back');
let light = document.getElementById('light');
let dark = document.getElementById('dark');
index = -1;

window.haladas = function(szam) {
    index = index + szam;
    if (index == szovegek.length) {
        kep.style.visibility = "hidden";
        nextGomb.style.visibility = "hidden";
        text.style.visibility = "hidden";
        aproBetusResz.style.visibility = "hidden";
        lista.style.visibility = "visible";
        
    }else if (index == 0) {
        backGomb.style.visibility = "hidden";
        lista.style.visibility = "hidden";
        text.style.visibility = "visible";
        kep.style.visibility = "visible";
        aproBetusResz.style.visibility = "visible";

    } else {
        nextGomb.style.visibility = "visible";
        backGomb.style.visibility = "visible";
        text.style.visibility = "visible";
        kep.style.visibility = "visible";
        aproBetusResz.style.visibility = "visible";
        lista.style.visibility = "hidden";
    }
    kep.setAttribute('src', 'Images/' + String(index) + '.png');
    text.innerHTML = szovegek[index];
}

function darkMode() {
    body.style.backgroundColor = "rgb(45, 45, 45)";
    body.style.color = "white";
    dark.style.visibility = "hidden";
    light.style.visibility = "visible";
}

function lightMode() {
    body.style.backgroundColor = "white";
    body.style.color = "rgb(45, 45, 45)";
    light.style.visibility = "hidden";
    dark.style.visibility = "visible";
}
