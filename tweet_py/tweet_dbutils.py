"""
filename: dbutils.py
Requires the driver:  conda install mysql-connector-python

description: A collection of database utilities to make it easier
to implement a database application
"""

import pandas as pd
import pymysql


class DBUtils:
    def __init__(self, user, password, database, host="localhost"):
        """Future work: Implement connection pooling"""
        self.con = pymysql.connect(
            host=host, user=user, password=password, database=database
        )

    def close(self):
        """Close or release a connection back to the connection pool"""
        self.con.close()  # type: ignore
        self.con = None

    def execute(self, query):
        """Execute a select query and returns the result as a dataframe"""

        # Step 1: Create cursor
        rs = self.con.cursor()  # type: ignore

        # Step 2: Execute the query
        rs.execute(query)

        # Step 3: Get the resulting rows and column names
        rows = rs.fetchall()
        cols = [desc[0] for desc in rs.description]

        # Step 4: Close the cursor
        rs.close()

        # Step 5: Return result
        return pd.DataFrame(rows, columns=cols)

    def insert_one(self, sql: str, val: tuple):
        """
        Insert a single row into a database table.

        Args:
        sql (str): The SQL query to be executed. It should be an INSERT statement.
        val (tuple): A tuple containing the values to be inserted.

        """
        cursor = self.con.cursor()  # type: ignore
        cursor.execute(sql, val)
        self.con.commit()  # type: ignore

    def insert_many(self, sql: str, vals: list):
        """
        Insert multiple rows into a database table.

        Args:
        sql (str): The SQL query to be executed. It should be an INSERT statement.
        vals (list): A list of tuples, where each tuple contains the values to be inserted in a row.

        """
        cursor = self.con.cursor()  # type: ignore
        cursor.executemany(sql, vals)
        self.con.commit()  # type: ignore

    def create_indices(self, column, table):
        """
        This method creates an index on the specified column of the specified table if it does not already exist.
        """
        # check if the index exists
        sql = f"SHOW INDEX FROM {table} WHERE Key_name = '{column}_index'"
        index_exists = self.execute(sql)

        # if the index does not exist, create it
        if index_exists.empty:
            sql = f"CREATE INDEX {column}_index ON {table} ({column})"
            self.execute(sql)
