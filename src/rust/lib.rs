use std::collections::HashMap;
use data_types::Value;
use pyo3::prelude::*;
use pyo3::types::{PyDict};

mod data_types;

mod db_methods {
    pub mod bulk_insert_transactions;
    pub mod insert_csv;
    pub mod insert_into_transactions;
    pub mod stock_split;
}

mod dt_methods {
    pub mod rawtransaction;
    pub mod share;
    pub mod transaction;
}

#[pyfunction]
fn insert_acquire_or_dispose(path: &str, value_dic: &PyDict) -> PyResult<()> {
    let ex_value_dic:HashMap<String, Value> = value_dic.extract()?;
    db_methods::insert_into_transactions::insert_acquire_or_dispose(path, &ex_value_dic)
        .expect("Error: insert_acquire_or_dispose failed in lib.rs");
    Ok(())
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn stock_split(path: String) -> PyResult<()> {
    db_methods::stock_split::main(path).unwrap();
    Ok(())
}

#[pyfunction]
fn insert_csv_to_db(db_path: &str, path_to_csv: &str) -> PyResult<()> {
    db_methods::insert_csv::main(db_path, path_to_csv);
    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn tolio(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(stock_split, m)?)?;
    m.add_function(wrap_pyfunction!(insert_csv_to_db, m)?)?;
    m.add_function(wrap_pyfunction!(insert_acquire_or_dispose, m)?)?;
    Ok(())
}
