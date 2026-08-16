import pandas as pd


def temporal_split(df, timestamp_col='Timestamp', test_frac=0.2):
    """Sort by time and split so test is strictly later than train.

    Never use a random split for this project — a random split would leak
    future transaction information into training, which is not a realistic
    or valid way to evaluate a fraud/AML detection model.
    """
    df = df.sort_values(timestamp_col).reset_index(drop=True)
    split_idx = int(len(df) * (1 - test_frac))
    train = df.iloc[:split_idx].copy()
    test = df.iloc[split_idx:].copy()
    return train, test
