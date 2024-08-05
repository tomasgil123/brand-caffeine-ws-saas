import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from dashboard.charts.competitors_charts_utils import (get_main_attributes)

def plot_radar_chart(data, metrics, labels, title):
    N = len(metrics)
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    theta = np.concatenate([theta, [theta[0]]])
    
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': 'polar'})
    
    ax.set_title(title, y=1.15, fontsize=20)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(90)
    ax.spines['polar'].set_zorder(1)
    ax.spines['polar'].set_color('lightgrey')
    
    color_palette = ['#339F00', '#0500FF', '#9CDADB', '#FF00DE', '#FF9900', '#FFFFFF']
    
    scales = [(data[metric].min(), data[metric].max()) for metric in metrics]
    
    for idx, (i, row) in enumerate(data.iterrows()):
        values = row[metrics].values.flatten().tolist()
        values = values + [values[0]]
        ax.plot(theta, values, linewidth=1.75, linestyle='solid', label=labels[idx], marker='o', markersize=10, color=color_palette[idx % len(color_palette)])
        ax.fill(theta, values, alpha=0.50, color=color_palette[idx % len(color_palette)])
    
    max_scale = max([max(scale) for scale in scales])
    y_ticks = np.linspace(0, max_scale, num=5)
    
    plt.yticks(y_ticks, [str(int(y_tick)) for y_tick in y_ticks], color="black", size=12)
    plt.xticks(theta, metrics + [metrics[0]], color='black', size=12)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1)) 
    
    return fig


def plot_radar_chart_competitors(df_competitors):

    df_competitors = get_main_attributes(df_competitors)

    # we normalize the different columns
    for column in df_competitors.columns[1:]:
        df_competitors[column] = df_competitors[column] / df_competitors[column].max()

    metrics = df_competitors.columns[1:].tolist()

    labels = df_competitors['Brand Name'].tolist()

    fig = plot_radar_chart(df_competitors, metrics, labels, 'Main Attributes Comparison')

    st.pyplot(fig)

def number_reviews_per_brand(df_competitors, highlight_brand):

    df_competitors = df_competitors.copy()
    df_sorted = df_competitors.sort_values(by="Number of Reviews", ascending=False)

    fig, ax = plt.subplots()

    # Set the title and labels for the chart displaying the number of reviews
    ax.set_xlabel('Brand')
    ax.set_ylabel('Number of Reviews per brand')

    # Plot the number of reviews as a bar chart
    bars = ax.bar(df_sorted["Brand Name"], df_sorted["Number of Reviews"], color='#ADD8E6')

    # Customize the appearance of the chart
    plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
    plt.title('Total Reviews per Brand', loc='left')

    # Highlight the specific brand by changing the color of its bar
    for bar, brand in zip(bars, df_sorted["Brand Name"]):
        if brand == highlight_brand:
            bar.set_color('#4682B4')  # Change this to any color you prefer

    # Display the chart in your Streamlit app
    st.pyplot(fig)


def get_competitors_minimum_order_data(data, target_brand):
    data = data.copy()
    # sort in ascending order by first order minimum amount
    data = data.sort_values(by='First Order Minimum Amount', ascending=True)
    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()

    # Set x-axis labels to be the Brand Names
    brand_names = data['Brand Name']
    x = range(len(brand_names))

    # Plot First Order Minimum Amount
    first_order_min = data['First Order Minimum Amount']
    reorder_min = data['Reorder Minimum Amount']

    for idx in x:
        if brand_names.iloc[idx] == target_brand:
            color_first_order = '#4682B4'
            color_reorder = 'orange'
        else:
            color_first_order = '#ADD8E6'  # Light blue
            color_reorder = '#FFA07A'     # Light orange

        ax.bar(idx - 0.125, first_order_min.iloc[idx], width=0.25, color=color_first_order, label='First Order Minimum Amount' if idx == 0 else "")
        ax.bar(idx + 0.125, reorder_min.iloc[idx], width=0.25, color=color_reorder, label='Reorder Minimum Amount' if idx == 0 else "")

    # Set x-axis labels and legend
    ax.set_xticks(x)
    ax.set_xticklabels(brand_names, rotation=45, ha='right')
    ax.legend()

    # Set labels and title
    ax.set_xlabel('Brand Name')
    ax.set_ylabel('Amount')

    plt.title('First Order and Reorder Minimum Amount per Brand', loc='left')

    st.pyplot(fig)

