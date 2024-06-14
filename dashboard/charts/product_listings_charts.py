import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from datetime import datetime, timedelta

def generate_page_views_chart_by_category_last_12_months(data, date_last_update):

    data = data.copy()

    # Convert 'date' column to datetime format
    data['date'] = pd.to_datetime(data['date'])

    # Filter the data for the last 12 months
    today = pd.to_datetime(date_last_update)
    last_12_months_start = today - timedelta(days=365)
    last_12_months_data = data[(data['date'] >= last_12_months_start) & (data['date'] <= today)]

    # Group the data by the 'category' column and calculate the sum of 'visit_count'
    category_views_last_12_months = last_12_months_data.groupby('category')['visit_count'].sum().reset_index()

    # Sort the DataFrame by 'visit_count' in descending order
    category_views_last_12_months = category_views_last_12_months.sort_values(by='visit_count', ascending=False)

    # Select only the top 15 categories
    top_15_categories = category_views_last_12_months.head(15)

    # Create a bar chart using matplotlib
    plt.figure()
    plt.bar(top_15_categories['category'], top_15_categories['visit_count'])
    plt.xlabel('Product Category')
    plt.ylabel('Total Visit Count')
    plt.xticks(rotation=45, ha='right')

    plt.title("Total Page Views by Product Category (Last 12 Months)", fontsize=13, loc='left', pad=20, fontweight=500, color="#31333f", fontfamily="Microsoft Sans Serif")

    st.pyplot(plt)

def generate_page_views_evolution_last_12_months_by_category(data):
    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'])

    default_category = data['category'].unique()[0]
    # Sidebar for category selection
    selected_categories = st.multiselect("Select categories", data['category'].unique(), default_category)

    # Filter data based on selected categories
    filtered_data = data[data['category'].isin(selected_categories)]

    # Group data by month and sum sales_count
    grouped_data = filtered_data.groupby(['category', pd.Grouper(key='date', freq='M')]).sum().reset_index()

    # Filter data for the last 12 months
    last_12_months = grouped_data[grouped_data['date'] >= grouped_data['date'].max() - pd.DateOffset(months=11)]

    # Plot the data
    fig, ax = plt.subplots()
    for category, category_data in last_12_months.groupby('category'):
        ax.plot(category_data['date'].dt.strftime('%Y/%m'), category_data['visit_count'], marker='o', linestyle='-', label=category)

    # Customize the plot
    ax.set_title("Evolution of Page Views by Category (Last 12 Months)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.grid(True)
    ax.legend()
    plt.xticks(rotation=45, ha='right')

    # Display the plot
    st.pyplot(fig)
    

def generate_page_views_chart_by_product_last_12_months(data_original, date_last_update):

    data = data_original.copy()

    # Convert 'date' column to datetime type if not already done
    if not isinstance(data['date'], pd.DatetimeIndex):
        data['date'] = pd.to_datetime(data['date'])

    # Filter data for the last 12 months
    end_date = date_last_update
    start_date = end_date - timedelta(days=365)
    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

    options = filtered_data['category'].unique()
    default_index = 0  # Assuming the first category is the default

    selected_category = st.selectbox(
        "Select Product Category",
        options,
        key="generate_page_views_chart_by_product",
        index=default_index
    )

    # Filter data for the selected category
    filtered_data = filtered_data[filtered_data['category'] == selected_category]

    # Group the filtered data by 'name' column and calculate the sum of 'visit_count'
    product_views_last_12_months = filtered_data.groupby('name')['visit_count'].sum().reset_index()

    # Sort the DataFrame by 'visit_count' in descending order
    product_views_last_12_months = product_views_last_12_months.sort_values(by='visit_count', ascending=False)

    # Take top 12 products by visit count
    top_products = product_views_last_12_months.head(12)

    # Create a bar chart using matplotlib
    plt.figure()
    plt.bar(top_products['name'], top_products['visit_count'])
    plt.xlabel('Product Name')
    plt.ylabel('Total Page Views')
    plt.xticks(rotation=45, ha='right')

    plt.title("Total Page Views by Product (Last 12 Months)", fontsize=13, loc='left', pad=20, fontweight=500, color="#31333f", fontfamily="Microsoft Sans Serif")

    # Display the chart in your Streamlit app
    st.pyplot(plt)

def generate_conversion_rate_chart_by_category(data_original, date_last_update):

    data = data_original.copy()
    # Calculate the date range for the last 12 months
    end_date = pd.to_datetime(date_last_update)
    start_date = end_date - timedelta(days=365)
    
    # Filter data for the last 12 months
    data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

    # Calculate total page views for each product category
    category_views_orders = data.groupby('category').agg({'visit_count': 'sum', 'order_count': 'sum'}).reset_index()
    category_views_orders = category_views_orders.rename(columns={'visit_count': 'Page views', 'order_count': 'Orders'})
    
    # Filter categories with at least 500 total page views
    categories_with_500_views = category_views_orders[category_views_orders['Page views'] >= 500]

    # Check if there are more than 5 categories
    if len(categories_with_500_views) > 5:
        # Filter categories with at least 500 total page views
        category_views_orders = category_views_orders[category_views_orders['Page views'] >= 500]
    else:
        # we keep 10 categories with most views
        category_views_orders = category_views_orders.sort_values(by='Page views', ascending=False).head(10)

    # Calculate the ratio of Page views to Orders
    category_views_orders['Conversion'] = (category_views_orders['Orders'] / category_views_orders['Page views'])*100

    # Sort the DataFrame by the ratio in descending order
    category_views_orders = category_views_orders.sort_values(by='Conversion', ascending=False)

    # Create a bar chart using matplotlib
    plt.figure()
    plt.bar(category_views_orders['category'], category_views_orders['Conversion'])
    plt.xlabel('Product Category')
    plt.ylabel('Conversion Rate')
    plt.xticks(rotation=45, ha='right')

    # Add % symbol to y-axis tick labels
    fmt = '%.0f%%'  # Format as percentage with no decimal places
    plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: fmt % x))


    plt.title("Conversion Rate by Product Category (Descending Order, >= 500 Total Views)", fontsize=13, loc='left', pad=20, fontweight=500, color="#31333f", fontfamily="Microsoft Sans Serif")

    # Display the chart in your Streamlit app
    st.pyplot(plt)

