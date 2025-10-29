import sys
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QDialog


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('sifra_gui.ui', self)

        # button_zasifruj
        self.button_zasifruj.clicked.connect(self.buttonclick_zasifruj)

        # button_zasifruj
        self.button_desifruj.clicked.connect(self.buttonclick_desifruj)

        # button_abeceda
        self.button_abeceda.clicked.connect(self.buttonclick_abeceda)

        # radio buttony
        self.radio_en.clicked.connect(self.radio_en_clicked)
        self.radio_cz.clicked.connect(self.radio_cz_clicked)

    def buttonclick_zasifruj(self):
        input_text = str(self.input_otevreny.toPlainText())
        key = str(self.input_key.toPlainText())
        bigramovy_text = bigram_text(input_text)
        encrypted_text = encrypt(bigramovy_text, key)
        self.output_bigramovy.setText(str(bigramovy_text))
        self.output_sifrovany.setText(str(encrypted_text))

    def buttonclick_desifruj(self):
        input_text = str(self.input_sifrovany.toPlainText())
        key = str(self.input_key.toPlainText())
        decrypted_text = decrypt(input_text, key)
        otevreny_text = open_text(decrypted_text)
        self.output_desifrovany.setText(str(decrypted_text))
        self.output_otevreny.setText(str(otevreny_text))

    def display_matrix(self, matrix):
        rows = len(matrix)
        columns = len(matrix[0])

        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)

        for row in range(rows):
            for col in range(columns):
                item = matrix[row][col]
                cell = QtWidgets.QTableWidgetItem(item)
                self.table.setItem(row, col, cell)

    def buttonclick_abeceda(self):
        key = str(self.input_key.toPlainText())
        matrix = create_matrix(key)
        self.display_matrix(matrix)

    def radio_en_clicked(self):
        global cz
        cz = 0

    def radio_cz_clicked(self):
        global cz
        cz = 1


# Proměnná cz slouží k výběru jazyka (0 = en, 1 = cz; defaultně cz)
cz = 1


def filter_text(text):
    # Převod všech písmen na velká
    text = text.upper()

    # Odstranění diakritiky
    diacritics = {'Á': 'A', 'Â': 'A', 'Ä': 'A', 'Ą': 'A', 'Ā': 'A', 'À': 'A', 'Ã': 'A', 'Å': 'A', 'Æ': 'AE', 'Ĉ': 'C',
                  'Ċ': 'C', 'Č': 'C', 'Ç': 'C', 'Ć': 'C', 'Ð': 'D', 'Ď': 'D', 'É': 'E', 'Ę': 'E', 'Ê': 'E', 'È': 'E',
                  'Ë': 'E', 'Ė': 'E', 'Ě': 'E', 'Ē': 'E', 'Ĝ': 'G', 'Ğ': 'G', 'Ġ': 'G', 'Ģ': 'G', 'Ĥ': 'H', 'Ħ': 'H',
                  'Ĩ': 'I', 'Ĭ': 'I', 'İ': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I', 'Í': 'I', 'Į': 'I', 'Ī': 'I', 'Ĵ': 'J',
                  'Ķ': 'K', 'Ļ': 'L', 'Ł': 'L', 'Ĺ': 'L', 'Ľ': 'L', 'Ň': 'N', 'Ñ': 'N', 'Ņ': 'N', 'Ń': 'N', 'Ó': 'O',
                  'Ò': 'O', 'Ö': 'O', 'Ō': 'O', 'Ô': 'O', 'Ø': 'O', 'Ŏ': 'O', 'Ő': 'O', 'Œ': 'OE', 'Ř': 'R', 'Ŕ': 'R',
                  'Ŗ': 'R', 'Š': 'S', 'Ŝ': 'S', 'Ş': 'S', 'Ś': 'S', 'ẞ': 'SS', 'Ţ': 'T', 'Ŧ': 'T', 'Ť': 'T', 'Ú': 'U',
                  'Ũ': 'U', 'Ŭ': 'U', 'Ű': 'U', 'Ů': 'U', 'Ü': 'U', 'Ù': 'U', 'Û': 'U', 'Ų': 'U', 'Ū': 'U', 'Ŵ': 'W',
                  'Ý': 'Y', 'Ÿ': 'Y', 'Ž': 'Z', 'Ż': 'Z'}
    for char in diacritics:
        text = text.replace(char, diacritics[char])

    # Odstranění čárek, matematických znamének apod.
    punctuation = {',', "'", '"', '.', '-', '+', '#', 'ˇ', '>', '<', '(', ')', '/', '%', ':', '&', ';', '~', '@', '}',
                   '{', '[', ']', '*', '^', '°', '_', '$', '`', '¯', '±', '¨', '§', '©', '¦', '|', '¤', '¡', '»', '×',
                   '÷', '¬', '®', '¿', '·', '˄', '˅', '≥', '≤', '≡', '≈', '≠', '∩', '∞', '√', '←', '↑', '→', '↓', '↔',
                   '↕', '∆'}
    for char in punctuation:
        text = text.replace(char, '')

    # Nahrazení mezer, čísel a otazníků/vykřičníků
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
    text = text.replace('!', 'XVYKRX')
    text = text.replace('?', 'XOTAZX')

    if cz == 0:
        text = text.replace('J', 'I')
    else:
        text = text.replace('W', 'V')
    text = [char for char in text if char.isalpha()]
    text = ''.join(text)

    return text


