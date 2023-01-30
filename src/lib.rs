use pyo3::prelude::*;

mod ext_db;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn insert_into_all_shares(path: String) -> PyResult<()> {
    ext_db::main(path).unwrap();
    Ok(())
}
/// A Python module implemented in Rust.
#[pymodule]
fn tolio(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(insert_into_all_shares, m)?)?;
    Ok(())
}