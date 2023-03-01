use std::error::Error;

use rusqlite::{named_params, Connection};

use crate::data_types::{EditedRawTransaction, PreparedStatement, RawTransaction, Transaction};

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
        let institution_id = vec[0];

        if institution_id == None {
            self.insert_institution(db_path)?;
            let mut prepared_sql = PreparedStatement::new(&conn, sql);
            let mut rows = prepared_sql
                .statement
                .query((self.institution_name.clone(),))?;
            let mut vec: Vec<Option<i8>> = Vec::new();
            while let Some(row) = rows.next()? {
                vec.push(row.get(0)?);
            }
            let institution_id = institution_id.unwrap();
            Ok(institution_id)
        } else {
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
        let security_id = vec[0];
        if security_id == None {
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
            let security_id = security_id.unwrap();
            Ok(security_id)
        }
    }

    pub fn insert_into_transactions(&self, db_path: &str) -> Result<(), Box<dyn Error>> {
        let conn = Connection::open(db_path)?;
        let security_id = self.get_security_id(db_path).unwrap();
        let institution_id = self.get_institution_id(db_path).unwrap();
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

impl EditedRawTransaction {}
