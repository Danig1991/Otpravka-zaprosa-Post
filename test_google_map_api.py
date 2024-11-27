from random import uniform, randint
from faker import Faker

import requests


class TestGoogleMapApi:
    def __init__(self, base_url, key):
        self.base_url = base_url
        self.key = key

    # получить новую локацию
    def get_new_location(self):
        return {
            "location": {
                "lat": round(uniform(-100, 100), 6),
                "lng": round(uniform(-100, 100), 6)
            },
            "accuracy": randint(10, 100),
            "name": "Frontline house",
            "phone_number": Faker("ru_Ru").phone_number(),
            "address": "29, side layout, cohen 09",
            "types": [
                "shoe park",
                "shop"
            ],
            "website": "http://google.com",
            "language": "French-IN"
        }

    # отправить метод POST
    def send_post_method(self):
        post_resourse = "/maps/api/place/add/json"
        full_post_url = self.base_url + post_resourse + self.key
        return requests.post(full_post_url, json=self.get_new_location())

    # создать 5 place_id и поместить их в текстовый файл
    def five_place_id_in_text_file(self):
        number = 1
        while number <= 5:
            place_id = self.send_post_method().json()["place_id"]
            with open("data.txt", "a", encoding="utf-8") as file:
                file.write(place_id + "\n")
            print(f"В файл \"data.txt\" добавлен {number} place_id - \"{place_id}\"")
            number += 1

    # отправить метод Get
    def send_get_method(self, place_id):
        get_resourse = "/maps/api/place/get/json"
        full_get_url = self.base_url + get_resourse + self.key + "&place_id=" + place_id
        return requests.get(full_get_url)

    # убедиться, что данные place_id существуют
    def check_place_id(self):
        with open("data.txt", "r", encoding="utf-8") as file:
            for place_id in file:
                assert self.send_get_method(place_id.strip()).status_code == 200, \
                    f"Ошибка: place_id - {place_id.strip()} не существует!"
                print(f"Запрос по place_id - {place_id.strip()} выполнен успешно")

    # очистить текстовый файл
    def clear_text_file(self):
        with open("data.txt", 'w'):
            pass
        print(f"Файл \"data.txt\" очищен")


if __name__ == "__main__":
    base_url = "https://rahulshettyacademy.com"
    key = "?key=qaclick123"
    start_test = TestGoogleMapApi(base_url, key)
    start_test.five_place_id_in_text_file()
    start_test.check_place_id()
    start_test.clear_text_file()
