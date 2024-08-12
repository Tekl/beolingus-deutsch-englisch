# Changelog für Beolingus Deutsch-Englisch

Sorry, there’s no english changelog.

## v2024.08.12

### Geändert (Changed)

- Datenbestand vom 11.8.2024 mit 904138 Einträgen.

## v2024.07.14

### Geändert (Changed)

- Schreibweise von BeoLingus auf Beolingus korrigiert.
- Links in der Fußzeile von Einträgen zeigen nun zur Online-Suche auf [dict.zero-g.net](https://dict.zero-g.net), da die Suche auf beolingus.de [abgeschaltet](https://tekl.de/news/beolingus-website-wird-ende-juni-2024-eingestellt) wurde.
- Datenbestand vom 11.7.2024 mit 899477 Einträgen.

## v2024.05.14

### Geändert (Changed)

- Datenbestand vom 10.5.2024 mit 898498 Einträgen.

## v2024.01.19

### Fehler behoben (Fixed)

- Bei einigen Anwendern zeigte das Plug-in nur leere Seiten, weil bei der Installation nicht alle Standard-Optionen gesetzt wurden.

## v2023.12.28

### Geändert (Changed)

- Datenbestand vom 13.4.2023 mit 877754 Einträgen.
- Font-Auswahl reduziert, da das Lexikon schon länger nur noch System-Fonts unterstützt.

### Fehler behoben (Fixed)

- Automatische Aktivierung des Plug-ins nach der Installation verbessert. Manchmal wurden bereits aktivierte Plug-ins deaktiviert.

## v2022.07.02

### Geändert (Changed)

- Datenbestand vom 22.7.2022 mit 859482 Einträgen (nun aber wirklich).

## v2022.07.22

### Geändert (Changed)

- ~~Datenbestand vom 22.7.2022 mit 859482 Einträgen.~~ (es war nur der Stand vom 23.12.2021 enthalten)
- Änderung des Namens im Copyright und im Klappentext (Wolfgang Reszel→Wolfgang Kreutz).

## v2022.03.16

### Geändert (Changed)

- Datenbestand vom 23.12.2021 mit 848014 Einträgen
- Code auf Python 3 aktualisiert, weil Python 2 mit macOS 12.3 nicht mehr verfügbar ist. Das ist aber nur relevant, wenn man das Plug-in selbst erzeugen möchte. 

## v2021.12.09

### Fehler behoben (Fixed)

- Der Installer behebt jetzt zuverlässiger das Problem mit leeren Seiten nach dem Update von einer sehr alten Version des Plug-ins.

### Geändert (Changed)

- Aktualisierte Plug-in-Grafik im Installer und fürs Bundle.

## v2021.11.05

### Fehler behoben (Fixed)

- Der Installer kann nun auch auf ganz frischen Systemen das Plug-in automatisch aktivieren.
- Der Installer verlangt nicht mehr, dass der Prozess DictionaryServiceHelper geschlossen sein muss. Ist nicht nötig.

### Geändert (Changed)

- Datenbestand vom 21.10.2021 mit 843044 Einträgen.

## v2021.10.17

### Fehler behoben (Fixed)

- Die Installation funktioniert nun wieder unter OS X 10.11 und bricht nicht mehr mit dem Fehler „Ungültige Signatur“ ab.

## v2021.10.06

### Geändert (Changed)

- Das Installationsprogramm setzt nun die Standard-Einstellungen, sofern entsprechende Einträge in der Preferences-Datei fehlen. Damit wird verhindert, dass das Plug-in keine Inhalte zeigt ([siehe FAQ](https://tekl.de/lexikon-faq/lexikon-plug-zeigt-keine-inhalte)) falls die zuvor installierte Version weniger Einstellmöglichkeiten bot.

## v2021.09.29

### Fehler behoben (Fixed)

- Die Einstellungen waren versehentlich komplett leer (Danke maelcum [#2](https://github.com/Tekl/beolingus-deutsch-englisch/issues/2)).

## v2021.09.28

### Hinzugefügt (Added)

- Man kann neben der Standardschrift von macOS aus 28 weiteren Fonts auswählen. Die Auswahl enthält größtenteils System-Fonts aber auch meine zwei kommerziellen Lieblings-Fonts „Sys 2.0“ und „PragmataPro“ von [Fabrizio Shiavi](https://fsd.it).
- In den Einstellungen des Plug-ins und im Klappentext (Vorderer/hinterer Teil) gibt es einen Button, über den Sie prüfen können, ob eine neue Version des Plug-ins vorliegt. Im Sinne der Datensparsamkeit erfolgt die Überprüfung nicht automatisch im Hintergrund, sondern nur manuell per Klick.
- Respektiert die [Jugendschutz-Einstellung](https://support.apple.com/de-de/guide/mac-help/mchlbcf0dfe2/mac) von macOS für anstößige Sprache. Damit lassen sich alle obszönen Einträge verbergen, die mit [vulg.] gekennzeichnet sind.
- Verweilt der Mauspfeil auf Abkürzungen in Klammern wie [fig.], erscheint ein Tooltip mit einer Erläuterung.

### Geändert (Changed)

- Berücksichtigt deutlich mehr Wortformen bei Suchbegriffen (auf Basis des [Morphologie-Lexikons](https://www.danielnaber.de/morphologie/) von Daniel Naber, Stand 25.6.2021, LT v5.4)
- Das Plug-in liegt nun in einem moderneren Format vor, das allerdings nur zu OS X 10.11 und höher kompatibel ist. Das verhindert auf aktuellen Systemen willkürliche Abstürze bei einigen Programmen wie PDF Expert.
- Datenbestand vom 29.08.2021 mit 839160 Einträgen.

## v2020.05.10

### Geändert (Changed)

- Datenbestand vom 09.05.2020 mit 803022 Einträgen.

## v2019.04.25

### Geändert (Changed)

- Das Installationsprogramm enthält nun eine Deinstallations-Routine.

### Fehler behoben (Fixed)

- Das Lexikon flackert nun nicht mehr bei der Eingabe von Suchbegriffen im Darkmode von macOS 10.14 Mojave.
- Absturzursache bei einigen Anwendern in OS X 10.10.5 Yosemite behoben.

## v2019.04.15

### Hinzugefügt (Added)

- Einstellung hinzugefügt, über die man die Flaggen-Symbole ausschalten kann.

### Geändert (Changed)

- Das Plug-in wird wieder über ein Installations-Paket für alle Benutzer installiert. Über „Ort für die Installation ändern“ lässt es sich weiterhin für einzelne Benutzer installieren.
- Datenbestand vom 30.03.2019 mit 777685 Einträgen.
- Update für macOS 10.14 Mojave mit Unterstützung des Darkmode.
- Flaggen-Icons durch Emojis ersetzt.

### Entfernt (Removed)

- Da die Updateprüfung auf neueren Versionen von macOS nicht mehr funktioniert, habe ich sie entfernt. Sie funktionierte eh nicht zuverlässig.
- Obsolete Einstellungen entfernt.

## v2015.10.08

### Geändert (Changed)

- Datenbestand vom 8.6.2015 mit 667044 Einträgen.
- Update für OS X El Capitan.
