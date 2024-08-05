import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

def get_email_marketing_kpis_last_30_days(df, date_last_update):

    # Convert start_sending_at to datetime
    df['start_sending_at'] = pd.to_datetime(df['start_sending_at'], unit='ms')

    # Filter rows with state "COMPLETED" and start_sending_at within the last 30 days
    recent_completed_campaigns = df[(df['states'] == 'COMPLETED') & (df['start_sending_at'] >= date_last_update - timedelta(days=30))]

    # Calculate the weighted averages
    weighted_average_view = (recent_completed_campaigns['view_count'] / recent_completed_campaigns['delivered_count']).mean()
    weighted_average_click = (recent_completed_campaigns['click_count'] / recent_completed_campaigns['delivered_count']).mean()
    weighted_average_open_based_orders = (recent_completed_campaigns['open_based_orders_count'] / recent_completed_campaigns['delivered_count']).mean()

    # Count the number of campaigns
    number_of_campaigns = len(recent_completed_campaigns)

    card_data = [
        {"title": "Total campaigns", "value": f"{number_of_campaigns:,.2f}"},
        {"title": "Average open rate", "value": f"{weighted_average_view:.2%}"},
        {"title": "Average click rate", "value": f"{weighted_average_click:.2%}"},
        {"title": "Average placed order rate", "value": f"{weighted_average_open_based_orders:.2%}"},
    ]

    st.markdown(f"""

                    <div class="row">
                            <div class="col">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">{card_data[0]["title"]}</h5>
                                        <p class="card-text">Value: {card_data[0]["value"]}</p>
                                    </div>
                                </div>
                            </div>
                        <div class="col">
                        <div class="card">
                            <div class="card-body">
                            <h5 class="card-title">{card_data[1]["title"]}</h5>
                            <p class="card-text">Value: {card_data[1]["value"]}</p>
                            </div>
                        </div>
                        </div>
                        <div class="col">
                        <div class="card">
                            <div class="card-body">
                            <h5 class="card-title">{card_data[2]["title"]}</h5>
                            <p class="card-text">Value: {card_data[2]["value"]}</p>
                            </div>
                        </div>
                        </div>
                        <div class="col">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">{card_data[3]["title"]}</h5>
                                        <p class="card-text">Value: {card_data[3]["value"]}</p>
                                    </div>
                                </div>
                            </div>
                    </div>
    """, unsafe_allow_html=True)


def get_email_marketing_kpis_by_month(df):
    df = df.copy()
        # Filter rows with state equal to "DRAFT"
    # Filter rows with "state" equal to "COMPLETED"
    completed_rows = df[df['states'] == 'COMPLETED']

    # Convert 'start_sending_at' to datetime
    completed_rows['start_sending_at'] = pd.to_datetime(completed_rows['start_sending_at'], unit='ms')

    # Group by month
    completed_rows['month'] = completed_rows['start_sending_at'].dt.to_period('M').astype(str)

    # Calculate weighted sum for each ratio by month
    completed_rows['view_ratio'] = completed_rows['view_count'] / completed_rows['delivered_count']
    completed_rows['click_ratio'] = completed_rows['click_count'] / completed_rows['delivered_count']
    completed_rows['open_based_ratio'] = completed_rows['open_based_orders_count'] / completed_rows['delivered_count']

    # Calculate the total delivered count for weighting by month
    total_delivered_count_by_month = completed_rows.groupby('month')['delivered_count'].sum()

    # Calculate weighted average for each ratio by month
    weighted_avg_view_ratio_by_month = (completed_rows['view_ratio'] * completed_rows['delivered_count']).groupby(completed_rows['month']).sum() / total_delivered_count_by_month
    weighted_avg_click_ratio_by_month = (completed_rows['click_ratio'] * completed_rows['delivered_count']).groupby(completed_rows['month']).sum() / total_delivered_count_by_month
    weighted_avg_open_based_ratio_by_month = (completed_rows['open_based_ratio'] * completed_rows['delivered_count']).groupby(completed_rows['month']).sum() / total_delivered_count_by_month

    # we multiple by 100 to get the percentage
    weighted_avg_view_ratio_by_month = weighted_avg_view_ratio_by_month * 100
    weighted_avg_click_ratio_by_month = weighted_avg_click_ratio_by_month * 100
    weighted_avg_open_based_ratio_by_month = weighted_avg_open_based_ratio_by_month * 100

    columns = ['Average open rate', 'Average click rate', 'Average placed order rate']
    # Create a DataFrame to store the results
    weighted_avg_by_month_df = pd.DataFrame({
        columns[0]: weighted_avg_view_ratio_by_month,
        columns[1]: weighted_avg_click_ratio_by_month,
        columns[2]: weighted_avg_open_based_ratio_by_month
    })

    # weighted_avg_by_month_df = weighted_avg_by_month_df
    weighted_avg_by_month_df['month'] = weighted_avg_by_month_df.index

    # Plotting
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))

    for i, column in enumerate(columns):
        axes[i].plot(weighted_avg_by_month_df['month'].iloc[-12:], weighted_avg_by_month_df[column].iloc[-12:], marker='o', linestyle='-')
        axes[i].set_title(column, fontsize=20, loc='left', pad=12, fontweight=500, color="#31333f", fontfamily="Microsoft Sans Serif")
        axes[i].set_xlabel('Month')
        axes[i].set_ylabel('Value')
        axes[i].grid(axis='y')
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].set_ylim(0, None)
        # Add % symbol to y-axis tick labels
        fmt = '%.2f%%'  # Format as percentage with no decimal places
        axes[i].yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: fmt % x))
        

    
    plt.tight_layout()
    
    st.pyplot(fig)

