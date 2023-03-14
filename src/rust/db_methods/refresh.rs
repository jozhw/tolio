use rusqlite::Connection;
use std::error::Error;

use crate::data_types::Transaction;

/// Used to delete all of the shares from the all_shares table
/// Must not be null or else will error
fn delete_all_from_all_shares(db_path: &str) -> Result<(), Box<dyn Error>> {
    let conn = Connection::open(db_path)?;
    let sql = "DELETE FROM all_shares;";
    conn.execute(sql, ())
        .unwrap_or_else(|_| panic!("Error: Failed to execute: {} ", sql));
    Ok(())
}

/// Used to delete all of the records from stock split history table
/// Must not be null or sel will error
fn delete_all_from_stock_split_history(db_path: &str) -> Result<(), Box<dyn Error>> {
    let conn = Connection::open(db_path)?;
    let sql = "DELETE FROM stock_split_history;";
    conn.execute(sql, ())
        .unwrap_or_else(|_| panic!("Error: Failed to execute: {}", sql));

    Ok(())
}

/// Call to refresh the database after an edit or an action that affects the database
/// Calls the delete all_from_all_shares and delete_all_from_stock_split_history methods
pub fn refresh_db(db_path: &str) -> Result<(), Box<dyn Error>> {
    delete_all_from_all_shares(db_path)?;
    delete_all_from_stock_split_history(db_path)?;
    let transactions = Transaction::get_all_transactions(db_path)?;

    for transaction in transactions {
        transaction.insert_into_all_shares(db_path)?;
    }

    Ok(())
}

/// TESTS

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_delete_all() {
        use rusqlite::config::DbConfig;
        use std::fs::remove_file;
        use std::fs::File;
        use std::io::prelude::*;

        let db_path = "files/data/test_update.db";
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

        delete_all_from_all_shares(db_path).expect("Error: Failed to delete all shares");
        delete_all_from_stock_split_history(db_path)
            .expect("Error: Failed to delete stock split history");

        // Delete database file
        remove_file(db_path).unwrap_or_else(|_| {
            panic!("Error: remove_file function failed for file: {}", &db_path)
        });
    }
}
