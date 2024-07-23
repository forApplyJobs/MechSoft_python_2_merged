#SQL Alchemy==2.0.20
#pandas==2.0.3
#pyodbc==4.0.39


from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pandas as pd


class ConnectionHander:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        
        #driver = "SQL Server"
        driver = "ODBC Driver 17 for SQL Server"
        
        connection_string = f'DRIVER={driver};SERVER={self.host};PORT=1433;DATABASE={self.db};UID={self.user};PWD={self.password};&autocommit=true'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        self.engine = create_engine(connection_url, use_setinputsizes = False, echo = False)
        
        self.db_connection = self.engine.connect()
        
    def fetch_data(self, query):
        return pd.read_sql(query, con=self.db_connection)
    
    def insert_data(self, df, tablename):
        df.to_sql(tablename, if_exists = 'append', index = False, con = self.db_connection)
    
    def execute_query(self, query):
        self.db_connection.execute(query)
        
    def __del__(self):
        try:
            self.db_connection.close()
        except:
            None
    
CH = ConnectionHander('DESKTOP-MS8F2DP', 'eurocommerce', 'eurocommerce', 'DbOtopark')
query = 'select * from cars'

df = CH.fetch_data(query)

print(df)
