import matplotlib.pyplot as pyplt
import argparse

#Klasse zur Darstellung eines Prozesses
class Process:
	def __init__(self, name, runtime, arrival_time):
	# Intialisierung der Prozessattribute
		self.name = name #Name des Prozesses
		self.runtime = runtime #Gesamtlaufzeit des Prozesses
		self.remaining_time = runtime #Verbleibende Laufzeit des Prozesses
		self.arrival_time = arrival_time #Ankunftszeit des Prozesses
		self.waiting_time = 0 #Wartezeit des Prozesses
		self.processing_time = 0 #Durchlaufzeit des Prozesses
	
#Funktion zur Eingabe der Quantums für jede Warteschlange
def get_quantum_for_queues(number_of_queues, CLI_quantum=None):
	quantum = [] #Liste zur Speicherung der Quantums
	if CLI_quantum:
		#Wenn Quantums über Kommandozeilenargumente bereitgestellt werden
		for q in CLI_quantum:
			quantum_value = int(q)
			if quantum_value <= 0: 
				raise ValueError("Quantum muss eine positive Zahl sein.")
			quantum.append(quantum_value) #Hinzufügen des Quantum-Werts zur Liste
		if len(quantum) != number_of_queues:
			raise ValueError("Die Anzahl der Quanten, muss die Anzahl der Warteschlangen entsprechen.")
	else:
		#Interaktive Eingabe der Quanten
		for number in range(1, number_of_queues + 1):
			while True:
				try:
					quantum_value = int(input(f"Gib den Quantum der {number}. Warteschlange an: "))
					if quantum_value <= 0:
						raise ValueError("Quantum muss eine positive Zahl sein.")
					quantum.append(quantum_value) #Hinzufügen des Quantum-Werts zur Liste
					break
				except ValueError as e:
					print(f"Ungültige Eingabe: {e}. Bitte versuchen Sie es erneut.")
	return quantum
	
#Funktion zum Einlesen der Prozesse aus einer Datei
def read_processes_from_file(inputfile_path):
	processes = [] # Liste zur Speicherung der Prozesse
	try:
		with open(inputfile_path, 'r') as file:
			lines = file.readlines() #Einlesen aller Zeilen der Datei
			for line in lines:
				parts = line.split() #Aufteilen der Zeile in einzelnen Teile
				if len(parts) == 3:
					name = parts[0] #Name des Prozesses
					try:
						runtime = int(parts[1]) #Laufzeit des Prozesses
						arrival_time = int(parts[2]) #Ankunftszeit des Prozesses
						processes.append(Process(name, runtime, arrival_time)) #Hinzufügen des Prozesses zur Liste
					except ValueError as e:
						print(f"Fehler beim lesen der Prozessdaten: {e}")
	except Exception as e:
		print(f"Fehler beim lesen der Datei: {e}")
	return processes
	
#Funktion zum Erstellen der Warteschlangen
def generate_queue(number_of_queues):
	return [[] for i in range(number_of_queues)] #Rückgabe einer Liste von leeren Listen, eine für jede Warteschlange

#Funktion zum Hinzufügen von Prozessen in die Warteschlange
def add_process_to_queue(current_time, process_list, queue_list, added_processes, log_file):
	for process in process_list:
		if current_time >= process.arrival_time and process not in added_processes:
			log_file.write(f"{current_time}ms: Prozess {process.name} ist angekommen und in Warteschlange 1 eingereiht.\n")
			queue_list[0].append(process) #Hinzufügen des Prozesses zu ersten Warteschlange
			added_processes.append(process) #Markierung des Prozesses als hinzugefügt

