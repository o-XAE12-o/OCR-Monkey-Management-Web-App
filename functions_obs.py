import csv
import hashlib
import math
import glob
import re
import streamlit as st
from time import sleep
import random
import string
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


# User Management Functions
def account_create(username, hashed_pwd):
    with open(f"users/{username.strip('').lower()}.txt", 'w') as file_local:
        file_local.write(f"{username} {hashed_pwd}\n")


def hash_pw(pwd):
    pwd_bytes = pwd.encode('utf-8')
    hashed_pwd = hashlib.sha256(pwd_bytes).hexdigest()
    return hashed_pwd


def save_user(username, hashed_pwd, email):
    with open("user_details.csv", "a") as f:
        f.write(f"{username}, {hashed_pwd}, {email}\n")


def user_exists(username):
    try:
        with open("user_details.csv", "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if parts[0] == username:
                    return True
    except FileNotFoundError:
        print("user_details.csv not found. Creating a new file.")
    return False


def authenticate_user(email, password):
    hashed_pwd =hash_pw(password)
    try:
        with open("user_details.csv", "r") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if len(row) >= 2 and row[2] == email and row[1] == hashed_pwd:
                    return True
    except FileNotFoundError:
        print("user_details.csv not found.")
    return False


def find_username_by_email(email):
    with open('user_details.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 2 and row[2] == email:
                return row[0]
    return None


def generate_username(first_name, email):
    base_username = first_name.lower() + "_" + email.split('@')[0]
    username = base_username
    while user_exists(username):
        username = base_username + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return username


def store_user_with_generated_username(first_name, email, password):
    hashed_pwd = hash_pw(password)
    username = generate_username(first_name, email)
    save_user(username, hashed_pwd, email)
    account_create(username, hashed_pwd)
    return username


# Utility Functions
def sign(bol):
    if bol:
        return True
    else:
        return False


def ver_code():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str


def is_valid_email(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+([.]\w+)+$'
    if re.match(regex, email):
        return True
    else:
        return False


def is_valid_pw(password):
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_-])[A-Za-z\d@$!#%*?&_-]{6,20}$"
    if re.match(regex, password):
        return True
    else:
        return False


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")
    return pages[ctx.page_script_hash]["page_name"]


def find(email):
    user = glob.glob("users/*.txt")
    email_b = f"{email}.txt"
    length = len(user)
    for j in range(length):
        for i in user:
            if email_b in i:
                return True
            else:
                return False
