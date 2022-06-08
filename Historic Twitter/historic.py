from textblob import TextBlob
import re
import emoji
import pandas as pd
import json
from shapely.geometry import shape, Point, Polygon, MultiPolygon


# Remove hashtags, mentions, urls
# These elements mostly does not contain user's emotions, but might distract the sentiment analysis process
def tweet_cleaning(text):
    # remove hashtags
    remove_hashtag = ' '.join(re.sub("(#[A-Za-z0-9]+)", " ", text).split())
    # remove mentions
    remove_mentions = ' '.join(re.sub("(@[A-Za-z0-9_]+)", " ", remove_hashtag).split())
    # remove url start with http: or https:
    remove_url = ' '.join(re.sub("^http:\S+ | ^https:\S+", " ", remove_mentions).split())
    return remove_url


# emojis or emoticons contain emotion information a lot, transfer to text
def emoji_transformation(text):
    # express the emoji/emoji unicode into its actual meaning in text
    emoji_meaning = emoji.demojize(text)
    # a dictionary of commonly used emoticons
    emoticon_dict = {':‑(': 'sad', ':(': 'sad', ':)': 'smile', ':-)': 'smile', 'XD': 'laugh', ':‑D': 'laugh',
                     ':D': 'laugh', ';-)': 'winking smile', ':-/': 'frown', ':-D': 'big smile'}
    emoticon_list = list(emoticon_dict.keys())
    word_list = emoji_meaning.split()
    new_word_list = []
    for word in word_list:
        # if there is a emoticon, convert to its meaning
        if word in emoticon_list:
            new_word_list.append(emoticon_dict[word])
        else:
            new_word_list.append(word)
    emoticon_meaning = ' '.join(new_word_list)
    return emoticon_meaning


def main(text):
    remove_useless = tweet_cleaning(text)
    express_emoji = emoji_transformation(remove_useless)
    tweet_cleand = TextBlob(express_emoji)
    # polarity ranges from -1 to 1
    polarity = tweet_cleand.sentiment.polarity
    # if the polarity is from -1 to -0.1, treat as negative
    if -1 <= polarity < -0.1:
        attitude = 'negative'
    # if the polarity is from -0.1 to 0.1, treat as neutral
    elif -0.1 <= polarity <= 0.1:
        attitude = 'neutral'
    # if the polarity is from 0.1 to 1, treat as positive
    elif 0.1 < polarity <= 1:
        attitude = 'positive'
    return attitude


with open('/Users/lynnzky/Documents/GitHub/ccc-project2/Melbourne/melbourne_division.geojson') as f:
    division = json.load(f)


vaccine_geo = pd.read_csv("vaccine_geo.csv")
# add sentiment to each tweet
v_sentiments = []
for i in vaccine_geo['text']:
    senti = main(i)
    v_sentiments.append(senti)
# get coordinates of each tweet
point_list = []
for location in vaccine_geo['coordinates']:
    location = json.loads(location)
    long = float(location[0])
    lat = float(location[1])
    point = Point(long, lat)
    point_list.append(point)
code_list = []
area_list = []
# check which area the point locates in
for feature in division['features']:
    polygon = shape(feature['geometry'])
    for i in point_list:
        if polygon.contains(i):
            code_list.append(feature['properties']['SA3_CODE16'])
            area_list.append(feature['properties']['SA3_NAME16'])
vaccine_geo['sentiments'] = v_sentiments
vaccine_geo['SA3_CODE16'] = code_list
vaccine_geo['SA3_NAME16'] = area_list
vaccine_geo.to_json('vaccine_geo.json', orient="records")



flu_geo = pd.read_csv("flu_geo.csv")
flu_sentiments = []
for j in flu_geo['text']:
    sent = main(j)
    flu_sentiments.append(sent)

flu_point_list = []
for location in flu_geo['coordinates']:
    location = json.loads(location)
    long = float(location[0])
    lat = float(location[1])
    point = Point(long,lat)
    flu_point_list.append(point)
flu_code_list = ['out']*len(flu_point_list)
flu_area_list = ['out']*len(flu_point_list)
# check which area the point locates in
for f in division['features']:
    polygon = shape(f['geometry'])
    for i in flu_point_list:
        if polygon.contains(i):
            index = flu_point_list.index(i)
            flu_code_list[index] = f['properties']['SA3_CODE16']
            flu_area_list[index] = f['properties']['SA3_NAME16']

flu_geo['sentiments'] = flu_sentiments
flu_geo['SA3_CODE16'] = flu_code_list
flu_geo['SA3_NAME16'] = flu_area_list
flu_geo = flu_geo[flu_geo.SA3_CODE16 != 'out']
flu_geo.to_json('flu_geo.json', orient = "records")

