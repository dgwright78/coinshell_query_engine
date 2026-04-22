import csv

def load_aliases(filename):
    aliases = {}
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            aliases[row["alias"].strip().lower()] = row["canonical"].strip()
    return aliases