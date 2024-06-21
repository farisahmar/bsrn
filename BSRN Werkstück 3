import os
import matplotlib.pyplot as plt
import argpase

#Klasse zur Darstellung eines Prozesses
class Process:
	def __init__(self, name, burst_time, arrival_time):
	#Intialisierung der Prozessattribute
	self.name = name #Name des Prozesses
	self.burst_time = burst_time #Gesamtlaufzeit des Prozesses
	self.remaining_time = burst_time #Verbleibende Laufzeit des Prozesses
	self.arrival_time = arrival_time #Ankunftszeit des Prozesses
	self.waiting_time = 0 #Wartezeit des Prozesses
	self.turnaround_time = 0 #Durchlaufzeit des Prozesses
	
#Funktion zur Eingabe der Quantums für jede Warteschlange
def get_quantum_for_queues(warteschlangen_gesamt, input_quantum=None):
	quantum = [] #Liste zur Speicherung der Quantums
	if input_quantum:
		#Wenn Quantums über Kommandozeilenargumente bereitgestellt werden
		for q in input_quantum:
			quantum_value = int(q)
			if quantum_value <= 0: 
				raise ValueError("Quantum muss eine positive Zahl sein.")
			qauntum.append(quantum_value) #Hinzufügen des Quantum-Werts zur Liste
		if len(quantum) != warteschlangen_gesamt:
			raise ValueError("Die Anzahl der Quantums muss der Anzahl der Warteschlangen entsprechen.")
	else:
		#Interaktive Eingabe der Quantums
		for number in range(1, warteschlangen_gesamt +1):
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
def read_processes_from_file(file_path):
	processes = [] #Einlesen aller zeilen der Datei
	try:
		with open(file_path, 'r') as file:
			lines = file.readlines() #Einlesen aller Zeilen der Datei
			for line in lines:
				parts = line.split #Aufteilen der Zeile in einzelnen Teile
				if len(parts) == 3:
				name =parts [0] #Name des Prozesses
				try:
					burst_time = int(parts[1]) #Laufzeit des Prozesses
					arrival_time = int(parts[2] #Ankunftszeit des Prozesses
					processes.append(Process(name, burst_time, arrival_time)) #Hinzufügen des Prozesses zur Liste
				except ValueError as e:
					print(f"Fehler beim Lesen der Prozessdaten: {e}")
	except Exception as e:
		print(f"Fehler beim Lesen der Prozessdaten")
	return processes
	
#Funktion zum Erstellen der Warteschlangen
def erstelle_warteschlangen(warteschlangen_gesamt):
	return [[] for _ in range(warteschlangen_gesamt)] #Rückgabe einer Liste von leeren Listen, eine für jede Warteschlange

#Funktion zum Hinzufügen von Prozessen in die Warteschlange
def prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse, log_file):
	for prozess in prozesse:
		if aktuelle_zeit >= prozess.arrival_time and not in hinzugefuegte_prozesse:
		log_file.write(f"{aktuelle_zeit}ms: Prozess {prozess.name} ist angekommen und in Warteschlange 1 eingereiht.\n")
		warteschlangen[0].append(prozess) #Hinzufügen des Prozesses zu ersten Warteschlange
		hinzugefuegte_prozesse.append(prozess) #Markierung des Prozesses als hinzugefügt

