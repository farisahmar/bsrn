# Importe = Erweiterung der Programmiermöglichkeiten
import argparse # Parsen von Kommandozeilenargumente
import json #Ergebnisse im JSON-Format speichern, falls notwendig/gewollt
import matplotlib.pyplot as plt #Grafische Ausgaben, falls notwendig

#Definieren der Argumente für die Ausgabedatei, als auch Logdatei
#Funktion zum Parsen der Kommandozeilenargumente
#Parsen = Analyse der Eingabedateien und diese in eine strukturierte Form zu bringen. Die das Programm verarbeiten kann
def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulator für das Multilevel-Feedback-Scheduling')
    parser.add_argument('-outputformat', type=str, choices=['text', 'grafisch'], required=True, help='Ausgabeformat')
    parser.add_argument('-outputfile', type=str, required=True, help='Datei für die Ausgabe')
    parser.add_argument('-logfile', type=str, required=True, help='Datei für Logdaten')
    return parser.parse_args()

args = parse_arguments() #ist Aufruf der Funktion zum Parsen der Argumente

#Funktion zum Schreiben der Logdatei
#def schreibe_log(dateiname, logs):
   # with open(dateiname, 'w') as file:
        for line in result: 
            file.write(line + '\n')

#Funktion zum Schreiben von Ergebnissen in eine Textdatei
def write_result_text(filename, result):
    with open(dateiname, 'w') as file:
        for line in result:
            file.write(line + '\n')

# Funktion zum Erstellen eines Gantt-Diagramms und Speichern als Bilddatei
def create_gantt_chart(filename, process):
    fig, gnt = plt.subplots()  # Erstellt eine neue Figur und ein Achsenobjekt
    gnt.set_xlabel('Time')  # Setzt das Label der x-Achse
    gnt.set_ylabel('Processes')  # Setzt das Label der y-Achse

    for process in processes:  # Iteriert über alle Prozesse
        # Erstellt eine Zeitbalken (Broken Bar) für jeden Prozess
        #time = dauer
        gnt.broken_barh([(process['start'], process['time'])], (process['row'], 9), facecolors=('tab:blue'))

    plt.savefig(filename)  # Speichert das Diagramm als Bilddatei

# Funktion zum Speichern der Ergebnisse basierend auf dem Ausgabeformat
def save_result(args, result, logs):
    if args.outputformat == 'text':  # Überprüft, ob das Ausgabeformat Text ist
        write_result_text(args.outputfile, result)  # Ruft die Funktion zum Schreiben der Textdatei auf
    elif args.outputformat == 'grafisch':  # Überprüft, ob das Ausgabeformat grafisch ist
        create_gantt_chart(args.outputfile, result)  # Ruft die Funktion zum Erstellen des Gantt-Diagramms auf
    
    write_log(args.logfile, logs)  # Ruft die Funktion zum Schreiben der Logdatei auf

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

    save_result(args, result, logs)  # Aufruf der Funktion zum Speichern der Ergebnisse und Logs


    