def sales_by_month(df, type_action, title, date_last_update):
    df = df.copy()
    # Filter rows with state "COMPLETED"
    completed_campaigns = df[df['states'] == 'COMPLETED']

    # Convert the 'start_sending_at' column to datetime
    completed_campaigns['start_sending_at'] = pd.to_datetime(completed_campaigns['start_sending_at'], unit='ms')

    # Extract month from the 'start_sending_at' column
    completed_campaigns['month'] = completed_campaigns['start_sending_at'].dt.to_period('M')

    # Group by month and sum the 'open_based_total_order_value'
    sales_by_month = completed_campaigns.groupby('month')[type_action].sum()

    # Get the last 12 months
    end_date = pd.to_datetime(date_last_update.date())
    start_date = end_date - pd.DateOffset(months=11)
    last_12_months = pd.period_range(start=start_date, end=end_date, freq='M')

    # Filter sales for the last 12 months
    #sales_by_last_12_months = sales_by_month[last_12_months]
    sales_by_last_12_months = sales_by_month.reindex(last_12_months, fill_value=0)

    # Create a bar chart
    fig, ax = plt.subplots()
    sales_by_last_12_months.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Sales')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(range(len(last_12_months)), [month.strftime('%Y-%m') for month in last_12_months], rotation=45)
    plt.tight_layout()

    plt.title(title, fontsize=13, loc='left', pad=12, fontweight=500, color="#31333f", fontfamily="Microsoft Sans Serif")

    # Show the chart
    st.pyplot(fig)

def retailers_did_not_reorder(df, day_data_was_obtained):
    df = df.copy()
    # Calculate the date 12 months ago from today
    df_filtered_2023 = df[df['brand_contacted_at_values'].dt.year == 2023]

    # Filter by 'very_first_order_for_brand_values' equal to True
    df_filtered_very_first = df_filtered_2023[df_filtered_2023['very_first_order_for_brand_values'] | df_filtered_2023['first_order_for_brand_values']]

    # Create an array of unique retailer_tokens
    unique_retailer_tokens = df_filtered_very_first['retailer_tokens'].unique()

    # Filter the original DataFrame using the unique retailer_tokens
    df_final = df[df['retailer_tokens'].isin(unique_retailer_tokens)]

    # Sort the DataFrame by retailer and timestamp
    df_final_sorted = df_final.sort_values(by=['retailer_tokens', 'brand_contacted_at_values'])

    # we group by retailer and count number of orders
    number_of_orders = df_final_sorted.groupby('retailer_tokens').size()

    # we convert this to a dataframe
    number_of_orders = number_of_orders.to_frame()

    # we set the index as a column
    number_of_orders.reset_index(inplace=True)

    # we rename both columns
    number_of_orders.columns = ['retailer_tokens', 'number_of_orders']

    # Count the number of retailers with only one order
    one_order_retailers = number_of_orders[number_of_orders['number_of_orders'] == 1].shape[0]

    # Count the number of retailers with more than one order
    more_than_one_order_retailers = number_of_orders[number_of_orders['number_of_orders'] > 1].shape[0]

    # Pie chart data
    labels = ['Retailers with 1 Order', 'Retailers with more than 1 Order']
    sizes = [one_order_retailers, more_than_one_order_retailers]
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)  # explode 1st slice

    # Create figure and axis
    fig, ax = plt.subplots()

    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.set_title('Percentage of Retailers with Only One Order (Year 2023)')
    
    # Display chart in Streamlit
    st.pyplot(fig)

def sales_for_quantile(df, day_data_was_obtained, quantile):
    # we make a copy of the dataframe 
    df = df.copy()

    # Calculate the date 12 months ago from today
    last_12_months_date = day_data_was_obtained - timedelta(days=365)

    # Filter the DataFrame for the last 12 months
    df_last_12_months = df[df['brand_contacted_at_values'] >= last_12_months_date]

    # Determine the column to group by
    group_by_column = 'retailer_tokens'
    if 'retailer_names' in df.columns:
        group_by_column = 'retailer_names'

    # Group by retailer_tokens and sum the payout_total_values for each retailer
    sales_by_retailer = df_last_12_months.groupby(group_by_column)['payout_total_values'].sum().sort_values(ascending=False)

    # we convert this series to a dataframe
    sales_by_retailer = sales_by_retailer.to_frame()

    # we add index as a column
    sales_by_retailer.reset_index(inplace=True)

    rounded_number = round(sales_by_retailer['payout_total_values'].quantile(quantile) / 10) * 10
    
    return rounded_number