def get_competitors_fulfillment_data(data, special_brand):
    # Make a copy of the data
    data = data.copy()
    data.sort_values(by='Upper Bound Lead Time Days', ascending=True, inplace=True)
    
    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()

    # Set x-axis labels to be the Brand Names
    brand_names = data['Brand Name']
    x = range(len(brand_names))

    # Define colors
    color_first_order_normal = '#ADD8E6'  # Light blue
    color_reorder_normal = '#FFA07A' 
    color_first_order_special = '#4682B4'
    color_reorder_special = 'orange'

    # Plot Upper Bound Lead Time Days and Lower Bound Lead Time Days
    for i, brand in enumerate(brand_names):
        upper_lead_time = data.iloc[i]['Upper Bound Lead Time Days']
        lower_lead_time = data.iloc[i]['Lower Bound Lead Time Days']
        
        if brand == special_brand:
            color_first_order = color_first_order_special
            color_reorder = color_reorder_special
        else:
            color_first_order = color_first_order_normal
            color_reorder = color_reorder_normal
        
        ax.bar(i, upper_lead_time, width=0.4, label='Upper Bound Lead Time Days' if i == 0 else "", align='center', color=color_first_order)
        ax.bar(i, lower_lead_time, width=0.4, label='Lower Bound Lead Time Days' if i == 0 else "", align='edge', color=color_reorder)

    # Set x-axis labels and legend
    ax.set_xticks(x)
    ax.set_xticklabels(brand_names, rotation=45, ha='right')
    ax.legend()

    # Set labels and title
    ax.set_xlabel('Brand Name')
    ax.set_ylabel('Lead Time Days')

    plt.title('Fulfillment speed per Brand', fontsize=13, loc='left', pad=12, fontweight=500, color="#31333f", fontfamily="Microsoft Sans Serif")

    # Display the chart using Streamlit
    st.pyplot(fig)

def get_brands_best_sellers(df, highlight_brand, main_category):
    # Count the number of bestsellers per brand
    faire_bestseller_count = df[df["Badge List"] == "FAIRE_BESTSELLER"].groupby("Brand Name").size()
    faire_bestseller_count = faire_bestseller_count.reset_index()
    faire_bestseller_count.columns = ["Brand Name", "Bestseller Count"]

    # Sort the brands in descending order based on the number of bestsellers
    faire_bestseller_count = faire_bestseller_count.sort_values(by="Bestseller Count", ascending=False)

    # Create matplotlib chart
    fig, ax = plt.subplots()
    bars = ax.bar(faire_bestseller_count["Brand Name"], faire_bestseller_count["Bestseller Count"], color='#ADD8E6')

    # Highlight the specific brand with a different color
    for bar, brand in zip(bars, faire_bestseller_count["Brand Name"]):
        if brand == highlight_brand:
            bar.set_color('#4682B4')

    # Set the title and labels for the chart displaying the number of bestsellers
    ax.set_xlabel('Brand')
    ax.set_ylabel(f'Number of Bestsellers')
    ax.set_xticklabels(faire_bestseller_count["Brand Name"], rotation=45, ha='right')
    plt.title(f'Number of Bestsellers per Brand for Category {main_category}', loc='left')

    # Display the chart in your Streamlit app
    st.pyplot(fig)

def get_brands_new_products(df, highlight_brand, main_category):
    # Create a list of all unique brand names
    all_brands = df["Brand Name"].unique()

    # Count the number of new products per brand
    new_products_count = df[df["Is New"] == True].groupby("Brand Name").size()
    new_products_count = new_products_count.reindex(all_brands, fill_value=0).reset_index()
    new_products_count.columns = ["Brand Name", "New Product Count"]

    # Sort the brands in descending order based on the number of new products
    new_products_count = new_products_count.sort_values(by="New Product Count", ascending=False)

    # Create matplotlib chart
    fig, ax = plt.subplots()
    bars = ax.bar(new_products_count["Brand Name"], new_products_count["New Product Count"], color='#ADD8E6')

    # Highlight the specific brand with a different color
    for bar, brand in zip(bars, new_products_count["Brand Name"]):
        if brand == highlight_brand:
            bar.set_color('#4682B4')

    # Set the title and labels for the chart displaying the number of new products
    ax.set_xlabel('Brand')
    ax.set_ylabel('Number of New Products')
    ax.set_xticklabels(new_products_count["Brand Name"], rotation=45, ha='right')
    plt.title(f'Number of New Products per Brand for Category {main_category}', loc='left')

    # Display the chart in your Streamlit app
    st.pyplot(fig)