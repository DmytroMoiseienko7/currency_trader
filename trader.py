from random import uniform
from argparse import ArgumentParser
import json

args = ArgumentParser()

args.add_argument("command", nargs='?')
args.add_argument("amount", type=float, nargs='?')
args = vars(args.parse_args())
command = args["command"]
cur_amount = args["amount"]

file_config = "config.json"
file_Memory = "Memory.json"


def balance_update(balance_UAH, balance_USD):
    data = read_json_file(file_Memory)
    data["account_UAH"] = round(balance_UAH, 2)
    data["account_USD"] = round(balance_USD, 2)
    write_to_json(file_Memory, data)


def update_rate(price, delta):
    next_cur = round(uniform((price - delta), (price + delta)), 2)
    return next_cur


def show_available(account_UAH, account_USD):
    return f'Остаток на счету: \n {account_UAH} UAH \n {account_USD} USD'


def currency_rate_generator(price, delta):
    return round(uniform((price - delta), (price + delta)), 2)


def read_json_file(file_json_name):
    with open(file_json_name, 'r') as file:
        data = json.load(file)
    return data


def write_to_json(file_json_name, data):
    with open(file_json_name, 'w') as file:
        json.dump(data, file)


def buy_usd(amount_usd, balance_UAH, balance_USD):
    uah_conv = amount_usd * current_rate
    if uah_conv > balance_UAH:
        print(f"UNAVAILABLE, REQUIRED BALANCE UAH {uah_conv} AVAILABLE {account_UAH} ")
    else:
        balance_UAH -= uah_conv
        balance_USD += amount_usd
        balance_update(balance_UAH, balance_USD)


def sell_usd(amount_usd, balance_UAH, balance_USD):
    uah_conv = amount_usd * current_rate
    if amount_usd > account_USD:
        print(f"UNAVAILABLE, REQUIRED BALANCE USD {amount_usd}, AVAILABLE {account_USD}")
    else:
        balance_UAH += uah_conv
        balance_USD -= amount_usd
        balance_update(balance_UAH, balance_USD)


def buy_all(balance_UAH, balance_USD):
    usd_conv = round(balance_UAH / current_rate, 2)
    balance_UAH = 0
    balance_USD += usd_conv
    balance_update(balance_UAH, balance_USD)


def sell_all(balance_UAH, balance_USD):
    uah_conv = round(balance_USD * current_rate)
    balance_UAH += uah_conv
    balance_USD = 0
    balance_update(balance_UAH, balance_USD)


def restart_game():
    balance_UAH = read_json_file(file_config)["account_UAH"]
    balance_USD = read_json_file(file_config)["account_USD"]
    balance_update(balance_UAH, balance_USD)
    data["current_rate"] = rate_for_restart
    write_to_json(file_Memory, data)


rate_for_restart = read_json_file(file_config)["current_rate"]
price = read_json_file(file_config)["price"]
delta = read_json_file(file_config)["delta"]
currency_rate = currency_rate_generator(price, delta)
account_UAH = read_json_file(file_Memory)["account_UAH"]
account_USD = read_json_file(file_Memory)["account_USD"]
available = show_available(account_UAH, account_USD)
current_rate = read_json_file(file_Memory)["current_rate"]
data = read_json_file(file_Memory)
data["current_rate"] = currency_rate

if command == "RATE":
    if current_rate == 0:
        write_to_json(file_Memory, data)
        current_rate = read_json_file(file_Memory)["current_rate"]
        print(current_rate)
    else:
        print(current_rate)
elif command == "NEXT":
    write_to_json(file_Memory, data)
elif command == "AVAILABLE":
    print(available)
elif command == "BUY":
    buy_usd(cur_amount, account_UAH, account_USD)
elif command == "SELL":
    sell_usd(cur_amount, account_UAH, account_USD)
elif command == "BUY_ALL":
    buy_all(account_UAH, account_USD)
elif command == "SELL_ALL":
    sell_all(account_UAH, account_USD)
elif command == "RESTART":
    restart_game()
