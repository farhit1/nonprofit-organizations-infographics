import re


COLOR_RE = re.compile('#[^;]*')


def fill(vertex, color):
    if None:
        return
    try:
        styleString = vertex.attrs['style']
        styleString = re.sub(COLOR_RE, '#'+color, styleString)
        vertex.attrs['style'] = styleString
    except:
        pass
    try:
        for child in vertex.contents:
            fill(child, color)
    except:
        pass