def top_10_customers(df, day_data_was_obtained):
    df = df.copy()

    # Calculate the date 12 months ago from today
    last_12_months_date = day_data_was_obtained - timedelta(days=365)

    # Filter the DataFrame for the last 12 months
    df_last_12_months = df[df['brand_contacted_at_values'] >= last_12_months_date]

    # Determine the column to group by
    group_by_column = 'retailer_tokens'
    if 'retailer_names' in df.columns:
        group_by_column = 'retailer_names'

    # Group by retailer_tokens and sum the payout_total_values for each retailer
    sales_by_retailer = df_last_12_months.groupby(group_by_column).agg({
        'payout_total_values': 'sum',
        'brand_contacted_at_values': 'max'  # Get the most recent purchase date
    }).sort_values('payout_total_values', ascending=False)

    # Convert this series to a dataframe
    sales_by_retailer = sales_by_retailer.reset_index()

    # Calculate top 10 customers
    top_10_customers = sales_by_retailer.head(10)

    # we make a left join top_10_customers to add "retailer_tokens" column
    top_10_customers = top_10_customers.merge(df[['retailer_tokens', 'retailer_names']], on='retailer_names', how='left')

    # keep unique rows
    top_10_customers = top_10_customers.drop_duplicates(subset=['retailer_names'])
    
    top_10_customers['retailer_tokens'] = top_10_customers['retailer_tokens'].apply(lambda x: f"https://www.faire.com/brand-portal/messages/{x}")

    top_10_customers['retailer_tokens'] = top_10_customers['retailer_tokens'].apply(lambda x: f'<a href="{x}" target="_blank">Send a DM</a>')

    # Calculate days since last purchase
    top_10_customers['days_since_last_purchase'] = (day_data_was_obtained - top_10_customers['brand_contacted_at_values']).dt.days

    # Calculate total revenue
    total_revenue = sales_by_retailer['payout_total_values'].sum()

    # last column should be retailer_tokens
    top_10_customers = top_10_customers[['retailer_names', 'payout_total_values','brand_contacted_at_values', 'days_since_last_purchase', 'retailer_tokens']]

    # Format the date as mm-dd-yyyy
    top_10_customers['brand_contacted_at_values'] = top_10_customers['brand_contacted_at_values'].dt.strftime('%m-%d-%Y')
    
    # Calculate revenue percentage for the top 10 customers
    top_10_revenue = top_10_customers['payout_total_values'].sum()
    top_10_revenue_percentage = round((top_10_revenue / total_revenue) * 100, 2)

    return top_10_customers, top_10_revenue_percentage

def purchase_frequency(df):
    # Select orders made in 2023
    df_filtered_2023 = df[df['brand_contacted_at_values'].dt.year == 2023]

    # Sort the DataFrame by retailer and timestamp
    df_final_sorted = df_filtered_2023.sort_values(by=['retailer_tokens', 'brand_contacted_at_values'])

    # Calculate the time difference between consecutive orders for each retailer
    df_final_sorted['time_diff'] = df_final_sorted.groupby('retailer_tokens')['brand_contacted_at_values'].diff().dt.days

    # Group by retailer and find the median number of days between orders for every retailer
    median_days_between_orders = df_final_sorted.groupby('retailer_tokens')['time_diff'].median()

    # we filter rows were time_dff is None
    median_days_between_orders = median_days_between_orders[~median_days_between_orders.isna()]

    # we filter rows were time_dff is 0
    median_days_between_orders = median_days_between_orders[median_days_between_orders != 0]

    # we convert this series to a dataframe
    median_days_between_orders = median_days_between_orders.to_frame()

    # use index as column retailer_tokens
    median_days_between_orders.reset_index(inplace=True)

    # Create figure and axis
    fig, ax = plt.subplots()

    # Create histogram
    ax.hist(median_days_between_orders['time_diff'], bins=20, color='skyblue', edgecolor='black')

    # Add labels and title
    ax.set_xlabel('Time Difference (days)')
    ax.set_ylabel('Frequency (Number of retailers)')
    ax.set_title('Distribution of Days between Orders (Orders made in 2023)')

    # Calculate percentiles
    fiftieth_percentile = np.percentile(median_days_between_orders['time_diff'], 50)
    seventy_fifth_percentile = np.percentile(median_days_between_orders['time_diff'], 75)

    # Add percentage annotation
    ax.axvline(x=fiftieth_percentile, color='r', linestyle='--', linewidth=1)
    ax.text(fiftieth_percentile+1, ax.get_ylim()[1]*0.05, '50% of retailers re-order in less than {} days'.format(int(fiftieth_percentile)), rotation=90)

    # Add percentage annotation
    ax.axvline(x=seventy_fifth_percentile, color='r', linestyle='--', linewidth=1)
    ax.text(seventy_fifth_percentile+1, ax.get_ylim()[1]*0.05, '75% of retailers re-order in less than {} days'.format(int(seventy_fifth_percentile)), rotation=90)
    
    # Display chart in Streamlit
    st.pyplot(fig)