def open_text(text):
    # Zpětné nahrazení zástupných řetězců za čísla a mezery
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
    text = text.replace('XVYKRX', '!')
    text = text.replace('XOTAZX', '?')

    return text


def bigram_text(text):
    text = filter_text(text)
    bigrams = []
    i = 0
    while i < len(text):
        # Ošetření situace, kdy jsou v bigramu dva stejné znaky
        if i < len(text) - 1 and text[i] == text[i + 1]:
            bigrams.append(text[i] + 'X')
            i += 1
        else:
            # Ošetření situace, kdy je na konci v bigramu jen jeden znak
            if i == len(text) - 1:
                bigrams.append(text[i] + 'X')
            else:
                bigrams.append(text[i:i + 2])
            i += 2

    return ' '.join(bigrams)


def create_matrix(key):
    # Nahrazení znaků v klíči v závislosti na zvoleném jazyku
    if cz == 0:
        key = key.upper().replace('J', 'I')
    else:
        key = key.upper().replace('W', 'V')

    # Odstranění diakritiky z klíče
    diacritics = {'Á': 'A', 'Â': 'A', 'Ä': 'A', 'Ą': 'A', 'Ā': 'A', 'À': 'A', 'Ã': 'A', 'Å': 'A', 'Æ': 'AE', 'Ĉ': 'C',
                  'Ċ': 'C', 'Č': 'C', 'Ç': 'C', 'Ć': 'C', 'Ð': 'D', 'Ď': 'D', 'É': 'E', 'Ę': 'E', 'Ê': 'E', 'È': 'E',
                  'Ë': 'E', 'Ė': 'E', 'Ě': 'E', 'Ē': 'E', 'Ĝ': 'G', 'Ğ': 'G', 'Ġ': 'G', 'Ģ': 'G', 'Ĥ': 'H', 'Ħ': 'H',
                  'Ĩ': 'I', 'Ĭ': 'I', 'İ': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I', 'Í': 'I', 'Į': 'I', 'Ī': 'I', 'Ĵ': 'J',
                  'Ķ': 'K', 'Ļ': 'L', 'Ł': 'L', 'Ĺ': 'L', 'Ľ': 'L', 'Ň': 'N', 'Ñ': 'N', 'Ņ': 'N', 'Ń': 'N', 'Ó': 'O',
                  'Ò': 'O', 'Ö': 'O', 'Ō': 'O', 'Ô': 'O', 'Ø': 'O', 'Ŏ': 'O', 'Ő': 'O', 'Œ': 'OE', 'Ř': 'R', 'Ŕ': 'R',
                  'Ŗ': 'R', 'Š': 'S', 'Ŝ': 'S', 'Ş': 'S', 'Ś': 'S', 'ẞ': 'SS', 'Ţ': 'T', 'Ŧ': 'T', 'Ť': 'T', 'Ú': 'U',
                  'Ũ': 'U', 'Ŭ': 'U', 'Ű': 'U', 'Ů': 'U', 'Ü': 'U', 'Ù': 'U', 'Û': 'U', 'Ų': 'U', 'Ū': 'U', 'Ŵ': 'W',
                  'Ý': 'Y', 'Ÿ': 'Y', 'Ž': 'Z', 'Ż': 'Z'}
    for char in diacritics:
        key = key.replace(char, diacritics[char])

    # Odstranění ostatního balastu z klíče
    punctuation = {',', "'", '"', '.', '!', '?', '-', '+', '#', 'ˇ', '>', '<', '(', ')', '/', '%', ':', '&', ';', '~',
                   '@', '}', '{', '[', ']', '*', '^', '°', '_', '$', '`', '¯', '±', '¨', '§', '©', '¦', '|', '¤', '¡',
                   '»', '×', '÷', '¬', '®', '¿', '·', '˄', '˅', '≥', '≤', '≡', '≈', '≠', '∩', '∞', '√', '←', '↑', '→',
                   '↓', '↔', '↕', '∆', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' '}
    for char in punctuation:
        key = key.replace(char, '')

    # Odstranění duplicity
    key = ''.join(dict.fromkeys(key))

    # Šifrovací abeceda - záleží na zvoleném jazyce
    if cz == 0:
        alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    else:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVXYZ'
    matrix = []
    key_set = set(key)

    for char in key:
        key_set.discard(char)  # Odstranění znaků již použitých v klíči
        alphabet = alphabet.replace(char, '')
        matrix.append(char)

    for char in alphabet:
        matrix.append(char)

    return [matrix[i:i + 5] for i in range(0, 25, 5)]


