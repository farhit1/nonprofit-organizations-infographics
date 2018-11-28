from keynote.constants import *
from keynote import block_name
from keynote import convert_color
from keynote import shorten_string


class KeynoteTextBlock:
    def __init__(self, x, y, fontSize, text,
                 isBold=False, color=BLACK, opacity=100, font=DEFAULT_FONT, disableShortening=False):
        maxLength = 1000 if disableShortening else 45

        self.x = x
        self.y = y
        if text.find('"') != -1:
            fq = text.find('"') + 1
            sq = text.find('"', fq)
            self.text = shorten_string.shorten(text[fq:sq], maxLength)
        elif text.find('(') != -1:
            fq = text.find('(') + 1
            sq = text.find(')', fq)
            self.text = shorten_string.shorten(text[fq:sq], maxLength)
        else:
            self.text = shorten_string.shorten(text, maxLength)
        self.opacity = opacity
        self.fontSize = fontSize
        self.color = convert_color.convertColorAppleScript(color)
        self.font = font
        self.name = block_name.getAppleScriptName()
        if isBold:
            self.font += ' Bold'

    def toText(self, remove, indent=0):
        remove.append('delete %s' % self.name)
        strings = [
            "set %s to make new text item" % self.name,
            "tell %s" % self.name,
            "\tset the object text to \"%s\"" % self.text,
            "\tset the size of its object text to %d" % self.fontSize,
            "\tset the color of its object text to %s" % self.color,
            "\tset the font of its object text to \"%s\"" % self.font,
            "\tset the position to {%d, %d}" % (self.x, self.y),
            "\tset the opacity to %d" % self.opacity,
            "end tell", ""
        ]
        strings = map(lambda x: '%s%s' % ('\t' * indent, x), strings)
        return strings
