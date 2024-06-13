
def get_main_attributes(df_competitors):

    df_competitors = df_competitors.copy()
    # Calculating the average lead time
    df_competitors["Fulfillment Times"] = df_competitors[["Upper Bound Lead Time Days", "Lower Bound Lead Time Days"]].mean(axis=1)

    # we keep only column "Fulfillment Times", "Number of Reviews", "First Order Minimum Amount" and "Reorder Minimum Amount"
    df_competitors = df_competitors[["Brand Name", "Fulfillment Times", "Number of Reviews", "First Order Minimum Amount", "Reorder Minimum Amount"]]

    return df_competitors

def get_brand_values(df_competitors):

    df_competitors = df_competitors.copy()
    
    # we keep only columns Sold on Amazon	Eco-Friendly	Hand-Made	Charitable	Organic	Woman Owned	Small Batch
    df_competitors = df_competitors[["Brand Name", "Sold on Amazon", "Eco-Friendly", "Hand-Made", "Charitable", "Organic", "Woman Owned", "Small Batch"]]

    return df_competitors
