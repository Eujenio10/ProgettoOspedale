import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
from pazienti import SchedaClinicaWindow

class GestioneStanzeWindow:
    def __init__(self, parent, db_manager, reparto):
        """Inizializza la finestra di gestione stanze"""
        self.parent = parent
        self.db_manager = db_manager
        self.reparto = reparto
        self.stanza_selezionata = None
        
        # Configurazione finestra
        self.window = tk.Toplevel(parent)
        self.window.title(f"Gestione Stanze - {reparto}")
        self.window.geometry("1000x700")
        self.window.configure(bg='#ecf0f1')
        
        # Centra la finestra
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.carica_stanze()
        
    def create_widgets(self):
        """Crea i widget dell'interfaccia"""
        # Frame principale
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titolo
        title_label = tk.Label(main_frame, text=f"GESTIONE STANZE - REPARTO {self.reparto.upper()}", 
                              font=('Arial', 16, 'bold'), 
                              bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Frame per inserimento
        input_frame = tk.Frame(main_frame, bg='#ecf0f1')
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Griglia per i campi
        tk.Label(input_frame, text="Nome Stanza:", bg='#ecf0f1').grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.nome_entry = tk.Entry(input_frame, width=20)
        self.nome_entry.grid(row=0, column=1, padx=(0, 20))
        
        tk.Label(input_frame, text="Max Pazienti:", bg='#ecf0f1').grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.max_pazienti_entry = tk.Entry(input_frame, width=10)
        self.max_pazienti_entry.grid(row=0, column=3, padx=(0, 20))
        
        # Pulsanti
        btn_frame = tk.Frame(input_frame, bg='#ecf0f1')
        btn_frame.grid(row=1, column=0, columnspan=4, pady=(15, 0))
        
        tk.Button(btn_frame, text="Aggiungi Stanza", command=self.aggiungi_stanza,
                 bg='#27ae60', fg='white', relief='flat').pack(side='left', padx=(0, 10))
        tk.Button(btn_frame, text="Modifica Stanza", command=self.modifica_stanza,
                 bg='#f39c12', fg='white', relief='flat').pack(side='left', padx=(0, 10))
        tk.Button(btn_frame, text="Elimina Stanza", command=self.elimina_stanza,
                 bg='#e74c3c', fg='white', relief='flat').pack(side='left')
        

        
        # Frame principale diviso in due colonne
        content_frame = tk.Frame(main_frame, bg='#ecf0f1')
        content_frame.pack(expand=True, fill='both')
        
        # Colonna sinistra - Stanze
        left_frame = tk.Frame(content_frame, bg='#ecf0f1')
        left_frame.pack(side='left', expand=True, fill='both', padx=(0, 10))
        
        tk.Label(left_frame, text="🏥 STANZE DEL REPARTO:", bg='#ecf0f1', font=('Arial', 12, 'bold')).pack(anchor='w')
        
        # Treeview per le stanze
        columns_stanze = ('ID', 'Nome Stanza', 'Max Pazienti', 'Pazienti Attuali', 'Posti Liberi')
        self.tree_stanze = ttk.Treeview(left_frame, columns=columns_stanze, show='headings', height=15)
        
        for col in columns_stanze:
            self.tree_stanze.heading(col, text=col)
            if col == 'ID':
                self.tree_stanze.column(col, width=50)
            elif col == 'Nome Stanza':
                self.tree_stanze.column(col, width=150)
            else:
                self.tree_stanze.column(col, width=100)
        
        self.tree_stanze.pack(expand=True, fill='both', pady=(10, 0))
        self.tree_stanze.bind('<<TreeviewSelect>>', self.seleziona_stanza)
        
        # Scrollbar per stanze
        scrollbar_stanze = ttk.Scrollbar(left_frame, orient='vertical', command=self.tree_stanze.yview)
        scrollbar_stanze.pack(side='right', fill='y')
        self.tree_stanze.configure(yscrollcommand=scrollbar_stanze.set)
        
        # Colonna destra - Pazienti della stanza selezionata
        right_frame = tk.Frame(content_frame, bg='#ecf0f1')
        right_frame.pack(side='right', expand=True, fill='both', padx=(10, 0))
        
        self.pazienti_label = tk.Label(right_frame, text="👥 PAZIENTI DELLA STANZA:", bg='#ecf0f1', font=('Arial', 12, 'bold'))
        self.pazienti_label.pack(anchor='w')
        
        # Treeview per i pazienti
        columns_pazienti = ('ID', 'Nome', 'Cognome', 'Codice Fiscale', 'Data Nascita', 'Scheda Clinica')
        self.tree_pazienti = ttk.Treeview(right_frame, columns=columns_pazienti, show='headings', height=15)
        
        for col in columns_pazienti:
            self.tree_pazienti.heading(col, text=col)
            if col == 'ID':
                self.tree_pazienti.column(col, width=50)
            elif col in ['Nome', 'Cognome']:
                self.tree_pazienti.column(col, width=100)
            elif col == 'Codice Fiscale':
                self.tree_pazienti.column(col, width=120)
            elif col == 'Data Nascita':
                self.tree_pazienti.column(col, width=100)
            else:
                self.tree_pazienti.column(col, width=100)
        
        self.tree_pazienti.pack(expand=True, fill='both', pady=(10, 0))
        self.tree_pazienti.bind('<Double-1>', self.apri_scheda_clinica)
        
        # Scrollbar per pazienti
        scrollbar_pazienti = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree_pazienti.yview)
        scrollbar_pazienti.pack(side='right', fill='y')
        self.tree_pazienti.configure(yscrollcommand=scrollbar_pazienti.set)
        
    def carica_stanze(self):
        """Carica la lista delle stanze"""
        # Pulisce la lista
        for item in self.tree_stanze.get_children():
            self.tree_stanze.delete(item)
        
        # Carica dal database
        stanze = self.db_manager.get_stanze_reparto(self.reparto)
        for stanza in stanze:
            try:
                max_pazienti = int(stanza[3])  # max_pazienti è alla posizione 3
                pazienti_attuali = int(stanza[5])  # pazienti_attuali è alla posizione 5
                posti_liberi = max_pazienti - pazienti_attuali
                
                self.tree_stanze.insert('', 'end', values=(
                    stanza[0],  # ID
                    stanza[1],  # Nome stanza
                    max_pazienti,  # Max pazienti
                    pazienti_attuali,  # Pazienti attuali
                    posti_liberi
                ))
            except (ValueError, TypeError) as e:
                print(f"Errore nel caricamento stanza {stanza[1]}: {e}")
                self.tree_stanze.insert('', 'end', values=(
                    stanza[0],  # ID
                    stanza[1],  # Nome stanza
                    stanza[3],  # Max pazienti (originale)
                    0,  # Pazienti attuali (default)
                    0  # Posti liberi di default
                ))
    

    
    def seleziona_stanza(self, event):
        """Gestisce la selezione di una stanza"""
        selection = self.tree_stanze.selection()
        if selection:
            item = self.tree_stanze.item(selection[0])
            values = item['values']
            
            # Popola i campi di modifica
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, values[1])  # Nome stanza
            self.max_pazienti_entry.delete(0, tk.END)
            self.max_pazienti_entry.insert(0, values[2])  # Max pazienti
            
            # Carica i pazienti della stanza
            self.stanza_selezionata = values[0]  # ID stanza
            self.pazienti_label.config(text=f"👥 PAZIENTI DELLA STANZA: {values[1]}")
            self.carica_pazienti_stanza(self.stanza_selezionata)
    
    def carica_pazienti_stanza(self, stanza_id):
        """Carica i pazienti di una stanza specifica"""
        # Pulisce la lista pazienti
        for item in self.tree_pazienti.get_children():
            self.tree_pazienti.delete(item)
        
        # Ottieni tutti i pazienti del reparto
        pazienti = self.db_manager.get_pazienti_reparto(self.reparto)
        
        # Filtra per stanza
        for paziente in pazienti:
            if paziente[5] == stanza_id:  # stanza_id è alla posizione 5
                # Verifica se ha una scheda clinica
                scheda_clinica = self.db_manager.get_scheda_clinica(paziente[0])
                has_scheda = "✅" if scheda_clinica else "❌"
                
                self.tree_pazienti.insert('', 'end', values=(
                    paziente[0],  # ID
                    paziente[1],  # Nome
                    paziente[2],  # Cognome
                    paziente[3],  # Codice Fiscale
                    paziente[4],  # Data Nascita
                    has_scheda
                ))
    
    def apri_scheda_clinica(self, event):
        """Apre la scheda clinica del paziente selezionato"""
        selection = self.tree_pazienti.selection()
        if selection:
            item = self.tree_pazienti.item(selection[0])
            values = item['values']
            paziente_id = values[0]
            nome = values[1]
            cognome = values[2]
            
            # Apri la finestra della scheda clinica
            SchedaClinicaWindow(self.window, self.db_manager, paziente_id, nome, cognome)
    
    def aggiungi_stanza(self):
        """Aggiunge una nuova stanza"""
        nome = self.nome_entry.get().strip()
        max_pazienti = self.max_pazienti_entry.get().strip()
        
        if not nome or not max_pazienti:
            messagebox.showerror("Errore", "Inserisci tutti i campi")
            return
        
        try:
            max_pazienti = int(max_pazienti)
            if max_pazienti <= 0:
                messagebox.showerror("Errore", "Il numero massimo di pazienti deve essere positivo")
                return
        except ValueError:
            messagebox.showerror("Errore", "Il numero massimo di pazienti deve essere un numero")
            return
        
        # Inserisci nel database
        self.db_manager.inserisci_stanza(nome, self.reparto, max_pazienti)
        
        # Ricarica la lista
        self.carica_stanze()
        self.pulisci_campi()
        messagebox.showinfo("Successo", "Stanza aggiunta con successo")
    
    def modifica_stanza(self):
        """Modifica la stanza selezionata"""
        selection = self.tree_stanze.selection()
        if not selection:
            messagebox.showerror("Errore", "Seleziona una stanza da modificare")
            return
        
        item = self.tree_stanze.item(selection[0])
        values = item['values']
        stanza_id = values[0]
        
        nome = self.nome_entry.get().strip()
        max_pazienti = self.max_pazienti_entry.get().strip()
        
        if not nome or not max_pazienti:
            messagebox.showerror("Errore", "Inserisci tutti i campi")
            return
        
        try:
            max_pazienti = int(max_pazienti)
            if max_pazienti <= 0:
                messagebox.showerror("Errore", "Il numero massimo di pazienti deve essere positivo")
                return
        except ValueError:
            messagebox.showerror("Errore", "Il numero massimo di pazienti deve essere un numero")
            return
        
        # Verifica che non ci siano più pazienti del nuovo massimo
        try:
            pazienti_attuali = int(values[3])  # Pazienti attuali nel Treeview
        except (ValueError, TypeError):
            pazienti_attuali = 0
        
        if max_pazienti < pazienti_attuali:
            messagebox.showerror("Errore", f"Non puoi ridurre la capacità a {max_pazienti} perché ci sono già {pazienti_attuali} pazienti")
            return
        
        # Aggiorna nel database
        self.db_manager.aggiorna_stanza(stanza_id, nome, max_pazienti)
        
        # Ricarica la lista
        self.carica_stanze()
        self.pulisci_campi()
        messagebox.showinfo("Successo", "Stanza modificata con successo")
    
    def elimina_stanza(self):
        """Elimina la stanza selezionata"""
        selection = self.tree_stanze.selection()
        if not selection:
            messagebox.showerror("Errore", "Seleziona una stanza da eliminare")
            return
        
        item = self.tree_stanze.item(selection[0])
        values = item['values']
        stanza_id = values[0]
        
        # Verifica che non ci siano pazienti
        try:
            pazienti_attuali = int(values[3])  # Pazienti attuali nel Treeview
        except (ValueError, TypeError):
            pazienti_attuali = 0
        
        if pazienti_attuali > 0:
            messagebox.showerror("Errore", "Non puoi eliminare una stanza che contiene pazienti")
            return
        
        # Conferma eliminazione
        if messagebox.askyesno("Conferma", "Sei sicuro di voler eliminare questa stanza?"):
            self.db_manager.elimina_stanza(stanza_id)
            self.carica_stanze()
            self.pulisci_campi()
            messagebox.showinfo("Successo", "Stanza eliminata con successo")
    
    def pulisci_campi(self):
        """Pulisce i campi di inserimento"""
        self.nome_entry.delete(0, tk.END)
        self.max_pazienti_entry.delete(0, tk.END)
        self.stanza_selezionata = None
        self.pazienti_label.config(text="👥 PAZIENTI DELLA STANZA:")
        
        # Pulisce la lista pazienti
        for item in self.tree_pazienti.get_children():
            self.tree_pazienti.delete(item) 