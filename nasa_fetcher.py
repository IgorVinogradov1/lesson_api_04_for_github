import os
import requests
from dotenv import load_dotenv
from helpers import get_file_extension
from helpers import create_img


def fetch_nasa_img(nasa_api_key, nasa_api_spare_key, nasa_api_url, folder):      
    for api_key, count in [(nasa_api_key, '50'), (nasa_api_spare_key, '5')]:
        try:
            payload = {'api_key': api_key, 'count': count}
            response = requests.get(nasa_api_url, params=payload)
            response.raise_for_status()
            nasa_img_data = response.json()
            break
        except:
            continue
    else:
        print("Ключи NASA API не работают!")
        return
    nasa_img_url = []
    for item in nasa_img_data:
        if item['media_type'] == 'image':
            nasa_img_url.append(item['url'])
    for index, url in enumerate(nasa_img_url, start=1):
        img_ext = get_file_extension(url)
        filename = f'nasa_apod_{index}{img_ext}'
        create_img(url, filename, folder)

def main():
    folder = 'images'
    os.makedirs(folder, mode=0o755, exist_ok=True)
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_TOKEN']
    nasa_api_spare_key = 'DEMO_KEY'
    nasa_api_url = 'https://api.nasa.gov/planetary/apod'
    fetch_nasa_img(nasa_api_key, nasa_api_spare_key, nasa_api_url, folder)

if __name__ == '__main__':
    main()