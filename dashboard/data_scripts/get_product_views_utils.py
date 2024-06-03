
import requests
import time
from datetime import datetime, timedelta
import streamlit as st

def generate_monthly_ranges(start_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    today = datetime.now()
    
    # Initialize result list
    ranges = []
    
    # Generate monthly ranges
    while start_date < today:
        # Calculate end of the month
        end_of_month = start_date.replace(day=28) + timedelta(days=4)
        end_of_month = end_of_month - timedelta(days=end_of_month.day)
        
        # Convert dates to milliseconds
        start_at = int(start_date.timestamp() * 1000)
        end_at = int(end_of_month.timestamp() * 1000)
        
        # Append to result list
        ranges.append((start_at, end_at))
        
        # Move to the next month
        start_date = end_of_month + timedelta(days=1)
    
    return ranges

def get_page_views_for_specific_period(start_at, end_at, cookie):
    print(f"Getting page views for period: start_at = {start_at}, end_at = {end_at}")
    endpoint_url = f"https://www.faire.com/api/brand/analytics/product-sales-and-conversion?start_at={start_at}&end_at={end_at}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie
    }

    product_tokens = []
    names = []
    categories = []
    sales_count = []
    order_count = []
    visit_count = []
    date = []

    # we will retry the request 3 times if it fails

    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        try:
            # Make the GET request to the API
            response = requests.get(endpoint_url, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Loop through the product tiles
                for product in data["product_sales_and_conversion_data"]:
                    product_data = product["product"]
                    product_tokens.append(product_data["product_token"])
                    names.append(product_data["name"])
                    # if category is not in product append none
                    if "category" in product_data:
                        categories.append(product_data["category"])
                    else:
                        categories.append(None)
                    sales_count.append(product["sales_count"])
                    order_count.append(product["order_count"])
                    visit_count.append(product["visit_count"])
                    # we convert start_at to a date that looks like YYYY-mm-dd
                    date.append(datetime.fromtimestamp(start_at / 1000).strftime('%Y-%m-%d'))
                
                break
            
            elif response.status_code == 429:
                print(f"Rate limit exceeded. Retrying in 30 seconds (Retry {retry_count + 1}/3)")
                time.sleep(30)  # Wait for 30 seconds before retrying
                retry_count += 1
            else:
                print(response)
                print(f"An error occurred:", response.status_code)
                time.sleep(10)
                retry_count += 1
        except Exception as e:
            print(f"An error occurred: {e}")
            retry_count += 1
            time.sleep(10)
    
    return product_tokens, names, categories, sales_count, order_count, visit_count, date

# we get page views starting for each month starting first day 2023 until today
def get_page_views_for_all_months_since_date(cookie, starting_date):

    product_tokens = []
    names = []
    categories = []
    sales_count = []
    order_count = []
    visit_count = []
    date = []

    # we create a set of months from the starting date until today
    ranges = generate_monthly_ranges(starting_date)
    total_months = len(ranges)

    # Initialize a progress bar
    progress_bar = st.progress(0)

    for idx, (start_at, end_at) in enumerate(ranges, 1):
        print(f"Getting page views for month {idx}: start_at = {start_at}, end_at = {end_at}")
        product_tokens_month, names_month, categories_month, sales_count_month, order_count_month, visit_count_month, date_month = get_page_views_for_specific_period(start_at, end_at, cookie)
        time.sleep(10)
        product_tokens.extend(product_tokens_month)
        names.extend(names_month)
        categories.extend(categories_month)
        sales_count.extend(sales_count_month)
        order_count.extend(order_count_month)
        visit_count.extend(visit_count_month)
        date.extend(date_month)

        # Update the progress bar
        progress_percentage = idx / total_months
        progress_bar.progress(progress_percentage)
    
    data = {
        "product_token": product_tokens,
        "name": names,
        "category": categories,
        "sales_count": sales_count,
        "order_count": order_count,
        "visit_count": visit_count,
        "date": date
    }
    return data

