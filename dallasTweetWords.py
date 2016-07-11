#!/usr/bin/env python

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re

#read the text file with all tweets
text = open('dallasShooting_3.csv').read()
newtext = re.sub(r"http\S+", "", text)
#print(newtext)

#Preprocessing the text a little bit
stopwords = set(STOPWORDS)
stopwords.add("https://t.co")
stopwords.add("http")
stopwords.add("dallas")

#stopwords.add(" C ")
#stopwords.add(" O ")

wordcloud = WordCloud(stopwords=stopwords,
                        ).generate(newtext)
print(wordcloud)
# Open a plot of the generated image.
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

