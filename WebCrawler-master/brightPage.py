from brightCrawler import Fetcher
from bs4 import BeautifulSoup
import re
import string
import brightParam as param
import brightUtil as util

class Page:
    def __init__(self, url, content, topPhrases=10, topKeywords=5):
        self.content = content
        self.pageObj = None
        self.outLink = []
        self.metaKey = ''
        self.title = ''
        self.metaDesc = ''
        self.keyPhrases = []
        self.keywords = []
        self.topPhrasesCnt = topPhrases
        self.topKeyCount = topKeywords
        self.__getPageObject()

    def __fill_details(self):
        '''Currently only extracts the metatags related attributes. Can be extended as per use'''
        try:
            obj = self.pageObj.findAll(attrs=param.METATAG['DESC'])
            if obj:
                self.metaDesc = obj[0]['content']
                if self.metaDesc:
                    self.keyPhrases.append(self.metaDesc)
        except KeyError:
            logging.info("meta description missing")
        
        #extracting keywords
        try:
            obj = self.pageObj.findAll(attrs=param.METATAG['KEY'])
            if obj:
                self.metaKey = obj[0]['content']
                if self.metaKey:
                    self.keyPhrases.append(self.metaKey)
        except KeyError:
            logging.info("meta keywords missing")

        try:
            self.title = self.pageObj.title.text
            if self.title:
                self.keyPhrases.append(self.title)
        except Exception:
            logging.info("url title missing")

    def __getPageObject(self):
        ''' 
        Creates the BeautifulSoup object to parse the HTML Content. After successful
        creation of BeautifulSoup object it fills in the metatags and other related information.
        '''
        try:
            self.pageObj = BeautifulSoup(self.content, "lxml")
            self.__fill_details()
        except Exception as e:
            logging.debug('Cannot create beatifulsoup object:%s',e)
            raise

    def getOutLink(self):
        ''' Gets the outlink from the 'a href' tag. We need to form the absolute url if need
        to crawl these URL.
        '''
        for link in self.pageObj.find_all('a'):
            self.outlink.append(link.contents)

    def getText(self):
        '''
        This methods returns the raw text from the html content
        '''
        if not self.pageObj:
            self.__getPageObject()
        [s.extract() for s in self.pageObj(['style', 'script', '[document]', 'head'])]
        visible_text = self.pageObj.getText()
        return visible_text

    def _getSentences(self, text):
        '''
        From the given raw text, it returns the clean list of sentences.
        '''
        sent = text.split('.')
        sent = filter(lambda s: s != '', sent)
        return self._cleanSent(sent)

    def _cleanSent(self, sent):
        '''
        It cleans the given list of sentences by removing STOPWORDS and Punctuations.
        '''
        clean = []
        for i in range(len(sent)):
            rawText = util.removePunctuation(sent[i])
            rawText = re.sub('\d+','',sent[i])
            rawText = util.removeStopWords(rawText, param.STOPWORDS)
            clean.append(rawText)
        return clean

    def get_score(self, text):
        '''
        Generates the score matrix based on similarity of pair of sentences.
        It takes rawText and returns the list of sentences along with the score. 
        '''
        sentences = self._getSentences(text)
        slen = len(sentences)
        score = [[0 for x in range(slen)] for x in range(slen)]
        
        for i in range(1, slen):
            if len(sentences[i])<15:
                continue
            j = 0
            while j<i:
                if len(sentences[j])<15:
                    j+=1
                    continue
                score[i][j] = util.compareSentences(sentences[i],sentences[j])
                score[j][i] = score[i][j]
                j+=1
        return sentences, score

    def __extract_meta_tags(self):
        '''
        Returns the metatags present in webpage.
        '''
        tags = []
        tags.extend(util.get_tags([self.metaKey]))
        tags.extend(util.get_tags([self.metaDesc]))
        tags.extend(util.get_tags([self.title]))
        return tags

    def get_key_phrases(self, count=0):
        '''
        Returns the top keyphrases present in the text. It uses the content provided during the initialization of
        this object.
        '''
        if self.pageObj:
            text = self.getText()
            text = text.lower()
            text = util.removeStopWords(text, param.STOPWORDS)
        sent, score = self.get_score(text)
        slen = len(sent)
        score_dict = {}
        nxt_count = 0
        if not count:
            count = self.topPhrasesCnt

        for i in range(slen):
            score_dict[sum(score[i])] = i

        top_sent = sorted(score_dict.keys(), reverse=True)

        self.keywords.extend(self.__extract_meta_tags())
        for t in top_sent:
            #print 'sent:', sent[score_dict[t]], ' score: ',t
            self.keyPhrases.append(sent[score_dict[t]])
            nxt_count+=1
            if nxt_count==count:
                break
        return self.keyPhrases

    def getKeywords(self, count=0):
        '''
        Returns the top keywords present in the text. It uses the content provided during the initialization of
        this object.
        '''
        keyPhrases = self.get_key_phrases()
        self.keywords = util.get_tags(keyPhrases, self.keywords)
        keywords = []
        i = 0
        if not count:
            count = self.topKeyCount
        while i<count and i<len(self.keywords):
            keywords.append(self.keywords[i][0])
            i+=1
        return keywords        