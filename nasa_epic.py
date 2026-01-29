import os
import requests
from helpers import create_img


def download_epic_photos(folder):
    nasa_api_spare_key = 'DEMO_KEY'
    nasa_epic_api_url = 'https://api.nasa.gov/EPIC/api/natural/images'   
    epic_photos_links = []
    try:
        payload = {'api_key': nasa_api_spare_key}
        response = requests.get(nasa_epic_api_url, params=payload, timeout=10)
        if response.status_code != 200:
            print("NASA API недоступен (скачивание EPIC-фото Земли)")
        else:
            epic_photos_data = response.json()[:5]
            for item in epic_photos_data:
                year, month, day = item['date'].split()[0].split('-')
                img_url = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{item['image']}.png?api_key={nasa_api_spare_key}'
                epic_photos_links.append(img_url)
            for index, url in enumerate(epic_photos_links, start=1):
                filename = f'nasa_epic_{index}.png'
                create_img(url, filename, folder)
    except Exception as error:
        print(f'Ошибка соединения: {error}')

def main():
    folder = 'images'
    os.makedirs(folder, mode=0o755, exist_ok=True)
    download_epic_photos(folder)

if __name__ == '__main__':
    main()