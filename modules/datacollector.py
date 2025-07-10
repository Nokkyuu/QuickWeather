import requests
import logging #TODO: add logging
import datetime

class DataCollector:
    """Class to collect weather data from OpenWeatherMap API."""

    def __init__(self, api_key: str | None, lang: str = "de"):
        self.api_key = api_key
        self.lang = lang

    def get_weather_information(self, searchtype:str, **kwargs) -> dict: #type: ignore
        """main function to get weather information from OpenWeatherMap API

        Args:
            searchtype (str): either "name" for city name search or "geo" for geographical coordinates search
            **kwargs: _description_
                name (str): city name for name search
                country (str): country code, default is "de"
                lat (float): latitude for geo search
                lon (float): longitude for geo search
                
        Returns:
            dict : API resonse data in JSON format
        """
        country = kwargs.get("country", "de")
        lat = kwargs.get("lat", None)
        lon = kwargs.get("lon", None)
        name = kwargs.get("name", None)

        if searchtype not in ["name", "geo"]:
            raise ValueError("searchtype must be 'name' or 'geo'")
        else:
            if searchtype == "name":
                url = f"https://api.openweathermap.org/data/2.5/weather?q={name},{country}&appid={self.api_key}&units=metric&lang={self.lang}"  
                data = requests.get(url).json()
                return data
            elif searchtype == "geo":
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric&lang={self.lang}"
                data = requests.get(url).json()
                return data
    
    def get_description(self, data) -> str:
        """function to get weather description from API response

        Args:
            data (_type_): response data from API collected with get_city_information

        Returns:
            str: weather description from API response
        """
        try:
            return data['weather'][0]['description']
        except KeyError:
            return "No description available"
        
    def get_temperature(self, data) -> dict:
        """gets current, min and max temperature from API response

        Args:
            data (_type_): response data from API collected with get_city_information

        Returns:
            tuple: current temp, feels_like temp, min temp, max temp
            If no temperature data is available, returns (0, 0, 0)
        """
        try:
            return {"current" : data['main']['temp'], "feels_like" : data['main']['feels_like'], "min" : data['main']['temp_min'], "max" : data['main']['temp_max']}
        except KeyError:
            return {"current" : 0, "feels_like" : 0, "min" : 0, "max" : 0}

    def get_coordinates(self, data) -> dict:
        """function to get coordinates from API response

        Args:
            data (dict): response data from API collected with get_city_information

        Returns:
            dict: dictionary with latitude and longitude
        """
        try:
            return data['coord']
        except KeyError:
            return {"lat": 0, "lon": 0}
        
    def get_windspeed(self, data) -> float:
        """function to get wind speed from API response

        Args:
            data (_type_): response data from API collected with get_city_information

        Returns:
            float: wind speed in m/s
        """
        try:
            return data['wind']['speed']
        except KeyError:
            return 0.0

    def get_time(self, data) -> dict:
        """function to get time information in the local time from API response

        Args:
            data (_type_): response data from API collected with get_city_information

        Returns:
            dict: dictionary with current time, sunrise and sunset times
        """
        tz = data.get('timezone', 0) #shift in seconds, default is 0
        try:
            return {
                "current": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=tz)).strftime("%H:%M"),
                "sunrise": (datetime.datetime.fromtimestamp(data['sys']['sunrise'], datetime.timezone.utc)+ datetime.timedelta(seconds=tz)).strftime("%H:%M"),
                "sunset": (datetime.datetime.fromtimestamp(data['sys']['sunset'], datetime.timezone.utc)+ datetime.timedelta(seconds=tz)).strftime("%H:%M")
            }
        except KeyError:
            return {"current": "00:00", "sunrise": "00:00", "sunset": "00:00"}
  
    def get_city_information(self, data) -> dict:
        """function to get city information from API response
        Args:
            data (_type_): response data from API collected with get_city_information
        Returns:
            tuple: city name and country code
        """
        try:
            return {"city_name" : data["name"], "country_short" : data["sys"]["country"]}
        except KeyError:
            return {"city_name": "Unknown", "country_short": "Unknown"}

    def get_search_entry(self, data) -> dict:
        """function to get all relevant information from API response

        Args:
            data (_type_): response data from API collected with get_city_information

        Returns:
            dict: dictionary with all relevant information
            description: weather description
            temperature: current, feels_like, min and max temperature
            coordinates: latitude and longitude
            windspeed: wind speed in m/s
            time: current time, sunrise and sunset times in the local time
            city_information: city name and country code
        """
        search_entry = {
            "description": self.get_description(data),
            "temperature": self.get_temperature(data),
            "coordinates": self.get_coordinates(data),
            "windspeed": self.get_windspeed(data),
            "time": self.get_time(data),
            "city_information": self.get_city_information(data)
        }

        return search_entry
  

if __name__ == "__main__":
    pass