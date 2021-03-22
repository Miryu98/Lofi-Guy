import pygame
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()  # jest to po to, żeby PyGame działał

zegar = pygame.time.Clock()
fps = 60  # 60 klatek na sekunde 'frames per second'

# ekran
ekran_dlugosc = 640  # 685(38)   540  612   576(32)        (640 pikseli)
ekran_szerokosc = 640  # 798(38)   630  714   672(32)      (640 pikseli)


ekran = pygame.display.set_mode((ekran_szerokosc, ekran_dlugosc))  # ta funkcja tworzy ekran gry
pygame.display.set_caption("Lofi Guy")  # tytuł gry
ikonka = pygame.image.load("obrazki/boombox.png")
pygame.display.set_icon(ikonka)

# czcionka
czcionka = pygame.font.SysFont("Cooper Black", 35)
czcionka_tytul = pygame.font.SysFont("Cooper Black", 43)
czcionka_samouczek = pygame.font.SysFont("Cooper Black", 20)
czcionka_smierc = pygame.font.SysFont("Cooper Black", 40)
czcionka_punkty = pygame.font.SysFont("Bauhaus 93", 29)
czcionka_muzyka = pygame.font.SysFont("Cooper Black", 20)
czcionka_numer_poziomu = pygame.font.SysFont("Cooper Black", 32)

rozmiar_plytka = 32  # 20 poziomo, 20 pionowo   57 wstepnie 38  (32 pikseli)
koniec_gry = 0  # poki jest 0, to nie ma konca gry
menu_glowne = True
nr_poziom_na_ekranie = 0
poziom = 0  # zaczyna sie od samouczka
max_poziomow = 7
punkty = 0

# kolory
bialy = (255, 255, 255)
czerwony = (255, 0, 0)
niebieski = (0, 0, 255)
brazowy = (128, 0, 0)
zielony = (0, 128, 0)
pomaranczowy = (255, 69, 0)

# obrazki
tlo_obraz = pygame.image.load("Obrazki/bg.jpg")
tlo_obraz = pygame.transform.scale(tlo_obraz, (800, 685))  # rozmiar tla
restart_obr = pygame.image.load("Obrazki/restart_btn.png")
start_obr = pygame.image.load("Obrazki/start_btn.png")
start_obr = pygame.transform.scale(start_obr, (120, 42))
wyjscie_z_gry_obr = pygame.image.load("Obrazki/exit_game_btn.png")
wyjscie_z_gry_obr = pygame.transform.scale(wyjscie_z_gry_obr, (120, 42))


# muzyka w tle i dzwieki
pygame.mixer.music.load("Muzyka_dzwieki/didi-crazzz-jazz-is-always-present.mp3")
pygame.mixer.music.play(-1, 0.0, 5000)
pygame.mixer.music.set_volume(0.6)


plyta_cd_fx = pygame.mixer.Sound("Muzyka_dzwieki/plyta_cd.wav")
plyta_cd_fx.set_volume(0.3)
skok_fx = pygame.mixer.Sound("Muzyka_dzwieki/skok.wav")
skok_fx.set_volume(0.3)
koniec_gry_fx = pygame.mixer.Sound("Muzyka_dzwieki/koniec_gry.wav")
koniec_gry_fx.set_volume(0.3)
odzyskany_boombox_fx = pygame.mixer.Sound("Muzyka_dzwieki/short_triumphal_fanfare-.wav")
odzyskany_boombox_fx.set_volume(0.3)
nastepny_poziom_fx = pygame.mixer.Sound("Muzyka_dzwieki/next_level.wav")
nastepny_poziom_fx.set_volume(0.3)


def rysuj_tekst(tekst, czcionka, tekst_kolor, x, y):
    obr = czcionka.render(tekst, True, tekst_kolor)
    ekran.blit(obr, (x, y))


