import requests
import argparse
import re
import json

check_api='https://club.pokemon.com/api/signup/verify-username'

s=requests.session()

def touch():
	r=s.get('https://club.pokemon.com/de/pokemon-trainer-club/anmelden/')
	relic=re.search('loader_config={xpid:".*"};window.NREUM',r.content)
	relic=re.sub('.*xpid:"','',relic.group(0))
	relic=re.sub('"}.*','',relic)
	return s.cookies['csrftoken'],relic

def check(username,csrftoken,relic):
	head={'X-CSRFToken':csrftoken,
			'User-Agent':'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
			'X-NewRelic-ID':relic,
			'Content-Type':'application/json'}
	i='{"name":"%s"}'%(username)
	r=s.post(check_api,data=i,headers=head)
	return json.loads(r.content)['inuse'] or not json.loads(r.content)['valid']
	
def main():
	csrftoken,relic= touch()
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--username", help="Username", required=True)
	args = parser.parse_args()
	if check(args.username,csrftoken,relic):
		print '[-] username taken/invalid'
	else:
		print '[+] username available'
	
if __name__ == '__main__':
	main()
