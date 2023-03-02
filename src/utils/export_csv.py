import sqlite3
import pandas as pd

def export_csv(db_path: str = "files/data/portfolio.db") -> None:
    conn = sqlite3.connect(db_path)

    # convert all of the null institution_ids to the institution_id for stock split
    # first must test to see if stock split is in the institutions table
    institution_id = conn.execute("SELECT institution_id FROM institutions WHERE institution_name = ?;", ("Stock Split",)).fetchone()
    if bool(institution_id) == False:
        conn.execute("INSERT INTO institutions (institution_name) VALUES ('Stock Split');", )
        institution_id = conn.execute("SELECT institution_id FROM institutions WHERE institution_name = ?", ("Stock Split",)).fetchone()
        conn.commit()
    
    conn.execute("UPDATE transactions SET institution_id =? WHERE institution_id IS NULL;", (institution_id[0],))
    conn.commit()
    

    sql_query = """
    SELECT s.security_name, s.security_ticker, i.institution_name, t.timestamp, t.transaction_abbreviation, t.amount, t.price_USD,
    t.transfer_from, t.transfer_to, t.age_transaction, t.long
    FROM institutions as i INNER JOIN transactions AS t on i.institution_id=t.institution_id INNER JOIN 
    securities AS s USING(security_id)
    """

    df = pd.read_sql(sql_query, conn)
    df.rename({"price_USD":"price_usd"}, axis = 1, inplace = True)
    df.to_csv("transactions_data.csv", index = False)




  


