# Sammelimport der benötigten PyQt5-Klassen 
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QLineEdit, QTabWidget
)
# Matplotlib-Import für Verbindung mit PyQt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# Import für die Matplotlib-Figur
from matplotlib.figure import Figure

import sys  # Zugriff auf Systemfunktionen z.B für den Programmstart oder das Beenden der Anwendung
import os   # Zugriff auf Betriebssystemfunktionen, z.B. für Dateipfade

# Lokale Importe der Module, die die Logik für die Stadtverwaltung und Modelle enthalten
from stadt_verwaltung import StadtManager
from regression_model import CityTemperatureAnalyzer
from classification_model import TemperatureTrendClassifier

# Tab für die Regression
# Dieser Tab ermöglicht die Auswahl einer Stadt, eines Regressionsgrads und die Eingabe eines zukünftigen Jahres, um eine Temperaturprognose zu erstellen.
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
        self.city_combo.addItems(self.manager.get_stadt_namen()) # Füllt das Dropdown-Menü mit Stadtnamen
        self.degree_combo = QComboBox()
        self.degree_combo.addItems(["1", "2", "3"]) # Füllt das Dropdown-Menü mit Regressionsgraden (falls Nutzer von Voreinstellung abweichen möchte)
        self.degree_combo.setCurrentText("3")       # Setzt den Standardwert auf Grad 3 
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
        self.predict_button.clicked.connect(self.run_prediction) # Aufruf der Methode zur Durchführung der Vorhersage
        self.result_label = QLabel("")

        # Plot
        self.fig = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        # Layout zusammensetzen
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addWidget(self.predict_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    # Methode zur Durchführung der Vorhersage als Methode des Tabs für die Regression
    def run_prediction(self):
        city_name = self.city_combo.currentText()
        degree = int(self.degree_combo.currentText())

        # Eingabevalidierung, ob Jahr eine Zahl ist
        try:
            year = int(self.year_input.text())
        except ValueError:
            self.result_label.setText("Ungültiges Jahr.")
            return

        stadt = self.manager.get_stadt_by_name(city_name)  # Holt das Stadtobjekt basierend auf dem ausgewählten Stadtnamen
        # Zur Übersichtlichkeit mit Funktionen direkt in Jahre und Temperaturen aufgeteilt abgerufen
        jahre = stadt.get_years()           # Nutzt Methode des Stadtobjekts um die Jahre aus dem gesammelten DataFrame zu erhalten
        temps = stadt.get_temperatures()    # Nutzt Methode des Stadtobjekts um die Temperaturen aus dem gesammelten DataFrame zu erhalten

        # Erstellen des Modells und Vorhersage
        model = CityTemperatureAnalyzer(degree)
        model.train(jahre, temps)
        prediction = model.predict(year)

        # Ausgabe des vorhergesagten Wertes als Text
        self.result_label.setText(f"Prognose: {prediction:.2f} °C")

        # Plotausgabe
        self.ax.clear()
        self.ax.plot(jahre, temps, label="Originaldaten", linestyle='dotted')
        self.ax.plot(jahre, model.get_regression_curve(jahre), label="Regression", color="green")
        self.ax.plot(year, prediction, "ro", label=f"Prognose {year}")
        self.ax.set_title(f"Temperaturverlauf: {stadt.name}")
        self.ax.legend()
        self.canvas.draw()

# Tab für die Klassifikation
# Dieser Tab ermöglicht die Eingabe von Temperaturänderungen und Standardabweichungen, um den Temperaturtrend zu klassifizieren.
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
        self.classify_button.clicked.connect(self.run_classification) # Aufruf der Klassifikationsmethode
        self.result_label = QLabel("")

        # Entscheidungsbaum
        self.fig = Figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)

        # Layout zusammensetzen
        layout.addLayout(row1)
        layout.addWidget(self.classify_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    # Methode zur Durchführung der Klassifikation als Methode des Tabs für die Klassifikation
    def run_classification(self):
        try:
            change = float(self.input_change.text())
            std = float(self.input_std.text())
        except ValueError:
            self.result_label.setText("Ungültige Eingabe.")
            return

        X = [[s.temp_change_25y, s.temp_std] for s in self.manager.get_all()]   # benutzt die get_all-Methode des StadtManagers, um alle Städte zu erhalten, macht daraus Liste von Temperaturänderungen und Standardabweichungen
        y = [s.temp_trend for s in self.manager.get_all()]                      # benutzt die get_all-Methode des StadtManagers, um alle Städte zu erhalten, macht daraus Liste von Temperaturtrends

        # clf als Instanz der Klasse TemperatureTrendClassifier (classification_model.py)
        clf = TemperatureTrendClassifier()
        clf.train(X, y) #Training des Modells, wie es in classification_model.py definiert ist

        prediction = clf.predict([change, std]) # Vorhersage durch das trainierte Modell
        result_text = f"<b>Trend:</b> {prediction}<br>"
        # Hier wird die Genauigkeit des Modells angezeigt
        result_text += f"<br><i>Test-Genauigkeit des Modells: {clf.accuracy*100:.1f}%</i>"

        # Anzeige des verketteten Resultat-Textes
        self.result_label.setText(result_text)
  
        # Plot des Entscheidungsbaums
        self.ax.clear()
        clf.plot(["TempChange25y", "TempStd"],  list(clf.model.classes_), ax=self.ax)
        self.ax.set_title("Entscheidungsbaum")
        self.canvas.draw()

# MainWindow-Klasse, die das Hauptfenster der Anwendung darstellt
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temperaturanalyse")
        # Set up des StadtManager mit dem CSV-file (nutzt os.path, um den Pfad anzupassen, damit das klappt, wenn die csv im gleichen Ornder, wie die Scripte liegt)
        base_path = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_path, "GlobalLandTemperaturesByMajorCity_yearly_1900-2012_sigma_classified.csv")
        self.manager = StadtManager(csv_path)   # Initialisierung des StadtManagers mit dem Pfad zur CSV-Datei als festen Bestandteil des Hauptfensters -> bleibt bei Wechsel zwischen den Tabs erhalten und wird an diese Übergeben
        self.init_ui()

    # Initialisierung der UI-Elemente des Hauptfensters
    def init_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()

        self.regression_tab = RegressionTab(self.manager)           # Übergabe des initialisierten StadtManagers an die Instanz der RegressionTab-Klasse
        self.classification_tab = ClassificationTab(self.manager)   # Übergabe des initialisierten StadtManagers an die Instanz der ClassificationTab-Klasse 

        # Hinzufügen der Tabs zum TabWidget
        tabs.addTab(self.regression_tab, "Regression")
        tabs.addTab(self.classification_tab, "Klassifikation")

        layout.addWidget(tabs)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(1000, 800)
    win.show()
    sys.exit(app.exec())
