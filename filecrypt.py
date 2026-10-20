import sys
import os
import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Chiffrement symetrique d'un fichier a partir d'un mot de passe.
# La cle Fernet est derivee du mot de passe avec PBKDF2 + un sel aleatoire.
# Le sel est stocke au debut du fichier chiffre pour pouvoir dechiffrer.

SALT_SIZE = 16


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt(path, password):
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    f = Fernet(key)

    data = open(path, "rb").read()
    token = f.encrypt(data)

    out = path + ".enc"
    with open(out, "wb") as fh:
        fh.write(salt + token)
    print(f"chiffre -> {out}")


def decrypt(path, password):
    blob = open(path, "rb").read()
    salt, token = blob[:SALT_SIZE], blob[SALT_SIZE:]
    key = derive_key(password, salt)
    f = Fernet(key)

    data = f.decrypt(token)   # leve une exception si mauvais mot de passe

    out = path.removesuffix(".enc") + ".dec"
    with open(out, "wb") as fh:
        fh.write(data)
    print(f"dechiffre -> {out}")


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("enc", "dec"):
        print("usage: python filecrypt.py enc|dec <fichier>")
        return

    mode, path = sys.argv[1], sys.argv[2]
    pwd = getpass.getpass("mot de passe: ")

    if mode == "enc":
        encrypt(path, pwd)
    else:
        decrypt(path, pwd)


if __name__ == "__main__":
    main()
