# Parses CSS

READ_PROPERTIES = [
    "background-color",
    "background",
    "color",
    "box-shadow",
    "text-shadow",
    "border",
    "border-color",
    "border-left",
    "border-bottom",
]

PREDEF_COLORS = {
    "white": "#fff",
    "black": "#000"
}

def parse(fstr, colorDict):
    # Flags
    curr = 0 # Current Position
    startPtr = 0 # Start of Parsing Position
    endPtr = 0 # End Parsing Position, -1 if not yet found

    # Comment Parsing
    isComment = False
    commentStage = 0 # 1 if "/" is found, then 0 if "*" is found, after setting the isComment Variable. 

    while curr < len(fstr):
        c = fstr[curr]
        if isComment:
            # Check if comment is ending
            if commentStage == 0 and c == "*":
                commentStage = 1
                curr += 1
                continue
            if commentStage == 1 and c == "/":
                isComment = False
                commentStage = 0
                curr += 1
                continue
            elif commentStage == 1:
                commentStage = 0
        else:
            # Check if a comment is starting
            if commentStage == 0 and c == "/":
                commentStage = 1
                curr += 1
                continue
            if commentStage == 1 and c == "*":
                commentStage = 0
                isComment = True
                continue
            elif commentStage == 1:
                commentStage = 0
            
            # This is most likely a selector
            curr = parseSelector(fstr, curr + 1, colorDict)

        curr += 1



# str -> CSS String to be parsed
# start -> Starting Position of Parsing
# colorDict -> Dictionary to insert Colors into
# @return: End Index
def parseSelector(fstr, start, colorDict):
    # print("Parsing Selector:", start)
    curr = start

    foundScope = False

    selectorStr = ""

    # Comment Parsing
    isComment = False
    commentStage = 0 # 1 if "/" is found, then 0 if "*" is found, after setting the isComment Variable. 

    while curr < len(fstr):
        # Check if comment
        c = fstr[curr]
        if isComment:
            # Check if comment is ending
            if commentStage == 0 and c == "*":
                commentStage = 1
                curr += 1
                continue
            if commentStage == 1 and c == "/":
                isComment = False
                commentStage = 0
                # print("Selector: Comment Ended")
                curr += 1
                continue
            elif commentStage == 1:
                commentStage = 0
        else:
            # Check if a comment is starting
            if commentStage == 0 and c == "/":
                commentStage = 1
                curr += 1
                continue
            if commentStage == 1 and c == "*":
                commentStage = 0
                isComment = True
                # print("Selector: Comment Started")
                curr += 1
                continue
            elif commentStage == 1:
                commentStage = 0
            
            # Look for properties
            if not foundScope and c == "{":
                selectorStr = selectorStr.lstrip().rstrip()
                curr = parseScope(fstr, curr + 1, selectorStr, colorDict)
                foundScope = False
                # curr += 1
                # continue
                return curr

            if not foundScope:
                selectorStr = selectorStr + c
        curr += 1

    return curr


