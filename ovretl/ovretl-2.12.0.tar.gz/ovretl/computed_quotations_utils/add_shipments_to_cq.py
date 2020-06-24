import pandas as pd


def add_shipments_to_cq(computed_quotations_df: pd.DataFrame, shipments_all_propositions_df: pd.DataFrame):
    computed_quotations_df = computed_quotations_df.rename(columns={"id": "computed_quotation_id"})
    computed_quotations_df = computed_quotations_df.dropna(subset=["proposition_id"])
    computed_quotations_df = computed_quotations_df.sort_values(by=["proposition_id", "created_at"], ascending=False)
    computed_quotations_df = computed_quotations_df.drop_duplicates(subset=["proposition_id"])
    computed_quotations_df = pd.merge(
        shipments_all_propositions_df[["shipment_id", "proposition_id"]],
        computed_quotations_df.drop(["shipment_id"], axis=1),
        how="inner",
        on="proposition_id",
    )
    return computed_quotations_df
