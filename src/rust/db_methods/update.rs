use std::collections::HashMap;
use std::error::Error;

use rusqlite::{named_params, Connection};

use crate::data_types::{PreparedStatement, RawTransaction, TransactionAge, Value};
use crate::db_methods::refresh::refresh_db;

// influences all_shares table
pub fn update_transaction_age(db_path: &str) -> Result<(), Box<dyn Error>> {
    let conn = Connection::open(db_path)?;
    let sql = "SELECT transaction_id,
    CASE
      WHEN strftime('%m', date('now')) > strftime('%m', date(timestamp)) THEN strftime('%Y', date('now')) - strftime('%Y', date(timestamp))
      WHEN strftime('%m', date('now')) = strftime('%m', date(timestamp)) THEN
        CASE
          WHEN strftime('%D', date('now')) >= strftime('%D', date(timestamp)) THEN strftime('%Y', date('now')) - strftime('%Y', date(timestamp))
          ELSE strftime('%Y', date('now')) - strftime('%Y', date(timestamp)) - 1
        END
    WHEN strftime('%m', date('now')) < strftime('%m', date(timestamp)) THEN strftime('%Y', date('now')) - strftime('%Y', date(timestamp)) - 1
    END AS 'age' FROM transactions;";

    let mut prepare_sql = PreparedStatement::new(&conn, sql);
    let prepare_iter = prepare_sql.statement.query_map([], |row| {
        Ok(TransactionAge {
            transaction_id: row.get(0)?,
            transaction_age: row.get(1)?,
        })
    })?;

    for transaction in prepare_iter {
        let transaction = transaction.unwrap();
        let transaction_age = transaction.transaction_age;
        let transaction_id = transaction.transaction_id;

        // Set the age of the transaction
        let sql = "UPDATE transactions SET age_transaction = :transaction_age WHERE transaction_id = :transaction_id;";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql.statement.execute(
            named_params! {":transaction_age": &transaction_age, ":transaction_id": &transaction_id},
        )?;

        // Set the amount that are long
        let sql = "UPDATE transactions SET long=(SELECT amount FROM Transactions WHERE age_transaction > 0 and transaction_abbreviation='A') WHERE transaction_id=:transaction_id AND transaction_abbreviation='A' AND age_transaction > 0;";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql
            .statement
            .execute(named_params! {":transaction_id": &transaction_id})?;

        // Set all_shares table
        // Since when a share is disposed, the transaction_id changes, you must check if that id exists
        let sql = "UPDATE all_shares SET age_transaction = :age_transaction WHERE EXISTS ( SELECT transaction_id FROM all_shares WHERE transaction_id = :transaction_id);";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql
            .statement
            .execute(named_params! {":transaction_id": &transaction_id, ":age_transaction": &transaction_age})?;

        let sql = "UPDATE all_shares SET long_counter='+' WHERE EXISTS (SELECT transaction_id FROM all_shares WHERE transaction_id = :transaction_id) AND amount=0 AND age_transaction >= 1 AND long_counter='-';";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql
            .statement
            .execute(named_params! {":transaction_id": &transaction_id})?;
    }

    Ok(())
}

