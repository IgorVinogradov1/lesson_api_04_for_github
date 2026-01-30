import os
import requests
from datetime import datetime
from helpers import download_image


def download_epic_photos(folder):
    nasa_api_spare_key = 'DEMO_KEY'
    nasa_epic_api_url = 'https://api.nasa.gov/EPIC/api/natural/images'   
    epic_photos_links = []
        
    payload = {'api_key': nasa_api_spare_key}
    response = requests.get(nasa_epic_api_url, params=payload, timeout=10)
    if not response.ok:
        print("NASA API недоступен (скачивание EPIC-фото Земли)")
    else:
        photos_limit = 5
        epic_photos_data = response.json()[:photos_limit]
        for item in epic_photos_data:
            date_obj = datetime.fromisoformat(item['date'].split()[0].replace('Z', '+00:00'))
            year, month, day = f"{date_obj:%Y/%m/%d}".split('/')
            url = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{item["image"]}.png'
            epic_photos_links.append(url)
        for index, url in enumerate(epic_photos_links, start=1):
            filename = f'nasa_epic_{index}.png'
            download_image(url, filename, folder, payload)

def main():
    folder = 'images'
    os.makedirs(folder, mode=0o755, exist_ok=True)
    download_epic_photos(folder)

if __name__ == '__main__':
    main()