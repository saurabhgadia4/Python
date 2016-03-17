import os
import logging
import subprocess
import shutil
import sys
import nltk
from nltk.corpus import stopwords
from string import ascii_lowercase
import time
import re
import string
import datetime
import logging
import brightParam as param


SAMPLE_FILE = 'clean-file'
CORPUS_FILE = 'sample_test.txt'
CORPUS_WORDS = 'sample_word.txt'

cachedStopWords = stopwords.words("english")

def sentToWords():
    '''
    Used to break sentences to words. It can be used for ngram creations. Right now not used.
    '''
# #1. splitting file by words
    try:
        shutil.copy2(SAMPLE_FILE, CORPUS_FILE)
        #truncExpr('\.', CORPUS_FILE, CORPUS_MINUS_SPACE)
        command = "tr -sc \'A-Za-z\.\' \'~\' < " + CORPUS_FILE + ">" + CORPUS_WORDS
        ret = subprocess.call(command, shell=True)
        if(ret):
            print "Error"
            sys.exit(-1)
        logging.info('successfully created word file')
        
        command = "sed -i \'s/~/~\\n/g\' " +  CORPUS_WORDS
        ret = subprocess.call(command, shell=True)
        if(ret):
            print "Error"
            sys.exit(-1)
        logging.info('successfully added space characters')

    except Exception as e:
        logging.exception(e)

def truncate(expr, inFile, outFile):
    '''
    Used to translate the data of file as requried. Right now not used.
    '''
    try:
        command = "tr -d \'~\' < " + inFile + ">" + outFile
        ret = subprocess.call(command, shell=True)
        if(ret):
            print "Error"
            sys.exit(-1)
        logging.info('successfully added space characters')
    except Exception as e:
        logging.exception(e)

def removeStopWords(corpus, stopwords):
    '''
    Removes the stopwords from the corpus and returns the corpus without stopwords.
    '''
    stopwords = stopwords.split(',')
    parseList = [word for word in corpus.split() if word.lower() not in stopwords]
    return ' '.join(parseList)

def removePunctuation(text):
    '''
    Removes the punctuation from the corpus and returns the corpus.
    '''
    return re.sub('[%s]' % string.punctuation,'',text)

def compareSentences(s1, s2):
    '''
    Calculates and returns normalize intersection score of two sentences.
    '''
    set_1 = set(s1.split(' '))
    set_2 = set(s2.split(' '))
    #print 'Inter: ',set_1.intersection(set_2)

    if len(set_1)==0 or len(set_2)==0:
        return 0
    return float(len(set_1.intersection(set_2)))/((len(set_1)+len(set_2))/2)

def get_tags(sentences, base_keywords=[], tags=['NN', 'JJ','NNP']):
    '''
    Extracts the provided part of speech tag words from the sentences.
    '''
    pos_tags = []
    pos_tags.extend(base_keywords)
    for i in range(len(sentences)):
        tokens = nltk.word_tokenize(sentences[i])
        keywords = nltk.pos_tag(tokens)
        keywords = filter(lambda s: s[1] in tags , keywords)
        pos_tags.extend(keywords)
        #print 'sent-->Tag:',sentences[i]
    pos_tags = map(lambda s: s[0], pos_tags)
    key_dict = {}
    for word in pos_tags:
        if word.lower() not in key_dict:
            key_dict[word.lower()] = 1
        else:
            key_dict[word.lower()]+=1
    key_dict = sorted(key_dict.items(), key=lambda x: x[1], reverse=True)
    return key_dict

def getTime(baseName):
    '''
    Returns the human readable time format as string
    '''
    value = datetime.datetime.fromtimestamp(time.time())
    return baseName+value.strftime('%Y-%m-%d-%H-%M-%S')+'.log'

if __name__=="__main__":
    pass