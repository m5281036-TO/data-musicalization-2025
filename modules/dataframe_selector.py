import pandas as pd

class DataFrameSelector:
    """
    DataFrameSelector Class
    -----------------------
    Provides methods to:
    1. Select specified columns from a pandas DataFrame.
    2. Filter rows by index range or timestamp range.
    """

    def select_columns(
        self,
        df: pd.DataFrame,
        timestamp: str,
        col1_index: str,
        col2_index: str,
        start_row=None,
        end_row=None
    ) -> pd.DataFrame:
        """
        Select one column for timestamp, and two additional columns from the input DataFrame,
        with optional row filtering by range.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame.
        timestamp : str
            Column name representing timestamp or time index.
        col1_index : str
            First data column name.
        col2_index : str
            Second data column name.
        start_row : int, float, str, optional
            Start of selection range. Can be:
                - Integer (row index)
                - Datetime-like string (timestamp-based filter)
        end_row : int, float, str, optional
            End of selection range. Same format as `start`.

        Returns
        -------
        pd.DataFrame
            Filtered DataFrame containing selected columns.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        
        missing_cols = [c for c in [timestamp, col1_index, col2_index] if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Columns not found in DataFrame: {missing_cols}")

        selected_df = df[[timestamp, col1_index, col2_index]].copy()

        # Filter by range if specified
        if start_row is not None or end_row is not None:
            if pd.api.types.is_datetime64_any_dtype(selected_df[timestamp]):
                # Timestamp-based slicing
                if start_row:
                    start_row = pd.to_datetime(start_row)
                if end_row:
                    end_row = pd.to_datetime(end_row)
                mask = (selected_df[timestamp] >= start_row) & (selected_df[timestamp] <= end_row)
                selected_df = selected_df.loc[mask]
            else:
                # Row index-based slicing
                start_idx = start_row if start_row is not None else 0
                end_idx = end_row if end_row is not None else len(selected_df)
                selected_df = selected_df.iloc[start_idx:end_idx]

        return selected_df
