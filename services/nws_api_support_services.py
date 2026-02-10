from typing import Optional, Any, List
import json
from log_writer.logger import get_logger

#instantiate module level logger
logger = get_logger(__name__)


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
    """
    Purpose: Format an alert feature into a readable string.
        Parse out specific elements from the alert feature:
            - Event
            - Area
            - Timespan
            - Severity
            - Description
            - Instructions

    Parameters:
        feature: dict - dictionary containing the alert feature information
    """
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

