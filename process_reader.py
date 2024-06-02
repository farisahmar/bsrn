
class Process:
    # Hier wird definiert, wie der Computer Infos über jeden Prozess speichert.
    
    def __init__(self, name, ankunftszeit, laufzeit):
        # Wenn ein neuer Prozess erstellt wird, werden hier seine Eigenschaften festgelegt.
        self.name = name  # Name des Prozesses
        self.ankunftszeit = ankunftszeit  # Zeit, zu der der Prozess startklar ist
        self.laufzeit = laufzeit  # Dauer des Prozesses

    def __repr__(self):
        # Hier wird festgelegt, wie der Computer den Prozess anzeigen soll, wenn wir ihn sehen wollen.
        return f'("{self.name}", {self.ankunftszeit}, {self.laufzeit})'

def read_processes_from_file(file_path):
    # Hier wird dem Computer erklärt, wie er Prozessinfos aus einer Datei lesen soll.
    processes = []  # Hier werden die gelesenen Prozesse gespeichert.

    try:
        with open(file_path, 'r') as file:
            # Die Datei wird geöffnet, um die Prozessinfos zu lesen.
            lines = file.readlines()  # Jede Zeile der Datei wird gelesen.

            for line in lines:
                # Für jede Zeile der Datei wird Folgendes gemacht:
                parts = line.split()  # Die Zeile wird in Stücke geteilt.

                if len(parts) == 3:
                    # Wenn die Zeile drei Stücke hat (Name, Ankunftszeit, Laufzeit):
                    name = parts[0]  # Der Name wird geholt.
                    ankunftszeit = int(parts[1])  # Die Ankunftszeit wird geholt.
                    laufzeit = int(parts[2])  # Die Laufzeit wird geholt.

                    # Dann wird ein neues Prozessobjekt erstellt und der Liste hinzugefügt.
                    processes.append(Process(name, ankunftszeit, laufzeit))

    except Exception as e:
        # Falls es Probleme beim Lesen gibt, wird eine Fehlermeldung angezeigt.
        print(f"Error reading the file: {e}")

    return processes  # Am Ende wird die Liste der Prozesse zurückgegeben.

if __name__ == "__main__":
    file_path = "processes.txt"  # Hier wird dem Computer gesagt, wo er die Datei mit den Prozessinfos finden kann.
    processes = read_processes_from_file(file_path)  # Die Prozessinfos werden aus der Datei gelesen.

    # Dem Computer wird gesagt, dass er uns die gelesenen Prozesse anzeigen soll.
    print("Processes read from file:")
    for process in processes:
        print(process)  # Jeder Prozess wird angezeigt.
