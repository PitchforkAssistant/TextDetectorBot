import requests
from PIL import Image


def DownloadImage(url):
    if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"):
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return None
        image = image.open(response.raw).convert("RGB")
        return image
    return None
