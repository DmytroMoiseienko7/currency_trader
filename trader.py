from random import uniform
from argparse import ArgumentParser
import json

args = ArgumentParser()

args.add_argument("command", nargs='?')
args.add_argument("second_command", nargs='?')
args = vars(args.parse_args())
command = args["command"]
second_command = args["second_command"]

file_config = "config.json"
FILE_MEMORY = "Memory.json"

def balance_update(balance_UAH, balance_USD):
    data = read_json_file(FILE_MEMORY)
    data["account_UAH"] = round(balance_UAH, 2)
    data["account_USD"] = round(balance_USD, 2)
    write_to_json(FILE_MEMORY, data)


def update_rate(price, delta):
    next_cur = round(uniform((price - delta), (price + delta)), 2)
    return next_cur


def show_available(account_UAH, account_USD):
    return f'Your current balance is: \n {account_UAH} UAH \n {account_USD} USD'


def currency_rate_generator(price, delta):
    return round(uniform((price - delta), (price + delta)), 2)


def read_json_file(file_json_name):
    with open(file_json_name, 'r') as file:
        data = json.load(file)
    return data


def write_to_json(file_json_name, data):
    with open(file_json_name, 'w') as file:
        json.dump(data, file)

def buy_usd(amount_usd, balance_UAH, balance_USD, current_rate):
    uah_conv = amount_usd * current_rate
    if uah_conv > balance_UAH:
        print(f"UNAVAILABLE, REQUIRED BALANCE UAH {uah_conv} AVAILABLE {account_UAH} ")
    else:
        balance_UAH -= uah_conv
        balance_USD += amount_usd
        balance_update(balance_UAH, balance_USD)

def sell_usd(amount_usd, balance_UAH, balance_USD, current_rate):
    uah_conv = amount_usd * current_rate
    if amount_usd > account_USD:
        print(f"UNAVAILABLE, REQUIRED BALANCE USD {amount_usd}, AVAILABLE {account_USD}")
    else:
        balance_UAH += uah_conv
        balance_USD -= amount_usd
        balance_update(balance_UAH, balance_USD)


def buy_all(balance_UAH, balance_USD, current_rate):
    usd_conv = round(balance_UAH / current_rate, 2)
    balance_UAH = 0
    balance_USD += usd_conv
    balance_update(balance_UAH, balance_USD)

def sell_all(balance_UAH, balance_USD, current_rate):
    uah_conv = round(balance_USD * current_rate)
    balance_UAH += uah_conv
    balance_USD = 0
    balance_update(balance_UAH, balance_USD)

def restart_game(default_balance_UAH, default_balance_USD, default_rate):
    data["account_UAH"] = default_balance_UAH
    data["account_USD"] = default_balance_USD
    data["current_rate"] = default_rate
    write_to_json(FILE_MEMORY, data)


default_rate = read_json_file(file_config)["current_rate"]
default_balance_UAH = read_json_file(file_config)["account_UAH"]
default_balance_USD = read_json_file(file_config)["account_USD"]
price = read_json_file(file_config)["price"]
delta = read_json_file(file_config)["delta"]
currency_rate = currency_rate_generator(price, delta)
account_UAH = read_json_file(FILE_MEMORY)["account_UAH"]
account_USD = read_json_file(FILE_MEMORY)["account_USD"]
available = show_available(account_UAH, account_USD)
current_rate = read_json_file(FILE_MEMORY)["current_rate"]
data = read_json_file(FILE_MEMORY)
data["current_rate"] = currency_rate

if command == "RATE":
    if current_rate == 0:
        write_to_json(FILE_MEMORY, data)
        current_rate = read_json_file(FILE_MEMORY)["current_rate"]
        print(current_rate)
    else:
        print(current_rate)
elif command == "NEXT":
    write_to_json(FILE_MEMORY, data)
elif command == "AVAILABLE":
    print(available)
elif command == "BUY" and second_command.isdigit():
    buy_usd(float(second_command), account_UAH, account_USD,current_rate)
elif command == "SELL" and second_command.isdigit():
    sell_usd(float(second_command), account_UAH, account_USD,current_rate)
elif command == "BUY" and second_command == "ALL":
    buy_all(account_UAH, account_USD, current_rate)
elif command == "SELL" and second_command == "ALL":
    sell_all(account_UAH, account_USD, current_rate)
elif command == "RESTART":
    restart_game(default_balance_UAH, default_balance_USD, default_rate)