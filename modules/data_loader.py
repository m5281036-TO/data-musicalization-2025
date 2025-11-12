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
    When loading a JSON file, a CSV copy is also saved to ../data/output/.
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

        # --- Load from URL ---
        if source_lower.startswith("https://") or source_lower.startswith("http://"):
            response = requests.get(source)
            response.raise_for_status()

            if ".csv" in source_lower:
                df = pd.read_csv(io.StringIO(response.text))
            elif ".json" in source_lower:
                df = pd.read_json(io.StringIO(response.text))
                self._save_as_csv(df)
            else:
                raise ValueError("Unsupported file format. Only CSV or JSON are allowed.")

        # --- Load from local file ---
        else:
            if not os.path.exists(source):
                raise FileNotFoundError(f"File not found: {source}")

            if source_lower.endswith(".csv"):
                df = pd.read_csv(source)
            elif source_lower.endswith(".json"):
                df = pd.read_json(source)
                self._save_as_csv(df)
            else:
                raise ValueError("Unsupported file format. Only CSV or JSON are allowed.")
        return df

    def _save_as_csv(self, df: pd.DataFrame):
        """
        Save the given DataFrame as a CSV file in ../data/output/csv/.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to save.
        """
        output_dir = os.path.join("..", "data", "output", "csv")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "json_decoded.csv")
        df.to_csv(output_path, index=False, encoding="utf-8")
