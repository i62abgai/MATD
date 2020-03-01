import re
import argparse
import click
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
from urllib.error import HTTPError
from collections import Counter, defaultdict
from math import log10
from bs4 import BeautifulSoup
import numpy as np
import nltk
from nltk.corpus import stopwords

"""
Implementation of a search engine by Ismael Abu-jadur García (ABU0007) and José Luis Gordillo Relaño (GOR0088)

This program consist of multiple procedures that allows the search engine to work:

    - Website crawling: The user inputs an URL and this URL is crawled recursively to get all links and generate a tree 
                        with all the links found in the URL which they will be crawled too, until the criterion of max
                        level of the tree is reached
                        
    - PageRank: After the crawling process is made, the program ranks all the URL and links found with a similar algorithm
                to PageRank from Google. This allows to calculate the score of each document. 

    - Inverted Index: The program generates the inverse document frequency, and calculates the score for each document based on the query.
    
    - Cosine Similarity: The program calculates the cosine similarity between the query and each document.
    
After all this procedures are completed the program outputs all the documents ranked, in order of relevance.
"""

nIter = 0 # Actual generated level of the tree
maxN = 0 # Max level of the tree generated recursively
damping = 0.05 # Damping Factor to explore links

rI = 0 # Rank influence
cI = 0 # Cosine influence

stop_words = []

@click.command()
@click.option('--query', "-q", default=None, required=True,
              help=u'Query to search.')
@click.option('--url', "-u", default=None, required=True,
              help=u'Url to crawl.')
@click.option('--level', "-l", default=1, required=False,
              help=u'Levels of crawling.')
@click.option('--cosineinfluence', "-ci", default=2, required=False,
              help=u'Cosine influence.')
@click.option('--rankinfluence', "-ri", default=1, required=False,
              help=u'Page rank influence.')
def main(query, url, level, cosineinfluence, rankinfluence):
    """[Main Function]
    
    Arguments:
        query {[string]} -- [Query to search]
        url {[string]} -- [Url to crawl]
        level {[string]} -- [Maximum level of crawling]
        cosineinfluence {[string]} -- [Cosine influence]
        rankinfluence {[string]} -- [Page rank influence]
    """    
    global maxN, cI, rI, stop_words
    stop_words = set(stopwords.words('english'))
    maxN = int(level)
    cI = int(cosineinfluence)
    rI = int(rankinfluence)
    # Crawl and page rank with google PageRank algorithm
    pages = crawl([url])
    ranks = rankPages(pages)
    #Ranked pages
    rank = rankDict(ranks, pages)
    nPages = len(pages)
    index = createIndex(pages)
    weighted_index = weigthIndex(index, nPages)

    # Print results
    print('\nNumber of pages crawled:', len(pages))
    print('Terms in the index:', len(index))
    print('Search results for the query', query,': ')
    for url, score in calculateScore(index, nPages, rank, query):
        print('\t%.10f  %s' % (score, url))

def crawl(urls, _frontier={}, _bases=None):
    """[Takes a list of urls as argument and crawls them recursivly, creating a tree of recursive calls, until
    the level of the tree stablished by the user is reached]
    
    Arguments:
        urls {[list]} -- [list with all the urls to crawl]
    
    Keyword Arguments:
        _frontier {dict} -- [dictionary to control the no repetition of crawled urls] (default: {{}})
        _bases {[list]} -- [Saves the base url] (default: {None})
    
    Returns:
        [list] -- [sorted list of tuples (url, content, links), where links is a list of urls]
    """    
    global nIter, maxN

    if not _bases:
        _bases = [urlparse(u).netloc for u in urls]
    for url in [u.rstrip('/') for u in urls]:
        if url in _frontier:
            continue
        try:
            response = getHTML(url)
        except HTTPError as e:
            print(e, url)
            continue

        page = parse(response, url, _bases)
        print('crawled \"%s\" , found %s links' % (url, len(page[2])))
        _frontier[url] = page
        nIter += 1
        if nIter <= maxN:
            crawl(page[2], _frontier, _bases)
    return sorted(_frontier.values())


def getHTML(url):
    """[Downloads the url passed as argument]
    
    Arguments:
        url {[string]} -- [Url to download the html]
    
    Returns:
        [string] -- [html of the url]
    """    
    return urlopen(url)


def parse(html, url, bases):
    """[Function that takes an html string and returns a tuple parsed from the html with the content of the page]
    
    Arguments:
        html {[string]} -- [HTML document in string format]
        url {[string]} -- [Crawled url]
        bases {[list]} -- [Base url for the crawling]
    
    Returns:
        [tuple] -- [Returns 3 elements: the url, the content, and the links finded in this page]
    """    

    soup = BeautifulSoup(html, 'lxml')
    htmlBody = soup.find('body').get_text().strip()
    links = [urljoin(url, l.get('href')) for l in soup.findAll('a')]
    links = [l for l in links if urlparse(l).netloc in bases]
    return url, htmlBody, links


