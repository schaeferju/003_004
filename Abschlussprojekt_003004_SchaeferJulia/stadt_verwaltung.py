import pandas as pd     # Importiere pandas für die Datenverarbeitung
from stadt import Stadt # Importiere die Stadt-Klasse, um Stadtobjekte zu erstellen

class StadtManager:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)                     # Liest die CSV-Datei am angegebenen Pfad ein
        self.staedte = self._erstelle_alle_stadtobjekte()   # Funktion in der Initialisierung, damit alle Städte in der Liste verfügbar werden

    # Diese Methode erstellt Stadtobjekte für jede Stadt in der DataFrame und speichert sie in einer Liste
    def _erstelle_alle_stadtobjekte(self):
        stadt_liste = []
        for city in self.df["City"].unique():                               # Schleife für alle einzigartigen Städte im DataFrame
            stadt_df = self.df[self.df["City"] == city].copy()              # Filtert den DataFrame für die aktuelle Stadt
            temp_df = stadt_df[["Year", "Temperature"]].sort_values("Year") # Temperaturdaten für die Stadt, sortiert nach Jahr
            first_row = stadt_df.iloc[0]                                    # Nimmt die erste Zeile des DataFrames für die aktuelle Stadt

            # Erstelle ein Stadtobjekt mit den gesammelten Informationen
            # alles mit "first_row" sind Daten die nur einmal pro Stadt benötigt werden
            # Für Übersichtlichkeit werden die Daten mit den Attributsnamen der Stadt-Klasse übergeben
            stadt = Stadt(
                _name=first_row["City"],
                _country=first_row["Country"],
                _latitude=first_row["Latitude"],
                _longitude=first_row["Longitude"],
                _temp_df=temp_df,
                _temp_change_25y=first_row["TempChange25y"],
                _temp_std=first_row["TempStd"],
                _temp_trend=first_row["TempTrend"]
            )
            # Füge das Stadtobjekt der Liste hinzu
            stadt_liste.append(stadt)

        return stadt_liste

    # Diese Methode gibt ein Stadtobjekt zurück, wenn der Name der Stadt übereinstimmt (Wird für Wertübergabe im Regressionstab genutzt)
    def get_stadt_by_name(self, name):
        for stadt in self.staedte:
            if stadt.name == name:
                return stadt
        return None

    # Diese Methode gibt eine sortierte Liste aller Stadtnamen zurück (Regressionstab nutzt diese Methode für Dropdown)
    def get_stadt_namen(self):
        return sorted([s.name for s in self.staedte])
    
    # Diese Methode gibt eine Liste aller Stadtobjekte zurück (wird für die Übergabe der Werte im Klassifikationstab genutzt)
    def get_all(self):
        return self.staedte
