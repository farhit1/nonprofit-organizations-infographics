from keynote.image import *
from keynote.rectangle import *
from keynote.text_block import *

from infographics.constants import *
from infographics.miscellaneous import *

import json


def getFirstInfographics(groupId, regionId, yearFrom, yearTo, categories, topN = 5):
    data = json.load(open('data/%d.json' % regionId))
    arr = []
    for i in range(len(data)):
        organization = data[i]
        total = 0
        if groupId in [ALL, int(organization['type']['code'])]:
            for category in categories:
                for j in organization[category]:
                    try:
                        year = int(j['date'][0:4])
                        if year >= yearFrom and year <= yearTo:
                            total += j['amount']
                    except:
                        pass
            arr.append((total, i))
    arr.sort()
    arr.reverse()

    if len(arr) < topN:
        raise Exception('not enough organizations in region')

    MIN_HEIGHT = 60
    TOTAL_HEIGHT = 470
    L = 70
    WIDTH = 900
    BOTTOM = 650

    heights = [MIN_HEIGHT for i in range(topN)]
    remains = TOTAL_HEIGHT - topN*MIN_HEIGHT
    while remains:
        maxCost = 0
        at = 0
        for i in range(topN):
            pixelCost = arr[i][0] / heights[i]
            if pixelCost > maxCost:
                maxCost = pixelCost
                at = i
        remains -= 1
        heights[at] += 1

    yPosition = BOTTOM
    objects = []

    for i in range(topN):
        organization = data[i]

        BONUS1 = 5 if heights[i] > MIN_HEIGHT + 15 else 0
        BONUS2 = 20 if heights[i] > MIN_HEIGHT + 30 else 9 if heights[i] > MIN_HEIGHT + 15 else -1
        BONUS3 = 28 if heights[i] > MIN_HEIGHT + 30 else 14 if heights[i] > MIN_HEIGHT + 15 else 1
        AMOUNT_FONT_SIZE = 35 if heights[i] > MIN_HEIGHT + 30 else 24

        yPosition -= heights[i]
        objects.append(KeynoteRectangle(L, yPosition, heights[i], WIDTH, COLORS[i]))
        objects.append(KeynoteTextBlock(L + 387, yPosition + BONUS1, AMOUNT_FONT_SIZE,
                '{} {}'.format(numberToString(arr[i][0]), rusNumeralEnding('рубл', round(arr[i][0]), 'ь', 'я', 'ей')), True, WHITE))
        objects.append(KeynoteTextBlock(L + 387, yPosition + 22 + BONUS2, 20, organization['name'], False, WHITE))
        objects.append(KeynoteTextBlock(L + 387, yPosition + 39 + BONUS3, 14, organization['type']['name'], False, WHITE))

    # header
    objects.append(KeynoteImage(L, 52, 'images/flags/%d.png' % regionId))
    objects.append(KeynoteTextBlock(L + 106, 48, 54, regionName(regionId).split('-')[0], True))

    # sub header
    receiversInfo = "Топ-%d получателей " % topN
    rusCategories = []
    if 'grants' in categories:
        rusCategories.append('грантов')
    if 'subsidies' in categories:
        rusCategories.append('субсидий')
    if 'contracts' in categories:
        rusCategories.append('контрактов')
    receiversInfo += rusJoin(rusCategories) + ' за %d-%d гг.' % (yearFrom, yearTo)
    objects.append(KeynoteTextBlock(L, 111, 24, receiversInfo, False, BLACK, 100, DEFAULT_FONT, True))
    objects.append(KeynoteTextBlock(L, 135, 24, 'Категория: %s' % groupName(groupId)))

    # rouble sign
    objects.append(KeynoteTextBlock(L, 215, 500, 'j', False, WHITE, 88, 'ALS Rubl'))

    # footer
    totalReceived = round(sum([i[0] for i in arr]))
    objects.append(KeynoteTextBlock(L, 660, 34, 'Всего выделено {} {}'.format(
            numberToString(totalReceived), rusNumeralEnding('рубл', totalReceived, 'ь', 'я', 'ей')),
                                    True, BLACK, 100, DEFAULT_FONT, True))
    objects.append(KeynoteTextBlock(L, 695, 34, 'для {} {}'.format(
            numberToString(sum([i[0] > 0 for i in arr])),
            rusNumeralEnding('организаци', round(arr[i][0]), 'и', 'й', 'й')), True))

    return objects