# funkcja na reset poziomu
def restart_poziom(poziom):
    postac.restart(36, ekran_dlugosc - 119)  # 100, 119
    sluz_grupa.empty()
    platforma_grupa.empty()
    plyta_cd_grupa.empty()
    lawa_grupa.empty()
    wyjscie_grupa.empty()
    boombox_grupa.empty()

    # wczytywanie poziomow i tworzenie swiata
    if path.exists(f"level{poziom}_data"):
        pickle_in = open(f"level{poziom}_data", "rb")
        swiat_dane = pickle.load(pickle_in)
    swiat = Swiat(swiat_dane)

    punkty_plyta_cd = Plyta(rozmiar_plytka // 2, rozmiar_plytka // 2)
    plyta_cd_grupa.add(punkty_plyta_cd)

    return swiat


class Przycisk:
    def __init__(self, x, y, obraz):
        self.image = obraz
        self.prostokat = self.image.get_rect()
        self.prostokat.x = x
        self.prostokat.y = y
        self.klikniete = False

    def rysuj(self):
        akcja = False

        # pozycja myszki
        pozycja = pygame.mouse.get_pos()

        # sprawdz ruch myszki i klikniecie
        if self.prostokat.collidepoint(pozycja):
            if pygame.mouse.get_pressed()[0] == 1 and self.klikniete == False:
                akcja = True
                self.klikniete = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.klikniete = False

        # narysuj przycisk
        ekran.blit(self.image, self.prostokat)

        return akcja


class Postac(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.restart(x, y)

    def update(self, koniec_gry):
        dx = 0
        dy = 0
        chod_spokojny = 5
        kolizja_prog = 20

        if koniec_gry == 0:
            klawisz = pygame.key.get_pressed()

            if klawisz[pygame.K_SPACE] and self.skok == False and self.w_powietrzu == False:
                skok_fx.play()
                self.predkosc_y = -11.5
                self.skok = True

            if not klawisz[pygame.K_SPACE]:
                self.skok = False

            if klawisz[pygame.K_LEFT]:
                dx -= 3.8
                self.licznik += 1
                self.kierunek = -1

            if klawisz[pygame.K_RIGHT]:
                dx += 3.8
                self.licznik += 1
                self.kierunek = 1

            if klawisz[pygame.K_LEFT] == False and klawisz[pygame.K_RIGHT] == False:
                self.licznik = 0
                self.index = 0

                if self.kierunek == 1:
                    self.obr = self.obrazy_prawo[self.index]

                if self.kierunek == -1:
                    self.obr = self.obrazy_lewo[self.index]

            # animacja
            if self.licznik > chod_spokojny:
                self.licznik = 0 # 0
                self.index += 1

                if self.index >= len(self.obrazy_prawo):
                    self.index = 0

                if self.kierunek == 1:
                    self.obr = self.obrazy_prawo[self.index]

                if self.kierunek == -1:
                    self.obr = self.obrazy_lewo[self.index]

            # grawitacja
            self.predkosc_y += 1
            if self.predkosc_y > 7:
                self.predkosc_y = 7
            dy += self.predkosc_y

            # kolizje
            self.w_powietrzu = True
            for plytka in swiat.plytka_lista:
                # sprawdz kolizjie w linii x
                if plytka[1].colliderect(self.rect.x + dx, self.rect.y, self.szerokosc, self.dlugosc):
                    dx = 0
                # sprawdz czy jest kolizja w linii y
                if plytka[1].colliderect(self.rect.x, self.rect.y + dy, self.szerokosc, self.dlugosc):
                    # sprawdz czy jest ponizej ziemi czyli skakanie
                    if self.predkosc_y < 0:
                        dy = plytka[1].bottom - self.rect.top
                        self.predkosc_y = 0
                    # sprawdz czy jest powyżej ziemi czyli spadanie
                    elif self.predkosc_y >= 0:
                        dy = plytka[1].top - self.rect.bottom
                        self.predkosc_y = 0
                        self.w_powietrzu = False


            if pygame.sprite.spritecollide(self, sluz_grupa, False):
                koniec_gry = -1
                koniec_gry_fx.play()


            if pygame.sprite.spritecollide(self, lawa_grupa, False):
                koniec_gry = -1
                koniec_gry_fx.play()


            if pygame.sprite.spritecollide(self, wyjscie_grupa, False):
                koniec_gry = 1
                nastepny_poziom_fx.play()


            if pygame.sprite.spritecollide(self, boombox_grupa, False):
                koniec_gry = 1
                odzyskany_boombox_fx.play()

            # kolizje z platformami
            for platforma in platforma_grupa:
                # kolizja na osi X
                if platforma.rect.colliderect(self.rect.x + dx, self.rect.y, self.szerokosc, self.dlugosc):
                    dx = 0
                # kolizja na osi Y
                if platforma.rect.colliderect(self.rect.x, self.rect.y + dy, self.szerokosc, self.dlugosc):
                    # sprawdz czy jest pod platforma
                    if abs((self.rect.top + dy) - platforma.rect.bottom) < kolizja_prog:
                        self.predkosc_y = 0
                        dy = platforma.rect.bottom - self.rect.top
                    # sprawdz czy jest nad platforma
                    elif abs((self.rect.bottom + dy) - platforma.rect.top) < kolizja_prog:
                        self.rect.bottom = platforma.rect.top - 1
                        self.w_powietrzu = False
                        dy = 0
                    # ruszanie sie postaci bokiem razem z platforma
                    if platforma.ruch_x != 0:
                        self.rect.x += platforma.ruch_kierunek

            # wspolrzedne postaci
            self.rect.x += dx
            self.rect.y += dy

        elif koniec_gry == -1:
            self.obr = self.smierc_obr
            rysuj_tekst("YOU ARE DEAD!", czcionka_smierc, czerwony, (ekran_szerokosc // 2) - 155, ekran_dlugosc // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        # wyswietlenie postaci na ekranie
        ekran.blit(self.obr, self.rect)
        # pygame.draw.rect(ekran, (255, 255, 255), self.rect, 2)

        return koniec_gry

    def restart(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.obrazy_prawo = []
        self.obrazy_lewo = []
        self.index = 0
        self.licznik = 0

        for licz in range(1, 4):
            obraz_prawo = pygame.image.load(f"Obrazki/player{licz}.png")
            obraz_prawo = pygame.transform.scale(obraz_prawo, (24, 64))  # 33, 73
            obraz_lewo = pygame.transform.flip(obraz_prawo, True, False)
            self.obrazy_prawo.append(obraz_prawo)
            self.obrazy_lewo.append(obraz_lewo)

        self.smierc_obr = pygame.image.load("Obrazki/ghost_dead.png")
        self.smierc_obr = pygame.transform.scale(self.smierc_obr, (33, 73))
        self.obr = self.obrazy_prawo[self.index]
        self.rect = self.obr.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.szerokosc = self.obr.get_width()
        self.dlugosc = self.obr.get_height()
        self.predkosc_y = 0
        self.skok = False
        self.kierunek = 0
        self.w_powietrzu = True


class Swiat:
    def __init__(self, dane):
        self.plytka_lista = []

        sciana_obraz = pygame.image.load("Obrazki/brickWall.png")
        trawa_obraz = pygame.image.load("Obrazki/grass.png")

        # umiejscowienie platform na ekranie
        wiersz_licz = 0
        for wiersz in dane:
            kolumna_licz = 0
            for plytka in wiersz:
                if plytka == 1:  # sciana i sufit - BrickWall
                    obraz = pygame.transform.scale(sciana_obraz, (rozmiar_plytka, rozmiar_plytka))  # 38 na 38 pikseli (x, y)
                    obraz_prostokat = obraz.get_rect()
                    obraz_prostokat.x = kolumna_licz * rozmiar_plytka
                    obraz_prostokat.y = wiersz_licz * rozmiar_plytka
                    plytka = (obraz, obraz_prostokat)
                    self.plytka_lista.append(plytka)

                if plytka == 2:  # trawa
                    obraz = pygame.transform.scale(trawa_obraz, (rozmiar_plytka, rozmiar_plytka))
                    obraz_prostokat = obraz.get_rect()
                    obraz_prostokat.x = kolumna_licz * rozmiar_plytka
                    obraz_prostokat.y = wiersz_licz * rozmiar_plytka
                    plytka = (obraz, obraz_prostokat)
                    self.plytka_lista.append(plytka)

                if plytka == 3:  # śluz kwadrat
                    sluz = Przeciwnik(kolumna_licz * rozmiar_plytka, wiersz_licz * rozmiar_plytka + 12)  # 13
                    sluz_grupa.add(sluz)

                if plytka == 4:  # platforma ruszajaca sie po linii x (lewo i prawo)
                    platforma = Platforma(kolumna_licz * rozmiar_plytka, wiersz_licz * rozmiar_plytka, 1, 0)
                    platforma_grupa.add(platforma)

                if plytka == 5:  # platforma ruszajaca sie po linii y (gora i dol)
                    platforma = Platforma(kolumna_licz * rozmiar_plytka, wiersz_licz * rozmiar_plytka, 0, 1)
                    platforma_grupa.add(platforma)

                if plytka == 6:  # lawa
                    lawa = Lawa(kolumna_licz * rozmiar_plytka,
                                wiersz_licz * rozmiar_plytka + (rozmiar_plytka // 2))  # wspolrzedne x i y
                    lawa_grupa.add(lawa)

                if plytka == 7:  # plyta cd
                    plyta_cd = Plyta(kolumna_licz * rozmiar_plytka + (rozmiar_plytka // 2),
                                     wiersz_licz * rozmiar_plytka + (rozmiar_plytka // 2))  # wspol x i y
                    plyta_cd_grupa.add(plyta_cd)

                if plytka == 8:  # drzwi/przejscie
                    wyjscie = Drzwi(kolumna_licz * rozmiar_plytka,
                                    wiersz_licz * rozmiar_plytka - (rozmiar_plytka // 2))
                    wyjscie_grupa.add(wyjscie)
                if plytka == 9:  # boombox
                    boombox = Boombox(kolumna_licz * rozmiar_plytka, wiersz_licz * rozmiar_plytka)
                    boombox_grupa.add(boombox)
                kolumna_licz += 1
            wiersz_licz += 1

    def rysuj(self):
        for plytka in self.plytka_lista:
            ekran.blit(plytka[0], plytka[1])
        # pygame.draw.rect(ekran, (255, 255, 255), obiekt[1], 2)


class Przeciwnik(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Obrazki/slimeBlock.png")
        self.image = pygame.transform.scale(self.image, (21, 21))  # 25  25
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ruch_kierunek = 1
        self.ruch_licznik = 0

    def update(self):
        self.rect.x += self.ruch_kierunek
        self.ruch_licznik += 1
        if abs(self.ruch_licznik) > 27:  # 27
            self.ruch_kierunek *= -1
            self.ruch_licznik *= -1


class Platforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ruch_x, ruch_y):
        pygame.sprite.Sprite.__init__(self)
        obr = pygame.image.load("Obrazki/grass_half.png")
        self.image = pygame.transform.scale(obr, (rozmiar_plytka, rozmiar_plytka // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ruch_licznik = 0
        self.ruch_kierunek = 1
        self.ruch_x = ruch_x
        self.ruch_y = ruch_y

    def update(self):
        self.rect.x += self.ruch_kierunek * self.ruch_x
        self.rect.y += self.ruch_kierunek * self.ruch_y
        self.ruch_licznik += 1
        if abs(self.ruch_licznik) > 50:  # 27
            self.ruch_kierunek *= -1
            self.ruch_licznik *= -1


class Lawa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        lawa = pygame.image.load("Obrazki/liquidLavaTop.png")
        self.image = pygame.transform.scale(lawa, (rozmiar_plytka, rozmiar_plytka // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Plyta(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        plyta_cd = pygame.image.load("Obrazki/plyta_cd.png")
        self.image = pygame.transform.scale(plyta_cd, (rozmiar_plytka // 2, rozmiar_plytka // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Drzwi(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        obr = pygame.image.load("Obrazki/exit.png")
        self.image = pygame.transform.scale(obr, (rozmiar_plytka, int(rozmiar_plytka * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Boombox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        obr = pygame.image.load("Obrazki/boombox.png")
        self.image = pygame.transform.scale(obr, (rozmiar_plytka, rozmiar_plytka))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


postac = Postac(36, ekran_dlugosc - 119)  # 100

sluz_grupa = pygame.sprite.Group()
platforma_grupa = pygame.sprite.Group()
lawa_grupa = pygame.sprite.Group()
plyta_cd_grupa = pygame.sprite.Group()
boombox_grupa = pygame.sprite.Group()
wyjscie_grupa = pygame.sprite.Group()

# stworzenie plyty cd ukazujacej punktacje
punkty_plyta_cd = Plyta(rozmiar_plytka // 2, rozmiar_plytka // 2)
plyta_cd_grupa.add(punkty_plyta_cd)


# wczytywanie poziomow i tworzenie swiata
if path.exists(f"level{poziom}_data"):
    pickle_in = open(f"level{poziom}_data", "rb")
    swiat_dane = pickle.load(pickle_in)
swiat = Swiat(swiat_dane)

# stworz przyciski na ekranie
przycisk_restart = Przycisk(ekran_szerokosc // 2 - 50, ekran_dlugosc // 2 + 100, restart_obr)
start_przycisk = Przycisk(ekran_szerokosc // 2 - 250, ekran_dlugosc // 2, start_obr)
wyjscie_z_gry_przycisk = Przycisk(ekran_szerokosc // 2 + 150, ekran_dlugosc // 2, wyjscie_z_gry_obr)


# działająca pętla dla ekranu gry
dzialajacy_ekran = True
pauza = False
while dzialajacy_ekran:
    for event in pygame.event.get():  # gdy użytkownik coś robi
        if event.type == pygame.QUIT:
            dzialajacy_ekran = False  # jak klikam "X", to ekran się zamknie i petla przestanie dzialac

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            dzialajacy_ekran = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pauza = not pauza
                rysuj_tekst("PAUSE!", czcionka_smierc, czerwony, (ekran_szerokosc // 2) - 70, ekran_dlugosc // 2)
                rysuj_tekst("Press 'P' to continue", czcionka_smierc, czerwony, (ekran_szerokosc // 2) - 185,
                            (ekran_dlugosc // 2) + 50)

        pygame.display.update()

    if pauza == True:
        continue

    zegar.tick(fps)
    ekran.blit(tlo_obraz, (0, 0))

    if menu_glowne is True:
        if wyjscie_z_gry_przycisk.rysuj():  # czyli EXIT
            dzialajacy_ekran = False

        if start_przycisk.rysuj():
            menu_glowne = False

        rysuj_tekst("LOFI GUY", czcionka_tytul, zielony, (ekran_szerokosc // 2) - 110, (ekran_dlugosc // 2) - 320)
        rysuj_tekst("GET THE BOOMBOX BACK! ", czcionka_tytul, niebieski, (ekran_szerokosc // 2) - 300, (ekran_dlugosc // 2) - 230)
        rysuj_tekst("COLLECT ORANGE CDs!", czcionka_tytul, brazowy, (ekran_szerokosc // 2) - 300, ekran_dlugosc // 2 - 120)
        rysuj_tekst("Music: Didi Crazzz - 'Jazz is always present'", czcionka_muzyka, pomaranczowy,
                    (ekran_szerokosc // 2) - 290, ekran_dlugosc // 2 + 250)
    else:
        swiat.rysuj()

        if poziom == 0:
            rysuj_tekst("Move the character by pressing LEFT or RIGHT key!", czcionka_samouczek, brazowy,
                        (ekran_szerokosc // 2) - 282, ekran_dlugosc // 2 - 180)
            rysuj_tekst("Press SPACEBAR to jump!", czcionka_samouczek, brazowy,
                        (ekran_szerokosc // 2) - 282, ekran_dlugosc // 2 - 120)
            rysuj_tekst("Avoid ENEMIES and LAVA!", czcionka_samouczek, brazowy,
                        (ekran_szerokosc // 2) - 282, ekran_dlugosc // 2 - 60)
            rysuj_tekst("Press 'P' to pause the game!", czcionka_samouczek, brazowy,
                        (ekran_szerokosc // 2) - 282, ekran_dlugosc // 2)

        if koniec_gry == 0:
            nr_poziom_na_ekranie = poziom
            sluz_grupa.update()
            platforma_grupa.update()
            # update punktow
            # kolizja z plytami cd
            if pygame.sprite.spritecollide(postac, plyta_cd_grupa, True):
                punkty += 1
                plyta_cd_fx.play()
            rysuj_tekst(" X " + str(punkty), czcionka_punkty, niebieski, rozmiar_plytka - 10, 0)  # 10  5

            rysuj_tekst("Level: " + str(nr_poziom_na_ekranie), czcionka_numer_poziomu, zielony, rozmiar_plytka + 220, -4)

        sluz_grupa.draw(ekran)
        platforma_grupa.draw(ekran)
        lawa_grupa.draw(ekran)
        plyta_cd_grupa.draw(ekran)
        wyjscie_grupa.draw(ekran)
        boombox_grupa.draw(ekran)

        koniec_gry = postac.update(koniec_gry)

        # jesli postac ginie
        if koniec_gry == -1:
            if przycisk_restart.rysuj():
                swiat_dane = []
                swiat = restart_poziom(poziom)
                koniec_gry = 0
                punkty = 0

        # jesli postac ukonczyla poziom
        if koniec_gry == 1:
            # reset gry i przejscie do nastepnego poziomu
            poziom += 1
            nr_poziom_na_ekranie += 1
            if poziom <= max_poziomow:
                # reset poziom
                swiat_dane = []
                swiat = restart_poziom(poziom)
                koniec_gry = 0
            else:
                pygame.mixer.music.stop()
                rysuj_tekst("YOU GOT THE BOOMBOX BACK!", czcionka, niebieski, (ekran_szerokosc // 2) - 280,
                            (ekran_dlugosc // 2) - 50)
                rysuj_tekst("Orange CDs: " + str(punkty), czcionka, brazowy, (ekran_szerokosc // 2) - 110,
                            (ekran_dlugosc // 2) + 20)
                if przycisk_restart.rysuj():
                    pygame.mixer.music.play(-1, 0.0, 5000)
                    poziom = 1
                    # restart poziom
                    swiat_dane = []
                    swiat = restart_poziom(poziom)
                    koniec_gry = 0
                    punkty = 0
                    nr_poziom_na_ekranie = 1

    #for event in pygame.event.get():  # gdy użytkownik coś robi
     #   if event.type == pygame.QUIT:
            #dzialajacy_ekran = False  # jak klikam "X", to ekran się zamknie i petla przestanie dzialac
        #elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
         #   dzialajacy_ekran = False   # klikam Escape i ekran gry sie zamyka

    pygame.display.update()  # aktualizacja zmian jakichs dokonalismy na ekranie

pygame.quit()
