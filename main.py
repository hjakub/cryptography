import random
import sys
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QDialog, QTableWidgetItem


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('sifra_gui.ui', self)

        # table
        self.table.setRowCount(5)
        self.table.setColumnCount(5)

        # button_zasifruj
        self.button_zasifruj.clicked.connect(self.buttonclick_zasifruj)

        # button desifruj
        self.button_desifruj.clicked.connect(self.buttonclick_desifruj)

        # radio buttony
        self.radio_en.clicked.connect(self.radio_en_clicked)
        self.radio_en.clicked.connect(self.clear_table)
        self.radio_cz.clicked.connect(self.radio_cz_clicked)
        self.radio_cz.clicked.connect(self.clear_table)
        self.radio_v.clicked.connect(self.radio_v_clicked)
        self.radio_v.clicked.connect(self.clear_table)

        # button_over
        self.button_over_klic.clicked.connect(self.buttonclick_over_klic)
        self.button_over_tabulku.clicked.connect(self.buttonclick_over_tabulku)

        # button_generovat
        self.button_generovat.clicked.connect(self.generate_table)

        # button_vymazat
        self.button_vymazat.clicked.connect(self.clear_table)

    def radio_en_clicked(self):
        # angličtina, adfgx
        global cz
        cz = 0
        global vx
        vx = 0
        self.table.setRowCount(5)
        self.table.setColumnCount(5)

    def radio_cz_clicked(self):
        # čeština, adfgx
        global cz
        cz = 1
        global vx
        vx = 0
        self.table.setRowCount(5)
        self.table.setColumnCount(5)

    def radio_v_clicked(self):
        # adfgvx, jazyk je jedno
        global cz
        cz = 2
        global vx
        vx = 1
        self.table.setRowCount(6)
        self.table.setColumnCount(6)

    def generate_table(self):
        if vx == 0:
            if cz == 1:
                alphabet = list('ABCDEFGHIJKLMNOPQRSTUVXYZ')
            else:
                alphabet = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
            random.shuffle(alphabet)

            for row in range(5):
                for col in range(5):
                    item = QTableWidgetItem(alphabet.pop())
                    self.table.setItem(row, col, item)
        else:
            alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            random.shuffle(alphabet)
            for row in range(6):
                for col in range(6):
                    item = QTableWidgetItem(alphabet.pop())
                    self.table.setItem(row, col, item)

    def clear_table(self):
        if vx == 0:
            for row in range(5):
                for col in range(5):
                    self.table.setItem(row, col, None)
        if vx == 1:
            for row in range(6):
                for col in range(6):
                    self.table.setItem(row, col, None)
        self.output_ano_2.setText('')
        self.output_ne_2.setText('')

    def buttonclick_zasifruj(self):
        input_text = str(self.input_otevreny.toPlainText())
        key = str(self.input_key.toPlainText())
        key = filter_key(key)
        if vx == 0:
            if cz == 1:
                alphabet = list('ABCDEFGHIJKLMNOPQRSTUVXYZ')
            else:
                alphabet = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
            data = []
            for row in range(5):
                for col in range(5):
                    item = self.table.item(row, col)
                    if item:
                        data.append(item.text())
                    else:
                        data.append('')
            table = create_table_adfgx(data)
            filtrovany_text = filter_numbers(filter_text(input_text))
            encrypted_text = encrypt_adfgx(table, filtrovany_text, key)
            self.output_filtrovany.setText(str(filtrovany_text))
            if len(data) == 25:
                if all(char in alphabet for char in data):
                    if len(data) == len(set(data)):
                        self.output_sifrovany.setText(str(encrypted_text))
                    else:
                        self.output_sifrovany.setText('Špatně vyplněná tabulka!')
                else:
                    self.output_sifrovany.setText('Špatně vyplněná tabulka!')
            else:
                self.output_sifrovany.setText('Špatně vyplněná tabulka!')
        else:
            alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            data = []
            for row in range(6):
                for col in range(6):
                    item = self.table.item(row, col)
                    if item:
                        data.append(item.text())
                    else:
                        data.append('')
            table = create_table_adfgvx(data)
            filtrovany_text = filter_text(input_text)
            encrypted_text = encrypt_adfgvx(table, filtrovany_text, key)
            self.output_filtrovany.setText(str(filtrovany_text))
            if len(data) == 36:
                if all(char in alphabet for char in data):
                    if len(data) == len(set(data)):
                        self.output_sifrovany.setText(str(encrypted_text))
                    else:
                        self.output_sifrovany.setText('Špatně vyplněná tabulka!')
                else:
                    self.output_sifrovany.setText('Špatně vyplněná tabulka!')
            else:
                self.output_sifrovany.setText('Špatně vyplněná tabulka!')

    def buttonclick_desifruj(self):
        encrypted_text = str(self.input_sifrovany.toPlainText())
        key = str(self.input_key.toPlainText())
        key = filter_key(key)
        if vx == 0:
            if cz == 1:
                alphabet = list('ABCDEFGHIJKLMNOPQRSTUVXYZ')
            else:
                alphabet = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
            data = []
            for row in range(5):
                for col in range(5):
                    item = self.table.item(row, col)
                    if item:
                        data.append(item.text())
                    else:
                        data.append('')
            table = create_table_adfgx(data)
            decrypted_text = decrypt_adfgx(table, encrypted_text, key)
            otevreny_text = open_text(decrypted_text)
            if len(data) == 25:
                if all(char in alphabet for char in data):
                    if len(data) == len(set(data)):
                        self.output_desifrovany.setText(str(decrypted_text))
                        self.output_otevreny.setText(str(otevreny_text))
                    else:
                        self.output_desifrovany.setText('Špatně vyplněná tabulka!')
                else:
                    self.output_desifrovany.setText('Špatně vyplněná tabulka!')
            else:
                self.output_desifrovany.setText('Špatně vyplněná tabulka!')
        else:
            alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            data = []
            for row in range(6):
                for col in range(6):
                    item = self.table.item(row, col)
                    if item:
                        data.append(item.text())
                    else:
                        data.append('')
            table = create_table_adfgvx(data)
            decrypted_text = decrypt_adfgvx(table, encrypted_text, key)
            otevreny_text = open_text(decrypted_text)
            if len(data) == 36:
                if all(char in alphabet for char in data):
                    if len(data) == len(set(data)):
                        self.output_desifrovany.setText(str(decrypted_text))
                        self.output_otevreny.setText(str(otevreny_text))
                    else:
                        self.output_desifrovany.setText('Špatně vyplněná tabulka!')
                else:
                    self.output_desifrovany.setText('Špatně vyplněná tabulka!')
            else:
                self.output_desifrovany.setText('Špatně vyplněná tabulka!')

    def buttonclick_over_klic(self):
        key = str(self.input_key.toPlainText())
        key = filter_key(key)
        if len(key) < 8:
            self.output_ne.setText('NE')
            self.output_ano.setText('')
        else:
            self.output_ano.setText('ANO')
            self.output_ne.setText('')

    def buttonclick_over_tabulku(self):
        if vx == 0:
            if cz == 1:
                alphabet = list('ABCDEFGHIJKLMNOPQRSTUVXYZ')
            else:
                alphabet = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
            data = []
            for row in range(5):
                for col in range(5):
                    item = self.table.item(row, col)
                    if item:
                        data.append(item.text())
            if len(data) == 25:
                if all(char in alphabet for char in data):
                    if len(data) == len(set(data)):
                        self.output_ano_2.setText('ANO')
                        self.output_ne_2.setText('')
                    else:
                        self.output_ne_2.setText('NE')
                        self.output_ano_2.setText('')
                else:
                    self.output_ne_2.setText('NE')
                    self.output_ano_2.setText('')
            else:
                self.output_ne_2.setText('NE')
                self.output_ano_2.setText('')
        else:
            data = []
            alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            for row in range(6):
                for col in range(6):
                    item = self.table.item(row, col)
                    if item:
                        data.append(item.text())
            if len(data) == 36:
                if all(char in alphabet for char in data):
                    if len(data) == len(set(data)):
                        self.output_ano_2.setText('ANO')
                        self.output_ne_2.setText('')
                    else:
                        self.output_ne_2.setText('NE')
                        self.output_ano_2.setText('')
                else:
                    self.output_ne_2.setText('NE')
                    self.output_ano_2.setText('')
            else:
                self.output_ne_2.setText('NE')
                self.output_ano_2.setText('')


