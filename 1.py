import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
from map_utils import calculate_spn
import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
# toponym_to_find = " ".join(sys.argv[1:])
toponym_to_find = "Москва, ул. Ак. Королева, 12"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "6efcb3a6-70e4-4738-abdf-e75aa2835e20",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    print("Ошибка выполнения запроса:")
    print(response.url)

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = "0.005"
apikey = "65ff937e-7030-4077-b49f-16a9183354c4"
spn = calculate_spn(toponym)
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": spn,
    "l": "map",
    "pt": ",".join([toponym_longitude, toponym_lattitude]) + ",pm2dgl",
    "apikey": apikey,

}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()  # Создадим картинку и тут же ее покажем встроенным просмотрщиком операционной системы
