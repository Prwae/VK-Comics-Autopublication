import random
import os
import logging

import requests
from dotenv import load_dotenv


def download_image(path, params=None):
    url = "https://xkcd.com/info.0.json"

    response = requests.get(url, params=params)
    response.raise_for_status()

    image_number = response.json()["num"]

    final_url = f"https://xkcd.com/{random.randint(1, image_number)}/info.0.json"

    response = requests.get(final_url, params=params)
    response.raise_for_status()

    image_link = response.json()["img"]

    image = requests.get(image_link, params=params)
    image.raise_for_status()

    with open(path, "wb") as file:
        file.write(image.content)

    return response.json()["alt"]


def get_upload_url(access_token, group_id):
    payload = {
        "access_token": access_token,
        "v": "5.131",
        "group_id": group_id

    }

    url = "https://api.vk.com/method/photos.getWallUploadServer"

    response = requests.post(url, params=payload)
    response.raise_for_status()

    return response.json()["response"]["upload_url"]


def upload_photo(access_token, group_id, path, upload_url):
    payload = {
        "access_token": access_token,
        "v": "5.131",
        "group_id": group_id

    }

    with open(path, 'rb') as file:
        payload["photo"] = file

        response = requests.post(upload_url, files=payload)
    response.raise_for_status()

    return response.json()


def save_photo(access_token, group_id, photo, server, hash):
    payload = {
        "access_token": access_token,
        "v": "5.131",
        "group_id": group_id,
        "photo": uploaded_photo_response["photo"],
        "server": uploaded_photo_response["server"],
        "hash": uploaded_photo_response["hash"]
    }

    url = "https://api.vk.com/method/photos.saveWallPhoto"

    response = requests.post(url, data=payload)
    response.raise_for_status()

    return response.json()


def post_photo(access_token, group_id, attachments, message="----"):
    payload = {
        "access_token": access_token,
        "v": "5.131",
        "owner_id": -group_id,
        "attachments": attachments,
        "from_group": 1,
        "message": message

    }

    url = "https://api.vk.com/method/wall.post"

    response = requests.post(url, params=payload)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    load_dotenv()
    access_token = os.environ["VK_ACCESS_TOKEN"]
    group_id = int(os.environ["VK_GROUP_ID"])

    try:
        msg = download_image("comic.jpg")
        upload_url = get_upload_url(access_token, group_id)

        uploaded_photo_response = upload_photo(access_token, group_id, "comic.jpg", upload_url)
        photo = uploaded_photo_response["photo"]
        photo_server = uploaded_photo_response["server"]
        photo_hash = uploaded_photo_response["hash"]

        saved_photo_response = save_photo(access_token, group_id, photo, photo_server, photo_hash)
        attachments = f"photo{saved_photo_response['response'][0]['owner_id']}_{saved_photo_response['response'][0]['id']}"

        post_photo(access_token, group_id, attachments, msg)
    except requests.exceptions.HTTPError:
        logging.exception("Ошибка при запросе к ВК")
    finally:
        os.remove("comic.jpg")