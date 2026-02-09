import requests
from typing import Optional, Dict
from log_writer.logger import get_logger

#instantiate module level logger
logger = get_logger(__name__)

def get_api_request(url: str,
                    params: dict,
                    headers: dict,
                    timeout: int = 20) -> Optional[Dict]:
    """
    Purpose:
        Perform a RESTFUL HTTP GET request to a url

    Parameters:
        url (str): URL the request is reaching out to
        params (dict): parameters to include in the request
        timeout (int, optional): Request timeout in seconds. Defaults to 20.
    Returns:
        Optional[Dict]: JSON response as a dictionary if successful
            None if request failed

    Exceptions:
        Prints error message to console if request fails
        Returns result parameter:
            result = {"result": False,
                      "response": message}
    """
    try:
        logger.info(f"Attempting to access NWS url {url}... ")
        response = requests.get(url,
                                params=params,
                                headers=headers,
                                timeout=timeout)

        # Check if the response status code indicates success
        response.raise_for_status()

        # return GET request as JSON
        result = {
            "result": True,
            "status_code": response.status_code,
            "response": response.json()
            }
        logger.info(f"Successful retrival of NWS data")
        return result

    except requests.exceptions.Timeout:
        message = f"EXCEPTION occurred: Request timeout after {timeout} seconds for URL: {url}"
        logger.error(message)
        result = {"result": False,
                  "response": message}
        return result

    except requests.exceptions.ConnectionError:

        message = f"EXCEPTION occurred: Connection error occurred for URL: {url}"
        logger.error(message)
        result = {"result": False,
                  "response": message}
        return result

    except requests.exceptions.HTTPError as e:
        message = f"EXCEPTION occurred: HTTP error for URL: {url} - exception: {e}"
        logger.error(message)
        result = {"result": False,
                  "response": message}
        return result

    except Exception as e:
        message = f"EXCEPTION occurred: Unexpected error for URL: {url} - exception: {e}"
        logger.error(message)
        result = {"result": False,
                  "response": message}
        return result

