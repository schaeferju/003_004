# ------------------------------------------------
# AA2_HandyNavigation.py
#
# Enthält die beispielhafte Implementierung eines objektorientierten Modells einer Navigationsanwendung auf Smart Devices (Smartphone oder Tablet).
# Es werden verschiedene Klassen definiert, die in einem mobil genutzten Navigationssystem eine Rolle spielen:
# - NavigationsApp nutzt einen NavigationsAlgorithmus zur Routenberechnung und einen Kartenspeicher, der die aktuell geladene Karte enthält
# - NavigationsApp greift über einen Kartendienst (z. B. Google Kartenserver) auf Kartendaten zu, die im Kartenspeicher abgelegt werden.
# - Auf Smartphone und Tablet kann die NavigationsApp installiert werden.
# Das Hauptprogramm zeigt, wie zwei Geräte (ein Smartphone und ein Tablet) jeweils eine eigene NavigationsApp installieren, Karten erweitern und Routen berechnen.
# Die Implementierung der Methoden liegt nur beispielhaft vor.
#
# ------------------------------------------------


# ------------------------------------------------
# Module:
# ------------------------------------------------
import numpy as np


# ------------------------------------------------
# Klassendefinitionen:
# ------------------------------------------------

class NavigationsAlgorithmus:
    def __init__(self, fortbewegungsmittel_init):
        self.fortbewegungsmittel = fortbewegungsmittel_init         # Das zur Routenberechnung zugrunde gelegt Fortbewegungsmittel

    def berechneRoute(self, start, ziel):
        print(f"Route wird berechnet von {start} nach {ziel}.")

class Kartenspeicher:
    def __init__(self):
        self.laengeBreite = np.array([500, 1000])                   # Länge und Breite des Kartenausschnitts, der im Speicher liegt (initial mit der Größe 500 x 1000)

class NavigationsApp(): 
    def __init__(self, name_init):
        self.name = name_init                                           # Name der App
        self.autoRoutenAlgo = NavigationsAlgorithmus("Automobil")       # Navigationsalgorithmus für Automobil
        self.aktuelleKarte = Kartenspeicher()                           # aktuell geladene Karte

    def erweitereKarte(self, kartendienst):                             # erweitert die aktuell geladenen Karte
        neuerKartenabschnitt = kartendienst.ladeKartenabschnitt()
        self.aktuelleKarte.laengeBreite += neuerKartenabschnitt


class Kartendienst:     
    def __init__(self, serverDomain_init):
        self.serverDomain = serverDomain_init           # Domain name des Kartendienstes

    def ladeKartenabschnitt(self):                      # stellt neue Kartenabschnitte zur Verfügung
        return np.array([200, 0])                       # der neue Kartenabschnitt hat eine fixe Größe
    

class SmartDevice:
    def __init__(self, modell_init):
        self.modell = modell_init                       # Modell des smart device
        self.navigationsApp = None                      # Installierte NavigationsApp, bei Initialisierung noch nicht vorhanden ( = None)

    def navigationsAppInstallieren(self, app):          # installiet NavigagtionsApp
        self.navigationsApp = app


class Smartphone(SmartDevice):
    def anrufen(self, gespraechspartner):               # beispielhafte Zusatzfunktion im Smartphone
        print(f"{gespraechspartner} wird angerufen.")

class Tablet(SmartDevice):
    pass



# ------------------------------------------------
# Hauptprogramm:
# ------------------------------------------------

# Instanziierung von Objekten der obigen Klassen:

handyPrivat = Smartphone("Samsung Galaxy")
tabletPrivat = Tablet("Lenovo Tab")

googleKartendienst = Kartendienst("maps.googleapis.com")

GoogleMapsApp1 = NavigationsApp("Maps for Smartphone")
GoogleMapsApp2 = NavigationsApp("Maps for Tablet")
print()


# 1. Beispielaufrufe handyPrivat

# - GoogleMapsApp1 auf handyPrivat installieren. Namen der installierten NavigationsApp ausgeben lassen.:
handyPrivat.navigationsAppInstallieren(GoogleMapsApp1)
print(f"Navigationsanwendung in {handyPrivat.modell}: {handyPrivat.navigationsApp.name}")

# - Karte der NavigationsApp auf handyPrivat erweitern und neue Größe der Karte ausgeben lassen:
handyPrivat.navigationsApp.erweitereKarte(googleKartendienst)
print(f"Groesse der aktuell geladenen Karte in {handyPrivat.modell}: {handyPrivat.navigationsApp.aktuelleKarte.laengeBreite}")

# - Route für Auto auf NavigationsApp des handyPrivat berechnen:
handyPrivat.navigationsApp.autoRoutenAlgo.berechneRoute("Trier", "Bonn")
print()


# 2. Beispielaufrufe tabletPrivat:

# - GoogleMapsApp2 auf tabletPrivat installieren. Namen der installierten NavigationsApp ausgeben lassen.:
tabletPrivat.navigationsAppInstallieren(GoogleMapsApp2)
print(f"Navigationsanwendung in {tabletPrivat.modell}: {tabletPrivat.navigationsApp.name}")

# - Karte der NavigationsApp auf tabletPrivat erweitern und neue Größe der Karte ausgeben lassen:
tabletPrivat.navigationsApp.erweitereKarte(googleKartendienst)
tabletPrivat.navigationsApp.erweitereKarte(googleKartendienst)
print(f"Groesse der aktuell geladenen Karte in {tabletPrivat.modell}: {tabletPrivat.navigationsApp.aktuelleKarte.laengeBreite}")

# - Route für Auto auf NavigationsApp des tabletPrivat berechnen:
tabletPrivat.navigationsApp.autoRoutenAlgo.berechneRoute("Trier", "Münster")
print()