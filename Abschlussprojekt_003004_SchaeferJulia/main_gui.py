import tkinter as tk
import os
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from stadt_verwaltung import StadtManager
from regression_model import CityTemperatureAnalyzer
from classification_model import TemperatureTrendClassifier

class TemperatureApp:
    def __init__(self, root):
        # Set up the StadtManager with the CSV file (using os.path to adjust the path, to always work when csy file is in the same directroy as the scripts)
        base_path = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_path, "GlobalLandTemperaturesByMajorCity_yearly_1900-2012_sigma_classified.csv")
        self.manager = StadtManager(csv_path)

        self.root = root
        self.root.title("Temperaturanalyse")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.regression_tab = ttk.Frame(self.notebook)
        self.classification_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.regression_tab, text="Regression")
        self.notebook.add(self.classification_tab, text="Klassifikation")

        self.init_regression_tab()
        self.init_classification_tab()

    def init_regression_tab(self):
        self.city_var = tk.StringVar()
        self.degree_var = tk.IntVar(value=2)

        ttk.Label(self.regression_tab, text="Stadt:").grid(row=0, column=0)
        self.city_menu = ttk.Combobox(self.regression_tab, textvariable=self.city_var, values=self.manager.get_stadt_namen(), width=30)
        self.city_menu.grid(row=0, column=1)

        ttk.Label(self.regression_tab, text="Regressionsgrad:").grid(row=1, column=0)
        self.degree_menu = ttk.Combobox(self.regression_tab, textvariable=self.degree_var, values=[1, 2, 3])
        self.degree_menu.grid(row=1, column=1)

        ttk.Label(self.regression_tab, text="Zukünftiges Jahr:").grid(row=2, column=0)
        self.year_entry = ttk.Entry(self.regression_tab)
        self.year_entry.grid(row=2, column=1)

        self.predict_button = ttk.Button(self.regression_tab, text="Vorhersage starten", command=self.predict_temperature)
        self.predict_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(self.regression_tab, text="", font=("Arial", 12))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=5)

        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.regression_tab)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)

    def predict_temperature(self):
        city_name = self.city_var.get()
        degree = self.degree_var.get()

        try:
            future_year = int(self.year_entry.get())
        except ValueError:
            self.result_label.config(text="Bitte gültiges Jahr eingeben.")
            return

        stadt = self.manager.get_stadt_by_name(city_name)
        if not stadt:
            self.result_label.config(text="Stadt nicht gefunden.")
            return

        jahre = stadt.get_years()
        temps = stadt.get_temperatures()

        analyzer = CityTemperatureAnalyzer(degree=degree)
        analyzer.train(jahre, temps)
        predicted_temp = analyzer.predict(future_year)

        self.result_label.config(text=f"Prognose für {future_year}: {predicted_temp:.2f} °C")

        self.ax.clear()
        self.ax.plot(jahre, temps, label="Originaldaten", marker='o', linestyle='dotted')
        self.ax.plot(jahre, analyzer.get_regression_curve(jahre), label=f"Regression (Grad {degree})", color='green')
        self.ax.plot(future_year, predicted_temp, 'ro', label=f"Prognose {future_year}")
        self.ax.set_title(f"Temperaturverlauf: {stadt.name}")
        self.ax.set_xlabel("Jahr")
        self.ax.set_ylabel("Temperatur (°C)")
        self.ax.legend()
        self.canvas.draw()

    def init_classification_tab(self):
        self.temp_change_var = tk.DoubleVar()
        self.temp_std_var = tk.DoubleVar()
        self.classify_result = tk.StringVar()

        ttk.Label(self.classification_tab, text="TempChange25y:").grid(row=0, column=0, sticky="e")
        ttk.Entry(self.classification_tab, textvariable=self.temp_change_var).grid(row=0, column=1)

        ttk.Label(self.classification_tab, text="TempStd:").grid(row=1, column=0, sticky="e")
        ttk.Entry(self.classification_tab, textvariable=self.temp_std_var).grid(row=1, column=1)

        ttk.Button(self.classification_tab, text="Trend klassifizieren", command=self.classify_trend).grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Label(self.classification_tab, textvariable=self.classify_result, font=("Arial", 12)).grid(row=3, column=0, columnspan=2)

        # Baum-Grafik
        self.tree_fig = Figure(figsize=(6, 4))
        self.tree_ax = self.tree_fig.add_subplot(111)
        self.tree_canvas = FigureCanvasTkAgg(self.tree_fig, master=self.classification_tab)
        self.tree_canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, pady=10)

    def classify_trend(self):
        try:
            x_input = [self.temp_change_var.get(), self.temp_std_var.get()]
        except tk.TclError:
            self.classify_result.set("Ungültige Eingaben!")
            return

        X = [[s.temp_change_25y, s.temp_std] for s in self.manager.get_all()]
        y = [s.temp_trend for s in self.manager.get_all()]

        classifier = TemperatureTrendClassifier()
        classifier.train(X, y)
        prediction = classifier.predict(x_input)

        self.classify_result.set(f"Prognostizierter Trend: {prediction}")

        # Entscheidungsbaum zeichnen
        self.tree_ax.clear()
        classifier.plot(feature_names=["TempChange25y", "TempStd"], class_names=["Moderate warming", "Strong warming"], ax=self.tree_ax)
        self.tree_ax.set_title("Entscheidungsbaum")
        self.tree_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureApp(root)
    root.mainloop()
