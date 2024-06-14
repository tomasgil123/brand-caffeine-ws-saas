import pandas as pd
from datetime import datetime

from dashboard.global_utils import (download_csv_from_cloud_storage, upload_dataframe_to_cloud_storage, delete_file_from_cloud_storage)
from dashboard.data_scripts.get_marketing_campaign_info_utils import get_marketing_campaigns_info

def get_marketing_info(client_name):

    # Get the data from the Google Cloud Storage bucket
    bucket_name = "faire_marketing_info"
    source_blob_name = f"{client_name}"

    df_marketing_info = download_csv_from_cloud_storage(bucket_name, source_blob_name)

    # df_marketing_info is None we return an empty dataframe
    if df_marketing_info is None:
        return pd.DataFrame()
    else:
        return df_marketing_info

def upload_marketing_info(brand_token, client_name, cookie):

    df_marketing_info, _ = get_marketing_info(client_name)

    bucket_name = "faire_marketing_info"

    # we add current date with format yyyy-mm-dd to file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    source_blob_name = f"{client_name}_{current_date}.csv"

    time_most_recent_campaign = 0

    # check if the dataframe is empty
    if df_marketing_info.empty:
        data = get_marketing_campaigns_info(brand_token, cookie=cookie, time_most_recent_campaign=time_most_recent_campaign, max_date="2023-01-01")

        # we create a new dataframe
        df = pd.DataFrame(data)

        return upload_dataframe_to_cloud_storage(bucket_name, source_blob_name, df)
    else:

        time_most_recent_campaign = df_marketing_info['start_sending_at'].max()
        # we substract a month to the time_most_recent_campaign
        # we do this because some campaign attributes could have been updated. We assume older campaigns don't get updated anymore
        time_most_recent_campaign = time_most_recent_campaign - 2630304000

        marketing_campaign_info = get_marketing_campaigns_info(brand_token, cookie=cookie, time_most_recent_campaign=time_most_recent_campaign)

        # we convert orders_info to a dataframe and then we download it as csv
        df = pd.DataFrame(marketing_campaign_info)

        # we append to df_current_marketing_campaign_info the new data
        df = pd.concat([df, df_marketing_info], ignore_index=True)

        # we drop duplicates
        df = df.drop_duplicates(subset='tokens', keep='first')

        # we delete previous file
        delete_file_from_cloud_storage(bucket_name, f"{client_name}")

        return upload_dataframe_to_cloud_storage(bucket_name, source_blob_name, df)