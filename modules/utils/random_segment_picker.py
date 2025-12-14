import numpy as np
import pandas as pd


class RandomSegmentPicker:
    def __init__(self, df, num_rows=5):
        self.df = df.copy()
        self.num_rows = num_rows
        

    def pick_random_segment(self, isNormalized: bool = False) -> pd.DataFrame:
        start = np.random.randint(1, len(self.df) - self.num_rows)
        subset = self.df.iloc[start:start + self.num_rows].copy()

        if isNormalized:
            numeric_cols = subset.select_dtypes(include=[np.number]).columns
            subset[numeric_cols] = (
                subset[numeric_cols] - subset[numeric_cols].min()
            ) / (
                subset[numeric_cols].max() - subset[numeric_cols].min()
            )

        return subset