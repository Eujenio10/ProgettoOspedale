import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
from stanze import GestioneStanzeWindow
from pazienti import GestionePazientiWindow
from datetime import datetime
from logger import activity_logger

class DashboardWindow:
    def __init__(self, parent, db_manager, impiegato):
        """Inizializza la dashboard principale"""
        self.parent = parent
        self.db_manager = db_manager
        self.impiegato = impiegato
        
        print(f"Creazione dashboard per {impiegato['nome']} {impiegato['cognome']} - {impiegato['reparto']}")
        
        # Configurazione finestra
        self.window = tk.Toplevel(parent)
        self.window.title(f"Dashboard - {impiegato['reparto']}")
        self.window.geometry("800x600")
        self.window.configure(bg='#ecf0f1')
        
        # Centra la finestra
        self.center_window()
        self.window.transient(parent)
        self.window.grab_set()
        
        # Assicura che la finestra sia visibile
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()
        
        # Binding per la chiusura della finestra
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.create_widgets()
        print("Dashboard creata e configurata")
        
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def on_closing(self):
        """Gestisce la chiusura della finestra"""
        print("Tentativo di chiusura dashboard")
        if messagebox.askyesno("Logout", "Vuoi effettuare il logout?"):
            print("Logout confermato")
            self.window.destroy()
            self.parent.deiconify()
        else:
            print("Logout annullato")
        
    def create_widgets(self):
        """Crea i widget della dashboard"""
        print("Creazione widget dashboard...")
        
        # Header
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Informazioni impiegato
        impiegato_info = tk.Label(header_frame, 
                                 text=f"Impiegato: {self.impiegato['nome']} {self.impiegato['cognome']}",
                                 font=('Arial', 14, 'bold'),
                                 bg='#2c3e50', fg='white')
        impiegato_info.pack(side='left', padx=20, pady=20)
        
        # Reparto
        reparto_info = tk.Label(header_frame,
                               text=f"Reparto: {self.impiegato['reparto']}",
                               font=('Arial', 12),
                               bg='#2c3e50', fg='#bdc3c7')
        reparto_info.pack(side='left', padx=(20, 0), pady=20)
        
        # Pulsante logout
        logout_btn = tk.Button(header_frame, text="LOGOUT",
                              command=self.logout,
                              font=('Arial', 10, 'bold'),
                              bg='#e74c3c', fg='white',
                              relief='flat', width=10)
        logout_btn.pack(side='right', padx=20, pady=20)
        
        # Contenuto principale
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titolo
        title_label = tk.Label(main_frame, 
                              text=f"GESTIONE REPARTO {self.impiegato['reparto'].upper()}",
                              font=('Arial', 18, 'bold'),
                              bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=(0, 30))
        
        # Frame per i pulsanti
        buttons_frame = tk.Frame(main_frame, bg='#ecf0f1')
        buttons_frame.pack(expand=True)
        
        # Griglia di pulsanti
        self.create_menu_buttons(buttons_frame)
        
        print("Widget dashboard creati")
        
    def create_menu_buttons(self, parent):
        """Crea i pulsanti del menu principale"""
        print("Creazione pulsanti menu...")
        
        # Configurazione griglia
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_columnconfigure(3, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        
        # Pulsante Gestione Stanze
        stanze_btn = tk.Button(parent, text="🏥\nGESTIONE STANZE",
                               command=self.apri_gestione_stanze,
                               font=('Arial', 16, 'bold'),
                               bg='#3498db', fg='white',
                               width=20, height=6,
                               relief='flat')
        stanze_btn.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')
        
        # Pulsante Gestione Pazienti
        pazienti_btn = tk.Button(parent, text="👥\nGESTIONE PAZIENTI",
                                command=self.apri_gestione_pazienti,
                                font=('Arial', 16, 'bold'),
                                bg='#27ae60', fg='white',
                                width=20, height=6,
                                relief='flat')
        pazienti_btn.grid(row=0, column=1, padx=15, pady=15, sticky='nsew')
        
        # Pulsante Backup
        backup_btn = tk.Button(parent, text="💾\nBACKUP DATABASE",
                              command=self.esporta_backup,
                              font=('Arial', 16, 'bold'),
                              bg='#f39c12', fg='white',
                              width=20, height=6,
                              relief='flat')
        backup_btn.grid(row=0, column=2, padx=15, pady=15, sticky='nsew')
        
        # Pulsante Import Backup
        import_btn = tk.Button(parent, text="📥\nIMPORT BACKUP",
                              command=self.importa_backup,
                              font=('Arial', 16, 'bold'),
                              bg='#e67e22', fg='white',
                              width=20, height=6,
                              relief='flat')
        import_btn.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')
        
        # Pulsante Export CSV
        csv_btn = tk.Button(parent, text="📊\nEXPORT CSV",
                           command=self.esporta_backup_csv,
                           font=('Arial', 16, 'bold'),
                           bg='#16a085', fg='white',
                           width=20, height=6,
                           relief='flat')
        csv_btn.grid(row=1, column=1, padx=15, pady=15, sticky='nsew')
        
        # Pulsante Statistiche
        stats_btn = tk.Button(parent, text="📊\nSTATISTICHE",
                             command=self.mostra_statistiche,
                             font=('Arial', 16, 'bold'),
                             bg='#9b59b6', fg='white',
                             width=20, height=6,
                             relief='flat')
        stats_btn.grid(row=1, column=2, padx=15, pady=15, sticky='nsew')
        

        
        # Pulsante Log Attività
        log_btn = tk.Button(parent, text="📊\nLOG ATTIVITÀ",
                           command=self.apri_log_attivita,
                           font=('Arial', 16, 'bold'),
                           bg='#e74c3c', fg='white',
                           width=20, height=6,
                           relief='flat')
        log_btn.grid(row=2, column=1, padx=15, pady=15, sticky='nsew')
        
        print("Pulsanti menu creati")
    

    
    def apri_gestione_stanze(self):
        """Apre la finestra di gestione stanze"""
        print("Apertura gestione stanze...")
        GestioneStanzeWindow(self.window, self.db_manager, self.impiegato['reparto'])
    
    def apri_gestione_pazienti(self):
        """Apre la finestra di gestione pazienti"""
        print("Apertura gestione pazienti...")
        GestionePazientiWindow(self.window, self.db_manager, self.impiegato['reparto'], self.impiegato)
    
    def apri_log_attivita(self):
        """Apre la finestra di visualizzazione log attività"""
        print("Apertura visualizzatore log attività...")
        from log_viewer import LogViewerWindow
        LogViewerWindow(self.window, self.impiegato)
    
    def esporta_backup(self):
        """Esporta un backup del database"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".sql",
                filetypes=[("SQL files", "*.sql"), ("All files", "*.*")],
                title="Salva backup database"
            )
            
            if filename:
                self.db_manager.export_backup(filename)
                messagebox.showinfo("Successo", f"Backup salvato in: {filename}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il backup: {str(e)}")
    
    def importa_backup(self):
        """Importa un backup del database"""
        try:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                filetypes=[("SQL files", "*.sql"), ("All files", "*.*")],
                title="Seleziona file di backup da importare"
            )
            
            if filename:
                success, message = self.db_manager.import_backup(filename)
                if success:
                    messagebox.showinfo("Successo", message)
                    # Ricarica le statistiche
                    self.update_statistics(self.window)
                else:
                    messagebox.showerror("Errore", message)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'import: {str(e)}")
    
    def esporta_backup_csv(self):
        """Esporta un backup in formato CSV"""
        try:
            from tkinter import filedialog
            directory = filedialog.askdirectory(
                title="Seleziona cartella per salvare backup CSV"
            )
            
            if directory:
                success, message = self.db_manager.export_csv_backup(directory)
                if success:
                    messagebox.showinfo("Successo", message)
                else:
                    messagebox.showerror("Errore", message)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'export CSV: {str(e)}")
    
    def mostra_statistiche(self):
        """Mostra statistiche dettagliate"""
        # Ottieni dati
        stanze = self.db_manager.get_stanze_reparto(self.impiegato['reparto'])
        pazienti = self.db_manager.get_pazienti_reparto(self.impiegato['reparto'])
        
        # Calcola statistiche
        num_stanze = len(stanze)
        num_pazienti = len(pazienti)
        
        posti_totali = 0
        posti_occupati = 0
        
        for stanza in stanze:
            try:
                max_pazienti = int(stanza[3])  # max_pazienti è alla posizione 3
                pazienti_attuali = int(stanza[5])  # pazienti_attuali è alla posizione 5
                posti_totali += max_pazienti
                posti_occupati += pazienti_attuali
            except (ValueError, TypeError) as e:
                print(f"Errore nel calcolo statistiche per stanza {stanza[1]}: {e}")
        
        posti_liberi = posti_totali - posti_occupati
        percentuale_occupazione = (posti_occupati / max(posti_totali, 1)) * 100
        
        # Crea finestra statistiche
        stats_window = tk.Toplevel(self.window)
        stats_window.title("Statistiche Dettagliate")
        stats_window.geometry("500x400")
        stats_window.configure(bg='#ecf0f1')
        
        # Contenuto statistiche
        tk.Label(stats_window, text="STATISTICHE DETTAGLIATE",
                font=('Arial', 16, 'bold'),
                bg='#ecf0f1').pack(pady=20)
        
        stats_text = f"""
        REPARTO: {self.impiegato['reparto']}
        
        STANZE:
        - Numero totale: {num_stanze}
        - Posti totali: {posti_totali}
        - Posti occupati: {posti_occupati}
        - Posti liberi: {posti_liberi}
        
        PAZIENTI:
        - Numero totale: {num_pazienti}
        - Ricoverati oggi: {len([p for p in pazienti if p[7].startswith(datetime.now().strftime('%Y-%m-%d'))])}
        
        UTILIZZO:
        - Percentuale occupazione: {percentuale_occupazione:.1f}%
        """
        
        tk.Label(stats_window, text=stats_text,
                font=('Arial', 11),
                bg='#ecf0f1', justify='left').pack(padx=20)
    

    
    def logout(self):
        """Effettua il logout"""
        print("Richiesta logout...")
        if messagebox.askyesno("Logout", "Vuoi effettuare il logout?"):
            print("Logout confermato")
            # Log del logout
            activity_logger.log_logout(
                user_id=self.impiegato['id_impiegato'],
                user_name=f"{self.impiegato['nome']} {self.impiegato['cognome']}",
                user_reparto=self.impiegato['reparto']
            )
            self.window.destroy()
            # Torna alla finestra di login
            self.parent.deiconify()
        else:
            print("Logout annullato") 