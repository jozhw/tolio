CREATE TABLE IF NOT EXISTS securities (security_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        security_name TEXT NOT NULL UNIQUE, security_ticker TEXT UNIQUE NOT NULL, amount_held REAL, total_cost REAL,
        cost_basis REAL, number_long REAL,total_price_sold REAL, average_price_sold REAL);

CREATE TABLE IF NOT EXISTS transaction_names (transaction_type_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        transaction_type TEXT UNIQUE NOT NULL, transaction_abbreviation TEXT UNIQUE NOT NULL);

INSERT OR IGNORE INTO transaction_names (transaction_type, transaction_abbreviation) VALUES
            ("Dispose", "D"), ("Acquire", "A"), ("Transfer", "T"), ("Stock_split", "SS");

CREATE TABLE IF NOT EXISTS institutions (institution_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        institution_name TEXT UNIQUE NOT NULL);
        
INSERT OR IGNORE INTO institutions (institution_name) VALUES ("Fidelity"),
            ("Computershare");

CREATE TABLE IF NOT EXISTS transactions(transaction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, security_id INTEGER NOT NULL,
        institution_id NOT NULL INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, transaction_abbreviation TEXT NOT NULL,
        amount REAL, price_USD REAL NOT NULL, transfer_from TEXT, transfer_to TEXT, age_transaction INTEGER, long REAL,
        FOREIGN KEY(institution_id) REFERENCES institutions(institution_id),
        FOREIGN KEY(security_id) REFERENCES securities(security_id),
        FOREIGN KEY(transaction_abbreviation) REFERENCES transaction_names(transaction_abbreviation));

CREATE TABLE IF NOT EXISTS institutions_held (institution_id INTEGER NOT NULL,
        security_id INTEGER NOT NULL, amount_held REAL, total_cost REAL, cost_basis REAL, number_long REAL, total_price_sold REAL, average_price_sold REAL, 
        PRIMARY KEY (institution_id, security_id),
        FOREIGN KEY (institution_id) REFERENCES institutions(institution_id),
        FOREIGN KEY (security_id) REFERENCES securities(security_id));

CREATE TABLE IF NOT EXISTS all_shares (individual_share_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, transaction_id INT, security_id INTEGER NOT NULL,
        institution_id INTEGER NOT NULL, timestamp DATETIME, amount REAL NOT NULL, price_USD REAL NOT NULL, sold_price REAL, age_transaction INTEGER, long_counter TEXT, date_disposed DATETIME,
        FOREIGN KEY(institution_id) REFERENCES institutions(institution_id),
        FOREIGN KEY(security_id) REFERENCES securities(security_id),
        FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id)
        );

CREATE TABLE IF NOT EXISTS stock_split_history (history_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        security_id INTEGER NOT NULL, split_amount INT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (security_id) REFERENCES all_shares(security_id));







