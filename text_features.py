import itertools
import nltk
import numpy
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem.wordnet import WordNetLemmatizer
from scipy.stats import stats
from sklearn.feature_extraction.text import CountVectorizer
import csv_read_write

DATA_PATH = "training_data.csv"
def text_extraction(data):
    dataframe = pd.read_csv(data, low_memory=False)
    motivation = dataframe["custom.Motivation"].tolist()
    notes = dataframe["custom.Notes"].tolist()
    occupation = dataframe["custom.Occupation"].tolist()
    recreation = dataframe["custom.Recreation"].tolist()
    for i in range(len(motivation)):
        notes[i] = str(motivation[i])+str(notes[i])+str(occupation[i])+str(recreation[i])
    return np.array(notes)


# data
def preprocessing(data):
    text_str_list = []
    for i in data:
        text_str = ""
        for j in i:
            if str(j) != "nan":
                str(j).replace("-","")
                text_str = text_str + " " + str(j)
        text_str_list.append(text_str)
    # Preprocessing
    stops = stopwords.words("english")
    corpus = []
    for i in data:
        text_str = re.sub("[^a-zA-Z]", " ", i)
        text_str = text_str.lower()
        text_str = text_str.split()
        lemmed = [WordNetLemmatizer().lemmatize(word) for word in text_str if not word in set(stops)]
        tocken = " ".join(lemmed)
        corpus.append(tocken)
    print("-----------------Finish Preprocessing")
    return corpus


# Priority word list
def get_priority_list(corpus):
    priority_word_list = pd.read_csv("data/priority_word_list_vinn.csv", low_memory=False)
    priority_word_list = np.array(priority_word_list["Word"])
    priority_result = []
    for i in corpus:
        each_result = []
        for j in priority_word_list:
            if j in i:
                each_result.append(1)
            else:
                each_result.append(0)
        priority_result.append(each_result)
    print("-----------------Finish get priority list")
    return priority_result


# Bag of Words
def bag_of_words(corpus):
    matrix = CountVectorizer(max_features=100)
    bow_list = matrix.fit_transform(corpus).toarray()
    print("-----------------Finish Bag of Words")
    return bow_list


# Sentiment analysis
def sentiment_analysis(corpus):
    sentiment_list = []
    sia = SentimentIntensityAnalyzer()
    for i in corpus:
        score = sia.polarity_scores(i)
        if score['compound'] < 0:
            f1=-10
        else:
            f1=10
        each_result  = []
        each_result.append(round(score['neg']*10))
        each_result.append(round(score['neu'] * 10))
        each_result.append(round(score['pos'] * 10))
        each_result.append(round(score['compound'] * 10))
        each_result.append(f1)
        sentiment_list.append(each_result)
    print("-----------------Finish Sentiment Analysis")
    return sentiment_list


def frequency_hist(data):
    text_str = []
    for i in data:
        str_list = i.split(" ")
        for k in str_list:
            text_str.append(k)
    fdist = nltk.FreqDist(text_str)
    return fdist.most_common(500)


def freq_split_list():
    sale = frequency_hist(preprocessing(text_extraction("data/text_data_3k_sale&deal.csv")))
    dead = frequency_hist(preprocessing(text_extraction("data/text_data_3k_dead.csv")))
    sale_list = []
    dead_list = []
    same_sale_list = []
    same_dead_list = []
    for i in range(len(sale)):
        for j in range(len(dead)):
            if sale[i][0] == dead[j][0]:
                same_sale_list.append(sale[i])
                same_dead_list.append(dead[j])
                break
    for k in sale:
        if k not in same_sale_list:
            sale_list.append(k[0])
    for k in dead:
        if k not in same_dead_list:
            dead_list.append(k[0])
    same_word_features = []
    for i in range(len(same_sale_list)):
        if abs(same_dead_list[i][1] - same_sale_list[i][1]) > 100:
            same_word_features.append(same_dead_list[i][0])

    return sale_list, dead_list, same_word_features


def get_split_features(corpus):
    sale_list, dead_list, same_list = freq_split_list()
    feature_result = []
    for i in corpus:
        sale_result = []
        dead_result = []
        same_result = []
        for j in sale_list:
            sale_result.append(i.count(j))
        for k in dead_list:
            dead_result.append(-i.count(k))
        for l in same_list:
            same_result.append(-i.count(l))
        feature_result.append(sale_result+dead_result+same_result)
    print("-----------------Finish get split feature list")
    return feature_result


def text_features_extraction(data):
    label = np.array(pd.read_csv("data/label.csv", low_memory=False))
    profile_feature = np.array(pd.read_csv("data/profile_features.csv", low_memory=False)).transpose()
    corpus = preprocessing(text_extraction(data))
    split_feature_list = numpy.array(get_split_features(corpus)).transpose()
    sentiment_feature_list = numpy.array(sentiment_analysis(corpus)).transpose()
    priority_list = numpy.array(get_priority_list(corpus)).transpose()
    frequency_list = numpy.array(bag_of_words(corpus)).transpose()
    corr_list = []
    combine_list = list(itertools.chain(sentiment_feature_list, split_feature_list, priority_list, frequency_list, profile_feature))
    high_corr_list = []
    feature_num = 0
    for k in combine_list:
        correlation, p_value = stats.kendalltau(k, label)
        corr_list.append(correlation)
        if correlation > 0:
            high_corr_list.append(k)
            csv_read_write.list_write_csv("data/All_features.csv", feature_num, k)
            feature_num+=1
    re_list = numpy.array(high_corr_list).transpose()
    print("-----------------Finish get all feature list")
    return re_list


#text_features_extraction(DATA_PATH)