def sales_by_store_type(df, df_order_items, df_page_views):

    # we create a copy of the dataframe
    df = df.copy()

    # we remove rows where retailer_store_types is null
    df.dropna(subset=['retailer_store_types'], inplace=True)

    # Filter data for the last 12 months
    current_date = pd.to_datetime('now')
    one_year_ago = current_date - pd.DateOffset(months=12)
    df_last_12_months = df[df['brand_contacted_at_values'] >= one_year_ago]

    # Group data by 'retailer_store_types' and calculate the sales count for each type of store
    sales_by_store_type = df_last_12_months.groupby('retailer_store_types')['payout_total_values'].sum()

    # Calculate the total sales count for the last 12 months
    total_sales = sales_by_store_type.sum()

    # Calculate the percentage of sales for each type of store
    sales_percentage = (sales_by_store_type / total_sales) * 100

    # Sort the sales percentages in descending order and select the top 5
    top_5_sales_percentage = sales_percentage.sort_values(ascending=False).head(5)
    others_percentage = 100 - top_5_sales_percentage.sum()

    # Create a new Series for "Others" with the same index as the top 5 for consistency
    others_series = pd.Series([others_percentage], index=['Others'])

    # Use concat to combine the series
    sales_percentage_with_others = pd.concat([top_5_sales_percentage, others_series])

    # Create a pie chart
    fig, ax = plt.subplots()
    sales_percentage_with_others.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
    ax.set_ylabel('')  # Remove the y-label as it's not needed for pie charts
    ax.set_title('Sales Percentage by Store Type (Last 12 Months)')

    st.pyplot(fig)

    # we select the top 3 store types from top_5_sales_percentage
    top_3_store_types = top_5_sales_percentage.index[:3].values

    filtered_df = df_last_12_months[df_last_12_months['retailer_store_types'].isin(top_3_store_types)]

    df_orders_merged = pd.merge(filtered_df, df_order_items, left_on=["tokens"], right_on=["brand_order_token"])

    # Group by store type and product name, then sum the quantities sold
    grouped_products = df_orders_merged.groupby(['retailer_store_types', 'product_token'])['quantity'].sum().reset_index()

    # Sort each group by quantity sold in descending order
    grouped_products['rank'] = grouped_products.groupby('retailer_store_types')['quantity'].rank(method='dense', ascending=False)

    # Filter to get the top five most sold products for each store type
    top_five_products_by_type = grouped_products[grouped_products['rank'] <= 5]

    # Sort the DataFrame by store type and rank
    top_five_products_by_type_sorted = top_five_products_by_type.sort_values(by=['retailer_store_types', 'rank'])

    # merge top_five_products_by_type_sorted with df_page_views, bringing only column "name". Merge on column "product_token"
    df_page_views = df_page_views[['product_token', 'name']]
    # drop duplicates
    df_page_views.drop_duplicates(subset=['product_token'], inplace=True)
    top_five_products_by_type_sorted = pd.merge(top_five_products_by_type_sorted, df_page_views, left_on=["product_token"], right_on=["product_token"])

    # drop column "product_token"
    top_five_products_by_type_sorted.drop(columns=['product_token'], inplace=True)
    # change name of columns to "Store Type", "Product Name", "Quantity Sold" and "Rank"
    top_five_products_by_type_sorted.rename(columns={"retailer_store_types": "Store Type", "quantity": "Quantity Sold", "rank": "Rank", "name": "Product Name"}, inplace=True)
    st.write("TOp 5 products by store type")
    st.dataframe(top_five_products_by_type_sorted)

def sales_by_category(df_orders, df_order_items, df_page_views):

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

    # we keep only 5 first categories
    sales_percentage = sales_percentage.head(5)

    # Create a bar chart
    # Create figure and axis
    fig, ax = plt.subplots()

    sales_percentage.plot(kind='bar', color='skyblue')

    ax.set_title('Sales by Category (Last 12 Months)')
    ax.set_xlabel('Category')
    ax.set_ylabel('Percentage of Sales')
    ax.set_xticklabels(sales_percentage.index, rotation=45)
    ax.set_ylim(0, 100)  # Set y-axis limit to 0-100%

    # add grid to the chart
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Display the chart in Streamlit
    st.pyplot(fig)

def avg_order_value_by_store_type(df, day_data_was_obtained):
    # we make a copy of the dataframe 
    df = df.copy()

    # Calculate the date 12 months ago from today
    last_12_months_date = day_data_was_obtained - timedelta(days=365)

    # Filter the DataFrame for the last 12 months
    df_last_12_months = df[df['brand_contacted_at_values'] >= last_12_months_date]

    # Group by retailer_store_types and calculate the average order value for each type of store
    avg_order_value_by_store_type = df_last_12_months.groupby('retailer_store_types')['payout_total_values'].mean()

    # Sort the values in descending order
    avg_order_value_by_store_type = avg_order_value_by_store_type.sort_values(ascending=False)

    # Create a bar chart
    # Create figure and axis
    fig, ax = plt.subplots()

    avg_order_value_by_store_type.plot(kind='bar', color='skyblue')

    ax.set_title('Average Order Value by Store Type (Last 12 Months)')
    ax.set_xlabel('Store Type')
    ax.set_ylabel('Average Order Value')
    ax.set_xticklabels(avg_order_value_by_store_type.index, rotation=45)

    # add grid to the chart
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Display the chart in Streamlit
    st.pyplot(fig)

