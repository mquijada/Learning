# -*- coding: utf-8 -*-

import fnmatch
import os

import docx

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.collocations import *
#nltk.download('universal_tagset')
#nltk.download('treebnk')

import math
import re

import csv
import collections

import operator

# Retrieve text from a document
def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

# Retrieve stopwords 
with open('stopwords.csv','r', newline='', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    smaStopwordList = [item for sublist in reader for item in sublist]
    
    
# Convert text to tokens, eliminating stop words
def preProcess(sentence):
    stop_words = set(stopwords.words('english'))
    word_tokens = nltk.word_tokenize(sentence.lower())
    word_sma = [i for i in word_tokens if i not in smaStopwordList]
    processed_words = [w for w in word_sma if not w in stop_words]
    words_only = [word for word in processed_words if len(word) > 1]
    return words_only

# List of tokens and sentence strings
tokenList = []
sentenceList = []

# Final loop to agreggate all docx files in current directory and return a list
# of all words 
for filepath in os.listdir('.'):
        if fnmatch.fnmatch(filepath, '*.docx'):
            sentence = getText(filepath)
            sentenceList.append(sentence)
            processed_tokens = preProcess(sentence)
            for i in processed_tokens:
                tokenList.append(i)

    
fdist = FreqDist(tokenList)
for word, frequency in fdist.most_common(50):
        print(u'{};{}'.format(word, frequency))

# Function to count words
print('Total Words:', len(tokenList))

# Create bigrams
bgs = nltk.bigrams(tokenList)
fdist = nltk.FreqDist(bgs)
for k,v in fdist.most_common(50):
    print(k, v) 

# Import Vocabulary CSV, Identify vocabulary/phrases 

def identify_vocab():
    #word_freq = collections.Counter()
    with open('vocab.csv', newline='') as f:
        csv_reader = csv.reader(f)
        vocab_list = [item for sublist in csv_reader for item in sublist]        
        count_list = []
    for word in vocab_list:
        count_list.append((word, tokenList.count(word)))
        #vocab_count = tokenList.count(word)
        #print(word, vocab_count)
    count_list.sort(key = lambda count_list: count_list[1], reverse = True) 
    print(str(count_list))
            

identify_vocab()


# POS Tagging

tagged_words = nltk.pos_tag(tokenList)
wsj = nltk.corpus.treebank.tagged_words(tagset='universal')
word_tag_fd = nltk.FreqDist(wsj)
propernouns = [word for word,pos in tagged_words if pos == 'NNP']

[wt[0] for (wt, _) in word_tag_fd.most_common(50) if wt[1] == 'VERB']
# ======================================================================== #
# Term Frequency - UNDER CONSTRUCTION 



def count_words(sentence):
    count= 0
    words = word_tokenize(sentence)
    for words in words:
        count += 1
    return count
 

def remove_string_special_characters(s):
    stripped = re.sub('{^\w\s]', '', s)
    stripped = re.sub('_', '', stripped)
    stripped = re.sub('\s+', ' ', stripped)
    stripped = stripped.strip()

def create_freq_dict(sents):
    i = 0
    freqDict_list = []
    for sent in sents:
        i += 1
        freq_dict = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            if word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
            temp = {'doc_id' : i, 'freq_dict' : freq_dict}
        freqDict_list.append(temp)
    return freqDict_list

create_freq_dict(tokenList)      
freqDict_list = create_freq_dict(tokenList)
    
orig_sentence = ''.join(str(r) for v in sentenceList for r in v).translate('\t\n ')
total_words = count_words(orig_sentence)
print("Total Word Count", total_words)    
    


  