# -*- coding: utf-8 -*-
"""
Vladislav Selivanov
wooterland@fastmail.com
2020-2021
"""

import re
import requests
import time

import telebot

from sakugabot_vk import upload_video
from tokens import tg_bot_token, tg_channel_name

while True:
    # Делаю запрос к api Sakugabooru
    payload = {'limit': 100}
    r = requests.get('https://www.sakugabooru.com/post.json', params=payload)
    r.json = r.json()
    for post in r.json:
        id = post['id']
        file_url = post['file_url']
        tags = post['tags']
        file_ext = post['file_ext']
        size = post['file_size']
        score = post['score']
        title = ''
        artist = ''
        other = ''

        # Запрос на получения списка тегов
        payload = {'limit': 0}
        tag = requests.get('https://www.sakugabooru.com/tag.json', params=payload)
        tag.json = tag.json()

        for tag in tag.json:
            name = tag['name']
            type = tag['type']

            # Очистка тегов и разделение их на типы
            tags_split = tags.split()
            if name in tags_split:
                name = re.sub(r"[':()!+]+", '', name)
                name = re.sub(r'\W+', '_', name)

                if type == 3:
                    title = ' #' + name + ''.join(title)
                if type == 1:
                    artist = ' #' + name + ''.join(artist)
                if type == 0:
                    other = ' #' + name + ''.join(other)
                if type >= 4:
                    other = ' #' + name + ''.join(other)

        if title == '':
            title = '#title_unknow'
        if artist == '':
            artist = '#artist_unknow'

        all_tags = f'Title:{title}\nArtist:{artist}\nOther:{other}'

        # Проверяю чтобы в документ записывались и отправлялись только видео с новым id
        video_delete = False

        post_id = open('post_id.txt', 'r+')
        for line in post_id:
            if int(line) == id:
                print(time.ctime(), '❌ [TG] Post already exist')
                video_delete = True
                break
            elif size > 18000000:
                print(time.ctime(), '❌[TG] BFF')
                video_delete = True
                break
        else:
            tb = telebot.TeleBot(tg_bot_token)
            tb.send_document(tg_channel_name, file_url, caption=all_tags)

            if file_ext in ['mp4', 'webm'] and score >= 70:
                print('Score =', score)
                upload_video(file_url, all_tags, artist, title, video_delete)
            else:
                print(time.ctime(), '❌ [VK] Need mp4/webm or score < 70')

            print(time.ctime(), '✅ [TG] Publish post with ID: ', id)
            post_id = open('post_id.txt', 'a+')
            post_id.write('%s\n' % id)
            time.sleep(5400)

    print(time.ctime(), '✅ [TG] Add 100 post from Sakugabooru')
    time.sleep(1)
