import nltk
import string
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import markovify

from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import os
import pickle
import re
import math

from mysite import settings

MAX_TOKEN_LENGTH = 31
MAX_SENT_TOKEN_LENGTH = 100


FIG_X = 19.2
FIG_Y = 10.8
BIG_X = 19.2
BIG_Y = 10.8

TOP_MOST_COMMON_NUM = 500
MAX_TOKENS = 5000

# _____________________________________________________________ COMMON _________

def tokenize(text):
    # firstly let's apply nltk tokenization
    tokens = nltk.word_tokenize(text)
    tokens = tokens[:MAX_TOKENS]

    # let's delete punctuation symbols
    tokens = [i for i in tokens if (i not in string.punctuation)]

    # deleting stop_words
    # stop_words = stopwords.words('russian')
    # stop_words.extend(["--", "''", "``", "..", "x", '', 'что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...'])
    # tokens = [i for i in tokens if (i not in stop_words)]

    remove_this = ["--", "''", "``", "..", "x", '', '—', '–', 'к', 'на', '...',]
    tokens = [i for i in tokens if (i not in remove_this)]

    # cleaning words
    tokens = [re.sub("\d|«|»|…", "", i).lower() for i in tokens]
    tokens = [i for i in tokens if (i not in ['', '...'])]
    return tokens

def cleaned(text):
    tokens = tokenize(text)
    cleaned_text = ''
    for token in tokens:
        cleaned_text += token + ' '
    return cleaned_text

def save_obj(fn, obj):
    try:
        f = open(fn, 'wb')
        pickle.dump(obj, f) # помещаем объект в файл
        f.close()
        return True
    except:
        return False

def load_obj(fn):
    try:
        f = open(fn, 'rb')
        obj = pickle.load(f)
        return obj
    except:
        return False

# _______________________________________________________ MENDENHALL ___________

def plot_mendenhall(text):
    tokens = tokenize(text)
    token_lengths = [len(token) for token in tokens]
    dist = nltk.FreqDist(token_lengths)

    freqs = []
    for i in range(1, MAX_TOKEN_LENGTH):
        freqs.append(dist.freq(i))

    fig = plt.figure(figsize=[FIG_X, FIG_Y])
    ax = fig.add_subplot(111)
    plot = dist.plot(30, title='Mendenhall')
    fn = os.path.join(settings.MEDIA_ROOT, 'graphs', 'mendenhall.png')
    fig.savefig(fn)
    fn = os.path.join(settings.MEDIA_URL, 'graphs', 'mendenhall.png')

    fig1 = plt.figure(figsize=[FIG_X, FIG_Y])
    ax1 = fig1.add_subplot(111)
    xpoints = np.array(range(1, MAX_TOKEN_LENGTH))
    ypoints = np.array(freqs)
    ax1.plot(xpoints, ypoints)
    ax1.set_title("Mendenhall frequences")
    fn1 = os.path.join(settings.MEDIA_ROOT, 'graphs', 'mendenhall_freqs.png')
    fig1.savefig(fn1)
    fn1 = os.path.join(settings.MEDIA_URL, 'graphs', 'mendenhall_freqs.png')

    return fn, fn1

def get_mendenhall(text):
    tokens = tokenize(text)
    token_lengths = [len(token) for token in tokens]
    dist = nltk.FreqDist(token_lengths)
    freqs = []
    for i in range(1, MAX_TOKEN_LENGTH):
        freqs.append(dist.freq(i))
    return freqs

def mendenhall_distance(object1, object2):
    text1 = object1.text()
    text2 = object2.text()
    freqs1 = get_mendenhall(text1)
    freqs2 = get_mendenhall(text2)
    d = 0
    for i in range(len(freqs1)):
        l = 100 * (freqs1[i] - freqs2[i])
        d += l * l * l * l
    # d = math.sqrt(d)
    # d *= 1000000
    return d

def plot_mendenhall_array(objects, param='mendenhall'):
    fig = plt.figure(figsize=[BIG_X, BIG_Y])
    ax = fig.add_subplot(111)
    name = None
    for object in objects:
        text = object.text()
        y = get_mendenhall(text)
        dim = len(y)
        xpoints = np.array(range(1, dim+1))
        ypoints = np.array(y)
        ax.plot(xpoints, ypoints, label=f'({object.id}) {object.label()}')

    name = param + '_multy.png'
    ax.legend()
    fn = os.path.join(settings.MEDIA_ROOT, 'graphs', name)
    fig.savefig(fn)
    return name


