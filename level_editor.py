import pygame
import pickle
from os import path

pygame.init()

zegar = pygame.time.Clock()
fps = 60

# okno gry
rozmiar_plytka = 32
kolumny = 20
margines = 35 # 35
ekran_dlugosc = (rozmiar_plytka * kolumny) + margines
ekran_szerokosc = rozmiar_plytka * kolumny


ekran = pygame.display.set_mode((ekran_szerokosc, ekran_dlugosc))
pygame.display.set_caption("Level Editor")

# wczytywanie obrazkow
tlo_obraz = pygame.image.load("Obrazki/bg.jpg")
tlo_obraz = pygame.transform.scale(tlo_obraz, (ekran_szerokosc, ekran_dlugosc - margines))
sciana_obraz = pygame.image.load("Obrazki/brickWall.png")
trawa_obraz = pygame.image.load("Obrazki/grass.png")
sluz_obraz = pygame.image.load("Obrazki/slimeBlock.png")
platforma_x_obraz = pygame.image.load("Obrazki/grass_half.png")
platforma_y_obraz = pygame.image.load("Obrazki/grass_half.png")
lawa_obraz = pygame.image.load("Obrazki/liquidLavaTop.png")
plyta_cd_obraz = pygame.image.load("Obrazki/plyta_cd.png")
boombox_obraz = pygame.image.load("Obrazki/boombox.png")
wyjscie_obraz = pygame.image.load("Obrazki/exit.png")
zapis_obraz = pygame.image.load("Obrazki/save_btn.png")
zapis_obraz = pygame.transform.scale(zapis_obraz, (50, 30))
wczytaj_obraz = pygame.image.load("Obrazki/load_btn.png")
wczytaj_obraz = pygame.transform.scale(wczytaj_obraz, (50, 30))

# zmienne gry
klikniete = False
poziom = 0

# kolory
bialy = (255, 255, 255)
zielony = (144, 201, 120)

czcionka = pygame.font.SysFont("Futura", 20)

# tworzenie pustej listy platform
swiat_dane = []
for wiersz in range(20):
    r = [0] * 20
    swiat_dane.append(r)

# tworzenie granicy
for plytka in range(0, 20):
    swiat_dane[19][plytka] = 2  # 2
    swiat_dane[0][plytka] = 1
    swiat_dane[plytka][0] = 1
    swiat_dane[plytka][19] = 1

# funkcja wyprowadzajaca tekst na ekran
def rysuj_tekst(tekst, czcionka, tekst_kolor, x, y):
    obr = czcionka.render(tekst, True, tekst_kolor)
    ekran.blit(obr, (x, y))


def rysuj_siatka():
    for c in range(21):
        # pionowe linie
        pygame.draw.line(ekran, bialy, (c * rozmiar_plytka, 0), (c * rozmiar_plytka, ekran_dlugosc - margines))
        # poziome linie
        pygame.draw.line(ekran, bialy, (0, c * rozmiar_plytka), (ekran_szerokosc, c * rozmiar_plytka))


