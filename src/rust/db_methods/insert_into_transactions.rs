use either::*;
use std::collections::HashMap;
use std::error::Error;

use crate::data_types::{RawTransaction, Transaction, Value};

impl Value {
    pub fn unwrap(&self) -> Either<f32, String> {
        match self {
            Value::Float(f32) => {
                let value: f32 = *f32;
                Left(value)
            }
            Value::String(string) => Right(String::from(string)),
        }
    }
}

pub fn insert_acquire_or_dispose(
    db_path: &str,
    value_dic: &HashMap<String, Value>,
) -> Result<(), Box<dyn Error>> {
    let security_name = value_dic
        .get("security_name")
        .expect("Error: Security name is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let security_ticker = value_dic
        .get("security_ticker")
        .expect("Error: Security ticker is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let institution_name = value_dic
        .get("institution_name")
        .expect("Error: Institution name is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let timestamp = value_dic
        .get("timestamp")
        .expect("Error: Timestamp is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let transaction_abbreviation = value_dic
        .get("transaction_abbreviation")
        .expect("Error: Transaction abbreviation is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let amount = value_dic
        .get("amount")
        .expect("Error: Amount is null")
        .clone()
        .unwrap()
        .unwrap_left();
    let price_usd = value_dic
        .get("price_USD")
        .expect("Error: Price is null.")
        .clone()
        .unwrap()
        .unwrap_left();

    let to_insert = RawTransaction::new_acquire_or_dispose(
        security_name,
        security_ticker,
        institution_name,
        timestamp,
        transaction_abbreviation,
        amount,
        price_usd,
    )?;

    to_insert.insert_into_transactions(db_path)?;

    // get the inserted transaction and insert into the all_shares table
    let recent_transaction: Transaction = Transaction::get_recent_transaction(db_path).unwrap();
    recent_transaction.insert_into_all_shares(db_path)?;

    Ok(())
}

pub fn insert_transfer(
    db_path: &str,
    value_dic: &HashMap<String, Value>,
) -> Result<(), Box<dyn Error>> {
    let security_name = value_dic
        .get("security_name")
        .expect("Error: Security name is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let security_ticker = value_dic
        .get("security_ticker")
        .expect("Error: Security ticker is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let institution_name = value_dic
        .get("institution_name")
        .expect("Error: Institution name is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let from_institution_name = Some(institution_name.clone());
    let timestamp = Some(
        value_dic
            .get("timestamp")
            .expect("Error: Timestamp is null.")
            .clone()
            .unwrap()
            .unwrap_right(),
    );
    let transaction_abbreviation = value_dic
        .get("transaction_abbreviation")
        .expect("Error: Transaction abbreviation is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let amount = value_dic
        .get("amount")
        .expect("Error: Amount is null")
        .clone()
        .unwrap()
        .unwrap_left();
    let to_institution_name: Option<String> = Some(
        value_dic
            .get("to_institution_name")
            .expect("Error: Price is null.")
            .clone()
            .unwrap()
            .unwrap_right(),
    );

    let to_insert = RawTransaction {
        security_name: { security_name },
        security_ticker: { security_ticker },
        institution_name: { institution_name },
        timestamp: { timestamp },
        transaction_abbreviation: { transaction_abbreviation },
        amount: { amount },
        age_transaction: { 0 },
        long: { 0.0 },
        price_usd: { None },
        transfer_from: { from_institution_name },
        transfer_to: { to_institution_name },
    };

    to_insert.insert_into_transactions(db_path)?;
    let recent_transaction: Transaction = Transaction::get_recent_transaction(db_path).unwrap();
    recent_transaction.insert_into_all_shares(db_path)?;

    Ok(())
}

pub fn insert_stock_split(
    db_path: &str,
    value_dic: &HashMap<String, Value>,
) -> Result<(), Box<dyn Error>> {
    let security_name = value_dic
        .get("security_name")
        .expect("Error: Security name is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let security_ticker = value_dic
        .get("security_ticker")
        .expect("Error: Security ticker is null.")
        .clone()
        .unwrap()
        .unwrap_right();

    let timestamp = Some(
        value_dic
            .get("timestamp")
            .expect("Error: Timestamp is null.")
            .clone()
            .unwrap()
            .unwrap_right(),
    );
    let transaction_abbreviation = value_dic
        .get("transaction_abbreviation")
        .expect("Error: Transaction abbreviation is null.")
        .clone()
        .unwrap()
        .unwrap_right();
    let amount = value_dic
        .get("amount")
        .expect("Error: Amount is null")
        .clone()
        .unwrap()
        .unwrap_left();
    let institution_name = String::from("Stock Split");

    let to_insert = RawTransaction {
        security_name: { security_name },
        security_ticker: { security_ticker },
        institution_name: { institution_name },
        timestamp: { timestamp },
        transaction_abbreviation: { transaction_abbreviation },
        amount: { amount },
        age_transaction: { 0 },
        long: { 0.0 },
        price_usd: { None },
        transfer_from: { None },
        transfer_to: { None },
    };

    to_insert.insert_into_transactions(db_path)?;
    let recent_transaction: Transaction = Transaction::get_recent_transaction(db_path).unwrap();
    recent_transaction.split_all_shares(db_path)?;
    recent_transaction.insert_into_all_shares(db_path)?;

    Ok(())
}
