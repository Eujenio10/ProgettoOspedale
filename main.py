#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GESTIONE OSPEDALE - Applicazione Desktop
Sviluppato con Python e Tkinter

Autore: Sistema di Gestione Ospedaliera
Versione: 1.0
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import traceback

# Importa i moduli dell'applicazione
try:
    from database import DatabaseManager
    from login import LoginWindow
    from dashboard import DashboardWindow
except ImportError as e:
    print(f"Errore di importazione: {e}")
    sys.exit(1)

class GestioneOspedaleApp:
    def __init__(self):
        """Inizializza l'applicazione principale"""
        try:
            # Crea la finestra principale
            self.root = tk.Tk()
            self.root.title("Gestione Ospedale v1.0")
            self.root.geometry("400x300")
            self.root.resizable(False, False)
            self.root.configure(bg='#2c3e50')
            
            # Centra la finestra
            self.center_window()
            
            # Inizializza il database
            print("Inizializzazione database...")
            self.db_manager = DatabaseManager()
            print("Database inizializzato con successo")
            
            # Crea l'interfaccia di benvenuto
            self.create_welcome_screen()
            
        except Exception as e:
            print(f"Errore durante l'inizializzazione: {e}")
            traceback.print_exc()
            raise
        
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_welcome_screen(self):
        """Crea la schermata di benvenuto"""
        # Frame principale
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Logo/Titolo
        title_label = tk.Label(main_frame, 
                              text="🏥\nGESTIONE OSPEDALE",
                              font=('Arial', 24, 'bold'),
                              bg='#2c3e50', fg='white')
        title_label.pack(pady=(0, 30))
        
        # Sottotitolo
        subtitle_label = tk.Label(main_frame,
                                 text="Sistema di Gestione Ospedaliera",
                                 font=('Arial', 12),
                                 bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack(pady=(0, 40))
        
        # Pulsante di avvio
        start_btn = tk.Button(main_frame, text="AVVIA APPLICAZIONE",
                             command=self.start_application,
                             font=('Arial', 14, 'bold'),
                             bg='#3498db', fg='white',
                             width=20, height=2,
                             relief='flat')
        start_btn.pack(pady=(0, 20))
        
        # Informazioni versione
        version_label = tk.Label(main_frame,
                                text="Versione 1.0 - Python + Tkinter + SQLite",
                                font=('Arial', 10),
                                bg='#2c3e50', fg='#95a5a6')
        version_label.pack(side='bottom')
        
        # Binding per chiusura
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def start_application(self):
        """Avvia l'applicazione principale"""
        try:
            print("Avvio applicazione...")
            
            # Nasconde la finestra principale
            self.root.withdraw()
            print("Finestra principale nascosta")
            
            # Apre la finestra di login
            print("Creazione finestra di login...")
            login_window = LoginWindow(self.root, self.db_manager)
            print("Finestra di login creata")
            
            # Assicura che la finestra di login sia visibile
            login_window.window.deiconify()
            login_window.window.lift()
            login_window.window.focus_force()
            print("Finestra di login resa visibile")
            
            # Aspetta che la finestra di login si chiuda
            print("Attendo chiusura finestra di login...")
            self.root.wait_window(login_window.window)
            print("Finestra di login chiusa")
            
            # Controlla se il login è stato effettuato
            impiegato_loggato = login_window.get_impiegato_loggato()
            print(f"Impiegato loggato: {impiegato_loggato}")
            
            if impiegato_loggato:
                # Apre la dashboard
                print("Creazione dashboard...")
                dashboard = DashboardWindow(self.root, self.db_manager, impiegato_loggato)
                print("Dashboard creata")
                
                # Aspetta che la dashboard si chiuda
                print("Attendo chiusura dashboard...")
                self.root.wait_window(dashboard.window)
                print("Dashboard chiusa")
                
                # Torna alla schermata di benvenuto
                self.root.deiconify()
                print("Tornato alla schermata di benvenuto")
            else:
                # Torna alla schermata di benvenuto
                self.root.deiconify()
                print("Login annullato, tornato alla schermata di benvenuto")
                
        except Exception as e:
            print(f"Errore durante l'avvio dell'applicazione: {e}")
            traceback.print_exc()
            messagebox.showerror("Errore", f"Errore durante l'avvio dell'applicazione:\n{str(e)}")
            self.root.deiconify()
    
    def on_closing(self):
        """Gestisce la chiusura dell'applicazione"""
        if messagebox.askokcancel("Uscita", "Vuoi chiudere l'applicazione?"):
            try:
                # Chiudi tutte le connessioni al database
                self.db_manager.close_all_connections()
            except:
                pass
            self.root.destroy()
            sys.exit()

def main():
    """Funzione principale dell'applicazione"""
    try:
        print("Avvio applicazione Gestione Ospedale...")
        # Crea e avvia l'applicazione
        app = GestioneOspedaleApp()
        print("Applicazione creata, avvio mainloop...")
        app.root.mainloop()
    except Exception as e:
        print(f"Errore fatale: {e}")
        traceback.print_exc()
        messagebox.showerror("Errore", f"Errore durante l'avvio dell'applicazione:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 