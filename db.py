def run_query(is_count, conn, sql, params=(), count_sql=None):
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()

    if not rows:
        print("No results.")
        return
    
    if is_count:
        count = rows[0][0]
        label = "coin" if count == 1 else "coins"
        print(f"{rows[0][0]} matching {label}.")
    else:
        label = "result" if len(rows) == 1 else "results"
        if count_sql:
            cur.execute(count_sql, params)
            total = cur.fetchone()[0]
            if total == len(rows):
                print(f"Showing {total} {label}.")
            else:
                print(f"Showing {len(rows)} {label} out of {total} matching.")
        else:
            print(f"Showing {len(rows)} {label}.")
        for row in rows:
            out_row = f"{row[0]} {row[1]} - {row[2]} ({row[3]}"
            if row[3] == "silver":
                out_row += f" - {row[4]} fineness"
            out_row += ")"
            if row[5] not in (None, "", "0"):
                out_row += f". {row[5]} mintmark."
            out_row += f" [{row[7]}]"
            print(out_row)

def count_all_coins(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM coins")
    return cur.fetchone()[0]