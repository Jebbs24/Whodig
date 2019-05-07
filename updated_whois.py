#!/usr/bin/env python3.6
#Written by Jon Mason
#11/9/2017

import dns.resolver
import json
import io
import whois
import requests

try:
    to_unicode = unicode
except NameError:
    to_unicode = str
#set dig dictionary
data = dict()
#specify domain
domain = str(input("what domain?: "))
#query whois server
whois_results = dict()
whois_results = whois.query(domain)
if whois_results == None:
        print("Not a valid domain.")
        quit()
else:
        resolver = dns.resolver.Resolver()
        records = {"A record": "A",
                   "Nameservers": "NS",
                   "Mail records": "MX"}

#query domain for records and create ditctionary with results
for val in records.values():
        for rdata in resolver.query(domain, val):
                if rdata == "":
                        continue
                elif val in data:
                    # append the new number to the existing array at this slot
                        data[val].append(str(rdata))
                else:
                # create a new array in this slot
                        data[val] = [str(rdata)]

#write JSON file
with io.open('data.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(data,
                indent=4, sort_keys=True,
                ensure_ascii=False)
        outfile.write(to_unicode(str_))

#read JSON file
with open('data.json') as data_file:
    data_loaded = json.load(data_file)
    print(json.dumps(data_loaded, indent=4, sort_keys=True))


ip = str(data['A'])
ip = ip.strip("['']")
url = 'http://ipinfo.io/'+ip+'/json'
#dict ={'request': "'"+url+"'"}
#url2 = "URL: %s" % dict.get('request', "")
r = requests.get(url)
print(r.text)
