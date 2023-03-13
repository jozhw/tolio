use std::error::Error;

use rusqlite::{named_params, Connection};

use crate::data_types::{EditedRawTransaction, PreparedStatement, RawTransaction};

impl RawTransaction {
    pub fn new_acquire_or_dispose(
        security_name: String,
        security_ticker: String,
        institution_name: String,
        timestamp: String,
        transaction_abbreviation: String,
        amount: f32,
        price_usd: f32,
    ) -> Result<RawTransaction, Box<dyn Error>> {
        Ok(RawTransaction {
            security_name: (security_name),
            security_ticker: (security_ticker),
            institution_name: (institution_name),
            timestamp: (Some(timestamp)),
            transaction_abbreviation: (transaction_abbreviation),
            amount: (amount),
            price_usd: (Some(price_usd)),
            transfer_from: (None),
            transfer_to: (None),
            age_transaction: (0),
            long: (0.0),
        })
    }
    fn insert_security(&self, db_path: &str) -> Result<(), Box<dyn Error>> {
        let conn = Connection::open(db_path)?;
        let sql = "INSERT INTO securities (security_name, security_ticker) VALUES (?,?);";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql
            .statement
            .execute((self.security_name.clone(), self.security_ticker.clone()))?;

        Ok(())
    }

    fn insert_institution(&self, db_path: &str) -> Result<(), Box<dyn Error>> {
        let conn = Connection::open(db_path)?;
        let sql = "INSERT INTO institutions (institution_name) VALUES (?);";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql
            .statement
            .execute((self.institution_name.clone(),))?;
        Ok(())
    }

    pub fn get_institution_id(&self, db_path: &str) -> Result<i8, Box<dyn Error>> {
        let conn = Connection::open(db_path)?;
        let sql = "SELECT institution_id FROM institutions WHERE institution_name=?;";
        let mut prepared_sql = PreparedStatement::new(&conn, sql);
        let mut rows = prepared_sql
            .statement
            .query((self.institution_name.clone(),))?;
        let mut vec: Vec<Option<i8>> = Vec::new();
        while let Some(row) = rows.next()? {
            vec.push(row.get(0)?);
        }

        if vec.len() == 0 {
            self.insert_institution(db_path)?;
            let mut prepared_sql = PreparedStatement::new(&conn, sql);
            let mut rows = prepared_sql
                .statement
                .query((self.institution_name.clone(),))?;
            let mut vec: Vec<Option<i8>> = Vec::new();
            while let Some(row) = rows.next()? {
                vec.push(row.get(0)?);
            }
            let institution_id = vec[0].unwrap();
            Ok(institution_id)
        } else {
            let institution_id = vec[0];
            let institution_id = institution_id.unwrap();
            Ok(institution_id)
        }
    }

    pub fn get_security_id(&self, db_path: &str) -> Result<i8, Box<dyn Error>> {
        let conn = Connection::open(db_path)?;
        let sql = "SELECT security_id FROM securities WHERE security_name=? AND security_ticker=?;";
        let mut prepared_sql = PreparedStatement::new(&conn, sql);
        let mut rows = prepared_sql
            .statement
            .query((self.security_name.clone(), self.security_ticker.clone()))?;
        let mut vec: Vec<Option<i8>> = Vec::new();
        while let Some(row) = rows.next()? {
            vec.push(row.get(0)?);
        }

        // if the result of the prepared statement is none, then the variable vec will contain no elements
        if vec.len() == 0 {
            self.insert_security(db_path)?;
            let mut prepared_sql = PreparedStatement::new(&conn, sql);
            let mut rows = prepared_sql
                .statement
                .query((self.security_name.clone(), self.security_ticker.clone()))?;
            let mut vec: Vec<Option<i8>> = Vec::new();
            while let Some(row) = rows.next()? {
                vec.push(row.get(0)?);
            }
            let security_id = vec[0].unwrap();
            Ok(security_id)
        } else {
            let security_id = vec[0];
            let security_id = security_id.unwrap();
            Ok(security_id)
        }
    }

