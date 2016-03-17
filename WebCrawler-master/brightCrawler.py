from optparse import OptionParser
import logging
import sys
import urllib2
import brightParam as param
import brightPage
import brightUtil as util


class Fetcher:
    def __init__(self, url, headers={}):
        self.url = url
        self.headers = headers

    def __request(self):
        try:
            request = urllib2.Request(self.url, headers=self.headers)
            handle = urllib2.build_opener()
        except Exception as e:
            print 'Unable to request for the url:',self.url
            print 'Error:',e.message
            return (None,None)
        return (request, handle)


    def fetch(self):
        ''' Uses requests package to get the webpage content. Returns the content.
        '''
        req, handle = self.__request()
        content = ''
        if handle:
            try:
                content = handle.open(req).read()
            except urllib2.HTTPError, error:
                print '%s: %s' % (error, self.url)
                logging.debug("Error:%s:%s",e, self.url)
            except urllib2.URLError, error:
                print 'URL Error: %s: %s' % (error, self.url)
                logging.debug("Error:%s:%s",error,self.url)
            except Exception as e:
                print 'Error: %s: %s' % (e)
                logging.debug("Error:%s",e)
        return content


if __name__=="__main__":
    
    #checking the command line arguments
    parser = OptionParser()
    parser.add_option("-i", "--ip",action="store", type="string", dest="input", help="specify input url to crawl")
    parser.add_option("-p", "--pc",action="store", type="string", dest="phraseCnt", help="specify top summary sentences count")
    parser.add_option("-n", "--kn",action="store", type="string", dest="keyCnt", help="specify top keywords count")
    (options, args) = parser.parse_args()
    if options.input==None:
        print 'Program needs url as argument'
        print 'try --help for more option'
        exit()
    if options.keyCnt==None:
        keyCnt = 6
    if options.phraseCnt==None:
        phraseCnt = 5

    #creating the log file
    logFile = util.getTime(param.LOGFILE)
    logging.basicConfig(filename=logFile,level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    url = options.input
    logging.info("Request Url: %s",url)


    try:
        #fetches the content of the requested url.
        fobj = Fetcher(url, headers={"User-Agent":param.USER_AGENT})
        content = fobj.fetch()
        if not content:
            exit()

        #Creates the page object and passes the content for keyword density analysis
        page = brightPage.Page(url, content, phraseCnt, keyCnt)
        phrases = page.get_key_phrases()
        print 'Summary:-'
        for i in range(phraseCnt):
            print '[%d] %r:' % (i+1,phrases[i])
        keywords = page.getKeywords()
        print '\nkeywords: ',keywords
    except Exception as e:
        print 'Error while fetching keywords - check log file:',logFile
        logging.debug("Cannot Fetch Keywords:%s",e)
        logging.exception(e)