# _______________________________________________________ mendenhall_s _________

def plot_mendenhall_s(text):
    tokens = sent_tokenize(text)
    token_lengths = [len(token) for token in tokens]
    dist = nltk.FreqDist(token_lengths)

    freqs = []
    for i in range(1, MAX_SENT_TOKEN_LENGTH):
        freqs.append(dist.freq(i))

    fig = plt.figure(figsize=[FIG_X, FIG_Y])
    ax = fig.add_subplot(111)
    plot = dist.plot(30, title='mendenhall_s')
    fn = os.path.join(settings.MEDIA_ROOT, 'graphs', 'mendenhall_s.png')
    fig.savefig(fn)
    fn = os.path.join(settings.MEDIA_URL, 'graphs', 'mendenhall_s.png')

    fig1 = plt.figure(figsize=[FIG_X, FIG_Y])
    ax1 = fig1.add_subplot(111)
    xpoints = np.array(range(1, MAX_SENT_TOKEN_LENGTH))
    ypoints = np.array(freqs)
    ax1.plot(xpoints, ypoints)
    ax1.set_title("mendenhall_s frequences")
    fn1 = os.path.join(settings.MEDIA_ROOT, 'graphs', 'mendenhall_s_freqs.png')
    fig1.savefig(fn1)
    fn1 = os.path.join(settings.MEDIA_URL, 'graphs', 'mendenhall_s_freqs.png')

    return fn, fn1

def get_mendenhall_s(text):
    tokens = sent_tokenize(text)
    token_lengths = [len(token) for token in tokens]
    dist = nltk.FreqDist(token_lengths)
    freqs = []
    for i in range(1, MAX_SENT_TOKEN_LENGTH):
        freqs.append(dist.freq(i))
    return freqs

def mendenhall_s_distance(object1, object2):
    text1 = object1.text()
    text2 = object2.text()
    freqs1 = get_mendenhall_s(text1)
    freqs2 = get_mendenhall_s(text2)
    d = 0
    for i in range(len(freqs1)):
        l = 100 * (freqs1[i] - freqs2[i])
        d += l * l * l * l
    return d

def plot_mendenhall_s_array(objects, param='mendenhall'):
    fig = plt.figure(figsize=[BIG_X, BIG_Y])
    ax = fig.add_subplot(111)
    name = None
    for object in objects:
        text = object.text()
        y = get_mendenhall_s(text)
        dim = len(y)
        xpoints = np.array(range(1, dim+1))
        ypoints = np.array(y)
        ax.plot(xpoints, ypoints, label=f'({object.id}) {object.label()}')

    name = param + '_multy.png'
    ax.legend()
    fn = os.path.join(settings.MEDIA_ROOT, 'graphs', name)
    fig.savefig(fn)
    return name

# __________________________________________________________ Kilgariff _________

def most_common(tokens):
    freq_dist = nltk.FreqDist(tokens)
    common = list(freq_dist.most_common(TOP_MOST_COMMON_NUM))
    return common

def kilgariff_distance(object1, object2):
    logfile = os.path.join(settings.MEDIA_ROOT, 'log', 'kilgariff_distance.txt')
    log = default_storage.open(logfile, 'a')
    log.write(f'\r\n\r\n objects: {object1.label()}, {object2.label()}\r\n')

    tokens1 = tokenize(object1.text())
    tokens2 = tokenize(object2.text())
    tokens = tokens1 + tokens2

    len1 = len(tokens1)
    len2 = len(tokens2)

    if len1 == 0 or len2 == 0:
        return False

    k1 = MAX_TOKENS / len1
    k2 = MAX_TOKENS / len2

    m_common = most_common(tokens)

    log.write(f'len1, len2, len: {len1}, {len2}, {len(tokens)}), [{len(m_common)}]\r\n')

    chisquared = 0
    i = 0
    for word,joint_count in m_common:
        c1 = tokens1.count(word) * k1
        c2 = tokens2.count(word) * k2
        c12 = c1 + c2
        e1 = c12 * 0.5
        e2 = c12 * 0.5
        chi1 = ((c1-e1) * (c1-e1) / e1)
        chi2 = ((c2-e2) * (c2-e2) / e2)
        chisquared += chi1 + chi2
        i += 1
        if i < 2 :
            log.write(f'{word}, {joint_count} -> [{tokens1.count(word)} ({c1}), {e1} = {chi1}] + [{tokens2.count(word)} ({c2}), {e2} = {chi2}] = {chi1 + chi2}\r\n')

    log.close()
    return chisquared

