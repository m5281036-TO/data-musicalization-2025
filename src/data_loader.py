import pandas as pd
import requests
import io
import os

class DataLoader:
    """
    DataLoader Class
    ----------------
    Loads a CSV or JSON file from a local file path or an online source (URL),
    and returns the data as a formatted pandas DataFrame.

    Example
    -------
    >>> loader = DataLoader()
    >>> df = loader.load("https://example.com/data.csv")
    >>> print(df.head())
    """

    def load(self, source: str) -> pd.DataFrame:
        """
        Load data from a local file path or online source.

        Parameters
        ----------
        source : str
            Path to the local file or URL of the data source.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the loaded data.
        """
        source_lower = source.lower()
        if source_lower.startswith("https://") or source.lower().startswith("http://"): # load online files
            response = requests.get(source)
            response.raise_for_status()
            if ".csv" in source_lower:
                df = pd.read_csv(io.StringIO(response.text))
            elif ".json" in source_lower:
                df = pd.read_json(io.StringIO(response.text))
            else:
                raise ValueError("Unsupported file format. Only CSV or JSON are allowed.")
            
        else: # load local file
            if not os.path.exists(source):
                raise FileNotFoundError(f"File not found: {source}")
            if ".csv" in source_lower:
                df = pd.read_csv(io.StringIO(response.text))
            elif ".json" in source_lower:
                df = pd.read_json(io.StringIO(response.text))
            else:
                raise ValueError("Unsupported file format. Only CSV or JSON are allowed.")
            

        print(df)
        return df


# DEBUG
if __name__ == "__main__":
    # test_source = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
    test_source = "https://api.safecast.org/en-US/measurements.json?latitude=37.483&longitude=139.929&radius=10000&limit=500"

    loader = DataLoader()
    df = loader.load(test_source)

    print("Loaded DataFrame:")
    print(df.head())
    print(f"\nShape: {df.shape}")