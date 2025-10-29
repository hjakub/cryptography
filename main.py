import base64
import hashlib
import os
import random
import sys
from datetime import datetime
from zipfile import ZipFile

from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('sifra_gui.ui', self)

        # button_vybrat
        self.button_vybrat.clicked.connect(self.buttonclick_vybrat)

        # button_keygen
        self.button_keygen.clicked.connect(self.buttonclick_keygen)

        # button_podpis
        self.button_podpis.clicked.connect(self.buttonclick_podepsat)

        # button_overit
        self.button_overit.clicked.connect(self.buttonclick_over)

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
        # veřejný klíč (e)
        e = random.randint(2, euler - 1)
        while gcd(e, euler) != 1:
            e = random.randint(2, euler - 1)  # 1 < e < euler && gcd(e, euler) == 1
        # privátní klíč (d)
        d = mod_inverse(e, euler)
        self.output_d.setText(str(d))
        self.output_e.setText(str(e))

        private_key = (n, d)
        public_key = (n, e)

        self.output_priv.setText(str(private_key))
        self.output_pub.setText(str(public_key))

    def buttonclick_vybrat(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Vyber soubor k podepsání", "C:/temp", "All Files (*)")
        if file_path:
            file_name = os.path.basename(file_path)  # název souboru
            file_time = os.path.getmtime(file_path)  # datum / sekundy od poslední modifikace
            human_time = datetime.fromtimestamp(file_time).strftime('%d.%m.%Y, %H:%M:%S')  # převod na čitelný formát

            self.output_soubor.setText(file_name)
            self.output_path.setText(file_path)
            self.output_datum.setText(str(human_time))

    def buttonclick_podepsat(self):
        file_path = self.output_path.toPlainText()
        sha3_hash = hashlib.sha3_512()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                sha3_hash.update(chunk)
        file_hash = sha3_hash.hexdigest()

        private_key = int(self.output_n.toPlainText()), int(self.output_d.toPlainText())
        public_key = int(self.output_n.toPlainText()), int(self.output_e.toPlainText())
        sign = encrypt(file_hash, private_key)
        sign_str = ' '.join(map(str, sign))

        # .priv
        private_key_str = str(private_key)
        private_key_bytes = base64.b64encode(bytes(private_key_str, 'utf-8'))
        private_key_base64 = private_key_bytes.decode('utf-8')
        private_key_path = os.path.join("C:/temp", "private_key.priv")
        with open(private_key_path, "w", encoding="utf-8") as private_key_file:
            private_key_file.write(f"RSA {private_key_base64}")

        # .pub
        public_key_str = str(public_key)
        public_key_bytes = base64.b64encode(bytes(public_key_str, 'utf-8'))
        public_key_base64 = public_key_bytes.decode('utf-8')
        public_key_path = os.path.join("C:/temp", "public_key.pub")
        with open(public_key_path, "w", encoding="utf-8") as public_key_file:
            public_key_file.write(f"RSA {public_key_base64}")

        # .sign
        sign_bytes = base64.b64encode(bytes(sign_str, 'utf-8'))
        sign_base64 = sign_bytes.decode('utf-8')
        file_folder = str(os.path.dirname(file_path))
        sign_path = os.path.join(file_folder, "signature.sign")
        with open(sign_path, "w", encoding="utf-8") as sign_file:
            sign_file.write(f"RSA_SHA3-512 {sign_base64}")

        # .zip
        zip_file_path, _ = QFileDialog.getSaveFileName(self, "Ulož .zip soubor", "C:/temp", "ZIP Files (*.zip)")
        if zip_file_path:
            with ZipFile(zip_file_path, "w") as zip_file:
                zip_file.write(file_path, arcname=os.path.basename(file_path))
                zip_file.write(sign_path, arcname=os.path.basename(sign_path))
                self.output_message.setText("Podepsání proběhlo úspěšně!")

    def buttonclick_over(self):
        zip_file_path, _ = QFileDialog.getOpenFileName(self, "Vyber zip soubor pro ověření", "C:/temp", "ZIP Files (*.zip)")
        file_name = os.path.basename(zip_file_path)
        self.output_soubor_zip.setText(file_name)
        self.output_path_zip.setText(zip_file_path)
        zip_ex_path = str(os.path.dirname(zip_file_path)) + "/ex"
        if zip_file_path:
            with ZipFile(zip_file_path, "r") as zip_file:
                zip_file.extractall(zip_ex_path)
            sign_file_path = str(zip_ex_path) + "/signature.sign"
            with open(sign_file_path, "rb") as sign_file:
                signature_data = sign_file.read()
            signature_str = str(signature_data)
            signature_str = signature_str.replace("b'RSA_SHA3-512 ", "")
            signature_str = signature_str.replace("'", "")

            signature_no_base = str(base64.b64decode(signature_str))
            signature_no_base = signature_no_base.replace("b'", "")
            signature_no_base = signature_no_base.replace("'", "")

            public_key = int(self.input_n.toPlainText()), int(self.input_e.toPlainText())
            signature_no_base = str(signature_no_base).strip()
            signature_block_list = signature_no_base.split()  # rozdělení input stringu na bloky
            signature_blocks = [int(block) for block in signature_block_list]  # převod bloků na int
            signature_hash_decrypted = str(decrypt(signature_blocks, public_key))

            extract_path, _ = QFileDialog.getOpenFileName(self, "Vyber soubor, který byl extrahován spolu s .sign", zip_ex_path, "All Files (*)")
            if extract_path:
                sha3_hash = hashlib.sha3_512()
                with open(extract_path, "rb") as file:
                    for chunk in iter(lambda: file.read(4096), b""):
                        sha3_hash.update(chunk)
                file_hash = sha3_hash.hexdigest()
            file_hash_str = str(file_hash)

            if signature_hash_decrypted == file_hash_str:
                self.output_message2.setText("Ověření bylo ÚSPĚŠNÉ!")
            else:
                self.output_message2.setText("Ověření SELHALO!")


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


# šifrování (rsa -- záměna public za private key)
def encrypt(plain_text, private_key):
    n, d = private_key
    block_size = 7  # velikost jednoho bloku

    # převod textu na čísla (bloky)
    blocks = [text_to_decimal(plain_text[i:i + block_size]) for i in range(0, len(plain_text), block_size)]

    # zašifrování bloků
    cipher_blocks = [pow(block, d, n) for block in blocks]

    return cipher_blocks


# dešifrování (rsa -- záměna private za public key)
def decrypt(cipher_blocks, public_key):
    n, e = public_key

    # dešifrování po blocích
    decrypted_blocks = [pow(cipher_block, e, n) for cipher_block in cipher_blocks]

    # převod čísel na text
    decrypted_text = ''.join((decimal_to_text(block) for block in decrypted_blocks))

    return decrypted_text


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(683)
widget.setFixedWidth(1259)
widget.show()
app.exec()
