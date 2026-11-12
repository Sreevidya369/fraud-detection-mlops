import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "database.db"

def run(conn, title, sql, params=()):
    print(f"\n{title}")
    for row in conn.execute(sql, params):
        print("  ", *row)

def main():
    cust = input("Customer ID (press Enter for all customers): ").strip()
    where, params = ("WHERE customer_id = ?", (cust,)) if cust else ("", ())

    with sqlite3.connect(DB_PATH) as conn:
        run(conn, "Valid transactions:", f"SELECT COUNT(*) FROM transactions {where}", params)
        run(conn, "Total amount:", f"SELECT ROUND(COALESCE(SUM(amount), 0), 2) FROM transactions {where}", params)
        run(conn, "Quarantined transactions:", "SELECT COUNT(*) FROM quarantine_transactions")
        run(conn, "Quarantined by reason:", """
            SELECT rejection_reason, COUNT(*) FROM quarantine_transactions
            GROUP BY rejection_reason ORDER BY COUNT(*) DESC""")
        run(conn, "Transactions by city:", f"""
            SELECT city, COUNT(*) FROM transactions {where}
            GROUP BY city ORDER BY COUNT(*) DESC""", params)
        run(conn, "Transactions by device:", f"""
            SELECT device, COUNT(*) FROM transactions {where}
            GROUP BY device ORDER BY COUNT(*) DESC""", params)
        run(conn, "Top 5 customers by transaction count:", """
            SELECT customer_id, COUNT(*) FROM transactions
            GROUP BY customer_id ORDER BY COUNT(*) DESC LIMIT 5""")

if __name__ == "__main__":
    main()
