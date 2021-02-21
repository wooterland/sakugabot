# -*- coding: utf-8 -*-
"""
Vladislav Selivanov
wooterland@fastmail.com
2021
"""

import os
import time

import requests
import vk_api

from tokens import vk_login, vk_password, vk_group_id, vk_album_id


def download_video(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    f.write(chunk)
        f.close()
    return local_filename


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def upload_video(file_url, all_tags, artist, title, video_delete):
    vk_session = vk_api.VkApi(
        login=vk_login,
        password=vk_password,
        auth_handler=auth_handler,
        scope=471568,
        api_version='5.126',
    )
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    # Загрукза видео
    upload = vk_api.VkUpload(vk_session)

    video = upload.video(
        video_file=download_video(file_url),
        name=f'{title} ({artist})',
        description=all_tags,
        is_private=0,
        wallpost=0,
        group_id=vk_group_id,
        album_id=vk_album_id,
        privacy_view='all',
        repeat=1
    )

    vk_video_url = 'https://vk.com/video{}_{}'.format(
        video['owner_id'], video['video_id']
    )

    print(time.ctime(), '✅ [VK] Upload video: ', vk_video_url)

    if vk_video_url or video_delete:
        os.remove(download_video(file_url))

    # Публикация видео на стене
    vk = vk_session.get_api()

    wall_post = vk.wall.post(
        owner_id=video['owner_id'],
        from_group=1,
        message=all_tags,
        attachments='video{}_{}'.format(video['owner_id'], video['video_id'])
    )

    print(time.ctime(), '✅ [VK] Post id: ', wall_post)
