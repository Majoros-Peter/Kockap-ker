szovegek = [
    "A játék során a gép 5-5db 6 oldalú dobókockával dob neked is és az ellenfelednek is. A tieid bal oldalt, az ellenfélnek jobb oldalt lesznek kiírva ezekben a mezőben",
    "Minden dobás után a játékosnak rá kell kattintania a bal oldalon lévő gombok egyikére.",
    "Ha a dobás megfelel az adott mező szabályának, akkor a gombra rákattintva megváltozik a szövege a megfelelő értékre (pl. van 3 db 3-as, a drillre kattintva 9 pontod lesz).",
    "Minden gombra csak egyszer lehet rákattintani, tehát ha már egy gombra már rákattintottál, azt már nem lehet megváltoztatni.",
    "Az ↺ gombra rányomva a jelenlegi játék véget ér, és egy új kezdődik.",
    "Ha a dobott eredmények több helyre is jók, akkor el kell dönteni, hogy melyik gombra fogsz kattintani (pl. 3db 3-ast be lehet írni <b>9 pontért drillnek</b>, vagy <b>6 pontért párnak</b>).",
    "Előfordul, hogy dobott eredmények egyik helyre se jók. Ilyenkor rá kell kattintani az egyik gombra, attól, hogy 0 pontot fog érni.",
    "A játék akkor ér véget, ha minden gombra rákattintottál. Az nyer akinek a legtöbb pontja van.",
];

let kep = document.getElementById('img');
let div = document.getElementById('div');
let p = document.getElementById('text');
let lista = document.getElementById('lista');
let nextGomb = document.getElementById('next');
let backGomb = document.getElementById('back');
index = -1;

window.haladas = function(szam) {
    index = index + szam;
    if (index == szovegek.length) {
        nextGomb.style.visibility = "hidden";
        p.style.visibility = "hidden";
        lista.style.visibility = "visible";
        
    }else if (index == 0) {
        backGomb.style.visibility = "hidden";
        lista.style.visibility = "hidden";
        p.style.visibility = "visible";

    } else {
        nextGomb.style.visibility = "visible";
        backGomb.style.visibility = "visible";
        p.style.visibility = "visible";
        lista.style.visibility = "hidden";
    }
    kep.setAttribute('src', 'Images/' + String(index) + '.png');
    p.innerHTML = szovegek[index];
}
