Ohjelma 'pintaalat' tekee binääritiedoston kunkin ajon jokaiselta vuodelta jään pinta-alasta kullakin aika-askelella. Ohjelma lukee sisäänpanona tekstiksi käännetyt nc-tiedostot, joihin on otettu vain haluttu muuttuja. Tekstiksi kääntämistä varten on olemassa shell-ohjelma tekstiksi.sh.

Tiedostossa pintaalavakiot.h on käyttäjän määrittämät vakiot:
AIKAASK: aika-askelten määrä luettavassa tiedostossa, tähän voi laittaa todellista suuremman luvun
KATEG: jääkategorioitten lukumäärä
KONSRAJA alaraja jääkonsentraatiolle, joka lasketaan mukaan jään pinta-alaan
PAKSRAJA alaraja jään paksuudelle, joka lasketaan mukaan pinta-alaan
LATRAJA0/LATRAJA1 (LONRAJA0/LONRAJA1) leveyspiirit (pituuspiirit) joitten väliset koordinaatit ainoastaan huomioidaan
R maapallon säde metreinä

Komentoriviargumentteina annetaan ensin ajojen nimet ja lopussa ensimmäinen ja viimeinen vuosi

Luettavien tiedostojen kansiossa on myös oltava tiedosto latlon.txt, jossa on:
1. Ensin jokaisen ruudun leveyspiiri. Arvot erotetaan pilkuilla ja pilkun on tultava myös viimeisen arvon jälkeen.
2. ';'-merkki osoittamassa leveyspiirien päättymistä
3. Ruutujen pituuspiirit vastaavalla tavalla.

Tiedosto voidaan tehdä komennoilla
ncdump -v nav_lat tiedosto.nc > latlon.txt
ncdump -v nav_lon tiedosto.nc >> latlon.txt,
kunhan lisätään pilkku viimeisten arvojen jälkeen ja poistetaan tiedostosta kaikki ylimääräinen.
_________________________________________________

TOIMINTA:

Pääfunktio on tiedostossa pintaalat.c.

Funktio lue_grid lukee kunkin ruudun leveys- ja pituuspiirit tiedostosta latlon.txt
Lasketaan funktiolla 'maapintaala' (tiedostossa maapintaala.c) jokaisen ruudun pinta-ala, joka osuu annettujen koordinaattirajojen (LATRAJA0 yms.) välille. Tämä palauttaa pinta-alat ja mukaan otettujen ruutujen indeksit.

Jokaisen ajon jokainen vuosi on eri tiedostossa. Nämä käydään läpi yksitellen seuraavasti:
1. Luetaan konsentraatiot ja paksuudet halutuista indekseistä (maapintaala-funktion palauttamat indeksit) funktiolla lue_jaa tiedostosta jaagrid.c.
2. Tehdään taulukko, 'jaassa' jossa on jokaisesta ruudusta tieto 0/1 sen mukaan, onko se jäässä. Aluksi jokaisen ruudun arvo on 0.
3. Käydään yhdellä aika-askelella jokainen ruutu läpi. Jos paksuus- ja konsentraatioraja ylittyvät, taulukkoon 'jaassa' asetetaan tälle indeksille arvoksi 1. Jos on monta jääkategoriaa, tämä kohta toistuu.
4. Lasketaan yhteen jäässä olevien ruutujen pinta-alat. Taulukkoa 'jaassa' tarvittiin siihen, ettei monen jääkategorian tapauksessa lasketa yhtä ruutua monta kertaa.
5. Toistetaan kohtia 2 – 4, niin paljon kuin on aika-askelia vuodessa.
6. Tallennetaan nämä pinta-alat tiedostoksi.
7. Toistetaan kohtia 1 – 6 niin paljon kuin on ajoja ja vuosia.

–––––––––––––––––––––––––––––––––––––––––––––––––

MUUTA:
tekstiksi.sh kääntää nc-tiedostot tekstiksi niin, että ne voidaan lukea pinta-alat.c-ohjelmalla

tee_maksimit.m hakee pinta-alat.c:n ulostuloista vuosittaiset maksimit kullakin ajolla ja tekee niistä tekstitiedoston, jossa on pinta-ala, päivä, vuosi.

plottaa_gumbel.py plottaa pinta-alat gumbel-koordinaatistossa, sovittaa niihin suoran ja tulostaa suoran kulmakertoimen ja vakiotermin. Suoran sovituksessa ei huomioida arvoja, jolloin koko Pohjanlahti on jäässä.

gumbel_toistumisajat.py lukee (ei siis laske) suoran parametrit gumbel-koordinaatistossa ja niitten perusteella laskee ja tulostaa toistumisajat halutulle pinta-alan arvolle.

gumbel_pintaalat.py on käänteinen edellisestä: lukee suoran parametrit ja laskee toistumisajat kysytylle pinta-alalle.

gumbel_plottaa_pintaalat.py plottaa yhteen kuvaajaan jokaisesta ajosta pinta-alan toistumisajan funktiona