    pub fn insert_into_transactions(&self, db_path: &str) -> Result<(), Box<dyn Error>> {
        let conn = Connection::open(db_path)?;
        let security_id = self.get_security_id(db_path).unwrap();
        let institution_id = self.get_institution_id(db_path).unwrap();
        let timestamp = self.timestamp.clone();
        match timestamp {
            None => {
                let sql = "INSERT INTO transactions(security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long) VALUES (:security_id,:institution_id, datetime(CURRENT_TIMESTAMP, 'localtime'),:transaction_abbreviation,:amount,:price_USD,:transfer_from,:transfer_to,:age_transaction,:long);";
                let mut prepare_sql = PreparedStatement::new(&conn, sql);

                prepare_sql.statement.execute(named_params! {
                    ":security_id": security_id,
                    ":institution_id": institution_id,
                    ":transaction_abbreviation": self.transaction_abbreviation,
                    ":amount": self.amount,
                    ":price_USD": self.price_usd,
                    ":transfer_from": self.transfer_from,
                    ":transfer_to": self.transfer_to,
                    ":age_transaction": self.age_transaction,
                    ":long": self.long
                })?;
            }
            _ => {
                let sql = "INSERT INTO transactions(security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long) VALUES (:security_id,:institution_id,:timestamp,:transaction_abbreviation,:amount,:price_USD,:transfer_from,:transfer_to,:age_transaction,:long);";
                let mut prepare_sql = PreparedStatement::new(&conn, sql);

                prepare_sql.statement.execute(named_params! {
                    ":security_id": security_id,
                    ":institution_id": institution_id,
                    ":timestamp": self.timestamp,
                    ":transaction_abbreviation": self.transaction_abbreviation,
                    ":amount": self.amount,
                    ":price_USD": self.price_usd,
                    ":transfer_from": self.transfer_from,
                    ":transfer_to": self.transfer_to,
                    ":age_transaction": self.age_transaction,
                    ":long": self.long
                })?;
            }
        }

        Ok(())
    }

    pub fn convert_to_edited_rawtransaction(
        &self,
        db_path: &str,
    ) -> Result<EditedRawTransaction, Box<dyn Error>> {
        let security_id = self
            .get_security_id(db_path)
            .expect("Error: Failed to get security id.");
        let institution_id = self
            .get_institution_id(db_path)
            .expect("Error: Failed to get institution id.");
        let timestamp = self.timestamp.clone();
        let transaction_abbreviation = self.transaction_abbreviation.clone();
        let amount = self.amount;
        let price_usd = self.price_usd;
        let transfer_from = self.transfer_from.clone();
        let transfer_to = self.transfer_to.clone();
        let age_transaction = self.age_transaction;
        let long = self.long;

        Ok(EditedRawTransaction {
            security_id,
            institution_id,
            timestamp,
            transaction_abbreviation,
            amount,
            price_usd,
            transfer_from,
            transfer_to,
            age_transaction,
            long,
        })
    }
}

/// TESTS

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_insert_and_get_functions() {
        use rusqlite::config::DbConfig;
        use std::fs::remove_file;
        use std::fs::File;
        use std::io::prelude::*;

        let db_path = "files/data/test_raw_transaction.db";
        let conn = &mut Connection::open(db_path)
            .unwrap_or_else(|_| panic!("Error: Failed to open database: {} ", db_path));
        let _ = conn.set_db_config(DbConfig::SQLITE_DBCONFIG_ENABLE_FKEY, true);

        let mut file = File::open("test/queries/test_rs_db_query.sql").unwrap();
        let mut contents = String::new();
        file.read_to_string(&mut contents).unwrap();
        // Split each sql command and execute each
        let split = contents.split(";");
        let vec: Vec<&str> = split.collect();
        for command in vec {
            if command == "" {
                // prevent the trailing space from the split function from executing
            } else {
                conn.execute(command, [])
                    .unwrap_or_else(|_| panic!("Error: Failed to execute command: {}", command));
                conn.transaction().unwrap().commit().unwrap();
            }
        }
        // test exiting values
        {
            // with existing security and institution
            let test_transaction = RawTransaction {
                security_name: "Tesla".to_string(),
                security_ticker: "TSLA".to_string(),
                institution_name: "Computershare".to_string(),
                timestamp: Some("2022-03-03".to_string()),
                transaction_abbreviation: "A".to_string(),
                amount: 10.0,
                price_usd: Some(100.0),
                transfer_from: None,
                transfer_to: None,
                age_transaction: 0,
                long: 0.0,
            };

            // test to see if existing security can be get
            let security_id = test_transaction.get_security_id(db_path).unwrap();
            assert_eq!(security_id, 2);

            // test to see if existing insitution can be get
             let institution_id = test_transaction.get_institution_id(db_path).unwrap();
             assert_eq!(institution_id, 2);

            // insert existing into the transactions table
            test_transaction.insert_into_transactions(db_path).unwrap();

        }
        // test new values
        {
            // with new security and institution
            let test_transaction = RawTransaction {
                security_name: "Microsoft".to_string(),
                security_ticker: "MSFT".to_string(),
                institution_name: "Charles Schwab".to_string(),
                timestamp: Some("2022-03-03".to_string()),
                transaction_abbreviation: "A".to_string(),
                amount: 10.0,
                price_usd: Some(100.0),
                transfer_from: None,
                transfer_to: None,
                age_transaction: 0,
                long: 0.0,
            };

            // get the security_id from a new security

            let security_id = test_transaction.get_security_id(db_path).unwrap();
            assert_eq!(security_id, 3);

            // get the institution_id from new transaction
            let institution_id = test_transaction.get_institution_id(db_path).unwrap();
            assert_eq!(institution_id, 3);

            // insert new into the transactions table
            test_transaction.insert_into_transactions(db_path).unwrap();
        }

        remove_file(db_path).unwrap_or_else(|_| {
            panic!("Error: remove_file function failed for file: {}", &db_path)
        });
    }
}
