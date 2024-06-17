import pandas as pd
from datetime import datetime, timedelta

from dashboard.customers.get_customers import (get_top_20_customers_without_purchases_last_60_days, 
                                               get_customers_without_second_purchase_last_60_days)

from dashboard.data_scripts.get_orders import (get_orders_data)

from dashboard.charts.email_marketing_charts import (sales_for_quantile)

from dashboard.global_utils import (get_date_from_blob_name, delete_file_from_cloud_storage, 
                             upload_dataframe_to_cloud_storage, download_csv_from_cloud_storage)

def get_marketing_recommendations(client_name):
    # Get the data from the Google Cloud Storage bucket
    bucket_name = "faire_marketing_info"
    source_blob_name = f"{client_name}_marketing_recommendations"

    df_marketing_recommendations, blob_name = download_csv_from_cloud_storage(bucket_name, source_blob_name)

    # df_marketing_recommendations is None we return an empty dataframe
    if df_marketing_recommendations is None:
        return pd.DataFrame(), blob_name
    else:
        return df_marketing_recommendations, blob_name


def upload_marketing_recommendations(client_name, cookie):

    df_orders, blob_name = get_orders_data(client_name)

    date_last_update = get_date_from_blob_name(blob_name)

    if not df_orders.empty:

        date_last_update = pd.to_datetime(date_last_update)

        sales_for_top_20 = sales_for_quantile(df=df_orders,day_data_was_obtained=date_last_update, quantile=0.8)*100

        # Get today's date
        today = datetime.today()

        # Calculate the date 60 days in the past
        date_60_days_ago = today - timedelta(days=60)

        # Calculate the date 120 days in the past
        date_120_days_ago = today - timedelta(days=120)

        # Convert to Unix timestamp in milliseconds
        timestamp_60_days_ago = int(date_60_days_ago.timestamp())*1000
        timestamp_120_days_ago = int(date_120_days_ago.timestamp())*1000

        # Get the top 20 customers without purchases in the last 60 days
        top_20_customers, _ = get_top_20_customers_without_purchases_last_60_days(cookie, timestamp_120_days_ago, timestamp_60_days_ago , sales_for_top_20)
        top_20_customers_faire_direct, _ = get_top_20_customers_without_purchases_last_60_days(cookie,timestamp_120_days_ago, timestamp_60_days_ago, sales_for_top_20, True)

        # Get the customers without a second purchase in the last 60 days
        customers_without_second_purchase, _ = get_customers_without_second_purchase_last_60_days(cookie,timestamp_120_days_ago, timestamp_60_days_ago)
        customers_without_second_purchase_faire_direct, _ = get_customers_without_second_purchase_last_60_days(cookie, timestamp_120_days_ago, timestamp_60_days_ago, True)

        # we create a dataframe with this columns get_top_20_customers_without_purchases_last_60_days and
        # get_customers_without_second_purchase_last_60_days
        df = pd.DataFrame({
            "get_top_20_customers_without_purchases_last_60_days": [top_20_customers],
            "get_top_20_customers_without_purchases_last_60_days_faire_direct": [top_20_customers_faire_direct],
            "get_customers_without_second_purchase_last_60_days": [customers_without_second_purchase],
            "get_customers_without_second_purchase_last_60_days_faire_direct": [customers_without_second_purchase_faire_direct]
        })

        bucket_name = "faire_marketing_info"

        # we add current date with format yyyy-mm-dd to file name
        current_date = datetime.now().strftime("%Y-%m-%d")
        source_blob_name = f"{client_name}_marketing_recommendations_{current_date}.csv"

        # we delete previous files
        delete_file_from_cloud_storage(bucket_name, f"{client_name}_marketing_recommendations")

        # we upload the new file
        return upload_dataframe_to_cloud_storage(bucket_name=bucket_name, destination_blob_name=source_blob_name, df=df )
    else:
        return False