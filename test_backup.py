from backup import *
import pytest
import json
import hashlib
import re
import os

def test_get_data():
    d = json.loads(get_data())
    assert isinstance(d, list)

def test_chack_change():
    content0 = ''
    content1 = None
    content2 = 'aha'
    content3 = 'bhb'
    m2 = hashlib.md5()
    m2.update(content2.encode())
    m2 = m2.hexdigest()
    assert check_change(content0, content2) == (content2, m2, False)
    with pytest.raises(TypeError):
        check_change(content1, content2)
    assert check_change(content3, content2) == (content2, m2, False)
    assert check_change(content2, content2) == (content2, m2, True)

def test_record():
    LOGFILE = 'data/test_log.txt'
    # No changes to content
    nochange = ('mock content', 'mock_md5', True)
    
    record(*nochange, LOGFILE=LOGFILE)
    with open(LOGFILE, 'r') as log:
        assert re.match(r'\d{4}-\d{2}-\d{2}T\d{6}\tNOCHANGE\n', log.read())
    os.remove(LOGFILE)

    # Changed content
    content1 = '[content that is used]'
    hashv = hashlib.md5()
    hashv.update(content1.encode())
    hashv = hashv.hexdigest()
    change = (content1, hashv, False)
    t='2019-07-03T120507'
    record(*change, LOGFILE=LOGFILE, t=t)
    with open(LOGFILE, 'r') as log:
        assert re.match(r'2019-07-03T120507\tMD5:'+ hashv + '\n', log.read())
    os.remove(LOGFILE)
    with open('data/{}.json'.format(t), 'r') as newdata:
        assert newdata.read() == content1
    os.remove('data/{}.json'.format(t))

def test_findlast():
    os.mkdir('data_test')
    fns = ['1224_test.json', '1234_test.json', '0234_test.json',
           '0264_test.json', '0261_test.json']
    for f in fns:
        open('data_test/' + f,'w').close()
    assert findlast(datadir='data_test') == 'data_test/1234_test.json'
    for f in fns:
        os.remove('data_test/' + f)
    assert findlast(datadir='data_test') == ''
    os.rmdir('data_test')
        

def test_oldcontent():
    os.mkdir('data_test')
    with open('data_test/oc.json', 'w') as oc:
        oc.write('This is the old content, man!')
    assert oldcontent('data_test/oc.json') == 'This is the old content, man!'
    assert oldcontent('') == ''
    os.remove('data_test/oc.json')
    os.rmdir('data_test')

        
        
    
    
    