def parseScope(fstr, start, selectorStr, colorDict):
    # print("Parsing Scope:", selectorStr)
    curr = start

    propertyName = ""
    propertyValue = ""

    parsingName = True
    parsingValue = False

    # Comment Parsing
    isComment = False
    commentStage = 0 # 1 if "/" is found, then 0 if "*" is found, after setting the isComment Variable.

    while curr < len(fstr):
        # print("Scope: Status:", parsingName, parsingValue, curr)
        # Check if comment
        c = fstr[curr]
        if isComment:
            # Check if comment is ending
            if commentStage == 0 and c == "*":
                commentStage = 1
                curr += 1
                continue
            if commentStage == 1 and c == "/":
                isComment = False
                commentStage = 0
                # print("Scope: Comment Ended")
                curr += 1
                continue
            elif commentStage == 1:
                commentStage = 0
        else:
            # Check if a comment is starting
            if commentStage == 0 and c == "/":
                commentStage = 1
                curr += 1
                continue
            if commentStage == 1 and c == "*":
                commentStage = 0
                isComment = True
                # print("Scope: Comment Started")
                curr += 1
                continue
            elif commentStage == 1:
                commentStage = 0

            # Check for end of scope
            if c == "}":
                # print("Closing Scope")
                return curr

            if parsingName:
                if c == ":":
                    parsingName = False
                    parsingValue = True
                    propertyName = propertyName.lstrip().rstrip()
                    curr += 1
                    continue
                elif c == "{":
                    # Special case for media queries
                    # print("Found a Nested Scope!")
                    parsingValue = False
                    parsingName = True
                    propertyName = propertyName.lstrip().rstrip()
                    curr = parseScope(fstr, curr + 1, selectorStr + "|" + propertyName, colorDict)
                    propertyName = ""
                    propertyValue = ""
                    curr += 1
                    continue
                else:
                    propertyName = propertyName + c
            if parsingValue:
                if c == ";":
                    parsingValue = False
                    parsingName = True
                    propertyValue = propertyValue.lstrip().rstrip()
                    parseProperty(propertyName, propertyValue, selectorStr, colorDict)
                    propertyName = ""
                    propertyValue = ""
                    curr += 1
                    continue
                elif c == "{":
                    # Special case for media queries
                    # print("Found a Nested Scope!")
                    parsingValue = False
                    parsingName = True
                    propertyValue = propertyValue.lstrip().rstrip()
                    curr = parseScope(fstr, curr + 1, selectorStr + "|" + propertyName, colorDict)
                    propertyName = ""
                    propertyValue = ""
                    curr += 1
                    continue
                else:
                    propertyValue = propertyValue + c
        curr += 1
    return curr

def parseProperty(name, value, selectorStr, colorDict):
    # print("Parsed Property!", name, value)
    if (name in READ_PROPERTIES):
        print("Parsed:", selectorStr, "->", name, value)
        color = parseColor(value)
        print("\tColor:", color)
        if color in colorDict:
            colorDict[color].append(selectorStr)
        else:
            colorDict[color] = []
            colorDict[color].append(selectorStr)
    pass

# Returns an rgba value from a passed-in color
def parseColor(value):
    r = 0
    g = 0
    b = 0
    a = 0
    prefix = -1

    # Try parsing as a hex string
    prefix = value.find("#")
    if prefix != -1:
        print("Found a Hex Color:", value, value[prefix + 1:prefix + 1 + 6])
        rstr = ""
        bstr = ""
        gstr = ""
        astr = ""
        if len(value) - prefix >= 9 and value[prefix + 1:prefix + 1 + 8].find(" ") == -1:
            # 8-character version
            rstr = value[prefix + 1 : prefix + 1 + 2]
            bstr = value[prefix + 1 + 2 : prefix + 1 + 4]
            gstr = value[prefix + 1 + 4 : prefix + 1 + 6]
            astr = value[prefix + 1 + 6 : prefix + 1 + 8]
            print("Parsed Hex8 Color: ", rstr, bstr, gstr, astr)
        elif len(value) - prefix >= 7 and value[prefix + 1:prefix + 1 + 6].find(" ") == -1:
            # 6-character Version
            rstr = value[prefix + 1 : prefix + 1 + 2]
            bstr = value[prefix + 1 + 2 : prefix + 1 + 4]
            gstr = value[prefix + 1 + 4 : prefix + 1 + 6]
            astr = "FF"
            print("Parsed Hex6 Color: ", rstr, bstr, gstr)
        elif len(value) - prefix >= 4 and value[prefix + 1:prefix + 1 + 3].find(" ") == -1:
            # 3-character version
            rstr = value[prefix + 1] + value[prefix + 1]
            bstr = value[prefix + 1 + 1] + value[prefix + 1 + 1]
            gstr = value[prefix + 1 + 2] + value[prefix + 1 + 2]
            astr = "FF"
            print("Parsed Hex3 Color: ", rstr, bstr, gstr)
        r = int(rstr, 16)
        g = int(gstr, 16)
        b = int(bstr, 16)
        a = int(astr, 16)

    # rgba value
    prefix = value.find("rgba(")
    if prefix != -1:
        # @TODO Finish This
        pass
    
    # css variable (not supported)
    prefix = value.find("var(")
    if prefix != -1:
        print("CSS Variables are not yet supported!")
        return

    # Try searching for predefined colors
    for val in value.split(" "):
        if val in PREDEF_COLORS.keys():
            return parseColor(PREDEF_COLORS[val])
    
    return "rgba({}, {}, {}, {})".format(r,g,b,a)


