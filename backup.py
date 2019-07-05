#!/bin/env python

import requests
import hashlib
import time
import glob


HOST = '86.119.40.114'
URL = '/api/getsr'

def isotime():
    return  time.strftime('%Y-%m-%dT%H%M%S')

def findlast(datadir='data'):
    fl = glob.glob(datadir + '/*.json')
    fl.sort()
    try:
        return fl.pop()
    except IndexError:
        return ''

def oldcontent(lastfn):
    oc = '' if lastfn == '' else open(lastfn, 'r').read()
    return oc

def get_data():
    r = requests.get('http://{}{}'.format(HOST, URL))
    return(r.content.decode('utf-8'))

def check_change(content0, content1):
    if content0 is None or content1 is None:
        raise TypeError
    m0 = hashlib.md5()
    m0.update(content0.encode())
    m0 = m0.hexdigest()
    m1 = hashlib.md5()
    m1.update(content1.encode())
    m1 = m1.hexdigest()
    nochange = True if m0 == m1 else False
    return (content1, m1, nochange)

def record(content, hashsum, nochange, LOGFILE='./data/log.txt', t=isotime()):
    if nochange:
        with open(LOGFILE, 'a') as logfile:
            logfile.write('{}\tNOCHANGE\n'.format(t))
    else:
        fnew = 'data/{}.json'.format(t)
        with open(LOGFILE, 'a') as logfile:
            logfile.write('{}\tMD5:{}\n'.format(t, hashsum))
            
        with open(fnew, 'w') as newdata:
            newdata.write(content)

    
if __name__ == '__main__':
    old = oldcontent(findlast())
    new = get_data()
    record(*check_change(old, new))

    

    
