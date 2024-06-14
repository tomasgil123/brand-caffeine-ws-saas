
from dashboard.data_scripts.get_product_views import (get_product_views)

from dashboard.utils.product_listings import (get_category_with_most_sales, get_products_to_improve)
from dashboard.global_utils import ( get_date_from_blob_name)

from dashboard.data_scripts.get_orders import (get_orders_data, get_order_items_data)

def get_product_listings_recommendations(selected_client):

    df_page_views, blob_name = get_product_views(client_name=selected_client)
    df_orders, _ = get_orders_data(client_name=selected_client)
    df_order_items, _ = get_order_items_data(client_name=selected_client)

    top_category, sales_percentage_top_category = get_category_with_most_sales(df_orders, df_order_items, df_page_views)

    date_last_update = get_date_from_blob_name(blob_name)
    product_most_page_views_worst_conversion_rate, product_least_page_views_best_conversion_rate = get_products_to_improve(data_original=df_page_views, date_last_update=date_last_update, selected_category=top_category)
    
    return top_category, sales_percentage_top_category, product_most_page_views_worst_conversion_rate, product_least_page_views_best_conversion_rate