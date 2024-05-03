warteschlangen_gesamt = int(2)
quantum = []

# Quantum pro Warteschlange generrieren
def get_quantum_for_queues(warteschlangen_gesamt):
    quantum = []
    for number in range(1, warteschlangen_gesamt + 1):
        quantum_value = int(input("Gib den Quantum der " + str(number) + ". Warteschlange an: "))
        quantum.append(quantum_value)
    return quantum

# Warteschlangen generieren, je nachdem wie viel Warteschlangen es insgesamt gibt
def erstelle_warteschlangen(warteschlangen_gesamt):
    warteschlangen = []
    for i in range(1, warteschlangen_gesamt + 1):
        warteschlange_name = "warteschlange" + str(i)
        warteschlange = []  # leeres Array für jede Warteschlange erstellen
        warteschlangen.append(warteschlange)
    return warteschlangen

warteschlangen = erstelle_warteschlangen(warteschlangen_gesamt)

# Prozesse in Warteschlange 1 hinzufügen
def prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlange):
    for prozess in prozesse:
        if aktuelle_zeit == prozess.ankunftszeit:
            print(f"Prozess {prozess.name} ist zur Zeit {aktuelle_zeit} angekommen und wird zur Warteschlange 1 hinzugefügt.")
            warteschlange[0].append(prozess)

# Prozess-Klasse definieren
class Prozess:
    def __init__(self, name, laufzeit ,ankunftszeit):
        self.name = name
        self.laufzeit = laufzeit
        self.ankunftszeit = ankunftszeit

# Prozessbeispiele erstellen
prozesse = [
    Prozess("A", 8, 0),
    Prozess("B", 4, 1),
    Prozess("C", 13, 5)
]
# gesamtlaufzeit berechnen
gesamtlaufzeit = sum(Prozess.laufzeit for Prozess in prozesse)
aktuelle_zeit = 0


print(warteschlangen)
for number in range(gesamtlaufzeit):
    prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen)
    aktuelle_zeit += 1
print(warteschlangen)


# Laufzeit bestimmen
#while aktuelle_zeit <= gesamtlaufzeit:
 #   for prozess in prozesse:
#
        # Prozess hinzufügen
 #       if aktuelle_zeit == Prozess.ankunftszeit:
  #          warteschlange.append(Prozess)
   #         print(f"Prozess {Prozess.name} ist angekommen.")

            # Iteration durch Warteschlange
    #        for number in range(1, warteschlange + 1):
     #           print("Warteschlange: " + str(number) + "\n-----------------------")

                # Round Robin in Warteschlange
      #          for prozess_in_warteschlange in prozesse:
       #             prozess_in_warteschlange.laufzeit -= quantum[number - 1]
        #            aktuelle_zeit += 1
         #           print(aktuelle_zeit)
          #          print(f"Restliche Laufzeit von {prozess_in_warteschlange.name}: {prozess_in_warteschlange.laufzeit}")

#