#Funktion zum Round-Robin-Scheduling
def round_robin_scheudling(queue_list, quantum, process_list, added_processes, log_file):
	current_time = 0 #Initialisierung der aktuellen Zeit
	total_runtime = sum(process.runtime for process in process_list) #Berechnung der Gesamtlaufzeit aller Prozesse
	timeline_data = [] #Liste zur Speicherungder Timeline-Daten
	
	while any(queue for queue in queue_list) or current_time < total_runtime:
		#Hinzufügen von Prozessen zur Warteschlange
		add_process_to_queue(current_time, process_list, queue_list, added_processes, log_file)
		prozess_gelaufen = False #Flag zur Überprüfung, ob ein Prozess in diesem Zyklus gelaufen ist
	
		for i, queue in enumerate(queue_list):
			if queue:
				current_quantum = quantum[i] #Aktuelles Quantum für die Warteschlange
				process = queue.pop(0) #Prozess aus der Warteschlange entfernen
				
				for j in range(current_quantum):
					if process.remaining_time > 0:
						process.remaining_time -= 1 #Verbleibende Laufzeit des Prozesses verringern
						current_time += 1 #Aktuelle Zeit erhöhen
						timeline_data.append((current_time, process.name, i + 1)) #Hinzufügen der Timeline_Daten
						if current_time < 10:
							log_file.write(f"{current_time}ms: Prozess {process.name} läuft für 1ms(Restlaufzeit: {process.remaining_time}ms)\n")
						else:
							log_file.write(f"{current_time}ms:Prozess {process.name} läuft für 1ms(Restlaufzeit: {process.remaining_time}ms)\n")
						prozess_gelaufen = True	# Markierung, dass ein Prozess gelaufen ist
						if current_time >= total_runtime:
							break
							
				if process.remaining_time > 0:
					if i < len(queue_list) - 1:
						queue_list[i + 1].append(process) #Verschieben des Prozesses in die nächste Warteschlange
						log_file.write(f"     Prozess {process.name} ist in Warteschlange {i + 2} verschoben worden\n")
					else:
						queue_list[i].append(process) #Prozess bleibt in der letzten Warteschlange
						log_file.write(f"     Prozess {process.name} bleibt in der letzten Warteschlange\n")
				else:
					process.processing_time = current_time - process.arrival_time #Berechung der Durchlaufzeit
					process.waiting_time = process.processing_time - process.runtime #Berechnung der Wartezeit
					log_file.write(f"     Prozess {process.name} wurde abgeschlossen\n")
					
				break #Schleife für die Warteschlangen beenden, wenn kein Prozess gefunden wurde
				
		if not prozess_gelaufen:
			current_time += 1 #Erhöhung der aktuellen Zeit, wenn kein Prozess gelaufen ist

	return timeline_data
	
#Funktion zur Generierung der Warteschlangenfarben
def generate_colors(num_colors):
	colors = pyplt.get_cmap('tab10', num_colors) #Nutzung der 'tab10' Farbkarte von matplotlib, um die Fraben besser voneienader unterscheiden zu können
	return [colors(i) for i in range(num_colors)] #Rückgabe der Farben

