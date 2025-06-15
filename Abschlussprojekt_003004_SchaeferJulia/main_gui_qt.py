from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QLineEdit, QTabWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import sys

from stadt_verwaltung import StadtManager
from regression_model import CityTemperatureAnalyzer
from classification_model import TemperatureTrendClassifier

class RegressionTab(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Auswahlfelder
        row1 = QHBoxLayout()
        self.city_combo = QComboBox()
        self.city_combo.addItems(self.manager.get_stadt_namen())
        self.degree_combo = QComboBox()
        self.degree_combo.addItems(["1", "2", "3"])
        row1.addWidget(QLabel("Stadt:"))
        row1.addWidget(self.city_combo)
        row1.addWidget(QLabel("Regressionsgrad:"))
        row1.addWidget(self.degree_combo)

        # Jahr
        row2 = QHBoxLayout()
        self.year_input = QLineEdit()
        row2.addWidget(QLabel("Zukünftiges Jahr:"))
        row2.addWidget(self.year_input)

        # Button & Ergebnis
        self.predict_button = QPushButton("Vorhersage starten")
        self.predict_button.clicked.connect(self.run_prediction)
        self.result_label = QLabel("")

        # Plot
        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        # Layout zusammensetzen
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addWidget(self.predict_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def run_prediction(self):
        city_name = self.city_combo.currentText()
        degree = int(self.degree_combo.currentText())
        try:
            year = int(self.year_input.text())
        except ValueError:
            self.result_label.setText("Ungültiges Jahr.")
            return

        stadt = self.manager.get_stadt_by_name(city_name)
        jahre = stadt.get_years()
        temps = stadt.get_temperatures()

        model = CityTemperatureAnalyzer(degree)
        model.train(jahre, temps)
        prediction = model.predict(year)

        self.result_label.setText(f"Prognose: {prediction:.2f} °C")

        self.ax.clear()
        self.ax.plot(jahre, temps, label="Originaldaten", linestyle='dotted')
        self.ax.plot(jahre, model.get_regression_curve(jahre), label="Regression", color="green")
        self.ax.plot(year, prediction, "ro", label=f"Prognose {year}")
        self.ax.set_title(f"Temperaturverlauf: {stadt.name}")
        self.ax.legend()
        self.canvas.draw()


class ClassificationTab(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Eingabe
        row1 = QHBoxLayout()
        self.input_change = QLineEdit()
        self.input_std = QLineEdit()
        row1.addWidget(QLabel("TempChange25y:"))
        row1.addWidget(self.input_change)
        row1.addWidget(QLabel("TempStd:"))
        row1.addWidget(self.input_std)

        # Button & Ergebnis
        self.classify_button = QPushButton("Trend klassifizieren")
        self.classify_button.clicked.connect(self.run_classification)
        self.result_label = QLabel("")

        # Entscheidungsbaum
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)

        layout.addLayout(row1)
        layout.addWidget(self.classify_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def run_classification(self):
        try:
            change = float(self.input_change.text())
            std = float(self.input_std.text())
        except ValueError:
            self.result_label.setText("Ungültige Eingabe.")
            return

        X = [[s.temp_change_25y, s.temp_std] for s in self.manager.get_all()]
        y = [s.temp_trend for s in self.manager.get_all()]

        clf = TemperatureTrendClassifier()
        clf.train(X, y)
        prediction = clf.predict([change, std])

        self.result_label.setText(f"Trend: {prediction}")

        self.ax.clear()
        clf.plot(["TempChange25y", "TempStd"], ["Moderate warming", "Strong warming"], ax=self.ax)
        self.ax.set_title("Entscheidungsbaum")
        self.canvas.draw()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temperaturanalyse (PyQt)")
        self.manager = StadtManager("GlobalLandTemperaturesByMajorCity_yearly_1900-2012_sigma_classified.csv")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()

        self.regression_tab = RegressionTab(self.manager)
        self.classification_tab = ClassificationTab(self.manager)

        tabs.addTab(self.regression_tab, "Regression")
        tabs.addTab(self.classification_tab, "Klassifikation")

        layout.addWidget(tabs)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec())
