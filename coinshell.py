import sqlite3
import readline

from config import (
    DB_FILE,
    MONARCH_FILE,
    GRADES_FILE,
    DENOMS_FILE,
    METALS_FILE,
    COMMANDS,
)
from aliases import load_aliases
from parser import parse_query
from db import run_query, count_all_coins
from build_db import db_create

def completer(text, state):
    options = [cmd for cmd in COMMANDS if cmd.startswith(text.lower())]
    if state < len(options):
        return options[state]
    return None

def load_all_aliases():
    return {
        "monarchs": load_aliases(MONARCH_FILE),
        "grades": load_aliases(GRADES_FILE),
        "denominations": load_aliases(DENOMS_FILE),
        "metals": load_aliases(METALS_FILE),
    }

def setup_readline():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    try:
        readline.read_history_file(".coin_history")
    except FileNotFoundError:
        pass

def print_help():
    print("Coin Shell help")
    print()
    print("Examples:")
    print("  before 1920")
    print("  monarch george v")
    print("  monarch george v and silver sort year")
    print("  victoria penny")
    print("  silver random")
    print("  silver sort year limit 5")
    print("  count")
    print("  help")
    print("  quit")

def main():
    db_create()
    conn = sqlite3.connect(DB_FILE)
    aliases = load_all_aliases()
    setup_readline()
    total_coins = count_all_coins(conn)

    print("Coin Shell")
    print(f"Database contains {total_coins} coins.")
    print("Press ↑ to recall previous commands. Type 'quit' to exit.")
    print()

    while True:
        try:
            user_input = input("> ").strip()
            sql, params, is_count, is_random, count_sql = parse_query(user_input, aliases)

            if sql == "HELP":
                print_help()
                continue
            
            if sql == "QUIT":
                break

            if sql:
                run_query(is_count, conn, sql, params, count_sql)

        except ValueError as e:
            print("Error: ", e)
        except KeyboardInterrupt:
            print()
            break
        except EOFError:
            print()
            break
        
    conn.close()
    readline.write_history_file(".coin_history")

if __name__ == "__main__":
    main()