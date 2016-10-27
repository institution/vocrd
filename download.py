#!/usr/bin/python
# coding: utf-8
import os, pycurl


def buffered_stdin_lines():	
	while 1:
		try:
			x = raw_input()	
			
		except EOFError: 
			break
		
		yield x


def download_one(c, url, agent, referer, fpath):
	# file already exists?
	if os.path.isfile(fpath):
		print 'file exists:',fpath
		return 'EXISTS'
				
	# assert path
	d = os.path.dirname(fpath)
	if d != '' and not os.path.isdir(d):
		os.makedirs(d)
		
	# set headers
	c.setopt(pycurl.USERAGENT, agent)
	c.setopt(pycurl.REFERER, referer)	
		
	# download		
	file = open(fpath, "w")
	c.setopt(pycurl.WRITEFUNCTION, file.write)
	c.setopt(pycurl.URL, url)
	c.perform()	
	file.close()
	
	# get result
	resp = c.getinfo(pycurl.RESPONSE_CODE)
	tt = c.getinfo(pycurl.TOTAL_TIME)
	tm = c.getinfo(pycurl.STARTTRANSFER_TIME)
	size = c.getinfo(pycurl.SIZE_DOWNLOAD) / 1000
	speed = c.getinfo(pycurl.SPEED_DOWNLOAD) / 1000
	
	# check response
	print fpath
	if resp == 200:
		print '> status:',resp, 'time: %.1fs' % tt, '(mark: %.1fs)' % tm, 'speed: %.0fkB/s' % speed,'size: %.0fkB' % size
		return 'OK'
		
	elif resp == 404:
		print resp, 'time: %.1fs' % tt
		os.unlink(fpath)
		return 'NOT_FOUND'
	
	elif resp == 500:
		print resp, 'time: %.1fs' % tt
		os.unlink(fpath)
		return 'SERVER_ERROR'
				
	else:
		print url
		os.unlink(fpath)
		raise Exception('Unexpected Response Code: ' + str(resp))