def retailers_did_not_reorder_month_over_month(df):

    df = df.copy()
    # Convert 'brand_contacted_at_values' to datetime
    df['brand_contacted_at'] = pd.to_datetime(df['brand_contacted_at_values'], unit='ms')

    # Assign month to each order
    df['order_month'] = df['brand_contacted_at'].dt.to_period('M')

    # Sort the dataframe by date
    df = df.sort_values('brand_contacted_at')

    # Filter for first orders
    first_orders = df[(df['first_order_for_brand_values'] == True) | (df['very_first_order_for_brand_values'] == True)]

    # Function to check if a retailer made an order within 90 days
    def ordered_within_90_days(row):
        retailer_token = row['retailer_tokens']
        first_order_date = row['brand_contacted_at']
        next_90_days = first_order_date + timedelta(days=90)
        return any((df['retailer_tokens'] == retailer_token) & 
                (df['brand_contacted_at'] > first_order_date) & 
                (df['brand_contacted_at'] <= next_90_days))

    # Apply the function to each first order
    first_orders['ordered_within_90_days'] = first_orders.apply(ordered_within_90_days, axis=1)

    # Group by month and count retailers
    monthly_stats = first_orders.groupby('order_month').agg({
        'retailer_tokens': 'count',
        'ordered_within_90_days': lambda x: x.sum()
    }).rename(columns={
        'retailer_tokens': 'total_new_retailers',
        'ordered_within_90_days': 'retailers_ordered_within_90_days'
    })

    monthly_stats['retailers_not_ordered_within_90_days'] = monthly_stats['total_new_retailers'] - monthly_stats['retailers_ordered_within_90_days']

    # create new column with index
    monthly_stats['order_month'] = monthly_stats.index

    # Dynamically calculate the end date (3 months before the current month)
    current_date = pd.Timestamp.now()
    start_date = (current_date - pd.DateOffset(months=15)).to_period('M')
    end_date = (current_date - pd.DateOffset(months=3)).to_period('M')

    # Filter out orders before 2023 and the last three months
    monthly_stats = monthly_stats[(monthly_stats['order_month'] >= start_date) & (monthly_stats['order_month'] <= end_date)]

    # Convert the index to mm/yyyy format
    monthly_stats['order_month'] = monthly_stats['order_month'].dt.strftime('%m/%Y')

    # Calculate percentages
    monthly_stats['reorder_percentage'] = monthly_stats['retailers_ordered_within_90_days'] / monthly_stats['total_new_retailers'] * 100
    monthly_stats['no_reorder_percentage'] = monthly_stats['retailers_not_ordered_within_90_days'] / monthly_stats['total_new_retailers'] * 100

    # Create the stacked bar chart
    fig, ax = plt.subplots(figsize=(8, 4))

    # Plot the bars
    ax.bar(monthly_stats['order_month'], monthly_stats['reorder_percentage'], label='Reordered')
    ax.bar(monthly_stats['order_month'], monthly_stats['no_reorder_percentage'], 
        bottom=monthly_stats['reorder_percentage'], label='Did Not Reorder')

    # Customize the chart
    ax.set_ylabel('Percentage of Retailers')
    ax.set_title('Retailer Reorder Behavior by Month')
    ax.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Add percentage labels on the bars
    for i, (reorder, no_reorder) in enumerate(zip(monthly_stats['reorder_percentage'], monthly_stats['no_reorder_percentage'])):
        ax.text(i, reorder/2, f'{reorder:.1f}%', ha='center', va='center')
        ax.text(i, reorder + no_reorder/2, f'{no_reorder:.1f}%', ha='center', va='center')

    # Adjust layout and display the chart
    plt.tight_layout()

    # If you're using Streamlit, use this instead of plt.show()
    st.pyplot(fig)

def top_retailers_did_not_reorder_month_over_month(df, start_date_str, spending_threshold):
    # Convert date strings to datetime objects
    df['brand_contacted_at'] = pd.to_datetime(df['brand_contacted_at_values'], unit='ms')
    
    # Parse start date and get current date
    start_date = datetime.strptime(start_date_str, "%m-%Y")
    end_date = datetime.now().replace(day=1)
    
    # Sort the dataframe by date
    df = df.sort_values('brand_contacted_at')
    
    # Initialize results list
    results = []
    
    current_date = start_date
    while current_date <= end_date:
        # Calculate date ranges
        three_months_ago = current_date - timedelta(days=90)
        fifteen_months_ago = three_months_ago - timedelta(days=365)
        
        # Filter orders for the 12 months starting from 3 months ago
        last_12_months = df[(df['brand_contacted_at'] > fifteen_months_ago) & 
                            (df['brand_contacted_at'] <= three_months_ago)]
        
        # Group by retailer and sum payout_total_values
        retailer_spending = last_12_months.groupby('retailer_tokens')['payout_total_values'].sum()
        
        # Filter retailers who spent more than the threshold
        high_spending_retailers = retailer_spending[retailer_spending > spending_threshold]
        
        recent_purchase_count = 0
        no_recent_purchase_count = 0
        
        retailers_data = []
        
        for retailer, spend in high_spending_retailers.items():
            retailer_name = df[df['retailer_tokens'] == retailer]['retailer_names'].iloc[0]
            
            # Check if the retailer made a purchase in the last 90 days
            recent_purchase = not df[(df['retailer_tokens'] == retailer) & 
                                     (df['brand_contacted_at'] > three_months_ago) & 
                                     (df['brand_contacted_at'] <= current_date)].empty
            
            if recent_purchase:
                recent_purchase_count += 1
            else:
                no_recent_purchase_count += 1
            
            retailers_data.append({
                'retailer_token': retailer,
                'retailer_name': retailer_name,
                'total_spend': spend,
                'recent_purchase': recent_purchase
            })
        
        results.append({
            'month': current_date.strftime('%B %Y'),
            'retailers': retailers_data,
            'recent_purchase_count': recent_purchase_count,
            'no_recent_purchase_count': no_recent_purchase_count
        })
        
        # Move to the next month
        current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    
    # convert results to dataframe
    results_df = pd.DataFrame(results)

    months = results_df['month']
    recent_purchase_percentages = []
    no_recent_purchase_percentages = []

    for _, row in results_df.iterrows():
        total = row['recent_purchase_count'] + row['no_recent_purchase_count']
        recent_purchase_percentages.append(row['recent_purchase_count'] / total * 100)
        no_recent_purchase_percentages.append(row['no_recent_purchase_count'] / total * 100)

    fig, ax = plt.subplots(figsize=(8, 4))
    
    bars1 = ax.bar(months, recent_purchase_percentages, label='Recent Purchase')
    bars2 = ax.bar(months, no_recent_purchase_percentages, bottom=recent_purchase_percentages, label='No Recent Purchase')

    ax.set_xlabel('Month')
    ax.set_ylabel('Percentage of Top Retailers')
    ax.set_title('Percentage of Top Retailers with Recent Purchases vs No Recent Purchases')
    ax.legend()

    plt.xticks(rotation=45, ha='right')
    # Function to add value labels on the bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_y() + height/2,
                    f'{height:.1f}%',
                    ha='center', va='center', rotation=0)

    add_value_labels(bars1)
    add_value_labels(bars2)

    plt.tight_layout()

    st.pyplot(fig)