# Proměnná cz slouží k výběru jazyka (0 = en, 1 = cz, 2 = adfgvx; defaultně cz = 1)
cz = 1

# Proměnná vx slouží pro rozhodování, zda bude použita šifra ADFGX či ADFGVX (defaultně 0 = ADFGX)
vx = 0


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

    # Nahrazení mezer, otazníků a vykřičníků
    text = text.replace(' ', 'XMEZERAX')
    text = text.replace('!', 'XVYKRX')
    text = text.replace('?', 'XOTAZX')

    # Nahrazení znaku v závislosti na zvoleném jazyce
    if cz == 0:
        text = text.replace('J', 'I')
    elif cz == 1:
        text = text.replace('W', 'V')
    text = [char for char in text]
    text = ''.join(text)

    return text


def filter_numbers(text):
    # Nahrazení čísel (jen u ADFGX)
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

    return text


def filter_key(key):
    # Převod všech písmen na velká
    key = key.upper()

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
        key = key.replace(char, diacritics[char])

    # Odstranění čárek, matematických znamének, čísel apod.
    punctuation = {',', "'", '"', '.', '-', '+', '#', 'ˇ', '>', '<', '(', ')', '/', '%', ':', '&', ';', '~', '@', '}',
                   '{', '[', ']', '*', '^', '°', '_', '$', '`', '¯', '±', '¨', '§', '©', '¦', '|', '¤', '¡', '»', '×',
                   '÷', '¬', '®', '¿', '·', '˄', '˅', '≥', '≤', '≡', '≈', '≠', '∩', '∞', '√', '←', '↑', '→', '↓', '↔',
                   '↕', '∆', ' ', '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    for char in punctuation:
        key = key.replace(char, '')

    # Odstranění duplicity
    key = ''.join(dict.fromkeys(key))

    return key


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


def create_table_adfgx(data):
    # tabulka 5x5 (ADFGX)
    table = [[data[row * 5 + col] for col in range(5)] for row in range(5)]
    return table


def create_table_adfgvx(data):
    # tabulka 6x6 (ADFGVX)
    table = [[data[row * 6 + col] for col in range(6)] for row in range(6)]
    return table


def encrypt_adfgx(table, text, key):
    text = filter_text(text)
    text = filter_numbers(text)
    key = filter_key(key)
    encrypted_text = ''

    # substituce
    if len(key) < 8:
        return ('Neplatný klíč! Klíč musí mít minimálně 8 znaků (respektive 8 písmen BEZ DUPLICITY, '
                'jelikož duplicitní a nepísmenné znaky jsou vyfiltrovány)!')
    else:
        for char in text:
            for row in range(5):
                for col in range(5):
                    row_index, col_index = 0, 0
                    if table[row][col] == char:
                        if row == 0:
                            row_index = 'A'
                        elif row == 1:
                            row_index = 'D'
                        elif row == 2:
                            row_index = 'F'
                        elif row == 3:
                            row_index = 'G'
                        elif row == 4:
                            row_index = 'X'
                        if col == 0:
                            col_index = 'A'
                        elif col == 1:
                            col_index = 'D'
                        elif col == 2:
                            col_index = 'F'
                        elif col == 3:
                            col_index = 'G'
                        elif col == 4:
                            col_index = 'X'
                        encrypted_text += row_index + col_index

    # transpozice
    transposed_text = [''] * len(key)
    for i, char in enumerate(encrypted_text):
        transposed_text[i % len(key)] += char

    # setřídění sloupců + přidání mezer
    sorted_cols = sorted(range(len(key)), key=lambda x: key[x])
    final_text = ' '.join(transposed_text[i] for i in sorted_cols)

    return final_text


def encrypt_adfgvx(table, text, key):
    text = filter_text(text)
    key = filter_key(key)
    encrypted_text = ''

    # substituce
    if len(key) < 8:
        return ('Neplatný klíč! Klíč musí mít minimálně 8 znaků (respektive 8 písmen, jelikož všchny ostatní znaky '
                'jsou vyfiltrovány)!')
    else:
        for char in text:
            for row in range(6):
                for col in range(6):
                    row_index, col_index = 0, 0
                    if table[row][col] == char:
                        if row == 0:
                            row_index = 'A'
                        elif row == 1:
                            row_index = 'D'
                        elif row == 2:
                            row_index = 'F'
                        elif row == 3:
                            row_index = 'G'
                        elif row == 4:
                            row_index = 'V'
                        elif row == 5:
                            row_index = 'X'
                        if col == 0:
                            col_index = 'A'
                        elif col == 1:
                            col_index = 'D'
                        elif col == 2:
                            col_index = 'F'
                        elif col == 3:
                            col_index = 'G'
                        elif col == 4:
                            col_index = 'V'
                        elif col == 5:
                            col_index = 'X'
                        encrypted_text += row_index + col_index

    # transpozice
    transposed_text = [''] * len(key)
    for i, char in enumerate(encrypted_text):
        transposed_text[i % len(key)] += char

    # setřídění sloupců + přidání mezer
    sorted_cols = sorted(range(len(key)), key=lambda x: key[x])
    final_text = ' '.join(transposed_text[i] for i in sorted_cols)

    return final_text


def reverse_transposition(encrypted_text, key):
    key = filter_key(key)
    encrypted_text = encrypted_text.replace(' ', '')
    encrypted_text = encrypted_text.upper()

    # počet řádků v sloupcích - u 'prodloužených' sloupců je při zpětné transpozici přidán řádek
    num_rows = len(encrypted_text) // len(key)

    # zpětné setřídění sloupců
    sorted_cols = sorted(range(len(key)), key=lambda x: key[x])
    transposed_text = [''] * len(key)

    # zpětná transpozice
    index = 0
    for col in sorted_cols:
        col_length = num_rows
        if len(encrypted_text) % len(key) != 0:
            if col < (len(encrypted_text) % len(key)):
                col_length += 1

        transposed_text[col] = encrypted_text[index:index + col_length]
        index += col_length

    reversed_text = ''
    for row in range(num_rows):
        for col in range(len(key)):
            reversed_text += transposed_text[col][row]
    if len(encrypted_text) % len(key) != 0:
        for row in range(num_rows, num_rows + 1):
            for col in range(len(encrypted_text) % len(key)):
                reversed_text += transposed_text[col][row]

    return reversed_text


def decrypt_adfgx(table, encrypted_text, key):
    key = filter_key(key)
    transposed_text = reverse_transposition(encrypted_text.replace(' ', ''), key)

    decrypted_text = ''
    index = 0

    # zpětná substituce
    if len(key) < 8:
        return ('Neplatný klíč! Klíč musí mít minimálně 8 znaků (respektive 8 písmen, jelikož všchny ostatní znaky '
                'jsou vyfiltrovány)!')
    else:
        while index < len(transposed_text):
            if transposed_text[index] == 'A':
                row = 0
                index += 1
            elif transposed_text[index] == 'D':
                row = 1
                index += 1
            elif transposed_text[index] == 'F':
                row = 2
                index += 1
            elif transposed_text[index] == 'G':
                row = 3
                index += 1
            elif transposed_text[index] == 'X':
                row = 4
                index += 1
            else:
                return 'V zašifrovaném textu se vyskytuje nepovolený znak!'

            if transposed_text[index] == 'A':
                col = 0
                index += 1
            elif transposed_text[index] == 'D':
                col = 1
                index += 1
            elif transposed_text[index] == 'F':
                col = 2
                index += 1
            elif transposed_text[index] == 'G':
                col = 3
                index += 1
            elif transposed_text[index] == 'X':
                col = 4
                index += 1
            else:
                return 'V zašifrovaném textu se vyskytuje nepovolený znak!'

            decrypted_text += table[row][col]

    return decrypted_text


def decrypt_adfgvx(table, encrypted_text, key):
    key = filter_key(key)
    transposed_text = reverse_transposition(encrypted_text.replace(' ', ''), key)

    decrypted_text = ''
    index = 0

    # zpětná substituce
    if len(key) < 8:
        return ('Neplatný klíč! Klíč musí mít minimálně 8 znaků (respektive 8 písmen, jelikož všchny ostatní znaky '
                'jsou vyfiltrovány)!')
    else:
        while index < len(transposed_text):
            if transposed_text[index] == 'A':
                row = 0
                index += 1
            elif transposed_text[index] == 'D':
                row = 1
                index += 1
            elif transposed_text[index] == 'F':
                row = 2
                index += 1
            elif transposed_text[index] == 'G':
                row = 3
                index += 1
            elif transposed_text[index] == 'V':
                row = 4
                index += 1
            elif transposed_text[index] == 'X':
                row = 5
                index += 1
            else:
                return 'V zašifrovaném textu se vyskytuje nepovolený znak!'

            if transposed_text[index] == 'A':
                col = 0
                index += 1
            elif transposed_text[index] == 'D':
                col = 1
                index += 1
            elif transposed_text[index] == 'F':
                col = 2
                index += 1
            elif transposed_text[index] == 'G':
                col = 3
                index += 1
            elif transposed_text[index] == 'V':
                col = 4
                index += 1
            elif transposed_text[index] == 'X':
                col = 5
                index += 1
            else:
                return 'V zašifrovaném textu se vyskytuje nepovolený znak!'

            decrypted_text += table[row][col]

    return decrypted_text


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(790)
widget.setFixedWidth(1332)
widget.show()
app.exec()
