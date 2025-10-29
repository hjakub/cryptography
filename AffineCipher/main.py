import sys
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QDialog


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("sifra_gui.ui", self)

        # button_over
        self.button_over.clicked.connect(self.buttonclick_over)

        # button_zasifruj
        self.button_zasifruj.clicked.connect(self.buttonclick_zasifruj)

        # button_desifruj
        self.button_desifruj.clicked.connect(self.buttonclick_desifruj)

        # button_abeceda
        self.button_abeceda.clicked.connect(self.buttonclick_abeceda)

    def buttonclick_zasifruj(self):
        input_text = str(self.input_otevreny.toPlainText())
        key_a = int(self.input_a.toPlainText())
        key_b = int(self.input_b.toPlainText())
        filtered_text = filter_text(input_text)
        encrypted_text = encrypt(filtered_text, key_a, key_b)
        self.output_filtrovany.setText(str(filtered_text))
        self.output_sifrovany.setText(str(encrypted_text))

    def buttonclick_desifruj(self):
        encrypted_text = str(self.input_sifrovany.toPlainText())
        key_a = int(self.input_a.toPlainText())
        key_b = int(self.input_b.toPlainText())
        decrypted_text = decrypt(encrypted_text, key_a, key_b)
        otevreny_text = open_text(decrypted_text)
        self.output_desifrovany.setText(str(decrypted_text))
        self.output_otevreny.setText(str(otevreny_text))

    def buttonclick_over(self):
        key_a = int(self.input_a.toPlainText())
        mod_inverse_a = mod_inverse(key_a, 26)
        if mod_inverse_a is None:
            self.overeni_ne.setText("NE")
            self.overeni_ano.setText("")
        else:
            self.overeni_ano.setText("ANO")
            self.overeni_ne.setText("")

    def buttonclick_abeceda(self):
        key_a = int(self.input_a.toPlainText())
        key_b = int(self.input_b.toPlainText())
        abeceda = [{"z": "A", "s": str(encrypt("A", key_a, key_b))}, {"z": "B", "s": str(encrypt("B", key_a, key_b))},
                   {"z": "C", "s": str(encrypt("C", key_a, key_b))}, {"z": "D", "s": str(encrypt("D", key_a, key_b))},
                   {"z": "E", "s": str(encrypt("E", key_a, key_b))}, {"z": "F", "s": str(encrypt("F", key_a, key_b))},
                   {"z": "G", "s": str(encrypt("G", key_a, key_b))}, {"z": "H", "s": str(encrypt("H", key_a, key_b))},
                   {"z": "I", "s": str(encrypt("I", key_a, key_b))}, {"z": "J", "s": str(encrypt("J", key_a, key_b))},
                   {"z": "K", "s": str(encrypt("K", key_a, key_b))}, {"z": "L", "s": str(encrypt("L", key_a, key_b))},
                   {"z": "M", "s": str(encrypt("M", key_a, key_b))}, {"z": "N", "s": str(encrypt("N", key_a, key_b))},
                   {"z": "O", "s": str(encrypt("O", key_a, key_b))}, {"z": "P", "s": str(encrypt("P", key_a, key_b))},
                   {"z": "Q", "s": str(encrypt("Q", key_a, key_b))}, {"z": "R", "s": str(encrypt("R", key_a, key_b))},
                   {"z": "S", "s": str(encrypt("S", key_a, key_b))}, {"z": "T", "s": str(encrypt("T", key_a, key_b))},
                   {"z": "U", "s": str(encrypt("U", key_a, key_b))}, {"z": "V", "s": str(encrypt("V", key_a, key_b))},
                   {"z": "W", "s": str(encrypt("W", key_a, key_b))}, {"z": "X", "s": str(encrypt("X", key_a, key_b))},
                   {"z": "Y", "s": str(encrypt("Y", key_a, key_b))}, {"z": "Z", "s": str(encrypt("Z", key_a, key_b))}]
        column = 0
        for znak in abeceda:
            self.table.setItem(0, column, QtWidgets.QTableWidgetItem(znak["z"]))
            self.table.setItem(1, column, QtWidgets.QTableWidgetItem(znak["s"]))
            column = column + 1


