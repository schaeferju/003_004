import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class CityTemperatureAnalyzer:
    def __init__(self, degree=2):
        self.degree = degree
        self.model = None
        self.poly = PolynomialFeatures(degree=self.degree)

    def train(self, years, temperatures):
        X = np.array(years).reshape(-1, 1)
        y = np.array(temperatures)
        X_poly = self.poly.fit_transform(X)
        self.model = LinearRegression().fit(X_poly, y)

    def predict(self, future_year):
        X_future = self.poly.transform(np.array([[future_year]]))
        return self.model.predict(X_future)[0]

    def get_regression_curve(self, years):
        X = np.array(years).reshape(-1, 1)
        X_poly = self.poly.transform(X)
        return self.model.predict(X_poly)
