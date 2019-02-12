import os
import json
import multiprocessing.pool

from pymongo import MongoClient
import requests

requests = requests.Session()
dbname = 'warframe_drops'
os.system('rm img/* -rf')
# download file
os.system('wget https://raw.githubusercontent.com/WFCD/warframe-items/development/data/json/Mods.json')
cli = MongoClient()
# clean db
cli.drop_database(dbname)

db = cli[dbname]
# create index
db.mods.create_index('name')

mods = json.load(open('Mods.json', 'r', encoding="UTF-8"))
for mod in mods:
    if 'Beginner' in mod['uniqueName']:
        # mod['name'] += " - Defectuoso"
        continue

    name = mod['name'].replace(' ', '_').replace(
        '-', '_').replace("'", "").replace('&', 'and').lower()
    replace = [
        ("brain_storm", "brain_storm_(grakata)"),
        ("ambush_optics", "ambush_optics_(rubico)"),
        ("mesas_waltz", "mesa%E2%80%99s_waltz"),
        ("rifle_riven_mod", "rifle_riven_mod_(veiled)"),
        ('primed_pistol_ammo_mutation', 'primed_pistol_mutation'),
        ('melee_riven_mod', 'melee_riven_mod_(veiled)'),
        ('pistol_riven_mod', 'pistol_riven_mod_(veiled)'),
        ('static_alacrity', 'static_alacrity_(staticor)'),
        ('skull_shots', 'skull_shots_(viper)'),
        ('primed_pistol_ammo_mutation', 'primed_pistol_mutation'),
        ('shotgun_riven_mod', 'shotgun_riven_mod_(veiled)'),
        # ('primed_sure_footed', 'primed_sure_footed'),
        ('zaw_riven_mod', 'zaw_riven_mod_(veiled)'),
        ('vermillion_storm', 'vermilion_storm'),
        ('shrapnel_rounds', 'shrapnel_rounds_(marelok)'),
        ('thundermiter', 'thundermiter_(miter)'),
    ]
    for x in replace:
        if name == x[0]:
            name = x[1]
            break

    mod['imageName'] = "%s.png" % name
    print(mod['imageName'])
    db['mods'].insert_one(mod)
os.remove('Mods.json')

print("download images")
def download_img(imageName):
    # print("download", name)

    r = requests.get('https://api.warframe.market/v1/items/%s' %
                     imageName[:-4]).json()
    try:
        url = r['payload']['item']['items_in_set'][0]['icon']
    except:
        print("skip", r)
        return

    command = 'wget "https://warframe.market/static/assets/%s" -O "img/%s" > /dev/null 2>&1' % (
        url, imageName)
    print(command)
    os.system(command)

p = multiprocessing.pool.Pool(20)
p.map(download_img, [v['imageName'] for v in db['mods'].find({}, {'imageName': True})])
main_js = """
let arr = %s
const updateResult = query => {
	let resultList = document.querySelector(".result");
	resultList.innerHTML = "";
        if (query.length == 0){
                return
	}
	max = 10;
	actual = 0;
	arr.map(algo =>{
		[query].map(word =>{
			if(algo.toLowerCase().indexOf(word.toLowerCase()) != -1){

				if (max == actual){return ""}
        resultList.innerHTML += `<li class="list-group-item"><a href="/mod/${algo}">${algo}</a></li>`;
				actual ++;

			}
		})
	})
}

updateResult("")
""" % str([mod['name'] for mod in db.mods.find({}, {'name': True})])

with open('js/main.js', 'w') as f:
    f.write(main_js)
