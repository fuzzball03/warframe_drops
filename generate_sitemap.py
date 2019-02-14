from urllib.parse import quote
import datetime

from pymongo import MongoClient


cli = MongoClient(connect=False)
db = cli['warframe_items']
url = 'https://mods.agalera.info/item/'

now = datetime.datetime.utcnow().replace(
    microsecond=0).replace(
    tzinfo=datetime.timezone.utc).isoformat()


xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset
      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">

"""
for item in db.items.find({}, {'name': True}):
    xml += """
    <url>
        <loc>""" + url + quote(item['name']) + """</loc>
        <lastmod>""" + now + """</lastmod>
        <priority>1.00</priority>
    </url>"""

xml += """
</urlset>
"""
with open('xml/sitemap.xml', 'w') as f:
    f.write(xml)
