#!/usr/bin/python
import re, sys, argparse, requests

aparser = argparse.ArgumentParser() 
aparser.add_argument("-m", "--wan", help="\nprovide wan ipv4 manually")
aparser.add_argument("-s", "--soft", help="\nsoft fail.\nfalls back on network-\nprovided wan address\nif -m is passed an invalid\n ipv4 address.", action="store_true")
aparser.add_argument("-e", "--errors", help="\nprint errors when exceptions occur.", action="store_true")
aparser.add_argument("-v", "--verbose", help="\nverbose output.", action="store_true")
args = aparser.parse_args()

vip = re.compile(r"\b((25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(25[0-5[|2[0-4]\d|[01]?\d?\d)\b")
dip = re.compile(r"(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})")
spreg = re.compile(r"(u*)([^\d]+|911)( *)([0-9\.]*)")
vresp = re.compile(r"(good|nochg|nohost|badauth|badagent|!donator|abuse|911)")
presp = re.compile(r"(good|nochg)")
nresp = re.compile(r"(nohost|badauth|badagent|!donator|abuse|911)")
#The following line is broken; USER, PASS and HOST should be replaced with variables
nirs = 'http://USER:PASS@dynupdate.no-ip.com/nic/update?hostname=HOST&myip='
wqurl = 'http://ip.keithscode.com'

def gett(ip):
	nirf = nirs + ip
	try:
		sresp = str(requests.get(nirf))
	except: 
		if not args.errors:
        		exit('error. use -e for error reports.')
		else:
			e =  sys.exc_info()[0]
			exit('network error. %s' % e)
	else:
		print 'request sent succesfully.\nserver response received.'

def auto():
	try:
		wqresp = requests.get(wqurl)
	except:
        	if not args.errors:
        		exit('error. use -e for error reports.')
		else:
			e =  sys.exc_info()[0]
			exit('network error. %s' % e)
    	else:
        	r1 = vip.search(wqresp.text)
        	if not r1:
            		exit('server-provided string  ' + wqresp + '\nis not a valid ipv4 address.')
        	else:
			gett(r1.group(0))
#main 			        
if not args.wan:
	auto()
else:    
	r1 = vip.search(args.wan) 
	if r1:
        	gett(r1.group(0))
	else:
		if args.soft:
			auto()
        	else:	
            		exit('user-provided string  ' + args.wan  + '\nis not a valid ipv4 address.')
#server responded, parse response. 
#par = spreg.search(inp0)
#if not par:
#	print 'woah.'
#else:
#	print 'else'
#	p1 = vresp.search(par.group(2))
#	if p1:
#		#valid server response. parse. 	
#		pr = presp.search(p1.group(0))
#		nr = nresp.search(p1.group(0))
#		if pr:
#			if pr.group(1) == 'good':
#				if args.verbose:
#					print 'positive response: ' + pr.group(0) 
#			elif pr.group(1) == 'nochg':
#				if args.verbose:
#					print 'positive response: ' + pr.group(0) 
#			else:
#				l1 = "x"
#		elif nr:
#			print 'negative response: ' + nr 	
#		else:	
#			exit('CODE -RF;\nRegex parsing Failure')
#	else:
#		#did not understand response. exit. 
#		exit()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
