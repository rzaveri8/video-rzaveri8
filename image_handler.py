import requests
import config
import os
import tweepy
#import pandas as pd
import csv
import datetime
import time
import json
from flask import jsonify
import math
from PIL import Image
from PIL import ImageDraw
from io import BytesIO

def format_tweet_text(text):
    # if full text is longer than 25 characters, add a new line so it wraps
    if len(text) > 25:
        i = 0
        res = '\n'.join(text[i:i + 25] for i in range(0, len(text), 25))
        new_lines = math.floor(len(text) // 25)
        return res, new_lines
    else:
        return text, 1


def getImage(tweet, image):
    url = tweet.entities['media'][0]['media_url_https']
    bytes =  requests.get(url)
    photo = Image.open(BytesIO(bytes.content))
    image.paste(photo, (10, 130))

def tweet_video(all_tweets, screen_name): #DOES NOT CHECK FOR IMAGES & CHANGE THIS - SIZE FOR IMAGES>..
    index = 0
    for tweet in all_tweets:
        path = make_dir(screen_name)
        if (datetime.datetime.now() - tweet.created_at).days < 1:
            wrapped_text, new_lines = format_tweet_text(tweet.full_text)
            img_height = 125
            img = Image.new('RGB', (200, img_height), (255, 255, 255))
            d = ImageDraw.Draw(img)
            d.text((10, 10), wrapped_text.encode(
                'cp1252', 'ignore'), fill=(0, 0, 0))
        # IF THERE IS AN IMAGE
            if 'media' in tweet.entities:
                    getImage(tweet, img)
            image_name = "tweet" + str(index) + ".png"
            img.save(path + image_name)
            index += 1

def check_dir(path): #from https://thispointer.com/how-to-create-a-directory-in-python/
    try:
        os.mkdir(path)
    except OSError:
        print ("directory %s already exists" % path)
    else:
        print ("Successfully created the directory %s " % path)
    return True

def make_dir(screen_name):
    # create directories for images.
    check_dir(os.getcwd()+ "/MyVids")
    path = os.getcwd()+ "/MyImages"
    check_dir(path)
    path = path + '/' + screen_name + '/'
    check_dir(path)
    return path

