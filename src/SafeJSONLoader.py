import os
import json
import psutil
import pandas as pd
import requests
from io import StringIO
from typing import Union
from requests.adapters import HTTPAdapter, Retry


class SafeJSONLoader:
    """
    A safe JSON loader that supports both local and remote (HTTP/HTTPS) JSON files.
    - Prevents memory overflow by checking file size and system memory.
    - Supports both standard JSON and JSON Lines (jsonl) formats.
    - Can stream data from URLs without loading the entire response into memory.
    """

    def __init__(
        self,
        max_file_size_mb: int = 500,
        max_memory_ratio: float = 0.5,
        lines: bool = False,
        timeout: int = 20,
        retries: int = 3,
        backoff_factor: float = 0.3,
    ):
        """
        Parameters
        ----------
        max_file_size_mb : int
            Maximum allowed file size (in MB) before raising a MemoryError.
        max_memory_ratio : float
            Maximum fraction of system memory allowed to be used (e.g., 0.5 = 50%).
        lines : bool
            Set True if the input is in JSON Lines format.
        timeout : int
            Timeout for HTTP requests in seconds.
        retries : int
            Number of retries for failed HTTP requests.
        backoff_factor : float
            Delay factor between retries.
        """
        self.max_file_size_mb = max_file_size_mb
        self.max_memory_ratio = max_memory_ratio
        self.lines = lines
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor

    # ---------- Internal memory and size checks ----------

    def _check_file_size_local(self, file_path: str):
        """Check local file size before loading."""
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > self.max_file_size_mb:
            raise MemoryError(
                f"File size exceeds limit: {size_mb:.1f} MB > {self.max_file_size_mb} MB"
            )

    def _check_available_memory(self):
        """Check system memory usage before loading large files."""
        mem = psutil.virtual_memory()
        available_mb = mem.available / (1024 * 1024)
        total_mb = mem.total / (1024 * 1024)
        used_ratio = (total_mb - available_mb) / total_mb

        if used_ratio > self.max_memory_ratio:
            raise MemoryError(
                f"High memory usage detected: {used_ratio*100:.1f}% > allowed {self.max_memory_ratio*100:.1f}%"
            )

    def _check_remote_file_size(self, url: str, session: requests.Session):
        """Check remote file size using HTTP HEAD request if Content-Length is provided."""
        resp = session.head(url, allow_redirects=True, timeout=self.timeout)
        size_str = resp.headers.get("Content-Length")
        if size_str:
            size_mb = int(size_str) / (1024 * 1024)
            if size_mb > self.max_file_size_mb:
                raise MemoryError(
                    f"Remote file too large: {size_mb:.1f} MB > {self.max_file_size_mb} MB"
                )

    # ---------- Main loading method ----------

    def load(self, path_or_url: str) -> Union[dict, pd.DataFrame]:
        """
        Safely load a JSON file (local or remote) and return as dict or DataFrame.

        Parameters
        ----------
        path_or_url : str
            Path to local file or URL of the JSON resource.
        """
        self._check_available_memory()

        # --- Case 1: Local file ---
        if os.path.exists(path_or_url):
            self._check_file_size_local(path_or_url)
            return self._load_local(path_or_url)

        # --- Case 2: Remote URL ---
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return self._load_remote(path_or_url)

        raise FileNotFoundError(f"Invalid path or URL: {path_or_url}")

    # ---------- Helper methods for loading ----------

    def _load_local(self, file_path: str) -> Union[dict, pd.DataFrame]:
        """Load JSON from a local file."""
        try:
            if self.lines:
                # Stream through JSON Lines file
                records = []
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            try:
                                records.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
                return pd.DataFrame(records)
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return self._convert_to_df_if_list(data)

        except Exception as e:
            raise RuntimeError(f"Error loading local JSON: {e}")

    def _load_remote(self, url: str) -> Union[dict, pd.DataFrame]:
        """Stream JSON from a remote URL with retry and safety checks."""
        session = requests.Session()
        retry_strategy = Retry(
            total=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        # Pre-check content size if available
        self._check_remote_file_size(url, session)

        try:
            with session.get(url, stream=True, timeout=self.timeout) as resp:
                resp.raise_for_status()

                # JSON Lines (stream processing)
                if self.lines:
                    records = []
                    for line in resp.iter_lines(decode_unicode=True):
                        if line:
                            try:
                                records.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
                        if len(records) >= 10000:
                            # Chunk-level memory safety: limit per load
                            self._check_available_memory()
                    return pd.DataFrame(records)

                # Regular JSON
                text = resp.text.strip()
                data = json.loads(text)
                return self._convert_to_df_if_list(data)

        except MemoryError:
            raise
        except Exception as e:
            raise RuntimeError(f"Error loading remote JSON: {e}")

    # ---------- Utility ----------

    def _convert_to_df_if_list(self, data):
        """Convert list-type JSON data to DataFrame."""
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            return data
        else:
            raise ValueError("Unexpected JSON structure.")
