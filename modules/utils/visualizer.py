import pandas as pd
import matplotlib.pyplot as plt


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
        
        
    def plot_time_series_data(self, col_timestamp_index: str, col_x_index: str, col_y_index: str):
        """
        Plot two numerical columns from the stored DataFrame against a common timestamp column.

        Parameters
        ----------
        col_timestamp_index : str
            The column name representing timestamps (x-axis).
        col_x_index : str
            The first data column to plot (displayed in blue).
        col_y_index : str
            The second data column to plot (displayed in red).

        Description
        -----------
        This method visualizes the temporal behavior of two numerical variables
        on the same time axis for comparison. The timestamp column is used as
        the horizontal axis, and both specified columns are plotted as separate
        colored lines. The resulting figure includes a legend, gridlines, and
        labeled axes for clarity.
        """
        
        plt.plot(
            self.df[col_timestamp_index],
            self.df[col_x_index],
            label=f"{col_x_index}",
            color="blue",
            linewidth=2
        )

        # Red line
        plt.plot(
            self.df[col_timestamp_index],
            self.df[col_y_index],
            label=f"{col_y_index}",
            color="red",
            linewidth=2
        )

        plt.title("Time Series Comparison")
        plt.xlabel("Timestamp")
        plt.ylabel("Value")
        plt.grid(True)
        plt.legend(loc="best")
        plt.tight_layout()
        plt.show()
            

    def plot_binned_histogram(self, col_x_index: str, col_y_index: str, bins: int = 10):
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
        if col_x_index not in self.df.columns or col_y_index not in self.df.columns:
            raise ValueError("Specified columns are not present in the DataFrame.")

        # omit NaN
        data = self.df[[col_x_index, col_y_index]].dropna()

        # bins
        data["x_bin"] = pd.cut(data[col_x_index], bins=bins)

        # compute average on each bin
        binned_means = data.groupby("x_bin")[col_y_index].mean()

        # get mean value of bin
        bin_centers = [interval.mid for interval in binned_means.index]

        plt.figure(figsize=(8, 5))
        plt.bar(bin_centers, binned_means, width=(bin_centers[1] - bin_centers[0]) * 0.8)
        plt.xlabel(col_x_index)
        plt.ylabel(f"Mean of {col_y_index}")
        plt.title(f"{col_y_index} vs {col_x_index} (binned into {bins} intervals)")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

