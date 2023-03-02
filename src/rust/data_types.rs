use rusqlite::{Connection, Statement};

pub struct PreparedStatement<'conn> {
    pub statement: Statement<'conn>,
}
impl<'conn> PreparedStatement<'conn> {
    pub fn new<'a>(conn: &'a Connection, sql: &str) -> PreparedStatement<'a> {
        PreparedStatement {
            statement: conn.prepare(sql).unwrap(),
        }
    }
}

// For inserting CSV Transaction
#[derive(Debug, serde::Deserialize)]
pub struct RawTransaction {
    pub security_name: String,
    pub security_ticker: String,
    pub institution_name: String,
    pub timestamp: Option<String>,
    pub transaction_abbreviation: String,
    pub amount: f32,
    pub price_usd: Option<f32>,
    pub transfer_from: Option<String>,
    pub transfer_to: Option<String>,
    pub age_transaction: i8,
    pub long: f32,
}
#[derive(Debug, Clone)]
pub struct EditedRawTransaction {
    pub security_id: i8,
    pub institution_id: i8,
    pub timestamp: Option<String>,
    pub transaction_abbreviation: String,
    pub amount: f32,
    pub price_usd: Option<f32>,
    pub transfer_from: Option<String>,
    pub transfer_to: Option<String>,
    pub age_transaction: i8,
    pub long: f32,
}

// For inserting into database transactions table
#[derive(Clone)]
pub struct Transaction {
    pub transaction_id: Option<i8>,
    pub security_id: i8,
    pub institution_id: i8,
    pub timestamp: String,
    pub transaction_abbreviation: String,
    pub amount: f32,
    pub price_usd: Option<f32>,
    pub transfer_from: Option<String>,
    pub transfer_to: Option<String>,
    pub age_transaction: i8,
    pub long: f32,
}

#[derive(Debug, Clone)]
pub struct Share {
    pub transaction_id: i8,
    pub security_id: i8,
    pub institution_id: i8,
    pub timestamp: String,
    pub amount: f32,
    pub price_usd: f32,
    pub sold_price: Option<f32>,
    pub age_transaction: i8,
    pub long_counter: String,
    pub date_disposed: Option<String>,
}

#[derive(Debug, Clone)]
pub struct UpdatedShare {
    pub individual_share_id: i8,
    pub transaction_id: i8,
    pub security_id: i8,
    pub institution_id: i8,
    pub timestamp: String,
    pub amount: f32,
    pub price_usd: f32,
    pub sold_price: Option<f32>,
    pub age_transaction: i8,
    pub long_counter: String,
    pub date_disposed: Option<String>,
}

#[derive(Debug, Clone)]
pub struct TransactionAge {
    pub transaction_id: i8,
    pub transaction_age: i8,
}

use pyo3::prelude::*;
#[derive(FromPyObject)]
pub enum Value {
    #[pyo3(transparent, annotation = "float")]
    Float(f32),
    #[pyo3(transparent, annotation = "str")]
    String(String),
}
