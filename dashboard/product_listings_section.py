import streamlit as st

from dashboard.data_scripts.get_product_views import (get_product_views)

from dashboard.charts.product_listings_charts import (generate_page_views_chart_by_category_last_12_months,
                                                generate_pageviews_orders_ratio_chart, 
                                                generate_page_views_evolution_last_12_months_by_category,
                                                generate_page_views_and_ratio_by_category_with_selector, 
                                                generate_conversion_rate_chart_by_category,
                                                generate_page_views_and_ratio_by_product_with_selector)

from dashboard.global_utils import (get_date_from_blob_name)

from dashboard.recommendations.product_listings import get_product_listings_recommendations

def create_product_listings_section(selected_client, type_plan):
    df_page_views, blob_name = get_product_views(client_name=selected_client)

    # id dataframe is empty tell user to click the update button
    if df_page_views is None or df_page_views.empty:
        st.write("No product listings data available. Go to the 'Account' section to update it.")

    if blob_name is not None:
        date_last_update = get_date_from_blob_name(blob_name)
        if date_last_update is not None:
            st.write(f"Data last updated at: {date_last_update}")
    
    
    if not df_page_views.empty:


        top_category, sales_percentage_top_category, product_most_page_views_worst_conversion_rate, product_least_page_views_best_conversion_rate = get_product_listings_recommendations(selected_client)
        

        if product_most_page_views_worst_conversion_rate.empty or product_least_page_views_best_conversion_rate.empty:
            st.write("No product listings recommendations available. Go to the 'Account' section to update it.")
            return
        else:


            product_most_page_views_worst_conversion_rate_rounded = round(product_most_page_views_worst_conversion_rate['Conversion rate'], 2)
            product_least_page_views_best_conversion_rate_rounded = round(product_least_page_views_best_conversion_rate['Conversion rate'], 2)
            sales_percentage_top_category_rounded = round(sales_percentage_top_category, 2)

            st.markdown("""
                    #### Customized Recommendations:
                    """)
            
            st.markdown(f"""

                Your top product category is **{top_category}**. This category represents **{sales_percentage_top_category_rounded}%** of your total sales in the last 12 months.
                Its is interesting to note that some products have high amount of page views compared to other products in the same category, yet their conversion rates tend to fall below the category median. Conversely, some products with the highest conversion rates often receive the lowest page views.

                1 - For products like **{product_most_page_views_worst_conversion_rate['name']}** that have the most page views but below median conversion rate ({product_most_page_views_worst_conversion_rate_rounded}% in this case), refresh product imagery, add videos, or adjust pricing to experiment with improving conversion rates.

                2 - For products like **{product_least_page_views_best_conversion_rate['name']}** that have a conversion rate above the median ({product_least_page_views_best_conversion_rate_rounded}% in this case), but the not so many page views, increase visibility through SEO (updating title, description, tags, etc.).

                """)
            
            st.markdown("""
                    #### Traits of a Top Shop:
                    """)
            
            st.markdown(f"""
                    1 - Assure your top 10 best-selling products have video content. [Here is a helpful article](https://www.faire.com/blog/selling/how-to-use-video-in-your-brands-marketing/).
                        
                    2 - Make sure all of your initial product photos are on simple, white backgrounds. [You can find the Faire do’s + don’ts here](https://www.faire.com/support/articles/360016568092). (And make sure you have two photos or more for each product.)
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
        st.write(f"All products in the {top_category} category, along with their page views and conversion rates over the past 12 months.")
        generate_pageviews_orders_ratio_chart(data_original=df_page_views, date_last_update=date_last_update, top_category=top_category)
        st.write("")
        st.write("")
        st.write(f"Select a product from category {top_category} to see how its page views and conversion rate evolved over the past 12 months.")
        generate_page_views_and_ratio_by_product_with_selector(data_original=df_page_views, top_category=top_category)