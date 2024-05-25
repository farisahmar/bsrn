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
def prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse):
    for prozess in prozesse:
        # Überprüfen, ob der Prozess an der aktuellen Zeit ankommt und noch nicht hinzugefügt wurde
        if aktuelle_zeit >= prozess.ankunftszeit and prozess not in hinzugefuegte_prozesse:
            print(f"{aktuelle_zeit}ms: Prozess {prozess.name} ist angekommen und in Warteschlange 1 eingereiht.")
            # Prozess in Warteschlange 1 einreihen
            warteschlangen[0].append(prozess)
            # Prozess zur Liste der hinzugefügten Prozesse hinzufügen
            hinzugefuegte_prozesse.append(prozess)

# Round Robin Scheduling
def round_robin_scheduling(warteschlangen, quantum, prozesse, hinzugefuegte_prozesse):
    aktuelle_zeit = 0
    # Gesamtlaufzeit aller Prozesse berechnen
    gesamtlaufzeit = sum(prozess.laufzeit for prozess in prozesse)

    # Hauptschleife, die läuft, solange es Prozesse gibt
    while aktuelle_zeit < gesamtlaufzeit:
        # Prozesse der aktuellen Zeit zur ersten Warteschlange hinzufügen
        prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse)

        # Schleife durch alle Warteschlangen
        for i, warteschlange in enumerate(warteschlangen):
            # Wenn die Warteschlange nicht leer ist
            if warteschlange:
                # Quantum der aktuellen Warteschlange abrufen
                current_quantum = quantum[i]
                # Ersten Prozess aus der Warteschlange holen
                prozess = warteschlange.pop(0)
                laufzeit_vorher = prozess.laufzeit

                # Reduzieren der Laufzeit des Prozesses um das Quantum
                for j in range(current_quantum):
                    if prozess.laufzeit > 0:
                        prozess.laufzeit -= 1
                        # Ausgabe jeder Millisekunde
                        print(f"{aktuelle_zeit}ms: Prozess {prozess.name} läuft für 1ms (Restlaufzeit: {prozess.laufzeit}ms)")
                        aktuelle_zeit += 1

                # Gelaufene Zeit berechnen
                gelaufene_zeit = min(current_quantum, laufzeit_vorher)

                # Wenn der Prozess noch Laufzeit hat
                if prozess.laufzeit > 0:
                    # Wenn es eine tiefere Warteschlange gibt
                    if i < len(warteschlangen) - 1:
                        # Prozess in die nächst tiefere Warteschlange verschieben
                        warteschlangen[i + 1].append(prozess)
                        print(f"{aktuelle_zeit}ms: Prozess {prozess.name} ist in Warteschlange {i + 2} verschoben worden")
                    else:
                        # Prozess bleibt in der letzten Warteschlange
                        warteschlangen[i].append(prozess)
                        print(f"{aktuelle_zeit}ms: Prozess {prozess.name} bleibt in der letzten Warteschlange")
                else:
                    # Wenn der Prozess abgeschlossen ist
                    print(f"{aktuelle_zeit}ms: Prozess {prozess.name} wurde abgeschlossen")

                # Beende die innere Schleife, um die aktuelle Zeit zu aktualisieren
                break
        else:
            # Erhöhe die aktuelle Zeit, wenn keine Prozesse bearbeitet wurden
            aktuelle_zeit += 1

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
