#DAY 3 ------PROJECT 1------- Vegetable Market Price Scraping 


import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta

start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 6, 30)

arr_data = []

directory = 'Day_3'
if not os.path.exists(directory):
    os.makedirs(directory)

current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')

    url = "https://vegetablemarketprice.com/api/dataapi/market/delhi/daywisedata?date=" + date_str

    header = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "Usr-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "sec-fetch-site": "same-origin",
        "cookie": "JSESSIONID=EFBD5BF0C820AA3BC815DB9769E0F25C; _ga=GA1.1.1260642287.1723005027; __gads=ID=6089d59fbf36470f:T=1723005024:RT=1723006868:S=ALNI_MZXZxt1v8qy9i959X44eiumAIY46A; __eoi=ID=e68a330d9f151d09:T=1723005024:RT=1723006868:S=AA-AfjaXO5sHi0wd_-rR1Otg_VTQ; _ga_2RYZG7Y4NC=GS1.1.1723005026.1.1.1723006880.0.0.0; FCNEC=%5B%5B%22AKsRol_ymKn9F6Ju4kje_wxllm36WapgP5SmO8FDNhjyv9FO4IKmydhGQwSQzxmwkO4s71PKPICJ3ycTn-OxbqRtUOpGxi0_ttfidE2s5qJOlrYjoUVwDiaNJXTh20DEcxPAqy2sZj4o2RFAkBG1XAgXHQEXUlNpLw%3D%3D%22%5D%5D",
        "Referer": "https://vegetablemarketprice.com/market/maharashtra/today",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    try:
        data = requests.get(url, headers=header)
        data.raise_for_status()  # Raise an error for bad responses
        print(f"Fetching data for {date_str}")

        js_data = json.loads(data.text)

        for api in js_data.get("data", []):
            veg_id = str(api.get("id", ""))
            veg_name = str(api.get("vegetablename", ""))
            whole_price = str(api.get("price", ""))
            retail_price = str(api.get("retailprice", ""))
            shoping_mall_price = str(api.get("shopingmallprice", ""))
            unit_val = str(api.get("units", ""))
            veg_image = str(api.get("table", {}).get("table_image_url", ""))

            new_js = {
                "Date": date_str,
                "State_Name": "Delhi",
                "veg_id": veg_id,
                "veg_name": veg_name,
                "whole_price": whole_price,
                "retail_price": retail_price,
                "shop_mall_price": shoping_mall_price,
                "unit_val": unit_val,
                "Vegetable_Image": veg_image
            }
            arr_data.append(new_js)

    except Exception as e:
        print(f"Error fetching data for {date_str}: {e}")
    
    current_date += timedelta(days=1)

if not arr_data:
    print("No data collected. Please check the API responses.")
else:
    df = pd.DataFrame(arr_data)

    file_path = os.path.join(directory, "out_Delhi.csv")
    df.to_csv(file_path, index=False)
    print(f"Data has been successfully saved to {file_path}.")


