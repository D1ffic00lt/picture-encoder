""" this program encodes and decodes images by generated keys """
# -*- coding: utf-8 -*-
import base64
import os

from PIL import Image
from io import BytesIO
from cryptography.fernet import Fernet, InvalidToken

coder = False
encode = False
result = False
decode = False


def create_folders(encode_folder: bool = False, result_folder: bool = False, decode_folder: bool = False):
    """

    :param encode_folder:
    :param result_folder:
    :param decode_folder:
    """
    try:
        if not encode_folder:
            os.mkdir("coder/encode")
    except FileExistsError:
        pass
    try:
        if not result_folder:
            os.mkdir("coder/result")
    except FileExistsError:
        pass
    try:
        if not decode_folder:
            os.mkdir("coder/decode")
    except FileExistsError:
        pass


for folder in os.listdir():
    if folder == 'coder':
        coder = True
        break
if coder:
    for folder in os.listdir():
        if folder == "encode":
            encode = True
        elif folder == "result":
            result = True
        elif folder == "decode":
            decode = True
    create_folders(encode_folder=encode, result_folder=result, decode_folder=decode)
else:
    os.mkdir("coder")
    create_folders()


def encrypt(message: bytes, key: bytes) -> bytes:
    """

    :param message:
    :param key:
    :return:
    """
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    """

    :param token:
    :param key:
    :return:
    """
    return Fernet(key).decrypt(token)


if input("Encode or decode an image?(E/D)").lower() == "e":
    key = Fernet.generate_key()
    name = input("Enter the file name in the \"encode\" folder: ")
    try:
        with open("coder\\encode\\" + name, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        extension = []
        for i in name[::-1]:
            if i == ".":
                break
            extension = [i] + extension
        os.remove("coder\\encode\\{}".format(name))
        name = encrypt(base64.b64encode(bytes(name[:-4], 'utf-8')), key)
        with open("coder\\result\\{}.cdp".format(name.decode() + '.' + ''.join(extension)), "wb+") as file:
            file.write(encrypt(encoded_string, key))
        print("Your key: {}".format(key.decode()))
    except FileNotFoundError:
        print("File not Found")
else:
    key = input("Enter key: ").encode()
    true = False
    name = ""
    file_name = ""
    for file in os.listdir("coder\\result"):
        try:
            name = decrypt(bytes(file, "utf-8"), key)
            file_name = file
            true = True
        except InvalidToken:
            pass
    if true:
        with open("coder\\result\\{}.cdp".format(file_name[:-4]), "rb") as file:
            encode = decrypt(file.read(), key)
        im = Image.open(BytesIO(base64.b64decode(encode)))
        extension = []
        count = 0
        for i in file_name[::-1]:
            if i == ".":
                count += 1
                if count == 2:
                    break
            extension = [i] + extension
        extension = ''.join(extension[:-4])
        os.remove("coder\\result\\{}.cdp".format(file_name[:-4]))
        im.save('coder\\result\\{}.{}'.format(base64.b64decode(name).decode(), extension))
    else:
        print("Invalid token")
