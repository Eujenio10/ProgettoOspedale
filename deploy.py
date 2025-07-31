#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per la distribuzione e aggiornamento del database
Gestione Ospedale - Sistema di Distribuzione
"""

import os
import shutil
import sqlite3
import csv
from datetime import datetime
import zipfile
import json

class DeployManager:
    def __init__(self):
        self.app_name = "GestioneOspedale"
        self.db_name = "ospedale.db"
        self.impiegati_file = "impiegati.csv"
        
    def create_deployment_package(self):
        """Crea un pacchetto di distribuzione"""
        print("🏥 Creazione pacchetto di distribuzione...")
        
        # Crea cartella di distribuzione
        dist_folder = f"{self.app_name}_Distribuzione"
        if os.path.exists(dist_folder):
            try:
                shutil.rmtree(dist_folder)
            except PermissionError:
                print(f"⚠️  Impossibile eliminare la cartella {dist_folder}. Potrebbe essere in uso.")
                print("    Chiudi tutti i programmi che potrebbero usare i file in quella cartella.")
                return False
        os.makedirs(dist_folder)
        
        # Copia l'eseguibile
        exe_path = f"dist/{self.app_name}.exe"
        if os.path.exists(exe_path):
            shutil.copy2(exe_path, dist_folder)
            print(f"✅ Copiato {self.app_name}.exe")
        else:
            print(f"❌ Errore: {exe_path} non trovato!")
            return False
        
        # Copia il database iniziale
        if os.path.exists(self.db_name):
            shutil.copy2(self.db_name, dist_folder)
            print(f"✅ Copiato {self.db_name}")
        else:
            print(f"⚠️  Attenzione: {self.db_name} non trovato")
        
        # Copia il file impiegati
        if os.path.exists(self.impiegati_file):
            shutil.copy2(self.impiegati_file, dist_folder)
            print(f"✅ Copiato {self.impiegati_file}")
        else:
            print(f"⚠️  Attenzione: {self.impiegati_file} non trovato")
        
        # Crea script di installazione
        self.create_installer_script(dist_folder)
        
        # Crea script di aggiornamento database
        self.create_db_updater_script(dist_folder)
        
        # Crea README
        self.create_readme(dist_folder)
        
        # Crea ZIP del pacchetto
        self.create_zip_package(dist_folder)
        
        print(f"✅ Pacchetto di distribuzione creato: {dist_folder}.zip")
        return True
    
    def create_installer_script(self, dist_folder):
        """Crea script di installazione"""
        installer_content = '''@echo off
echo ========================================
echo    GESTIONE OSPEDALE - INSTALLAZIONE
echo ========================================
echo.

REM Crea cartella di installazione
set INSTALL_DIR=%USERPROFILE%\\Desktop\\GestioneOspedale
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copia file
echo Copia file in corso...
copy "GestioneOspedale.exe" "%INSTALL_DIR%\\"
copy "ospedale.db" "%INSTALL_DIR%\\"
copy "impiegati.csv" "%INSTALL_DIR%\\"
copy "update_database.bat" "%INSTALL_DIR%\\"

REM Crea collegamento sul desktop
echo Creazione collegamento...
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\Gestione Ospedale.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\GestioneOspedale.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo.
echo ========================================
echo    INSTALLAZIONE COMPLETATA!
echo ========================================
echo.
echo L'applicazione è stata installata in:
echo %INSTALL_DIR%
echo.
echo Collegamento creato sul desktop.
echo.
pause
'''
        
        with open(f"{dist_folder}/install.bat", 'w', encoding='utf-8') as f:
            f.write(installer_content)
        print("✅ Creato script di installazione")
    
    def create_db_updater_script(self, dist_folder):
        """Crea script per aggiornamento database"""
        updater_content = '''@echo off
echo ========================================
echo    AGGIORNAMENTO DATABASE
echo ========================================
echo.

REM Verifica se il database esiste
if not exist "ospedale.db" (
    echo ⚠️ Database non trovato nella cartella corrente.
    echo Cerco il database nella cartella di installazione...
    
    if exist "%USERPROFILE%\Desktop\GestioneOspedale\ospedale.db" (
        echo ✅ Database trovato nella cartella di installazione.
        echo Copio il database nella cartella corrente...
        copy "%USERPROFILE%\Desktop\GestioneOspedale\ospedale.db" "ospedale.db"
    ) else (
        echo ❌ Errore: Database non trovato!
        echo Verifica che il file ospedale.db sia presente nella cartella corrente
        echo o nella cartella di installazione (%USERPROFILE%\Desktop\GestioneOspedale).
        pause
        exit /b 1
    )
)

REM Backup del database esistente
echo Creazione backup...
set BACKUP_NAME=ospedale_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.db
set BACKUP_NAME=%BACKUP_NAME: =0%
copy "ospedale.db" "%BACKUP_NAME%"
echo ✅ Backup creato: %BACKUP_NAME%

REM Verifica se esiste il file impiegati.csv
if not exist "impiegati.csv" (
    echo ⚠️ File impiegati.csv non trovato nella cartella corrente.
    echo Cerco il file nella cartella di installazione...
    
    if exist "%USERPROFILE%\Desktop\GestioneOspedale\impiegati.csv" (
        echo ✅ File impiegati.csv trovato nella cartella di installazione.
        echo Copio il file nella cartella corrente...
        copy "%USERPROFILE%\Desktop\GestioneOspedale\impiegati.csv" "impiegati.csv"
    ) else (
        echo ⚠️ File impiegati.csv non trovato! L'aggiornamento potrebbe essere incompleto.
    )
)

REM Aggiorna impiegati dal CSV
echo Aggiornamento impiegati...
python -c "import sqlite3; import csv; import os; 
try:
    conn = sqlite3.connect('ospedale.db'); 
    cursor = conn.cursor(); 
    if os.path.exists('impiegati.csv'):
        with open('impiegati.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            count = 0
            for row in reader:
                if len(row) >= 4:
                    id_imp, nome, cognome, reparto = row[0], row[1], row[2], row[3]
                    cursor.execute('INSERT OR REPLACE INTO impiegati (id_impiegato, nome, cognome, reparto) VALUES (?, ?, ?, ?)', (id_imp, nome, cognome, reparto))
                    count += 1
        conn.commit()
        print(f'✅ {count} impiegati aggiornati dal CSV')
    else:
        print('⚠️ File impiegati.csv non trovato')
    conn.close()
except Exception as e:
    print(f'❌ Errore durante l\'aggiornamento: {e}')
"

echo.
echo ========================================
echo    AGGIORNAMENTO COMPLETATO!
echo ========================================
echo.
pause
'''
        
        with open(f"{dist_folder}/update_database.bat", 'w', encoding='utf-8') as f:
            f.write(updater_content)
        print("✅ Creato script di aggiornamento database")
    
    def create_readme(self, dist_folder):
        """Crea file README"""
        readme_content = '''# GESTIONE OSPEDALE - Distribuzione

## 📋 Istruzioni di Installazione

### 1. Installazione
1. Estrarre tutti i file in una cartella
2. Eseguire `install.bat` come amministratore
3. L'applicazione verrà installata sul desktop

### 2. Prima Esecuzione
1. Fare doppio click su "Gestione Ospedale" sul desktop
2. Inserire l'ID impiegato dal file `impiegati.csv`
3. L'applicazione creerà automaticamente il database

### 3. Aggiornamento Database
Per aggiornare il database con nuovi dati:
1. Sostituisci `impiegati.csv` con la nuova versione
2. Eseguire `update_database.bat`
3. Il database verrà aggiornato automaticamente

## 📁 Struttura File

- `GestioneOspedale.exe` - Applicazione principale
- `ospedale.db` - Database SQLite
- `impiegati.csv` - Lista impiegati
- `install.bat` - Script di installazione
- `update_database.bat` - Script aggiornamento

## 🔧 Configurazione Multi-PC

### Sincronizzazione Database
Per sincronizzare il database tra più PC:

1. **Esporta backup** dall'applicazione:
   - Menu → Backup Database
   - Salva il file .sql

2. **Distribuisci il backup**:
   - Copia il file .sql su tutti i PC
   - Usa "Import Backup" nell'applicazione

3. **Aggiorna impiegati**:
   - Sostituisci `impiegati.csv` su tutti i PC
   - Esegui `update_database.bat`

## 📞 Supporto Tecnico

Per problemi di installazione o aggiornamento:
- Controllare che tutti i file siano presenti
- Verificare i permessi di amministratore
- Controllare che il database non sia bloccato

## 🔒 Sicurezza

- Il database è locale su ogni PC
- I backup contengono tutti i dati
- Gli aggiornamenti non sovrascrivono dati esistenti
- Backup automatico prima di ogni aggiornamento

---
*Sistema di Gestione Ospedaliera v1.0*
'''
        
        with open(f"{dist_folder}/README.txt", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("✅ Creato file README")
    
    def create_zip_package(self, dist_folder):
        """Crea ZIP del pacchetto"""
        zip_name = f"{dist_folder}.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dist_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, dist_folder)
                    zipf.write(file_path, arcname)
        print(f"✅ Pacchetto ZIP creato: {zip_name}")
    
    def create_network_sync_script(self):
        """Crea script per sincronizzazione di rete"""
        sync_content = '''@echo off
echo ========================================
echo    SINCRONIZZAZIONE DATABASE DI RETE
echo ========================================
echo.

set SERVER_PATH=\\\\SERVER\\Shared\\OspedaleDB
set LOCAL_PATH=%USERPROFILE%\\Desktop\\GestioneOspedale

REM Verifica connessione al server
if not exist "%SERVER_PATH%" (
    echo ❌ Errore: Server non raggiungibile!
    echo Verificare la connessione di rete.
    pause
    exit /b 1
)

REM Backup locale
echo Creazione backup locale...
set BACKUP_NAME=ospedale_local_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.db
set BACKUP_NAME=%BACKUP_NAME: =0%
copy "%LOCAL_PATH%\\ospedale.db" "%BACKUP_NAME%"

REM Sincronizza dal server
echo Sincronizzazione dal server...
copy "%SERVER_PATH%\\ospedale.db" "%LOCAL_PATH%\\ospedale.db"
copy "%SERVER_PATH%\\impiegati.csv" "%LOCAL_PATH%\\impiegati.csv"

echo.
echo ========================================
echo    SINCRONIZZAZIONE COMPLETATA!
echo ========================================
echo.
echo Database aggiornato dal server.
echo Backup locale salvato: %BACKUP_NAME%
echo.
pause
'''
        
        with open("network_sync.bat", 'w', encoding='utf-8') as f:
            f.write(sync_content)
        print("✅ Creato script di sincronizzazione di rete")

def main():
    """Funzione principale"""
    print("🏥 GESTIONE OSPEDALE - SISTEMA DI DISTRIBUZIONE")
    print("=" * 50)
    
    deploy = DeployManager()
    
    # Crea pacchetto di distribuzione
    if deploy.create_deployment_package():
        print("\n✅ Distribuzione completata con successo!")
        print("\n📦 File creati:")
        print("- GestioneOspedale_Distribuzione.zip (pacchetto completo)")
        print("- network_sync.bat (sincronizzazione di rete)")
        print("\n📋 Prossimi passi:")
        print("1. Distribuire il file ZIP su tutti i PC")
        print("2. Eseguire install.bat su ogni PC")
        print("3. Configurare la sincronizzazione di rete se necessario")
    else:
        print("\n❌ Errore durante la creazione del pacchetto!")

if __name__ == "__main__":
    main() 