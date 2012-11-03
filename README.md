Merodii
=====================

Eine Implementierung von Merodii (Chatbot für #nsw-anime)

Features
=====================
(quoted by Monk42)

*

    !hilfe regeln = Zeigt regeln an 
    !hilfe = zeigt alle hilfen an 
    !hilfe FUNKTION = Zeigt zu der jeweiligen Funktion ausser Funktionen für Moderatoren an wie sie geht 
*

    !stream =zeigt den Das aktuelle Lied an das auf dem Stream Läuft 
    !fliegen = User wird von Merodii mit einen Abschiedsgruß geschmissen 
    !kekse USER = Merodii wirft Kekse auf einen User der im Chat Online ist, ist der User nicht vorhanden frisst sie die Kekse selber 
    !plüsch USER = Merodii plüscht bestimmten User, ist der User nicht vorhanden plüscht sie Oto 
    !glaskugel = Merodii lässt einen zufälligen SInnfreien Spruch wie "Nachts ist es kälter als draußen von"sich 
    !zitat = Merodii zitiert eine Berühmte Persönlichkeit 

*

    !dj SENDUNGSNAMEN = damit änderte man den Topic vom NSW CHannel 
    !pl = damit setzte man den Topic zurück auf die Playliste wenn die Sendung vorbei war


Installierung
=====================

Benötigt wird python3.
Zum starten: python3 phenny -c config/merodii.py

Benötigte Python Module:
oursql (für fun actions)


Implementierung
=====================

Phenny selbst ist ein IRC Bot-Framework zur einfachen Implementation eines Bots.
Die NSW Funktionen liegen in modules/nsw.py. Jede Funktion verfügt über einen Trigger (commands/event/rule), sowie einen Hilfetext (example).
Im Helper Package liegen die Hilfsfunktionen zum auslesen von Website, Stream oder ähnlichem.
Viele NSW Funktionen beziehen sich dabei aus config Einstellungen aus config/merodii.py. Ein Großteil der Konfiguration sollte darüber erfolgen.
Aktive Module sind nsw und startup. Startup übernimmt die Authentifizierung gegenüber Authserv und das Betreten der Channel.



