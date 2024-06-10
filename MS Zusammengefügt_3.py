import argparse  # Importiert das argparse-Modul zur Verarbeitung von Kommandozeilenargumenten
import sys       # Importiert das sys-Modul, um auf Systemfunktionen zuzugreifen

class Process:
    # Initialisiert ein Prozess-Objekt mit Name, Laufzeit, Ankunftszeit und anderen Attributen
    def __init__(self, name, burst_time, arrival_time):
        self.name = name  # Name des Prozesses
        self.burst_time = burst_time  # Gesamtlaufzeit des Prozesses
        self.remaining_time = burst_time  # Verbleibende Laufzeit des Prozesses, initial gleich der Gesamtlaufzeit
        self.arrival_time = arrival_time  # Ankunftszeit des Prozesses
        self.waiting_time = 0  # Wartezeit des Prozesses, initial 0
        self.turnaround_time = 0  # Gesamtlaufzeit bis zum Abschluss des Prozesses, initial 0

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

def read_processes_from_file(file_path):
    # Liest die Prozessdaten aus einer Datei und gibt eine Liste von Prozess-Objekten zurück
    processes = []  # Liste, um die Prozesse zu speichern
    try:
        # Öffnet die Datei im Lesemodus
        with open(file_path, 'r') as file:
            lines = file.readlines()  # Liest alle Zeilen der Datei
            for line in lines:
                parts = line.split()  # Teilt jede Zeile in Teile auf, die durch Leerzeichen getrennt sind
                if len(parts) == 3:
                    # Überprüft, ob die Zeile genau drei Teile enthält
                    name = parts[0]  # Der erste Teil ist der Name des Prozesses
                    try:
                        burst_time = int(parts[1])  # Der zweite Teil ist die Gesamtlaufzeit des Prozesses
                        arrival_time = int(parts[2])  # Der dritte Teil ist die Ankunftszeit des Prozesses
                        # Erstellt einen neuen Prozess und fügt ihn der Liste hinzu
                        processes.append(Process(name, burst_time, arrival_time))
                    except ValueError as e:
                        # Gibt eine Fehlermeldung aus, wenn die Umwandlung in Integer fehlschlägt
                        print(f"Fehler beim Lesen der Prozessdaten: {e}")
    except Exception as e:
        # Gibt eine Fehlermeldung aus, wenn die Datei nicht gelesen werden kann
        print(f"Fehler beim Lesen der Datei: {e}")
    return processes  # Gibt die Liste der Prozesse zurück

def create_queues(num_queues):
    # Erstellt eine Liste von leeren Listen für die angegebenen Anzahl von Warteschlangen
    return [[] for _ in range(num_queues)]  # Erstellt eine leere Liste für jede Warteschlange

def add_processes_to_queue(current_time, processes, queues, added_processes, log_file):
    # Fügt Prozesse, die angekommen sind, zur ersten Warteschlange hinzu
    for process in processes:
        if current_time >= process.arrival_time and process not in added_processes:
            # Überprüft, ob der Prozess angekommen ist und noch nicht hinzugefügt wurde
            log_file.write(f"{current_time}ms: Process {process.name} arrived and added to queue 1.\n")
            queues[0].append(process)  # Fügt den Prozess zur ersten Warteschlange hinzu
            added_processes.append(process)  # Fügt den Prozess zur Liste der hinzugefügten Prozesse hinzu

