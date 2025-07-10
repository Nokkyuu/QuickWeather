import os 
from pathlib import Path 
from dotenv import load_dotenv
from modules import DataBaseHandler, DataCollector
import streamlit as st
import pandas as pd
import plotly.express as px
import logging #TODO: add logging


os.chdir(Path(__file__).parent)
load_dotenv(override=True)


API_KEY = os.getenv('WEATHER_APIKEY')
DB_PATH = "db/search_results.db"



def main():
    db_handler = DataBaseHandler(db_path=DB_PATH)
    db_handler.load_search_history()    
    collector = DataCollector(api_key=API_KEY, lang="en")
    search_entry = None

    st.title("🌦️ QuickWeather")
    st.subheader("Local Time and Weather information")
    
    
    with st.sidebar:
        search_mode = st.radio("Searchmode:", ["city name and country code", "geolocation"])
        if search_mode == "city name and country code":
            city = st.text_input("city name", "Hildesheim")
            country = st.text_input("country code", "de")
            if st.button("Quick Info"):
                search_entry = collector.get_search_entry(collector.get_weather_information(searchtype="name", name=city, country=country))
                db_handler.add_search_entry(search_entry=search_entry)
        elif search_mode == "geolocation":
            lat = st.number_input("Latitude", format="%.4f")
            lon = st.number_input("Longitude", format="%.4f")
            if st.button("Quick Info"):
                search_entry = collector.get_search_entry(collector.get_weather_information(searchtype="geo", lat=lat, lon=lon))
                db_handler.add_search_entry(search_entry=search_entry)

    # Showresults
    if search_entry:
        city_name = search_entry['city_information']['city_name']
        country_code = search_entry['city_information']['country_short']
        lat = search_entry['coordinates']['lat']
        lon = search_entry['coordinates']['lon']
        temp = search_entry['temperature']['current']
        feels_like = search_entry['temperature']['feels_like']
        min_temp = search_entry['temperature']['min']
        max_temp = search_entry['temperature']['max']
        wind_speed = search_entry['windspeed']
        local_time = search_entry['time']['current']
        sunrise = search_entry['time']['sunrise']
        sunset = search_entry['time']['sunset']
        desc = search_entry['description']

        

        col1, col2 = st.columns(2, vertical_alignment="center")

        with col1:
            fig = px.scatter_mapbox(
                db_handler.get_last_search_entry(),
                lat="lat", lon="lon", hover_name="cityname", hover_data=["temperature"],
                zoom=10, height=300
            )
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(f"""
            | City                 | {city_name}, {country_code}|
            |----------------------|----------------------|
            | Description          | {desc}               |
            | Lat/Lon             | {lat}, {lon}.         |
            | Temperature (°C)     | {temp}               |
            | Feels Like (°C)      | {feels_like}         |
            | Min/Max temp (°C) | {min_temp}, {max_temp}|
            | Wind Speed (m/s)     | {wind_speed}         |
            | Local Time           | {local_time}         |
            | Sunrise              | {sunrise}            |
            | Sunset               | {sunset}             |
            
            """)

    else:
        st.info("Please enter a city name and country code or geolocation to get local information.")
    
    st.subheader("Search History")
    st.dataframe(db_handler.df.iloc[::-1], use_container_width=True)
    


if __name__ == "__main__":
    main()
   