def top_products_by_type_of_store(df_orders, df_order_items):
    df_orders = df_orders.copy()
    df_order_items = df_order_items.copy()

    # Calculate revenue by store type
    revenue_by_store_type = df_orders.groupby('retailer_store_types')['payout_total_values'].sum().sort_values(ascending=False)

    # we filter "Other"
    revenue_by_store_type = revenue_by_store_type[revenue_by_store_type.index != 'Other']

    # Get top 5 store types by revenue
    top_3_store_types = revenue_by_store_type.nlargest(3)

    merged_df = pd.merge(df_orders, df_order_items, left_on='tokens', right_on='brand_order_token')

    # we keep only last 90 days of data
    current_date = pd.to_datetime('now')
    last_90_days = current_date - pd.DateOffset(days=90)
    merged_df = merged_df[merged_df['brand_contacted_at_values'] >= last_90_days]

    df_orders = df_orders[df_orders['brand_contacted_at_values'] >= last_90_days]

    # create a date column witrh format yyyy-mm-dd
    df_orders['date'] = df_orders['brand_contacted_at_values'].dt.date

    # Group by store type and product name, then sum the quantities
    grouped = merged_df.groupby(['retailer_store_types', 'product_name'])['quantity'].sum().reset_index()
    

    # Sort the results and get the top product for each store type
    top_products = grouped.sort_values(['retailer_store_types', 'quantity'], ascending=[True, False])
    # Get the top 5 products for each store type
    top_10_products = top_products.groupby('retailer_store_types').head(10).reset_index(drop=True)

    # Optional: Sorting within each store type for better readability
    top_10_products = top_10_products.sort_values(['retailer_store_types', 'quantity'], ascending=[True, False]).reset_index(drop=True)

    # we keep only store types in top_3_store_types
    top_10_products = top_10_products[top_10_products['retailer_store_types'].isin(top_3_store_types.index)]

    st.write("Top 10 products by store type")
    st.dataframe(top_10_products)

def percentage_revenue_store_type(df):
    df = df.copy()

    # Replace empty store types with 'Other'
    df['retailer_store_types'] = df['retailer_store_types'].fillna('Other')

    # Calculate revenue by store type
    revenue_by_store_type = df.groupby('retailer_store_types')['payout_total_values'].sum().sort_values(ascending=False)

    # Calculate percentage of stores with and without type
    total_stores = df['retailer_tokens'].nunique()
    stores_with_type = df[df['retailer_store_types'] != 'Other']['retailer_tokens'].nunique()
    stores_without_type = total_stores - stores_with_type

    st.write(f"Percentage of stores with type: {stores_with_type/total_stores*100:.2f}%")
    st.write(f"Percentage of stores without type (Other): {stores_without_type/total_stores*100:.2f}%")

    # we filter "Other"
    revenue_by_store_type = revenue_by_store_type[revenue_by_store_type.index != 'Other']

    # Get top 5 store types by revenue
    top_5_store_types = revenue_by_store_type.nlargest(5)

    # Create a new series with top 5 and 'Other'
    revenue_by_store_type_grouped = pd.Series(dtype='float64')
    revenue_by_store_type_grouped = top_5_store_types.copy()

    # Sum the revenue for all other store types
    other_revenue = revenue_by_store_type[~revenue_by_store_type.index.isin(top_5_store_types.index)].sum()

    # Add 'Other' category to the new series
    revenue_by_store_type_grouped['Other'] = other_revenue

    # Create a pie chart
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(revenue_by_store_type_grouped, 
                                    labels=revenue_by_store_type_grouped.index, 
                                    autopct='%1.1f%%', 
                                    startangle=90,
                                    wedgeprops=dict(width=0.5))

    # Enhance the appearance
    ax.set_title('Top 5 Store Types by Revenue')
    plt.setp(autotexts, size=8, weight="bold")
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Add a legend
    ax.legend(wedges, top_5_store_types.index,
            title="Store Types",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1))

    plt.tight_layout()

    # display chart astreamlit
    st.pyplot(fig)

def percentage_revenue_store_type_by_month(df):
    df = df.copy()
    # Convert brand_contacted_at_values to datetime
    df['brand_contacted_at'] = pd.to_datetime(df['brand_contacted_at_values'], unit='ms')

    # Replace empty store types with 'Other'
    df['retailer_store_types'] = df['retailer_store_types'].fillna('Other')

    # Extract month and year
    df['month_year'] = df['brand_contacted_at'].dt.to_period('M')

    # Group by month_year and store type, then sum the revenue
    revenue_by_month_store = df.groupby(['month_year', 'retailer_store_types'])['payout_total_values'].sum().unstack(fill_value=0)

    # remove "Other" column
    revenue_by_month_store = revenue_by_month_store.drop(columns='Other', errors='ignore')

    # Function to get top 5 store types and group others
    def top_5_and_other(series):
        top_5 = series.nlargest(5)
        other_sum = series[~series.index.isin(top_5.index)].sum()
        result = pd.concat([top_5, pd.Series({'Other': other_sum})])
        return result

    # Apply the function to each month
    result = revenue_by_month_store.apply(top_5_and_other, axis=1)

    # Sort columns by total revenue
    column_order = result.sum().sort_values(ascending=False).index
    result = result[column_order]

    # Replace None values with 0
    result = result.fillna(0)

    # Calculate percentages
    result_percentages = result.div(result.sum(axis=1), axis=0) * 100

    # Round percentages to two decimal places
    result_percentages = result_percentages.round(2)

    result_percentages.index = result_percentages.index.strftime('%m/%Y')

    fig, ax = plt.subplots(figsize=(12, 6))

    result_percentages.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Percentage Revenue by Store Type and Month')
    ax.set_xlabel('Month/Year')
    ax.set_ylabel('Percentage')
    ax.legend(title='Store Types', bbox_to_anchor=(1.05, 1), loc='upper left')

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    st.pyplot(fig)

