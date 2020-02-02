import datetime
import json
import urllib.request
import urllib.parse


def get_result(url: str) -> dict:
    '''
    This function takes a URL and returns a Python dictionary representing the
    parsed JSON response.
    '''
    response = None
    try:
        response = urllib.request.urlopen(url)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)
    finally:
        if response != None:
            response.close()
            
if __name__ == '__main__':
    print(get_result('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2020-02-01&maxlatitude=42.010122&minlatitude=32.467133&maxlongitude=-113.881617&minlongitude=-124.718872&minmagnitude=2'))