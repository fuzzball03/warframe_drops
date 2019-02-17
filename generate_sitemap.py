from urllib.parse import quote
import datetime

import requests
from pymongo import MongoClient


cli = MongoClient(connect=False)
db = cli['warframe_items']
url = 'https://warframemods.com'

now = datetime.datetime.utcnow().replace(
    microsecond=0).replace(
    tzinfo=datetime.timezone.utc).isoformat()


xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>""" + url + """</loc>
        <lastmod>""" + now + """</lastmod>
        <priority>1.00</priority>
    </url>

"""
for item in db.items.find({}, {'name': True}):
    xml += """
    <url>
        <loc>""" + url + "/item/" + quote(item['name']) + """</loc>
        <lastmod>""" + now + """</lastmod>
        <priority>1.00</priority>
    </url>"""

for place in db.places.find({}, {'name': True}):
    xml += """
    <url>
        <loc>""" + url + "/place/" + quote(item['name']) + """</loc>
        <lastmod>""" + now + """</lastmod>
        <priority>1.00</priority>
    </url>"""

xml += """
</urlset>
"""
with open('xml/sitemap.xml', 'w') as f:
    f.write(xml)
sitemap_url = '%s/sitemap.xml' % url

print(sitemap_url)
print(requests.get('http://www.google.com/ping?sitemap=%s' % sitemap_url).content)

