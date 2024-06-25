import streamlit as st

from dashboard.data_scripts.get_reviews import get_reviews_data
from dashboard.data_scripts.get_orders import get_orders_data
from dashboard.recommendations.reviews import get_review_recommendations

from dashboard.charts.review_charts import get_reviews_orders_ratio_chart
from dashboard.utils.reviews import (get_reviews_orders_ratio, calculate_avg_ratio_and_total_reviews,
                                    get_retailers_with_reviews_purchase_last_60_days)

from dashboard.global_utils import (get_date_from_blob_name)

def create_review_optimization_section(selected_client):

    df_reviews, blob_name = get_reviews_data(client_name=selected_client)

    # id dataframe is empty tell user to click the update button
    if df_reviews is None or df_reviews.empty:
        st.write("No reviews data available. Go to the 'Account' section to update it.")

    if blob_name is not None:
        date_last_update = get_date_from_blob_name(blob_name)
        if date_last_update is not None:
            st.write(f"Data last updated at: {date_last_update}")

    if not df_reviews.empty:

        df_recommendations, blob_name = get_review_recommendations(client_name=selected_client)

        customers_with_purchase_last_60_days_no_review = df_recommendations['get_customers_with_purchase_last_60_days_no_review'].values[0]

        # we get max and min value of column "order_amount"
        max_order_amount = df_recommendations['order_amount'].max()
        min_order_amount = df_recommendations['order_amount'].min()

        df_orders, _ = get_orders_data(client_name=selected_client)

        df_monthly_counts = get_reviews_orders_ratio(df_orders, df_reviews, date_last_update)

        avg_ratio, total_reviews, total_orders = calculate_avg_ratio_and_total_reviews(dataframe=df_monthly_counts, reference_date=date_last_update)

        df_retailers_with_reviews = get_retailers_with_reviews_purchase_last_60_days(df_orders, df_reviews, date_last_update)

        number_retailers_with_reviews = df_retailers_with_reviews.shape[0]

        st.markdown("""
                    #### Customized Recommendations:
                    """)
        
        st.markdown(f"""
                    
            Given that the **average ratio of reviews to orders** in the last three months is **{round(avg_ratio*100)}%** (your store only got {total_reviews} reviews out of {total_orders} orders), we recommend the following actions:
            
            1 - Create a new segment in Faire for customers that have made a purchase in the last 60 days but haven't left a review yet (**{customers_with_purchase_last_60_days_no_review} customers** match that condition) and launch targeted email campaigns to encourage them to leave a review.

            2 - Send direct messages to the top 20 customers (find the complete list in the recommendation details section) that have made a purchase in the last 60 days but haven't left a review yet. These customers have spent beetween \${round(min_order_amount)} to \${round(max_order_amount)} since they become customers, indicating a strong trust in your brand and a higher likelihood of leaving a review.

            There are **{number_retailers_with_reviews} customers** that made a purchase in the last 60 days and haven't left a review for their last order, but have left one or more reviews before. They have already made a review so they are more likely to leave another one. You can find the complete list in the recommendation details section.

            1 - Send a direct message to these customers asking them to leave a review again.
                    
                    """)
        
        st.markdown("""
                    #### Traits of a Top Shop:
                    """)
        st.markdown(f"""
                    1 - Reviews are KEY to Seller success - and we ALWAYS recommend reaching out via Direct Message to request them. But you’ve only got 90 days after the order is delivered to do this. [Here’s what Faire recommends](https://www.faire.com/support/articles/360030186831).
                """)
        
        st.write("")
        st.write("")
        st.write("Need help putting these recommendations into action?")
        st.markdown('<a href="https://calendly.com/benschreiberbrandcaffeine/15min-faire-growth-intro-clone-1" class="consultation-button" target="_blank">Book a free expert consultation</a>', unsafe_allow_html=True)
        st.write("")
        st.write("")
        
        st.markdown("""
                    #### Recommendation Details:
                    """)
        
        st.write("How the ratio reviews / orders evolved over the last 6 months:")
        get_reviews_orders_ratio_chart(df_monthly_counts)

        st.write("Retailers that made a purchase in the last 60 days and haven't left a review for their last order, but have left one or more reviews before:")

        df_retailers_with_reviews.columns = ['Retailer Name', 'Review Count', 'Send a DM']

        st.write(df_retailers_with_reviews.to_html(escape=False, index=False), unsafe_allow_html=True)

        