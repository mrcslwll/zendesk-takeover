import sys
import requests
import os

if len(sys.argv) < 2:
	print('Determine if a zendesk subdomain is available to takeover.')
	print('Usage: zendesk_takeover.py <subdomain>')
	sys.exit()

os.system('dig ' + sys.argv[1] + ' | grep CNAME > dig')

dig = open('dig', 'r')
dig = dig.readlines()

for line in dig:
	if "zendesk" not in line:
		pass
	else:
		cname = line.split('CNAME	')[1].rstrip()
		if "zendesk" not in cname:
			print("I dont think this is a zendesk subdomain")
			os.system("rm dig")
			sys.exit()
os.system("rm dig")

try:
	headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0', "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
	r = requests.post('https://www.zendesk.com/wp-content/themes/zendesk-twentyeleven/lib/domain-check.php', data = "domain="+cname, headers=headers)
	if '{\"available\":false}' in r.text:
		print('Unfortunately, this subdomain is not available to takeover')

	elif '{\"available\":true}' in r.text:
		print('Great! This subdomain is available to takeover')

	else:
		print("A strange error occurred.")


except:
	print("A strange error occurred.")

