import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from dashboard.data_scripts.get_product_views import (get_product_views)

from dashboard.data_scripts.get_marketing_campaign_info import (get_marketing_info)
from dashboard.data_scripts.get_orders import (get_orders_data, get_order_items_data)

from dashboard.charts.email_marketing_charts import (get_email_marketing_kpis_last_30_days,  
                                              get_email_marketing_kpis_by_month, sales_by_month, percentage_revenue_store_type, 
                                              sales_for_quantile, top_10_customers, retailers_did_not_reorder, 
                                              retailers_did_not_reorder_month_over_month, percentage_revenue_store_type_by_month,
                                              avg_order_value_by_store_type, top_products_by_type_of_store, purchase_frequency, sales_by_category,
                                              sales_quantiles, product_quantity_sold, top_retailers_did_not_reorder_month_over_month, 
                                              top_10_products_last_90_days, top_10_products_by_category_last_90_days)

from dashboard.recommendations.email_marketing import (get_marketing_recommendations)

from dashboard.global_utils import ( get_date_from_blob_name)

def create_analytics_section(selected_client, type_plan, brand_name_in_faire):

    df_page_views, _ = get_product_views(client_name=selected_client)

    df_email_marketing, blob_name = get_marketing_info(client_name=selected_client)

    df_orders, _ = get_orders_data(client_name=selected_client)

    df_order_items, _ = get_order_items_data(client_name=selected_client)

    if blob_name is not None:
        date_last_update = get_date_from_blob_name(blob_name)
        if date_last_update is not None:
            st.write(f"Data last updated at: {date_last_update}")

    date_last_update = datetime.strptime(date_last_update, '%Y-%m-%d')

    st.markdown("""
                ### Email marketing overview
                """)
    
    get_email_marketing_kpis_last_30_days(df_email_marketing, date_last_update)

    get_email_marketing_kpis_by_month(df_email_marketing)

    sales_by_month(df_email_marketing, 'open_based_total_order_value', 'Total Sales Open emails (12 months)', date_last_update)
    sales_by_month(df_email_marketing, 'click_based_total_order_value', 'Total Sales Click emails (12 months)', date_last_update)

    st.markdown("""
                ### Re-engagement data
                """)
    
    retailers_did_not_reorder_month_over_month(df_orders)

    sales_for_top_20 = sales_for_quantile(df=df_orders,day_data_was_obtained=date_last_update, quantile=0.8)

    start_date_str = "04-2024"
    top_retailers_did_not_reorder_month_over_month(df_orders, start_date_str, sales_for_top_20)

    percentage_revenue_store_type(df_orders)

    percentage_revenue_store_type_by_month(df_orders)

    avg_order_value_by_store_type(df_orders)

    top_products_by_type_of_store(df_orders, df_order_items)

    top_10_products_last_90_days(df_orders, df_order_items)

    top_10_products_by_category_last_90_days(df_orders, df_order_items, df_page_views)

    #product_quantity_sold()

    #purchase_frequency(df_orders)

    st.write("sales_by_category")

    sales_by_category(df_orders, df_order_items, df_page_views)

    sales_quantiles(df_orders, date_last_update)

    # que es lo que quiero ver?
    # quiero ver que onda cada campana de email marketing. Las campanas de marketing van a estar clasificadas en grupos:

    # - Re-engagement campaigns
    # - Sell more to your top customers campaigns
    # - Sell more by store type campaigns