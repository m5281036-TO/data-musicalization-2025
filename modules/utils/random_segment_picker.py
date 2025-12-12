import pandas as pd
import numpy as np

class RandomSegmentPicker:
    def __init__(self, df, num_rows=5):
        self.df = df
        self.num_rows = num_rows
        

    def picker(self):
        start = np.random.randint(1, len(self.df) - self.num_rows)
        subset = self.df.iloc[start:start + self.num_rows]
        print(subset)
