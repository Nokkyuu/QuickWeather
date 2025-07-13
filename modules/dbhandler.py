import sqlite3
import logging #
import pandas as pd
from datetime import datetime

logger = logging.getLogger()
class DataBaseHandler:
    """Class for handling SQLite database operations for weather data.
    This class provides methods to add cities, retrieve city IDs,
    add weather data, and retrieve weather data for specific cities.
    It also includes methods to initiate the database and create necessary tables.
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        logger.debug(f"Initializing DataBaseHandler with db_path: {self.db_path}")
        
    def get_search_entries(self):
        """Retrieves all entries from the search_result table and returns a dataframe."""
        df = pd.read_sql("SELECT * FROM search_result", self.conn, index_col='ID')
        logger.debug("Retrieved search entries from the database.")
        return df 
    
    def load_search_history(self):
        """connect to the SQLite database and load the search_result table into a pandas DataFrame.
        """
        try:
            sql = "SELECT * FROM search_result"
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.df = self.get_search_entries() #in memory data handling with pandas DataFrame to avoid rendundant sql queries.
            logger.info("Search history loaded successfully.")
        except sqlite3.OperationalError as e:
            logger.error(f"Database error: {e}")
        
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")


    def close_connection(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            logger.debug("Database connection closed.")
            
    def add_search_entry(self, search_entry: dict):
        """add a new entry to the search_result table in the database.

        Args:
            takes a dictionary of a search entry created by the DataCollector class.
        """
        timestamp = datetime.now()
        try:
            city_name = search_entry["city_information"]["city_name"]
            country_code = search_entry["city_information"]["country_short"]
            lat = search_entry["coordinates"]["lat"]
            lon = search_entry["coordinates"]["lon"]
            description = search_entry["description"]
            temperature = search_entry["temperature"]["current"]
            feels_like = search_entry["temperature"]["feels_like"]
            min_temp = search_entry["temperature"]["min"]
            max_temp = search_entry["temperature"]["max"]
            wind_speed = search_entry["windspeed"]
            local_time = search_entry["time"]["current"]
            sunrise = search_entry["time"]["sunrise"]
            sunset = search_entry["time"]["sunset"]
            logger.debug(f"Adding search entry for {city_name}, {country_code} at {timestamp}.")
        except KeyError as e:
            logger.error(f"Missing key in search entry: {e}")     
        else:
            sql = """INSERT INTO search_result 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            
            data = (None, timestamp ,city_name, country_code, lat, lon, description, temperature, feels_like, min_temp, max_temp, wind_speed, local_time, sunrise, sunset)
            self.cursor.execute(sql, data)
            self.conn.commit()
            logger.info(f"Search entry for {city_name}, {country_code} added successfully.")

            new_row = {
                "timestamp": timestamp,
                "cityname": city_name,
                "country_code": country_code,
                "lat": lat,
                "lon": lon,
                "description": description,
                "temperature": temperature,
                "feels_like": feels_like,
                "min_temp": min_temp,
                "max_temp": max_temp,
                "wind_speed": wind_speed,
                "local_time": local_time,
                "sunrise": sunrise,
                "sunset": sunset
            }
            #to keep in memory data (self.df) synchronized with database during runtime
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
            logger.debug("New search entry added to the in-memory DataFrame.") 
    
    def get_last_search_entry(self):
        """Retrieves the last entry from the search_result table as a dataframe."""
        df = pd.read_sql("SELECT * FROM search_result ORDER BY ID DESC LIMIT 1", self.conn)
        logger.debug("Retrieved the last search entry from the database.")
        return df

    

if __name__ == "__main__":
    db_handler = DataBaseHandler(db_path="db/search_results.db")

