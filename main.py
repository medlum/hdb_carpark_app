import folium
import streamlit_folium
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import requests, datetime, time, json
from cp_dict import cp_dict
from folium.features import DivIcon
from utils import *

# ------------------------- lta api call ----------------------------#
url = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"
#headers = {"AccountKey": " ",
#           "accept": "application/json"}
headers = {"AccountKey": st.secrets["LTA_APIKEY"],
           "accept": "application/json"}
response = requests.request(method="get", url=url, headers=headers)
lta_data = response.json()
# ------------------------- data.gov.sg api call ----------------------------#

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


# ------------------------- data process malls ----------------------------#
malls = []
for item in lta_data["value"]:
    if item["Area"] != "":
        malls.append([item["Development"], float(item["Location"].split(" ")[
                     0]), float(item["Location"].split(" ")[1]), item["AvailableLots"]])

mall_names = [mall[0] for mall in malls]

# ------------------------- data process hdb ----------------------------#
cp_code = []
total_lots = []
avail_lots = []
complete_list = []
# data variable is from api_call
for item in data["items"]:
    for detail in item["carpark_data"]:
        # extract carpark_code, total lots and available lots
        cp_code.append(detail['carpark_number'])
        total_lots.append(detail["carpark_info"][0]["total_lots"])
        avail_lots.append(detail["carpark_info"][0]["lots_available"])

# removed first element as it is not useful
total_lots = total_lots[1:]
avail_lots = avail_lots[1:]

# combined details in cp_dict with the extracted data from api
for index in range(len(cp_code) - 1):
    if cp_code[index] in cp_dict:
        complete_list.append([index,
                              cp_code[index],
                              cp_dict[cp_code[index]][0],
                              cp_dict[cp_code[index]][1],
                              float(cp_dict[cp_code[index]][2]),
                              float(cp_dict[cp_code[index]][3]),
                              cp_dict[cp_code[index]][4],
                              cp_dict[cp_code[index]][5],
                              cp_dict[cp_code[index]][6],
                              cp_dict[cp_code[index]][7],
                              total_lots[index],
                              avail_lots[index]])

location = sorted(list(set([address[2] for address in complete_list])))

# ---------------- create icon -----------------------#


def hdb_DivIcon(hdb_selected, total, available):
    icon = DivIcon(
        icon_size=(250, 250),
        icon_anchor=(120,35),
        html=f'<p style= "font-size: 10pt; color : DarkSlateGray; text-align: center"> {hdb_selected} <br> <br> <br> Total {total} <br> Available {available}</strong></p>'
    )
    return icon


def mall_DivIcon(mall_selected, lots_avail):
    icon = DivIcon(
        icon_size=(180, 180),
        icon_anchor=(100, 35),
        html=f'<p style="font-size: 10pt; color : DarkSlateGray; text-align: center"> <strong> {mall_selected} <br> <br> <br> Available: {lots_avail}</strong></p>'
    )
    return icon


# ------------------------- map and stream ----------------------------#
st.set_page_config(
    page_title='Bus ',
    page_icon=':shark:',
    layout="wide",
    menu_items={"About": "Data is updated on one minute interval"}
)
set_bg("wallpaper3.jpg")
head()
st.write(
    f"<p style='text-align: left; color:GreenYellow'> Current Date Time: {now_modifed}</p>", unsafe_allow_html=True)

#st.set_page_config(page_title="hello", page_icon=":shark:", layout="wide")
#st.title("Carpark Availability in Real-Time")
#st.text("data source: data.gov.sg and datamall.lta.gov.sg")
#st.text("[V1.0] Andy Oh | School of Business & Acccountancy | Ngee Ann Polytechnic".upper())
#st.header(f"Current Date Time | {now_modifed}")

#st.sidebar.subheader(f"{now_modifed}")
with st.expander("HDB"):
    filter_hdb = st.multiselect("You may select more than one", location)
    

with st.expander("Shopping Mall"):
    filter_malls = st.multiselect("You may select more than one", mall_names)


m = folium.Map(location=[1.3521, 103.8198],
            min_zoom=11,
            max_zoom=18,
            zoom_start=12,
            max_bounds=True,
            tiles="CartoDB positron",
            name="Light Map")


if len(filter_malls) != 0:

    for index in range(len(malls)):
        if malls[index][0] not in filter_malls:
            pass
        else:
            mall_selected = malls[index][0]
            lots_avail = malls[index][3]
            lat = malls[index][1]
            long = malls[index][2]
        
            custom_icon = folium.CustomIcon(icon_image='mall_icon.png', icon_size=(30, 30))
            folium.Marker(location=[lat, long], icon=custom_icon).add_to(m)
            #tooltip = (f"{mall_selected} <br> Available Lots: {lots_avail}"),
            folium.Marker(location=[lat, long],
                          icon=mall_DivIcon(mall_selected, lots_avail)).add_to(m)

            st.metric(label=mall_selected, value=lots_avail)

