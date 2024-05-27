# Importe = Erweiterung der Programmiermöglichkeiten
import argparse # Parsen von Kommandozeilenargumente
import json #Ergebnisse im JSON-Format speichern, falls notwendig/gewollt
import matplotlib.pyplot as plt #Grafische Ausgaben, falls notwendig

#Definieren der Argumente für die Ausgabedatei, als auch Logdatei
#Funktion zum Parsen der Kommandozeilenargumente
#Parsen = Analyse der Eingabedateien und diese in eine strukturierte Form zu bringen. Die das Programm verarbeiten kann
def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulator für das Multilevel-Feedback-Scheduling')
    parser.add_argument('-ausgabeformat', type=str, choices=['text', 'grafisch'], required=True, help='Ausgabeformat')
    parser.add_argument('-ausgabedatei', type=str, required=True, help='Datei für die Ausgabe')
    parser.add_argument('-logdatei', type=str, required=True, help='Datei für Logdaten')
    return parser.parse_args()

args = parse_arguments() #ist Aufruf der Funktion zum Parsen der Argumente

#Funktion zum Schreiben der Logdatei
#def schreibe_log(dateiname, logs):
   # with open(dateiname, 'w') as file:
        for zeile in ergebnisse: 
            file.write(zeile + '\n')

#Funktion zum Schreiben von Ergebnissen in eine Textdatei
def schreibe_ergebnisse_text(dateiname, ergebnisse):
    with open(dateiname, 'w') as file:
        for zeile in ergebnisse:
            file.write(zeile + '\n')

# Funktion zum Erstellen eines Gantt-Diagramms und Speichern als Bilddatei
def erstelle_gantt_chart(dateiname, prozesse):
    fig, gnt = plt.subplots()  # Erstellt eine neue Figur und ein Achsenobjekt
    gnt.set_xlabel('Zeit')  # Setzt das Label der x-Achse
    gnt.set_ylabel('Prozesse')  # Setzt das Label der y-Achse

    for prozess in prozesse:  # Iteriert über alle Prozesse
        # Erstellt eine Zeitbalken (Broken Bar) für jeden Prozess
        gnt.broken_barh([(prozess['start'], prozess['dauer'])], (prozess['reihe'], 9), facecolors=('tab:blue'))

    plt.savefig(dateiname)  # Speichert das Diagramm als Bilddatei

# Funktion zum Speichern der Ergebnisse basierend auf dem Ausgabeformat
def speichere_ergebnisse(args, ergebnisse, logs):
    if args.ausgabeformat == 'text':  # Überprüft, ob das Ausgabeformat Text ist
        schreibe_ergebnisse_text(args.ausgabedatei, ergebnisse)  # Ruft die Funktion zum Schreiben der Textdatei auf
    elif args.ausgabeformat == 'grafisch':  # Überprüft, ob das Ausgabeformat grafisch ist
        erstelle_gantt_chart(args.ausgabedatei, ergebnisse)  # Ruft die Funktion zum Erstellen des Gantt-Diagramms auf
    
    schreibe_log(args.logdatei, logs)  # Ruft die Funktion zum Schreiben der Logdatei auf

# Hauptfunktion zum Ausführen des Skripts
#if __name__ == "__main__":
#    args = parse_arguments()  # Aufruf der Funktion zum Parsen der Argumente

    # Beispiel-Ergebnisse und Logs für die Demonstration
  #  ergebnisse = [
  #      "Prozess P1: Laufzeit 5, Wartezeit 0",
  #      "Prozess P2: Laufzeit 3, Wartezeit 4"
 #   ]
  #  logs = [
  #      "Zeit 0: Prozess P1 gestartet",
  #      "Zeit 5: Prozess P1 gestoppt, Prozess P2 gestartet"
   # ]

    # Beispiel-Daten für die Prozesse (nur für das Gantt-Diagramm)
    #prozesse = [
   #     {'name': 'P1', 'start': 0, 'dauer': 5, 'reihe': 10},
    #    {'name': 'P2', 'start': 5, 'dauer': 3, 'reihe': 20}
   # ]

    speichere_ergebnisse(args, ergebnisse, logs)  # Aufruf der Funktion zum Speichern der Ergebnisse und Logs


    
