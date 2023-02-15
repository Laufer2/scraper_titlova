import urllib.parse
import urllib.request
import urllib.error
import bs4 as bs


def kreiraj_zahtjev(url, film, jezik=""):
    parametri = {
        '?prijevod': film,
        'jezik': jezik}
    podaci = urllib.parse.urlencode(parametri, safe='?')
    url = urllib.parse.urljoin(url, podaci)
    zahtjev = urllib.request.Request(url)
    return zahtjev


def posalji_zahtjev(zahtjev):
    try:
        zahtjev.add_header('User-Agent', 'Mozilla/5.0')
        odgovor = urllib.request.urlopen(zahtjev)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print('Poslužitelj nije mogao izvršiti zahtjev. Kod greške: ' +
              str(e.code) + ' Razglog: ' + e.reason)
        return 0
    return odgovor


def parsiranje(odgovor):
    web_dokument = odgovor.read().decode('utf-8')
    soup = bs.BeautifulSoup(web_dokument, 'html.parser')
    return soup


def obrada_odgovora(soup):
    neobradjena_lista = soup.select('section.titlovi > ul > li')
    lista_titlova = {}
    for titl in neobradjena_lista:
        anchor = titl.find('a', href=True)
        link = (anchor['href'])
        ime_filma = anchor.text
        godina = titl.find('i').text
        titl.find('span').extract()
        tip = titl.find('h4').text
        lista_titlova[link] = ime_filma + godina + " - " + tip
    return lista_titlova


def menu():
    unos = 9
    while unos != 0:
        print("1. Pretraga titlova")
        print("0. Izlaz")
        unos = int(input("Odaberi: "))
        redni_broj = 1

        if unos == 1:
            ime_filma = input("Ime filma(eng): ")
            jezik = input("Jezik titla: ")
            zahtjev = kreiraj_zahtjev(url, ime_filma, jezik)
            odgovor = posalji_zahtjev(zahtjev)

            if odgovor:
                soup = parsiranje(odgovor)
                broj_rezultata = soup.select_one('.results_count > b')
                if int(broj_rezultata.text):
                    lista_titlova = obrada_odgovora(soup)
                    for link, ime in lista_titlova.items():
                        print(str(redni_broj) + ". " + ime + " -> " +
                              urllib.parse.urljoin(url, link))
                        redni_broj += 1
                else:
                    print("Nema titlova za navedeni film.")
        else:
            exit()


url = "https://titlovi.com/titlovi/"
menu()
