from sklearn.tree import (DecisionTreeClassifier , plot_tree)   # Elemente aus sklearn.tree für Entscheidungsbaum-Modell und Visualisierung
from sklearn.model_selection import train_test_split            # train_test_split aus sklearn für Aufteilung der Daten in Trainings- und Testdaten

class TemperatureTrendClassifier:
    def __init__(self):
        self.model = DecisionTreeClassifier(random_state=666)   # Initialisierung des Entscheidungsbaum-Klassifikators mit einem festen random_state für (teuflisch gute) Reproduzierbarkeit
        self.accuracy = None                                    # Platzhalter für die Genauigkeit

    # Trainieren des Modells mit aufgeteilten Trainings- und Testdaten
    def train(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)   # 80% Training, 20% Test und ein random_state (mit der Antwort auf alles) für Reproduzierbarkeit
        self.model.fit(X_train, y_train)
        self.accuracy = self.model.score(X_test, y_test)    # Genauigkeitsbestimmung

    '''
    train ohne getrennte Testdaten:
    def train(self, X, y):
        self.model.fit(X, y)
    '''

    # Vorhersage
    def predict(self, features):
        return self.model.predict([features])[0]

    # Visualisierung des Entscheidungsbaums 
    def plot(self, feature_names, class_names, ax=None):
        plot_tree(
            self.model,
            feature_names=feature_names,
            class_names=class_names,
            filled=True,
            rounded=True,
            ax=ax
        )

