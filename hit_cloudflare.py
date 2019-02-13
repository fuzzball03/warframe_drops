import threading

from pymongo import MongoClient
import requests
import queue

cli = MongoClient(connect=False)
db = cli['warframe_items']
qitems = queue.Queue()
concurrency = 10
url = 'https://mods.agalera.info/item/'

for item in db.items.find({}, {'name': True}):
    qitems.put(item['name'])


def worker():
    r = requests.Session()
    while True:
        try:
            item = qitems.get_nowait()
        except queue.Empty:
            break
        res = r.get('%s%s' % (url, item))
        if not res.ok:
            print("------------------------------------")
            print(item, '%s%s' % (url, item))


workers = [threading.Thread(target=worker) for x in range(concurrency)]
[w.start() for w in workers]
[w.join() for w in workers]
