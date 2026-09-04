import requests
import pandas as pd
import urllib3

from configer import HEADERS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_data(url: str) -> pd.DataFrame:
    """Fetch and clean data from a given API URL."""
    session = requests.Session()
    session.headers.update(HEADERS)
    try:
        response = session.get(url, verify=False, timeout=60)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data.get("items", []))
            return df.dropna()
        else:
            print(f"Failed to fetch {url} - Status: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print(f"ERROR fetching {url}: {e}")
        return pd.DataFrame()