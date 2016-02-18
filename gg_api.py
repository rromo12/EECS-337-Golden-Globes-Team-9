import urllib2
import gzip
import json
import os
import re
import pickle 
<<<<<<< HEAD
import nltk
from nltk.util import everygrams
from nltk.util import ngrams
from nltk.tokenize import TweetTokenizer
=======
from collections import Counter
from fuzzywuzzy import process, fuzz
>>>>>>> origin/master

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


def get_tweets_for_year(year):
    tweets = []
    with open("gg%s.json" % year) as tweet_file:
        json_object = json.load(tweet_file)
        for tweet_object in json_object:
            tweets.append((tweet_object["id"], tweet_object["text"]))
    return tweets

def parse_tweets(tweets, regexp, dictionary={}):
    '''Take Tweet and seperate out id and text, search text for regexp, if match then add to dictionary'''
    for tweet in tweets:
        tweetid = tweet[0]
        text = tweet[1]
        ##maybe add stop list before matching
        match =  re.search(regexp, text)
        if(match != None):
            extracted = match.group(0)
            dictionary[tweetid] = extracted
    return dictionary

def get_names(tweet,nameset,max_tokens):
    #get ngrams in tweet, compare them to list of actors and actressss 
    # Need to fix 
    names= []
    tweetid = tweet[0]
    text = tweet[1]
    grams = nltk.word_tokenize(text)
    # use stop list to limit grams
    tweet_ngrams = everygrams(grams, min_len=1, max_len=max_tokens)
    for gram in tweet_ngrams:
            name = ' '.join(gram)
            if(name in nameset):
                names.append(name)
    return names
    
def get_host_dictionary(tweets):
    regexp = '(host(s?|ing)\s)'
    host_dictionary = parse_tweets(tweets ,regexp)
    return host_dictionary
    pass

def award_names(tweets):
    award_regex = r"(Best(?=\s[A-Z])(?:\s([A-Z]\w+|in|a|by an|\s-\s))+)"
    award_dictionary = parse_tweets(tweets, award_regex)
    return award_dictionary

def get_nominees_dictionary(tweets):
    # rene
    pass

def get_presenters_dictionary(tweets):
    # rene
    pass

def get_winners_dictionary(tweets):
    # rene
    pass

def get_master_award(found_awards, cutoff=25):
    frequent_appearing_awards = [found_award for found_award in found_awards if found_awards.count(found_award) > 5]
    unique_award_names = set(frequent_appearing_awards)
    print unique_award_names
    found_award_counts = Counter(frequent_appearing_awards)
    top_awards = [a[0] for a in found_award_counts.most_common(cutoff)]
    print top_awards
    ordered_by_count = [i[0] for i in found_award_counts.most_common()[::-1]]
    for award in ordered_by_count:
        best_match = process.extractOne(award, ordered_by_count[ordered_by_count.index(award)+1:], scorer=fuzz.token_sort_ratio, score_cutoff=85)
        if best_match:
            if award not in top_awards:
                print award, best_match
                unique_award_names.remove(award)

    return unique_award_names




#Tweet contains match for award and nomineee ---> add to lists
#dictionary Hosts: {key:value} = tweetid: hostname 
#dictionary Award Names: {key:value} = tweetid: awardname 
#dictionary Nominees: {key:value} = tweetid: nominees 
# d_winners{};
# d_nominee{};
# d_award{};

#d_winners_nominee{};
# d_nominee_award{};
# d_winner_award{};

def match_IDs(d_winners, d_nominee, d_award):
    for key_a, value_a in d_award:
        for key_n, value_n in d_nominee:
            if key_n == key_a:
                d_nominee_award[value_n] = value_a;
        for key_w, value_w in d_winners:
            if key_w == key_a:
                d_winner_award[value_w] = value_w;


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    regexp = ''
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winners(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

def download(url):
    '''http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
    '''
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
    return f

def extract(file_name):
    '''http://stackoverflow.com/questions/20635245/using-gzip-module-with-python
    '''
    inFile = gzip.open(file_name, 'rb')
    outFile = open(file_name[:-3], 'wb')
    outFile.write( inFile.read() )
    inFile.close()
    outFile.close()
    return

def delete(file_name):
    os.remove(file_name)
    return

def save(dObj, sFilename):
  """Given an object and a file name, write the object to the file using pickle."""
  f = open(sFilename, "w")
  p = pickle.Pickler(f)
  p.dump(dObj)
  f.close()

def load(sFilename):
  """Given a file name, load and return the object stored in the file."""
  f = open(sFilename, "r")
  u = pickle.Unpickler(f)
  dObj = u.load()
  f.close()
  return dObj


def Make_IMDB_List(f):
    c  = open(f,'rb').read()
    List = re.findall(r'\n{2,}(.*)', c)
    exp = re.compile('([A-z \-\.]*)(?:,(( [A-z\-\.]*){0,3})(?:\(I*\))?)(.*)\s(\(.*\))\s*(\[.*\])?',re.M)
    imdblists =[]
    for index,item in enumerate(List):
        match = re.match(exp, item)
        if(match!= None):
            imdblists.append(match.group(2).strip() +  ' ' +match.group(1).strip())
    return imdblists

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    #get IMDB Actor,Actress,Nicknames, and Movie List
    if (not(os.path.isfile("actors.lst")) and not(os.path.isfile("actresses.lst"))):
        urls = ['ftp://ftp.fu-berlin.de/pub/misc/movies/database/actors.list.gz','ftp://ftp.fu-berlin.de/pub/misc/movies/database/actresses.list.gz','ftp://ftp.fu-berlin.de/pub/misc/movies/database/aka-names.list.gz','ftp://ftp.fu-berlin.de/pub/misc/movies/database/movies.list.gz']
        for url in urls:
            file_name = url.split('/')[-1]
            download(url)
            extract(file_name)
            delete(file_name)
        lists  = ['actresses.list','actors.list']
        actresses = Make_IMDB_List(lists[0])
        actors = Make_IMDB_List(lists[1])
        actors = set(actors)
        actresses =set (actresses)
        #movie list
        #nick nameslist
        save(actors, 'actors.lst')
        save(actresses, 'actresses.lst')

    print "Pre-ceremony processing complete."
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''

    # Your code here
    # max_tokens = 4;
    # print 'loading lists'
    # x = load('actors.lst')
    # y = load('actresses.lst')
    # print 'Lists loaded'
    # # for item in x:
    # #         print nltk.tokenize()
    # # for n in x[:1000]:
    #     # print n
    # # for n in y[:1000]:
    #     # print n
    # # print len(x)
    # # print len(y)
    # # if('Ricky Gervais' in x):
    #     # print True
    # tweets = get_tweets_for_year(2013)
    # print len(tweets)
    # actor_names = []
    # for tweet in tweets:
    #     anames = get_names(tweet,x,max_tokens)
    #     if (anames != []):
    #         actor_names.append(anames)
    #         print anames
    #     print tweet

if __name__ == '__main__':
    pre_ceremony()
    main()

