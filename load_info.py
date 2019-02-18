import os
import json
import multiprocessing.pool
import hashlib
import urllib

from pymongo import MongoClient
import requests


def md5(text):
    return hashlib.md5(
        urllib.parse.quote(text).encode('utf-8')).hexdigest()


requests = requests.Session()
dbname = 'warframe_items'
download = False
if download:
    os.system('rm img/*.png -rf')
# download file
#os.system('wget https://raw.githubusercontent.com/WFCD/warframe-drop-data/gh-pages/data/all.slim.json')
cli = MongoClient()
# clean db
cli.drop_database(dbname)

db = cli[dbname]
# create index
db.items.create_index('name')
db.places.create_index('name')

items = json.load(open('warframe-drop-data/data/all.slim.json', 'r', encoding="UTF-8"))

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
    extra = 'Extra' in item['place']

    name_clean = item['place'].replace(
        '<b>', '').replace(
        '</b>', '')

    tmp = name_clean.split(', Rotation ')
    if len(tmp) == 2:
        rotation = tmp[1]
    if 'stage' in item:
        rotation += " - <b>%s</b>" % item['stage']
        item['place'] += ", %s" % item['stage']
    tmp = tmp[0].split(' (')
    if len(tmp) == 2:
        level = tmp[1].split(')')[0]
    name_clean = tmp[0]
    if extra:
        name_clean += " (Extra)"

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
        'link_place': name_clean + "#" + item['item'],
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
            'hash': md5(item['item']),
            'rarity': item.get('rarity', 'undefined'),
            'chance': item.get('chance', 'undefined'),
        }
    )

    prepare_items[item['item']]['drops'].append(drop)

for item in prepare_items:
    db.items.insert_one(prepare_items[item])

for place in prepare_places:
    db.places.insert_one(prepare_places[place])

#os.remove('all.slim.json')

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


if download:
    p = multiprocessing.pool.Pool(20)
    p.map(download_img, downloads)
main_js = """
var hash = function(d){result = M(V(Y(X(d),8*d.length)));return result.toLowerCase()};function M(d){for(var _,m="0123456789ABCDEF",f="",r=0;r<d.length;r++)_=d.charCodeAt(r),f+=m.charAt(_>>>4&15)+m.charAt(15&_);return f}function X(d){for(var _=Array(d.length>>2),m=0;m<_.length;m++)_[m]=0;for(m=0;m<8*d.length;m+=8)_[m>>5]|=(255&d.charCodeAt(m/8))<<m%32;return _}function V(d){for(var _="",m=0;m<32*d.length;m+=8)_+=String.fromCharCode(d[m>>5]>>>m%32&255);return _}function Y(d,_){d[_>>5]|=128<<_%32,d[14+(_+64>>>9<<4)]=_;for(var m=1732584193,f=-271733879,r=-1732584194,i=271733878,n=0;n<d.length;n+=16){var h=m,t=f,g=r,e=i;f=md5_ii(f=md5_ii(f=md5_ii(f=md5_ii(f=md5_hh(f=md5_hh(f=md5_hh(f=md5_hh(f=md5_gg(f=md5_gg(f=md5_gg(f=md5_gg(f=md5_ff(f=md5_ff(f=md5_ff(f=md5_ff(f,r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+0],7,-680876936),f,r,d[n+1],12,-389564586),m,f,d[n+2],17,606105819),i,m,d[n+3],22,-1044525330),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+4],7,-176418897),f,r,d[n+5],12,1200080426),m,f,d[n+6],17,-1473231341),i,m,d[n+7],22,-45705983),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+8],7,1770035416),f,r,d[n+9],12,-1958414417),m,f,d[n+10],17,-42063),i,m,d[n+11],22,-1990404162),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+12],7,1804603682),f,r,d[n+13],12,-40341101),m,f,d[n+14],17,-1502002290),i,m,d[n+15],22,1236535329),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+1],5,-165796510),f,r,d[n+6],9,-1069501632),m,f,d[n+11],14,643717713),i,m,d[n+0],20,-373897302),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+5],5,-701558691),f,r,d[n+10],9,38016083),m,f,d[n+15],14,-660478335),i,m,d[n+4],20,-405537848),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+9],5,568446438),f,r,d[n+14],9,-1019803690),m,f,d[n+3],14,-187363961),i,m,d[n+8],20,1163531501),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+13],5,-1444681467),f,r,d[n+2],9,-51403784),m,f,d[n+7],14,1735328473),i,m,d[n+12],20,-1926607734),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+5],4,-378558),f,r,d[n+8],11,-2022574463),m,f,d[n+11],16,1839030562),i,m,d[n+14],23,-35309556),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+1],4,-1530992060),f,r,d[n+4],11,1272893353),m,f,d[n+7],16,-155497632),i,m,d[n+10],23,-1094730640),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+13],4,681279174),f,r,d[n+0],11,-358537222),m,f,d[n+3],16,-722521979),i,m,d[n+6],23,76029189),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+9],4,-640364487),f,r,d[n+12],11,-421815835),m,f,d[n+15],16,530742520),i,m,d[n+2],23,-995338651),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+0],6,-198630844),f,r,d[n+7],10,1126891415),m,f,d[n+14],15,-1416354905),i,m,d[n+5],21,-57434055),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+12],6,1700485571),f,r,d[n+3],10,-1894986606),m,f,d[n+10],15,-1051523),i,m,d[n+1],21,-2054922799),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+8],6,1873313359),f,r,d[n+15],10,-30611744),m,f,d[n+6],15,-1560198380),i,m,d[n+13],21,1309151649),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+4],6,-145523070),f,r,d[n+11],10,-1120210379),m,f,d[n+2],15,718787259),i,m,d[n+9],21,-343485551),m=safe_add(m,h),f=safe_add(f,t),r=safe_add(r,g),i=safe_add(i,e)}return Array(m,f,r,i)}function md5_cmn(d,_,m,f,r,i){return safe_add(bit_rol(safe_add(safe_add(_,d),safe_add(f,i)),r),m)}function md5_ff(d,_,m,f,r,i,n){return md5_cmn(_&m|~_&f,d,_,r,i,n)}function md5_gg(d,_,m,f,r,i,n){return md5_cmn(_&f|m&~f,d,_,r,i,n)}function md5_hh(d,_,m,f,r,i,n){return md5_cmn(_^m^f,d,_,r,i,n)}function md5_ii(d,_,m,f,r,i,n){return md5_cmn(m^(_|~f),d,_,r,i,n)}function safe_add(d,_){var m=(65535&d)+(65535&_);return(d>>16)+(_>>16)+(m>>16)<<16|65535&m}function bit_rol(d,_){return d<<_|d>>>32-_}

var item_name = window.location.hash.substr(1);
elements = document.getElementsByClassName(hash(item_name));
for (var i = 0; i < elements.length; i++) {
	elements[i].style.backgroundColor = "#DDF";
}

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
os.system('git checkout img/favicon.ico')
