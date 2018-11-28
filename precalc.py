from infographics.constants import *

import json
import os
import urllib.request
import zipfile


DATASET = 'http://hubofdata.ru/dataset/88131b19-0cb2-430e-97ac-af5c9c92a1a1/resource/12204501-7bd2-4db8-9652-27a7361e925b/download/openngodb_dump_07112017.zip'


if __name__ == '__main__':
    os.mkdir('data')

    print("[0/4] Downloading data archive")
    request = urllib.request.Request(DATASET, headers={'User-Agent' : "Magic Browser"})
    result = urllib.request.urlopen(request)
    with open('data/archive.zip', 'wb') as file:
        file.write(result.read())

    print("[1/4] Extracting archive")
    with zipfile.ZipFile('data/archive.zip', 'r') as zipRef:
        zipRef.extractall('data')
    os.rename('data/openngodb_dump_07112017.json', 'data/0.json')
    os.remove('data/archive.zip')

    print("[2/4] Splitting data")
    organizationsByRegion = [[] for i in range(MAX_REGIONS)]
    regions = ['' for i in range(MAX_REGIONS)]
    categories = ['' for i in range(MAX_CATEGORIES)]
    data = json.load(open('data/0.json'))

    arr = dict()
    for category in CATEGORIES:
        arr[category] = [dict() for i in range(MAX_REGIONS)]
        for regionNumber in range(MAX_REGIONS):
            for year in range(2010, 2030):
                arr[category][regionNumber][year] = [0 for i in range(MAX_CATEGORIES)]

    for organization in data:
        regionNumber = int(organization['region']['code'])
        typeCode = int(organization['type']['code'])
        organizationsByRegion[int(organization['region']['code'])].append(organization)
        regions[regionNumber] = organization['region']['name']
        categories[typeCode] = organization['type']['name']
        for cat in CATEGORIES:
            for j in organization[cat]:
                try:
                    year = int(j['date'][0:4])
                    arr[cat][regionNumber][year][typeCode] += j['amount']
                except:
                    pass

    print("[3/4] Printing data")
    for i in range(1, MAX_REGIONS):
        if organizationsByRegion[i]:
            with open('data/%d.json' % i, 'w') as out:
                json.dump(organizationsByRegion[i], out)

    regions[ALL] = 'Российская Федерация'
    regions[7] = 'Кабардино-Балкария'
    regions[9] = 'Карачаево-Черкессия'
    regions[15] = 'Северная Осетия'
    regions[79] = 'Еврейская АО'
    regions[86] = 'Ханты-Мансийский АО'
    regions[89] = 'Ямало-Ненецкий АО'
    categories[10] = 'Объединения юридических лиц'
    categories[20] = 'Союз общественных объединений'
    categories[22] = 'Садоводческое некоммерческое партнерство'
    categories[25] = 'Ассоциация фермерских хозяйств'
    categories[32] = 'Садоводческое некоммерческое объединение'
    categories[ALL] = 'все'
    with open('data/regions.json', 'w') as out:
        json.dump(regions, out)
    with open('data/categories.json', 'w') as out:
        json.dump(categories, out)
    with open('data/arr.json', 'w') as out:
        json.dump(arr, out)

    print("[4/4] Done")