def plot_most_common(text):
    tokens = tokenize(text)
    freq_dist = nltk.FreqDist(tokens)
    common = list(freq_dist.most_common(TOP_MOST_COMMON_NUM))

    common_nums = [count for word, count in common]
    common_nums_freqs = nltk.FreqDist(common_nums)

    fig = plt.figure(figsize=[FIG_X, FIG_Y])
    ax = fig.add_subplot(111)
    plot = freq_dist.plot(30, title='Most common')
    fn = os.path.join(settings.MEDIA_ROOT, 'graphs', 'common.png')
    fig.savefig(fn)
    fn = os.path.join(settings.MEDIA_URL, 'graphs', 'common.png')

    fig1 = plt.figure(figsize=[FIG_X, FIG_Y])
    ax1 = fig1.add_subplot(111)
    xpoints = np.array(range(0, len(common_nums)))
    ypoints = np.array(common_nums)
    ax1.plot(xpoints, ypoints)
    ax1.set_title("Common frequences")
    fn1 = os.path.join(settings.MEDIA_ROOT, 'graphs', 'common_freqs.png')
    fig1.savefig(fn1)
    fn1 = os.path.join(settings.MEDIA_URL, 'graphs', 'common_freqs.png')

    fig = plt.figure(figsize=[FIG_X, FIG_Y])
    ax2 = fig.add_subplot(111)
    plot = common_nums_freqs.plot(TOP_MOST_COMMON_NUM, title='Common frequences frequences')
    fn2 = os.path.join(settings.MEDIA_ROOT, 'graphs', 'common_f_f.png')
    fig.savefig(fn2)
    fn2 = os.path.join(settings.MEDIA_URL, 'graphs', 'common_f_f.png')

    bigrams = nltk.bigrams(tokens)
    bigrams_freq_dist = nltk.FreqDist(bigrams)
    bigrams_most_common = list(bigrams_freq_dist.most_common(TOP_MOST_COMMON_NUM))

    fig = plt.figure(figsize=[FIG_X, FIG_Y])
    ax3 = fig.add_subplot(111)

    qty = 50
    labels = []
    series = []
    height = 1
    for bigram, n in bigrams_most_common[:qty]:
        labels.append(str(bigram))
        series.append(n)
    ax3.barh(labels, series, height)
    ax3.set_title('Most common bigrams')
    fn3 = os.path.join(settings.MEDIA_ROOT, 'graphs', 'bigram_f.png')
    fig.savefig(fn3)
    fn3 = os.path.join(settings.MEDIA_URL, 'graphs', 'bigram_f.png')

    return fn, fn1, fn2, fn3

# __________________________________________________________ SUMMARIZE _________

def plot_array(objects, param):
    func = PLOT_FUNCTIONS[param]
    return func(objects, param)

def plots(text):
    names = dict()
    fn, fn1 = plot_mendenhall(text)
    names['mendenhall'] = fn
    names['mendenhall_freqs'] = fn1

    fn, fn1 = plot_mendenhall_s(text)
    names['mendenhall_s'] = fn
    names['mendenhall_s_freqs'] = fn1

    fn, fn1, fn2, fn3 = plot_most_common(text)
    names['common'] = fn
    names['common_freqs'] = fn1
    names['common_freqs_freqs'] = fn2
    names['bigram_freqs'] = fn3
    return names

def plot_histogram(labels, datasets, legend):
    height = 0.5
    names = []
    fig = plt.figure(figsize=[BIG_X, len(datasets[0])])
    ax = fig.add_subplot(111)

    left = []
    for i in range(len(labels)):
        left.append(0)

    for i in range(len(datasets)):
        ax.barh(labels, datasets[i], height, left=left, label=legend[i])
        for j in range(len(labels)):
            left[j] += datasets[i][j]

    name = 'histogram.png'
    ax.legend()
    fn = os.path.join(settings.MEDIA_ROOT, 'graphs', name)
    fig.savefig(fn)
    names.append(os.path.join(settings.MEDIA_URL, 'graphs', name))
    return names

DISTANCE_FUNCTIONS = {
    'mendenhall': mendenhall_distance,
    'mendenhall_s': mendenhall_s_distance,
    'kilgariff':  kilgariff_distance,
    }

PLOT_FUNCTIONS = {
    'mendenhall': plot_mendenhall_array,
    'mendenhall_s': plot_mendenhall_s_array,
    'kilgariff':  None,
    }