// influences all_shares table and stock_split_history table
pub fn update_table(
    db_path: &str,
    value_dic: &HashMap<String, Value>,
) -> Result<(), Box<dyn Error>> {
    // get values from HashMap of PyDict for table update
    let transaction_type = value_dic
        .get("transaction_type")
        .expect("Error: Failed to get transaction_type in update.rs")
        .clone()
        .unwrap()
        .unwrap_right();
    // see specific types of each value of the hashmap
    // dbg!(value_dic);
    let transaction_id = value_dic
        .get("transaction_id")
        .expect("Error: Failed to get transaction_id in update.rs")
        .clone()
        .unwrap()
        .unwrap_left() as i8;
    let security_name = value_dic
        .get("security_name")
        .expect("Error: Failed to get security_name in update.rs")
        .clone()
        .unwrap()
        .unwrap_right();
    let security_ticker = value_dic
        .get("security_ticker")
        .expect("Error: Failed to get security_ticker in update.rs")
        .clone()
        .unwrap()
        .unwrap_right();
    let institution_name = value_dic
        .get("institution_name")
        .expect("Error: Failed to get institution_name in update.rs")
        .clone()
        .unwrap()
        .unwrap_right();
    let timestamp = value_dic
        .get("timestamp")
        .expect("Error: Failed to get timestamp in update.rs")
        .clone()
        .unwrap()
        .unwrap_right();
    let amount = value_dic
        .get("amount")
        .expect("Error: Failed to get amount in update.rs")
        .clone()
        .unwrap()
        .unwrap_left();
    let age_transaction = value_dic
        .get("age_transaction")
        .expect("Error: Failed to get age_transaction in update.rs")
        .clone()
        .unwrap()
        .unwrap_left() as i8;
    let long = value_dic
        .get("long")
        .expect("Error: Failed to get long in update.rs")
        .clone()
        .unwrap()
        .unwrap_left();
    let raw_price_usd = value_dic.get("price_usd");
    let mut price_usd: f32 = 0.0;
    match raw_price_usd {
        None => {}
        _ => {
            price_usd = raw_price_usd
                .expect("Error: Failed to get price_usd in update.rs")
                .unwrap()
                .unwrap_left();
        }
    }
    let raw_transfer_from = value_dic.get("security_ticker");
    let mut transfer_from = String::from("");
    match raw_transfer_from {
        None => {}
        _ => {
            transfer_from = raw_transfer_from
                .expect("Error: Failed to get transfer_from in update.rs")
                .clone()
                .unwrap()
                .unwrap_right();
        }
    }
    let raw_transfer_to = value_dic.get("security_ticker");
    let mut transfer_to = String::from("");
    match raw_transfer_to {
        None => {}
        _ => {
            transfer_to = raw_transfer_to
                .expect("Error: Failed to get transfer_to in update.rs")
                .clone()
                .unwrap()
                .unwrap_right();
        }
    }

    let transaction_abbreviation;

    match transaction_type.as_str() {
        "Acquire" => {
            transaction_abbreviation = "A".to_string();
        }

        "Dispose" => {
            transaction_abbreviation = "D".to_string();
        }

        "Transfer" => {
            transaction_abbreviation = "T".to_string();
        }

        "Stock Split" => {
            transaction_abbreviation = "SS".to_string();
        }

        _ => {
            panic!("Error: transaction_type is invalid in update.rs")
        }
    }

    let raw_transaction = RawTransaction {
        security_name: { security_name },
        security_ticker: { security_ticker },
        institution_name: { institution_name },
        timestamp: { Some(timestamp) },
        transaction_abbreviation: { transaction_abbreviation },
        amount: { amount },
        price_usd: { Some(price_usd) },
        transfer_from: { Some(transfer_from) },
        transfer_to: { Some(transfer_to) },
        age_transaction: { age_transaction },
        long: { long },
    };
    let edited_raw_transaction = raw_transaction.convert_to_edited_rawtransaction(db_path)?;

    let conn = Connection::open(db_path)?;

    let sql = "UPDATE transactions SET security_id = :sec_id, institution_id = :institution_id,
    timestamp = :timestamp, transaction_abbreviation = :trans_abb, amount = :amount,
    price_USD = :price, transfer_from = :trans_from ,transfer_to = :trans_to WHERE transaction_id = :trans_id;";
    let mut prepare_sql = PreparedStatement::new(&conn, sql);
    prepare_sql.statement.execute(named_params! {
        ":sec_id": edited_raw_transaction.security_id,
        ":institution_id": edited_raw_transaction.institution_id,
        ":timestamp": edited_raw_transaction.timestamp,
        ":trans_abb": edited_raw_transaction.transaction_abbreviation,
        ":amount": edited_raw_transaction.amount,
        ":price": edited_raw_transaction.price_usd,
        ":trans_from": edited_raw_transaction.transfer_from,
        ":trans_to": edited_raw_transaction.transfer_to,
        ":trans_id": transaction_id
    })?;

    refresh_db(db_path)?;

    Ok(())
}

/// TESTS

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_update() {
        use rusqlite::config::DbConfig;
        use std::fs::remove_file;
        use std::fs::File;
        use std::io::prelude::*;

        let db_path = "files/data/test_delete_all.db";
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

        update_transaction_age(db_path).unwrap();

        remove_file(db_path).unwrap_or_else(|_| {
            panic!("Error: remove_file function failed for file: {}", &db_path)
        });
    }
}
