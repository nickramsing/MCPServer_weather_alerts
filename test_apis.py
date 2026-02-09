import apis.weather_gov.weather_api_requests as weather
import json

##WEATHER links
def test_get_WEATHER_alert_active_success():
    result = weather.get_weather_alerts_active(status="actual")
    assert result["result"] == True


def test_get_WEATHER_alert_active_fail():
    ##bad date parameter
    result = weather.get_weather_alerts_active(status="NOTHING_HERE")
    print(result)
    assert result["result"] == False


def test_get_WEATHER_alerts_state_success():
    result = weather.get_weather_alerts_state(area="MD")
    assert result["result"] == True


def test_get_WEATHER_alerts_state_fail():
    ##bad date parameter
    result = weather.get_weather_alerts_state(area="NOTHING_HERE")
    print(result)
    assert result["result"] == False