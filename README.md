# Skript zur Konkatenation von Labels in **.TextGrid**-Dateien
Dieses Skript dient zur Konkatenation von Pausen-Labels und Labels einzelner Wörter zu Labels in Form einer Satzstruktur in **.TextGrid**-Dateien.
Dabei werden aufeinanderfolgende Labels einzelner Wörter oder Pausen zu einem Label zusammengeführt. <br>
Außerdem wird eine **.csv**-Datei erstellt, welche die Unterschiede zwischen den vorannotierten Pausen und den danach annotierten Pausen hinsichtlich ihrer Länge vergleicht. 

## Ausführung
Zur Ausführung muss sich die Zieldatei (.TextGrid-Datei) im gleichen Ordner wie das Skript befinden.
Folgend wird das Skript ausgeführt:
```
python Skript.py
```
Danach wird man aufgefordert, den Namen der Datei anzugeben. <br>
<br>
*Name der Datei ohne Extension:*
<br>
Nach der Angabe des Namens werden im gleichen Ordner sowohl ein Textgrid (*ALTER_NAME*\_New.TextGrid) als auch eine **.csv**-Datei erstellt.

### .csv-Datei
Die .csv-Datei beinhaltet: <br>
* den Namen des vorannotierten Labels (Spalte 1)
* den Namen des danach annotierten Labels oder *COND*, wenn sich der Anfangs- und/oder Endpunkt des Pausenintervalls vom vorannotierten Punkt unterscheidet (Spalte 2)
* den Startpunkt des vorannotierten Intervalls (Spalte 3)
* den Endpunkt des vorannotierten Intervalls (Spalte 4)
* den Startpunkt des danach annotierten Intervalls (Spalte 5)
* den Endpunkt des danach annotierten Intervalls (Spalte 6) 
* die Differenz zwischen den Startpunkten des vorannotierten und danach annotierten Intervalls (Spalte 7)
* die Differenz zwischen den Endpunkten des vorannotierten und danach annotierten Intervalls (Spalte 8)
Weitere Erklärungen zu *COND* befinden sich im Abschnitt *conditions*.

<br>

Folgende Abbildung zeigt einen Ausschnitt aus der csv.-Datei:

![.csv-Datei](https://github.com/KirchnerS/TextGridSkript/blob/master/EXCEL_2021-07-06_12-19-13.png)

## conditions
Unterscheiden sich die Start- und/oder Endpunkte der vorannotierten und danach annotierten Pausen, so wird in der .csv-Datei *COND* annotiert. <br>
Seien *X0* der Startpunkt des voranotierten Labels, *X1* der Endpunkt des vorannotierten Labels, *Y0* der Startpunkt des danach annotierten Labels und *Y1* der Endpunkt des danach annotierten Labels, so gilt:
* COND1, wenn X0>=Y0 & X0<=Y1
* COND2, wenn X1>=Y0 & X1<=Y1
* COND3, wenn X0>=Y0 & X1<=Y1
* COND4, wenn X0<Y0 & X1>Y1

