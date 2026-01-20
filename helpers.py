import os
import requests
from urllib.parse import urlparse, unquote_plus


def get_file_extension(url):
    full_path = unquote_plus(urlparse(url).path, encoding='utf-8', errors='replace')
    *others, img_ext = os.path.splitext(full_path)
    return img_ext

def create_img(url, filename, folder):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(f'{folder}/{filename}', 'wb') as file:
        file.write(response.content)