#Funktion zum Schreiben der Timeline-Diagramme in einer PNG-Datei
def generate_timeline_chart(timeline_data, process_list, timeline_file_path):
	times = [time for time, i, i in timeline_data] #Extraktion der Zeiten aus der Timeline
	process_name = [name for i, name, i in timeline_data] #Extraktion der Prozessnamen aus der Timeline
	queues_indices = [queue for i, i, queue in timeline_data] #Extraktion der Warteschlangen-Indizes aus der Timeline

	#Generiere unterscheidbare Farben für die Warteschlangen
	queue_color = {}
	unique_queues = sorted(set(queues_indices)) #Identifikation der einzigartigen Warteschlangen
	colors = generate_colors(len(unique_queues))  #Generierung von Farben für jede Warteschlange

	for queue, color in zip(unique_queues, colors):
		queue_color[queue] = color #Zuordnug der Farben zu den Warteschlangen

	color = [queue_color[queue] for queue in queues_indices] #Zuordnung der Farben zu den Timeline-Daten

	fig, ax = pyplt.subplots(figsize=(20, 5)) #Erstellung einer Figur für das Diagramm

	#Erstellung der Tabelle mit Zeiten und Prozessnamen
	table_data = [['Zeit'] + [str(time) for time in times], ['Prozess'] + process_name]
	colors = [['white'] * len(table_data[0]), ['white'] + color]

	table = ax.table(cellText=table_data, cellColours=colors, cellLoc='center', loc='center') #Hinzufügen der Tabelle zur Figur
	table.scale(1, 2) #Skalierung der Tabelle

	ax.axis('off') #Deaktivierung der Achsen

	#Erstellung der Legende
	legend_elements = [pyplt.Line2D([0], [0], color=color, lw=4, label=f'Warteschlange {queue}') for queue, color in queue_color.items()]
	ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=len(unique_queues)) #Hinzufügen der Legende zur Figur

	#Berechnung der Wartezeiten und Durchlaufzeit
	total_waiting_time = sum(process.waiting_time for process in process_list) #Summe der Wartezeiten aller Prozesse
	total_processing_time = sum(process.processing_time for process in process_list) #Summe der Durchlaufzeitaller Prozesse
	avg_waiting_time = total_waiting_time / len(process_list) #Durchschnittliche Wartezeit
	avg_processing_time = total_processing_time / len(process_list) #Durchschnittliche Durchlaufzeit

	#Hinzufügen von Laufzeiten und Wartezeiten Informationen
	info_text = 'Laufzeiten und Wartezeiten:\n'
	for process in process_list:
		info_text += f"{process.name}: Laufzeit: {process.runtime}, Wartezeit: {process.waiting_time}, Gesamtlaufzeit: {process.processing_time}\n"
	info_text += f"Durchschnittliche Wartezeit: {avg_waiting_time}\n"
	info_text += f"Durchschnittliche Gesamtlaufzeit: {avg_processing_time}"

	pyplt.figtext(0.5, -0.1, info_text, ha="center", fontsize=12, wrap=True) #Hinzufügen des Informationstext zur Figur

	pyplt.subplots_adjust(left=0.1, top=0.8) #Anpassung des Layouts der Figur
	pyplt.savefig(timeline_file_path, format='png', bbox_inches='tight') #Speichern des Diagramms als PNG-Datei
	pyplt.close() #Schließen der Figur
	
#Funktion zum Schreiben der Timeline-Daten in eine TextDatei
def generate_timeline_text(timeline_data, process_list, timeline_file_path):
	with open(timeline_file_path, 'w') as text_file:
		text_file.write("Zeit\tProzess\tWarteschlangen\n") # Schreiben der Kopfzeile in die TextDatei
		for time, process, queue in timeline_data:
			text_file.write(f"{time}ms\t{process}\t{queue}\n") # Schreiben der Timeline-Daten in die TextDatei

			#Berechnung der Wartezeiten und Durchlaufzeiten
		total_waiting_time = sum(process.waiting_time for process in process_list) #Summe der Wartezeiten aller Prozesse
		total_turnaround_time = sum(process.processing_time for process in process_list) #Summe der Durchlaufzeiten aller Prozesse
		avg_waiting_time = total_waiting_time / len(process_list) #Durchschnittliche Wartezeit
		avg_turnaround_time = total_turnaround_time / len(process_list) #Durchschnittliche Durchlaufzeit

			#Hinzufügen von Laufzeiten und Wartezeiten Informationen
		text_file.write("\nLaufzeit und Wartezeiten:\n")
		for process in process_list:
			text_file.write(
				f"{process.name}: Laufzeit: {process.runtime}, Wartezeit: {process.waiting_time}, Gesamtlaufzeit: {process.processing_time}\n") #Schreiben der Laufzeiten und Wartezeiten der Prozesse in die TextDatei
		text_file.write(f"Durchschnittliche Wartezeit: {avg_waiting_time}\n")
		text_file.write(f"Durschnittliche Gesamtlaufzeit:{avg_turnaround_time}\n")
			
