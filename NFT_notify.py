
import requests
import json
from win10toast import ToastNotifier
import time


asset_count = 0
asset_list = []
toaster = ToastNotifier()

print("Hey, just wanted to let you know, everything is working fine, minimize me")
print("I'll let you know as soon as you get an NFT")
print("Author: TheViralClovers/k3bri.wam, send me a text at sammysnakes' server, if you have feature ideas")

with open("owner.txt", "r") as f:
    owner = f.read()

def retrieve_template():
    response = requests.get(f"https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=alien.worlds&only_duplicate_templates=false&hide_offers=false&page=1&limit=100&order=desc&sort=asset_id")
    raw_data = json.loads(response.content)
    asset_data = raw_data['data']
    sorted_asset_data = sorted(asset_data, key = lambda i: int(i['minted_at_time']))
    nft_template = sorted_asset_data[-1]['template']['template_id']
    return nft_template

def retrieve_price():
    sale_count = 0
    total_wax = 0
    market_response = requests.get(f"https://wax.api.atomicassets.io/atomicmarket/v1/prices/sales?collection_name=alien.worlds&template_id={retrieve_template()}&is_transferable=true&is_burnable=true")
    market_json_raw = json.loads(market_response.content)
    market_json = market_json_raw['data']
    sorted_market_data = sorted(market_json, key = lambda i: int(i['price']))

    for i in sorted_market_data:
        sale_count +=1
        total_wax += int(i['price']) 

    NFT_price = (total_wax/(sale_count*100000000))

    return NFT_price

while True: 
    try:    
        with open("asset_count.txt", "r") as f:
            initial_asset_count = int(f.read())

        response = requests.get(f"https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=alien.worlds&only_duplicate_templates=false&hide_offers=false&page=1&limit=100&order=desc&sort=asset_id")
        raw_data = json.loads(response.content)
        asset_data = raw_data['data']
        sorted_asset_data = sorted(asset_data, key = lambda i: int(i['minted_at_time']))
        asset_count = len(asset_data)
        new_nft = sorted_asset_data[-1]['template']['immutable_data']['name']
        rarity = sorted_asset_data[-1]['template']['immutable_data']['rarity']
        image_path = 'alienworlds.ico'
        NFT_price = retrieve_price()

        if asset_count > initial_asset_count:
            toaster.show_toast("Congratulations!!!", f"You have just acquired a {rarity} {new_nft} which is worth {NFT_price:.2f} WAX", icon_path = image_path, duration = 10)
            with open("asset_count.txt", "w") as f:
                f.write(str(initial_asset_count + 1))
            print(f"{new_nft}")

        if asset_count < initial_asset_count:
            with open("asset_count.txt", "w") as f:
                f.write(str(asset_count))
        time.sleep(2)
    except:
        # toaster.show_toast("Hey, listen" , " I give up man, start me again, lol")
        pass