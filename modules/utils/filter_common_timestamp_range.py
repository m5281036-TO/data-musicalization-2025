import pandas as pd


class FilterCommonTimestampRange:
    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2
        
        
    def filter_common_timestamp_range(self, col_timestamp_index1: str, col_timestamp_index2: str):
        """
        Extract rows where both DataFrames share a common timestamp range.

        Parameters
        ----------
        col_timestamp_index : str
            Column name representing timestamps in both DataFrames.

        Returns
        -------
        df1_filtered, df2_filtered : pd.DataFrame
            Filtered DataFrames restricted to the overlapping timestamp interval.
        """

        df1 = self.df1.copy()
        df2 = self.df2.copy()

        # datetime conversion
        df1[col_timestamp_index1] = pd.to_datetime(df1[col_timestamp_index2])
        df2[col_timestamp_index2] = pd.to_datetime(df2[col_timestamp_index2])

        # determine overlap
        start = max(df1[col_timestamp_index1].min(), df2[col_timestamp_index2].min())
        end   = min(df1[col_timestamp_index1].max(), df2[col_timestamp_index2].max())

        if start >= end:
            raise ValueError("No overlapping timestamp interval.")

        df1_filtered = df1[(df1[col_timestamp_index1] >= start) & (df1[col_timestamp_index1] <= end)]
        df2_filtered = df2[(df2[col_timestamp_index2] >= start) & (df2[col_timestamp_index2] <= end)]

        return df1_filtered, df2_filtered
