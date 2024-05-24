warteschlangen_gesamt = int(3)
quantum = []

# Quantum pro Warteschlange generieren
def get_quantum_for_queues(warteschlangen_gesamt):
    quantum = []
    for number in range(1, warteschlangen_gesamt + 1):
        quantum_value = int(input("Gib den Quantum der " + str(number) + ". Warteschlange an: "))
        quantum.append(quantum_value)
    return quantum

quantum = get_quantum_for_queues(warteschlangen_gesamt)

# Warteschlangen generieren, je nachdem wie viel Warteschlangen es insgesamt gibt
def erstelle_warteschlangen(warteschlangen_gesamt):
    warteschlangen = []
    for i in range(1, warteschlangen_gesamt + 1):
        warteschlange = []  # Leeres Array für jede Warteschlange erstellen
        warteschlangen.append(warteschlange)
    return warteschlangen

# Prozess-Klasse definieren
class Prozess:
    def __init__(self, name, laufzeit, ankunftszeit):
        self.name = name
        self.laufzeit = laufzeit
        self.ankunftszeit = ankunftszeit

# Prozesse in Warteschlange 1 hinzufügen
def prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen):
    for prozess in prozesse:
        if aktuelle_zeit == prozess.ankunftszeit:
            print(f"{aktuelle_zeit}ms: Prozess {prozess.name} ist angekommen und in Warteschlange 1 eingereiht.")
            warteschlangen[0].append(prozess)

# Round Robin Scheduling
def round_robin_scheduling(warteschlangen, quantum, prozesse):
    aktuelle_zeit = 0
    gesamtlaufzeit = sum(prozess.laufzeit for prozess in prozesse)


    while aktuelle_zeit < gesamtlaufzeit:
        prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen)
        aktuelle_zeit += 1

        for i, warteschlange in enumerate(warteschlangen):
            if warteschlange:
                current_quantum = quantum[i]
                prozess = warteschlange.pop(0)
                laufzeit_vorher = prozess.laufzeit
                for j in range(current_quantum):
                    prozess.laufzeit -= 1
                gelaufene_zeit = min(current_quantum, laufzeit_vorher)

                if prozess.laufzeit > 0:
                    if i < len(warteschlangen) - 1:
                        warteschlangen[i + 1].append(prozess)
                        print(f"{aktuelle_zeit}ms: Prozess {prozess.name} läuft für {gelaufene_zeit}ms (Restlaufzeit: {prozess.laufzeit}ms)")
                        print(f"{aktuelle_zeit}ms: Prozess {prozess.name} ist in Warteschlange {i + 2} verschoben worden")
                    else:
                        warteschlangen[i].append(prozess)
                        print(f"{aktuelle_zeit}ms: Prozess {prozess.name} läuft für {gelaufene_zeit}ms (Restlaufzeit: {prozess.laufzeit}ms)")
                        print(f"{aktuelle_zeit}ms: Prozess {prozess.name} bleibt in der letzten Warteschlange")
                else:
                    print(f"{aktuelle_zeit}ms: Prozess {prozess.name} läuft für {gelaufene_zeit}ms (Restlaufzeit: 0ms)")
                    print(f"{aktuelle_zeit}ms: Prozess {prozess.name} wurde abgeschlossen")


                break  # Beende die innere Schleife, um die aktuelle Zeit zu aktualisieren
        else:
            aktuelle_zeit += 1  # Erhöhe die aktuelle Zeit, wenn keine Prozesse bearbeitet wurden

# Initialisierung
warteschlangen = erstelle_warteschlangen(warteschlangen_gesamt)

# Prozessbeispiele erstellen
prozesse = [
    Prozess("A", 8, 0),
    Prozess("B", 4, 1),
    Prozess("C", 13, 5)
]

# Round Robin Scheduling ausführen
round_robin_scheduling(warteschlangen, quantum, prozesse)
