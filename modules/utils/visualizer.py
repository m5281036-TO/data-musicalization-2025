import os
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
        df1 = self.df1.copy()
        df2 = self.df2.copy()

        df1[col_timestamp_index] = pd.to_datetime(df1[col_timestamp_index])
        df2[col_timestamp_index] = pd.to_datetime(df2[col_timestamp_index])

        start = max(df1[col_timestamp_index].min(), df2[col_timestamp_index].min())
        end   = min(df1[col_timestamp_index].max(), df2[col_timestamp_index].max())

        if start >= end:
            raise ValueError("No overlapping timestamp interval.")

        df1_filtered = df1[(df1[col_timestamp_index] >= start) & (df1[col_timestamp_index] <= end)]
        df2_filtered = df2[(df2[col_timestamp_index] >= start) & (df2[col_timestamp_index] <= end)]

        return df1_filtered, df2_filtered


    def plot_time_series(
        self,
        col_timestamp_index: str,
        value_index1: str,
        value_index2: str,
        isSave: bool = False,
        output_dir: str = None,
        filename: str = "time_series.pdf",
    ):
        """
        Plot values from two DataFrames on the same timestamp range.

        Parameters
        ----------
        save : bool
            If True, save the figure to disk.
        output_dir : str
            Directory where the figure will be saved.
        filename : str
            Output file name.
        """

        plt.figure()

        plt.plot(
            self.df1[col_timestamp_index],
            self.df1[value_index1],
            # label=f"Data1: {value_index1}",
            label = f"Value1: Off the coast of Chiba",
            color="blue",
            linewidth=2
        )

        plt.plot(
            self.df2[col_timestamp_index],
            self.df2[value_index2],
            # label=f"Data2: {value_index2}",
            label=f"Value2: Kobe, Hyogo",
            color="red",
            linewidth=2
        )

        plt.title("Radiation Level in Two Different Loacation")
        plt.xlabel("Time")
        plt.xticks(rotation=70)
        plt.tight_layout()
        plt.ylabel("Radiation Level (CPM)")
        plt.grid(True)
        plt.legend(loc="best")
        plt.tight_layout()

        if isSave:
            if output_dir is None:
                raise ValueError("output_dir must be specified when save=True")
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(os.path.join(output_dir, filename))

        plt.show()