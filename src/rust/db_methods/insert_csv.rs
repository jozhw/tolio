use csv;
use std::error::Error;
use std::{collections::HashMap, os::raw};

use rusqlite::Connection;

use crate::{
    data_types::{EditedRawTransaction, RawTransaction, Transaction},
    db_methods::bulk_insert_transactions,
};

fn read_from_file(path: &str) -> Result<Vec<RawTransaction>, Box<dyn Error>> {
    let mut vector: Vec<RawTransaction> = Vec::new();
    let mut reader = csv::Reader::from_path(path)?;

    for result in reader.deserialize() {
        let transaction: RawTransaction = result?;
        vector.push(transaction);
        eprintln!("{:?}", vector);
    }

    Ok(vector)
}

fn csvtransaction_to_transaction(
    csvtransaction: Vec<RawTransaction>,
    db_path: &str,
) -> Result<Vec<EditedRawTransaction>, Box<dyn Error>> {
    // create hashmap of security_name, security_ticker, institution_name
    let mut available_ids: HashMap<String, i8> = HashMap::new();
    let mut transaction: Vec<EditedRawTransaction> = Vec::new();

    for item in csvtransaction {
        let raw_security_name = item.security_name.clone();
        let raw_security_id = available_ids.get(&raw_security_name).cloned();
        match raw_security_id {
            None => {
                let raw_security_id = item.get_security_id(db_path).unwrap();
                available_ids.insert(String::from(raw_security_name), raw_security_id);
            }
            _ => {}
        }

        let raw_institution_name = item.institution_name.clone();
        let raw_institution_id = available_ids.get(&raw_institution_name).cloned();
        match raw_institution_id {
            None => {
                let raw_institution_id = item.get_institution_id(db_path)?;
                available_ids.insert(String::from(raw_institution_name), raw_institution_id);
            }
            _ => {}
        }

        let raw_security_name = item.security_name.clone();
        let raw_institution_name = item.institution_name.clone();

        let security_id = available_ids.get(&raw_security_name).cloned().unwrap();
        let institution_id = available_ids.get(&raw_institution_name).cloned().unwrap();
        let timestamp = Some(item.timestamp.unwrap());
        let transaction_abbreviation = item.transaction_abbreviation;
        let amount = item.amount;
        let price_usd = item.price_usd;
        let transfer_from = item.transfer_from;
        let transfer_to = item.transfer_to;
        let age_transaction = item.age_transaction;
        let long = item.long;

        transaction.push(EditedRawTransaction {
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

    Ok(transaction)
}

pub fn main(db_path: &str, path_to_csv: &str) {
    let csvtransaction = read_from_file(path_to_csv)
        .expect("Error: Unable to convert csv file to intital rawtransaction.");
    let insert_bulk = csvtransaction_to_transaction(csvtransaction, db_path)
        .expect("Error: Unable to convert csv transaction to edited transaction.");
    bulk_insert_transactions::main(String::from(db_path), insert_bulk)
        .expect("Error: Failed to bulk insert transactions.");
    let all_transactions = Transaction::get_all_transactions(db_path)
        .expect("Error: Failed to get all transactions from database.");
    for transaction in all_transactions {
        transaction
            .insert_into_all_shares(db_path)
            .expect("Error: Failed to insert into all shares from transaction.")
    }

    /*
    This rust functionality does not contain the update_all_shares, update_institutions_held, update_securities,
    and update_stock_split.

    At the moment this application will use the python equivalents.
     */
}
