import csv
import sqlite3

def db_create():
    conn = sqlite3.connect("data/coins.db")
    cur = conn.cursor()

    cur.execute("""
    DROP TABLE IF EXISTS coins
    """)

    cur.execute("""
    CREATE TABLE coins (
                year INTEGER,
                denomination TEXT,
                monarch TEXT,
                metal TEXT,
                fineness REAL,
                weight REAL,
                mintmark TEXT,
                variety TEXT,
                grade TEXT
    )
    """)

    with open("data/coins.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cur.execute("""
            INSERT INTO coins (
                year, denomination, monarch, metal,
                fineness, weight, mintmark, variety, grade
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(row["year"]) if row["year"] else None,
                row["denomination"],
                row["monarch"],
                row["metal"],
                float(row["fineness"]) if row["fineness"] else None,
                float(row["weight"]) if row["weight"] else None,
                row["mintmark"],
                row["variety"],
                row["grade"]
            ))

    conn.commit()
    conn.close()