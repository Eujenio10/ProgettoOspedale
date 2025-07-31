import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
from datetime import datetime
from logger import activity_logger

class GestionePazientiWindow:
    def __init__(self, parent, db_manager, reparto, current_user=None):
        """Inizializza la finestra di gestione pazienti"""
        self.parent = parent
        self.db_manager = db_manager
        self.reparto = reparto
        self.current_user = current_user or {}
        
        # Configurazione finestra
        self.window = tk.Toplevel(parent)
        self.window.title(f"Gestione Pazienti - {reparto}")
        self.window.geometry("900x600")
        self.window.configure(bg='#ecf0f1')
        
        # Centra la finestra
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.carica_pazienti()
        self.carica_stanze_combo()
        
    def filtra_risultati(self, *args):
        """Filtra i risultati in base alla ricerca"""
        search_term = self.search_var.get().lower()
        
        # Pulisce la lista
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Carica tutti i pazienti e filtra
        pazienti = self.db_manager.get_pazienti_reparto(self.reparto)
        
        for paziente in pazienti:
            nome = paziente[1].lower()
            cognome = paziente[2].lower()
            cf = paziente[3].lower()
            
            # Applica filtro di ricerca
            if not search_term or search_term in nome or search_term in cognome or search_term in cf:
                self.tree.insert('', 'end', values=(
                    paziente[0],  # ID
                    paziente[1],  # Nome
                    paziente[2],  # Cognome
                    paziente[3],  # Codice Fiscale
                    paziente[4],  # Data Nascita
                    paziente[8],  # Sesso (indice 8)
                    paziente[9],  # Comune Nascita (indice 9)
                    paziente[10] if paziente[10] else "Non assegnata",  # Nome stanza (indice 10)
                    paziente[7]  # Data Ricovero (indice 7)
                ))
    
    def pulisci_ricerca(self):
        """Pulisce la ricerca e ricarica tutti i pazienti"""
        self.search_var.set("")
        self.carica_pazienti()
        
    def create_widgets(self):
        """Crea i widget dell'interfaccia"""
        # Frame principale
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titolo
        title_label = tk.Label(main_frame, text=f"GESTIONE PAZIENTI - REPARTO {self.reparto.upper()}", 
                              font=('Arial', 16, 'bold'), 
                              bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Frame per inserimento
        input_frame = tk.Frame(main_frame, bg='#ecf0f1')
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Griglia per i campi
        # Prima riga
        tk.Label(input_frame, text="Nome:", bg='#ecf0f1').grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.nome_entry = tk.Entry(input_frame, width=15)
        self.nome_entry.grid(row=0, column=1, padx=(0, 20))
        
        tk.Label(input_frame, text="Cognome:", bg='#ecf0f1').grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.cognome_entry = tk.Entry(input_frame, width=15)
        self.cognome_entry.grid(row=0, column=3, padx=(0, 20))
        
        tk.Label(input_frame, text="Codice Fiscale:", bg='#ecf0f1').grid(row=0, column=4, sticky='w', padx=(0, 10))
        self.cf_entry = tk.Entry(input_frame, width=15)
        self.cf_entry.grid(row=0, column=5, padx=(0, 20))
        
        # Seconda riga
        tk.Label(input_frame, text="Data Nascita:", bg='#ecf0f1').grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.data_nascita_entry = tk.Entry(input_frame, width=15)
        self.data_nascita_entry.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
        self.data_nascita_entry.insert(0, "DD-MM-YYYY")
        
        tk.Label(input_frame, text="Sesso:", bg='#ecf0f1').grid(row=1, column=2, sticky='w', padx=(0, 10), pady=(10, 0))
        self.sesso_combo = ttk.Combobox(input_frame, width=8, values=['M', 'F'])
        self.sesso_combo.grid(row=1, column=3, padx=(0, 20), pady=(10, 0))
        
        # Terza riga
        tk.Label(input_frame, text="Comune Nascita:", bg='#ecf0f1').grid(row=2, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.comune_entry = tk.Entry(input_frame, width=15)
        self.comune_entry.grid(row=2, column=1, padx=(0, 20), pady=(10, 0))
        
        tk.Label(input_frame, text="Stanza:", bg='#ecf0f1').grid(row=2, column=2, sticky='w', padx=(0, 10), pady=(10, 0))
        self.stanza_combo = ttk.Combobox(input_frame, width=12)
        self.stanza_combo.grid(row=2, column=3, padx=(0, 20), pady=(10, 0))
        
        # Pulsanti
        btn_frame = tk.Frame(input_frame, bg='#ecf0f1')
        btn_frame.grid(row=3, column=0, columnspan=6, pady=(15, 0))
        
        tk.Button(btn_frame, text="Aggiungi Paziente", command=self.aggiungi_paziente,
                 bg='#27ae60', fg='white', relief='flat').pack(side='left', padx=(0, 10))
        tk.Button(btn_frame, text="Modifica Paziente", command=self.modifica_paziente,
                 bg='#f39c12', fg='white', relief='flat').pack(side='left', padx=(0, 10))
        tk.Button(btn_frame, text="Elimina Paziente", command=self.elimina_paziente,
                 bg='#e74c3c', fg='white', relief='flat').pack(side='left', padx=(0, 10))
        tk.Button(btn_frame, text="Scheda Clinica", command=self.apri_scheda_clinica,
                 bg='#3498db', fg='white', relief='flat').pack(side='left')
        
        # Frame per la ricerca
        search_frame = tk.Frame(main_frame, bg='#ecf0f1')
        search_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(search_frame, text="🔍 Ricerca Pazienti:", bg='#ecf0f1', font=('Arial', 12, 'bold')).pack(side='left', padx=(0, 10))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filtra_risultati)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.pack(side='left', padx=(0, 10))
        
        # Pulsante per pulire la ricerca
        tk.Button(search_frame, text="❌ Pulisci", command=self.pulisci_ricerca,
                 bg='#95a5a6', fg='white', relief='flat').pack(side='left')
        
        # Lista pazienti
        list_frame = tk.Frame(main_frame, bg='#ecf0f1')
        list_frame.pack(expand=True, fill='both')
        
        tk.Label(list_frame, text="Pazienti del Reparto:", bg='#ecf0f1', font=('Arial', 12, 'bold')).pack(anchor='w')
        
        # Treeview per la lista
        columns = ('ID', 'Nome', 'Cognome', 'Codice Fiscale', 'Data Nascita', 'Sesso', 'Comune Nascita', 'Stanza', 'Data Ricovero')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == 'ID':
                self.tree.column(col, width=50)
            elif col in ['Nome', 'Cognome']:
                self.tree.column(col, width=100)
            elif col == 'Codice Fiscale':
                self.tree.column(col, width=120)
            elif col == 'Data Nascita':
                self.tree.column(col, width=100)
            elif col == 'Sesso':
                self.tree.column(col, width=60)
            elif col == 'Comune Nascita':
                self.tree.column(col, width=120)
            elif col == 'Stanza':
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=120)
        
        self.tree.pack(expand=True, fill='both', pady=(10, 0))
        self.tree.bind('<<TreeviewSelect>>', self.seleziona_paziente)
        self.tree.bind('<Double-1>', self.apri_scheda_clinica_double_click)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Carica le stanze disponibili
        self.carica_stanze_combo()
        
    def carica_stanze_combo(self):
        """Carica le stanze nel combobox"""
        stanze = self.db_manager.get_stanze_reparto(self.reparto)
        stanze_disponibili = []
        for stanza in stanze:
            try:
                max_pazienti = int(stanza[3])  # max_pazienti è alla posizione 3
                pazienti_attuali = int(stanza[5])  # pazienti_attuali è alla posizione 5
                posti_liberi = max_pazienti - pazienti_attuali
                
                if posti_liberi > 0:
                    stanze_disponibili.append(f"{stanza[1]} ({posti_liberi} posti liberi)")
            except (ValueError, TypeError) as e:
                print(f"Errore nel caricamento stanza {stanza[1]}: {e}")
                # Fallback: considera la stanza come disponibile
                stanze_disponibili.append(f"{stanza[1]} (disponibile)")
        
        self.stanza_combo['values'] = stanze_disponibili
        if stanze_disponibili:
            self.stanza_combo.set(stanze_disponibili[0])
    
    def carica_pazienti(self):
        """Carica la lista dei pazienti"""
        # Pulisce la lista
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Carica dal database
        pazienti = self.db_manager.get_pazienti_reparto(self.reparto)
        for paziente in pazienti:
            self.tree.insert('', 'end', values=(
                paziente[0],  # ID
                paziente[1],  # Nome
                paziente[2],  # Cognome
                paziente[3],  # Codice Fiscale
                paziente[4],  # Data Nascita
                paziente[8],  # Sesso (indice 8)
                paziente[9],  # Comune Nascita (indice 9)
                paziente[10] if paziente[10] else "Non assegnata",  # Nome Stanza (indice 10)
                paziente[7]   # Data Ricovero (indice 7)
            ))
        
        # Ricarica le stanze disponibili
        self.carica_stanze_combo()
    
    def seleziona_paziente(self, event):
        """Gestisce la selezione di un paziente"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, values[1])
            self.cognome_entry.delete(0, tk.END)
            self.cognome_entry.insert(0, values[2])
            self.cf_entry.delete(0, tk.END)
            self.cf_entry.insert(0, values[3])
            self.data_nascita_entry.delete(0, tk.END)
            # Converti da YYYY-MM-DD a DD-MM-YYYY per la visualizzazione
            try:
                data_db = values[4]
                if data_db and data_db != "None":
                    anno, mese, giorno = data_db.split('-')
                    data_visual = f"{giorno}-{mese}-{anno}"
                    self.data_nascita_entry.insert(0, data_visual)
                else:
                    self.data_nascita_entry.insert(0, "DD-MM-YYYY")
            except:
                self.data_nascita_entry.insert(0, "DD-MM-YYYY")
            
            # Popola sesso e comune
            self.sesso_combo.set(values[5] if values[5] else '')  # Sesso nella treeview
            self.comune_entry.delete(0, tk.END)
            self.comune_entry.insert(0, values[6] if values[6] else '')  # Comune nella treeview
            
            # Trova la stanza corrispondente
            stanza_nome = values[7]  # Nome Stanza (indice 7 nella treeview)
            if stanza_nome and stanza_nome != "Non assegnata":
                for i, stanza in enumerate(self.stanza_combo['values']):
                    if isinstance(stanza, str) and str(stanza_nome) in str(stanza):
                        self.stanza_combo.current(i)
                        break
    
    def aggiungi_paziente(self):
        """Aggiunge un nuovo paziente"""
        nome = self.nome_entry.get().strip()
        cognome = self.cognome_entry.get().strip()
        cf = self.cf_entry.get().strip()
        data_nascita = self.data_nascita_entry.get().strip()
        sesso = self.sesso_combo.get()
        comune_nascita = self.comune_entry.get().strip()
        stanza_selezionata = self.stanza_combo.get()
        
        if not all([nome, cognome, cf, data_nascita, sesso, comune_nascita]):
            messagebox.showerror("Errore", "Tutti i campi sono obbligatori!")
            return
        
        # Validazione data di nascita (formato DD-MM-YYYY)
        try:
            if data_nascita == "DD-MM-YYYY":
                raise ValueError()
            # Converti da DD-MM-YYYY a YYYY-MM-DD per il database
            giorno, mese, anno = data_nascita.split('-')
            data_convertita = f"{anno}-{mese.zfill(2)}-{giorno.zfill(2)}"
            datetime.strptime(data_convertita, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Errore", "Data di nascita non valida! Usa il formato DD-MM-YYYY")
            return
        
        # Validazione sesso
        if sesso not in ['M', 'F']:
            messagebox.showerror("Errore", "Seleziona un sesso valido (M/F)!")
            return
        
        # Validazione codice fiscale (semplice)
        if len(cf) != 16:
            messagebox.showerror("Errore", "Il codice fiscale deve essere di 16 caratteri!")
            return
        
        # Trova l'ID della stanza selezionata
        stanza_id = None
        if stanza_selezionata and stanza_selezionata != "Non assegnata":
            stanze = self.db_manager.get_stanze_reparto(self.reparto)
            for stanza in stanze:
                if stanza[1] in stanza_selezionata:
                    stanza_id = stanza[0]
                    break
        
        # Inserisce il paziente
        paziente_id = self.db_manager.inserisci_paziente(nome, cognome, cf, data_convertita, sesso, comune_nascita, stanza_id, self.reparto)
        
        if paziente_id:
            # Log dell'aggiunta paziente
            activity_logger.log_patient_action(
                user_id=self.current_user.get('id_impiegato', ''),
                user_name=f"{self.current_user.get('nome', '')} {self.current_user.get('cognome', '')}",
                user_reparto=self.reparto,
                action="INSERT",
                patient_id=paziente_id,
                patient_name=nome,
                patient_surname=cognome,
                details=f"CF: {cf}, Data: {data_convertita}, Sesso: {sesso}, Comune: {comune_nascita}"
            )
            messagebox.showinfo("Successo", f"Paziente {nome} {cognome} aggiunto con successo!")
            self.pulisci_campi()
            self.carica_pazienti()
        else:
            messagebox.showerror("Errore", "Codice fiscale già esistente!")
    
    def modifica_paziente(self):
        """Modifica un paziente esistente"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Errore", "Selezionare un paziente da modificare!")
            return
        
        # Ottieni i dati dal form
        nome = self.nome_entry.get().strip()
        cognome = self.cognome_entry.get().strip()
        cf = self.cf_entry.get().strip()
        data_nascita = self.data_nascita_entry.get().strip()
        sesso = self.sesso_combo.get()
        comune_nascita = self.comune_entry.get().strip()
        stanza_selezionata = self.stanza_combo.get()
        
        if not all([nome, cognome, cf, data_nascita, sesso, comune_nascita]):
            messagebox.showerror("Errore", "Tutti i campi sono obbligatori!")
            return
        
        # Validazione data di nascita (formato DD-MM-YYYY)
        try:
            if data_nascita == "DD-MM-YYYY":
                raise ValueError()
            # Converti da DD-MM-YYYY a YYYY-MM-DD per il database
            giorno, mese, anno = data_nascita.split('-')
            data_convertita = f"{anno}-{mese.zfill(2)}-{giorno.zfill(2)}"
            datetime.strptime(data_convertita, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Errore", "Data di nascita non valida! Usa il formato DD-MM-YYYY")
            return
        
        # Validazione sesso
        if sesso not in ['M', 'F']:
            messagebox.showerror("Errore", "Seleziona un sesso valido (M/F)!")
            return
        
        # Validazione codice fiscale (semplice)
        if len(cf) != 16:
            messagebox.showerror("Errore", "Il codice fiscale deve essere di 16 caratteri!")
            return
        
        # Trova l'ID della stanza selezionata
        stanza_id = None
        if stanza_selezionata and stanza_selezionata != "Non assegnata":
            stanze = self.db_manager.get_stanze_reparto(self.reparto)
            for stanza in stanze:
                if stanza[1] in stanza_selezionata:
                    stanza_id = stanza[0]
                    break
        
        # Ottieni l'ID del paziente selezionato
        item = self.tree.item(selection[0])
        values = item['values']
        paziente_id = values[0]
        
        # Aggiorna il paziente nel database
        success = self.db_manager.aggiorna_paziente(paziente_id, nome, cognome, cf, data_convertita, sesso, comune_nascita, stanza_id, self.reparto)
        
        if success:
            # Log della modifica paziente
            activity_logger.log_patient_action(
                user_id=self.current_user.get('id_impiegato', ''),
                user_name=f"{self.current_user.get('nome', '')} {self.current_user.get('cognome', '')}",
                user_reparto=self.reparto,
                action="UPDATE",
                patient_id=paziente_id,
                patient_name=nome,
                patient_surname=cognome,
                details=f"CF: {cf}, Data: {data_convertita}, Sesso: {sesso}, Comune: {comune_nascita}"
            )
            messagebox.showinfo("Successo", f"Paziente {nome} {cognome} modificato con successo!")
            self.pulisci_campi()
            self.carica_pazienti()
        else:
            messagebox.showerror("Errore", "Errore durante la modifica del paziente!")
    
    def elimina_paziente(self):
        """Elimina un paziente"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Errore", "Selezionare un paziente da eliminare!")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        paziente_id = values[0]
        nome = values[1]
        cognome = values[2]
        
        if messagebox.askyesno("Conferma", f"Eliminare il paziente {nome} {cognome}?"):
            # Elimina dal database
            success = self.db_manager.elimina_paziente(paziente_id)
            
            if success:
                # Log dell'eliminazione paziente
                activity_logger.log_patient_action(
                    user_id=self.current_user.get('id_impiegato', ''),
                    user_name=f"{self.current_user.get('nome', '')} {self.current_user.get('cognome', '')}",
                    user_reparto=self.reparto,
                    action="DELETE",
                    patient_id=paziente_id,
                    patient_name=nome,
                    patient_surname=cognome,
                    details="Paziente eliminato dal sistema"
                )
                messagebox.showinfo("Successo", f"Paziente {nome} {cognome} eliminato!")
                self.pulisci_campi()
                self.carica_pazienti()
            else:
                messagebox.showerror("Errore", "Errore durante l'eliminazione del paziente!")
    
    def apri_scheda_clinica(self):
        """Apre la finestra della scheda clinica"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Errore", "Selezionare un paziente per visualizzare la scheda clinica!")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        paziente_id = values[0]
        nome = values[1]
        cognome = values[2]
        
        # Log dell'accesso alla scheda clinica
        activity_logger.log_clinical_record_access(
            user_id=self.current_user.get('id_impiegato', ''),
            user_name=f"{self.current_user.get('nome', '')} {self.current_user.get('cognome', '')}",
            user_reparto=self.reparto,
            patient_id=paziente_id,
            patient_name=nome,
            patient_surname=cognome
        )
        SchedaClinicaWindow(self.window, self.db_manager, paziente_id, nome, cognome)
    
    def apri_scheda_clinica_double_click(self, event):
        """Apre la scheda clinica con doppio click"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            paziente_id = values[0]
            nome = values[1]
            cognome = values[2]
            
            # Apri la finestra della scheda clinica
            SchedaClinicaWindow(self.window, self.db_manager, paziente_id, nome, cognome, self.current_user)
    
    def pulisci_campi(self):
        """Pulisce tutti i campi"""
        self.nome_entry.delete(0, tk.END)
        self.cognome_entry.delete(0, tk.END)
        self.cf_entry.delete(0, tk.END)
        self.data_nascita_entry.delete(0, tk.END)
        self.data_nascita_entry.insert(0, "DD-MM-YYYY")
        self.sesso_combo.set('')
        self.comune_entry.delete(0, tk.END)
        if self.stanza_combo['values']:
            self.stanza_combo.set(self.stanza_combo['values'][0])

class SchedaClinicaWindow:
    def __init__(self, parent, db_manager, paziente_id, nome, cognome, current_user=None):
        """Inizializza la finestra della scheda clinica"""
        self.parent = parent
        self.db_manager = db_manager
        self.paziente_id = paziente_id
        self.nome = nome
        self.cognome = cognome
        self.current_user = current_user or {}
        
        # Configurazione finestra
        self.window = tk.Toplevel(parent)
        self.window.title(f"Scheda Clinica - {nome} {cognome}")
        self.window.geometry("800x700")
        self.window.configure(bg='#ecf0f1')
        
        # Centra la finestra
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.carica_scheda()
        
    def create_widgets(self):
        """Crea i widget dell'interfaccia"""
        # Frame principale con scrollbar
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titolo
        title_label = tk.Label(main_frame, text=f"SCHEDA CLINICA - {self.nome.upper()} {self.cognome.upper()}", 
                              font=('Arial', 16, 'bold'), 
                              bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Canvas con scrollbar per il contenuto
        canvas = tk.Canvas(main_frame, bg='#ecf0f1', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame per i campi
        form_frame = tk.Frame(scrollable_frame, bg='#ecf0f1')
        form_frame.pack(expand=True, fill='both', padx=10)
        
        # Diagnosi
        tk.Label(form_frame, text="Diagnosi:", bg='#ecf0f1', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        self.diagnosi_text = tk.Text(form_frame, height=4, width=80)
        self.diagnosi_text.pack(fill='x', pady=(0, 15))
        
        # Terapie
        tk.Label(form_frame, text="Terapie in corso:", bg='#ecf0f1', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        self.terapie_text = tk.Text(form_frame, height=4, width=80)
        self.terapie_text.pack(fill='x', pady=(0, 15))
        
        # Farmaci
        tk.Label(form_frame, text="Farmaci somministrati:", bg='#ecf0f1', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        self.farmaci_text = tk.Text(form_frame, height=4, width=80)
        self.farmaci_text.pack(fill='x', pady=(0, 15))
        
        # Esami
        tk.Label(form_frame, text="Esami eseguiti:", bg='#ecf0f1', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        self.esami_text = tk.Text(form_frame, height=4, width=80)
        self.esami_text.pack(fill='x', pady=(0, 15))
        
        # Medico referente
        tk.Label(form_frame, text="Medico referente:", bg='#ecf0f1', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        self.medico_entry = tk.Entry(form_frame, width=60)
        self.medico_entry.pack(anchor='w', pady=(0, 15))
        
        # Annotazioni
        tk.Label(form_frame, text="Annotazioni aggiuntive:", bg='#ecf0f1', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        self.annotazioni_text = tk.Text(form_frame, height=4, width=80)
        self.annotazioni_text.pack(fill='x', pady=(0, 15))
        
        # Pulsanti
        btn_frame = tk.Frame(form_frame, bg='#ecf0f1')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="💾 Salva Scheda", command=self.salva_scheda,
                 bg='#27ae60', fg='white', relief='flat', width=20, font=('Arial', 10, 'bold')).pack(side='left', padx=(0, 10))
        tk.Button(btn_frame, text="❌ Chiudi", command=self.window.destroy,
                 bg='#95a5a6', fg='white', relief='flat', width=15, font=('Arial', 10, 'bold')).pack(side='left')
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Binding per lo scroll con il mouse
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                # Ignora errori se il widget è stato distrutto
                pass
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def carica_scheda(self):
        """Carica i dati della scheda clinica"""
        scheda = self.db_manager.get_scheda_clinica(self.paziente_id)
        
        if scheda:
            self.diagnosi_text.delete('1.0', tk.END)
            self.diagnosi_text.insert('1.0', scheda[2] or '')
            
            self.terapie_text.delete('1.0', tk.END)
            self.terapie_text.insert('1.0', scheda[3] or '')
            
            self.farmaci_text.delete('1.0', tk.END)
            self.farmaci_text.insert('1.0', scheda[4] or '')
            
            self.esami_text.delete('1.0', tk.END)
            self.esami_text.insert('1.0', scheda[5] or '')
            
            self.medico_entry.delete(0, tk.END)
            self.medico_entry.insert(0, scheda[6] or '')
            
            self.annotazioni_text.delete('1.0', tk.END)
            self.annotazioni_text.insert('1.0', scheda[7] or '')
    
    def salva_scheda(self):
        """Salva la scheda clinica"""
        diagnosi = self.diagnosi_text.get('1.0', tk.END).strip()
        terapie = self.terapie_text.get('1.0', tk.END).strip()
        farmaci = self.farmaci_text.get('1.0', tk.END).strip()
        esami = self.esami_text.get('1.0', tk.END).strip()
        medico = self.medico_entry.get().strip()
        annotazioni = self.annotazioni_text.get('1.0', tk.END).strip()
        
        self.db_manager.aggiorna_scheda_clinica(
            self.paziente_id, diagnosi, terapie, farmaci, esami, medico, annotazioni
        )
        
        # Log dell'aggiornamento scheda clinica
        activity_logger.log_clinical_record_update(
            user_id="",  # Sarà impostato dal dashboard
            user_name="",  # Sarà impostato dal dashboard
            user_reparto="",  # Sarà impostato dal dashboard
            patient_id=self.paziente_id,
            patient_name=self.nome,
            patient_surname=self.cognome,
            details=f"Medico: {medico}, Diagnosi aggiornata"
        )
        
        messagebox.showinfo("Successo", "Scheda clinica salvata con successo!") 