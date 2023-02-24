use std::error::Error;

use rusqlite::{named_params, Connection};

use crate::data_types::{PreparedStatement, Share, UpdatedShare};

impl Share {
    pub fn get_all_shares(conn: &Connection, query: String) -> Result<Vec<Share>, Box<dyn Error>> {
        let mut non_split_list = conn.prepare(&query)?;

        let share_iter = non_split_list.query_map([], |row| {
            let transaction_id: i8 = row.get(0)?;
            let security_id: i8 = row.get(1)?;
            let institution_id: i8 = row.get(2)?;
            let timestamp: String = row.get(3)?;
            let amount: f32 = row.get(4)?;
            let price_usd: f32 = row.get(5)?;
            let sold_price: Option<f32> = row.get(6)?;
            let age_transaction: i8 = row.get(7)?;
            let long_counter: String = row.get(8)?;
            let date_disposed: Option<String> = row.get(9)?;

            Ok(Share {
                transaction_id,
                security_id,
                institution_id,
                timestamp,
                amount,
                price_usd,
                sold_price,
                age_transaction,
                long_counter,
                date_disposed,
            })
        })?;

        let mut security = Vec::new();
        for share in share_iter {
            security.push(share?);
        }
        Ok(security)
    }
}

impl UpdatedShare {
    pub fn update_share(&self, db_path: &str) -> Result<(), Box<dyn Error>> {
        let conn = Connection::open(db_path)?;

        let sql = "UPDATE TABLE all_shares SET 
        transaction_id = :transaction_id,
        security_id = :security_id,
        institution_id = :institution_id,
        timestamp = :timestamp,
        amount = :amount,
        price_USD = :price_usd,
        sold_price = :sold_price,
        age_transaction = :age_transaction,
        long_counter = :long_counter,
        date_disposed = :date_disposed
        WHERE individual_share_id = :individual_share_id;";

        let mut prepared_sql = PreparedStatement::new(&conn, &sql);

        prepared_sql.statement.execute(named_params! {
            ":transaction_id": self.transaction_id,
            ":security_id": self.security_id,
            ":institution_id": self.institution_id,
            ":timestamp": self.timestamp,
            ":amount": self.amount,
            ":price_usd": self.price_usd,
            ":sold_price": self.sold_price,
            ":age_transaction": self.age_transaction,
            ":long_counter": self.long_counter,
            ":date_disposed": self.date_disposed,
            ":individual_share_id": self.individual_share_id
        })?;

        Ok(())
    }
}
