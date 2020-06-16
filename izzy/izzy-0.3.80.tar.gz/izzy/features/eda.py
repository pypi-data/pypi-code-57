

# Correlation between DataFrame and an outcome
def outcome_corr(df, outcome, columns=None, method='pearson'):
    # Set columns if None; make sure not outcome
    if columns is None:
        columns = [column for column in columns if column != outcome]

    # Create new DataFrame with columns and outcome
    df = df[columns + [outcome]].copy()

    # Compute correlation
    # TODO is this more efficient than a for loop? Might be better to hard code equation in
    corr_matrix = df.corr(method=method)

    # Return
    return corr_matrix[outcome]

# Plot outcome_corr

