use rusqlite::Connection;
use std::error::Error;

use crate::data_types::{PreparedStatement, Transaction};

fn delete_all_from_all_shares(db_path: &str) -> Result<(), Box<dyn Error>> {
    let conn = Connection::open(db_path)?;
    let sql = "DELETE FROM all_shares;";
    let mut prepared_sql = PreparedStatement::new(&conn, sql);
    prepared_sql.statement.execute([])?;

    Ok(())
}

fn delete_all_from_stock_split_history(db_path: &str) -> Result<(), Box<dyn Error>> {
    let conn = Connection::open(db_path)?;
    let sql = "DELETE FROM stock_split_history;";
    let mut prepared_sql = PreparedStatement::new(&conn, sql);
    prepared_sql.statement.execute([])?;

    Ok(())
}

pub fn refresh_db(db_path: &str) -> Result<(), Box<dyn Error>> {
    delete_all_from_all_shares(db_path)?;
    delete_all_from_stock_split_history(db_path)?;
    let transactions = Transaction::get_all_transactions(db_path)?;

    for transaction in transactions {
        transaction.insert_into_all_shares(db_path)?;
    }

    Ok(())
}
