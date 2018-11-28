def shorten(s, maxSymbols):
    if len(s) <= maxSymbols:
        return s
    separated = s[:maxSymbols + 2].split(' ')
    separated.pop()
    if len(separated[-1]) < 3:
        separated.pop()
    return ' '.join(separated) + ' ...'