def generate_pageviews_orders_ratio_chart(data_original, date_last_update, top_category):
    data = data_original.copy()
    # Calculate the date range for the last 12 months
    end_date = pd.to_datetime(date_last_update)
    start_date = end_date - timedelta(days=365)
    
    # Filter data for the last 12 months
    data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

    # Calculate the total page views for each product
    total_page_views = data[data['category'] == top_category].groupby('name')['visit_count'].sum().reset_index()

    # Sort the products by Page views in descending order
    total_page_views = total_page_views.sort_values(by='visit_count', ascending=False)

    # Keep only the top 12 products
    filtered_products = total_page_views.head(12)['name']

    # Filter the original data to keep only the selected products
    filtered_data = data[data['name'].isin(filtered_products) & (data['category'] == top_category)]
    # Group by 'name' and aggregate the sum of 'visit_count', 'order_count', and 'sales_count'
    grouped_df = filtered_data.groupby('name').agg({
        'visit_count': 'sum',
        'order_count': 'sum',
        'sales_count': 'sum'
    }).reset_index()

    # Calculate the ratio of Page views to Orders
    grouped_df['Conversion rate'] =  (grouped_df['order_count']/grouped_df['visit_count'])*100

    # Sort the DataFrame by the ratio in descending order
    grouped_df = grouped_df.sort_values(by='Conversion rate', ascending=False)

    # Create the Matplotlib chart
    fig, ax1 = plt.subplots()

    # Plot 'visit_count' on the primary y-axis
    ax1.bar(grouped_df['name'], grouped_df['Conversion rate'], label='Conversion rate')
    ax1.set_xlabel('Product name')
    ax1.set_ylabel('Conversion rate')
    ax1.tick_params(axis='y')
    plt.xticks(rotation=45, ha='right')

    # Format y-axis labels to display '%' symbol
    fmt = '%.1f%%'  # Format as percentage with no decimal places
    ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: fmt % x))

    # Create a secondary y-axis for 'Page views'
    ax2 = ax1.twinx()
    ax2.plot(grouped_df['name'], grouped_df['visit_count'], linestyle='--', marker='x', color='tab:orange', label='Page views')
    ax2.set_ylabel('Page views')
    ax2.tick_params(axis='y')

    # Customize the chart
    plt.title(f"Page Views and Conversion Rate for {top_category} Products")

    # Set the y-axis limits to start from 0
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)

    # Add grid to the y-axis
    ax1.grid(axis='y')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Display the chart in your Streamlit app
    st.pyplot(plt)

    mean = grouped_df['Conversion rate'].mean()
    rounded_mean = round(mean, 2)
    median = grouped_df['Conversion rate'].median()
    rounded_median = round(median, 2)

    st.markdown(f"""
    {top_category} Median: {rounded_median} %
    """, unsafe_allow_html=True)