if len(filter_hdb) != 0:

    for index in range(len(complete_list)):
        if complete_list[index][2] not in filter_hdb:
            pass
        else:
            total = complete_list[index][10]
            avail = complete_list[index][11]
            type = complete_list[index][6]
            short = complete_list[index][7]
            free = complete_list[index][8]
            night = complete_list[index][9]
            lat = complete_list[index][4]
            long = complete_list[index][5]
            hdb_selected = complete_list[index][3]

            custom_icon = folium.CustomIcon(icon_image='carpark_logo.jpg', icon_size=(20, 20))       
            #poopup = folium.Popup(f"CARPARK TYPE:{type} <br> SHORT TERM PARKING: {short} <br> FREE PARKING: {free} <br> NIGHT PARKING: {night}",
            #                    min_width=300, max_width=300)
            
            folium.Marker(location=[lat, long], tooltip= folium.Tooltip(f"{hdb_selected} <br> Total {total} <br> Available {avail}"),
                          icon=custom_icon).add_to(m)
            #tooltip=f"{hdb_selected} <br> Total lots: {total} <br> Available lots: {avail}",
            #icon=custom_icon).add_to(m)

            #folium.Marker(location=[lat, long],
            #              icon=hdb_DivIcon(hdb_selected, total, avail)).add_to(m)

            st.metric(label=hdb_selected, value=avail)


text1 = """
 <p style='text-align: left; color:AliceBlue';'>
 Map displays the number of parkings lots available in the select carparks.</p>
"""

with st.expander("View Map"):
    st.write(text1, unsafe_allow_html=True)
    folium_static(m, width=250, height=500)

st.write(
    f"<p style='text-align: left; color:Grey'> Data is updated on one minute interval</p>", unsafe_allow_html=True)

#poopup = folium.Popup(
#f"Total Lots: {coord[7]} <br> Available Lots: {coord[8]} <br> Type of Carpark: {coord[5]} <br> Short Term Parking: {coord[6]}", min_width = 300, max_width = 300)
#       folium.Marker(location=[coord[3], coord[4]],
#                     popup=poopup,
#                     tooltip=coord[2],
#                     icon=custom_icon).add_to(m)
#

#
#
#  # MarkCluster plugin for faster mapping
#mc = MarkerCluster()
#
#   # map lat and long data from complete list
#for coord in complete_list:
#    # create custom icon with hdb logo
#    custom_icon = folium.CustomIcon(
#        icon_image='carpark_logo.jpg', icon_size=(20, 20))
#    #iframe = folium.IFrame(
#    #    f"Total Lots: {coord[7]} <br> Available Lots: {coord[8]} <br> Type of Carpark: {coord[5]} <br> Short Term Parking: {coord[6]}")
#
#    # put carpark details with api data as pop-up
#    poopup = folium.Popup(
#        f"Total Lots: {coord[7]} <br> Available Lots: {coord[8]} <br> Type of Carpark: {coord[5]} <br> Short Term Parking: {coord[6]}", min_width=300, max_width=300)
#    folium.Marker(location=[coord[3], coord[4]],
#                    popup=poopup,
#                    tooltip=coord[2],
#                    icon=custom_icon).add_to(m)
#
#mc.add_to(m)
## use streamlit function
#folium_static(m, width=1000, height=560)

#with st.empty():
#... for seconds in range(60):
#...         st.write(f"⏳ {seconds} seconds have passed")
#..         time.sleep(1)
# ...     st.write("✔️ 1 minute over!")


#start_button = st.empty()
#stop_button = st.empty()
#place_holder = st.empty()
#with st.empty():

#def timer():
#    st.title("Real-Time / Live Data Science Dashboard")
#    with st.empty():
#        while True:
#            now_dt = datetime.datetime.today().replace(microsecond=0)
#            now_str = str(now_dt)
#            st.write(now_str)
#            time.sleep(1)
#
#st.button("Start", on_click=timer)



#with st.empty():
#    if st.button("Start"):
#        while True:
#            now_dt = datetime.datetime.today().replace(microsecond=0)
#            now_str = str(now_dt)
#            now_T = now_str.replace(' ', 'T')
#
#            #st.header(now_str)
#
#            endpoint = "https://api.data.gov.sg/v1/transport/carpark-availability"
#            # query parameter
#            query_params = {'date_time': now_T}
#            # get data and convert to json
#            data = requests.get(endpoint, params=query_params).json()
#            cp_code = []
#            total_lots = []
#            avail_lots = []
#
#            for item in data["items"]:
#                for detail in item["carpark_data"]:
#                    total_lots.append(detail["carpark_info"][0]["total_lots"])
#                    avail_lots.append(detail["carpark_info"][0]["lots_available"])
#
#            total_lots = total_lots[1:]
#            avail_lots = avail_lots[1:]
#
#            complete_list = []
#            for index in range(len(cp_code) - 1):
#                if cp_code[index] in cp_dict:
#                    complete_list.append([index,
#                                        cp_code[index],
#                                        cp_dict[cp_code[index]][0],
#                                        cp_dict[cp_code[index]][1],
#                                        cp_dict[cp_code[index]][2],
#                                        cp_dict[cp_code[index]][3],
#                                        cp_dict[cp_code[index]][4],
#                                        total_lots[index],
#                                        avail_lots[index]])
#
#            for carpark in complete_list:
#                if "BLK 13A UPPER BOON KENG ROAD" in carpark:
#                    bk = f" {carpark[7]} {carpark[8]}"
#                    st.write(bk)
#
#          
#            time.sleep(1)
    


    #
        #while True:
        #    now_dt = datetime.datetime.today().replace(microsecond=0)
        #    now_str = str(now_dt)
        #    # add 8 hours for streamlit server due to timezone difference
        #    now_plus8 = str(now_dt + datetime.timedelta(hours=8))
        #    st.write(now_str)
        #    time.sleep(1)

