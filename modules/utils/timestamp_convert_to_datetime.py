import pandas as pd

class TimestampConvertToDatetime:
    """
    Class for converting a timestamp column to datetime type and sorting the DataFrame chronologically.
    """

    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize the class with a pandas DataFrame.

        Parameters
        ----------
        dataframe : pd.DataFrame
            The input DataFrame containing a timestamp column.
        """
        self.df = dataframe.copy()

    def timestamp_convert_to_datetime(self, col_timestamp_index: str) -> pd.DataFrame:
        """
        Convert the specified timestamp column to datetime type (without timezone) 
        and sort the DataFrame in chronological order based on that column.

        Parameters
        ----------
        col_timestamp_index : str
            The name of the column containing timestamp strings.

        Returns
        -------
        pd.DataFrame
            A new DataFrame with the timestamp converted to datetime and sorted chronologically.
        """
        # Convert to datetime with UTC awareness
        self.df[col_timestamp_index] = pd.to_datetime(self.df[col_timestamp_index], utc=True)

        # Remove timezone information
        self.df[col_timestamp_index] = self.df[col_timestamp_index].dt.tz_localize(None)

        # Sort DataFrame by timestamp
        self.df = self.df.sort_values(by=col_timestamp_index).reset_index(drop=True)

        return self.df
