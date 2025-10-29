import random
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

        # button_desifruj
        self.button_desifruj.clicked.connect(self.buttonclick_desifruj)

        # button_keygen
        self.button_keygen.clicked.connect(self.buttonclick_keygen)

    def buttonclick_keygen(self):
        # vygenerování prvočísel
        start_range = 10 ** 12
        end_range = 10 ** 13
        p = generate_random_prime(start_range, end_range)
        q = generate_random_prime(start_range, end_range)
        while q == p:
            q = generate_random_prime(start_range, end_range)
        self.output_p.setText(str(p))
        self.output_q.setText(str(q))

        # n, euler
        n = p * q
        euler = (p - 1) * (q - 1)
        self.output_n.setText(str(n))
        self.output_fi.setText(str(euler))
        self.output_key1_n.setText(str(n))
        self.output_key2_n.setText(str(n))
        # veřejný klíč (e)
        e = random.randint(2, euler - 1)
        while gcd(e, euler) != 1:
            e = random.randint(2, euler - 1)  # 1 < e < euler && gcd(e, euler) == 1
        self.output_e.setText(str(e))
        # privátní klíč (d)
        d = mod_inverse(e, euler)
        self.output_d.setText(str(d))

    def buttonclick_zasifruj(self):
        input_text = str(self.input_otevreny.toPlainText())
        n = int(self.output_n.toPlainText())
        e = int(self.output_e.toPlainText())
        public_key = (n, e)
        # decimal
        decimal_text = text_to_decimal(input_text)
        self.output_decimal.setText(str(decimal_text))
        # šifrování
        cipher_blocks = encrypt(input_text, public_key)
        cipher_text = ' '.join(map(str, cipher_blocks))
        self.output_sifrovany.setText(cipher_text)

    def buttonclick_desifruj(self):
        cipher_blocks_str = self.input_sifrovany.toPlainText().strip()
        cipher_block_str_list = cipher_blocks_str.split()  # rozdělení input stringu na bloky
        cipher_blocks = [int(block) for block in cipher_block_str_list]  # převod bloků na int
        n = int(self.output_n.toPlainText())
        d = int(self.output_d.toPlainText())
        private_key = (n, d)
        # dešifrování
        decrypted_text = decrypt(cipher_blocks, private_key)
        self.output_desifrovany.setText(str(decrypted_text))


# is_prime určí, zda je dané číslo num prvočíslem
def is_prime(num):
    if num < 2:
        return False
    # zbytek po dělení číslem větším než num/2 nemůže být nulový
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


# generate_random_prime využívá předešlé funkce ke generování prvočísel
def generate_random_prime(start, end):
    while True:
        # vygeneruje se náhodné číslo (kandidát na prvočíslo) v daném rozsahu
        random_num = random.randint(start, end)
        if is_prime(random_num):
            return random_num


# gcd funkce najde největší společný dělitel
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# modulární multiplikativní inverze pomocí pow
def mod_inverse(a, b):
    return pow(a, -1, b)


# text_to_decimal převede text na číslo
def text_to_decimal(text):
    return int.from_bytes(text.encode('utf-8'), byteorder='big')


# decimal_to_text převede číslo na text
def decimal_to_text(decimal):
    return decimal.to_bytes((decimal.bit_length() + 7) // 8, byteorder='big').decode('utf-8', 'ignore')


# šifrování
def encrypt(plain_text, public_key):
    n, e = public_key
    block_size = 7  # velikost jednoho bloku

    # převod textu na čísla (bloky)
    blocks = [text_to_decimal(plain_text[i:i + block_size]) for i in range(0, len(plain_text), block_size)]

    # zašifrování bloků
    cipher_blocks = [pow(block, e, n) for block in blocks]

    return cipher_blocks


# dešifrování
def decrypt(cipher_blocks, private_key):
    n, d = private_key

    # dešifrování po blocích
    decrypted_blocks = [pow(cipher_block, d, n) for cipher_block in cipher_blocks]

    # převod čísel na text
    decrypted_text = ''.join((decimal_to_text(block) for block in decrypted_blocks))

    return decrypted_text


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(670)
widget.setFixedWidth(1332)
widget.show()
app.exec()
