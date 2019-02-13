import threading

from pymongo import MongoClient
import requests
import queue

cli = MongoClient(connect=False)
db = cli['warframe_drops']
qmods = queue.Queue()
concurrency = 10
url = 'https://mods.agalera.info/mod/'

for mod in db.mods.find({}, {'name': True}):
    qmods.put(mod['name'])


def worker():
    r = requests.Session()
    while True:
        try:
            mod = qmods.get_nowait()
        except queue.Empty:
            break
        res = r.get('%s%s' % (url, mod))
        if not res.ok:
            print("------------------------------------")
            print(mod, '%s%s' % (url, mod))


workers = [threading.Thread(target=worker) for x in range(concurrency)]
[w.start() for w in workers]
[w.join() for w in workers]
