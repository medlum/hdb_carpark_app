import streamlit as st
from api_call import data
from cp_dict import cp_dict

# ------------------ data processing ------------------ #
global complete_list
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