def avg_order_value_by_store_type(df):
    df = df.copy()

    # 1. Filter out retailers without a store type
    df_filtered = df[df['retailer_store_types'].notna()]

    # 2. Pick the 10 store types which generated the most revenue
    store_type_revenue = df_filtered.groupby('retailer_store_types')['payout_total_values'].sum().sort_values(ascending=False)
    top_10_store_types = store_type_revenue.head(10).index.tolist()

    # 3. Label other store types as "Other"
    df_filtered['store_type_grouped'] = df_filtered['retailer_store_types'].apply(lambda x: x if x in top_10_store_types else 'Other')

    # Calculate average order value by store type
    avg_order_value = df_filtered.groupby('store_type_grouped')['payout_total_values'].mean().sort_values(ascending=False)
    st.write("Average order value by store type:")
    st.dataframe(avg_order_value)

# def sales_by_category(df_orders, df_order_items, df_page_views):

#     # we keep only orders of the last 12 months
#     current_date = pd.to_datetime('now')
#     one_year_ago = current_date - pd.DateOffset(months=12)
#     df_orders = df_orders[df_orders['brand_contacted_at_values'] >= one_year_ago]

#     # we merge df_order_items with df_page_views on column "product_token". We only want to add column "category"
#     df_page_views = df_page_views[['product_token', 'category']]
#     df_order_items = pd.merge(df_order_items, df_page_views, left_on=["product_token"], right_on=["product_token"])

#     # we merge df_orders with df_order_items on column "brand_order_token"
#     df_orders_merged = pd.merge(df_orders, df_order_items, left_on=["tokens"], right_on=["brand_order_token"])

#     # create a bar chart with categories 0n the x axis and percentage of sales on the y axis
#     # Group by category and sum the quantity sold
#     sales_by_category = df_orders_merged.groupby('category')['retailer_price'].sum()

#     # Calculate the total sales across all categories
#     total_sales = sales_by_category.sum()

#     # Calculate the percentage of total sales for each category
#     sales_percentage = (sales_by_category / total_sales) * 100

#     # Sort the sales percentages in descending order
#     sales_percentage = sales_percentage.sort_values(ascending=False)

#     # we keep only 5 first categories
#     sales_percentage = sales_percentage.head(5)

#     # Create a bar chart
#     # Create figure and axis
#     fig, ax = plt.subplots()

#     sales_percentage.plot(kind='bar', color='skyblue')

#     ax.set_title('Sales by Category (Last 12 Months)')
#     ax.set_xlabel('Category')
#     ax.set_ylabel('Percentage of Sales')
#     ax.set_xticklabels(sales_percentage.index, rotation=45)
#     ax.set_ylim(0, 100)  # Set y-axis limit to 0-100%

#     # add grid to the chart
#     ax.grid(axis='y', linestyle='--', alpha=0.7)

#     # Display the chart in Streamlit
#     st.pyplot(fig)

def top_10_products_last_90_days(df_orders, df_order_items):
    # we copy dataframes
    df_orders = df_orders.copy()
    df_order_items = df_order_items.copy()
    # Convert 'brand_contacted_at_values' to datetime if it's not already
    df_orders['brand_contacted_at_values'] = pd.to_datetime(df_orders['brand_contacted_at_values'])

    # Filter orders for the last 90 days
    current_date = pd.to_datetime('now')
    ninety_days_ago = current_date - pd.DateOffset(days=90)
    df_orders = df_orders[df_orders['brand_contacted_at_values'] >= ninety_days_ago]

    # Merge order items with orders
    df_merged = pd.merge(df_order_items, df_orders, left_on="brand_order_token", right_on="tokens")

    # Group by product and sum the quantity sold
    top_products = df_merged.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(10)
    st.write("Top 10 products sold in the last 90 days:")
    st.dataframe(top_products)

def top_10_products_by_category_last_90_days(df_orders, df_order_items, df_page_views):
    # we copy dataframes
    df_orders = df_orders.copy()
    df_order_items = df_order_items.copy()
    df_page_views = df_page_views.copy()
    # Convert 'brand_contacted_at_values' to datetime if it's not already
    df_orders['brand_contacted_at_values'] = pd.to_datetime(df_orders['brand_contacted_at_values'])

    # Filter orders for the last 90 days
    current_date = pd.to_datetime('now')
    ninety_days_ago = current_date - pd.DateOffset(days=90)
    df_orders = df_orders[df_orders['brand_contacted_at_values'] >= ninety_days_ago]

    # Merge order items with orders
    df_merged = pd.merge( df_orders, df_order_items, left_on="tokens", right_on="brand_order_token")

    df_page_views_deduplicated = df_page_views.drop_duplicates(subset='product_token')

    # Merge with page views to get product names and categories
    df_merged = pd.merge(df_merged, df_page_views_deduplicated[['product_token', 'category']], on="product_token")

    # Calculate total sales by category
    category_sales = df_merged.groupby('category')['quantity'].sum().sort_values(ascending=False)

    # Get the top 2 categories
    top_3_categories = category_sales.head(3).index.tolist()

    # Filter for top 2 categories
    df_top_categories = df_merged[df_merged['category'].isin(top_3_categories)]

    # Group by category and product, sum the quantity sold
    top_products = df_top_categories.groupby(['category', 'product_name'])['quantity'].sum().reset_index()

    # Sort within each category and keep top 10
    top_products = top_products.sort_values(['category', 'quantity'], ascending=[True, False])
    top_products = top_products.groupby('category').head(10)

    st.write("Top 10 products by category:")
    st.dataframe(top_products)

