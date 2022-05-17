import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
#import lxml

data1 = {}
gsheetid_req_prod_code = "1BsTIaLaV5b_XM0vCIG2mSx2JjEZRkcQtdezm2BkOGUo"
sheet_name_req_prod_code = "Sheet1"
gsheet_url_req_prod_code = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid_req_prod_code, sheet_name_req_prod_code)
req_product_codes = pd.read_csv(gsheet_url_req_prod_code)['Codigo ACO'].tolist()
# print(req_product_codes)
gsheetid_all_prod_code = "1qYzPPCfGXwwBlERq_D_FZZvq5mLd84jhKT75MtQfsuo"
sheet_name_all_prod_code = "Sheet1"
gsheet_url_all_prod_code = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid_all_prod_code, sheet_name_all_prod_code)

all_product_codes = pd.read_csv(gsheet_url_all_prod_code)
all_product_codes_dict = dict(zip(all_product_codes.Product_Code, all_product_codes.Product_Link))
# print(len(all_product_codes_dict))
#print(all_product_codes_dict)
# print(len(req_product_codes), len(all_product_codes)) 1131, 2791
# dict_obj.add(dict_obj.key, dict_obj.value)

for codes in all_product_codes_dict:
    if codes.strip() in req_product_codes:
        key = codes
        val = all_product_codes_dict[key]
        data1.update({key.strip(): val})


# print(data1["MI-GLA-052646"])
# mapped_product_codes.extend(req_product_codes)
# for codes in req_product_codes:
# if codes not in mapped_product_codes:
# not_mapped_codes.append(codes)

# print(len(all_product_codes), len(req_product_codes), len(mapped_product_codes), len(not_mapped_codes))
# df = pd.DataFrame(not_mapped_codes)
# df.to_csv("not_mapped_sku_codes.csv")
# df1 = pd.DataFrame(mapped_product_codes)
# df1.to_csv("mapped_sku_codes.csv")


def user(link):
    r = requests.get(link)
    data_stored = []
    soup = BeautifulSoup(r.content, "lxml")
    brand_name = soup.find(class_='marca').text.split(':')[1]
    product_name = soup.find(class_='name').text
    product_code = soup.find(class_='sku').text.split(':')[1]
    stock_online_stock_store = soup.find_all(class_='stock')
    stock_online = stock_online_stock_store[0].text.split(':')[1]
    stock_store = stock_online_stock_store[1].text.split(':')[1]
    list_price_dis_price = soup.find(class_='precio').getText(strip=True).split("$")
    list_price = "$" + list_price_dis_price[1]
    discount_price = "$" + str(''.join(i for i in list_price_dis_price[2] if i.isdigit()))
    discount = soup.find(class_='desc').text
    image_link = 'https://aco.cl/' + str(
        soup.find(class_='large cycle-slideshow').img['src'])
    data = ({
        "Brand Name": brand_name,
        "Product Name": product_name,
        "Product Code": product_code,
        "Stock Online": stock_online,
        "Stock Store": stock_store,
        "List Price": list_price,
        "Discount Price": discount_price,
        "Discount Percentage": discount,
        "Image Link": image_link
    })
    data_stored.append(data)

    # df = pd.DataFrame(data_stored)
    # ask_file_name = input("Enter your file name: ")
    # print("Completed")
    # df.to_csv(f"E:/AcoCl Script/{ask_file_name}.csv", index=False)
    all_data = {'sku_codes_data': data_stored}
    with open('sku_product_data.json', 'w') as outfile:
        json.dump(all_data, outfile, indent=4)
