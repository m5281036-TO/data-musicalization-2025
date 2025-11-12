import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import stumpy

class TimeSeriesPatternMiner:
    """
    Detect and visualize patterns and anomalies in time series using STUMPY.
    """

    def __init__(self, dataframe: pd.DataFrame, time_col: str, value_col: str):
        self.df = dataframe.copy()
        self.time_col = time_col
        self.value_col = value_col
        self.df[self.time_col] = pd.to_datetime(self.df[self.time_col])
        self.df = self.df.sort_values(by=self.time_col)

    def pattern_miner(self, window_size=20, threshold=None, highlight_anomalies=True,
                      normalize=False, smoothing_window=None, return_results=False):
        """
        Compute and visualize the matrix profile for pattern and anomaly detection.

        Parameters
        ----------
        window_size : int
            Length of the subsequences.
        threshold : float, optional
            Matrix profile threshold for anomaly detection.
        highlight_anomalies : bool
            If True, anomalies will be marked on the plot.
        normalize : bool
            If True, normalize the value column (z-score).
        smoothing_window : int, optional
            Apply moving average smoothing before analysis.
        return_results : bool
            If True, return a DataFrame with matrix profile and anomaly flags.
        """
        values = self.df[self.value_col].values

        # Optional smoothing
        if smoothing_window and smoothing_window > 1:
            values = pd.Series(values).rolling(smoothing_window, min_periods=1).mean().values

        # Optional normalization
        if normalize:
            values = (values - np.mean(values)) / np.std(values)

        # Compute matrix profile
        mp = stumpy.stump(values, window_size)
        matrix_profile = mp[:, 0]

        # Determine threshold
        if threshold is None:
            threshold = np.percentile(matrix_profile, 95)

        # Identify anomalies
        anomaly_idx = np.where(matrix_profile > threshold)[0]

        # Visualization
        fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

        # 1. Time series
        ax[0].plot(self.df[self.time_col], values, label=self.value_col)
        if highlight_anomalies:
            ax[0].scatter(self.df[self.time_col].iloc[anomaly_idx], values[anomaly_idx],
                          color='red', label='Anomaly', zorder=5)
        ax[0].set_ylabel("Value")
        ax[0].set_title("Time Series with Pattern and Anomaly Detection")
        ax[0].legend()
        ax[0].grid(True)

        # 2. Matrix profile
        ax[1].plot(self.df[self.time_col][:len(matrix_profile)], matrix_profile, color='orange', label='Matrix Profile')
        ax[1].axhline(y=threshold, color='red', linestyle='--', label='Threshold')
        ax[1].set_ylabel("Matrix Profile")
        ax[1].set_xlabel("Time")
        ax[1].legend()
        ax[1].grid(True)

        plt.tight_layout()
        plt.show()

        if return_results:
            result_df = self.df.iloc[:len(matrix_profile)].copy()
            result_df["matrix_profile"] = matrix_profile
            result_df["is_anomaly"] = 0
            result_df.loc[anomaly_idx, "is_anomaly"] = 1
            return result_df
