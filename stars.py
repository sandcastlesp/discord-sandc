import sys
text = ' '.join(sys.argv[1:])


charmap = {
    "B": ":b:",
    "å": ":AA:",
    "ä": ":AE:",
    "ö": ":OE:",
    }
state = []
for c in text:
    if c in charmap:
        state.append(charmap[c])
    elif c in [chr(c) for c in range(ord('a'),ord('z'))]:
        state.append(":regional_indicator_{}:".format(c))
    elif c == " ":
        state.append("   ")
    elif c == "å":
        state.append(":Inte_A:")
    else:
        state.append(c)
print(' '.join(state))
    
