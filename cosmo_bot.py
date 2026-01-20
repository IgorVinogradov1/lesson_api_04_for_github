import telegram
import random
import time
import os
import argparse
from dotenv import load_dotenv


def take_images(folder):
    images = []
    try:
        files = os.listdir(folder)
        for filename in files:
            _, img_ext = os.path.splitext(filename)
            if img_ext.lower() in ['.png', '.jpg', '.jpeg', '.gif']:
                img_path = os.path.join(folder, filename)
                images.append(img_path)
        return images
    except Exception as error:
        print(f'Ошибка: {error}')
        return []

def main():
    folder = 'images'
    load_dotenv()
    telegram_token = os.environ['COSMO_TG_TOKEN']
    channel_id = os.environ['CHANNEL_ID']
    bot = telegram.Bot(telegram_token)
    post_interval = 14400

    parser = argparse.ArgumentParser(description='Публикация фото в Telegram-канале')
    parser.add_argument('img', nargs='?', default=None, help='Название фотографии (по умолчанию: публикация случайной фото каждые 4 часа). Справка: [-h]')
    args = parser.parse_args()
    if args.img:
        user_img = args.img
        bot.send_photo(chat_id=channel_id, photo=open(user_img, 'rb'))
    else:
        if take_images(folder):
            images = take_images(folder)
            while True:
                random.shuffle(images)
                for image in images:
                    bot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))
                    time.sleep(post_interval)
        else:
            print('Фотографии отсутсвуют!')

if __name__ == '__main__':
    main()