warteschlangen_gesamt = int(input("Gib die Anzahl der Warteschlangen an: "))  # Anzahl der Warteschlangen vom Benutzer abfragen
quantum = []

# Quantum pro Warteschlange generieren
def get_quantum_for_queues(warteschlangen_gesamt):
    quantum = []
    for number in range(1, warteschlangen_gesamt + 1):
        quantum_value = int(input("Gib den Quantum der " + str(number) + ". Warteschlange an: "))  # Quantum für jede Warteschlange abfragen
        quantum.append(quantum_value)  # Quantum-Wert zur Liste hinzufügen
    return quantum

# Quantum für jede Warteschlange abfragen und speichern
quantum = get_quantum_for_queues(warteschlangen_gesamt)

# Warteschlangen generieren, je nachdem wie viele Warteschlangen es insgesamt gibt
def erstelle_warteschlangen(warteschlangen_gesamt):
    warteschlangen = []
    for i in range(1, warteschlangen_gesamt + 1):
        warteschlange = []  # Leeres Array für jede Warteschlange erstellen
        warteschlangen.append(warteschlange)  # Warteschlange zur Liste hinzufügen
    return warteschlangen

# Prozess-Klasse definieren
class Process:
    def __init__(self, name, laufzeit, ankunftszeit):
        self.name = name  # Name des Prozesses
        self.ankunftszeit = ankunftszeit  # Ankunftszeit des Prozesses
        self.laufzeit = laufzeit  # Laufzeit des Prozesses

    def __repr__(self):
        return f"Process(Name: {self.name}, Laufzeit: {self.laufzeit}, Ankunftszeit: {self.ankunftszeit})"

# Prozesse aus einer Datei lesen
def read_processes_from_file(file_path):
    processes = []  # Liste, um die gelesenen Prozesse zu speichern
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()  # Jede Zeile der Datei lesen
            for line in lines:
                parts = line.split()  # Die Zeile in Teile aufteilen
                if len(parts) == 3:
                    name = parts[0]  # Name des Prozesses
                    laufzeit = int(parts[1])  # Laufzeit des Prozesses
                    ankunftszeit = int(parts[2])  # Ankunftszeit des Prozesses
                    processes.append(Process(name, laufzeit, ankunftszeit))  # Prozess zur Liste hinzufügen
    except Exception as e:
        print(f"Error reading the file: {e}")
    return processes  # Die Liste der Prozesse zurückgeben

if __name__ == "__main__":
    file_path = input("Geben Sie den Pfad der Textdatei an: ")  # Pfad der Datei abfragen
    processes = read_processes_from_file(file_path)  # Prozesse aus der Datei lesen
    print("Processes read from file:")
    for process in processes:
        print(process)  # Die gelesenen Prozesse anzeigen

# Prozesse in Warteschlange 1 hinzufügen
def prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse):
    for prozess in prozesse:
        if aktuelle_zeit >= prozess.ankunftszeit and prozess not in hinzugefuegte_prozesse:
            print(f"{aktuelle_zeit}ms: Prozess {prozess.name} ist angekommen und in Warteschlange 1 eingereiht.")
            warteschlangen[0].append(prozess)  # Prozess in Warteschlange 1 einreihen
            hinzugefuegte_prozesse.append(prozess)  # Prozess zur Liste der hinzugefügten Prozesse hinzufügen

# Round Robin Scheduling
def round_robin_scheduling(warteschlangen, quantum, prozesse, hinzugefuegte_prozesse):
    aktuelle_zeit = 0  # Initialisierung der aktuellen Zeit
    gesamtlaufzeit = sum(prozess.laufzeit for prozess in prozesse)  # Gesamtlaufzeit aller Prozesse berechnen

    while any(warteschlange for warteschlange in warteschlangen) or aktuelle_zeit < gesamtlaufzeit:
        # Hauptschleife, die läuft, solange es Prozesse gibt oder die Gesamtlaufzeit nicht erreicht ist
        prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse)

        prozess_gelaufen = False  # Flag um zu überprüfen, ob ein Prozess in dieser Zeiteinheit lief

        for i, warteschlange in enumerate(warteschlangen):
            if warteschlange:
                current_quantum = quantum[i]  # Quantum der aktuellen Warteschlange abrufen
                prozess = warteschlange.pop(0)  # Ersten Prozess aus der Warteschlange holen

                for _ in range(current_quantum):
                    if prozess.laufzeit > 0:
                        prozess.laufzeit -= 1  # Reduzieren der Laufzeit des Prozesses um 1 ms
                        aktuelle_zeit += 1  # Erhöhen der aktuellen Zeit um 1 ms
                        print(f"{aktuelle_zeit}ms: Prozess {prozess.name} läuft für 1ms (Restlaufzeit: {prozess.laufzeit}ms)")
                        prozess_gelaufen = True  # Setze Flag, dass ein Prozess gelaufen ist
                        if aktuelle_zeit >= gesamtlaufzeit:
                            break  # Beende die Schleife, wenn die Gesamtlaufzeit erreicht ist

                if prozess.laufzeit > 0:
                    if i < len(warteschlangen) - 1:
                        warteschlangen[i + 1].append(prozess)  # Prozess in die nächst tiefere Warteschlange verschieben
                        print(f"{aktuelle_zeit}ms: Prozess {prozess.name} ist in Warteschlange {i + 2} verschoben worden")
                    else:
                        warteschlangen[i].append(prozess)  # Prozess bleibt in der letzten Warteschlange
                        print(f"{aktuelle_zeit}ms: Prozess {prozess.name} bleibt in der letzten Warteschlange")
                else:
                    print(f"{aktuelle_zeit}ms: Prozess {prozess.name} wurde abgeschlossen")  # Prozess abgeschlossen

                break  # Beende die innere Schleife, um die aktuelle Zeit zu aktualisieren

        if not prozess_gelaufen:
            aktuelle_zeit += 1  # Erhöhe die aktuelle Zeit, wenn kein Prozess bearbeitet wurde

# Initialisierung der Liste der hinzugefügten Prozesse
hinzugefuegte_prozesse = []

# Initialisierung der Warteschlangen
warteschlangen = erstelle_warteschlangen(warteschlangen_gesamt)

# Round Robin Scheduling ausführen
round_robin_scheduling(warteschlangen, quantum, processes, hinzugefuegte_prozesse)  # Übergabe der Liste `processes`, `warteschlangen`, `hinzugefuegte_prozesse`, und `quantum`
