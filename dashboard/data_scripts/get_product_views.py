import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from dashboard.global_utils import (download_csv_from_cloud_storage, upload_dataframe_to_cloud_storage, delete_file_from_cloud_storage)
from dashboard.data_scripts.get_product_views_utils import get_page_views_for_all_months_since_date

def get_product_views(client_name):

    # Get the data from the Google Cloud Storage bucket
    bucket_name = "faire_page_views"
    source_blob_name = f"{client_name}"

    df_page_views, blob_name = download_csv_from_cloud_storage(bucket_name, source_blob_name)

    # df_page_views is None we return an empty dataframe
    if df_page_views is None or df_page_views.empty:
        return pd.DataFrame(), blob_name
    else:
        def preprocess_date(date):
            if ' ' in date:
                return datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d')
            else:
                return datetime.strptime(date, '%Y-%m-%d').strftime('%Y/%m/%d')

        df_page_views['date'] = df_page_views['date'].apply(preprocess_date)

        df_page_views['date'] = pd.to_datetime(df_page_views['date'])

        return df_page_views, blob_name

def upload_product_views(client_name, cookie):

    df_page_views, _ = get_product_views(client_name)

    bucket_name = "faire_page_views"

    # we add current date with format yyyy-mm-dd to file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    source_blob_name = f"{client_name}_{current_date}.csv"

    # check if the dataframe is empty
    if df_page_views.empty:
        data = get_page_views_for_all_months_since_date(cookie=cookie, starting_date="2023-01-01")

        # we create a new dataframe
        df = pd.DataFrame(data)

        return upload_dataframe_to_cloud_storage(bucket_name, source_blob_name, df)
    else:

        # Parse the date column
        df_page_views['date'] = pd.to_datetime(df_page_views['date'])

        # Get the current date
        current_date = datetime.now()

        # Get the first day of the current month
        first_day_current_month = current_date.replace(day=1)

        # Get the first day of the previous month
        first_day_previous_month = (first_day_current_month - timedelta(days=1)).replace(day=1)

        # Get the first day of the month before the previous month
        first_day_previous_previous_month = first_day_previous_month - relativedelta(months=1)

        formatted_first_day_previous_month = first_day_previous_month.strftime("%Y-%m-%d")

        # Filter out rows from the current and previous months
        filtered_df = df_page_views[(df_page_views['date'] < first_day_previous_previous_month)]

        data = get_page_views_for_all_months_since_date(cookie=cookie, starting_date=formatted_first_day_previous_month)

        data_df = pd.DataFrame(data)
        # we add data rows to filtered_df dataframe
        combined_df = pd.concat([filtered_df, data_df])

        # Reset the index if necessary
        combined_df.reset_index(drop=True, inplace=True)

        # we delete previous file
        delete_file_from_cloud_storage(bucket_name, f"{client_name}")

        return upload_dataframe_to_cloud_storage(bucket_name, source_blob_name, combined_df)

        