def purchase_frequency(df):
    # Select orders made in 2023
    df_filtered_2023 = df[df['brand_contacted_at_values'].dt.year == 2023]

    # Sort the DataFrame by retailer and timestamp
    df_final_sorted = df_filtered_2023.sort_values(by=['retailer_tokens', 'brand_contacted_at_values'])

    # Calculate the time difference between consecutive orders for each retailer
    df_final_sorted['time_diff'] = df_final_sorted.groupby('retailer_tokens')['brand_contacted_at_values'].diff().dt.days

    # Group by retailer and find the median number of days between orders for every retailer
    median_days_between_orders = df_final_sorted.groupby('retailer_tokens')['time_diff'].median()

    # we filter rows were time_dff is None
    median_days_between_orders = median_days_between_orders[~median_days_between_orders.isna()]

    # we filter rows were time_dff is 0
    median_days_between_orders = median_days_between_orders[median_days_between_orders != 0]

    # we convert this series to a dataframe
    median_days_between_orders = median_days_between_orders.to_frame()

    # use index as column retailer_tokens
    median_days_between_orders.reset_index(inplace=True)

    # Create figure and axis
    fig, ax = plt.subplots()

    # Create histogram
    ax.hist(median_days_between_orders['time_diff'], bins=20, color='skyblue', edgecolor='black')

    # Add labels and title
    ax.set_xlabel('Time Difference (days)')
    ax.set_ylabel('Frequency (Number of retailers)')
    ax.set_title('Distribution of Days between Orders (Orders made in 2023)')

    # Calculate percentiles
    fiftieth_percentile = np.percentile(median_days_between_orders['time_diff'], 50)
    seventy_fifth_percentile = np.percentile(median_days_between_orders['time_diff'], 75)

    # Add percentage annotation
    ax.axvline(x=fiftieth_percentile, color='r', linestyle='--', linewidth=1)
    ax.text(fiftieth_percentile+1, ax.get_ylim()[1]*0.05, '50% of retailers re-order in less than {} days'.format(int(fiftieth_percentile)), rotation=90)

    # Add percentage annotation
    ax.axvline(x=seventy_fifth_percentile, color='r', linestyle='--', linewidth=1)
    ax.text(seventy_fifth_percentile+1, ax.get_ylim()[1]*0.05, '75% of retailers re-order in less than {} days'.format(int(seventy_fifth_percentile)), rotation=90)
    
    # Display chart in Streamlit
    st.pyplot(fig)

def sales_quantiles(df, day_data_was_obtained):
    # we make a copy of the dataframe 
    df = df.copy()

    # Calculate the date 12 months ago from today
    last_12_months_date = day_data_was_obtained - timedelta(days=365)

    # Filter the DataFrame for the last 12 months
    df_last_12_months = df[df['brand_contacted_at_values'] >= last_12_months_date]

    # Determine the column to group by
    group_by_column = 'retailer_tokens'
    if 'retailer_names' in df.columns:
        group_by_column = 'retailer_names'

    # Group by retailer_tokens and sum the payout_total_values for each retailer
    sales_by_retailer = df_last_12_months.groupby(group_by_column)['payout_total_values'].sum().sort_values(ascending=False)

    # we convert this series to a dataframe
    sales_by_retailer = sales_by_retailer.to_frame()

    # we add index as a column
    sales_by_retailer.reset_index(inplace=True)

    # Store quantiles for the specified options
    quantile_options = [0.90, 0.80, 0.70, 0.60, 0.50]
    quantiles_values = []

    for quantile in quantile_options:
        quantiles_values.append(sales_by_retailer['payout_total_values'].quantile(quantile)) 

    # we create a dataframe with the results. I want the quantiles as columns and the values as rows
    quantiles = pd.DataFrame()
    quantiles['quantile'] = quantile_options
    quantiles['value'] = quantiles_values

    # convert column "quantiles" to string
    quantiles['quantile'] = quantiles['quantile'].astype(str)

    # Create figure and axis
    fig, ax = plt.subplots()

    # we create a bar chart using quantile dataframe data
    ax.bar(quantiles['quantile'], quantiles['value'], color='skyblue')

    # Set labels and title
    ax.set_xlabel('Quantile')
    ax.set_ylabel('Sales')
    ax.set_title('Sales by Quantile (Last 12 months)')

    # we add a grid
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # display chart in Streamlit
    st.pyplot(fig)

def product_quantity_sold():
    # Read the CSV data
    df = pd.read_csv("./dashboard/charts/latico_leathers_orders.csv")

    # group by order number and get the total number of orders
    total_orders = df['Order Number'].nunique()

    st.write(f'Total Orders: {total_orders}')

    # Group by Product Name and sum the Quantity
    product_sales = df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).reset_index()

    # Rename the columns for clarity
    product_sales.columns = ['Product', 'Total Quantity Sold']

    st.dataframe(product_sales)

def product_quantity_sold_order_items(df):

    # we take only the last 90 days
    current_date = pd.to_datetime('now')
    last_90_days = current_date - pd.DateOffset(days=90)
    df = df[df['brand_contacted_at_values'] >= last_90_days]
    # Group by Product Name and sum the Quantity
    product_sales = df.groupby('product_name')['quantity'].sum().sort_values(ascending=False).reset_index()

    # Rename the columns for clarity
    product_sales.columns = ['Product', 'Total Quantity Sold']