def generate_page_views_and_ratio_by_category_with_selector(data_original):

    data = data_original.copy()

    # Create a selectbox for category selection with default value
    selected_category = st.selectbox(
        "Select Category",
        data['category'].unique(),
        key="generate_page_views_and_ratio_by_category_with_selector"
    )

    # Filter the data based on selected category
    filtered_data = data[data['category'] == selected_category]

    # Create a line chart using matplotlib
    fig, ax1 = plt.subplots()

    for category, group in filtered_data.groupby('category'):
        group = group.groupby('date').agg({'visit_count': 'sum', 'order_count': 'sum'})
        group['Conversion'] = group.apply(lambda row:  (row['order_count'] / row['visit_count'])*100 if row['order_count'] > 0 else 0, axis=1)
        ax1.plot(group.index, group['visit_count'], label=f'{category} Page Views', marker='o')
        
        # Add a secondary y-axis for Page views / Orders
        ax2 = ax1.twinx()
        ax2.plot(group.index, group['Conversion'], label=f'{category} Conversion Rate', linestyle='--', marker='x', color='tab:orange')

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Page Views', color='tab:blue')
    ax1.legend(loc='upper left')
    
    ax2.set_ylabel('Conversion Rate', color='tab:orange')
    ax2.legend(loc='upper right')

    # Set the y-axis limits to start from 0
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)

    fmt = '%.0f%%'  # Format as percentage with no decimal places
    ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: fmt % x))

    # Customize the chart
    plt.title("Conversion Rate Evolution by Category", fontsize=13, loc='left', pad=20, fontweight=500, color="#31333f", fontfamily="Microsoft Sans Serif")
    
    # Add grid to the x-axis
    ax1.grid(True, which='major', axis='both', linestyle='--')

    # Display the plot using Streamlit
    st.pyplot(fig)
    
def generate_page_views_and_ratio_by_product_with_selector(data_original, top_category):
    
    # Create a copy of the original data
    data = data_original.copy()
    
    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # we filter data by top_category
    data = data[data['category'] == top_category]

    # we keep only the 12 products with most page views in the category
    top_products = data.groupby('name')['visit_count'].sum().sort_values(ascending=False).head(12).index

    # we filter data by top_products
    data = data[data['name'].isin(top_products)]
    
    # Find the default selected product with the most visits in 2023
    most_viewed_product = data.loc[data['date'].dt.year == 2023].groupby('name')['visit_count'].sum().idxmax()

    # Create a selectbox for product selection with default value
    selected_product = st.selectbox(
        "Select Product",
        sorted(data['name'].unique()),
        key="generate_page_views_and_ratio_by_product_with_selector",
        index=sorted(data['name'].unique()).index(most_viewed_product)
    )

    # Filter data for selected product
    filtered_data = data[data['name'] == selected_product]

    # Resample data on a monthly basis
    monthly_data = filtered_data.resample('M', on='date').agg({'visit_count': 'sum', 'order_count': 'sum'})
    monthly_data['Conversion'] = monthly_data.apply(lambda row: (row['order_count'] / row['visit_count'])*100  if row['order_count'] > 0 else 0, axis=1)
    # Add a 'Date' column to the DataFrame
    monthly_data['Date'] = monthly_data.index
    # Change date format to YYYY/MM
    monthly_data['Date'] = monthly_data['Date'].dt.strftime("%Y-%m")

    # Create the Matplotlib chart
    fig, ax1 = plt.subplots()

    # Plot 'Page views' on the primary y-axis
    ax1.plot(monthly_data['Date'], monthly_data['visit_count'], marker='o', label='Page Views')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Page views')
    plt.xticks(rotation=45, ha='right')

    # Create a secondary y-axis for 'PageViews/Orders Ratio'
    ax2 = ax1.twinx()
    ax2.plot(monthly_data['Date'], monthly_data['Conversion'], linestyle='--', marker='x', color='tab:orange', label='Conversion Rate')
    ax2.set_ylabel('Conversion Rate')

    # Set the y-axis limits to start from 0
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)

    fmt = '%.0f%%'  # Format as percentage with no decimal places
    ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: fmt % x))

    # Add grid to the x-axis
    ax1.grid(True, which='major', axis='both', linestyle='--')

     # Customize the chart
    plt.title("Conversion Rate Evolution by Product", fontsize=13, loc='left', pad=20, fontweight=500, color="#31333f", fontfamily="Microsoft Sans Serif")

    plt.legend()
    st.pyplot(plt)


def sales_by_category(df_orders, df_order_items, df_page_views):

    # we keep only orders of the last 12 months
    current_date = pd.to_datetime('now')
    one_year_ago = current_date - pd.DateOffset(months=12)
    df_orders = df_orders[df_orders['brand_contacted_at_values'] >= one_year_ago]

    # we merge df_order_items with df_page_views on column "product_token". We only want to add column "category"
    df_page_views = df_page_views[['product_token', 'category']]
    df_order_items = pd.merge(df_order_items, df_page_views, left_on=["product_token"], right_on=["product_token"])

    # we merge df_orders with df_order_items on column "brand_order_token"
    df_orders_merged = pd.merge(df_orders, df_order_items, left_on=["tokens"], right_on=["brand_order_token"])

    # create a bar chart with categories 0n the x axis and percentage of sales on the y axis
    # Group by category and sum the quantity sold
    sales_by_category = df_orders_merged.groupby('category')['retailer_price'].sum()

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