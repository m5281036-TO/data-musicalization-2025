import pandas as pd

class DataFrameSelector:
    """
    DataFrameSelector Class
    -----------------------
    Provides methods to:
    1. Select specified columns from a pandas DataFrame.
    2. Filter rows by column values, with optional floating-point tolerance.
    """

    def select_columns(self, df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
        """
        Select two columns from the input DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        
        missing_cols = [c for c in [col1, col2] if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Columns not found in DataFrame: {missing_cols}")

        return df[[col1, col2]].copy()

    def select_columns_by_value(
        self,
        df: pd.DataFrame,
        col1: str,
        col2: str,
        row_index: str,
        row_keyword,
        float_tolerance: float = 1e-6
    ) -> pd.DataFrame:
        """
        Select two columns from df and filter rows where row_index column matches row_keyword.
        For numeric columns, a floating point tolerance can be specified.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        if any(c not in df.columns for c in [col1, col2, row_index]):
            raise ValueError(f"One or more specified columns not found in DataFrame.")
        
        # 対象列が数値型かどうかを判定
        if pd.api.types.is_numeric_dtype(df[row_index]):
            try:
                keyword_float = float(row_keyword)
            except ValueError:
                raise TypeError(f"row_keyword must be convertible to float for numeric column '{row_index}'.")
            filtered_df = df[(df[row_index] - keyword_float).abs() <= float_tolerance].copy()
        else:
            # 文字列として検索
            filtered_df = df.loc[
                df[row_index].astype(str).str.contains(str(row_keyword), na=False, regex=False)
            ].copy()
        
        # 0行チェック
        if len(filtered_df) == 0:
            raise ValueError(f"No rows matched '{row_keyword}' in column '{row_index}'.")

        return filtered_df[[col1, col2, row_index]].copy()
