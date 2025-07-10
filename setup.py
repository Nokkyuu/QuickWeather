import os
import sqlite3
import logging #TODO: add logging




def connect_db(db_path: str):
    """connect to the SQLite database and load the search_result table into a pandas DataFrame.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return cursor, conn

def initiate_database(cursor, conn, db_path, override: bool = False):
        
        """innitiates the SQLite database with city and weather tables.
        If `override` is True, it will remove the existing database file and recreate it.

        Args:
            override (bool, optional): delete and recreate the db file. Defaults to False.
        """
        
        if override and os.path.exists(db_path):
            os.remove(db_path)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            print(f"Database '{db_path}' removed and recreated.")
            
        sql='''
            CREATE TABLE IF NOT EXISTS search_result (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cityname TEXT,
                country_code TEXT,
                lat REAL,
                lon REAL,
                description TEXT,
                temperature REAL,
                feels_like REAL,
                min_temp REAL,
                max_temp REAL,
                wind_speed REAL,
                local_time TEXT,
                sunrise TEXT,
                sunset TEXT
            )
        '''
        
        cursor.execute(sql)
        conn.commit()
        conn.close()

        print(f"Database '{db_path}' initiated successfully.")

if __name__ == "__main__":
    db_path = "db/search_results.db"
    cursor, conn = connect_db(db_path)
    initiate_database(cursor, conn, db_path, override=True)