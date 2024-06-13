import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

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
    last_12_months_date = day_data_was_obtained - timedelta(days=365)

    # Filter the DataFrame for the last 12 months
    df_last_12_months = df[df['brand_contacted_at_values'] >= last_12_months_date]

    # Filter by 'very_first_order_for_brand_values' equal to True
    df_filtered_very_first = df_last_12_months[df_last_12_months['very_first_order_for_brand_values'] | df_last_12_months['first_order_for_brand_values']]

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
    ax.set_title('Percentage of Retailers with Only One Order (last 12 months)')
    
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
    sales_by_retailer = df_last_12_months.groupby(group_by_column)['payout_total_values'].sum().sort_values(ascending=False)

    # Convert this series to a dataframe
    sales_by_retailer = sales_by_retailer.to_frame()

    # Add index as a column
    sales_by_retailer.reset_index(inplace=True)

    # Calculate top 10 customers
    top_10_customers = sales_by_retailer.head(10)

    # Calculate total revenue
    total_revenue = sales_by_retailer['payout_total_values'].sum()

    # Calculate revenue percentage for the top 10 customers
    top_10_revenue = top_10_customers['payout_total_values'].sum()
    top_10_revenue_percentage = round((top_10_revenue / total_revenue) * 100, 2)

    return top_10_customers, top_10_revenue_percentage