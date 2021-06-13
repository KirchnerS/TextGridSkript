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

# Speichert Zeilennumer und tier number als list of tuples
item_index = []
for line in no_r:
    if '    item [' in line:
        item_index.append((no_r.index(line), line))

print(item_index)

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
        # Bei Pause Wörter in timestamps appenden
        if zwischen:
            timestamps.append(zwischen)
            zwischen = []

words = []
#print(timestamps)


for label in timestamps:
    word_label = []
    for x in label:
        if not Check_Nummer(x):
            word_label.append(x.replace('"', ''))
    laenge = float(label[0]) + float(label[-2])
    words.append((" ".join(word_label), float(label[0]), float(label[-2])))

# Hier werden die Mittelpunkte der annotierten Pausen gespiechert, um zu überprüfen, ob dieses Label kopiert werden muss
# oder nicht

range_pauses_cc = [] # Tuple aus Range der Pausen nach zusammenlegen, also (10.34, 12.00) für label von start bis ende
range_pauses_anno = []
for i in range(int(item_index[6][0]),int(item_index[7][0]),4):
    if 'text = "p"' in no_r[i+1]:
        range_pauses_anno.append((float(no_r[i-1].split()[2]), float(no_r[i].split()[2])))
        #print(float(no_r[i-1].split()[2])+(float(no_r[i].split()[2]) - float(no_r[i-1].split()[2]))/2)

print("DAS SIND DIE ANNOS LABELS\n",range_pauses_anno)
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
                    range_pauses_cc.append((words[index-1][2], words[index][1]))
                except IndexError:
                    pass
            else:
                f.write("        intervals [" + str(overallindex) + "]:\n" +
                        "            xmin = 0" + "\n" +
                        "            xmax = " + str(words[index][1]) + "\n" +
                        '            text = "<P>"' + "\n"
                        )
                range_pauses_cc.append((0, words[index][1]))
        overallindex += 1
print("DAS SIND DIE CC\n\n\n",range_pauses_cc)
Test_liste = []
for x in range_pauses_cc:
    for y in range_pauses_anno:
        if (x[0] >= y[0]) and (x[0] <= y[1]):
            Test_liste.append(("DA IST SCHON NE PAUSE", y[0], y[1]))

        elif (x[1] >= y[0]) and (x[1] <= y[1]):
            Test_liste.append(("DA IST SCHON NE PAUSE", y[0], y[1]))

        elif (x[0] >= y[0]) and (x[1] <= y[1]):
            Test_liste.append(("DA IST SCHON NE PAUSE", y[0], y[1]))

        elif (x[0] < y[0]) and (x[1] > y[1]):
            Test_liste.append(("DA IST SCHON NE PAUSE", y[0], y[1]))

        elif (x[0],x[1]) not in Test_liste:
            Test_liste.append((x[0],x[1]))





print(Test_liste)
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



