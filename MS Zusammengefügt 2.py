class Process:
    def __init__(self, name, burst_time, arrival_time):
        self.name = name
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.arrival_time = arrival_time
        self.waiting_time = 0
        self.turnaround_time = 0

def get_quantum_for_queues(warteschlangen_gesamt):
    quantum = []
    for number in range(1, warteschlangen_gesamt + 1):
        while True:
            try:
                quantum_value = int(input(f"Gib den Quantum der {number}. Warteschlange an: "))
                if quantum_value <= 0:
                    raise ValueError("Quantum muss eine positive Zahl sein.")
                quantum.append(quantum_value)
                break
            except ValueError as e:
                print(f"Ungültige Eingabe: {e}. Bitte versuchen Sie es erneut.")
    return quantum

def read_processes_from_file(file_path):
    processes = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.split()
                if len(parts) == 3:
                    name = parts[0]
                    try:
                        burst_time = int(parts[1])
                        arrival_time = int(parts[2])
                        processes.append(Process(name, burst_time, arrival_time))
                    except ValueError as e:
                        print(f"Fehler beim Lesen der Prozessdaten: {e}")
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
    return processes

def erstelle_warteschlangen(warteschlangen_gesamt):
    return [[] for _ in range(warteschlangen_gesamt)]

def prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse, log_file):
    for prozess in prozesse:
        if aktuelle_zeit >= prozess.arrival_time and prozess not in hinzugefuegte_prozesse:
            log_file.write(f"{aktuelle_zeit}ms: Prozess {prozess.name} ist angekommen und in Warteschlange 1 eingereiht.\n")
            warteschlangen[0].append(prozess)
            hinzugefuegte_prozesse.append(prozess)

def round_robin_scheduling(warteschlangen, quantum, prozesse, hinzugefuegte_prozesse, log_file):
    aktuelle_zeit = 0
    gesamtlaufzeit = sum(prozess.burst_time for prozess in prozesse)

    gantt_chart = []

    while any(warteschlange for warteschlange in warteschlangen) or aktuelle_zeit < gesamtlaufzeit:
        prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse, log_file)

        prozess_gelaufen = False

        for i, warteschlange in enumerate(warteschlangen):
            if warteschlange:
                current_quantum = quantum[i]
                prozess = warteschlange.pop(0)

                for _ in range(current_quantum):
                    if prozess.remaining_time > 0:
                        prozess.remaining_time -= 1
                        aktuelle_zeit += 1
                        gantt_chart.append((aktuelle_zeit, prozess.name))
                        log_file.write(f"{aktuelle_zeit}ms: Prozess {prozess.name} läuft für 1ms (Restlaufzeit: {prozess.remaining_time}ms)\n")
                        prozess_gelaufen = True
                        if aktuelle_zeit >= gesamtlaufzeit:
                            break

                if prozess.remaining_time > 0:
                    if i < len(warteschlangen) - 1:
                        warteschlangen[i + 1].append(prozess)
                        log_file.write(f"     Prozess {prozess.name} ist in Warteschlange {i + 2} verschoben worden\n")
                    else:
                        warteschlangen[i].append(prozess)
                        log_file.write(f"     Prozess {prozess.name} bleibt in der letzten Warteschlange\n")
                else:
                    prozess.turnaround_time = aktuelle_zeit - prozess.arrival_time
                    prozess.waiting_time = prozess.turnaround_time - prozess.burst_time
                    log_file.write(f"     Prozess {prozess.name} wurde abgeschlossen\n")

                break

        if not prozess_gelaufen:
            aktuelle_zeit += 1

    return gantt_chart

def schreibe_gantt_diagramm(gantt_chart, prozesse, gantt_file):
    gantt_file.write("Gantt Chart:\n")
    gantt_file.write("Zeit/Prozess\n")
    for zeit, name in gantt_chart:
        gantt_file.write(f"{'_____' * (zeit - 1)}{zeit}/{name}\n")

    total_waiting_time = sum(prozess.waiting_time for prozess in prozesse)
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
