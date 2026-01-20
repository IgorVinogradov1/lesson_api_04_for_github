import os
import argparse
import requests
from helpers import get_file_extension
from helpers import create_img


def fetch_spacex_last_launch(spacex_api_url, folder):
    spacex_img_links = []
    try:
        response = requests.get(spacex_api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print('Сервер не отвечает!')
    spacex_img_links = response.json()['links']['flickr']['original']
    if not spacex_img_links:
        print('По данному запуску SpaceX фото отсутствуют. Справка: [-h]')
        return
    for index, url in enumerate(spacex_img_links, start=1):
        try:
            img_ext = get_file_extension(url)
            filename = f'spacex_{index}{img_ext}'
            create_img(url, filename, folder)
        except Exception as error:
            print(f'Пропущена ссылка на фото: {url}, ошибка: {error}')
            continue

def main():
    folder = 'images'
    os.makedirs(folder, mode=0o755, exist_ok=True)

    parser = argparse.ArgumentParser(description='Загрузка фото от SpaceX по указанному ID запуска')
    parser.add_argument('id', nargs='?', default=None, help='Номер запуска (по умолчанию: latest)')
    args = parser.parse_args()
    if args.id:
        launch_id = args.id
        spacex_api_url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
        fetch_spacex_last_launch(spacex_api_url, folder)
    else:
        spacex_api_url = 'https://api.spacexdata.com/v5/launches/latest'
        fetch_spacex_last_launch(spacex_api_url, folder)

if __name__ == '__main__':
    main()