appleScriptObjects = 0
def getAppleScriptName():
    global appleScriptObjects
    appleScriptObjects += 1
    return "object" + str(appleScriptObjects)
