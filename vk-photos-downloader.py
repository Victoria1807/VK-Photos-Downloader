#!/usr/bin/python3.5
#-*- coding: UTF-8 -*-

import vk, os, time
from urllib.request import urlretrieve

token = input("Enter API token (access_token): ") # vk token


#Authorization
session = vk.Session(access_token=str(token))
vk_api = vk.API(session,v='5.102')

count = 0  # count of down. photos
perc = 0  # percent of down. photos
skipped = 0  # unsuccessful down.
time_now = time.time()  # current time

url = "'" + input("Enter a URL of an album: ") + "'"  # url of album
folder_name = input("Enter a folder name for the downloaded photos: ")  # fold. for photo
print("-------------------------------------------")

owner_id = url.split('album')[1].split('_')[0]  # id of owner
album_id = url.split('album')[1].split('_')[1][0:-1]  # id of album

get_album = vk_api.photos.getAlbums(owner_id=owner_id, album_ids=album_id)

photos_count = get_album['items'][0]['size']  # count of ph. in albums
album_title = get_album['items'][0]['title']  # albums title

collect = True
collected = 0

print("Album title: {}".format(album_title))
print("Photos in album: {}".format(photos_count))
print("---------------------------")

links = []

while collect is True:
    data = vk_api.photos.get(owner_id=owner_id, album_id=album_id, count=200, offset=collected)['items']
    collected = (len(data) + collected)
    print("Collecting data " + str(collected) + "/" + str(photos_count) + " ..")

    for item in data:
        largest = 0
        url = ''
        for i in item['sizes']:
            if i['width'] > largest:
                url = i['url']
                largest = i['width']
        if url:
            links.append(url)


    if collected >= photos_count or len(data) == 0:
        collect = False
    else:
        time.sleep(1)

if not os.path.exists(folder_name):
    os.makedirs(folder_name + '/' + album_title)  # creating a folder for download photos

print("Saving to: " + (folder_name + '/' + album_title))
print("---------------------------")

download_count = 0

for url in links:
    download_count += 1
    try:
        try:
            filename = url.split("/")[-1]
        except:
            filename = (download_count + ".jpg")

        destination = (folder_name + '/' + album_title + '/' + filename)

        if not os.path.isfile(destination):
            urlretrieve(url, destination)  # download photo
        else:
            skipped += 1

        perc = (100 * download_count) / photos_count
        print("Downloaded {} of {} photos. ({}%)".format(download_count, photos_count, round(perc, 2)))
    except:
        print("An error occurred, file skipped.")
        skipped += 1

minutes = int((time.time() - time_now) // 60)
seconds = int((time.time() - time_now) % 60)

print("---------------------------")
print("Successful downloaded {} photos.".format(count))
print("Skipped {} photos.".format(skipped))
print("Time spent: {}.{} minutes.".format(minutes, seconds))