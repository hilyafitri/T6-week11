"""
Nama  : Hilya Fitri
NIM   : F1D02310009
Kelas : C

"""

import requests

BASE_URL = "https://api.pahrul.my.id/api/posts"
TIMEOUT = 10


class ApiService:

    @staticmethod
    def get_posts():
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_post_detail(post_id):
        response = requests.get(
            f"{BASE_URL}/{post_id}",
            timeout=TIMEOUT
        )

        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_post(data):
        response = requests.post(
            BASE_URL,
            json=data,
            timeout=TIMEOUT
        )

        if response.status_code == 422:
            raise Exception("422 - Slug sudah digunakan")

        response.raise_for_status()
        return response.json()

    @staticmethod
    def update_post(post_id, data):
        response = requests.put(
            f"{BASE_URL}/{post_id}",
            json=data,
            timeout=TIMEOUT
        )

        if response.status_code == 422:
            raise Exception("422 - Slug sudah digunakan")

        response.raise_for_status()
        return response.json()

    @staticmethod
    def delete_post(post_id):
        response = requests.delete(
            f"{BASE_URL}/{post_id}",
            timeout=TIMEOUT
        )

        response.raise_for_status()
        return response.json()