#Funktion zum Round-Robin-Scheduling
def round_robin_scheudling(warteschlangen, quantum, prozesse, hinzugefuegte_prozesse, log_file):
	aktuelle_zeit = 0 #Initialisierung der aktuellen Zeit
	gesamtlaufzeit = sum(prozess.burst_time for prozess in prozesse) #Berechnung der Gesamtlaufzeit aller Prozesse
	timeline_chart = [] #Liste zur Speicherungder Timeline-Daten
	
	while any(warteschlange for warteschlange in warteschlangen) or aktuelle_zeit < gesamtlaufzeit:
	#Hinzufügen von Prozessen zur Warteschlange
	prozesse_in_warteschlange_hinzufuegen(aktuelle_zeit, prozesse, warteschlangen, hinzugefuegte_prozesse, log_file)
	prozess_gelaufen = False #Flag zur Überprüfung, ob ein Prozess in diesem Zyklus gelaufen ist
	
		for i, warteschlange in enumerate(warteschlangen):
			if warteschlange:
				current_quantum = quantum[i] #Aktuelles Quantum für die Warteschlange
				prozess = warteschlange.pop(0) #Prozess aus der Warteschlange entfernen
				
				for _ in range(current_quantum):
					if prozess.remaining_time > 0:
						prozess.remaining_time -= 1 #Verbleibende Laufzeit des Prozesses verringern
						aktuelle_zeit += 1 #Aktuelle Zeit erhöhen
						timeline_chart.append((aktuelle_zeit, prozess.name. i + 1)) #Hinzufügen der Timeline_Daten
						log_file.write(f"{aktuelle_zeit}ms: Prozess {prozess.name} läuft für 1ms(Restlaufzeit: {prozess.remaining_time}ms)\n)
						prozess_gelaufen = True #Markierung, dass ein Prozess gelaufen ist
						if aktuelle_zeit >= gesamtlaufzeit:
							break
							
				if prozess.remaining_time > 0:
					if i < len(warteschlangen) - 1
						warteschlangen[i + 1].append(prozess) #Verschieben des Prozesses in die nächste Warteschlange
						log_file.write(f"   Prozess {prozess.name} ist in Warteschlange {i + 2} verschoben worden\n")
					else:
						warteschlangen[i].append(prozess) #Prozess bleibt in der letzten Warteschlange
						log_file.write(f" Prozess {prozess.name} wurde abgeschlossen\n")
				else:
					prozess.turnaround_time = aktuelle_zeit - prozess.arrival_time #Berechung der Durchlaufzeit
					prozess.waiting_time = prozess.turnaround_time - prozess.burst_time #Berechnung der Wartezeit
					log_file.write(f"   Prozess {prozess.name} wurde abgeschlossen\n")
					
				break #Schleife für die Warteschlangen beenden, wenn kein Prozess gefunden wurde
				
		if not prozess_gelaufen:
			aktuelle_zeit += 1 #Erhöhung der aktuellen Zeit, wenn kein Prozess gelaufen ist

	return timeline_chart
	
#Funktion zur Generierung von deutlich unterscheidbaren Farben
def generate_distinct_colors(num_colors):
	colors = plt.get_cmap('tab10', num_colors) #Nutzung der 'tab10' Farbkarte von matplotlib
	return [colors(i) for in range(num_colors)] Rückgabe der Farben

#Funktion zum Schreiben der Timeline-Diagramme in einer PNG-Datei
def schreibe_timeline_diagramm(timeline_chart, prozesse, timeline_file_path):
	zeiten = [zeit for zeit, _, _ in timeline_chart #Extraktion der Zeiten aus der Timeline
	prozessnamen = [name for _, name, _ in timeline_chart] #Extraktion der Prozessnamen aus der Timeline
	warteschlangen_indices = [queue for _, _, queue in timeline_chart] #Extraktion der Warteschlangen-Indizes aus der Timeline
	
	#Generiere unterscheidbare Farben für die Warteschlangen
	warteschlange_farbe = {}
	unique_queues = sorted(set(warteschlangen_indices)) #Identifikation der einzigartigen Warteschlangen
	colors = generate_distinct_colors(len(unique_queues)) #Generierung von Farben für jede Warteschlange
	
	for queue, color in zip(unique_queues, colors):
		warteschlange_farbe[queue] = color #Zuordnug der Farben zu den Warteschlangen
		
	farben = [warteschlange_farbe[queue] for queue in warteschlangen_indices] #Zuordnung der Farben zu den Timeline-Daten
	
	fig, ax = plt.subplots(figsize=(20, 5)) #Erstellung einer Figur für das Diagramm
	
	#Erstellung der Tabelle mit Zeiten und Prozessnamen
	table_data = [['Zeit']] + [str(zeit) for zeit in zeiten], ['Prozess'] + prozessnamen]
	colors = [['white'] * len(table_data[0], ['white'] + farben]
	
	table = ax.table(cellText = table_data, cellColours = colors, celloc = 'center', loc = 'center') #Hinzufügen der Tabelle zur Figur
	table.scale(1, 2) #Skalierung der Tabelle
	
	ax.axis('off') #Deaktivierung der Achsen
	
	#Erstellung der Legende 
	legend_elements = [plt.Line2D([0], [0], color = color, lw = 4, label = f'Warteschlange {queue}') for queue, color in warteschlange_farbe.items()
	ax.legend(handles = legend_elements, loc = 'upper center', bbox_to_anchor(0.5, 1.15), ncol = len(unique_queues)) #Hinzufügen der Legende zur Figur
	
	#Berechnung der Wartezeiten und Durchlaufzeit
	total_waiting_time = sum(prozess.waiting_time for prozess in prozesse) #Summe der Wartezeiten aller Prozesse
	total_turnaround_time = sum(prozess.turnaround_time for prozess in prozesse) #Summe der Durchlaufzeitaller Prozesse
	avg_waiting_time = total_waiting_time / len(prozesse) #Durchschnittliche Wartezeit
	avg_turnaround_time = total_turnaround_time / len(prozesse) #Durchschnittliche Durchlaufzeit
	
	#Hinzufügen von Laufzeiten und Wartezeiten Informationen
	info_text = 'Laufzeiten und Wartezeiten:\n'
	for prozess in prozesse:
		info_text += f"{prozess.name}: Laufzeit: {prozess.burst_time}, Wartezeit: {prozess.waiting_time}, Gesamtlaufzeit: {prozess.turnaround_time}\n"
	info_text += f"Durchschnittliche Wartezeit: {avg_waiting_time}\n"
	info_text += f"Durchschnittliche Gesamtlaufzeit: {avg_turnaround_time}"
	
	plt.figtext(0.5, -0.1, info_text, ha = "center", frontsize = 12, wrap = True) #Hinzufügen des Informationstext zur Figur
	
	plt.subplots_adjust(left = 0.1, top = 0.8) #Anpassung des Layouts der Figur
	plt.savefig(timeline_file_path, format = 'png', bbox_inches = 'tight') #Speichern des Diagramms als PNG-Datei
	plt.close() #Schließen der Figur
	
#Funktion zum Schreiben der Timeline-Daten in eine TextDatei
def schreibe_timeline_txt(timeline_chart, prozesse, timeline_file_path):
	with open(timeline_file_path, 'w') as file:
		file.write("Zeit\tProzess\tWarteschlangen\n") #Schreiben der Kopfzeile in die TextDatei
		for zeit, prozess, warteschlange in timeline_chart:
			file.write(f"{zeit}ms\t{warteschlange}\n") #Schreiben der Timeline-Daten in die TextDatei
			
			#Berechnung der Wartezeiten und Durchlaufzeiten
			total_waiting_time = sum(prozess.waiting_time for prozess in prozesse) #Summe der Wartezeiten aller Prozesse
			total_turnaround_time = sum(prozess.turnaround_time for prozess in prozesse #Summe der Durchlaufzeiten aller Prozesse
			avg_waiting_time = total_waiting_time / len(prozesse) #Durchschnittliche Wartezeit
			avg_turnaround_time = total_turnaround_time / len(prozesse) #Durchschnittliche Durchlaufzeit
			
			#Hinzufügen von Laufzeiten und Wartezeiten Informationen
			file.write("\nLaufzeit und Wartezeiten:\n")
			for prozess in prozesse:
				file.write(
					f"{prozess.name}: Laufzeit: {prozess.burst_time}, Wartezeit: {prozess.waiting_time},´Gesamtlaufzeit: {prozess.turnaround_time}\n") #Schreiben der Laufzeiten und Wartezeiten der Prozesse in die TextDatei
			file.write(f"Durchschnittliche Wartezeit: {avg_waiting_time}\n")
			file.write(f"Durschnittliche Gesamtlaufzeit:{avg_turnaround_time}\n")
			
#Funktion zum Schreiben der Logdatei
def schreibe_logdatei(log_file_path, warteschlangen_gesamt, quantum, file_path, timeline_file_path, processes):
	with open(log_file_path, 'w') as log_file:
		log_file.write(f"Anzahl der Warteschlangen: {warteschlangen_gesamt}\n") #Schreiben der Anzahl der Warteschlangen in die Logdatei
		log_file.write(f"Quanten pro Warteschlange: {quantum}\n") #Schreiben der Quanten pro Warteschlangen in die Logdatei
		log_file.write(f"Eingabedatei: {file_path}\n") #Schreiben des Pfades der Eingabedatei in die Logdatei
		log_file.write(f"Logdatei: {log_file_path}\n") #Schreiben des Pfades der Logdatei in die Logdatei
		log_file.write(f"Ausgabedatei: {timeline_file_path}\n\n") #Schreiben des Pfades der Timeline-Ausgabedatei in die Logdatei
		
		log_file.write("Processes:\n")
		for process in processes:
			log.file.write(
				f"Name: {process.name}, Laufzeit: {process.burst_time}, Ankunftszeit: {process.arrival_time}\n") #Schreiben der Prozessinformationen in die Logdatei
		log_file.write("\n")
		
		hinzugefuegte_prozesse = []
		warteschlange = erstelle_warteschlangen(warteschlangen_gesamt)
		timeline_chart = round_robin_scheudling(warteschlangen, quantum, processes, hinzugefuegte_prozesse, log_file) #Durchführung des Round-Robin-Scheduling
		
		return timeline_chart
		
	#Hauptfunktion, die sowohl Kommandozeilenargumente als auch interaktive Eingaben unterstützt
	def main():
		parser = argparse.ArgumentParser(description = "Simuliert das Round-Robin-Scheduling von Prozessen.")
		parser.add_argument('-warteschlangen', type = int, help = "Anzahl der Warteschlangen")
		parser.add_argument('-quantum', type = int, nargs = '+', help = "Quanten pro Warteschlange")
		parser.add_argument('-processlistfile', type = str, help = "Quanten pro Warteschlange")
		parser.add_argument('-logdatei', type = str, help = "Pfad zur Logdatei")
		parser.add_argument('-ausgabeformat', type = str, choices = ['text','grafisch'], help = "Format der Ausgabedatei (text oder grafisch)") 
		parser.add_argument('ausgabedatei', type = str, help = "Pfad zur Ausgabedatei")
		
		args = parser.parser_args()
		
		if args.warteschlangen and args.quantum and args.processlistfile and args.logdatei and args.ausgabeformat and args.ausgabedatei:
			#Verwenden der Kommandozeilenargumente
			warteschlangen_gesamt = args.warteschlangen
			quantum = get_quantum_for_queues(warteschlangen_gesamt, args.quantum)
			processes = read_processes_from_file(args.processlistfile)
			log_file_path = args.logdatei
			timeline_file_path = args.ausgabedatei
			output_format = args.ausgabedatei
			file_path = args.processlistfile
		else:
			#Interaktive Eingabe der Parameter
			try:
				warteschlangen_gesamt = int(input("Gib die Anzahl der Warteschlangen an: "))
				if warteschlangen_gesamt <= 0:
					raise ValueError("Die Anzahl der Warteschlangen muss eine positive Zahl sein.")
				quantum = get_quantum_for_queues(warteschlangen_gesamt)
				file_path = input("Geben Sie den Pfad der Eingabedatei an: ")
				processes = read_processes_from_file(file_path)
				log_file_path = input("Geben Sie den Pfad für die Logdatei an: ")
				timeline_file_path = input("Geben Sie den Pfad für die Timeline-Ausgabedatei an: ")
				output_format = input("In welchem Format möchten Sie die Ausgabedatei haben? (text/grafisch): ").strip().lower()
				
				#Überprüfen des Ausgabeformats und des Dateipfades
				if(output_format == "grafisch" and not timeline_file_path.endswith(".png")):
					raise ValueError("Für das grafische Format muss die Ausgabedatei die Endung .png haben.")
				if(output_format == "text" and not timeline_file_path.endswith(".txt")):
					raise ValueError("Für das Textformat muss die Ausgabedatei die Endung .txt haben.")
			except ValueError as e:
				print(f"Ungültige Eingabe: {e}")
				return
				
		#Durchführung des Round-Robin-Scheduling und Schreiben der Logdatei
		timeline_chart = schreibe_logdatei(log_file_path, warteschlangen_gesamt, quantum, file_path, timeline_file_path, processes)
		
		#Schreiben der Timeline in das gewählte Format
		if output_format == 'grafisch':
			schreibe_timeline_diagramm(timeline_chart, processes, timeline_file_path)
		elif output_format == 'text':
			schreibe_timeline_txt(timeline_chart, processes, timeline_file_path)
			
	if __name__ == "__main__":
		main()