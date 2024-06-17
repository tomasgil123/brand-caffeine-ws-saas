import pandas as pd
from datetime import datetime

from dashboard.global_utils import (download_csv_from_cloud_storage, upload_dataframe_to_cloud_storage, delete_file_from_cloud_storage)
from dashboard.data_scripts.get_reviews_utils import get_reviews

def get_reviews_data(client_name):

    # Get the data from the Google Cloud Storage bucket
    bucket_name = "faire_reviews"
    source_blob_name = f"{client_name}_reviews"

    df_reviews, blob_name = download_csv_from_cloud_storage(bucket_name, source_blob_name)

    # df_orders is None we return an empty dataframe
    if df_reviews is None or df_reviews.empty:
        return pd.DataFrame(), blob_name
    else:
        df_reviews['created_at'] = pd.to_datetime(df_reviews['created_at'], unit='ms')
        df_reviews['publish_at'] = pd.to_datetime(df_reviews['publish_at'], unit='ms')
        return df_reviews, blob_name
    
def upload_reviews_data(brand_token, client_name, cookie):

    df_reviews, _ = get_reviews_data(client_name)

    bucket_name = "faire_reviews"

    # we add current date with format yyyy-mm-dd to file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    source_blob_name = f"{client_name}_reviews_{current_date}.csv"

    time_most_recent_review = 0

    # check if the dataframe is empty
    if df_reviews.empty:
        data = get_reviews(brand_token, cookie=cookie, time_most_recent_review=time_most_recent_review)

        # we create a new dataframe
        df = pd.DataFrame(data)

        return upload_dataframe_to_cloud_storage(bucket_name, source_blob_name, df)
    else:

        time_most_recent_review = df_reviews['created_at'].max()
        # we substract a month to the time_most_recent_review
        # we do this because some campaign attributes could have been updated. We assume older campaigns don't get updated anymore
        time_most_recent_review = time_most_recent_review - 2630304000

        df_reviews_last = get_reviews(brand_token, cookie=cookie, time_most_recent_review=time_most_recent_review)

        # we convert orders_info to a dataframe and then we download it as csv
        df = pd.DataFrame(df_reviews_last)

        # we append to df_current_marketing_campaign_info the new data
        df = pd.concat([df, df_reviews], ignore_index=True)

        # we drop duplicates
        df = df.drop_duplicates(subset='token', keep='first')

        # we delete previous file
        delete_file_from_cloud_storage(bucket_name, f"{client_name}_reviews")

        return upload_dataframe_to_cloud_storage(bucket_name, source_blob_name, df)