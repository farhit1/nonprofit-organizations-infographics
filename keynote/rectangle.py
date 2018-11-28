from keynote.block_name import *
from keynote.convert_color import *


class KeynoteRectangle:
    def __init__(self, x, y, height, width, color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = convertColorAppleScript(color)
        self.name = getAppleScriptName()

    def toText(self, remove, indent=0):
        remove.append('delete %s' % self.name)
        strings = [
            "set %s to make new table with properties {header column count:0, header row count:0}" % self.name,
            "tell %s" % self.name,
            "\tset the row count to 1",
			"\tset the column count to 1",
            "\ttell first row",
			"\t\tset the background color to %s" % self.color,
            "\tend tell",
            "\tset the height to %d" % self.height,
            "\tset the width to %d" % self.width,
            "\tset the position to {%d, %d}" % (self.x, self.y),
            "end tell", ""
        ]
        strings = map(lambda x: '%s%s' % ('\t' * indent, x), strings)
        return strings