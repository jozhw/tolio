CREATE TABLE IF NOT EXISTS securities (security_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        security_name TEXT NOT NULL UNIQUE, security_ticker TEXT UNIQUE NOT NULL, amount_held REAL, total_cost REAL,
        cost_basis REAL, number_long REAL,total_price_sold REAL, average_price_sold REAL);

INSERT OR IGNORE INTO securities (security_name, security_ticker, amount_held,
total_cost, cost_basis, number_long
) VALUES
        ("S&P500", "SPY", 20, 200, 10, 20),
        ("Tesla", "TSLA", 20, 100, 5, 20);

CREATE TABLE IF NOT EXISTS transaction_names (transaction_type_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        transaction_type TEXT UNIQUE NOT NULL, transaction_abbreviation TEXT UNIQUE NOT NULL);

INSERT OR IGNORE INTO transaction_names (transaction_type, transaction_abbreviation) VALUES
            ("Dispose", "D"), ("Acquire", "A"), ("Transfer", "T"), ("Stock_Split", "SS");

CREATE TABLE IF NOT EXISTS institutions (institution_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        institution_name TEXT UNIQUE NOT NULL);

INSERT OR IGNORE INTO institutions (institution_name) VALUES ("Fidelity"),
            ("Computershare");

CREATE TABLE IF NOT EXISTS transactions(transaction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, security_id INTEGER NOT NULL,
        institution_id INTEGER, timestamp TEXT DEFAULT CURRENT_TIMESTAMP, transaction_abbreviation TEXT NOT NULL,
        amount REAL, price_USD REAL, transfer_from TEXT, transfer_to TEXT, age_transaction INTEGER, long REAL,
        FOREIGN KEY(institution_id) REFERENCES institutions(institution_id),
        FOREIGN KEY(security_id) REFERENCES securities(security_id),
        FOREIGN KEY(transaction_abbreviation) REFERENCES transaction_names(transaction_abbreviation));

INSERT OR IGNORE INTO transactions(security_id, institution_id, timestamp, transaction_abbreviation,
amount, price_USD, age_transaction, long) VALUES
        (1, 1, "2022-01-01", "A", 10, 100, 1, 10),
        (2, 1, "2022-02-02", "A", 20, 100, 1, 20),
        (1, 2, "2022-03-03", "A", 10, 100, 1, 10);


CREATE TABLE IF NOT EXISTS institutions_held (institution_id INTEGER NOT NULL,
        security_id INTEGER NOT NULL, amount_held REAL, total_cost REAL, cost_basis REAL, number_long REAL, total_price_sold REAL, average_price_sold REAL, 
        PRIMARY KEY (institution_id, security_id),
        FOREIGN KEY (institution_id) REFERENCES institutions(institution_id),
        FOREIGN KEY (security_id) REFERENCES securities(security_id));

INSERT OR IGNORE INTO institutions_held(institution_id, security_id, amount_held, total_cost, cost_basis,
number_long, total_price_sold, average_price_sold) VALUES
        (1, 1, 10, 100, 10, 10, 0, 0),
        (2, 1, 20, 100, 5, 20, 0, 0),
        (1, 2, 10, 100, 10, 10, 0, 0);


CREATE TABLE IF NOT EXISTS all_shares (individual_share_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, transaction_id INT, security_id INTEGER NOT NULL,
        institution_id INTEGER NOT NULL, timestamp DATETIME, amount REAL NOT NULL, price_USD REAL NOT NULL, sold_price REAL, age_transaction INTEGER, long_counter TEXT, date_disposed DATETIME,   FOREIGN KEY(institution_id) REFERENCES institutions(institution_id),
            FOREIGN KEY(security_id) REFERENCES securities(security_id),
            FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id));

CREATE TABLE IF NOT EXISTS all_shares_split (individual_share_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, transaction_id INT, security_id INTEGER NOT NULL,
            institution_id INTEGER NOT NULL, timestamp DATETIME, amount REAL NOT NULL, price_USD REAL NOT NULL, sold_price REAL, age_transaction INTEGER, long_counter TEXT, date_disposed DATETIME,
            FOREIGN KEY(institution_id) REFERENCES institutions(institution_id),
            FOREIGN KEY(security_id) REFERENCES securities(security_id),
            FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id)
            );

CREATE TABLE IF NOT EXISTS stock_split_history (history_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        security_id INTEGER NOT NULL, security_name TEXT NOT NULL, ticker TEXT NOT NULL, split_amount INT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (security_id) REFERENCES all_shares(security_id));

