import re
import chardet

name = input("Name der Datei ohne Extension:")

text = []

text = open(name +".TextGrid", mode = "rb").read()

result = chardet.detect(text)
charenc = result['encoding']

mytext = text.decode(charenc)


lines = mytext.split("\n")

timestamps = []

zwischen = []

# \r Ersetzt mit none um ueberschreiben der line zu verhindern
no_r = [re.sub(r"\r", "", line) for line in lines]


item_index = []
for line in no_r:
    if '    item [' in line:
        item_index.append((no_r.index(line), line))

#Fürs Suchen der Timestamps in der Line
def Check_Nummer(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

reihenfolge = []

#Index 17 ist Startzeitpunkt des Interval des Erstens tiers, dann +4 für jedes nächste interval
newindex = item_index[0][0]+9 #Erste Text Label Index
newendindex = item_index[1][0]  #Hier endet das erste Tier

for r in no_r[newindex:newendindex+1:4]:
    newindex += 4
    print(r, "XXXX",no_r[newindex] )
    if "<P>" in r and "<P>" not in no_r[newindex]:
        reihenfolge.append("P")
    elif "<P>" in r and 'text = ""' in no_r[newindex]:
        reihenfolge.append("P")
    elif "<P>" not in r and "<P>" in no_r[newindex]:
        reihenfolge.append("Text")

#Checkt jedes textfeld jeden tiers, konstruiert reihenfolge ("TEXT", "PAUSE",....,"TEXT") zum Rekonstruieren des Files
index2 = item_index[0][0]+10
for r in no_r[index2:newendindex+1:4]:
    index2 +=4
    if "<P>" not in no_r[index2-1]:
        #print(no_r[index])
        try:
            zwischen.extend([no_r[index2-3].split()[2], no_r[index2-2].split()[2], no_r[index2-1].split()[2]])
        except IndexError:
            pass
    else:
        if zwischen:
            timestamps.append(zwischen)
            zwischen = []

words = []


for label in timestamps:
    word_label = []
    for x in label:
        if not Check_Nummer(x):
            word_label.append(x.replace('"', ''))
    laenge = float(label[0]) + float(label[-2])
    words.append((" ".join(word_label), float(label[0]), float(label[-2])))

index = 0
overallindex = 1
# :13 ist der Kopf des TextGrids, immer gleich
with open(name + "_New" + ".TextGrid", mode= "w+", encoding = "utf-8") as f:
    for x in no_r[:item_index[0][0]+5]:
        f.write(x+"\n")
    f.write("        intervals: size = "+str(len(reihenfolge)-1)+"\n")

    for r in reihenfolge:
        if r == "Text":
            f.write("        intervals [" + str(overallindex)+ "]:\n" +
                    "            xmin = " + str(words[index][1]) + "\n" +
                    "            xmax = " + str(words[index][2]) + "\n" +
                    '            text = ' + '"' + str(words[index][0]) + '"' + "\n"
                    )
            index += 1

        elif r == "P":
            if index != 0:
                try:
                    f.write("        intervals [" + str(overallindex)+ "]:\n" +
                            "            xmin = " + str(words[index-1][2]) + "\n" +
                            "            xmax = " + str(words[index][1]) + "\n" +
                            '            text = "<P>"' + "\n"
                            )
                except IndexError:
                    pass
            else:
                f.write("        intervals [" + str(overallindex) + "]:\n" +
                        "            xmin = 0" + "\n" +
                        "            xmax = " + str(words[index][1]) + "\n" +
                        '            text = "<P>"' + "\n"
                        )
        overallindex += 1

# 13882 sind restlichen Tiers
with open(name + "_New" + ".TextGrid" , encoding= "utf-8", mode = "a") as x:
    for r in no_r[item_index[0][0]:item_index[1][0]]:
        if "    item [" not in r:
            x.write(r + "\n")
        else:
            mynumber = int(re.findall(r'\d+', r)[0])
            x.write(f"    item [{str(mynumber + 1)}]:" + "\n")
    for r in no_r[item_index[1][0]:]:
        try:
            if "    item [" not in r:
                x.write(r+"\n")
            else:

                mynumber = int(re.findall(r'\d+',r)[0])
                x.write(f"    item [{str(mynumber+1)}]:" + "\n")
        except IndexError:
            pass



    # for x in reihenfolge:
    #
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

#('habe auch keine Ahnung mehr, was wir geredet haben', 3.36998958333333, 5.50998958333333),