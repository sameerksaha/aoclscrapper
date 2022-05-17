import streamlit as st

import app
from app import data1
import json

st.set_page_config(page_title="Scheduler Dashboard",layout='wide')

product_code = st.text_input('AOCL Scrapper')

button = st.button('submit')

if button:
    sku_datas = []
    link = data1[product_code]
    app.user(link)
    with open('sku_product_data.json')as json_file:
            data = json.load(json_file)
            for i in range(0, len(data["sku_codes_data"])):
                info = {
                    "Brand_Name": data['sku_codes_data'][i]['Brand Name'],
                    "Product_Name": data['sku_codes_data'][i]['Product Name'],
                    "Product_Code": data['sku_codes_data'][i]['Product Code'],
                    "Stock_Online": data['sku_codes_data'][i]['Stock Online'],
                    "Stock_Store": data['sku_codes_data'][i]['Stock Store'],
                    "List_Price": data['sku_codes_data'][i]['List Price'],
                    "Discount_Price": data['sku_codes_data'][i]['Discount Price'],
                    "Discount_Percentage": data['sku_codes_data'][i]['Discount Percentage'],
                    "Image_Link": data['sku_codes_data'][i]['Image Link']

                }
                sku_datas.append(info)

    st.write(sku_datas)