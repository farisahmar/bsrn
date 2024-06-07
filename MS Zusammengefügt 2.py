class Process:
    # Initialisiert ein Prozess-Objekt mit Name, Laufzeit, Ankunftszeit und anderen Attributen
    def __init__(self, name, burst_time, arrival_time):
        self.name = name  # Name des Prozesses
        self.burst_time = burst_time  # Gesamtlaufzeit des Prozesses
        self.remaining_time = burst_time  # Verbleibende Laufzeit des Prozesses, initial gleich der Gesamtlaufzeit
        self.arrival_time = arrival_time  # Ankunftszeit des Prozesses
        self.waiting_time = 0  # Wartezeit des Prozesses, initial 0
        self.turnaround_time = 0  # Gesamtlaufzeit bis zum Abschluss des Prozesses, initial 0

def get_quantum_for_queues(warteschlangen_gesamt):
    # Fragt den Benutzer nach dem Quantum für jede Warteschlange und gibt eine Liste von Quantum-Werten zurück
    quantum = []  # Liste, um die Quantum-Werte zu speichern
    for number in range(1, warteschlangen_gesamt + 1):
        while True:
            try:
                # Fragt den Benutzer nach dem Quantum für die aktuelle Warteschlange
                quantum_value = int(input(f"Gib den Quantum der {number}. Warteschlange an: "))
                if quantum_value <= 0:
                    # Überprüft, ob der Quantum-Wert positiv ist
                    raise ValueError("Quantum muss eine positive Zahl sein.")
                # Fügt den gültigen Quantum-Wert zur Liste hinzu
                quantum.append(quantum_value)
                break  # Bricht die Schleife ab, wenn ein gültiger Wert eingegeben wurde
            except ValueError as e:
                # Gibt eine Fehlermeldung aus und fordert zur erneuten Eingabe auf
                print(f"Ungültige Eingabe: {e}. Bitte versuchen Sie es erneut.")
    return quantum  # Gibt die Liste der Quantum-Werte zurück

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

def erstelle_warteschlangen(warteschlangen_gesamt):
    # Erstellt eine Liste von leeren Listen für die angegebenen Anzahl von Warteschlangen
    return [[] for _ in range(warteschlangen_gesamt)]  # Erstellt eine leere Liste für jede Warteschlange

def prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse, log_file):
    # Fügt Prozesse, die angekommen sind, zur ersten Warteschlange hinzu
    for prozess in prozesse:
        if aktuelle_zeit >= prozess.arrival_time and prozess not in hinzugefuegte_prozesse:
            # Überprüft, ob der Prozess angekommen ist und noch nicht hinzugefügt wurde
            log_file.write(f"{aktuelle_zeit}ms: Prozess {prozess.name} ist angekommen und in Warteschlange 1 eingereiht.\n")
            warteschlangen[0].append(prozess)  # Fügt den Prozess zur ersten Warteschlange hinzu
            hinzugefuegte_prozesse.append(prozess)  # Fügt den Prozess zur Liste der hinzugefügten Prozesse hinzu

