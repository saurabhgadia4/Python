# Word Density Analyser
This program will provide with summary of topmost sentences and topmost keywords present in the page for a given url.

Usage:
	input:-
		$: python brightCrawler -i <url>
		For commandline argument help:
		$: python brightCrawler --help

	output:-
		<summary>
		<keywords>


Dependencies:
	Language: Python
	
	Version:'2.7.6 (default, Jun 22 2015, 17:58:13) \n[GCC 4.8.2]'

	External Packages:
		1. BeautifulSoup4
			Installation:
				$: sudo pip install beautifulsoup4
			Used For:
				1. parsing html document.
		2. Nltk
			Installation:
				$: sudo pip install nltk
				$: then download nltk book for corpus and POS support
			Used For:
				1. extracting stopwords from the webpage
				2. Part of Speech(POS) Tagging of top sentences to extract top keywords

ALL Files:
	1. README.md
	2. brightCrawler.py - extracts the content of webpage and pass it to Page module for keyword extraction
	3. brightPage.py - extracts top keywords and phrases for a given page
	4. brightUtil.py - supportive function
	5. brightParam.py - constant parameters file



Program Flow and Algorithm:

1. After passing the url to the program, it fetches the page using requests package and transfers the content to Page module.

2. Algorithm for extracting top sentences and keywords:-
   a. split all stopwords from the text
   b. divide the text into sentences.
   c. Remove Punctuation marks
   d. When meta tags attributes like: description, keywords, title are present, then I am considering these phrases into my candidate list of top extracted sentences because most of the time it conveys accurate keywords and summary about the text.

   Scoring function of sentences:-
   e. Now for all the text sentences(N), I create a matrix of sentences (N*N)(symmetric). 
   f. To calculate the score of pair of sentences, I take the intersection of words of two sentences and return the normalize amount of intersection count. eg. float(len(set_1.intersection(set_2)))/((len(set_1)+len(set_2))/2)
   g. I also tried to implement the TextRank algorithm and bigram pair matching, but the result were not that convincing. May be I will require more time to further dig into these methods and find the missing link.
   h. After getting our score matrix(N*N), each sentence score is just the sum of its score against all other sentences. This way we are imparting context logic into our algorithm.
   i. Now we select the top K score sentences (k can be adjusted) and add the metatag sentences as well to this candidate list.
   j. Now we tokenize the sentences and calculate the Part of Speech tags (NN, JJ, NNP) which are configurable.
   h. Now we calculate the unique word count and return the keywords based on non-increasing word count of extracted keywords from POS tagger.

Notes: 
	1. I have also used the logging module in the program. So if the program does not outputs any result just have a look at the log file with name 'log-*.log' which matches with the execution time.

	2. For each execution new log will be created with the name matching the time of execution.
	3. We can easily extend this logging module to make it rolling based on size of log.

Further Algorithmic Enhancement:
1. We can take into account the outlinks webpage data to infer the keywords( Naive Bayes Method)
2. We can also create the score matrix based on heading, location of text, images in the webpage
3. We can roughly categorize the web page based on URL domain.
4. We can create the Tree Rank graph and induce results from it.
5. We can used supervised machine learning algorithms to get more probabilistic score model from the learning.


Results:

1. 
Link: http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster

Summary:-
[1] 'Online Shopping for Kitchen Small Appliances from a great selection of Coffee Machines, Blenders, Juicers, Ovens, Specialty Appliances, & more at everyday low prices':
[2] 'Conair Cuisinart CPT-122 2-Slice Compact Plastic Toaster (White),Cuisinart,CPT-122':
[3] u'Amazon.com: Conair Cuisinart CPT-122 2-Slice Compact Plastic Toaster (White): Kitchen & Dining':
[4] u'add wedding registry sellers amazon add cart $':
[5] u'& free shipping orders $':

keywords:  ['kitchen', 'cpt-122', 'cuisinart', '2-slice', 'compact', 'toaster']

2.
Link: http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/

Summary:-

[1] "Share your passion for the outdoors and introduce a friend to hike and camp--don't forget to start slow.":
[2] u'How to Introduce Your Indoorsy Friend to the Outdoors - REI Blog':
[3] u'keep mind friend level fitness':
[4] u'keep pace friend friend set pace fast go, joyfully follow suit':
[5] u'advise friend dress':

keywords:  ['friend', u'pace', u'indoorsy', u'blog', u'rei', 'passion']

3.
Link: http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/

Summary:-
[1] 'Edward Snowden might never live in the U.S. as a free man again after leaking secrets about a U.S. surveillance program':
[2] 'politics, Man behind NSA leaks says he did it to safeguard privacy, liberty - CNNPolitics.com':
[3] u'Man behind NSA leaks says he did it to safeguard privacy, liberty - CNNPolitics.com':
[4] u'snowden worked security guard nsa computer security job cia':
[5] u'watchmeet nsa leaker :story highlightsunclear snowden will wind up, leaving hong kong russiaedward snowden, , source leaks nsa surveillance program "the public decide programs':

keywords:  ['nsa', 'snowden', 'man', 'privacy', 'cnnpolitics.com', 'program']

