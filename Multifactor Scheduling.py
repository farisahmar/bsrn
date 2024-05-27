warteschlangen_gesamt = int(input("gib die anzahl der Warteschlangen an: "))
quantum = []


# Quantum pro Warteschlange generieren
def get_quantum_for_queues(warteschlangen_gesamt):
    quantum = []
    for number in range(1, warteschlangen_gesamt + 1):
        quantum_value = int(input("Gib den Quantum der " + str(number) + ". Warteschlange an: "))
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
class Prozess:
    def __init__(self, name, laufzeit, ankunftszeit):
        self.name = name  # Name des Prozesses
        self.laufzeit = laufzeit  # Laufzeit des Prozesses
        self.ankunftszeit = ankunftszeit  # Ankunftszeit des Prozesses


# Prozesse in Warteschlange 1 hinzufügen
def prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse):
    for prozess in prozesse:
        if prozess not in hinzugefuegte_prozesse and aktuelle_zeit >= prozess.ankunftszeit:
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
        # Prozesse der aktuellen Zeit zur ersten Warteschlange hinzufügen

        prozess_gelaufen = False  # Flag um zu überprüfen, ob ein Prozess in dieser Zeiteinheit lief

        for i, warteschlange in enumerate(warteschlangen):
            if warteschlange:
                current_quantum = quantum[i]  # Quantum der aktuellen Warteschlange abrufen
                prozess = warteschlange.pop(0)  # Ersten Prozess aus der Warteschlange holen

                for _ in range(current_quantum):
                    if prozess.laufzeit > 0:
                        prozess.laufzeit -= 1  # Reduzieren der Laufzeit des Prozesses um 1 ms
                        aktuelle_zeit += 1  # Erhöhen der aktuellen Zeit um 1 ms
                        print(
                            f"{aktuelle_zeit}ms: Prozess {prozess.name} läuft für 1ms (Restlaufzeit: {prozess.laufzeit}ms)")
                        prozess_gelaufen = True  # Setze Flag, dass ein Prozess gelaufen ist
                        if aktuelle_zeit >= gesamtlaufzeit:
                            break  # Beende die Schleife, wenn die Gesamtlaufzeit erreicht ist

                if prozess.laufzeit > 0:
                    if i < len(warteschlangen) - 1:
                        warteschlangen[i + 1].append(prozess)  # Prozess in die nächst tiefere Warteschlange verschieben
                        print(
                            f"{aktuelle_zeit}ms: Prozess {prozess.name} ist in Warteschlange {i + 2} verschoben worden")
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

# Beispielprozesse erstellen
prozesse = [
    Prozess("A", 8, 0),
    Prozess("B", 4, 1),
    Prozess("C", 13, 5)
]

# Round Robin Scheduling ausführen
round_robin_scheduling(warteschlangen, quantum, prozesse, hinzugefuegte_prozesse)
