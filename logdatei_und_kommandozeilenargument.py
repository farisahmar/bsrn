import argparse  # Importieren des argparse-Moduls, um Kommandozeilenargumente zu verarbeiten
import datetime  # Importieren des datetime-Moduls, um Zeitstempel zu erzeugen

def protokollieren(nachricht, logdatei):
    # Schreibt eine Nachricht mit Zeitstempel in die Logdatei.
    zeitstempel = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Aktuellen Zeitstempel erstellen
    with open(logdatei, 'a') as f:  # Logdatei im Anhängemodus öffnen
        f.write(f'{zeitstempel} - {nachricht}\n')  # Nachricht mit Zeitstempel in die Logdatei schreiben

# Einlesen der Kommandozeilenargumente
parser = argparse.ArgumentParser(description='Simulator für Multilevel-Feedback-Scheduling')  # Parser für Kommandozeilenargumente erstellen
parser.add_argument('-warteschlangen', type=int, required=True, help='Anzahl der Warteschlangen')  # Argument für die Anzahl der Warteschlangen hinzufügen
parser.add_argument('-quantum', type=int, nargs='+', required=True, help='Zeitquanten für die Warteschlangen')  # Argument für die Zeitquanten der Warteschlangen hinzufügen
parser.add_argument('-processlistfile', type=str, required=True, help='Pfad zur Eingabedatei mit den Prozessen')  # Argument für den Pfad zur Prozessliste hinzufügen
parser.add_argument('-logdatei', type=str, required=True, help='Pfad zur Logdatei')  # Argument für den Pfad zur Logdatei hinzufügen
parser.add_argument('-ausgabeformat', type=str, choices=['text', 'grafisch'], required=True, help='Ausgabeformat (text oder grafisch)')  # Argument für das Ausgabeformat hinzufügen
parser.add_argument('-ausgabedatei', type=str, required=True, help='Pfad zur Ausgabedatei')  # Argument für den Pfad zur Ausgabedatei hinzufügen

# Argumente parsen
args = parser.parse_args()  # Übergebene Argumente parsen

# Logdatei festlegen
logdatei = args.logdatei  # Pfad zur Logdatei aus den Argumenten extrahieren

# Protokollierung der Startnachricht
protokollieren("Simulator gestartet.", logdatei)  # Start des Simulators protokollieren

# Protokollierung der Kommandozeilenargumente
protokollieren(f"Kommandozeilenargumente eingelesen: {args}", logdatei)  # Eingelesene Kommandozeilenargumente protokollieren

# Weitere Protokollierungsbeispiele während der Simulation
protokollieren(f'Eingabedatei "{args.processlistfile}" erfolgreich geöffnet.', logdatei)  # Erfolgreiches Öffnen der Eingabedatei protokollieren
protokollieren('Prozesse aus Eingabedatei eingelesen.', logdatei)  # Einlesen der Prozesse protokollieren

# Initialisierung der Warteschlangen und Zeitquanten
protokollieren(f'Warteschlangen und Zeitquanten initialisiert: {args.warteschlangen} Warteschlangen, Zeitquanten {args.quantum}', logdatei)  # Initialisierung der Warteschlangen und Zeitquanten protokollieren

# Beispiel für Scheduling-Einträge
protokollieren('Scheduling gestartet.', logdatei)  # Start des Scheduling protokollieren


protokollieren('Scheduling abgeschlossen.', logdatei)  # Abschluss des Scheduling protokollieren

# Berechnung der Warte- und Laufzeiten
protokollieren('Wartezeiten und Laufzeiten berechnet.', logdatei)  # Berechnung der Warte- und Laufzeiten protokollieren

# Erstellung der Ausgabedatei
protokollieren(f'Ausgabedatei "{args.ausgabedatei}" erfolgreich erstellt.', logdatei)  # Erstellung der Ausgabedatei protokollieren

# Abschlussnachricht
protokollieren("Simulator beendet.", logdatei)  # Abschluss des Simulators protokollieren
