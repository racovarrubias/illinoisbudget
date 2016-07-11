#!/usr/bin/env python

from monkeylearn import MonkeyLearn
import os
import csv
from wordcloud import WordCloud

MONKEYLEARN_API_KEY = os.environ.get('MONKEYLEARN_API_KEY')
ml = MonkeyLearn(MONKEYLEARN_API_KEY)

module_id = 'pi_SyZF3Kje' # This is the id of the pipeline that we are using

tweets = []
limit=1000

chunk_size = min(500, limit)
chunk_count, count = 0, 0
chunk = []

#filename = 'illinois_budget.csv'
#filename = 'dallasShooting.csv'
filename = 'dallas.txt'


with open(filename, 'r') as csvfile:

    #dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=';, ')
    #csvfile.seek(0)
    #reader = csv.reader(csvfile, dialect)
    for row in csv.reader(csvfile):
    #for row in reader:
        #print('file row: ', row)
        chunk.append(row)
        count += 1
        chunk_count += 1
        if chunk_count == chunk_size:
            data = {
                "texts": [{"text": sample[0]} for sample in chunk]
            }
            #print("DATA  dictionary",data)
            res = ml.pipelines.run(module_id, data)
            i = 0
            for d in res.result['results']:
            	#print('results', d)
                if d['lang'][0]["label"] == "English" and d['lang'][0]["probability"] > 0.6:
                    tweets.append({"text": chunk[i][0], "sentiment": d["sentiment_tweet"][0]})
                i += 1
            chunk = []
            chunk_count = 0


print('Total tweets:', count)
print('Total tweets in English:', len(tweets))
positive_tweets = [tweet for tweet in tweets if tweet['sentiment']['label'] == 'positive']
print('Positive tweets:', len(positive_tweets))
negative_tweets = [tweet for tweet in tweets if tweet['sentiment']['label'] == 'negative']
print('Negative tweets:', len(negative_tweets))
neutral_tweets = [tweet for tweet in tweets if tweet['sentiment']['label'] == 'neutral']
print('Neutral tweets:', len(neutral_tweets))


sample_size = 5000

values = {
    "negative":{"found":0, "text":""},
    "neutral":{"found":0, "text":""},
    "positive":{"found":0, "text":""}
}

for tweet in tweets:
    sent = tweet["sentiment"]
    if sent["probability"] > 0.6:
        if values[sent["label"]]["found"] < sample_size:
            values[sent["label"]]["text"] += "\n" + tweet["text"]
            values[sent["label"]]["found"] += 1

    if values["negative"]["found"] >= sample_size and values["neutral"]["found"] >= sample_size and values["positive"]["found"] >= sample_size:
        break

module_id = 'ex_y7BPYzNG' # This is the id of the keyword extractor

for sentName, sentDict in values.items():
    print('sentName keywords: \n')
    res = ml.extractors.extract(module_id, [sentDict["text"]])
    for d in res.result[0]:
        print(d["keyword"], res.result)
    sentDict["keywords"] = res.result

#these are the keywords, you can add more
counts = {
    "hearts":{},
    "prayers":{},
    "last night":{},
    "nigel farage":{},
   	"loved ones":{},
   	"shootings":{},
   	"everyone":{},
   	"thoughts":{},
   	"love":{},
   	"violence":{},
   	"good guyv":{},
   	"first law enforcement":{},
   	"law enforcement agency":{},
   	"25-year-old Micah Johnson":{},
   	"Micah Xavier Johnson":{},
   	"robot":{},
   	"attack witness":{},
   	"Black Lives Matter":{},
   	"shooting":{},
   	"police officers":{},
   	"officers":{},
   	"Micah Xavier Johnson":{},
   	"ambush gunman":{},
   	"25-year-old recluse":{},
   	"last night":{},
   	"cops":{},
   	"white people":{},
   	"police":{},
   	"police officers":{},
   	"shooter":{},
   	"shooting":{}
}

for itemName, itemDict in counts.items():
    itemDict["positive"] = 0
    itemDict["neutral"] = 0
    itemDict["negative"] = 0

for tweet in tweets:
    for keyName, keyDict in counts.items():
        if keyName in tweet["text"].lower():
            keyDict[tweet["sentiment"]["label"]] += 1

print(counts)
