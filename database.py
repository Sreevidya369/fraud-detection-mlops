import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "database.db"


def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                customer_id TEXT,
                amount REAL,
                merchant TEXT,
                city TEXT,
                device TEXT,
                timestamp TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS quarantined_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT,
                raw_data TEXT,
                rejection_reason TEXT NOT NULL,
                rejected_at TEXT NOT NULL
            )
        """)

        expected_columns = {
            "transaction_id", "customer_id", "amount", "txn_count_5m",
            "amount_sum_1h", "avg_prior_amount", "amount_ratio",
            "city_changed", "feature_timestamp",
        }
        existing_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(transaction_features)")
        }
        if existing_columns and existing_columns != expected_columns:
            conn.execute("DROP TABLE transaction_features")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS transaction_features (
                transaction_id TEXT PRIMARY KEY,
                customer_id TEXT,
                amount REAL,
                txn_count_5m INTEGER,
                amount_sum_1h REAL,
                avg_prior_amount REAL,
                amount_ratio REAL,
                city_changed INTEGER,
                feature_timestamp TEXT,
                FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS fraud_predictions (
                transaction_id TEXT PRIMARY KEY,
                fraud_score REAL NOT NULL,
                is_suspicious INTEGER NOT NULL,
                model_version TEXT NOT NULL,
                predicted_at TEXT NOT NULL,
                FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
            )
        """)

    print("Database tables are ready at:", DB_PATH)


if __name__ == "__main__":
    create_database()
    

