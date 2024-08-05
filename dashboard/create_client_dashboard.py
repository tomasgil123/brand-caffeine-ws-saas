import streamlit as st

from dashboard.account import build_account_dashboard
from dashboard.product_listings_section import create_product_listings_section
from dashboard.email_marketing_section import create_email_marketing_section
from dashboard.competitors_section import create_competitors_section
from dashboard.review_optimization_section import create_review_optimization_section
from dashboard.analytics_section import create_analytics_section

def create_dashboard(selected_client, selected_report, type_plan, brand_name_in_faire):

    if selected_report == "Recommendations summary":
        st.markdown("""
                # Recommendations summary:
                
                #### Email improvements:

                **Re-engagement campaigns**:  
                    
                1 - Target the top 20% of customers who haven't made a purchase in a few months.
                    
                2 - Reach out to customers who made a purchase but haven't made a second one in the last few months.
                    
                **Sell more to your top customers campaigns**:
                    
                1 - For customers that drive 10% to 20% of your revenue just by themselves.
                
                #### Increase Reviews:
                    
                1 -  Ask customers who made a purchase but haven't left a review to do so.
                    
                2 - Encourage the top 20 customers who haven't left a review yet to write one.
                    
                3 - Request reviews from customers who made a purchase in the last 60 days but haven't reviewed their last order, especially if they have left reviews before.
                    
                #### Product Listing Optimization:
                    
                1 - For products with high page views but below-median conversion rates, refresh product imagery, add videos, or adjust pricing to improve conversion rates.
                    
                2 - For products with above-median conversion rates but fewer page views, increase visibility through SEO (update title, description, tags, etc.).
                    
                #### Competitor Spying:
                    
                1 - Optimize fulfillment times, first order minimum and reorder minimums to match or beat competitors.

                """)

    if selected_report == "Account":
        st.markdown("""
                # Account
                """)
        build_account_dashboard(selected_client, brand_name_in_faire)

    if selected_report == "Analytics Panel":
        st.markdown("""
                # Analytics Panel
                """)
        create_analytics_section(selected_client, type_plan, brand_name_in_faire)
        
        
    if selected_report == "Increase Reviews":
        
        st.markdown("""
                # Recommendations for Review Optimization
                """)
        create_review_optimization_section(selected_client)
    
    if selected_report == "Email Improvements":

        st.markdown("""
                # Recommendations to Improve Email Marketing
                """)
        create_email_marketing_section(selected_client, type_plan, brand_name_in_faire)
    
    if selected_report == "Competitor Spying":

        st.markdown("""
                # Recommendations for Outranking Competitors
                """)
        create_competitors_section(selected_client, brand_name_in_faire)

    if selected_report == "Product Listing Optimization":
        
        st.markdown("""
                # Recommendations for Product Listing Optimization
                """)
        create_product_listings_section(selected_client, type_plan)
        
        