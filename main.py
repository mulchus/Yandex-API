import requests
import typing
import json
import math
import smtplib

from environs import Env
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


__all__ = ["YandexGeocoderException", "UnexpectedResponse", "NothingFound", "InvalidKey"]


class YandexGeocoderException(Exception):
    pass


class UnexpectedResponse(YandexGeocoderException):
    pass


class NothingFound(YandexGeocoderException):
    pass


class InvalidKey(YandexGeocoderException):
    pass


def get_address(lat, lon, ya_api_key):
    url = 'https://geocode-maps.yandex.ru/1.x/'
    response = requests.get(url,
                            params=dict(format="json",
                                        apikey=ya_api_key,
                                        geocode=f'{lat},{lon}',
                                        sco='latlong',
                                        kind='house',
                                        results=1,
                                        lang='ru_RU'
                                        )
                            )
    return response.json()


def get_coordinates(address, ya_api_key):
    url = 'https://geocode-maps.yandex.ru/1.x/'
    response = requests.get(url,
                            params=dict(format="json", apikey=ya_api_key, geocode=address),
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


def lonlat_distance(a, b):  # Определяем функцию, считающую расстояние между двумя точками, заданными координатами
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
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
    env = Env()
    env.read_env()
    ya_api_key = env('YA_API_KEY')

    # отправка сообщения на почту
    # bot_mail_pasword = env('BOT_MAIL_PASWORD')
    # msg = MIMEMultipart()
    # msg['From']  = env('BOT_MAIL')
    # msg['To']  = env('CLIENT_MAIL')
    # msg['Subject'] = 'Subscription of mail # 1'
    # message = 'New message'
    # msg.attach(MIMEText(message, 'plain'))
    #
    # smtpObj = smtplib.SMTP('smtp.mail.ru: 587')
    # smtpObj.starttls()
    #
    # smtpObj.login(msg['From'], bot_mail_pasword)
    # smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())
    # smtpObj.quit()

    # получение адреса по координатам
    # lon = '37.587874'
    # lat = '55.73367'
    # result = get_address(lat, lon, ya_api_key)
    # address = result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
    # print(address)

    # получение координат по адресу
    # address = 'Москва, улица Льва Толстого, 16'
    # result = get_coordinates(address, ya_api_key)
    # print(json.dumps(result, sort_keys=True, indent=4))
    # coordinates = (result['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']).split(' ')
    # print(coordinates)

    # coord1 = '37.587874, 55.73367'
    # coord2 = '37.587880, 55.73380'
    # params = {'waypoints': coord1+'|'+coord2, 'apikey': ya_api_key}
    # response = requests.get('https://api.routing.yandex.net/v2/route', params=params)
    # print(response.text)
    # length = response['route']['legs'][0]['steps']
    # length = [i['length'] for i in length]
    # length = sum(length)  # длина маршрута
    # print(length)

    # рассчет дистанции между двумя коорждинатами по прямой
    # coord1 = (37.4796, 55.78484)
    # coord2 = (37.482120, 55.785697)
    # distance = lonlat_distance(coord1, coord2)
    # print(distance)


if __name__ == "__main__":
    main()
