import pandas as pd

class DataFrameSelector:
    """
    DataFrameSelector Class
    -----------------------
    Provides methods to:
    1. Select specified columns from a pandas DataFrame.
    2. Filter rows by column values, with optional floating-point tolerance.
    """

    def select_columns(self, df: pd.DataFrame, timestamp: str, col1: str) -> pd.DataFrame:
        """
        Select one column for timestamp, and two columns from the input DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        
        missing_cols = [c for c in [timestamp, col1] if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Columns not found in DataFrame: {missing_cols}")

        return df[[timestamp, col1]].copy()
