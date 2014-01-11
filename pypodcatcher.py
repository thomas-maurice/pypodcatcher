#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	  pypodcatcher.py : A simple podcast client commandline software
	
	           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004
 
	Copyright (C) 2013 Thomas Maurice <tmaurice59@gmail.com>
	 
	Everyone is permitted to copy and distribute verbatim or modified
	copies of this license document, and changing it is allowed as long
	as the name is changed.
	 
		         DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
		TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
	 
	 0. You just DO WHAT THE FUCK YOU WANT TO.
	 
"""

base_directory = '/home/thomas/pypodcatcher/podcast'
"""
	The fileformat accept those parameters:
		%C : Channel name
		%Y : Year
		%M : Month
		%D : datestring YYY-MM-DD
		%T : Podcast title
"""
file_format = '%C/%Y %M/%D %T'

__author__ = "Thomas Maurice"
__copyright__ = "Copyright 2013, Thomas Maurice"
__license__ = "WTFPL"
__version__ = "0.2"
__maintainer__ = "Thomas Maurice"
__email__ = "tmaurice59@gmail.com"
__status__ = "Development"

import urllib2
import sys
import time
import os
from xml.dom import minidom

def parse_feed(feed):
	"""
		Parses a feed transforming each item of it into
		a list of dictionaries containing:
		 - 'channel_name' the title of the *channel*
		 - 'title' the title of the podcast
		 - 'date' the podcast's date
		 - 'url' the url of the sound file
		 
		 In the input parameter 'feed' shall be put the URL of
		 the XML feed to parse
	"""
	
	item_list = []
	
	try:
		xml_file = urllib2.urlopen(feed).read()
		try:
			xml_tree = minidom.parseString(xml_file)
			for channel in xml_tree.getElementsByTagName("channel"):
				channel_name = channel.getElementsByTagName("title")[0].firstChild.nodeValue.encode("utf-8")
				for item in channel.getElementsByTagName("item"):
					try:
						d = item.getElementsByTagName("pubDate")[0].firstChild.nodeValue.split(" ") # Make a correct date string
						d.pop()
						t = time.strptime(" ".join(d), "%a, %d %b %Y %H:%M:%S")
						it = {'channel_name': channel_name,
							  'title': item.getElementsByTagName("title")[0].firstChild.nodeValue.encode("utf-8"),
							  'date': item.getElementsByTagName("pubDate")[0].firstChild.nodeValue,
							  'url': item.getElementsByTagName("enclosure")[0].attributes['url'].value.encode("utf-8"),
							  'date_string': time.strftime("%Y-%m-%d", t),
							  'month': time.strftime("%B", t),
							  'day': time.strftime("%a", t),
							  'year': time.strftime("%Y", t)
							 }
						item_list.append(it)
					except Exception as e:
						print "Failed to add one element from channel", channel_name, e
						
		except Exception as e:
			print "Could not parse feed", feed, e
	except:
		print "Could not fetch feed", feed
	
	return item_list

def save_items(items):
	if not os.path.isdir(base_directory):
		print "Creating root directory", base_directory
		os.makedirs(base_directory)
	for i in items:
		filename = file_format
		filename = filename.replace("%Y", i['year'])
		filename = filename.replace("%C", i['channel_name'])
		filename = filename.replace("%M", i['month'])
		filename = filename.replace("%T", i['title'])
		filename = filename.replace("%D", i['date_string'])
		filename = os.path.join(base_directory, filename)
		ext = i['url'].split('.')
		ext = ext[len(ext)-1]
		if ext == "":
			ext = ".mp3"
		filename += "." + ext
		filedir = os.path.dirname(filename)
		if not os.path.isdir(filedir):
			print "Creating podcast directory", filedir
			os.makedirs(filedir)
		
		if not os.path.exists(filename):
			print "Downloading", i['title'], "..."
			try:
				time.sleep(1)
				filename = filename.replace("\"", "\\\"")
				os.system("wget -T 5 -c -t 5 -O \"" + filename + "\" \"" + i['url'] + "\"")
			except Exception as e:
				print "Could not retrieve the file", i['url'], e
		else:
			print filename, "already exists, skipping"


if __name__ == "__main__":
	if len(sys.argv) == 2:
		f = open(sys.argv[1])
		feedlist = f.read().split("\n")
		for i in feedlist:
			l = parse_feed(i)
			save_items(l)
	
	
