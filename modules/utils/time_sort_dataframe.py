import pandas as pd

class TimeSortDataFrame:
    """
    Automatically detect a timestamp column and sort the DataFrame chronologically.
    """

    def __init__(self, df: pd.DataFrame, timestamp_index_name: str):
        """
        Initialize with a pandas DataFrame.

        Parameters
        ----------
        data : pandas.DataFrame
            The input dataset that contains at least one timestamp-like column.
        """
        self.df = df
        self.timestamp_col = self._detect_timestamp_column(timestamp_index_name)

    def _detect_timestamp_column(self, timestamp_index_name: str):
        """
        Detect the column whose name includes 'timestamp' (case-insensitive).

        Returns
        -------
        str
            The detected timestamp column name.

        Raises
        ------
        ValueError
            If no column containing 'timestamp' is found.
        """

    def sort_by_time(self, timestamp_index_name: str, ascending: bool = True):
        """
        Sort the DataFrame chronologically by the detected timestamp column.

        Parameters
        ----------
        ascending : bool, default=True
            Sort order; True for ascending (oldest first), False for descending.

        Returns
        -------
        pandas.DataFrame
            The time-sorted DataFrame.
        """
        for col in self.df.columns:
            if timestamp_index_name in col.lower():
                return col
            # raise ValueError(f"No column containing '{timestamp_index_name}' found in the DataFrame.")

        # Ensure column is datetime
        self.df[self.timestamp_col] = pd.to_datetime(self.df[self.timestamp_col], errors='coerce')

        # Drop rows with invalid timestamps before sorting
        self.df = self.df.dropna(subset=[self.timestamp_col])

        # Sort chronologically
        self.df = self.df.sort_values(by=self.timestamp_col, ascending=ascending).reset_index(drop=True)
        return self.df
