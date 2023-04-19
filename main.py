import requests
import typing
import json
import math


YA_API_KEY = '276f8125-0c0e-4290-9bb8-3cdd2adfd213'

__all__ = ["YandexGeocoderException", "UnexpectedResponse", "NothingFound", "InvalidKey"]


class YandexGeocoderException(Exception):
    pass


class UnexpectedResponse(YandexGeocoderException):
    pass


class NothingFound(YandexGeocoderException):
    pass


class InvalidKey(YandexGeocoderException):
    pass


def get_address(lat, lon):
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey={YA_API_KEY}&geocode={lat},{lon}&format=json&sco=latlong&kind=house&results=1&lang=ru_RU"
    result = requests.get(url).json()
    return result


def get_coordinates(address):
    response = requests.get(
    "https://geocode-maps.yandex.ru/1.x/",
    params=dict(format="json", apikey=YA_API_KEY, geocode=address),
    )

    if response.status_code == 200:
        got: dict[str, typing.Any] = response.json()["response"]
        return got
    elif response.status_code == 403:
        raise InvalidKey()
    else:
        raise UnexpectedResponse(
            f"status_code={response.status_code}, body={response.content!r}"
        )


def lonlat_distance(a, b): # Определяем функцию, считающую расстояние между двумя точками, заданными координатами

    degree_to_meters_factor = 111 * 1000 # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def main():

    # получение адреса по координатам
    # lon = '37.587874'
    # lat = '55.73367'
    # result = get_address(lat, lon)
    # print(result)
    # address = result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
    # print(address)

    # получение координат по адресу
    # address = 'Москва, Тухачевского 20 стр 2'
    # result = get_coordinates(address)
    # print(result)
    # print(json.dumps(result, sort_keys=True, indent=4))
    # coordinates = (result['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']).split(' ')
    # print(coordinates)


    # coord1 = '37.587874, 55.73367'
    # coord2 = '37.587880, 55.73380'
    # params = {'waypoints': coord1+'|'+coord2, 'apikey': YA_API_KEY}
    # response = requests.get('https://api.routing.yandex.net/v2/route', params=params)
    # print(response.text)
    # length = response['route']['legs'][0]['steps']
    # length = [i['length'] for i in length]
    # length = sum(length)  # длина маршрута
    # print(length)

    # рассчет дистанции между двумя коорждинатами по прямой
    coord1 = (37.4796, 55.78484)
    coord2 = (37.482120, 55.785697)
    distance = lonlat_distance(coord1, coord2)
    print(distance)


if __name__ == "__main__":
    main()
