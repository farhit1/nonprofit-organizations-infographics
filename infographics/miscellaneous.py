import json


def numberToString(n):
    n = round(n)
    s = str()
    while n:
        prepend = str(n % 1000)
        n //= 1000
        if n:
            while len(prepend) < 3:
                prepend = '0' + prepend
        if len(s):
            s = ' ' + s
        s = prepend + s
    if len(s) == 0:
        s = '0'
    return s


def rusNumeralEnding(begin, num, ending1, ending24, ending59):
    if (num % 100) in range(10, 20):
        return begin+ending59
    if num % 10 == 1:
        return begin+ending1
    if num % 10 in range(2, 5):
        return begin+ending24
    return begin+ending59


def rusJoin(l):
    if len(l) <= 1:
        return ''.join(l)
    return ', '.join(l[:-1]) + ' и ' + l[-1]


def groupName(categoryId):
    return json.load(open('data/categories.json'))[categoryId]


def regionName(regionId):
    return json.load(open('data/regions.json'))[regionId]
