import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlite3

import os
import pandas as pd

from typing import Optional

class Database:
    def __init__(self, db_name='M3_SQL.db'):
        self.db_name = db_name
        self.working_dir = os.path.join(os.getcwd().split('Datacademy')[0], "Datacademy", "Modules", "M3_SQL", "src")
        self.data_dir = os.path.join(os.getcwd().split('Datacademy')[0], "Datacademy", "data", "M3_SQL")
        self.database_location = os.path.join(self.working_dir, self.db_name) 
        self.SQLALCHEMY_DATABASE_URL = f"sqlite:///{self.database_location}"

        self.create_database()
        self.data_dtypes = {
            'customers': {'Id':int, 'firstName':str, 'lastName':str, 'address':str},
            'orders': {'Id':int, 'customerId':int, 'productId':int, 'date':str, 'quantity':int},
            'products': {'Id':int, 'name':str, 'price':float, 'stock':int}
        }
        self.insert_queries = {
            'customers': ''' INSERT INTO customers(id, firstName, lastName, address) VALUES(?, ?, ?, ?) ''',
            'orders': ''' INSERT INTO orders(id, customerId, productId, date, quantity) VALUES(?, ?, ?, ?, ?) ''',
            'products': ''' INSERT INTO products(id, name, price, stock) VALUES(?, ?, ?, ?) '''
        }
        self.populate_database()
    
    def setup_environment(self) -> None:
        """
        Create the database engine and the declarative base.
        """
        # If the database file already exists, delete file
        if os.path.exists(os.path.join(os.getcwd(), self.db_name)):
            os.remove(os.path.join(os.getcwd(), self.db_name))

        self.engine = _sql.create_engine(
            self.SQLALCHEMY_DATABASE_URL, 
            connect_args={"check_same_thread": False})

        self.Base = _declarative.declarative_base()
    
    def initiate_tables(self) -> None:
        """
        Initiate tables that comprise the database.
        """
        class Customers(self.Base):
            __tablename__ = "customers"
            id = _sql.Column(_sql.Integer, primary_key=True, index=True)
            firstName = _sql.Column(_sql.String, index=True)
            lastName = _sql.Column(_sql.String, index=True)
            address = _sql.Column(_sql.String, index=True)

        class Orders(self.Base):
            __tablename__ = "orders"
            id = _sql.Column(_sql.Integer, primary_key=True, index=True)
            customerId = _sql.Column(_sql.Integer, _sql.ForeignKey("customers.id"), index=True)
            productId = _sql.Column(_sql.Integer, _sql.ForeignKey("products.id"), index=True)
            date = _sql.Column(_sql.Date, index=True)
            quantity = _sql.Column(_sql.Integer, index=True)

        class Products(self.Base):
            __tablename__ = "products"
            id = _sql.Column(_sql.Integer, primary_key=True, index=True)
            name = _sql.Column(_sql.String, index=True)
            price = _sql.Column(_sql.Float, index=True)
            stock = _sql.Column(_sql.Integer, index=True)

    def create_database(self) -> None:
        """ 
        Initiate the database, creating its environment and the tables it is comprised of.
        """
        self.setup_environment()
        self.initiate_tables()
        self.Base.metadata.create_all(bind=self.engine)
    
    def populate_database(self) -> None:
        """
        Upload data from CSV files onto the created database using the insert queries.
        """
        # Establish database connection
        conn = sqlite3.connect(self.database_location)
        cur = conn.cursor()

        # For all data files in the directory
        fileNames = [f for f in os.listdir(self.data_dir) if ".csv" in f]
        for file in fileNames:
            df = pd.read_csv(os.path.join(self.data_dir, file), delimiter=';')

            # Ensure the correct data types of the dataframes
            for col, col_type in self.data_dtypes[file.split('.')[0]].items():
                df[col] = df[col].astype(col_type)

            # Insert and commit the data to the database
            for _, data in df.iterrows():
                cur.execute(self.insert_queries[file.split('.')[0]], data)
            conn.commit()
        
        # Close database connection
        conn.close()
        
    def execute_query(self, query:str, exercise: Optional[str]=None, return_df:bool=False, print_string:str="", save_output:bool=True) -> list or pd.DataFrame:
        """
        Establish database connection, execute query and close database connection.

        Args:
            query (pd.DataFrame): Query to be executed.
            return_df (bool): If True, output will be in a pandas dataframe.

        Returns:
            list: Query results.
            pd.DataFrame: If requested, the results will be transformed into a pandas DataFrame.
        """
        conn = sqlite3.connect(f'{os.getcwd()}/{self.db_name}')
    
        cursor = conn.execute(query)
        data = cursor.fetchall()

        if return_df:
            cols = list(map(lambda x: x[0], cursor.description))
            data = pd.DataFrame(data, columns=cols)
            try:
                data.set_index('id', inplace=True)
            except KeyError:
                pass

        conn.commit()
        conn.close()

        if len(print_string) > 0:
            return f"{print_string} {data[0][0]}"

        CRUD_Indicator = query[:6]
        if CRUD_Indicator == "CREATE":
            return "Table created successfully!"
        elif CRUD_Indicator == "INSERT":
            return "Data inserted successfully!"
        elif CRUD_Indicator == "UPDATE":
            return "Data record updated successfully!"
        elif CRUD_Indicator == "DELETE":
            return "Data record deleted successfully!"
        elif CRUD_Indicator[:4] == "DROP":
            return "Table dropped successfully!"
        else:
            if save_output:
                if not os.path.exists(os.path.join(self.data_dir, "answers")):
                    os.mkdir(os.path.join(self.data_dir, "answers"))
                if exercise is None:
                    return "Please provide the exercise name in the function if you want to save the outputs."
                data.to_csv(os.path.join(self.data_dir, "answers", f"{exercise}.csv"), sep=";", index=False)
            return data

    def retrieve_tables(self) -> list:
        """
        Return the names of the names of the different tables comprising the database.

        Returns:
            list: List of table names.
        """
        return self.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
