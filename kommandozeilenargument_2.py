import argparse  # Importiert das argparse-Modul zur Verarbeitung von Kommandozeilenargumenten
import sys       # Importiert das sys-Modul, um auf Systemfunktionen zuzugreifen

def parse_arguments():
    # Erstellt einen ArgumentParser zum Parsen von Kommandozeilenargumenten
    parser = argparse.ArgumentParser(description='Simulator for Multilevel Feedback Scheduling')
    
    # Fügt ein Argument für die Anzahl der Warteschlangen hinzu (erforderlich)
    parser.add_argument('-queues', type=int, required=True, help='Number of queues')
    
    # Fügt ein Argument für die Zeitquanten jeder Warteschlange hinzu (erforderlich, Liste von Ganzzahlen)
    parser.add_argument('-quantum', type=int, nargs='+', required=True, help='Time quantum for each queue')
    
    # Fügt ein Argument für den Pfad zur Eingabedatei mit der Prozessliste hinzu (erforderlich)
    parser.add_argument('-processlistfile', type=str, required=True, help='Path to the input file with the process list')
    
    # Fügt ein Argument für den Pfad zur Logdatei hinzu (erforderlich)
    parser.add_argument('-logfile', type=str, required=True, help='Path to the log file')
    
    # Fügt ein Argument für das Ausgabeformat hinzu (erforderlich, entweder 'text' oder 'grafisch')
    parser.add_argument('-outputformat', type=str, choices=['text', 'graphic'], required=True, help='Output format: text or graphic')
    
    # Fügt ein Argument für den Pfad zur Ausgabedatei hinzu (erforderlich)
    parser.add_argument('-outputfile', type=str, required=True, help='Path to the output file')

    # Parst die übergebenen Argumente
    args = parser.parse_args()

    # Überprüft, ob die Anzahl der Zeitquanten der Anzahl der Warteschlangen entspricht
    if len(args.quantum) != args.queues:
        # Gibt eine Fehlermeldung aus und beendet das Programm, falls die Anzahl nicht übereinstimmt
        print("The number of time quanta must match the number of queues.")
        sys.exit(1)
    
    # Gibt die geparsten Argumente zurück
    return args

def main():
    # Ruft die Funktion auf, die die Kommandozeilenargumente parst
    args = parse_arguments()
    
    # Hier würde die Implementierung des Simulators folgen. Diese Zeilen drucken die geparsten Argumente.
    print(f'Number of queues: {args.queues}')
    print(f'Time quanta: {args.quantum}')
    print(f'Input file: {args.processlistfile}')
    print(f'Log file: {args.logfile}')
    print(f'Output format: {args.outputformat}')
    print(f'Output file: {args.outputfile}')
    
    # Weiterer Code zur Verarbeitung und Simulation würde hier folgen

# Stellt sicher, dass die main-Funktion nur aufgerufen wird, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    main()
