from typing import Optional, Any, List
from apis.api_requests import get_api_request
import json
from log_writer.logger import get_logger

#instantiate module level logger
logger = get_logger(__name__)

def get_weather_alerts_active(status: Optional[str] = None):
    """
    Purpose:
        Retrieve weather alerts
        references: https://api.weather.gov/

    Parameters:
        api_key (str, optional): NASA API key from env file
        status (Optional[str]) array<string> fronm list [actual, exercise, system, test, draft]

    Returns:
        Optional[Dict]:

    Example usage:

    """

    # Set API URL and parameters
    url = "https://api.weather.gov/alerts/active"
    params = {}
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    if status:
        params["status"] = status
    else:
        params["status"] = "actual"

    result = get_api_request(url=url,
                             params=params,
                             headers=headers,
                             timeout=10)
    return result


#def get_weather_alerts_state(area: Optional[str] = None): #-> dict[str, Any] | None:
def get_weather_alerts_state(area: str | None = None) -> dict[str, Any]:
    """
    Purpose:
        Retrieve weather alerts by United States state. Provide the US state by TWO letter abbreviation state code.
        Returns listing of US weather alerts from US government api.weather.gov site
        references: https://api.weather.gov/

    Parameters:
        area (Optional[str]): State/territory code or marine area code
            This parameter is incompatible with the following parameters: point, region, region_type, zone
            State/territory code can be in following List: [‘AK’, ‘AL’, ‘AR’, ‘AS’, ‘AZ’, ‘CA’, ‘CO’, ‘CT’, ‘DC’,
                ‘DE’, ‘FL’, ‘GA’, ‘GU’, ‘HI’, ‘IA’, ‘ID’, ‘IL’, ‘IN’, ‘KS’, ‘KY’, ‘LA’, ‘MA’, ‘MD’, ‘ME’, ‘MI’,
                ‘MN’, ‘MO’, ‘MP’, ‘MS’, ‘MT’, ‘NC’, ‘ND’, ‘NE’, ‘NH’, ‘NJ’, ‘NM’, ‘NV’, ‘NY’, ‘OH’, ‘OK’, ‘OR’,
                ‘PA’, ‘PR’, ‘RI’, ‘SC’, ‘SD’, ‘TN’, ‘TX’, ‘UM’, ‘UT’, ‘VA’, ‘VI’, ‘VT’, ‘WA’, ‘WI’, ‘WV’, ‘WY’]

    Returns:
        Returns listing of US weather alerts from US government api.weather.gov site
        Optional[Dict]:

    Example usage:
    result = {
                "result": True,
                "status_code": result["status_code"],
                "response": alerts
            }

    """

    # Set API URL and parameters
    url = "https://api.weather.gov/alerts"
    params = {}
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    if area:
        params["area"] = area
    #else:
    #    params["status"] = "actual"

    result = get_api_request(url=url,
                             params=params,
                             headers=headers,
                             timeout=10)

    if result["result"] == False:

        outcome = format_result(result_outcome=False,
                                result_status=result["status_code"],
                                result_data=[])
        logger.info(f"Error retrieving from NWS API. Status code {result["status_code"]} ")
        return outcome

    else:
        #if doesn't have any alerts -- aka no features
        if not result["response"]["features"]:
            outcome = format_result(result_outcome=True,
                                    result_status=result["status_code"],
                                    result_data=["No active weather alerts for this region."])
            logger.info(f"No active weather alerts found for {area} ... ")
            return outcome
        else:
            ## If format_alerts(feature) returns None for invalid data, such as test messages
            logger.info(f"Attempting to format alerts: generating... ")
            alerts = [
                alert for feature in result["response"]["features"]
                for alert in [format_alerts(feature)]
                if alert is not None
            ]

            #returns list of alerts: JSON formatte
            #result = {
            #    "result": True,
            #    "status_code": result["status_code"],
            #    "response": [alerts]
            #}
            #output = json.dumps(result, indent=4)
            outcome = format_result(result_outcome=True,
                  result_status=result["status_code"],
                  result_data=[alerts])
        return outcome


def format_result(result_outcome: bool,
                  result_status: str,
                  result_data: List[str]) -> dict[str, Any]:
    """
    Purpose: Formats the result from calling the weather service.

    Parameters:
        result_outcome: bool - True or False from the API call
        result_status: str - Status code from the API call
        result_data: List[str]) - date from the API call
    """
    result = {
        "result": result_outcome,
        "status_code": result_status,
        "response": result_data
    }
    #output = json.dumps(result, indent=4)
    return result


class TestMessageException(Exception):
    """Custom exception for processing alerts that are test messages."""
    pass

def format_alerts(feature: dict) -> dict[str, Any]:
    """Format an alert feature into a readable string."""
    props = feature["properties"]

    try:
        if props.get("event").upper() == "TEST MESSAGE":
            raise TestMessageException("This is a test message")
            #don't log this!! too much white noise!
        else:

            parsedElements = {
                "Event": {props.get('event', 'Unknown')},
                "Area": {props.get('areaDesc', 'Unknown')},
                "Timespan": {
                    "Effective": {props.get('effective', 'Unknown')},
                    "Expires": {props.get('expires', 'Unknown')}
                },
                "Severity": {props.get('severity', 'Unknown')},
                "Description": {props.get('description', 'No description available')},
                "Instructions": {props.get('instruction', 'No specific instructions provided')}
            }
            return parsedElements
    except TestMessageException as tme:
        logger.exception(f"Test Message Exception:  {tme}")
        pass
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED: formatting alerts: {e}")

