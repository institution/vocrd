import re, sys, os, os.path
from download import download_one
import pycurl

agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"

import mechanize
b = mechanize.Browser()
# b.set_all_readonly(False)    # allow everything to be written to
b.set_handle_robots(False)   # ignore robots
# b.set_handle_refresh(False)  # can sometimes hang without this
b.addheaders = [('User-agent', agent)]



def read(x):
	resp = b.open(x)
	return resp.read()


def findone(pat, txt, default=Exception):
	vs = re.findall(pat, txt)
	if default == Exception:		
		assert len(vs) == 1,  (pat, vs, txt)
		return vs[0]
	else:		
		if len(vs) == 1:
			return vs[0]
		else:
			assert len(vs) == 0, (pat, vs, txt)
			return default

def findall(pat, txt, default=Exception):
	vs = re.findall(pat, txt)
	return vs



e = re.escape

def get_voc_file(key, path):

	# autocomplete	 
	# https://www.vocabulary.com/dictionary/autocomplete?search=mainte
	# freq="524.26">maintenance</span>


	url = "https://www.vocabulary.com/dictionary/{}".format(key)
	txt = read(url)
	pat = e(r'data-audio="') + r'(.+?)' + e(r'"')
	
	n = findone(pat, txt, None)
	if n is not None:
		return bbb(n, path)
	else:
		return False
	
def bbb(key, path):
	url = 'https://audio.vocab.com/1.0/us/{}.mp3'.format(key)
	print "download", url
	c = pycurl.Curl()	
	download_one(c, url = url, agent = agent, referer="", fpath = path)
	c.close()
	
	return True
	
	
