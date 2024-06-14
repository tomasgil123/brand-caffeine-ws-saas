import streamlit as st
import pandas as pd

from dashboard.data_scripts.get_marketing_campaign_info import (get_marketing_info)
from dashboard.data_scripts.get_orders import (get_orders_data, get_order_items_data)

from dashboard.charts.email_marketing_charts import (get_email_marketing_kpis_last_30_days, 
                                              get_email_marketing_kpis_by_month, sales_by_month, 
                                              sales_for_quantile, top_10_customers, retailers_did_not_reorder)

from dashboard.recommendations.email_marketing import (get_marketing_recommendations)


from dashboard.utils import ( get_date_from_blob_name)

def create_email_marketing_section(selected_client, type_plan, brand_name_in_faire):

    df_email_marketing, blob_name = get_marketing_info(client_name=selected_client)

    df_orders, _ = get_orders_data(client_name=selected_client)
    # df_order_items, _ = get_order_items_data(client_name=selected_client)

    # id dataframe is empty tell user to click the update button
    if df_email_marketing is None or df_email_marketing.empty or (df_orders is None or df_orders.empty):
        st.write("No email marketing data available. Go to the 'Account' section to update it.")
    
    if blob_name is not None:
        date_last_update = get_date_from_blob_name(blob_name)
        if date_last_update is not None:
            st.write(f"Data last updated at: {date_last_update}")

    if not df_email_marketing.empty and not df_orders.empty:

        date_last_update = pd.to_datetime(date_last_update)

        df_marketing_recommendations, _ = get_marketing_recommendations(client_name=selected_client)

        top_20_customers_without_purchases_last_60_days = df_marketing_recommendations['get_top_20_customers_without_purchases_last_60_days'].values[0]
        customers_without_second_purchase_last_60_days = df_marketing_recommendations['get_customers_without_second_purchase_last_60_days'].values[0]
        sales_for_top_20 = sales_for_quantile(df=df_orders,day_data_was_obtained=date_last_update, quantile=0.8)

        top_10, top_10_revenue_percentage = top_10_customers(df=df_orders, day_data_was_obtained=date_last_update)

        st.markdown("""
                    #### Recommendations:
                    """)
        
        st.markdown(f"""

                There are **{top_20_customers_without_purchases_last_60_days} customers** who belong to the top 20% of your best customers (those who have spent more than \${sales_for_top_20} in the last 12 months), have made a purchase between 60 to 120 days ago,  but have not made a purchase in the last 2 months.

                1 - Create a new segment in Faire for these customers and launch targeted email campaigns to encourage them to start purchasing again.
                
                """)
        st.write("")
        st.markdown(f"""
                    There are **{customers_without_second_purchase_last_60_days} customers** who made a single purchase between 60 to 120 days ago, but have not bought from your store in the last 2 months.

                1 - Create a new segment in Faire for these customers and launch targeted email campaigns to encourage them to make a second purchase.

                2 - Ask them why they didn't buy again and try to understand what happened.
                """)
        st.write("")
        st.markdown(f"""
                    Top **10 customers** accounted for **{top_10_revenue_percentage}%** of your total revenue in the last 12 months.

                    1 - Send personalized emails or direct messages to encourage them to make additional purchases.
                """)

        st.markdown("""
                    #### Data summary:
                    """)
        
        retailers_did_not_reorder(df_orders, date_last_update)

        st.write("Your top 10 customers and how much they spent in the last 12 months:")
        st.dataframe(top_10)
        
        # st.markdown("""
        #         ### Email performance review
        #         Last 30 days:
        #         """)
        # get_email_marketing_kpis_last_30_days(df_email_marketing, date_last_update)

        get_email_marketing_kpis_by_month(df_email_marketing)

        # sales_by_month(df_email_marketing, 'open_based_total_order_value', 'Total Sales Open emails (12 months)', date_last_update)
        # sales_by_month(df_email_marketing, 'click_based_total_order_value', 'Total Sales Click emails (12 months)', date_last_update)