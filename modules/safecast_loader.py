import requests
import pandas as pd
import time
from .utils import TimeSortDataFrame


class SafecastLoader:
    """
    Retrieve measurement data from the Safecast API for a specific device and time range.
    Handles network errors gracefully by retrying failed requests and returning partial results.
    """

    BASE_URL = "https://api.safecast.org/en-US/measurements.json"

    def __init__(self, time_sort: bool=False, timestamp_index_name: str=None, page_limit: int = 40, max_retries: int = 3, retry_delay: int = 5):
        """
        Initialize the SafecastLoader.

        Parameters
        ----------
        page_limit : int
            Maximum number of pages to fetch (default: 40, API limit recommended under 49).
        max_retries : int
            Number of retry attempts per failed request (default: 3).
        retry_delay : int
            Waiting time in seconds between retries (default: 5).
        """
        self.time_sort = time_sort
        self.timestamp_index_name = timestamp_index_name
        self.page_limit = page_limit
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def fetch_device_data(self, device_id, date_from="2011-01-01", date_to="2022-12-31", limit: int = 1000):
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
            Combined DataFrame of all measurement records (partial if connection fails).
        """
        df = []
        page = 1

        print(f"Fetching data for device_id={device_id} from {date_from} to {date_to} ...")

        for _ in range(self.page_limit):
            params = {
                "device_id": device_id,
                "captured_after": date_from,
                "captured_before": date_to,
                "page": page,
                "limit": limit
            }

            retries = 0
            while retries <= self.max_retries:
                try:
                    response = requests.get(SafecastLoader.BASE_URL, params=params, timeout=10)
                    print(f"Requesting page {page}... Status: {response.status_code}")

                    # Retry only on temporary server-side errors
                    if response.status_code >= 500:
                        retries += 1
                        print(f"Server error {response.status_code}, retrying ({retries}/{self.max_retries})...")
                        time.sleep(self.retry_delay)
                        continue

                    if response.status_code != 200:
                        print(f"Request failed with status {response.status_code}.")
                        raise requests.RequestException

                    data = response.json()
                    if not data:
                        print("No more data returned.")
                        raise StopIteration

                    df.extend(data)
                    print(f"Retrieved {len(data)} records from page {page}.")
                    page += 1
                    break  # success, break retry loop

                except (requests.Timeout, requests.ConnectionError) as e:
                    retries += 1
                    print(f"Connection error: {e}. Retrying ({retries}/{self.max_retries})...")
                    time.sleep(self.retry_delay)
                except StopIteration:
                    print("End of dataset reached.")
                    return pd.DataFrame(df)
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    retries = self.max_retries + 1  # stop further retries

            else:
                print(f"Failed to retrieve page {page} after {self.max_retries} retries. Stopping.")
                break

        if self.time_sort == True:
            time_sorter = TimeSortDataFrame(df, timestamp_index_name=self.timestamp_index_name)
            time_sorter.sort_by_time()
        print(f"Total records retrieved: {len(df)}")
        return pd.DataFrame(df)
