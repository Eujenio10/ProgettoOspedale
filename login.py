import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
from logger import activity_logger

class LoginWindow:
    def __init__(self, parent, db_manager):
        """Inizializza la finestra di login"""
        self.parent = parent
        self.db_manager = db_manager
        self.impiegato_loggato = None
        
        # Configurazione finestra
        self.window = tk.Toplevel(parent)
        self.window.title("Login - Gestione Ospedale")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.configure(bg='#f0f0f0')
        
        # Centra la finestra
        self.center_window()
        self.window.transient(parent)
        self.window.grab_set()
        
        # Assicura che la finestra sia in primo piano
        self.window.lift()
        self.window.focus_force()
        
        self.create_widgets()
        
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Crea i widget dell'interfaccia di login"""
        # Frame principale
        main_frame = tk.Frame(self.window, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titolo
        title_label = tk.Label(main_frame, text="ACCESSO SISTEMA", 
                              font=('Arial', 16, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Frame per il form
        form_frame = tk.Frame(main_frame, bg='#f0f0f0')
        form_frame.pack(expand=True)
        
        # ID Impiegato
        tk.Label(form_frame, text="ID Impiegato:", 
                font=('Arial', 12), bg='#f0f0f0').pack(anchor='w', pady=(0, 5))
        
        self.id_entry = tk.Entry(form_frame, font=('Arial', 12), width=25)
        self.id_entry.pack(pady=(0, 15))
        self.id_entry.focus()
        
        # Pulsante Login
        login_btn = tk.Button(form_frame, text="ACCEDI", 
                             command=self.verifica_login,
                             font=('Arial', 12, 'bold'),
                             bg='#3498db', fg='white',
                             width=15, height=2,
                             relief='flat')
        login_btn.pack(pady=20)
        

        
        # Binding per Enter
        self.window.bind('<Return>', lambda e: self.verifica_login())
        
        # Assicura che la finestra sia visibile
        self.window.deiconify()
        
    def verifica_login(self):
        """Verifica le credenziali di login"""
        id_impiegato = self.id_entry.get().strip()
        
        if not id_impiegato:
            messagebox.showerror("Errore", "Inserire l'ID impiegato!")
            return
        
        # Verifica nel database
        result = self.db_manager.verifica_login(id_impiegato)
        
        if result:
            self.impiegato_loggato = {
                'id': result[0],
                'nome': result[1],
                'cognome': result[2],
                'reparto': result[3],
                'id_impiegato': id_impiegato
            }
            # Log del login riuscito
            activity_logger.log_login(
                user_id=id_impiegato,
                user_name=f"{result[1]} {result[2]}",
                user_reparto=result[3],
                success=True
            )
            messagebox.showinfo("Successo", f"Benvenuto {result[1]} {result[2]}!")
            self.window.destroy()
        else:
            # Log del tentativo di login fallito
            activity_logger.log_login(
                user_id=id_impiegato,
                user_name="",
                user_reparto="",
                success=False
            )
            messagebox.showerror("Errore", "ID impiegato non trovato!")
            self.id_entry.delete(0, tk.END)
            self.id_entry.focus()
    

    
    def get_impiegato_loggato(self):
        """Restituisce i dati dell'impiegato loggato"""
        return self.impiegato_loggato

 