def rankPages(pages):
    """[Function that receives the all the urls and html of each urls, and ranks them by Google PageRank algorithm]
    
    Arguments:
        pages {[list]} -- [List of pages]
    
    Returns:
        [list] -- [list of list that contains the documents as columns and their values as rows]
    """    
    nPages = len(pages)
    transitionMatrix = createTransMatrix(pages)
    rankSteps = [[1 / nPages] * nPages]
    for i in range(0,10):
        p = rankSteps[-1] * transitionMatrix
        rankSteps.append(np.squeeze(np.asarray(p)))
    return rankSteps


def createTransMatrix(pages):
    """[Creates the transition matrix for each link where
    each link is equally probable to be selected as next to crawl]
    
    Arguments:
        pages {[list]} -- [List of pages]
    
    Returns:
        [list] -- [list of list where the rows are the document urls, and the columns are the document links]
    """
    links = getLinks(pages)
    urls = getUrls(pages)
    nPages = len(pages)
    m = np.matrix([[weightLink(nPages, u, l) for u in urls] for l in links])
    return dampingFactor(nPages, m)


def weightLink(nPages, url, links):
    if not links:
        return 1 / nPages
    if url in links:
        return 1 / len(links)
    else:
        return 0


def dampingFactor(nPages, m):
    return m * (1 - damping) + damping / nPages


def getUrls(pages):
    return [url for url, content, links in pages]


def getLinks(pages):
    return [links for url, content, links in pages]


def rankDict(ranks, pages):
    """[Function that returns a dictionary with document urls as keys and their rank values]
    
    Arguments:
        ranks {[list]} -- [List of ranks of each page]
        pages {[list]} -- [List of pages]
    
    Returns:
        [dict] -- [Dictionary with pages as key, and their rank as values]
    """
    tzip = zip(getUrls(pages), ranks[-1])
    tdict = dict(tzip)
    return tdict


def createIndex(pages):
    """[Function that creates the index of term frequency and the documents where they appear]
    
    Arguments:
        pages {[list]} -- [List with the content and url of the content]
    
    Returns:
        [dict] -- [Dictionary where each key is a term, and the value is a list where this term appears (tf) ]
    """    
    index = defaultdict(list)
    for url, content, links in pages:
        counts = getNumberTerms(content)
        for term, count in counts.items():
            index[term].append((url, count))
    return index


def getNumberTerms(content):
    """[Function that count the number of times a term appears in a string]
    
    Arguments:
        content {[string]} -- [Content of a page]
    
    Returns:
        [counter] -- [Counter object with the terms as keys, and their frequency as values]
    """    
    return Counter(getTerms(content))


clean = re.compile('[^a-z0-9]+')


def getTerms(s):
    """[Function that receives a string and split it in different terms,
    transforming the terms (lower case) and delete the stop words]
    
    Arguments:
        s {[string]} -- [string with the content of a page]
    
    Returns:
        [list] -- [list of all the terms found in the string]
    """    
    cleaned = [clean.sub('', t.lower()) for t in s.split()]
    return [t for t in cleaned if t not in stop_words]


def weigthIndex(index, nPages):
    """[Function that receives an index as first argument and all the documents, 
    and computes the tf_idf]
    
    Arguments:
        index {[dict]} -- [index tf]
        nPages {[int]} -- [number of documents]
    
    Returns:
        [dict] -- [dictionary that represents the tf_idf]
    """    
    weighted_index = defaultdict(list)
    for term, docs in index.items():
        df = len(docs)
        for url, count in docs:
            weight = tf_idf(count, nPages, df)
            weighted_index[term].append((url, weight))
    return weighted_index


def tf_idf(tf, nPages, df):
    return weightTF(tf) * idf(nPages, df)


def weightTF(tf):
    return 1 + log10(tf)


def idf(nPages, df):
    return log10(nPages / df)

def cosineSimilarity(index, nPages, query):
    """[Function that calculates the similarity between document and query.
    This is calculated using the cosine similarity]
    
    Arguments:
        index {[dict]} -- [Dictionary with the invertex index (tf_idf)]
        nPages {[int]} -- [Number of documents]
        query {[string]} -- [string of terms to earch]
    
    Returns:
        [list] -- [Sorted list with the cosine similarity of each url]
    """    
    scores = defaultdict(int)
    terms = query.split()
    qw = {t: tf_idf(1, nPages, len(index[t])) for t in terms if t in index}
    query_len = np.linalg.norm(list(qw.values()))
    for term in qw:
        query_weight = qw[term] / query_len
        for url, weight in index[term]:
            scores[url] += weight * query_weight
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def calculateScore(index, nPages, rank, query):
    global cI, rI
    """[Function that calculates the score for each document based on the query.
    The score is the product of the page rank and the cosine similarity between the document and the query.]
    
    Arguments:
        index {[dict]} -- [Dictionary with the invertex index (tf_idf)]
        nPages {[int]} -- [Number of documents]
        ranks {[list]} -- [List of ranks of each page]
        query {[string]} -- [string of terms to earch]
    
    Returns:
        [list] -- [Sorted list with the score of each url]
    """    
    scores = cosineSimilarity(index, nPages, query)
    combined = [(doc, (score**cI) * (rank[doc]**rI)) for doc, score in scores]
    return sorted(combined, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    main()