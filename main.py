import folium
import streamlit_folium
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from data_process import complete_list
from api_call import now_modifed

st.set_page_config(page_title="hello", page_icon=":shark:", layout="wide")
st.title("Real-Time HDB Carpark Availability")
st.subheader(f"Current Date & Time : {now_modifed}")
st.text("[V1.0] Andy Oh | School of Business & Acccountancy | Ngee Ann Polytechnic".upper())

location = sorted(list(set([address[2] for address in complete_list])))

m = folium.Map(location=[1.3521, 103.8198], 
                min_zoom=11, 
                max_zoom=18, 
                zoom_start=12,
                max_bounds=True, 
                tiles="CartoDB positron",
                name="Light Map")

#cp_filter = st.selectbox("Select Carpark", [address[2] for address in complete_list])
#st.sidebar.write("HDB CARPARK")
st.sidebar.subheader(f"{now_modifed}")
filter2 = st.sidebar.multiselect("Select Carpark", location)

for index in range(len(complete_list)):
    if complete_list[index][2] not in filter2:
        pass

    else:
        total = complete_list[index][10]
        avail = complete_list[index][11]
        type = complete_list[index][6]
        short = complete_list[index][7]
        free = complete_list[index][8]
        night = complete_list[index][9]


        custom_icon = folium.CustomIcon(icon_image='carpark_logo.jpg', icon_size=(20, 20))       
        poopup = folium.Popup(f" TOTAL LOTS: {total} <br> AVAILABLE LOTS: {avail} <br> CARPARK TYPE:{type} <br> SHORT TERM PARKING: {short} <br> FREE PARKING: {free} <br> NIGHT PARKING: {night}",
                              min_width=300, max_width=300)
        
        folium.Marker(location=[complete_list[index][4], complete_list[index][5]],
        popup=poopup,
        tooltip=complete_list[index][3],
        icon=custom_icon).add_to(m)

folium_static(m, width=1000, height=560)

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

