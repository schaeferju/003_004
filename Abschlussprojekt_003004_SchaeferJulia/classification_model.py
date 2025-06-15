from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree

class TemperatureTrendClassifier:
    def __init__(self):
        self.model = DecisionTreeClassifier()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, features):
        return self.model.predict([features])[0]

    def plot(self, feature_names, class_names, ax=None):
        plot_tree(
            self.model,
            feature_names=feature_names,
            class_names=class_names,
            filled=True,
            rounded=True,
            ax=ax
        )
