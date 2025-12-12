import pandas as pd
import numpy as np
import stumpy
import matplotlib.pyplot as plt


class TimeSeriesPatternAnalyzer:
    """
    Perform pattern analysis between two time-series DataFrames using Matrix Profile.
    Includes:
      - Timestamp conversion
      - Overlap range trimming
      - Resampling and alignment
      - Cross Matrix Profile computation
      - Visualization of results
    """

    def __init__(self, df1: pd.DataFrame, df2: pd.DataFrame):
        self.df1 = df1.copy()
        self.df2 = df2.copy()

    def _prepare_timestamp(self, df: pd.DataFrame, col_timestamp: str):
        """Convert timestamp column to datetime and set as index."""
        df[col_timestamp] = pd.to_datetime(df[col_timestamp], utc=True)
        df[col_timestamp] = df[col_timestamp].dt.tz_localize(None)
        df = df.set_index(col_timestamp)
        return df

    def _trim_to_overlap(self, df1: pd.DataFrame, df2: pd.DataFrame):
        """Trim both DataFrames so only the overlapping time range remains."""

        start = max(df1.index.min(), df2.index.min())
        end = min(df1.index.max(), df2.index.max())

        if start >= end:
            raise ValueError("No overlapping time range found between df1 and df2.")

        df1_trimmed = df1.loc[start:end].copy()
        df2_trimmed = df2.loc[start:end].copy()

        return df1_trimmed, df2_trimmed

    def resample_and_align(
        self,
        col_timestamp: str,
        col_value1: str,
        col_value2: str,
        freq: str = "1T",
        method: str = "interpolate"
    ):
        """
        Convert timestamps, trim to overlapping period, resample both.
        Returns numpy arrays for matrix profile.
        """

        df1 = self._prepare_timestamp(self.df1, col_timestamp)
        df2 = self._prepare_timestamp(self.df2, col_timestamp)

        df1, df2 = self._trim_to_overlap(df1, df2)

        self._aligned_index = df1.resample(freq).mean().index  # For plotting

        s1 = df1[col_value1].resample(freq)
        s2 = df2[col_value2].resample(freq)

        if method == "interpolate":
            ts1 = s1.interpolate().values
            ts2 = s2.interpolate().values
        elif method == "ffill":
            ts1 = s1.ffill().values
            ts2 = s2.ffill().values
        elif method == "bfill":
            ts1 = s1.bfill().values
            ts2 = s2.bfill().values
        else:
            raise ValueError("Unknown method for missing-value handling.")

        return ts1.astype(float), ts2.astype(float)

    def compute_cross_matrix_profile(self, ts1: np.ndarray, ts2: np.ndarray, window_size: int):
        """Perform cross-matrix profile analysis."""
        profile = stumpy.stump(ts1, window_size, T_B=ts2)
        return profile

    def plot_results(self, ts1, ts2, profile, window_size: int, label1="Series 1", label2="Series 2"):
        """
        Plot:
          1. Two resampled time series
          2. Cross matrix profile
        """

        index = self._aligned_index[:len(ts1)]

        fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

        # ---- 1. Time Series ----
        axes[0].plot(index, ts1, label=label1, linewidth=1.3)
        axes[0].plot(index, ts2, label=label2, linewidth=1.3)
        axes[0].set_title("Aligned Time Series")
        axes[0].set_ylabel("Value")
        axes[0].grid(True)
        axes[0].legend()

        # ---- 2. Matrix Profile ----
        mp = profile[:, 0]
        axes[1].plot(index[:len(mp)], mp, linewidth=1.2)
        axes[1].set_title("Cross Matrix Profile")
        axes[1].set_ylabel("Distance")
        axes[1].grid(True)

        # ---- 3. Highlight best motif match ----
        best_pos = np.argmin(mp)
        match_pos = int(profile[best_pos, 1])

        axes[2].plot(ts1, label=f"{label1}", linewidth=1)
        axes[2].plot(ts2, label=f"{label2}", linewidth=1, alpha=0.6)

        # Highlight motif windows
        axes[2].axvspan(best_pos, best_pos + window_size, color='blue', alpha=0.3)
        axes[2].axvspan(match_pos, match_pos + window_size, color='red', alpha=0.3)

        axes[2].set_title("Detected Motif Match (Highlighted)")
        axes[2].legend()
        axes[2].grid(True)

        plt.tight_layout()
        plt.show()
