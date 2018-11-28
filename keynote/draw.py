import os
import subprocess


def draw(blocks, pathToKeynoteSlides):
    remove = []
    strings = [
        "tell application \"Keynote\"",
        "\tset doc to open \"%s\"" % os.path.abspath(pathToKeynoteSlides),
        "\ttell doc",
        "\t\ttell first slide"
    ]
    for block in blocks:
        strings.extend(block.toText(remove, 3))
    strings.extend([
        "\t\tend tell",
        "\tend tell"
    ])
    strings.extend(['', "\texport doc to alias \"%s\" as slide images with properties {image format:JPEG}" %\
            "Macintosh HD%s" % ':'.join(os.path.abspath('slides').split('/')), ''])
    remove.reverse()
    strings.extend('\t%s' % s for s in remove)
    strings.extend([
        '\tclose doc',
        'end tell'
    ])

    bashScript = '#!/bin/bash\nosascript <<EOD\n\n' + '\n'.join(strings) + '\n\nEOD\n'
    with open('convert.sh', 'w') as out:
        out.write(bashScript)
    try:
        os.mkdir('slides')
    except:
        pass
    subprocess.call('chmod 0755 convert.sh', shell=True)
    subprocess.call('./convert.sh', shell=True)
