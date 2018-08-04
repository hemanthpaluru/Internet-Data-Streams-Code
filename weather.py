import requests

api_url = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(zip=None, lat=None, lon=None):
    key = "acbbd7367b56db20cf3137ca747b15db"
    if lat and lon:
        location = "lat={lat}&lon={lon}".format(lat=lat, lon=lon)
    elif zip:
        location = "zip={z},us".format(z=zip)
    else:
        assert False, "No location for openweathermap call."
    q = "{url}?{loc}&APPID={k}".format(url=api_url, loc=location, k=key)
    response = requests.get(q)
    data = response.json()
    result={
        'zip':zip,
        'time':data['dt'],
        'lat':data['coord']['lat'],
        'lon':data['coord']['lon'],
        'temp':int((data['main']['temp'] - 273.15) * 100)/100.0,
        'humidity':data['main']['humidity']
    }
    return(result)

if __name__ == "__main__":
    print(get_weather(zip="44240"))
    lat=38.55
    lon=-121.46
    print(get_weather(lat=lat, lon=lon))
