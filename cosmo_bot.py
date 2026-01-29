import telegram
import random
import time
import os
import argparse
from dotenv import load_dotenv


def take_images(folder):
    images = []
    files = os.listdir(folder)
    for filename in files:
        _, img_ext = os.path.splitext(filename)
        if img_ext.lower() in ['.png', '.jpg', '.jpeg', '.gif']:
            img_path = os.path.join(folder, filename)
            images.append(img_path)
    return images

def post_random_photo(bot, channel_id, images, post_interval):
    while True:
        random.shuffle(images)
        for image in images:
            with open(image, 'rb') as photo_file:
                bot.send_photo(chat_id=channel_id, photo=photo_file)
            time.sleep(post_interval)

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
        with open(user_img, 'rb') as photo_file:
            bot.send_photo(chat_id=channel_id, photo=photo_file)
    else:
        try:
            images = take_images(folder)
            if images:
                post_random_photo(bot, channel_id, images, post_interval)
            else:
                print('Фотографии отсутствуют!')
        except FileNotFoundError:
            print('Папка "images" отсутствует')

if __name__ == '__main__':
    main()