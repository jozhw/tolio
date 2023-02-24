use pyo3::prelude::*;

mod data_types;
mod db_methods {
    pub mod insert_csv;
    pub mod stock_split;
    pub mod bulk_insert_transactions;
}

mod dt_methods {
    pub mod rawtransaction;
    pub mod share;
    pub mod transaction;
}


/// Formats the sum of two numbers as string.
#[pyfunction]
fn split_update_all_shares(path: String) -> PyResult<()> {
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
    m.add_function(wrap_pyfunction!(split_update_all_shares, m)?)?;
    m.add_function(wrap_pyfunction!(insert_csv_to_db, m)?)?;
    Ok(())
    
}
