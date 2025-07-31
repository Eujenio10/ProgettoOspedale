import sqlite3
import os
from datetime import datetime
from tkinter import messagebox

class ActivityLogger:
    def __init__(self, db_path="ospedale.db"):
        """Inizializza il sistema di logging"""
        self.db_path = db_path
        self.create_log_table()
    
    def create_log_table(self):
        """Crea la tabella per i log se non esiste"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                user_name TEXT,
                user_reparto TEXT,
                action_type TEXT,
                action_description TEXT,
                target_table TEXT,
                target_id INTEGER,
                details TEXT,
                ip_address TEXT DEFAULT 'localhost'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_activity(self, user_id, user_name, user_reparto, action_type, action_description, 
                    target_table=None, target_id=None, details=None):
        """Registra un'attività nel log"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO activity_log 
                (user_id, user_name, user_reparto, action_type, action_description, 
                 target_table, target_id, details)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, user_name, user_reparto, action_type, action_description,
                  target_table, target_id, details))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nel logging: {e}")
            return False
    
    def log_login(self, user_id, user_name, user_reparto, success=True):
        """Log per il login"""
        action_type = "LOGIN_SUCCESS" if success else "LOGIN_FAILED"
        description = f"Accesso al sistema - Reparto: {user_reparto}"
        if not success:
            description = f"Tentativo di accesso fallito per ID: {user_id}"
        
        self.log_activity(user_id, user_name, user_reparto, action_type, description)
    
    def log_logout(self, user_id, user_name, user_reparto):
        """Log per il logout"""
        action_type = "LOGOUT"
        description = f"Logout dal sistema"
        self.log_activity(user_id, user_name, user_reparto, action_type, description)
    
    def log_patient_action(self, user_id, user_name, user_reparto, action, patient_id, 
                          patient_name, patient_surname, details=None):
        """Log per le operazioni sui pazienti"""
        action_type = f"PATIENT_{action.upper()}"
        description = f"Paziente: {patient_name} {patient_surname}"
        
        self.log_activity(user_id, user_name, user_reparto, action_type, description,
                         "pazienti", patient_id, details)
    
    def log_room_action(self, user_id, user_name, user_reparto, action, room_id, 
                       room_name, details=None):
        """Log per le operazioni sulle stanze"""
        action_type = f"ROOM_{action.upper()}"
        description = f"Stanza: {room_name}"
        
        self.log_activity(user_id, user_name, user_reparto, action_type, description,
                         "stanze", room_id, details)
    
    def log_clinical_record_access(self, user_id, user_name, user_reparto, patient_id, 
                                  patient_name, patient_surname):
        """Log per l'accesso alle schede cliniche"""
        action_type = "CLINICAL_RECORD_ACCESS"
        description = f"Accesso scheda clinica - Paziente: {patient_name} {patient_surname}"
        
        self.log_activity(user_id, user_name, user_reparto, action_type, description,
                         "schede_cliniche", patient_id)
    
    def log_clinical_record_update(self, user_id, user_name, user_reparto, patient_id, 
                                 patient_name, patient_surname, details=None):
        """Log per l'aggiornamento delle schede cliniche"""
        action_type = "CLINICAL_RECORD_UPDATE"
        description = f"Aggiornamento scheda clinica - Paziente: {patient_name} {patient_surname}"
        
        self.log_activity(user_id, user_name, user_reparto, action_type, description,
                         "schede_cliniche", patient_id, details)
    
    def get_user_activity(self, user_id=None, start_date=None, end_date=None, action_type=None):
        """Ottiene l'attività di un utente o tutti gli utenti"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM activity_log WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if start_date:
            query += " AND date(timestamp) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date(timestamp) <= ?"
            params.append(end_date)
        
        if action_type:
            query += " AND action_type = ?"
            params.append(action_type)
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_recent_activity(self, limit=50):
        """Ottiene le attività recenti"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM activity_log 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_activity_summary(self):
        """Ottiene un riassunto delle attività"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conteggio per tipo di azione
        cursor.execute('''
            SELECT action_type, COUNT(*) as count 
            FROM activity_log 
            GROUP BY action_type 
            ORDER BY count DESC
        ''')
        action_summary = cursor.fetchall()
        
        # Conteggio per utente
        cursor.execute('''
            SELECT user_name, COUNT(*) as count 
            FROM activity_log 
            GROUP BY user_name 
            ORDER BY count DESC
        ''')
        user_summary = cursor.fetchall()
        
        # Conteggio per reparto
        cursor.execute('''
            SELECT user_reparto, COUNT(*) as count 
            FROM activity_log 
            GROUP BY user_reparto 
            ORDER BY count DESC
        ''')
        reparto_summary = cursor.fetchall()
        
        conn.close()
        
        return {
            'action_summary': action_summary,
            'user_summary': user_summary,
            'reparto_summary': reparto_summary
        }
    
    def export_log_to_csv(self, filename="activity_log.csv"):
        """Esporta il log in formato CSV"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, user_id, user_name, user_reparto, action_type, 
                       action_description, target_table, target_id, details
                FROM activity_log 
                ORDER BY timestamp DESC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Timestamp,User ID,User Name,Reparto,Action Type,Description,Target Table,Target ID,Details\n")
                for row in results:
                    # Escape delle virgole nei campi
                    escaped_row = [str(field).replace(',', ';').replace('"', '""') if field else '' for field in row]
                    f.write(','.join(f'"{field}"' for field in escaped_row) + '\n')
            
            return True
        except Exception as e:
            print(f"Errore nell'esportazione: {e}")
            return False

# Istanza globale del logger
activity_logger = ActivityLogger() 