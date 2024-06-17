import pandas as pd
from datetime import datetime, timedelta

from dashboard.customers.get_customers import (get_customers_with_purchase_last_60_days_no_review)

from dashboard.global_utils import (delete_file_from_cloud_storage, 
                             upload_dataframe_to_cloud_storage, download_csv_from_cloud_storage)

def get_review_recommendations(client_name):
    # Get the data from the Google Cloud Storage bucket
    bucket_name = "faire_reviews"
    source_blob_name = f"{client_name}_recommendations"

    df_reviews_recommendations, blob_name = download_csv_from_cloud_storage(bucket_name, source_blob_name)

    # df_reviews_recommendations is None we return an empty dataframe
    if df_reviews_recommendations is None:
        return pd.DataFrame(), blob_name
    else:
        df_reviews_recommendations['order_amount'] = df_reviews_recommendations['order_amount']/100

        return df_reviews_recommendations, blob_name


def upload_reviews_recommendations(client_name, cookie):

    number_customers, first_20_customers = get_customers_with_purchase_last_60_days_no_review(cookie)

    # we create a dataframe with the first_20_customers
    df = pd.DataFrame(first_20_customers)
    df['get_customers_with_purchase_last_60_days_no_review'] = number_customers

    bucket_name = "faire_reviews"

    # we add current date with format yyyy-mm-dd to file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    source_blob_name = f"{client_name}_recommendations_{current_date}.csv"

    # we delete previous files
    delete_file_from_cloud_storage(bucket_name, f"{client_name}_recommendations")

    # we upload the new file
    return upload_dataframe_to_cloud_storage(bucket_name=bucket_name, destination_blob_name=source_blob_name, df=df )