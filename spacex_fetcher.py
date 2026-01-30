import os
import argparse
import requests
from helpers import get_file_extension
from helpers import create_img


def fetch_spacex_last_launch(launch_id, folder):
    spacex_api_url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    spacex_img_links = []
    try:
        response = requests.get(spacex_api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print('Сервер не отвечает!')
        return
    spacex_img_links = response.json()['links']['flickr']['original']
    if not spacex_img_links:
        print('По данному запуску SpaceX фото отсутствуют. Справка: [-h]')
        return
    for index, url in enumerate(spacex_img_links, start=1):
        try:
            img_ext = get_file_extension(url)
            filename = f'spacex_{index}{img_ext}'
            create_img(url, filename, folder)
        except requests.exceptions.RequestException as error:
            print(f'Пропущена ссылка на фото: {url}, ошибка: {error}')
            continue

def main():
    folder = 'images'
    os.makedirs(folder, mode=0o755, exist_ok=True)

    parser = argparse.ArgumentParser(description='Загрузка фото от SpaceX по указанному ID запуска')
    parser.add_argument('id', nargs='?', default='latest', help='Номер запуска (по умолчанию: latest)')
    args = parser.parse_args()
    fetch_spacex_last_launch(args.id, folder)

if __name__ == '__main__':
    main()