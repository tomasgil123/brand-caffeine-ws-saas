import pandas as pd
from datetime import datetime
import streamlit as st

from dashboard.global_utils import (download_csv_from_cloud_storage, upload_dataframe_to_cloud_storage, delete_file_from_cloud_storage)
from dashboard.data_scripts.get_orders_utils import get_orders_info

#@st.cache_data(ttl=3600)  # cache data for 1 hour
def get_orders_data(client_name):

    # Get the data from the Google Cloud Storage bucket
    bucket_name = "faire_orders"
    source_blob_name = f"{client_name}_orders"

    df_orders, blob_name = download_csv_from_cloud_storage(bucket_name, source_blob_name)

    # df_orders is None we return an empty dataframe
    if df_orders is None or df_orders.empty:
        return pd.DataFrame(), blob_name
    else:
        df_orders['payout_total_values'] = df_orders['payout_total_values']/100

        # Convert 'brand_contacted_at_values' to datetime
        df_orders['brand_contacted_at_values'] = pd.to_datetime(df_orders['brand_contacted_at_values'], unit='ms')

        # Filter orders where creation_reasons is equal to NEW_ORDER
        df_orders = df_orders[(df_orders['creation_reasons'] == 'NEW_ORDER') & ((df_orders['states'] == 'SHIPPED') | (df_orders['states'] == 'DELIVERED'))]

        return df_orders, blob_name

#@st.cache_data(ttl=3600)  # cache data for 1 hour
def get_order_items_data(client_name):

    # Get the data from the Google Cloud Storage bucket
    bucket_name = "faire_orders"
    source_blob_name = f"{client_name}_orders_items"

    df_order_items, blob_name = download_csv_from_cloud_storage(bucket_name, source_blob_name)

    # df_order_items is None we return an empty dataframe
    if df_order_items is None or df_order_items.empty:
        return pd.DataFrame(), blob_name
    else:
        return df_order_items, blob_name
    
def upload_orders_info(brand_token, client_name, cookie):

    df_current_orders, _ = get_orders_data(client_name)
    df_current_order_items, _ = get_order_items_data(client_name)

    bucket_name = "faire_orders"

    # we add current date with format yyyy-mm-dd to file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    source_blob_name_orders = f"{client_name}_orders_{current_date}.csv"
    source_blob_name_order_items = f"{client_name}_orders_items_{current_date}.csv"

    # by default, we will only grab orders data from 2023 onwards
    time_most_recent_campaign = 1672531200000

    # check if the dataframe is empty
    if not df_current_orders.empty and not df_current_order_items.empty:
        time_most_recent_campaign = df_current_orders['brand_contacted_at_values'].max()
        # we substract a month to the time_most_recent_campaign
        # we do this because some campaign attributes could have been updated. We assume older campaigns don't get updated anymore
        time_most_recent_campaign = time_most_recent_campaign.timestamp() * 1000 - 2630304000
    
    data_orders, data_order_items = get_orders_info(brand_token, cookie=cookie, time_most_recent_campaign=time_most_recent_campaign)

    # we create a new dataframe
    df_orders_data = pd.DataFrame(data_orders)
    df_order_items_data = pd.DataFrame(data_order_items)

    df_orders = pd.concat([df_orders_data, df_current_orders], ignore_index=True)
    df_items_order = pd.concat([df_order_items_data, df_current_order_items], ignore_index=True)

    # we drop duplicates
    df_orders = df_orders.drop_duplicates(subset='tokens', keep='first')
    df_items_order = df_items_order.drop_duplicates(subset='token', keep='first')

    # we delete previous files
    delete_file_from_cloud_storage(bucket_name, f"{client_name}_orders")
    delete_file_from_cloud_storage(bucket_name, f"{client_name}_orders_items")

    upload_result_orders = upload_dataframe_to_cloud_storage(bucket_name, source_blob_name_orders, df_orders_data)
    upload_result_order_items = upload_dataframe_to_cloud_storage(bucket_name, source_blob_name_order_items, df_order_items_data)
    
    upload_successful = upload_result_orders and upload_result_order_items

    return upload_successful