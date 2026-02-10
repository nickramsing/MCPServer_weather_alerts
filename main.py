import apis.weather_gov.weather_api_requests as weather
import json
from typing import List


def try_weatheralerts_byState(state: List[str]):
    #stateList = ["AK", "AL", "AR", "AS", "AZ", "CA", "CO", "CT", "DC", "DE",
    #"FL", "GA", "GU", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME",
    #"MI", "MN", "MO", "MP", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY",
    #"OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UM", "UT", "VA", "VI",
    #"VT", "WA", "WI", "WV", "WY"]
    #if state not in stateList:
    #    return f"You entered {state}. The State must be a TWO digit state abbreviation of a US State."
    print(state)
    result = weather.get_weather_alerts_state(area=state)
    print(f"type returned from API request call: {type(result)} ---  {result}")
    if result["result"] == True:
        for alert in result["response"]:
            print(alert)
    else:
        print("ERROR OCCURRED === ==")
        print(json.dumps(result["response"], indent=4))



if __name__ == "__main__":
    #try_nasaAPIs()
    print("Welcome to the Nasa Weather API")
    try_weatheralerts_byState(state=["MD"])

