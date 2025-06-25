import numpy as np                                      # Numpy für Datenhandling in nparrays
from sklearn.preprocessing import PolynomialFeatures    # sklearn-Modul für Vorbereitung der Daten für die Regression
from sklearn.linear_model import LinearRegression       # sklearn-Modul für lineare Regression (wird durch Vorbereitung als polynomielle Regression nutzbar)

class CityTemperatureAnalyzer:
    def __init__(self, degree=3):   # Initialisierung der Klasse mit einem Defaultwert des Grad des Polynoms für die Regression
        self.model = None
        self.poly = PolynomialFeatures(degree)

    # Trainieren des Modells mit den Jahren und Temperaturen
    def train(self, years, temperatures):
        X = np.array(years).reshape(-1, 1)  # Formanpassung des Arrays für die Regression
        y = np.array(temperatures)
        X_poly = self.poly.fit_transform(X) # Transformation der Jahre in polynomielle Merkmale
        self.model = LinearRegression().fit(X_poly, y)  

    def predict(self, future_year):
        X_future = self.poly.transform(np.array([[future_year]])) # Transformation des zukünftigen Jahres in polynomielles Merkmal
        return self.model.predict(X_future)[0]

    # Methode zur Berechnung der Regressionskurve für eine übergebene Liste von Jahren
    def get_regression_curve(self, years):
        X = np.array(years).reshape(-1, 1)
        X_poly = self.poly.transform(X)
        return self.model.predict(X_poly)
