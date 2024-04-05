import sys
import requests
from datetime import datetime
from plyer import notification

args = sys.argv[1:]

def skus_for_country():
    return {
        f"MU663LL/A": "256GB Black Titanium", 
        f"MU6A3LL/A": "512GB Black Titanium", 
        f"MU6F3LL/A": "1TB Black Titanium", 
        f"MU693LL/A": "256GB Blue Titanium", 
        f"MU6E3LL/A": "512GB Blue Titanium", 
        f"MU6J3LL/A": "1TB Blue Titanium", 
        f"MU683LL/A": "256GB Natural Titanium", 
        f"MU6D3LL/A": "512GB Natural Titanium", 
        f"MU6H3LL/A": "1TB Natural Titanium", 
        f"MU673LL/A": "256GB White Titanium", 
        f"MU6C3LL/A": "512GB White Titanium", 
        f"MU6G3LL/A": "1TB White Titanium"        
    }

control = "MU6A3LL/A"
store_number = "R065"
state = "PA"
country = "US"

if args:
    passed_store = args[0]
    country = args[1].upper() if len(args) > 1 else "US"
    if passed_store.startswith("R"):
        store_number = passed_store
        state = None

country_config = "us"
store_path = ""
sku_list = skus_for_country()


query = "&".join([f'parts.{i}={requests.utils.quote(k)}' for i, k in enumerate(sku_list.keys())]) + f"&searchNearby=true&store={store_number}"
url = f"https://www.apple.com{store_path}/shop/fulfillment-messages?{query}"

response = requests.get(url)
if response.status_code == 200:
    body = response.json()
    stores_array = body['body']['content']['pickupMessage']['stores']
    sku_counter = {}
    has_store_search_error = False

    print('Inventory\n---------')


    sku_mappings = skus_for_country()

    for store in stores_array:
        print(f"Store Name: {store['storeName']}")
        
        # Check each model's availability against the SKU mappings
        for sku, description in sku_mappings.items():
            availability = store['partsAvailability'].get(sku)
            
            # If the SKU is found in the store's parts availability
            if availability:
                status = "available for pickup" if availability.get('storePickEligible') and availability.get('pickupDisplay') == 'available' else "out of stock"
                print(f"  - {sku} ({description}): {status}")
            else:
                # If the SKU is not listed under this store's partsAvailability, it's considered not available
                print(f"  - {sku} ({description}): Not listed")
        
        print("-" * 50)  # Separator for readability
    # Example for sending notification

    # Log time at end
    print(f'\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
else:
    print("Failed to fetch data.")

