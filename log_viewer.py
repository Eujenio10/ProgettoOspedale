import tkinter as tk
from tkinter import ttk, messagebox
from logger import activity_logger
from datetime import datetime, timedelta
import csv

class LogViewerWindow:
    def __init__(self, parent, current_user):
        """Inizializza la finestra di visualizzazione log"""
        self.parent = parent
        self.current_user = current_user
        
        # Configurazione finestra
        self.window = tk.Toplevel(parent)
        self.window.title("Visualizzatore Log Attività")
        self.window.geometry("1200x700")
        self.window.configure(bg='#ecf0f1')
        
        # Centra la finestra
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.load_recent_activity()
        
    def create_widgets(self):
        """Crea i widget dell'interfaccia"""
        # Frame principale
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titolo
        title_label = tk.Label(main_frame, text="📊 VISUALIZZATORE LOG ATTIVITÀ", 
                              font=('Arial', 16, 'bold'), 
                              bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Frame per i filtri
        filter_frame = tk.Frame(main_frame, bg='#ecf0f1')
        filter_frame.pack(fill='x', pady=(0, 20))
        
        # Filtri
        tk.Label(filter_frame, text="Filtri:", bg='#ecf0f1', font=('Arial', 12, 'bold')).pack(side='left', padx=(0, 10))
        
        # Filtro per utente
        tk.Label(filter_frame, text="Utente:", bg='#ecf0f1').pack(side='left', padx=(0, 5))
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(filter_frame, textvariable=self.user_var, width=15)
        self.user_combo.pack(side='left', padx=(0, 10))
        
        # Filtro per tipo di azione
        tk.Label(filter_frame, text="Azione:", bg='#ecf0f1').pack(side='left', padx=(0, 5))
        self.action_var = tk.StringVar()
        self.action_combo = ttk.Combobox(filter_frame, textvariable=self.action_var, width=15)
        self.action_combo.pack(side='left', padx=(0, 10))
        
        # Filtro per data
        tk.Label(filter_frame, text="Data:", bg='#ecf0f1').pack(side='left', padx=(0, 5))
        self.date_var = tk.StringVar()
        self.date_combo = ttk.Combobox(filter_frame, textvariable=self.date_var, width=12)
        self.date_combo['values'] = ['Oggi', 'Ultimi 7 giorni', 'Ultimi 30 giorni', 'Tutti']
        self.date_combo.set('Tutti')
        self.date_combo.pack(side='left', padx=(0, 10))
        
        # Pulsanti
        tk.Button(filter_frame, text="🔍 Applica Filtri", command=self.apply_filters,
                 bg='#3498db', fg='white', relief='flat').pack(side='left', padx=(0, 10))
        tk.Button(filter_frame, text="🔄 Ricarica", command=self.load_recent_activity,
                 bg='#27ae60', fg='white', relief='flat').pack(side='left', padx=(0, 10))
        tk.Button(filter_frame, text="📊 Riassunto", command=self.show_summary,
                 bg='#f39c12', fg='white', relief='flat').pack(side='left', padx=(0, 10))
        tk.Button(filter_frame, text="📄 Esporta CSV", command=self.export_to_csv,
                 bg='#e74c3c', fg='white', relief='flat').pack(side='left')
        
        # Frame per la lista log
        list_frame = tk.Frame(main_frame, bg='#ecf0f1')
        list_frame.pack(expand=True, fill='both')
        
        # Treeview per i log
        columns = ('Timestamp', 'Utente', 'Reparto', 'Azione', 'Descrizione', 'Tabella', 'ID Target', 'Dettagli')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == 'Timestamp':
                self.tree.column(col, width=150)
            elif col == 'Utente':
                self.tree.column(col, width=100)
            elif col == 'Reparto':
                self.tree.column(col, width=100)
            elif col == 'Azione':
                self.tree.column(col, width=120)
            elif col == 'Descrizione':
                self.tree.column(col, width=200)
            elif col == 'Tabella':
                self.tree.column(col, width=80)
            elif col == 'ID Target':
                self.tree.column(col, width=80)
            else:
                self.tree.column(col, width=150)
        
        self.tree.pack(expand=True, fill='both', pady=(10, 0))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Popola i filtri
        self.populate_filters()
        
    def populate_filters(self):
        """Popola i filtri con i dati disponibili"""
        # Ottieni tutti gli utenti unici
        activities = activity_logger.get_recent_activity(1000)
        users = list(set([row[2] for row in activities if row[2]]))
        self.user_combo['values'] = ['Tutti'] + users
        
        # Ottieni tutti i tipi di azione unici
        actions = list(set([row[4] for row in activities if row[4]]))
        self.action_combo['values'] = ['Tutti'] + actions
        
    def load_recent_activity(self):
        """Carica le attività recenti"""
        self.clear_tree()
        activities = activity_logger.get_recent_activity(100)
        
        for activity in activities:
            self.tree.insert('', 'end', values=(
                activity[1],  # Timestamp
                activity[2],  # User Name
                activity[3],  # User Reparto
                activity[4],  # Action Type
                activity[5],  # Action Description
                activity[6] or '',  # Target Table
                activity[7] or '',  # Target ID
                activity[8] or ''   # Details
            ))
    
    def apply_filters(self):
        """Applica i filtri selezionati"""
        self.clear_tree()
        
        # Ottieni i parametri dei filtri
        user_filter = self.user_var.get()
        action_filter = self.action_var.get()
        date_filter = self.date_var.get()
        
        # Calcola le date per il filtro
        start_date = None
        end_date = None
        
        if date_filter == 'Oggi':
            start_date = datetime.now().strftime('%Y-%m-%d')
        elif date_filter == 'Ultimi 7 giorni':
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        elif date_filter == 'Ultimi 30 giorni':
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Ottieni le attività filtrate
        activities = activity_logger.get_user_activity(
            user_id=None if user_filter == 'Tutti' else user_filter,
            start_date=start_date,
            end_date=end_date,
            action_type=None if action_filter == 'Tutti' else action_filter
        )
        
        # Popola la treeview
        for activity in activities:
            self.tree.insert('', 'end', values=(
                activity[1],  # Timestamp
                activity[2],  # User Name
                activity[3],  # User Reparto
                activity[4],  # Action Type
                activity[5],  # Action Description
                activity[6] or '',  # Target Table
                activity[7] or '',  # Target ID
                activity[8] or ''   # Details
            ))
    
    def clear_tree(self):
        """Pulisce la treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def show_summary(self):
        """Mostra il riassunto delle attività"""
        summary = activity_logger.get_activity_summary()
        
        # Crea una nuova finestra per il riassunto
        summary_window = tk.Toplevel(self.window)
        summary_window.title("📊 Riassunto Attività")
        summary_window.geometry("600x500")
        summary_window.configure(bg='#ecf0f1')
        
        # Frame principale
        main_frame = tk.Frame(summary_window, bg='#ecf0f1')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titolo
        title_label = tk.Label(main_frame, text="📊 RIASSUNTO ATTIVITÀ", 
                              font=('Arial', 14, 'bold'), 
                              bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Notebook per le diverse sezioni
        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill='both')
        
        # Tab per tipo di azione
        action_frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(action_frame, text="Per Tipo di Azione")
        
        action_tree = ttk.Treeview(action_frame, columns=('Azione', 'Conteggio'), show='headings', height=10)
        action_tree.heading('Azione', text='Azione')
        action_tree.heading('Conteggio', text='Conteggio')
        action_tree.column('Azione', width=200)
        action_tree.column('Conteggio', width=100)
        action_tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        for action, count in summary['action_summary']:
            action_tree.insert('', 'end', values=(action, count))
        
        # Tab per utente
        user_frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(user_frame, text="Per Utente")
        
        user_tree = ttk.Treeview(user_frame, columns=('Utente', 'Conteggio'), show='headings', height=10)
        user_tree.heading('Utente', text='Utente')
        user_tree.heading('Conteggio', text='Conteggio')
        user_tree.column('Utente', width=200)
        user_tree.column('Conteggio', width=100)
        user_tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        for user, count in summary['user_summary']:
            user_tree.insert('', 'end', values=(user, count))
        
        # Tab per reparto
        reparto_frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(reparto_frame, text="Per Reparto")
        
        reparto_tree = ttk.Treeview(reparto_frame, columns=('Reparto', 'Conteggio'), show='headings', height=10)
        reparto_tree.heading('Reparto', text='Reparto')
        reparto_tree.heading('Conteggio', text='Conteggio')
        reparto_tree.column('Reparto', width=200)
        reparto_tree.column('Conteggio', width=100)
        reparto_tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        for reparto, count in summary['reparto_summary']:
            reparto_tree.insert('', 'end', values=(reparto, count))
    
    def export_to_csv(self):
        """Esporta i log in formato CSV"""
        try:
            filename = f"activity_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            success = activity_logger.export_log_to_csv(filename)
            
            if success:
                messagebox.showinfo("Successo", f"Log esportato con successo in {filename}")
            else:
                messagebox.showerror("Errore", "Errore durante l'esportazione del log")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'esportazione: {e}") 