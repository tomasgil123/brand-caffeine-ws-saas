import pandas as pd
import requests
import time
import streamlit as st

from dashboard.utils_chatgpt import OpenaiInsights

def get_brands_data(brand_ids):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    # Initialize an empty list to store responses
    responses_brand_data = []

    # Initialize a progress bar
    progress_bar = st.progress(0)

    insights = OpenaiInsights()

    # Iterate over each brand ID and make a request
    for index, brand_id in enumerate(brand_ids):
        url = f"https://www.faire.com/api/v2/brand-view/{brand_id}"
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            responses_brand_data.append(response.json())

            print(f"Successfully fetched data for brand {index} of {len(brand_ids)}")
        else:
            print(f"Failed to fetch data for brand ID {brand_id}")

        progress_bar.progress(index / len(brand_ids))
        time.sleep(15)
    
    # Define empty lists to store the extracted information
    brand_tokens = []
    brand_names = []
    average_ratings = []
    number_of_reviews = []
    minimum_order_amounts = []
    first_order_minimum_amounts = []
    reorder_minimum_amounts = []
    sold_on_amazon = []
    eco_friendly = []
    hand_made = []
    charitable = []
    organic = []
    women_owned = []
    small_batch = []
    upper_bound_lead_time_days = []
    lower_bound_lead_time_days = []
    description = []

    # Iterate through the brand_list and extract the required information
    for brand_data in responses_brand_data:
        brand = brand_data["brand"]

        brand_tokens.append(brand["token"])
        brand_names.append(brand["name"])

        description_long = brand["description"]
        description_summary = insights.generate_insights({"prompt_name": "Competitors - description - summary", "brand_name": "", "string_data": description_long})
        description.append(description_summary)

        
        # Extract review info
        average_ratings.append(brand["brand_reviews_summary"]["average_rating"])
        number_of_reviews.append(brand["brand_reviews_summary"]["number_of_reviews"])
        first_order_minimum_amounts.append(brand["first_order_minimum_amount"]["amount_cents"] / 100)  # Convert cents to dollars
        
        # Extract minimum order info
        minimum_order_amounts.append(brand["minimum_order_amount"]["amount_cents"] / 100)  # Convert cents to dollars
        reorder_minimum_amounts.append(brand["reorder_minimum_amount"]["amount_cents"] / 100)  # Convert cents to dollars
        
        if "sold_on_amazon" in brand:
            sold_on_amazon.append(brand["sold_on_amazon"])
        else:
            sold_on_amazon.append(False)

        # if key eco_friendly exists
        if "eco_friendly" in brand:
            eco_friendly.append(brand["eco_friendly"])
        else:
            eco_friendly.append(False)

        # if key hand_made exists
        if "hand_made" in brand:
            hand_made.append(brand["hand_made"])
        else:
            hand_made.append(False)

        # if key charitable exists
        if "charitable" in brand:
            charitable.append(brand["charitable"])
        else:
            charitable.append(False)

        # if key organic exists
        if "organic" in brand:
            organic.append(brand["organic"])
        else:
            organic.append(False)

        # if key women_owned exists
        if "women_owned" in brand:
            women_owned.append(brand["women_owned"])
        else:
            women_owned.append(False)

        # if key small_batch exists
        if "small_batch" in brand:
            small_batch.append(brand["small_batch"])
        else:
            small_batch.append(False)

        # if key upper_bound_lead_time_days exists
        if "upper_bound_lead_time_days" in brand:
            upper_bound_lead_time_days.append(brand["upper_bound_lead_time_days"])
        else:
            upper_bound_lead_time_days.append(0)

        # if key lower_bound_lead_time_days exists
            
        if "lower_bound_lead_time_days" in brand:
            lower_bound_lead_time_days.append(brand["lower_bound_lead_time_days"])
        else:
            lower_bound_lead_time_days.append(0)

    # Create a DataFrame using the extracted information
    data = {
        "Brand Token": brand_tokens,
        "Brand Name": brand_names,
        "Average Rating": average_ratings,
        "Number of Reviews": number_of_reviews,
        "First Order Minimum Amount": first_order_minimum_amounts,
        "Minimum Order Amount": minimum_order_amounts,
        "Reorder Minimum Amount": reorder_minimum_amounts,
        "Sold on Amazon": sold_on_amazon,
        "Eco-Friendly": eco_friendly,
        "Hand-Made": hand_made,
        "Charitable": charitable,
        "Organic": organic,
        "Woman Owned": women_owned,
        "Small Batch": small_batch,
        "Upper Bound Lead Time Days": upper_bound_lead_time_days,
        "Lower Bound Lead Time Days": lower_bound_lead_time_days,
        "Description": description
    }

    return data