def round_robin_scheduling(queues, quantum, processes, added_processes, log_file):
    # Implementiert das Round-Robin-Scheduling-Verfahren
    current_time = 0  # Initialisiert die aktuelle Zeit
    total_burst_time = sum(process.burst_time for process in processes)  # Berechnet die Gesamtlaufzeit aller Prozesse

    gantt_chart = []  # Liste, um das Gantt-Diagramm zu speichern

    while any(queue for queue in queues) or current_time < total_burst_time:
        # Hauptschleife, die läuft, solange noch Prozesse in den Warteschlangen sind oder die aktuelle Zeit kleiner als die Gesamtlaufzeit ist
        add_processes_to_queue(current_time, processes, queues, added_processes, log_file)

        process_executed = False  # Flag, um zu überprüfen, ob ein Prozess in diesem Durchlauf ausgeführt wurde

        for i, queue in enumerate(queues):
            if queue:
                # Wenn die Warteschlange nicht leer ist, wird der erste Prozess entnommen
                current_quantum = quantum[i]  # Holt den Quantum-Wert für die aktuelle Warteschlange
                process = queue.pop(0)  # Entfernt den ersten Prozess aus der Warteschlange

                for _ in range(current_quantum):
                    if process.remaining_time > 0:
                        # Führt den Prozess für einen Zeitschritt aus
                        process.remaining_time -= 1  # Verringert die verbleibende Laufzeit des Prozesses
                        current_time += 1  # Erhöht die aktuelle Zeit um 1
                        gantt_chart.append((current_time, process.name))  # Fügt die aktuelle Zeit und den Prozessnamen zum Gantt-Diagramm hinzu
                        log_file.write(f"{current_time}ms: Process {process.name} running for 1ms (remaining time: {process.remaining_time}ms)\n")
                        process_executed = True  # Setzt das Flag, dass ein Prozess gelaufen ist
                        if current_time >= total_burst_time:
                            break  # Bricht die Schleife ab, wenn die Gesamtlaufzeit erreicht ist

                if process.remaining_time > 0:
                    # Wenn der Prozess nicht abgeschlossen ist, wird er in die nächste Warteschlange verschoben
                    if i < len(queues) - 1:
                        queues[i + 1].append(process)  # Verschiebt den Prozess in die nächste Warteschlange
                        log_file.write(f"     Process {process.name} moved to queue {i + 2}\n")
                    else:
                        queues[i].append(process)  # Bleibt in der letzten Warteschlange, wenn es keine weitere gibt
                        log_file.write(f"     Process {process.name} remains in the last queue\n")
                else:
                    # Wenn der Prozess abgeschlossen ist, werden die Gesamt- und Wartezeit berechnet
                    process.turnaround_time = current_time - process.arrival_time  # Berechnet die Gesamtlaufzeit bis zum Abschluss
                    process.waiting_time = process.turnaround_time - process.burst_time  # Berechnet die Wartezeit des Prozesses
                    log_file.write(f"     Process {process.name} completed\n")

                break  # Bricht die Schleife ab, da ein Prozess bearbeitet wurde

        if not process_executed:
            # Wenn kein Prozess in diesem Durchlauf bearbeitet wurde, erhöht die aktuelle Zeit um 1
            current_time += 1

    return gantt_chart  # Gibt das Gantt-Diagramm zurück

def write_gantt_chart(gantt_chart, processes, gantt_file):
    # Schreibt das Gantt-Diagramm und die Zeiten in die Datei
    gantt_file.write("Gantt Chart:\n")
    gantt_file.write("Time/Process\n")
    for time, name in gantt_chart:
        # Schreibt jede Zeiteinheit und den zugehörigen Prozessnamen in die Datei
        gantt_file.write(f"{'_____' * (time - 1)}{time}/{name}\n")

    total_waiting_time = sum(process.waiting_time for process in processes)  # Berechnet die gesamte Wartezeit aller Prozesse
    total_turnaround_time = sum(process.turnaround_time for process in processes)
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)

    gantt_file.write("\nProcess execution times and waiting times:\n")
    for process in processes:
        gantt_file.write(f"Name: {process.name}, Burst Time: {process.burst_time}, Waiting Time: {process.waiting_time}, Turnaround Time: {process.turnaround_time}\n")

    gantt_file.write(f"\nAverage Waiting Time: {avg_waiting_time}\n")
    gantt_file.write(f"Average Turnaround Time: {avg_turnaround_time}\n")

if __name__ == "__main__":
    args = parse_arguments()

    try:
        if args.queues <= 0:
            raise ValueError("The number of queues must be a positive number.")

        quantum = args.quantum

        processes = read_processes_from_file(args.processlistfile)

        with open(args.logfile, 'w') as log_file, open(args.outputfile, 'w') as gantt_file:
            log_file.write("Processes:\n")
            for process in processes:
                log_file.write(f"Name: {process.name}, Burst Time: {process.burst_time}, Arrival Time: {process.arrival_time}\n")

            added_processes = []
            queues = create_queues(args.queues)
            gantt_chart = round_robin_scheduling(queues, quantum, processes, added_processes, log_file)

            write_gantt_chart(gantt_chart, processes, gantt_file)

    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
