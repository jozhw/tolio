use std::error::Error;

use rusqlite::{named_params, Connection};

use crate::data_types::{PreparedStatement, TransactionAge};

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
        let sql = "UPDATE transactions SET age_transaction=:transaction_age WHERE transaction_id=:transaction_id;";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql.statement.execute(
            named_params! {":transaction_age": transaction_age, ":transaction_id": transaction_id},
        )?;

        // Set the amount that are long
        let sql = "UPDATE transactions SET long=(SELECT amount FROM Transactions WHERE age_transaction > 0 and transaction_abbreviation='A') WHERE transaction_id=:transaction_id AND transaction_abbreviation='A' AND age_transaction > 0;";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql
            .statement
            .execute(named_params! {":transaction_id": transaction_id})?;

        // Set all_shares table
        // Since when a share is disposed, the transaction_id changes, you must check if that id exists
        let sql = "UPDATE all_shares SET age_transaction=:age_transaction WHERE EXISTS (transaction_id=:transaction_id);";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql
            .statement
            .execute(named_params! {":transaction_id": transaction_id})?;

        let sql = "UPDATE all_shares SET long_counter='+' WHERE EXISTS (transaction_id=:transaction_id) AND amount=0 AND age_transaction >= 1 AND long_counter='-';";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql
            .statement
            .execute(named_params! {":transaction_id": transaction_id})?;
    }

    Ok(())
}
