import pandas as pd
import argparse
import readline

coins = pd.read_csv("coins.csv")

COMMANDS = ["sterling", "before", "monarchs", "silver", "year", "monarch", "denom", "silverweight"]

def completer(text, state):
    options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

parser = argparse.ArgumentParser(description="Coin Collection Analyser")
parser.add_argument("command", nargs="?", help="analysis command")
parser.add_argument("value", nargs="?")
parser.add_argument("--sort", help="column to sort by")
parser.add_argument("column", nargs="?")

args = parser.parse_args()

result = None
result_str = None

if not vars(args) or not args.command:
    while True:
        command = input("> ").strip()
        if command == "quit":
            break
        parts = command.split()
        if parts[0] == "sterling":
            result = coins[coins.fineness == 92.5] [["year", "denomination", "monarch"]]
            result_str = "Number of sterling coins: " + str(len(coins[coins.fineness == 92.5]))
        elif parts[0] == "monarchs":
            result = coins["monarch"].value_counts()
            result_str = "Coins by monarch: " + str(result)
        elif parts[0] == "silver":
            result = coins[coins["metal"] == "silver"]
            result_str = "Number of silver coins: " + str(len(coins[coins["metal"] == "silver"]))
        elif parts[0] == "year":
            result = coins[coins["year"] == int(parts[1])] [["year", "denomination", "monarch"]]
            numcoins = str(len(coins[coins["year"] == int(parts[1])]))
            result_str = "Number of " + parts[1] + " coins: " + numcoins
        elif parts[0] == "monarch":
            name = " ".join(parts[1:])
            result = coins[coins["monarch"] == name]
            result_str = "Number of coins of " + name + ": " + str(len(coins[coins["monarch"] == name]))
        elif parts[0] == "before":
            year = int(parts[1])
            result = coins[coins["year"] < year] [["year", "denomination", "monarch"]]
            result_str = "Number of " + parts[1] + " coins: " + str(len(coins[coins["year"] == year]))
        elif parts[0] == "denom":
            result = coins["denomination"].value_counts()
        elif parts[0] == "silverweight":
            coins["silver_weight"] = coins["weight"] * coins["fineness"] / 100
            result = "Total silver weight: " + str(round(coins["silver_weight"].sum(), 2)) + " grams."
        else:
            result = "Unknown command, please try again."
        print(f"Total number of coins searched: {len(coins[coins["year"] > 0])}")
        if result is not None:
            print(result)
            if result_str is not None:
                print(result_str)
elif args.command == "sterling":
    result = coins[coins.fineness == 92.5] [["year", "denomination", "monarch"]]
    result_str = "Number of sterling coins: " + str(len(coins[coins.fineness == 92.5]))
elif args.command == "monarchs":
    result = coins["monarch"].value_counts()
    result_str = "Coins by monarch: " + str(result)
elif args.command == "silver":
    result = coins[coins["metal"] == "silver"]
    result_str = "Number of silver coins: " + str(len(coins[coins["metal"] == "silver"]))
elif args.command == "year":
    result = coins[coins["year"] == int(args.value)] [["year", "denomination", "monarch"]]
    result_str = "Number of " + args.value + " coins: " + str(len(coins[coins["year"] == int(args.value)]))
elif args.command == "monarch":
    result = coins[coins["monarch"] == args.value]
    result_str = "Number of coins of " + args.value + ": " + str(len(coins[coins["monarch"] == args.value]))
elif args.command == "before":
    result = coins[coins["year"] < int(args.value)]
    result_str = "Number of coins older than " + args.value + ": " + len(coins[coins["year"] < int(args.value)])
elif args.command == "denom":
    result = coins["denomination"].value_counts()
elif args.command == "silverweight":
    coins["silver_weight"] = coins["weight"] * coins["fineness"] / 100
    result = "Total silver weight: " + str(round(coins["silver_weight"].sum(), 2)) + " grams."
else:
    print(f"Unknown option: {args.command}")

if result is not None:
    if args.sort:
        result = result.sort_values(args.sort)
    print(result)
    if result_str is not None:
        print(result_str)

print(f"Total number of coins searched: {len(coins[coins["year"] > 0])}")