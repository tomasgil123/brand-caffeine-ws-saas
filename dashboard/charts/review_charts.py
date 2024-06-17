import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def get_reviews_orders_ratio_chart(df_monthly_counts):
    df = df_monthly_counts.copy()

    # Calculate percentages
    df['reviewed_percentage'] = df['reviews'] / df['orders'] * 100
    df['not_reviewed_percentage'] = 100 - df['reviewed_percentage']

    # Create a new DataFrame for stacking
    sales_by_source = df[['reviewed_percentage', 'not_reviewed_percentage']]
    sales_by_source.index = pd.to_datetime(df['month'])

    # Normalize data to represent 100% of sales
    bars = sales_by_source_percentage = sales_by_source.div(sales_by_source.sum(axis=1), axis=0) * 100

    # Create figure and axis objects
    fig, ax = plt.subplots()
    # Plot stacked bar chart
    sales_by_source_percentage.plot(kind='bar', stacked=True, ax=ax, color=[ '#FFA07A' , '#ADD8E6'])
    ax.set_xlabel('Orders with Review')
    ax.set_ylabel('Total Orders (%)')
    ax.set_xticklabels(sales_by_source_percentage.index.strftime('%b %Y'), rotation=45)
    ax.legend(['% Orders with review', '% Orders without Review'])
    plt.tight_layout()

    plt.title("Reviews / orders ratio (Last 6 Months)")

    # Add percentages on the bars
    for i in range(len(sales_by_source_percentage)):
        total = 0
        for j in range(len(sales_by_source_percentage.columns)):
            percentage = round(sales_by_source_percentage.iloc[i, j])
            if percentage > 0:
                total += percentage
                ax.text(i, total - (percentage / 2), f'{percentage:.0f}%', ha='center', va='center', color='#3e3c3e')


    # we display the chart in streamlit
    st.pyplot(fig)
