import requests
import pandas as pd


class SafecastLoader:
    """
    Retrieve measurement data from the Safecast API for a specific device and time range.
    """

    BASE_URL = "https://api.safecast.org/en-US/measurements.json"

    @staticmethod
    def fetch_device_data(device_id, date_from="2011-01-01", date_to="2022-12-31", limit: int = 1000):
        """
        Fetch measurement data for a given device within a defined time window.

        Parameters
        ----------
        device_id : int
            The unique ID of the Safecast device (can be found in the API data).
        date_from : str
            Start date (ISO format: YYYY-MM-DD).
        date_to : str
            End date (ISO format: YYYY-MM-DD).
        limit : int, optional
            Number of records per page (default 1000, API maximum).

        Returns
        -------
        pandas.DataFrame
            Combined DataFrame of all measurement records.
        """
        all_data = []
        page = 1

        print(f"Fetching data for device_id={device_id} from {date_from} to {date_to} ...")

        while True:
            params = {
                "user_id": device_id,
                "captured_after": date_from,
                "captured_before": date_to,
                "page": page,
                "limit": limit
            }
            response = requests.get(SafecastLoader.BASE_URL, params=params)
            print(f"Requesting page {page}... Status: {response.status_code}")

            if response.status_code != 200:
                print(f"Request failed (status {response.status_code}).")
                break

            data = response.json()
            if not data:
                print("No more data returned.")
                break

            all_data.extend(data)
            print(f"Retrieved {len(data)} records from page {page}.")
            page += 1

        print(f"Total records retrieved: {len(all_data)}")
        return pd.DataFrame(all_data)