def filter_text(text):
    # Prevod vsech pismen na velka
    text = text.upper()

    # Odstraneni diakritiky
    diacritics = {'Á': 'A', 'Â': 'A', 'Ä': 'A', 'Ą': 'A', 'Ā': 'A', 'Č': 'C', 'Ć': 'C', 'Ď': 'D', 'É': 'E', 'Ę': 'E',
                  'Ê': 'E', 'Ė': 'E', 'Ě': 'E', 'Ē': 'E', 'Ģ': 'G', 'Í': 'I', 'Į': 'I', 'Ī': 'I', 'Ķ': 'K', 'Ļ': 'L',
                  'Ł': 'L', 'Ň': 'N', 'Ņ': 'N', 'Ń': 'N', 'Ó': 'O', 'Ö': 'O', 'Ō': 'O', 'Ô': 'O', 'Ø': 'O', 'Ř': 'R',
                  'Š': 'S', 'Ś': 'S', 'ẞ': 'SS', 'Ť': 'T', 'Ú': 'U', 'Ů': 'U', 'Ü': 'U', 'Û': 'U', 'Ų': 'U', 'Ū': 'U',
                  'Ý': 'Y', 'Ž': 'Z', 'Ż': 'Z'}
    for char in diacritics:
        text = text.replace(char, diacritics[char])

    # Odstraneni carek, otazniku, vykricniku, apod.s
    diacritics = {',', "'", '"', '.', '!', '?', '-', '+', '#', 'ˇ', '>', '<', '(', ')', '/', '%', ':', '&', ';', '~',
                  '@', '}', '{', '[', ']', '*', '^', '°', '_'}
    for char in diacritics:
        text = text.replace(char, '')

    return text


def open_text(text):
    # Nahrazeni mezer a pismen
    text = text.replace('XMEZERAX', ' ')
    text = text.replace('XNULAX', '0')
    text = text.replace('XJEDNAX', '1')
    text = text.replace('XDVAX', '2')
    text = text.replace('XTRIX', '3')
    text = text.replace('XCTYRIX', '4')
    text = text.replace('XPETX', '5')
    text = text.replace('XSESTX', '6')
    text = text.replace('XSEDMX', '7')
    text = text.replace('XOSMX', '8')
    text = text.replace('XDEVETX', '9')

    return text


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_inverse(a, b):
    if gcd(a, b) != 1:
        return None

    for x in range(1, b):
        if (a * x) % b == 1:
            return x
    return None


def encrypt(text, key_a, key_b):
    # Nahrazeni mezer a cisel
    text = text.replace(' ', 'XMEZERAX')
    text = text.replace('0', 'XNULAX')
    text = text.replace('1', 'XJEDNAX')
    text = text.replace('2', 'XDVAX')
    text = text.replace('3', 'XTRIX')
    text = text.replace('4', 'XCTYRIX')
    text = text.replace('5', 'XPETX')
    text = text.replace('6', 'XSESTX')
    text = text.replace('7', 'XSEDMX')
    text = text.replace('8', 'XOSMX')
    text = text.replace('9', 'XDEVETX')

    encrypted_text = ""
    count = 0

    mod_inverse_a = mod_inverse(key_a, 26)
    if mod_inverse_a is None:
        return "Klíč 'a' je neplatný. Klíč 'a' musí být celé číslo nesoudělné s 26."

    for char in text:
        encrypted_char = chr(((ord(char) - ord('A')) * key_a + key_b) % 26 + ord('A'))
        encrypted_text += encrypted_char
        count += 1

        # Přidání mezery po pěti znacích
        if count == 5:
            encrypted_text += ' '
            count = 0

    return encrypted_text


def decrypt(encrypted_text, key_a, key_b):
    decrypted_text = ""
    mod_inverse_a = mod_inverse(key_a, 26)
    if mod_inverse_a is None:
        return "Klíč 'a' je neplatný. Klíč 'a' musí být celé číslo nesoudělné s 26."

    encrypted_text = encrypted_text.replace(' ', '')

    for char in encrypted_text:
        decrypted_char = chr(((ord(char) - ord('A') - key_b) * mod_inverse_a) % 26 + ord('A'))
        decrypted_text += decrypted_char
    return decrypted_text


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(672)
widget.setFixedWidth(990)
widget.show()
app.exec()
