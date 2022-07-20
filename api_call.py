import folium, requests, datetime, time
import streamlit as st
# orginal coordinates from data.gov.sg is in x,y coordinates system.
# data is converted into lat and long from
# https://developers.onemap.sg/commonapi/convert/3857to4326?Y=146924.54200324757&X=11559656.16256661
# before storing to cp_dict
from cp_dict import cp_dict  


# ------------------ set time and connect api ------------------ #
global data
global now_modifed
# set to system current datetime and remove microsecond
now_dt = datetime.datetime.today().replace(microsecond=0)
# convert string to include T in the required api query parameter
now_str = str(now_dt)
# include T in current datetime as a required api query parameter
now_T = now_str.replace(' ', 'T')
# add 8 hours server due to timezone difference in streamlit
now_modifed = str(now_dt + datetime.timedelta(hours=8))

# api url
endpoint = "https://api.data.gov.sg/v1/transport/carpark-availability"
# query parameter
query_params = {'date_time': now_T}
# get data and convert to json
data = requests.get(endpoint, params=query_params).json()

    
