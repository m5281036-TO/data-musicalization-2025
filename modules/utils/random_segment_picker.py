import numpy as np
import pandas as pd


class RandomSegmentPicker:
    def __init__(self, df, num_rows=5):
        self.df = df.copy()
        self.num_rows = num_rows
        

    def pick_random_segment(self) -> pd.DataFrame:
        start = np.random.randint(1, len(self.df) - self.num_rows)
        subset = self.df.iloc[start:start + self.num_rows]
        return subset
