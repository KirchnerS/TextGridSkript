import re

text = []

text = open("TestGrid.TextGrid", mode = "rb").read()

mytext = text.decode('utf-8')

lines = mytext.split("\n")

timestamps = []

zwischen = []

no_r = [re.sub(r"\r", "", line) for line in lines]


def Check_Nummer(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


for r in no_r[18::4]:
    if "<" not in no_r[no_r.index(r)+3]:
        zwischen.extend([no_r[no_r.index(r)+1].split()[2], no_r[no_r.index(r)+2].split()[2], no_r[no_r.index(r)+3].split()[2]])
    else:
        if zwischen:
            timestamps.append(zwischen)
            zwischen = []
summe = []

words = []

for label in timestamps:
    word_label = []
    for x in label:
        if not Check_Nummer(x):
            word_label.append(x.replace('"', ''))
    laenge = float(label[0]) + float(label[-2])
    words.append((" ".join(word_label), float(label[0]), float(label[-2])))


print(timestamps)
print(words)


    # if "        intervals " in r and "\"<p>\"" in no_r[no_r.index(r)-1] and "<" not in no_r[no_r.index(r)+3]:
    #     for i in [no_r.index(r)::4]:
    #         if "<p>" not in no_r[i + 1]:
    #             zwischen.append((no_r[i-1], no_r[i], no_r[i+1]))
    #
    #         else:
    #             timestamps.append(zwischen)
        #timestamps.append(zwischen)
        # for index in range(no_r.index(r))

#print(timestamps)

# for paar in timestamps:
#     for y in x:
#         print(y.split())
#
# print(lines)
#         timestamps.append((line, lines[lines.index(line)+3]))
#         print(line, lines[lines.index(line)+3])
# print(timestamps)


# with open("TestText.TextGrid", "w+") as f:
#     f.write('''File type = "ooTextFile"\nObject class = "TextGrid"\n\nxmin = 0\nxmax = 2.3510204081632655\ntiers? <exists>\nsize = 1\nitem []:\n    item [1]:\n        class = "IntervalTier"\n        name = "Anno"\n        xmin = 0\n        xmax = 2.3510204081632655\n        intervals: size = 4\n        intervals [1]:\n            xmin = 0\n            xmax = 0.7997809754530211\n            text = ""\n        intervals [2]:\n            xmin = 0.7997809754530211\n            xmax = 1.1304817503560034\n            text = "das"\n        intervals [3]:\n            xmin = 1.1304817503560034\n            xmax = 1.5763372593769887\n            text = "test"\n        intervals [4]:\n            xmin = 1.5763372593769887\n            xmax = 2.3510204081632655\n            text = ""
# ''')