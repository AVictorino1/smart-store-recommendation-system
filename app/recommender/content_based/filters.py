import pandas as pd


def price_filter(product_index, df):
    product = df.loc[product_index]
    filtered = df[(df["price"] >= 0.7 * product["price"]) & (df["price"] <= 1.3 * product["price"])]
    return filtered

