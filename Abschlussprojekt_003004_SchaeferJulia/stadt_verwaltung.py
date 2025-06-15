import pandas as pd
from stadt import Stadt

class StadtManager:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path).dropna(subset=["Temperature"])
        self.staedte = self._erstelle_alle_stadtobjekte()

    def _erstelle_alle_stadtobjekte(self):
        stadt_liste = []
        for city in self.df["City"].unique():
            stadt_df = self.df[self.df["City"] == city].copy()
            temp_df = stadt_df[["Year", "Temperature"]].dropna().sort_values("Year")
            first_row = stadt_df.iloc[0]

            stadt = Stadt(
                name=first_row["City"],
                country=first_row["Country"],
                latitude=first_row["Latitude"],
                longitude=first_row["Longitude"],
                temp_df=temp_df,
                temp_change_25y=first_row["TempChange25y"],
                temp_std=first_row["TempStd"],
                temp_trend=first_row["TempTrend"]
            )
            stadt_liste.append(stadt)

        return stadt_liste

    def get_stadt_by_name(self, name):
        for stadt in self.staedte:
            if stadt.name == name:
                return stadt
        return None

    def get_stadt_namen(self):
        return sorted([s.name for s in self.staedte])
    
    def get_all(self):
        return self.staedte
