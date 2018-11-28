def hexToBase10(number):
    result = 0
    for t in number:
        s = t.lower()
        if ord(s) in range(ord('a'), ord('f') + 1):
            result = result * 16 + ord(s) - ord('a') + 10
        elif ord(s) in range(ord('0'), ord('9') + 1):
            result += result * 16 + ord(s) - ord('0')
        else:
            raise 'Wrong symbol %s' % t
    result *= 256
    return result


def convertColorAppleScript(color):
    return "{%d, %d, %d}" % (hexToBase10(color[0:2]),
                             hexToBase10(color[2:4]),
                             hexToBase10(color[4:6]))
