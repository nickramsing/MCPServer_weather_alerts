import os
from dotenv import load_dotenv
from typing import Optional
from apis.api_requests import get_api_request

# initialize to obtain any environment variables
load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")


def get_nasa_apod(date: Optional[str] = None):
    """
    Purpose:
        Retrieve NASA's Astronomy Picture of the Day (APOD)
        references: https://api.nasa.gov/

    Paramerts:
        api_key (str, optional): NASA API key from env file
        date (Optional[str], optional): Date in YYYY-MM-DD format to retrieve image for specific date
            If no value provided, defaults to today

    Returns:
        Optional[Dict]: Data describing daily picture data.  includes: title, explanation,
        image URL, and other metadata.
        Returns None if request fails.

    Example usage:
       apod = get_nasa_apod(date="2023-01-01")
       print(apod["title"])
    """

    # Set API URL and parameters
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": NASA_API_KEY,
    }
    headers={}

    if date:
        params["date"] = date

    result = get_api_request(url=url,
                             params=params,
                             headers=headers,
                             timeout=10)
    return result


