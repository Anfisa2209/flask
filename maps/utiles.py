from io import BytesIO

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "format": "json"}


def get_object(address):
    geocoder_params['geocode'] = address
    response = requests.get(geocoder_api_server, geocoder_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError('Ошибка выполнения запроса.')
    feature = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    return feature if feature else None


def get_ll_spn(toponym: dict):
    object_ll = ','.join(toponym['Point']['pos'].split())
    envelope = toponym['boundedBy']['Envelope']
    left, bottom = envelope['lowerCorner'].split()
    right, top = envelope['upperCorner'].split()
    dx = abs(float(left) - float(right)) / 2
    dy = abs(float(top) - float(bottom)) / 2
    object_spn = f"{dx},{dy}"
    return object_ll, object_spn


def get_static_api_image(object_ll, z=12, theme='light', pt=''):
    map_params = {
        "ll": object_ll,
        'apikey': "66a74a17-2df9-44cc-aa42-006036c7be2b",
        'z': z,
        'theme': theme,
        'pt': pt
    }

    map_api_server = "https://static-maps.yandex.ru/v1?"
    session = requests.Session()
    retry = Retry(total=10, connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    response = session.get(map_api_server, params=map_params)
    if response:
        return response.content
    else:
        return None


def show_image(content):
    im = BytesIO(content)
    return im
    # image = Image.open(im)
    # image.show()
