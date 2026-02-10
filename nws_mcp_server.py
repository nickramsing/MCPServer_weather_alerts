from typing import Optional, Any, List
from apis.api_requests import get_api_request
from services.nws_api_support_services import format_alerts, format_result
from mcp.server.fastmcp import FastMCP
import json
from log_writer.logger import get_logger

#instantiate module level logger
logger = get_logger(__name__)

mcp = FastMCP()

@mcp.tool("Get_NWS_weather_alerts_by_state")
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
        Example output
            {
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

def main():
    mcp.run()

if __name__ == "__main__":
    main()