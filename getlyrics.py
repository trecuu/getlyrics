# -*- coding: utf-8 -*-
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import re
import json
from collections import Counter

def getsonglist(band):
	band = band.lower()
	band = band.replace('\'','')
	band = band.replace('/','-')
	band = band.replace(' ','-')
	try:
		response = urllib2.urlopen('https://www.letras.mus.br/'+band+'/')
		result = re.search('<ul class=\"cnt-list\">(.*)</ul>(.*)', response.read().decode('utf-8'))
		result = re.findall(r'(?<= href=")[^"]*',result.group(1))
	except:
		return ('Inexistente!')
	else:
		return (result)


def getlyric(songlist, length):
	lyrics = []
	
	if length == 0:
		quant = len(songlist)
	else:
		quant = length

	for x in range(quant):
		print(songlist[x])
		response = urllib2.urlopen('https://www.letras.mus.br'+songlist[x])
		result = re.search('cnt-letra p402_premium(.*)<\/div>', response.read().decode('utf-8'))
		if result is not None:
			result = re.findall(r'<p>(.*?)<\/p>',result.group(1))
			result = ' '.join(result).lower()
			

			filter_space = ['<br/>']
			for fil in filter_space:
				result = result.replace(fil,' ')

			
			filter_null = [',','!','?','(',')','[',']','\'']
			for fil in filter_null:
				result = result.replace(fil,'')

			lyrics.append(result)
	return(lyrics)


def countwords(lyrics):
	words = {}
	for x in lyrics:
		words.update(Counter(x.split()))
	return (words)
	


#print('Band name:')
#band = input()
band = 'blink 182'
#print('Songs quantity (0 for all)')
#quant = input()
quant = 10

words = countwords(getlyric(getsonglist(band),int(quant)))

#escreve no arquivo
f = open(band+".txt","w+")
f.write(json.dumps(words, indent=4))
f.close()