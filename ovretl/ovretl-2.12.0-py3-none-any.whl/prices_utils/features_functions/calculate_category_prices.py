import pandas as pd


def pivot_category_prices(prices_df):
    prices_df = pd.pivot_table(prices_df, index=["shipment_id"], columns=["category"], values=["price_in_eur"])
    prices_df.columns = prices_df.columns.droplevel()
    return prices_df.rename(
        columns={
            "arrival_fees": "arrival_fees_price",
            "arrival_truck_freight": "arrival_truck_freight_price",
            "customs": "customs_price",
            "departure_fees": "departure_fees_price",
            "departure_truck_freight": "departure_truck_freight_price",
            "freight": "freight_price",
            "insurance": "insurance_price",
            "other": "other_price",
        }
    )


def pivot_category_purchase_prices(prices_df):
    prices_df = pd.pivot_table(prices_df, index=["shipment_id"], columns=["category"], values=["purchase_price_in_eur"])
    prices_df.columns = prices_df.columns.droplevel()
    return prices_df.rename(
        columns={
            "arrival_fees": "arrival_fees_purchase_price",
            "arrival_truck_freight": "arrival_truck_freight_purchase_price",
            "customs": "customs_purchase_price",
            "departure_fees": "departure_fees_purchase_price",
            "departure_truck_freight": "departure_truck_freight_purchase_price",
            "freight": "freight_purchase_price",
            "insurance": "insurance_purchase_price",
            "other": "other_purchase_price",
        }
    )
