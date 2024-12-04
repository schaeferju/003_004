from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import sys

class CalculatorDialog(QDialog):
    
    def __init__(self):
        super().__init__()    
        self.setWindowTitle("PySide6 Calculator")
        
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        
        self.input_a = QLineEdit()
        self.input_a.setPlaceholderText("Eingabe A")  # Setzt einen Platzhaltertext.

        self.input_b = QLineEdit()
        self.input_b.setPlaceholderText("Eingabe B")  # Setzt einen Platzhaltertext.

        self.result_label = QLabel("Ergebnis: ")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 14px;")  # Textstil anpassen.

        self.add_button = QPushButton("+")  # Button für Addition.
        self.subtract_button = QPushButton("-")  # Button für Subtraktion.

        input_layout.addWidget(self.input_a)
        input_layout.addWidget(self.input_b)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.subtract_button)

        main_layout.addLayout(input_layout)  # Eingabefelder hinzufügen.
        main_layout.addLayout(button_layout)  # Buttons hinzufügen.
        main_layout.addWidget(self.result_label)  # Ergebnis-Label hinzufügen.

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add_numbers)  # Addition ausführen.
        self.subtract_button.clicked.connect(self.subtract_numbers)  # Subtraktion ausführen.

    def validate_inputs(self):
        try:
            num_a = float(self.input_a.text())  # Konvertiere Eingabe A in Float.
            num_b = float(self.input_b.text())  # Konvertiere Eingabe B in Float.
            return num_a, num_b
        except ValueError:  # Falls Eingabe keine Zahl ist.
            QMessageBox.warning(self, "Ungültige Eingabe", "Bitte geben Sie gültige Zahlen ein.")
            return None, None

    def add_numbers(self):
        num_a, num_b = self.validate_inputs()  # Eingaben validieren.
        if num_a is not None and num_b is not None:  # Nur wenn Eingaben gültig sind.
            result = num_a + num_b  # Addition durchführen.
            self.result_label.setText(f"Ergebnis: {result}")  # Ergebnis anzeigen.

    def subtract_numbers(self):        
        num_a, num_b = self.validate_inputs()  # Eingaben validieren.
        if num_a is not None and num_b is not None:  # Nur wenn Eingaben gültig sind.
            result = num_a - num_b  # Subtraktion durchführen.
            self.result_label.setText(f"Ergebnis: {result}")  # Ergebnis anzeigen.


app = QApplication(sys.argv)    # QApplication muss einmal min. existieren
myCalc = CalculatorDialog()     # Unseren Dialog erstellen, nutzt indirekt die QApplication
myCalc.show()                   # den Dialgo auf "anzeigen" stellen
sys.exit(app.exec())            # und nun tatstälich ausführe, damit er "läuft" und sichtbar wird.
