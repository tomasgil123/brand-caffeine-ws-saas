import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

def get_category_with_most_sales(df_orders, df_order_items, df_page_views):

    # we copy dataframes
    df_orders = df_orders.copy()
    df_order_items = df_order_items.copy()
    df_page_views = df_page_views.copy()

    # we keep only orders of the last 12 months
    current_date = pd.to_datetime('now')
    one_year_ago = current_date - pd.DateOffset(months=12)
    df_orders = df_orders[df_orders['brand_contacted_at_values'] >= one_year_ago]

    # we merge df_order_items with df_page_views on column "product_token". We only want to add column "category"
    df_page_views = df_page_views[['product_token', 'category']]
    # keep only unique rows
    df_page_views = df_page_views.drop_duplicates(subset=['product_token'])

    df_order_items = pd.merge(df_order_items, df_page_views, left_on=["product_token"], right_on=["product_token"])

    # we merge df_orders with df_order_items on column "brand_order_token"
    df_orders_merged = pd.merge(df_orders, df_order_items, left_on=["tokens"], right_on=["brand_order_token"])

    # create column retailer_price_total by multiplying quantity and retailer_price
    df_orders_merged['retailer_price_total'] = df_orders_merged['quantity'] * df_orders_merged['retailer_price']

    # create a bar chart with categories 0n the x axis and percentage of sales on the y axis
    # Group by category and sum the quantity sold
    sales_by_category = df_orders_merged.groupby('category')['retailer_price_total'].sum()

    # Calculate the total sales across all categories
    total_sales = sales_by_category.sum()

    # Calculate the percentage of total sales for each category
    sales_percentage = (sales_by_category / total_sales) * 100

    # Sort the sales percentages in descending order
    sales_percentage = sales_percentage.sort_values(ascending=False)

    # we keep only top category
    top_category = sales_percentage.idxmax()
    sales_percentage_top_category = sales_percentage.max()

    # we return category name and percentage
    return top_category, sales_percentage_top_category

def get_products_to_improve(data_original, date_last_update, selected_category):

    data = data_original.copy()
    # Calculate the date range for the last 12 months
    end_date = pd.to_datetime(date_last_update)
    start_date = end_date - timedelta(days=365)
    
    # Filter data for the last 12 months
    data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

    # Calculate the total page views for each product
    total_page_views = data[data['category'] == selected_category].groupby('name')['visit_count'].sum().reset_index()

    # Sort the products by Page views in descending order
    total_page_views = total_page_views.sort_values(by='visit_count', ascending=False)

    # Keep only the top 12 products
    filtered_products = total_page_views.head(12)['name']

    # Filter the original data to keep only the selected products
    filtered_data = data[data['name'].isin(filtered_products) & (data['category'] == selected_category)]
    # Group by 'name' and aggregate the sum of 'visit_count', 'order_count', and 'sales_count'
    grouped_df = filtered_data.groupby('name').agg({
        'visit_count': 'sum',
        'order_count': 'sum',
        'sales_count': 'sum'
    }).reset_index()

    grouped_df['Conversion rate'] =  (grouped_df['order_count']/grouped_df['visit_count'])*100

    # Find the median conversion rate
    median_conversion_rate = grouped_df['Conversion rate'].median()

    # Filter the products with conversion rate below the median
    product_most_page_views_worst_conversion_rate = grouped_df[grouped_df['Conversion rate'] < median_conversion_rate]

    # Select the product with the most page views among the filtered products
    product_most_page_views_worst_conversion_rate = product_most_page_views_worst_conversion_rate.loc[product_most_page_views_worst_conversion_rate['visit_count'].idxmax()]

    product_least_page_views_best_conversion_rate = grouped_df[grouped_df['Conversion rate'] > median_conversion_rate]

    # we select the product which has a conversion rate above the median with most views
    product_least_page_views_best_conversion_rate = product_least_page_views_best_conversion_rate.loc[product_least_page_views_best_conversion_rate['visit_count'].idxmax()]

    return  product_most_page_views_worst_conversion_rate, product_least_page_views_best_conversion_rate