# Funkce určená k nalezení daného znaku v rámci matice (vrací index řádku, sloupce)
def find_position(matrix, char):
    for row in matrix:
        if char in row:
            return matrix.index(row), row.index(char)


# Pomocná funkce určená k přidání mezery po každých n znacích
def insert_space(text, n):
    space_text = ''
    count = 0

    for char in text:
        space_text += char
        count += 1

        if count == n:
            space_text += ' '
            count = 0

    return space_text


def encrypt(text, key):
    text = text.replace(' ', '')
    matrix = create_matrix(key)
    encrypted_text = ''
    i = 0

    while i < len(text):
        char1 = text[i]
        char2 = text[i + 1] if i + 1 < len(text) else 'X'

        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)

        if col1 == col2:
            encrypted_text += matrix[(row1 + 1) % 5][col1]
            encrypted_text += matrix[(row2 + 1) % 5][col2]
        elif row1 == row2:
            encrypted_text += matrix[row1][(col1 + 1) % 5]
            encrypted_text += matrix[row2][(col2 + 1) % 5]
        else:
            encrypted_text += matrix[row1][col2]
            encrypted_text += matrix[row2][col1]

        i += 2

    encrypted_text = insert_space(encrypted_text, 5)

    return encrypted_text


def decrypt(encrypted_text, key):
    encrypted_text = encrypted_text.replace(' ', '')
    matrix = create_matrix(key)
    decrypted_text = ''
    i = 0

    while i < len(encrypted_text):
        char1 = encrypted_text[i]
        char2 = encrypted_text[i + 1]

        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)

        if col1 == col2:
            decrypted_text += matrix[(row1 - 1) % 5][col1]
            decrypted_text += matrix[(row2 - 1) % 5][col2]
        elif row1 == row2:
            decrypted_text += matrix[row1][(col1 - 1) % 5]
            decrypted_text += matrix[row2][(col2 - 1) % 5]
        else:
            decrypted_text += matrix[row1][col2]
            decrypted_text += matrix[row2][col1]

        i += 2

    return decrypted_text


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(790)
widget.setFixedWidth(990)
widget.show()
app.exec()