def round_robin_scheduling(warteschlangen, quantum, prozesse, hinzugefuegte_prozesse, log_file):
    # Implementiert das Round-Robin-Scheduling-Verfahren
    aktuelle_zeit = 0  # Initialisiert die aktuelle Zeit
    gesamtlaufzeit = sum(prozess.burst_time for prozess in prozesse)  # Berechnet die Gesamtlaufzeit aller Prozesse

    gantt_chart = []  # Liste, um das Gantt-Diagramm zu speichern

    while any(warteschlange for warteschlange in warteschlangen) or aktuelle_zeit < gesamtlaufzeit:
        # Hauptschleife, die läuft, solange noch Prozesse in den Warteschlangen sind oder die aktuelle Zeit kleiner als die Gesamtlaufzeit ist
        prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse, log_file)

        prozess_gelaufen = False  # Flag, um zu überprüfen, ob ein Prozess in diesem Durchlauf ausgeführt wurde

        for i, warteschlange in enumerate(warteschlangen):
            if warteschlange:
                # Wenn die Warteschlange nicht leer ist, wird der erste Prozess entnommen
                current_quantum = quantum[i]  # Holt den Quantum-Wert für die aktuelle Warteschlange
                prozess = warteschlange.pop(0)  # Entfernt den ersten Prozess aus der Warteschlange

                for _ in range(current_quantum):
                    if prozess.remaining_time > 0:
                        # Führt den Prozess für einen Zeitschritt aus
                        prozess.remaining_time -= 1  # Verringert die verbleibende Laufzeit des Prozesses
                        aktuelle_zeit += 1  # Erhöht die aktuelle Zeit um 1
                        gantt_chart.append((aktuelle_zeit, prozess.name))  # Fügt die aktuelle Zeit und den Prozessnamen zum Gantt-Diagramm hinzu
                        log_file.write(f"{aktuelle_zeit}ms: Prozess {prozess.name} läuft für 1ms (Restlaufzeit: {prozess.remaining_time}ms)\n")
                        prozess_gelaufen = True  # Setzt das Flag, dass ein Prozess gelaufen ist
                        if aktuelle_zeit >= gesamtlaufzeit:
                            break  # Bricht die Schleife ab, wenn die Gesamtlaufzeit erreicht ist

                if prozess.remaining_time > 0:
                    # Wenn der Prozess nicht abgeschlossen ist, wird er in die nächste Warteschlange verschoben
                    if i < len(warteschlangen) - 1:
                        warteschlangen[i + 1].append(prozess)  # Verschiebt den Prozess in die nächste Warteschlange
                        log_file.write(f"     Prozess {prozess.name} ist in Warteschlange {i + 2} verschoben worden\n")
                    else:
                        warteschlangen[i].append(prozess)  # Bleibt in der letzten Warteschlange, wenn es keine weitere gibt
                        log_file.write(f"     Prozess {prozess.name} bleibt in der letzten Warteschlange\n")
                else:
                    # Wenn der Prozess abgeschlossen ist, werden die Gesamt- und Wartezeit berechnet
                    prozess.turnaround_time = aktuelle_zeit - prozess.arrival_time  # Berechnet die Gesamtlaufzeit bis zum Abschluss
                    prozess.waiting_time = prozess.turnaround_time - prozess.burst_time  # Berechnet die Wartezeit des Prozesses
                    log_file.write(f"     Prozess {prozess.name} wurde abgeschlossen\n")

                break  # Bricht die Schleife ab, da ein Prozess bearbeitet wurde

        if not prozess_gelaufen:
            # Wenn kein Prozess in diesem Durchlauf bearbeitet wurde, erhöht die aktuelle Zeit um 1
            aktuelle_zeit += 1

    return gantt_chart  # Gibt das Gantt-Diagramm zurück

def schreibe_gantt_diagramm(gantt_chart, prozesse, gantt_file):
    # Schreibt das Gantt-Diagramm und die Zeiten in die Datei
    gantt_file.write("Gantt Chart:\n")
    gantt_file.write("Zeit/Prozess\n")
    for zeit, name in gantt_chart:
        # Schreibt jede Zeiteinheit und den zugehörigen Prozessnamen in die Datei
        gantt_file.write(f"{'_____' * (zeit - 1)}{zeit}/{name}\n")

    total_waiting_time = sum(prozess.waiting_time for prozess in prozesse)  # Berechnet die gesamte Wartezeit aller Prozesse
    total_turnaround_time = sum(prozess.turnaround_time for prozess in prozesse)
    avg_waiting_time = total_waiting_time / len(prozesse)
    avg_turnaround_time = total_turnaround_time / len(prozesse)

    gantt_file.write("\nLaufzeiten und Wartezeiten der Prozesse:\n")
    for prozess in prozesse:
        gantt_file.write(f"Name: {prozess.name}, Laufzeit: {prozess.burst_time}, Wartezeit: {prozess.waiting_time}, Gesamtlaufzeit: {prozess.turnaround_time}\n")

    gantt_file.write(f"\nDurchschnittliche Wartezeit: {avg_waiting_time}\n")
    gantt_file.write(f"Durchschnittliche Gesamtlaufzeit: {avg_turnaround_time}\n")

if __name__ == "__main__":
    try:
        warteschlangen_gesamt = int(input("Gib die Anzahl der Warteschlangen an: "))
        if warteschlangen_gesamt <= 0:
            raise ValueError("Die Anzahl der Warteschlangen muss eine positive Zahl sein.")

        quantum = get_quantum_for_queues(warteschlangen_gesamt)

        file_path = input("Geben Sie den Pfad der Eingabedatei an: ")
        processes = read_processes_from_file(file_path)

        log_file_path = input("Geben Sie den Pfad für die Log-Datei an: ")
        gantt_file_path = input("Geben Sie den Pfad für die Gantt-Diagramm Datei an: ")
        with open(log_file_path, 'w') as log_file, open(gantt_file_path, 'w') as gantt_file:
            log_file.write("Processes:\n")
            for process in processes:
                log_file.write(f"Name: {process.name}, Laufzeit: {process.burst_time}, Ankunftszeit: {process.arrival_time}\n")

            hinzugefuegte_prozesse = []
            warteschlangen = erstelle_warteschlangen(warteschlangen_gesamt)
            gantt_chart = round_robin_scheduling(warteschlangen, quantum, processes, hinzugefuegte_prozesse, log_file)

            schreibe_gantt_diagramm(gantt_chart, processes, gantt_file)

    except ValueError as e:
        print(f"Ungültige Eingabe: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
