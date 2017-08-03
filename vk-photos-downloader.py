#!/usr/bin/python3.5
#-*- coding: UTF-8 -*-

import vk, os, time
from urllib.request import urlretrieve

token = input("Enter a token: ")  # vk token

#Authorization
session = vk.Session(access_token=str(token))
vk_api = vk.API(session)

count = 0  # count of down. photos
perc = 0  # percent of down. photos
breaked = 0  # unsuccessful down.
time_now = time.time()  # current time

url = input("Enter a URL of album: ")  # url of album
folder_name = input("Enter a name of folder for download photos: ")  # fold. for photo

print("-------------------------------------------")

owner_id = url.split('album')[1].split('_')[0]  # id of owner
album_id = url.split('album')[1].split('_')[1][0:-1]  # id of album
photos_count = vk_api.photos.getAlbums(owner_id=owner_id, album_ids=album_id)[0]['size']  # count of ph. in albums
album_title = vk_api.photos.getAlbums(owner_id=owner_id, album_ids=album_id)[0]['title']  # albums title
photos_information = vk_api.photos.get(owner_id=owner_id, album_id=album_id)  # dictionaries of photos information

print("A title of album - {}".format(album_title))
print("Photos in album - {}".format(photos_count))
print("------------------")

if not os.path.exists(folder_name):
    os.makedirs(folder_name + '/' + album_title)  # creating a folder for download photos
    print("Created a folder for photo.")
    print("---------------------------")
else:
    print("A folder with this name already exists!")
    exit()

photos_link = []  #  photos link

for i in photos_information:
    photos_link.append(i['src_xxbig'])

photo_name = 0  # photo name

for i in photos_link:
    photo_name += 1
    try:
        urlretrieve(i, folder_name + '/' + album_title + '/' + str(photo_name) + '.jpg')  # download photos
        count += 1
        perc = (100 * count) / photos_count
        print("Download {} of {} photos. ({}%)".format(count, photos_count, round(perc, 2)))
    except:
        print("An error occurred, file skipped.")
        breaked += 1

minutes = int((time.time() - time_now) // 60)
seconds = int((time.time() - time_now) % 60)

print("------------------------")
print("Successful download {} photos.".format(count))
print("Skipped {} photos.".format(breaked))
print("Time spent: {}.{} minutes.".format(minutes, seconds))


