use rusqlite::config::DbConfig;
use rusqlite::{Connection, Result, ToSql, Transaction};
use std::env;

use crate::data_types::Share;

pub fn batch_insert(mut count: usize, tx: &Transaction, vector_proto: Vec<Share>) {
    let mut vector = vector_proto.clone();
    // Determine the batch size
    let mut min_batch_size = 50;
    let mut remainder: bool = false;
    let remainder_amount = 0;
    let mut times_iter = 1;

    if count < min_batch_size {
        min_batch_size = count;
    } else if count / min_batch_size > 1 {
        remainder = true;
        let remainder_amount = count / min_batch_size;

        // Make sure that count is an integer that is divisible by min_batch_size
        count = count - remainder_amount;
        times_iter = count / min_batch_size;
    }
    // Create the parameters of insert for the sql query
    let mut insert_param = " (?,?,?,?,?,?,?,?,?,?),".repeat(min_batch_size as usize);
    // Because the original counts, the total would be 51, but pop will bring it down to 50
    insert_param.pop();
    let insert_param = insert_param.as_str();

    // Create the standardized query
    let st = format!("INSERT INTO all_shares_split(transaction_id, security_id, institution_id, timestamp, amount, price_USD, sold_price, age_transaction, long_counter, date_disposed)
    VALUES {};", insert_param);

    let mut sql_statement = tx.prepare_cached(st.as_str()).unwrap();
    for _ in 0..(times_iter) {
        let mut param_values: Vec<_> = Vec::new();
        let push_vec: Vec<_> = vector.drain(..&min_batch_size).collect();
        for batch in push_vec.iter() {
            param_values.push(&batch.transaction_id as &dyn ToSql);
            param_values.push(&batch.security_id as &dyn ToSql);
            param_values.push(&batch.institution_id as &dyn ToSql);
            param_values.push(&batch.timestamp as &dyn ToSql);
            param_values.push(&batch.amount as &dyn ToSql);
            param_values.push(&batch.price_usd as &dyn ToSql);
            param_values.push(&batch.sold_price as &dyn ToSql);
            param_values.push(&batch.age_transaction as &dyn ToSql);
            param_values.push(&batch.long_counter as &dyn ToSql);
            param_values.push(&batch.date_disposed as &dyn ToSql);
        }
        sql_statement.execute(&*param_values).unwrap();
    }
    // add the remainder that was not part of the complete 50
    if remainder == true {
        let mut insert_param = " (?,?,?,?,?,?,?,?,?,?),".repeat(remainder_amount as usize);
        insert_param.pop();
        let insert_param = insert_param.as_str();

        // Create the standardized query
        let st = format!("INSERT INTO all_shares_split(transaction_id, security_id, institution_id, timestamp, amount, price_USD, sold_price, age_transaction, long_counter, date_disposed)
        VALUES {}", insert_param);
        let mut sql_statement = tx.prepare_cached(st.as_str()).unwrap();
        for _ in 0..(remainder_amount) {
            let mut param_values: Vec<_> = Vec::new();
            let push_vec: Vec<_> = vector.drain(0..).collect();
            for batch in push_vec.iter() {
                param_values.push(&batch.transaction_id as &dyn ToSql);
                param_values.push(&batch.security_id as &dyn ToSql);
                param_values.push(&batch.institution_id as &dyn ToSql);
                param_values.push(&batch.timestamp as &dyn ToSql);
                param_values.push(&batch.amount as &dyn ToSql);
                param_values.push(&batch.price_usd as &dyn ToSql);
                param_values.push(&batch.sold_price as &dyn ToSql);
                param_values.push(&batch.age_transaction as &dyn ToSql);
                param_values.push(&batch.long_counter as &dyn ToSql);
                param_values.push(&batch.date_disposed as &dyn ToSql);
            }
            sql_statement.execute(&*param_values).unwrap();
        }
    }
}

pub fn insert(tx: &Transaction, split: bool, vector_proto: &Vec<Share>) {
    let vector = vector_proto.clone();
    if split == false {
        let count: usize = vector.len();
        if count != 0 {
            batch_insert(count, tx, vector)
        } else {
            // ignore
        }
    } else if split == true {
        let mut split_vector: Vec<Share> = Vec::new();

        // Iterate through the initial vector with the split values and push to new vector for the splited shares
        for security in vector.iter() {
            if security.amount % 1 as f32 == 0.0 {
                for _ in 0..security.amount as usize {
                    split_vector.push(Share {
                        transaction_id: security.transaction_id,
                        security_id: security.security_id,
                        institution_id: security.institution_id,
                        timestamp: security.timestamp.clone(),
                        amount: 1.0,
                        price_usd: security.price_usd / security.amount,
                        sold_price: security.sold_price,
                        age_transaction: security.age_transaction.clone(),
                        long_counter: security.long_counter.clone(),
                        date_disposed: security.date_disposed.clone(),
                    })
                }
            } else if security.amount < 1.0 {
                split_vector.push(Share {
                    transaction_id: security.transaction_id,
                    security_id: security.security_id,
                    institution_id: security.institution_id,
                    timestamp: security.timestamp.clone(),
                    amount: security.amount,
                    price_usd: security.price_usd,
                    sold_price: security.sold_price,
                    age_transaction: security.age_transaction.clone(),
                    long_counter: security.long_counter.clone(),
                    date_disposed: security.date_disposed.clone(),
                })
            } else {
                let whole_share: f32 = security.amount - (security.amount % 1.0);
                for _ in 0..whole_share as usize {
                    split_vector.push(Share {
                        transaction_id: security.transaction_id,
                        security_id: security.security_id,
                        institution_id: security.institution_id,
                        timestamp: security.timestamp.clone(),
                        amount: 1.0,
                        price_usd: security.price_usd,
                        sold_price: security.sold_price,
                        age_transaction: security.age_transaction.clone(),
                        long_counter: security.long_counter.clone(),
                        date_disposed: security.date_disposed.clone(),
                    })
                }
                split_vector.push(Share {
                    transaction_id: security.transaction_id,
                    security_id: security.security_id,
                    institution_id: security.institution_id,
                    timestamp: security.timestamp.clone(),
                    amount: security.amount,
                    price_usd: security.price_usd,
                    sold_price: security.sold_price,
                    age_transaction: security.age_transaction.clone(),
                    long_counter: security.long_counter.clone(),
                    date_disposed: security.date_disposed.clone(),
                })
            }
        }

        // Define count variable
        let count: usize = split_vector.len();

        batch_insert(count, tx, split_vector);
    }
}

pub fn insert_wrapper(conn: &mut Connection, split: bool, vector_proto: Vec<Share>) {
    let tx = conn.transaction().unwrap();

    insert(&tx, split, &vector_proto);
    tx.commit().unwrap();
}

pub fn main(path: &str) -> Result<()> {
    env::set_var("RUST_BACKTRACE", "1");
    {
        // Create the all_shares_split table
        let path_ = path.clone();
        let conn = &mut Connection::open(path_).unwrap();
        let _ = conn.set_db_config(DbConfig::SQLITE_DBCONFIG_ENABLE_FKEY, true)?;

        conn.execute("CREATE TABLE IF NOT EXISTS all_shares_split (individual_share_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, transaction_id INT, security_id INTEGER NOT NULL,
            institution_id INTEGER NOT NULL, timestamp DATETIME, amount REAL NOT NULL, price_USD REAL NOT NULL, sold_price REAL, age_transaction INTEGER, long_counter TEXT, date_disposed DATETIME,
            FOREIGN KEY(institution_id) REFERENCES institutions(institution_id),
            FOREIGN KEY(security_id) REFERENCES securities(security_id),
            FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id)
            );", ())?;
    }

    {
        let path_ = path.clone();
        let conn = &mut Connection::open(path_).unwrap();
        let non_split_query: String = "SELECT transaction_id, security_id, institution_id, timestamp, amount, price_USD, sold_price, age_transaction, long_counter, date_disposed FROM all_shares WHERE long_counter = '-';".to_string();
        let non_split_arr = Share::get_all_shares(&conn, non_split_query).unwrap();
        insert_wrapper(conn, false, non_split_arr);
    }
    {
        let path_ = path.clone();
        let conn = &mut Connection::open(path_).unwrap();
        let split_query = "SELECT transaction_id, security_id, institution_id, timestamp, amount, price_USD, sold_price, age_transaction, long_counter, date_disposed FROM all_shares WHERE long_counter = '+';".to_string();
        let split_arr = Share::get_all_shares(&conn, split_query).unwrap();
        insert_wrapper(conn, true, split_arr);
    }

    {
        // Change the all_shares_split table to all_shares

        let path_ = path.clone();
        let conn = &mut Connection::open(path_).unwrap();
        conn.execute("DROP TABLE all_shares;", ())?;
        conn.execute("ALTER TABLE all_shares_split RENAME TO all_shares;", ())?;
    }

    let conn = &mut Connection::open(path).unwrap();
    let tx = conn.transaction()?;
    tx.commit()
}

/// TESTS

#[cfg(test)]
mod tests {
    use std::result;

    use super::*;
    #[test]
    fn inititate_db() {
        use rusqlite::config::DbConfig;
        use std::fs::File;
        use std::io::prelude::*;

        let conn = &mut Connection::open_in_memory().unwrap();
        let _ = conn.set_db_config(DbConfig::SQLITE_DBCONFIG_ENABLE_FKEY, true);

        let mut file = File::open("test/test_rs_db_query.sql").unwrap();
        let mut contents = String::new();
        file.read_to_string(&mut contents).unwrap();
        let split = contents.split(";");
        let vec: Vec<&str> = split.collect();
        for command in vec {
            conn.execute(command, []);
            conn.transaction().unwrap().commit();
        }

        {
            // test to see if the the insert of sql command worked
            let query = "SELECT transaction_id, security_id, institution_id, timestamp, amount, price_USD, sold_price, age_transaction, long_counter, date_disposed FROM all_shares WHERE long_counter = '-';".to_string();
            let number_of_shares = (Share::get_all_shares(conn, query)).unwrap().len();

            assert_eq!(number_of_shares, 1);
        }

        {
            // test to see if the splitting worked
            let query = "SELECT transaction_id, security_id, institution_id, timestamp, amount, price_USD, sold_price, age_transaction, long_counter, date_disposed FROM all_shares WHERE long_counter = '+';".to_string();
            let result_vec = Share::get_all_shares(conn, query).unwrap();
            insert_wrapper(conn, true, result_vec);

            let query = "SELECT transaction_id, security_id, institution_id, timestamp, amount, price_USD, sold_price, age_transaction, long_counter, date_disposed FROM all_shares_split;".to_string();
            let result_vec_new = Share::get_all_shares(conn, query).unwrap();
            assert_eq!(result_vec_new.len(), 15);
        }
    }
}
