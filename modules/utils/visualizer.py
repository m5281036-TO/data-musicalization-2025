import pandas as pd
import matplotlib.pyplot as plt


class Visualizer:
    """
    Visualize and analyze the relationship between two DataFrames.
    """

    def __init__(self, dataframe1: pd.DataFrame, dataframe2: pd.DataFrame):
        self.df1 = dataframe1
        self.df2 = dataframe2


    def _filter_common_timestamp_range(self, col_timestamp_index: str):
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
        df1[col_timestamp_index] = pd.to_datetime(df1[col_timestamp_index])
        df2[col_timestamp_index] = pd.to_datetime(df2[col_timestamp_index])

        # determine overlap
        start = max(df1[col_timestamp_index].min(), df2[col_timestamp_index].min())
        end   = min(df1[col_timestamp_index].max(), df2[col_timestamp_index].max())

        if start >= end:
            raise ValueError("No overlapping timestamp interval.")

        df1_filtered = df1[(df1[col_timestamp_index] >= start) & (df1[col_timestamp_index] <= end)]
        df2_filtered = df2[(df2[col_timestamp_index] >= start) & (df2[col_timestamp_index] <= end)]

        return df1_filtered, df2_filtered


    def plot_time_series(self, col_timestamp_index: str, value_index1: str, value_index2: str):
        """
        Plot values from two DataFrames on the same timestamp range.
        """

        # df1_f, df2_f = self._filter_common_timestamp_range(col_timestamp_index)

        plt.plot(
            self.df1[col_timestamp_index],
            self.df1[value_index1],
            label=f"df1: {value_index1}",
            color="blue",
            linewidth=2
        )

        plt.plot(
            self.df2[col_timestamp_index],
            self.df2[value_index2],
            label=f"df2: {value_index2}",
            color="red",
            linewidth=2
        )

        plt.title("Time Series Comparison (Overlapping Interval Only)")
        plt.xlabel("Timestamp")
        plt.ylabel("Value")
        plt.grid(True)
        plt.legend(loc="best")
        plt.tight_layout()
        plt.show()
