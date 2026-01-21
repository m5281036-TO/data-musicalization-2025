import pandas as pd
import numpy as np
from pathlib import Path


class CSVNaNReplacer:
    """
    Replace NaN values in a DataFrame with -1 and save it as a CSV file.
    """

    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize the class with a pandas DataFrame.

        Parameters
        ----------
        dataframe : pd.DataFrame
            The input DataFrame containing potential NaN values.
        """
        self.df = dataframe.copy()

    def replace_nan_and_save(self, output_path: str, scale_factor = 100, skip_first_row: bool = True):
        """
        Replace NaN values with -1 and save the DataFrame to a CSV file.

        Parameters
        ----------
        output_path : str
            Path to save the CSV file. Can be relative or absolute.
        """
        # Convert output_path to Path object
        path = Path(output_path)

        # Replace NaN with -1
        df_filled = self.df.fillna(-1)
        
        # when do not include first row
        if skip_first_row == True:
            df_filled = df_filled.iloc[1:]
        
        # Multiply numeric columns by scale_factor and round to get int values
        numeric_cols = df_filled.select_dtypes(include=[np.number]).columns
        df_filled[numeric_cols] = (df_filled[numeric_cols] * scale_factor).round().astype(int)

        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Save to CSV
        sep_char = "\t"
        df_filled.to_csv(path, index=False, encoding="utf-8", sep=sep_char)

        print(f"CSV saved to: {path.resolve()}")