def rysuj_swiat():
    for wiersz in range(20):
        for kolumna in range(20):
            if swiat_dane[wiersz][kolumna] > 0:
                if swiat_dane[wiersz][kolumna] == 1:
                    # sciana bloki
                    obr = pygame.transform.scale(sciana_obraz, (rozmiar_plytka, rozmiar_plytka))
                    ekran.blit(obr, (kolumna * rozmiar_plytka, wiersz * rozmiar_plytka))

                if swiat_dane[wiersz][kolumna] == 2:
                    # trawa
                    obr = pygame.transform.scale(trawa_obraz, (rozmiar_plytka, rozmiar_plytka))
                    ekran.blit(obr, (kolumna * rozmiar_plytka, wiersz * rozmiar_plytka))

                if swiat_dane[wiersz][kolumna] == 3:
                    # przeciwnicy
                    obr = pygame.transform.scale(sluz_obraz, (rozmiar_plytka, int(rozmiar_plytka * 0.75)))
                    ekran.blit(obr, (kolumna * rozmiar_plytka, wiersz * rozmiar_plytka + (rozmiar_plytka * 0.25)))

                if swiat_dane[wiersz][kolumna] == 4:
                    # platformy poruszajace sie poziomo
                    obr = pygame.transform.scale(platforma_x_obraz, (rozmiar_plytka, rozmiar_plytka // 2))
                    ekran.blit(obr, (kolumna * rozmiar_plytka, wiersz * rozmiar_plytka))

                if swiat_dane[wiersz][kolumna] == 5:
                    # platformy poruszajace sie pionowo
                    obr = pygame.transform.scale(platforma_y_obraz, (rozmiar_plytka, rozmiar_plytka // 2))
                    ekran.blit(obr, (kolumna * rozmiar_plytka, wiersz * rozmiar_plytka))

                if swiat_dane[wiersz][kolumna] == 6:
                    # lawa
                    obr = pygame.transform.scale(lawa_obraz, (rozmiar_plytka, rozmiar_plytka // 2))
                    ekran.blit(obr, (kolumna * rozmiar_plytka, wiersz * rozmiar_plytka + (rozmiar_plytka // 2)))

                if swiat_dane[wiersz][kolumna] == 7:
                    # plyta CD
                    obr = pygame.transform.scale(plyta_cd_obraz, (rozmiar_plytka // 2, rozmiar_plytka // 2))
                    ekran.blit(obr, ((kolumna * rozmiar_plytka) + 8, wiersz * rozmiar_plytka - (rozmiar_plytka // 100)))

                if swiat_dane[wiersz][kolumna] == 8:
                    # drzwi wyjscie
                    obr = pygame.transform.scale(wyjscie_obraz, (rozmiar_plytka, int(rozmiar_plytka * 1.5)))
                    ekran.blit(obr,
                               (kolumna * rozmiar_plytka, wiersz * rozmiar_plytka - (rozmiar_plytka // 1.8)))

                if swiat_dane[wiersz][kolumna] == 9:
                    # boombox
                    obr = pygame.transform.scale(boombox_obraz, (rozmiar_plytka, rozmiar_plytka))
                    ekran.blit(obr, (kolumna * rozmiar_plytka, wiersz * rozmiar_plytka))


class Przycisk:
    def __init__(self, x, y, obraz):
        self.image = obraz
        self.prostokat = self.image.get_rect()
        self.prostokat.topleft = (x, y)
        self.klikniete = False

    def rysuj(self):
        akcja = False

        # pozycja kursora
        pozycja = pygame.mouse.get_pos()

        # sprawdz ruch kursora i klikniecie
        if self.prostokat.collidepoint(pozycja):
            if pygame.mouse.get_pressed()[0] and self.klikniete == False:
                akcja = True
                self.klikniete = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.klikniete = False

        # przycisk rysuj
        ekran.blit(self.image, (self.prostokat.x, self.prostokat.y))

        return akcja

# tworzenie przyciskow ladowania i zapisu
zapis_przycisk = Przycisk(ekran_szerokosc // 2 + 30, ekran_dlugosc - 32, zapis_obraz)
wczytaj_przycisk = Przycisk(ekran_szerokosc // 2 + 150, ekran_dlugosc - 32, wczytaj_obraz)

# glowna petla gry
dzialajacy_ekran = True

while dzialajacy_ekran:
    zegar.tick(fps)

    # rysuj tlo
    ekran.fill(zielony)
    ekran.blit(tlo_obraz, (0, 0))

    # wczytanie i zapis poziomu
    if zapis_przycisk.rysuj():
        pickle_out = open(f"level{poziom}_data", "wb")
        pickle.dump(swiat_dane, pickle_out)
        pickle_out.close()
    if wczytaj_przycisk.rysuj():
        if path.exists(f"level{poziom}_data"):
            pickle_in = open(f"level{poziom}_data", "rb")
            swiat_dane = pickle.load(pickle_in)

    # pokazanie siatki i wstawianie platform do poziomow
    rysuj_siatka()
    rysuj_swiat()

    # tekst pokazujacy obecny poziom
    rysuj_tekst(f"Level: {poziom}", czcionka, bialy, rozmiar_plytka, ekran_dlugosc - 34)  # 60
    rysuj_tekst("Press UP or DOWN key to change the level", czcionka, bialy, rozmiar_plytka, ekran_dlugosc - 14)  # 40

    # modul obslugi zdarzen
    for event in pygame.event.get():
        # wyjscie z gry
        if event.type == pygame.QUIT:
            dzialajacy_ekran = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            dzialajacy_ekran = False

        # zmiana platform przez klikniecie myszka
        if event.type == pygame.MOUSEBUTTONDOWN and klikniete == False:
            klikniete = True
            pozycja = pygame.mouse.get_pos()
            x = pozycja[0] // rozmiar_plytka
            y = pozycja[1] // rozmiar_plytka
            # sprawdz czy wspolrzedne sa w obszarze platformy
            if x < 20 and y < 20:
                # update wartosc platformy
                if pygame.mouse.get_pressed()[0] == 1:
                    swiat_dane[y][x] += 1
                    if swiat_dane[y][x] > 9:
                        swiat_dane[y][x] = 0
        if event.type == pygame.MOUSEBUTTONUP:
            klikniete = False
        # strzalka w gore i w dol do zmiany numeru poziomu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                poziom += 1
            elif event.key == pygame.K_DOWN and poziom > 0:
                poziom -= 1

    # update okna wyswietlania gry
    pygame.display.update()

pygame.quit()
