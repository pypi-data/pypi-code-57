from .Describer import Describer


class GeneralDescriber(Describer):
    TEMP_SKEW_THRESHOLD = 0.4

    def get_section_header(self):
        return "General frame info"

    def describe(self, df):
        messages = [f"Shape: {df.shape}"]

        # NULLS
        columns_with_nulls = df.columns[df.isna().any()].array.to_numpy()
        if len(columns_with_nulls) > 0:
            messages.append(
                f"Columns with one or more null values: {columns_with_nulls}"
            )

        # LE CANDIDATES
        object_typed_columns = df.select_dtypes(
            include='object').columns.array.to_numpy()

        if len(object_typed_columns) > 0:
            messages.append(
                f"Columns of type \"object\" (may need label encoding): {object_typed_columns}"
            )

        # SKEW
        skewness = df.skew()
        skewed_keys = []
        for key in skewness.keys():
            if abs(1-skewness[key]) >= self.TEMP_SKEW_THRESHOLD:
                skewed_keys.append(key)

        if len(skewed_keys) > 0:
            messages.append(
                f"These columns are skewed beyond the threshold of 1 +/- {self.TEMP_SKEW_THRESHOLD}. You may want to scale them somehow.")

            for key in skewed_keys:
                messages.append(f" - {key} ({skewness[key]})")

        return messages
