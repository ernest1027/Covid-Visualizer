import json
import requests
import pickle
import sys

response = requests.get("https://api.covid19india.org/v4/min/timeseries.min.json")
thething = json.loads(response.text)

'''f = open('data.json', 'w')
json.dump(thething, f)
f.close()'''

count = 0
print(sys.version)

alist = []

def flatten(d, ret=None):
    if ret is None:
        ret = []
    for k, v in sorted(d.items()):
        ret.append(k)
        if v:
            flatten(v, ret)
    return ret


f = open('other.json', 'w')
json.dump(flatten(thething), f)
f.close()

# rint(type(thething['AN']['dates']['2020-03-26']['delta']['confirmed']))

