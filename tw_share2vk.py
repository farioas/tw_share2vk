#!/usr/bin/env python
# -*- coding: utf-8 -*-
#_author: Sergey Zhuk farioas@gmail.com
# https://github.com/farioas/tw_share2vk #

import urllib
import tweepy
import vk_api
import os.path

# -------TWITTER_APP_CONFIG--------------------------------------------
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
username = ""
# ---------------------------------------------------------------------
# -------VK_APP_CONFIG-------------------------------------------------
app_id = ''  # VK APP ID
app_secret = ''  # VK APP SECRET
login = ''  # Login
passwd = ''  # Pass
# ---------------------------------------------------------------------
path_to_twfile = './tw_file'
twtag = ""

def get_last_tweet():
    if os.path.isfile(path_to_twfile) and os.access(path_to_twfile, os.R_OK):
        print("Tweet file found")
        lasttweet = read_file()
    else:
        print("Tweet file is missing")
        write_file()
        lasttweet = read_file()
    return lasttweet


def read_file():
    with open(path_to_twfile, 'r') as tw_file:
        lasttweet = tw_file.readline()
        print("Last tweet loaded: " + str(lasttweet))
    return lasttweet


def write_file():
    try:
        tweets = tw_auth().user_timeline(id=username, count=1)
    except Exception as error_msg:
        print(error_msg)
        return None
    with open(path_to_twfile, 'w') as tw_file:
        tw_file.write(str(tweets[0].id))


def vk_auth():
    try:
        vk = vk_api.VkApi(login=login, password=passwd, app_id=app_id, token=app_secret, scope=8192)
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return None
    return vk


def tw_auth():
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except Exception as error_msg:
        print(error_msg)
        return None
    return api


def vk_wall_text_photo(text, photo):
    urllib.urlretrieve(photo, 'temp.jpg')
    response = vk_api.VkUpload(vk_auth()).photo_wall('temp.jpg')[0]
    photo = 'photo{}_{}'.format(response['owner_id'], response['id'])
    vk_auth().method('wall.post', {'message': text, 'attachments': photo})


def vk_wal_text(text):
    vk_auth().method('wall.post', {'message': text})


def main():
    for tweet in reversed(
            list(tweepy.Cursor(tw_auth().user_timeline, id=username, include_rts=False, exclude_replies=True,
                               include_entities=True, since_id=get_last_tweet()).items())):
        tweet_content = tweet.text
        if twtag in str(tweet.entities.get('hashtags')):
            print("Tweet.id: " + str(tweet.id))
            print("Tweet.txt: " + tweet_content.encode("utf-8"))
            for url in tweet.entities['urls']:
                tweet_content = tweet_content.replace(url['url'], url['expanded_url'])
            if 'media' in tweet.entities:
                for image in tweet.entities['media']:
                    photo = image['media_url'] + ":orig"
                    print("Tweet.img: " + str(photo))
                    vk_wall_text_photo(tweet_content.encode("utf-8"), photo)
                    print("Tweet sent on wall with photo")
            else:
                vk_wal_text(tweet_content.encode("utf-8"))
                print("Tweet sent on wall")
            print("\n")
    write_file()
    print("Last tweet saved")


if __name__ == '__main__':
    main()
