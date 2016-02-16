import urllib2
import gzip
import json
import os
import re

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

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

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    #get IMDB Actor,Actress,Nicknames, and Movie List
    urls = ['ftp://ftp.fu-berlin.de/pub/misc/movies/database/actors.list.gz','ftp://ftp.fu-berlin.de/pub/misc/movies/database/actresses.list.gz','ftp://ftp.fu-berlin.de/pub/misc/movies/database/aka-names.list.gz','ftp://ftp.fu-berlin.de/pub/misc/movies/database/movies.list.gz']
    for url in urls:
        file_name = url.split('/')[-1]
        #download(url)
        #extract(file_name)
        #delete(file_name)
    print "Pre-ceremony processing complete."
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    f  = 'actresses.list'
    c  = open(f,'rb').read()
    List = re.split(r'\n{2,}', c)
    exp = re.compile('^(.*)$',re.M)#grabs line with name + first role
    #grab first name and last name from this line possibly simplify and say lastname, firstname (ignoring any compound names or single names)
    lists =[]
    for index,item in enumerate(List):
            List[index] = re.match(exp, item).group(0) #so far gets a name and
    for item in List[2000:2100]:
        print item
    return

if __name__ == '__main__':
    pre_ceremony()
    main()
