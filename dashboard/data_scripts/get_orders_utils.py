import requests
import time
import streamlit as st

from dashboard.data_scripts.get_orders_items import (combine_order_items_info, get_order_items_info)


def get_orders_info_page(page_number, brand_token, cookie):
    endpoint_url = "https://www.faire.com/api/v2/brand-orders/list"

    payload = {
        "states": [],
        "brand_token": brand_token,
        "type_filter": "ALL",
        "page": page_number,
        "page_size": 100,
        "sort_by": "CREATED_AT",
        "sort_order": "DESC"
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie
    }

    # Initialize lists to store specific order attributes
    tokens = []
    creation_reasons = []
    states = []
    fulfillment_states = []
    sources = []
    brand_contacted_at_values = []
    first_order_for_brand_values = []
    very_first_order_for_brand_values = []
    retailer_tokens = []
    payout_total_values = []
    retailer_names = []
    retailer_website_urls = []
    retailer_store_types = []

    items_order = {}

    page_count = 1

    retry_count = 0

    while retry_count < 3:
        try:
            # Make the POST request to the API
            response = requests.post(endpoint_url, json=payload, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                page_count = data["pagination_data"]["page_count"]

                # Loop through the order tiles
                for order in data["brand_orders"]:
                    order_token = order["token"]
                    tokens.append(order_token)
                    creation_reasons.append(order["creation_reason"])
                    states.append(order["state"])
                    fulfillment_states.append(order["fulfillment_state"])
                    sources.append(order["source"])
                    brand_contacted_at_values.append(order["brand_contacted_at"])
                    first_order_for_brand_values.append(order["first_order_for_brand"])
                    # if the key very_first_order_for_brand is not present, we append None
                    if "very_first_order_for_brand" not in order:
                        very_first_order_for_brand_values.append(None)
                    else:
                        very_first_order_for_brand_values.append(order["very_first_order_for_brand"])
                    retailer_tokens.append(order["retailer_token"])
                    payout_total_values.append(order["payout_total"]["amount_cents"])

                    # we get retailers data
                    retailer_names.append(data["brand_order_tokens_to_retailer_names"][order_token])
                    retailer_details = data["brand_order_tokens_to_retailer_details"][order_token]
                    if "website_url" in retailer_details:
                        retailer_website_urls.append(retailer_details["website_url"])
                    else:
                        retailer_website_urls.append(None)
                    # if store_type exist, we add it to the list. Otherwise we add None
                    if "store_type" in retailer_details:
                        retailer_store_types.append(retailer_details["store_type"])
                    else:
                        retailer_store_types.append(None)
                    
                    # we add items order data to the dataframe
                    order_items = order["order_items"]
                    combine_order_items_info(items_order, get_order_items_info(order_items))
                

                break  # Successful request, exit the loop
            elif response.status_code == 429:
                print(f"Rate limit exceeded. Retrying in 30 seconds (Retry {retry_count + 1}/3)")
                time.sleep(30)  # Wait for 30 seconds before retrying
                retry_count += 1
            else:
                print(f"Request failed with status code {response.status_code}")
                break  # Exit the loop on other errors
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    print(f"Page {page_number} of {page_count} processed")

    data = {
        "tokens": tokens,
        "creation_reasons": creation_reasons,
        "states": states,
        "fulfillment_states": fulfillment_states,
        "sources": sources,
        "brand_contacted_at_values": brand_contacted_at_values,
        "first_order_for_brand_values": first_order_for_brand_values,
        "very_first_order_for_brand_values": very_first_order_for_brand_values,
        "retailer_tokens": retailer_tokens,
        "payout_total_values": payout_total_values,
        "retailer_names": retailer_names,
        "retailer_website_urls": retailer_website_urls,
        "retailer_store_types": retailer_store_types
    }

    return data, items_order, page_count

def find_first_older_date_index(brand_contacted_at_values, time_most_recent_campaign):
    # We check if the time_most_recent_campaign is bigger than any of the dates in start_sending_at
    # If it is, we return the index of the date that is not new

    print("start_sending_at", brand_contacted_at_values)
    print("time_most_recent_campaign", time_most_recent_campaign)
    
    for index, date in enumerate(brand_contacted_at_values):
        if date is not None and date < time_most_recent_campaign:
            # We return the index of the item that is not new
            print("index", index)
            return index
    return -1  # Return -1 if all dates are newer than time_most_recent_campaign

def get_orders_info(brand_token, cookie, time_most_recent_campaign):
    # Initialize lists to store the specific order attributes
    tokens = []
    creation_reasons = []
    sources = []
    states = []
    fulfillment_states = []
    brand_contacted_at_values = []
    first_order_for_brand_values = []
    very_first_order_for_brand_values = []
    retailer_tokens = []
    payout_total_values = []
    retailer_names = []
    retailer_website_urls = []
    retailer_store_types = []

    items_order = {}

    # we loop over the different pages and get the orders info
    page_number = 1
    data_orders, items_order_page, page_count  =  get_orders_info_page(page_number, brand_token, cookie)

    first_older_date_index = find_first_older_date_index(brand_contacted_at_values=data_orders["brand_contacted_at_values"], time_most_recent_campaign=time_most_recent_campaign)

    if first_older_date_index == -1:
        time.sleep(10)
        tokens.extend(data_orders["tokens"])
        creation_reasons.extend(data_orders["creation_reasons"])
        states.extend(data_orders["states"])
        fulfillment_states.extend(data_orders["fulfillment_states"])
        sources.extend(data_orders["sources"])
        brand_contacted_at_values.extend(data_orders["brand_contacted_at_values"])
        first_order_for_brand_values.extend(data_orders["first_order_for_brand_values"])
        very_first_order_for_brand_values.extend(data_orders["very_first_order_for_brand_values"])
        retailer_tokens.extend(data_orders["retailer_tokens"])
        payout_total_values.extend(data_orders["payout_total_values"])
        retailer_names.extend(data_orders["retailer_names"])
        retailer_website_urls.extend(data_orders["retailer_website_urls"])
        retailer_store_types.extend(data_orders["retailer_store_types"])
        # we append the items order data to the dataframe
        combine_order_items_info(items_order, items_order_page)
    else:
        tokens.extend(data_orders["tokens"][:first_older_date_index])
        creation_reasons.extend(data_orders["creation_reasons"][:first_older_date_index])
        states.extend(data_orders["states"][:first_older_date_index])
        fulfillment_states.extend(data_orders["fulfillment_states"][:first_older_date_index])
        sources.extend(data_orders["sources"][:first_older_date_index])
        brand_contacted_at_values.extend(data_orders["brand_contacted_at_values"][:first_older_date_index])
        first_order_for_brand_values.extend(data_orders["first_order_for_brand_values"][:first_older_date_index])
        very_first_order_for_brand_values.extend(data_orders["very_first_order_for_brand_values"][:first_older_date_index])
        retailer_tokens.extend(data_orders["retailer_tokens"][:first_older_date_index])
        payout_total_values.extend(data_orders["payout_total_values"][:first_older_date_index])
        retailer_names.extend(data_orders["retailer_names"][:first_older_date_index])
        retailer_website_urls.extend(data_orders["retailer_website_urls"][:first_older_date_index])
        retailer_store_types.extend(data_orders["retailer_store_types"][:first_older_date_index])
        # we append the items order data to the dataframe
        combine_order_items_info(items_order, items_order_page)

    # Initialize a progress bar
    progress_bar = st.progress(0)
    # we loop over the different pages and get the orders info
    if page_count > 1:
        for page_number in range(2, page_count + 1):
            data_orders, items_order_page, _ =  get_orders_info_page(page_number, brand_token, cookie)

            first_older_date_index = find_first_older_date_index(brand_contacted_at_values=data_orders["brand_contacted_at_values"], time_most_recent_campaign=time_most_recent_campaign)

            if first_older_date_index == -1:
                time.sleep(10)
                tokens.extend(data_orders["tokens"])
                creation_reasons.extend(data_orders["creation_reasons"])
                states.extend(data_orders["states"])
                fulfillment_states.extend(data_orders["fulfillment_states"])
                sources.extend(data_orders["sources"])
                brand_contacted_at_values.extend(data_orders["brand_contacted_at_values"])
                first_order_for_brand_values.extend(data_orders["first_order_for_brand_values"])
                very_first_order_for_brand_values.extend(data_orders["very_first_order_for_brand_values"])
                retailer_tokens.extend(data_orders["retailer_tokens"])
                payout_total_values.extend(data_orders["payout_total_values"])
                retailer_names.extend(data_orders["retailer_names"])
                retailer_website_urls.extend(data_orders["retailer_website_urls"])
                retailer_store_types.extend(data_orders["retailer_store_types"])
                # we append the items order data to the dataframe
                combine_order_items_info(items_order, items_order_page)
            else:
                tokens.extend(data_orders["tokens"][:first_older_date_index])
                creation_reasons.extend(data_orders["creation_reasons"][:first_older_date_index])
                states.extend(data_orders["states"][:first_older_date_index])
                fulfillment_states.extend(data_orders["fulfillment_states"][:first_older_date_index])
                sources.extend(data_orders["sources"][:first_older_date_index])
                brand_contacted_at_values.extend(data_orders["brand_contacted_at_values"][:first_older_date_index])
                first_order_for_brand_values.extend(data_orders["first_order_for_brand_values"][:first_older_date_index])
                very_first_order_for_brand_values.extend(data_orders["very_first_order_for_brand_values"][:first_older_date_index])
                retailer_tokens.extend(data_orders["retailer_tokens"][:first_older_date_index])
                payout_total_values.extend(data_orders["payout_total_values"][:first_older_date_index])
                retailer_names.extend(data_orders["retailer_names"][:first_older_date_index])
                retailer_website_urls.extend(data_orders["retailer_website_urls"][:first_older_date_index])
                retailer_store_types.extend(data_orders["retailer_store_types"][:first_older_date_index])
                # we append the items order data to the dataframe
                combine_order_items_info(items_order, items_order_page)
                break
            progress_bar.progress(page_number / (page_count + 1))

    data = {
        "tokens": tokens,
        "creation_reasons": creation_reasons,
        "states": states,
        "fulfillment_states": fulfillment_states,
        "sources": sources,
        "brand_contacted_at_values": brand_contacted_at_values,
        "first_order_for_brand_values": first_order_for_brand_values,
        "very_first_order_for_brand_values": very_first_order_for_brand_values,
        "retailer_tokens": retailer_tokens,
        "payout_total_values": payout_total_values,
        "retailer_names": retailer_names,
        "retailer_website_urls": retailer_website_urls,
        "retailer_store_types": retailer_store_types
    }

    return data, items_order