import os

from keynote import block_name


class KeynoteImage:
    def __init__(self, x, y, path, width=100, height=50):
        self.x = x
        self.y = y
        self.path = "Macintosh HD%s" % ':'.join(os.path.abspath(path).split('/'))
        self.width = width
        self.height = height
        self.name = block_name.getAppleScriptName()

    def toText(self, remove, indent=0):
        remove.append('delete %s' % self.name)
        strings = [
            "set %s to make new image with properties {file:alias \"%s\"}" % (self.name, self.path),
            "tell %s" % self.name,
            "\tset the width to %d" % self.width,
            "\tset the height to %d" % self.height,
            "\tset the position to {%d, %d}" % (self.x, self.y),
            "end tell", ""
        ]
        strings = map(lambda x: '%s%s' % ('\t' * indent, x), strings)
        return strings
