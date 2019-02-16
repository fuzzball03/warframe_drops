import os
import json
import multiprocessing.pool

from pymongo import MongoClient
import requests

requests = requests.Session()
dbname = 'warframe_items'
os.system('rm img/*.png -rf')
# download file
os.system('wget https://raw.githubusercontent.com/WFCD/warframe-drop-data/gh-pages/data/all.slim.json')
cli = MongoClient()
# clean db
cli.drop_database(dbname)

db = cli[dbname]
# create index
db.items.create_index('name')
db.places.create_index('name')

items = json.load(open('all.slim.json', 'r', encoding="UTF-8"))

downloads = []

prepare_items = {}
prepare_places = {}


def get_additional_data(name):
    try:
        additional_info = True
        r = requests.get(
            'https://api.warframe.market/v1/items/%s' %
            name).json()

        if 'error' in r:
            print('err', name)
            additional_info = False
    except Exception:
        additional_info = False
        r = {}
    return additional_info, r


for item in items:
    rotation = 'normal'
    level = 'normal'
    name_clean = item['place'].replace(
        '<b>', '').replace(
        '</b>', '')

    tmp = name_clean.split(', Rotation ')
    if len(tmp) == 2:
        rotation = tmp[1]

    tmp = tmp[0].split(' (')
    if len(tmp) == 2:
        level = tmp[1].split(')')[0]
    name_clean = tmp[0]

    if item['item'] not in prepare_items:
        name = item['item'].lower().replace(
            ' ', '_').replace(
            '-', '_').replace(
            "'", "").replace(
            '_blueprint', '')
        if 'relic' in name:
            if 'relic_' in name:
                name = name.replace('relic_(', '')[:-1]
            else:
                name = name.replace('relic', 'intact')
        if 'sculpture' in name:
            tmp = name.split('_')
            name = "_".join([tmp[1], tmp[0], tmp[2]])
        if not any(x in name for x in ['endo', 'credits']):
            additional_info, r = get_additional_data(name)

        info = {
            'name': item['item'],
            'drops': [],
            'imageName': "%s.png" % name
        }
        if additional_info:
            info['market_link'] = 'https://warframe.market/items/%s' % name
            info['wiki_link'] = r['payload']['item']['items_in_set'][0]['en']['wiki_link']
            info['imageName'] = "%s.png" % name
            url = r['payload']['item']['items_in_set'][0]['icon']
            downloads.append((url, name))

        else:
            info['imageName'] = "no.png"
            info['wiki_link'] = None
            info['market_link'] = None

        prepare_items[item['item']] = info

    drop = {
        'place': item['place'],
        'rarity': item.get('rarity', 'undefined'),
        'chance': item.get('chance', 'undefined'),
    }
    if name_clean not in prepare_places:
        prepare_places[name_clean] = {
            'name': name_clean,
            'levels': {}
        }

    if level not in prepare_places[name_clean]['levels']:
        prepare_places[name_clean]['levels'][level] = {'drops': {}}

    if rotation not in prepare_places[name_clean]['levels'][level]['drops']:
        prepare_places[name_clean]['levels'][level]['drops'][rotation] = []

    prepare_places[name_clean]['levels'][level]['drops'][rotation].append(
        {
            'item': item['item'],
            'rarity': item.get('rarity', 'undefined'),
            'chance': item.get('chance', 'undefined'),
        }
    )

    prepare_items[item['item']]['drops'].append(drop)

for item in prepare_items:
    db.items.insert_one(prepare_items[item])

for place in prepare_places:
    db.places.insert_one(prepare_places[place])

os.remove('all.slim.json')

print("download images")


def download_img(info):
    url, name = info
    command = 'wget "https://warframe.market/static/assets/%s" -O "img/%s.png" > /dev/null 2>&1' % (
        url, name)
    try:
        print(command)
        os.system(command)
    except Exception as ex:
        print("wtf", ex)


p = multiprocessing.pool.Pool(20)
p.map(download_img, downloads)
main_js = """
let items = %s;
let places = %s;
const updateResult = query => {
    let resultList = document.querySelector(".result");
    resultList.innerHTML = "";
        if (query.length == 0){
                return
    }
    max = 10;
    actual = 0;
    items.map(algo =>{
        [query].map(word =>{
            if(algo.toLowerCase().indexOf(word.toLowerCase()) != -1){

                if (max == actual){return ""}
        resultList.innerHTML += `<a href="/item/${algo}"><li class="list-group-item item2">${algo}</li></a>`;
                actual ++;

            }
        })
    })
    max = 10;
    actual = 0;
    places.map(algo =>{
        [query].map(word =>{
            if(algo.toLowerCase().indexOf(word.toLowerCase()) != -1){

                if (max == actual){return ""}
        resultList.innerHTML += `<a href="/place/${algo}"><li class="list-group-item place">${algo}</li></a>`;
                actual ++;

            }
        })
    })
}

updateResult("")
""" % (
    str([item['name'] for item in db.items.find({}, {'name': True})]),
    str([place['name'] for place in db.places.find({}, {'name': True})])
)

with open('js/main.js', 'w') as f:
    f.write(main_js)

os.system('git checkout img/no.png')
os.system('git checkout img/logo.png')
