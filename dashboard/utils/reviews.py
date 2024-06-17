import pandas as pd
import streamlit as st

def get_reviews_orders_ratio(df_orders, df_reviews, date_last_update):
    """
    This function calculates the ratio of reviews to orders
    """
    df_orders = df_orders.copy()
    df_reviews = df_reviews.copy()

    # we convert last_date_update to datetime
    last_date_update = pd.to_datetime(date_last_update)
    # Filter orders from the last six months from last_date_update
    six_months_ago = last_date_update - pd.DateOffset(months=6)
    df_recent_orders = df_orders[df_orders['brand_contacted_at_values'] >= six_months_ago]

    # we filter reviews
    df_recent_reviews = df_reviews[df_reviews['created_at'] >= six_months_ago]

    # Extract year and month from the dates
    df_recent_reviews['review_month'] = df_recent_reviews['created_at'].dt.to_period('M')
    df_recent_orders['order_month'] = df_recent_orders['brand_contacted_at_values'].dt.to_period('M')

    # Count the number of reviews by month
    reviews_by_month = df_recent_reviews['review_month'].value_counts().sort_index()

    # Count the number of orders by month
    orders_by_month = df_recent_orders['order_month'].value_counts().sort_index()

    # Combine the results into a single dataframe
    monthly_counts_df = pd.DataFrame({
        'reviews': reviews_by_month,
        'orders': orders_by_month
    }).fillna(0).astype(int)

    # Reset the index to make 'month' a column
    monthly_counts_df = monthly_counts_df.reset_index()
    monthly_counts_df.columns = ['month', 'reviews', 'orders']

    monthly_counts_df['month'] = monthly_counts_df['month'].dt.to_timestamp().dt.strftime('%Y/%m/%d')

    return monthly_counts_df

def calculate_avg_ratio_and_total_reviews(dataframe, reference_date):
    # Convert 'month' column to datetime if it's not already
    dataframe['month'] = pd.to_datetime(dataframe['month'])
    
    # Convert reference_date to datetime
    reference_date = pd.to_datetime(reference_date)

    # Calculate the start date for the last 3 months
    start_date = reference_date - pd.DateOffset(months=3)
    
    # Filtering the last 3 months based on the reference date
    last_3_months = dataframe[(dataframe['month'] > start_date) & (dataframe['month'] <= reference_date)]

    # Calculating the reviews/orders ratio
    last_3_months['ratio'] = last_3_months['reviews'] / last_3_months['orders']

    # Calculating the average rate of the reviews/orders ratio
    avg_ratio = last_3_months['ratio'].mean()

    # Getting the total number of reviews received in the last 3 months
    total_reviews = last_3_months['reviews'].sum()

    # calculate total orders
    total_orders = last_3_months['orders'].sum()

    return avg_ratio, total_reviews, total_orders

def get_retailers_with_reviews_purchase_last_60_days(df_orders, df_reviews, data_last_update):

    # Assuming df_orders and df_reviews are your dataframes
    # Convert date columns to datetime if not already
    df_reviews['created_at'] = pd.to_datetime(df_reviews['created_at'])
    df_orders['brand_contacted_at_values'] = pd.to_datetime(df_orders['brand_contacted_at_values'])

    # 1. Filter orders data for last 60 days
    today = pd.to_datetime(data_last_update)
    # we make sure data_last_update is a date
    cutoff_date = today - pd.DateOffset(days=60)
    df_orders_filtered = df_orders[df_orders['brand_contacted_at_values'] >= cutoff_date]

    # 2. Identify retailers who have left reviews
    merged_df = pd.merge(df_orders_filtered, df_reviews, left_on='retailer_names', right_on='retailer_name', how='left')

    # Count reviews left by each retailer
    retailer_review_counts = merged_df.groupby('retailer_name')['rating'].count().reset_index()
    retailer_review_counts.rename(columns={'rating': 'review_count'}, inplace=True)

    # 3. Remove retailers who left a review for their last order
    # Identify retailers who left a review for their last order
    last_order_retailers = df_orders_filtered.loc[df_orders_filtered.groupby('retailer_names')['brand_contacted_at_values'].idxmax()]

    # we merge the last order retailers with the df_reviews and we keep only the retailers that left a review
    retailers_left_review_last_order = pd.merge(last_order_retailers, df_reviews, left_on='tokens', right_on='brand_order_token', how='inner')['retailer_names'].to_list()

    # we filter from retailer_review_counts the retailers that left a review for their last order
    final_retailers = retailer_review_counts[~retailer_review_counts['retailer_name'].isin(retailers_left_review_last_order)]

    # order by review count descending
    final_retailers = final_retailers.sort_values(by='review_count', ascending=False)

    # reset index
    final_retailers = final_retailers.reset_index(drop=True)

    return final_retailers
