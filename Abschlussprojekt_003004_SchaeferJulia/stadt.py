class Stadt:
    def __init__(self, name, country, latitude, longitude, temp_df, temp_change_25y, temp_std, temp_trend):
        self.name = name
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.temp_df = temp_df
        self.temp_change_25y = temp_change_25y
        self.temp_std = temp_std
        self.temp_trend = temp_trend

    def get_years(self):
        return self.temp_df["Year"].values

    def get_temperatures(self):
        return self.temp_df["Temperature"].values

    def __str__(self):
        return f"{self.name} ({self.country}) – Trend: {self.temp_trend}"
