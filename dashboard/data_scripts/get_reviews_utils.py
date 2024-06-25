import requests
import time
import streamlit as st

def get_reviews_page(brand_token, cookie, page_number):

    url_endpoint = f"https://www.faire.com/api/brand/reviews/{brand_token}?page={page_number}&pageSize=10&sortBy=CREATED_AT&requestedSortOrder=DESC"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie
    }

    token =[]
    brand_order_token = []
    rating = []
    comment = []
    replies = []
    retailer_name = []
    created_at = []
    publish_at = []

    page_count = 1

    retry_count = 0

    rate_limit_hits = 0

    while retry_count < 3:
        try:
            response = requests.get(url_endpoint, headers=headers)
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                page_count = data["pagination_data"]["page_count"]

                for review in data["brand_reviews"]:
                    token.append(review.get("token", None))
                    brand_order_token.append(review.get("brand_order_token", None))
                    rating.append(review.get("rating", None))
                    
                    # we need to combine "title" and "comment in a single string
                    title = review.get("title", "")
                    comments = review.get("comment", "")

                    title_comment = title + " " + comments

                    comment.append(title_comment)
                    replies.append(len(review.get("replies", [])))  # Default to empty list if "replies" is missing
                    retailer_name.append(review.get("retailer_name", None))
                    created_at.append(review.get("created_at", None))
                    publish_at.append(review.get("publish_at", None))
                
                break  # Successful request, exit the loop

            elif response.status_code == 429:
                print(f"Rate limit exceeded. Retrying in 30 seconds (Retry {retry_count + 1}/3)")
                time.sleep(30)  # Wait for 30 seconds before retrying
                retry_count += 1
                rate_limit_hits += 1
                
                # Update headers to bypass rate limit
                ip_suffix = rate_limit_hits + 1
                headers.update({
                    'X-Originating-IP': f'127.0.0.{ip_suffix}',
                    'X-Forwarded-For': f'127.0.0.{ip_suffix}',
                    'X-Remote-IP': f'127.0.0.{ip_suffix}',
                    'X-Remote-Addr': f'127.0.0.{ip_suffix}',
                    'X-Client-IP': f'127.0.0.{ip_suffix}',
                    'X-Host': f'127.0.0.{ip_suffix}',
                    'X-Forwarded-Host': f'127.0.0.{ip_suffix}'
                })
            else:
                print(f"Request failed with status code {response.status_code}")
                break  # Exit the loop on other errors
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    data = {
        "token": token,
        "brand_order_token": brand_order_token,
        "rating": rating,
        "comment": comment,
        "replies": replies,
        "retailer_name": retailer_name,
        "created_at": created_at,
        "publish_at": publish_at
    }
    return data, page_count

def find_first_older_date_index(created_at, time_most_recent_review):
    # We check if the time_most_recent_review is bigger than any of the dates in created_at
    # If it is, we return the index of the date that is not new
    
    for index, date in enumerate(created_at):
        if date is not None and date < time_most_recent_review:
            # We return the index of the item that is not new
            return index
    return -1  # Return -1 if all dates are newer than time_most_recent_review

def get_reviews(brand_token, cookie, time_most_recent_review):

    all_data = {
        "token": [],
        "brand_order_token": [],
        "rating": [],
        "comment": [],
        "replies": [],
        "retailer_name": [],
        "created_at": [],
        "publish_at": []
    }

    page_number = 1

     # Initialize a progress bar
    progress_bar = st.progress(0)

    while True:
        data, page_count = get_reviews_page(brand_token, cookie, page_number)

        created_at_page = data["created_at"]

        first_older_date_index = find_first_older_date_index(created_at=created_at_page, time_most_recent_review=time_most_recent_review)

        if first_older_date_index == -1:
            # If all dates are newer than time_most_recent_review, we add all data
            for key in all_data.keys():
                all_data[key].extend(data[key])
        else:
            # If we find a date that is older than time_most_recent_review, we only add the data up to that point
            for key in all_data.keys():
                all_data[key].extend(data[key][:first_older_date_index])
            break
        
        # Update the progress bar
        progress_bar.progress(page_number / page_count)

        if page_number >= page_count:
            break  # Exit the loop when all pages have been fetched
        time.sleep(20)  # Add a delay to avoid hitting the rate limit
        page_number += 1

    return all_data
