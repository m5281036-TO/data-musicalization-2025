import pandas as pd

class TimeAlignedDataMerger:
    def __init__(self, freq: str = "5H", how: str = "mean"):
        """
        freq : リサンプリング間隔 (例: "1H", "1D")
        how  : リサンプリング時の集計方法 ("mean", "sum", "max" など)
        """
        self.freq = freq
        self.how = how

    def _prepare(self, df: pd.DataFrame, timestamp_idx_name: str, value_name: str):
        df = df.copy()
        df[timestamp_idx_name] = pd.to_datetime(df[timestamp_idx_name])
        df = df.set_index(timestamp_idx_name)

        df_resampled = df["value"].resample(self.freq).agg(self.how)
        df_resampled = df_resampled.to_frame(name=value_name)

        return df_resampled

    def merge(
        self,
        df1: pd.DataFrame,
        df1_timestamp_idx_name: str,
        df2: pd.DataFrame,
        df2_timestamp_idx_name: str,
    ):
        df1_q = self._prepare(df1, timestamp_idx_name=df1_timestamp_idx_name, value_name="data1")
        df2_q = self._prepare(df2, timestamp_idx_name=df2_timestamp_idx_name, value_name="data2")

        merged = pd.concat([df1_q, df2_q], axis=1)

        merged = merged.interpolate(method="linear")
        
        merged = merged.reset_index()
        return merged
