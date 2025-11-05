import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    """
    Visualize and analyze the distribution relationship between two numerical columns
    by binning the X-axis and summarizing Y-axis values.
    """

    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize the visualizer with a pandas DataFrame.

        Parameters
        ----------
        dataframe : pd.DataFrame
            The dataset to analyze. Must contain the numeric columns of interest.
        """
        self.df = dataframe

    def plot_binned_histogram(self, col_x: str, col_y: str, bins: int = 10):
        """
        Plot a histogram-like bar chart where X is binned and Y represents the mean value
        within each bin.

        Parameters
        ----------
        col_x : str
            Column name to be used as the binning variable (X-axis).
        col_y : str
            Column name for the dependent variable (Y-axis).
        bins : int, optional
            Number of bins to use for grouping X values (default is 10).

        Returns
        -------
        None
            Displays the bar plot.
        """
        if col_x not in self.df.columns or col_y not in self.df.columns:
            raise ValueError("Specified columns are not present in the DataFrame.")

        # 欠損値を除去
        data = self.df[[col_x, col_y]].dropna()

        # col_xをbins個に区切ってカテゴリ化
        data["x_bin"] = pd.cut(data[col_x], bins=bins)

        # 各binにおけるcol_yの平均値を計算
        binned_means = data.groupby("x_bin")[col_y].mean()

        # ビンの中心を取得
        bin_centers = [interval.mid for interval in binned_means.index]

        # 棒グラフ描画
        plt.figure(figsize=(8, 5))
        plt.bar(bin_centers, binned_means, width=(bin_centers[1] - bin_centers[0]) * 0.8)
        plt.xlabel(col_x)
        plt.ylabel(f"Mean of {col_y}")
        plt.title(f"{col_y} vs {col_x} (binned into {bins} intervals)")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

        print("Binned mean values:")
        print(binned_means)
