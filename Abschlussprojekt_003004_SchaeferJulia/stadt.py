# Klasse, die ermöglicht alle Informationen zu einer Stadt zu sortieren
class Stadt:
    def __init__(self, _name, _country, _latitude, _longitude, _temp_df, _temp_change_25y, _temp_std, _temp_trend):
        self.name = _name
        self.country = _country
        self.latitude = _latitude
        self.longitude = _longitude
        self.temp_df = _temp_df 
        self.temp_change_25y = _temp_change_25y
        self.temp_std = _temp_std
        self.temp_trend = _temp_trend

    # Rückgabe aller Jahre
    def get_years(self):
        return self.temp_df["Year"].values

    # Rückgabe aller Temperaturen
    def get_temperatures(self):
        return self.temp_df["Temperature"].values