#Funktion zum Schreiben der Logdatei
def generate_logfile(log_file_path, number_of_queues, quantum, inputfile_path, timeline_file_path, processes):
	with open(log_file_path, 'w') as log_file:
		log_file.write(f"Anzahl der Warteschlangen: {number_of_queues}\n") #Schreiben der Anzahl der Warteschlangen in die Logdatei
		log_file.write(f"Quanten pro Warteschlange: {quantum}\n") #Schreiben der Quanten pro Warteschlangen in die Logdatei
		log_file.write(f"Eingabedatei: {inputfile_path}\n") #Schreiben des Pfades der Eingabedatei in die Logdatei
		log_file.write(f"Logdatei: {log_file_path}\n") #Schreiben des Pfades der Logdatei in die Logdatei
		log_file.write(f"Ausgabedatei: {timeline_file_path}\n\n") #Schreiben des Pfades der Timeline-Ausgabedatei in die Logdatei
		
		log_file.write("Processes:\n")
		for process in processes:
			log_file.write(
				f"Name: {process.name}, Laufzeit: {process.runtime}, Ankunftszeit: {process.arrival_time}\n") #Schreiben der Prozessinformationen in die Logdatei
		log_file.write("\n")
		
		added_processes = []
		queue_list = generate_queue(number_of_queues)
		timeline_data = round_robin_scheudling(queue_list, quantum, processes, added_processes, log_file) #Durchführung des Round-Robin-Scheduling
		
		return timeline_data
		
	#Hauptfunktion, die sowohl Kommandozeilenargumente als auch interaktive Eingaben unterstützt
def main():
	parser = argparse.ArgumentParser(description="Simuliert das Round-Robin-Scheduling von Prozessen.")
	parser.add_argument('-queues', type=int, help="Anzahl der Warteschlangen")
	parser.add_argument('-quantum', type=int, nargs='+', help="Quanten pro Warteschlange")
	parser.add_argument('-processlistfile', type=str, help="Quanten pro Warteschlange")
	parser.add_argument('-logfile', type=str, help="Pfad zur Logdatei")
	parser.add_argument('-outputformat', type=str, choices=['text', 'grafisch'], help="Format der Ausgabedatei (text oder grafisch)")
	parser.add_argument('-outputfile', type=str, help="Pfad zur Ausgabedatei")

	args = parser.parse_args()

	if args.queues and args.quantum and args.processlistfile and args.logfile and args.outputformat and args.outputfile:
		# Verwenden der Kommandozeilenargumente
		number_of_queues = args.queues
		quantum = get_quantum_for_queues(number_of_queues, args.quantum)
		processes = read_processes_from_file(args.processlistfile)
		log_file_path = args.logfile
		timeline_file_path = args.outputfile
		output_format = args.outputformat
		inputfile_path = args.processlistfile
	else:
		#Interaktive Eingabe der Parameter
		try:
			number_of_queues = int(input("Gib die Anzahl der Warteschlangen an: "))
			if number_of_queues <= 0:
				raise ValueError("Die Anzahl der Warteschlangen muss eine positive Zahl sein.")
			quantum = get_quantum_for_queues(number_of_queues)
			inputfile_path = input("Geben Sie den Pfad der Eingabedatei an: ")
			processes = read_processes_from_file(inputfile_path)
			log_file_path = input("Geben Sie den Pfad für die Logdatei an: ")
			timeline_file_path = input("Geben Sie den Pfad für die Timeline-Ausgabedatei an: ")
			output_format = input("In welchem Format möchten Sie die Ausgabedatei haben? (text/grafisch): ").strip().lower()

			#Überprüfen des Ausgabeformats und des Dateipfades
			if (output_format == "grafisch" and not timeline_file_path.endswith(".png")):
				raise ValueError("Für das grafische Format muss die Ausgabedatei die Endung .png haben.")
			if (output_format == "text" and not timeline_file_path.endswith(".txt")):
				raise ValueError("Für das Textformat muss die Ausgabedatei die Endung .txt haben.")
		except ValueError as e:
			print(f"Ungültige Eingabe: {e}")
			return

	#Durchführung des Round-Robin-Scheduling und Schreiben der Logdatei
	timeline_data = generate_logfile(log_file_path, number_of_queues, quantum, inputfile_path, timeline_file_path, processes)

	#Schreiben der Timeline in das gewählte Format
	if output_format == 'grafisch':
		generate_timeline_chart(timeline_data, processes, timeline_file_path)
	elif output_format == 'text':
		generate_timeline_text(timeline_data, processes, timeline_file_path)
			
if __name__ == "__main__":
	main()
