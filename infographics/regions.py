from keynote.image import *
from keynote.rectangle import *
from keynote.text_block import *
from keynote.convert_color import hexToBase10

from infographics.constants import *
from infographics.fill_svg import fill
from infographics.miscellaneous import *

from bs4 import BeautifulSoup
import math
import subprocess


GOLD = 'DBA501'
SILVER = '424242'
BRONZE = '945200'
BLUE = '004C86'
HEADER = '009193'


def getThirdInfographics(groupId, yearFrom, yearTo, categories):
    arr = json.load(open('data/arr.json'))
    pic = BeautifulSoup(open('images/russia.svg'), 'lxml')

    regionNumbers = [0 for i in range(MAX_REGIONS)]

    for group in range(1, MAX_CATEGORIES):
        if groupId in [ALL, group]:
            for region in range(1, MAX_REGIONS):
                for year in range(yearFrom, yearTo + 1):
                    for category in categories:
                        regionNumbers[region] += arr[category][region][str(year)][group]

    leaders = [(regionNumbers[i], i) for i in range(MAX_REGIONS)]
    leaders.sort()
    leaders.reverse()

    MAP_ID = {
        1: "AD",
        2: "BA",
        3: "BU",
        4: "AL",
        5: "DA",
        6: "IN",
        7: "KB",
        8: "KL",
        9: "KC",
        10: "KR",
        11: "KO",
        12: "ME",
        13: "MO",
        14: "SA",
        15: "SE",
        16: "TA",
        17: "TY",
        18: "UD",
        19: "KK",
        20: "CE",
        21: "CU",
        22: "ALT",
        23: "KDA",
        24: "KYA",
        25: "PRI",
        26: "STA",
        27: "KHA",
        28: "AMU",
        29: "ARK",
        30: "AST",
        31: "BEL",
        32: "BRY",
        33: "VLA",
        34: "VGG",
        35: "VLG",
        36: "VOR",
        37: "IVA",
        38: "IRK",
        39: "KGD",
        40: "KLU",
        41: "KAM",
        42: "KEM",
        43: "KIR",
        44: "KOS",
        45: "KGN",
        46: "KRS",
        47: "LEN",
        48: "LIP",
        49: "MAG",
        50: "MOS",
        51: "MUR",
        52: "NIZ",
        53: "NGR",
        54: "NVS",
        55: "OMS",
        56: "ORE",
        57: "ORL",
        58: "PNZ",
        59: "PER",
        60: "PSK",
        61: "ROS",
        62: "RYA",
        63: "SAM",
        64: "SAR",
        65: "SAK",
        66: "SVE",
        67: "SMO",
        68: "TAM",
        69: "TVE",
        70: "TOM",
        71: "TUL",
        72: "TYU",
        73: "ULY",
        74: "CHE",
        75: "Zabaykalsky",
        76: "YAR",
        77: "MOW",
        78: "SPE",
        79: "YEV",
        83: "NEN",
        86: "KHM",
        87: "CHU",
        89: "YAN",
        91: "Krimea",
        92: "Sevastopol"
    }

    colors = [None for i in range(MAX_REGIONS)]

    fill(pic.find(id=MAP_ID[leaders[0][1]]), GOLD)
    fill(pic.find(id=MAP_ID[leaders[1][1]]), SILVER)
    fill(pic.find(id=MAP_ID[leaders[2][1]]), BRONZE)
    hundertPercent = leaders[3][0]
    for i in range(3, len(leaders)):
        color = str()
        for j in range(3):
            c = hexToBase10(BLUE[2*j:2*j+2]) // 256
            c = round(255 - (255 - c) * math.pow(leaders[i][0] / hundertPercent, 0.25))
            cstr = str()
            while c:
                x = c % 16
                c //= 16
                if x in range(10, 16):
                    cstr = chr(ord('A')+x-10) + cstr
                else:
                    cstr = chr(ord('0')+x) + cstr
            while len(cstr) < 2:
                cstr = '0' + cstr
            color += cstr
        if leaders[i][1] in MAP_ID:
            fill(pic.find(id=MAP_ID[leaders[i][1]]), color)
        colors[leaders[i][1]] = color

    objects = []

    # backward part of header
    objects.append(KeynoteRectangle(0, 0, 173, 1024, HEADER))

    # first
    objects.append(KeynoteRectangle(25, 594, 50, 105, GOLD))
    objects.append(KeynoteTextBlock(101, 596, 40, "1", True, WHITE))
    objects.append(KeynoteTextBlock(138, 593, 28, regionName(leaders[0][1]), True))
    objects.append(KeynoteTextBlock(138, 619, 19, "%s %s" % (numberToString(leaders[0][0]), rusNumeralEnding(
        'рубл', round(leaders[0][0]), 'ь', 'я', 'ей'
    ))))

    # second
    objects.append(KeynoteRectangle(25, 649, 50, 105, SILVER))
    objects.append(KeynoteTextBlock(98, 651, 40, "2", True, WHITE))
    objects.append(KeynoteTextBlock(138, 648, 28, regionName(leaders[1][1]), True))
    objects.append(KeynoteTextBlock(138, 673, 19, "%s %s" % (numberToString(leaders[1][0]), rusNumeralEnding(
        'рубл', round(leaders[1][0]), 'ь', 'я', 'ей'
    ))))

    # third
    objects.append(KeynoteRectangle(25, 704, 50, 105, BRONZE))
    objects.append(KeynoteTextBlock(98, 706, 40, "3", True, WHITE))
    objects.append(KeynoteTextBlock(138, 703, 28, regionName(leaders[2][1]), True))
    objects.append(KeynoteTextBlock(138, 728, 19, "%s %s" % (numberToString(leaders[2][0]), rusNumeralEnding(
        'рубл', round(leaders[2][0]), 'ь', 'я', 'ей'
    ))))

    # fourth
    objects.append(KeynoteRectangle(517, 594, 50, 105, colors[leaders[3][1]]))
    objects.append(KeynoteTextBlock(587, 596, 40, "4", True, WHITE))
    objects.append(KeynoteTextBlock(632, 593, 28, regionName(leaders[3][1]), True))
    objects.append(KeynoteTextBlock(632, 619, 19, "%s %s" % (numberToString(leaders[3][0]), rusNumeralEnding(
        'рубл', round(leaders[3][0]), 'ь', 'я', 'ей'
    ))))

    # fifth
    objects.append(KeynoteRectangle(517, 649, 50, 105, colors[leaders[4][1]]))
    objects.append(KeynoteTextBlock(587, 651, 40, "5", True, WHITE))
    objects.append(KeynoteTextBlock(632, 648, 28, regionName(leaders[4][1]), True))
    objects.append(KeynoteTextBlock(632, 673, 19, "%s %s" % (numberToString(leaders[4][0]), rusNumeralEnding(
        'рубл', round(leaders[4][0]), 'ь', 'я', 'ей'
    ))))

    # sixth
    objects.append(KeynoteRectangle(517, 704, 50, 105, colors[leaders[5][1]]))
    objects.append(KeynoteTextBlock(587, 706, 40, "6", True, WHITE))
    objects.append(KeynoteTextBlock(632, 703, 28, regionName(leaders[5][1]), True))
    objects.append(KeynoteTextBlock(632, 728, 19, "%s %s" % (numberToString(leaders[5][0]), rusNumeralEnding(
        'рубл', round(leaders[5][0]), 'ь', 'я', 'ей'
    ))))

    # map
    with open('images/map.svg', 'w') as f:
        picData = str(pic)
        picData = picData[picData.find('<svg'):picData.find('</body>')]
        f.write(picData)
    subprocess.call('rsvg-convert -h 1000 images/map.svg > images/map.png', shell=True)
    objects.append(KeynoteImage(32, 30, 'images/map.png', 950, 560))

    # header
    objects.append(KeynoteRectangle(370, 120, 52, 130, HEADER))
    objects.append(KeynoteTextBlock(32, 20, 44, 'Топ регионов в %d-%d гг.' % (yearFrom, yearTo), True, WHITE))
    rusCategories = []
    if 'grants' in categories:
        rusCategories.append('грантам')
    if 'subsidies' in categories:
        rusCategories.append('субсидиям')
    if 'contracts' in categories:
        rusCategories.append('контрактам')
    objects.append(KeynoteTextBlock(32, 62, 44, 'по ' + rusJoin(rusCategories), True, WHITE))
    objects.append(KeynoteTextBlock(32, 117, 26, 'Категория: %s' % groupName(groupId), False, WHITE))

    return objects
