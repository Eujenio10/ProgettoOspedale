# 🏥 Gestione Ospedale - Applicazione a cura di Eugenio Iandoli

Un'applicazione desktop multipiattaforma per la gestione di ospedali, sviluppata in Python con Tkinter e SQLite.

NOTA BENE : Per utilizzare semplicemente l'applicazione puoi scaricare il file .zip e seguirne le istruzioni all'interno per avviarlo.

📋 Caratteristiche

✅ Funzionalità Implementate

1. **🔐 Sistema di Login Sicuro**
   - Login con ID impiegato
   - Gestione impiegati tramite file CSV
   - Accesso controllato per reparto

2. **🏥 Gestione Stanze**
   - Aggiunta/modifica/eliminazione stanze
   - Controllo capacità massima
   - Prevenzione eliminazione stanze con pazienti

3. **👥 Gestione Pazienti**
   - Inserimento pazienti con dati completi
   - Assegnazione a stanze
   - Validazione dati (codice fiscale, date)
   - Controllo disponibilità posti

4. **📋 Schede Cliniche**
   - Diagnosi dettagliate
   - Terapie in corso
   - Farmaci somministrati
   - Esami eseguiti
   - Medico referente
   - Annotazioni aggiuntive

5. **📊 Dashboard e Statistiche**
   - Statistiche rapide del reparto
   - Monitoraggio occupazione stanze
   - Controllo numero pazienti

6. **💾 Backup e Sicurezza**
   - Esportazione backup database
   - Validazione dati inseriti
   - Prevenzione errori

🚀 Installazione

### Prerequisiti

- Python 3.7 o superiore
- Tkinter (incluso con Python)
- SQLite3 (incluso con Python)

Processo di Installazione

1. **Clona o scarica il progetto**
   ```bash
   git clone <repository-url>
   cd App-Ospedale
   ```

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inizializza il database con impiegati di default**
   ```bash
   py init_database.py
   ```

4. **Avvia l'applicazione**
   ```bash
   py main.py
   ```

## 🎯 Utilizzo

### Primo Avvio

1. **Inizializza il database** con `py init_database.py`
2. **Avvia l'applicazione** con `py main.py`
3. **Clicca "AVVIA APPLICAZIONE"**
4. **Inserisci uno degli ID impiegato** mostrati durante l'inizializzazione
5. **Clicca "ACCEDI"**

### Gestione Impiegati

#### Metodo 1: Inizializzazione Automatica
```bash
py init_database.py
```
Crea automaticamente 15 impiegati di default per tutti i reparti.

#### Metodo 2: Gestione tramite CSV
1. **Modifica il file `impiegati.csv`** per aggiungere/rimuovere impiegati
2. **Carica nel database**:
   ```bash
   py load_impiegati.py
   ```

#### Metodo 3: Aggiunta Singola
```bash
py load_impiegati.py add CARD004 "Giovanni" "Bianchi" "Cardiologia"
```

#### Metodo 4: Visualizzazione
```bash
py load_impiegati.py show
```

### Gestione Reparto

Una volta loggato, avrai accesso a:

- **🏥 Gestione Stanze**: Crea e gestisci le stanze del reparto
- **👥 Gestione Pazienti**: Inserisci e gestisci i pazienti
- **💾 Backup Database**: Esporta backup del database
- **📊 Statistiche**: Visualizza statistiche del reparto
- **❓ Aiuto**: Guida utente completa

### Workflow Tipico

1. **Crea le stanze** del reparto con capacità appropriate
2. **Inserisci i pazienti** assegnandoli alle stanze disponibili
3. **Gestisci le schede cliniche** per ogni paziente
4. **Monitora le statistiche** per controllare l'occupazione

## 🛠️ Struttura del Progetto

```
App-Ospedale/
├── main.py              # File principale dell'applicazione
├── database.py          # Gestione database SQLite
├── login.py             # Sistema di login e gestione impiegati
├── dashboard.py         # Dashboard principale
├── stanze.py            # Gestione stanze
├── pazienti.py          # Gestione pazienti e schede cliniche
├── init_database.py     # Inizializzazione database con dati di default
├── load_impiegati.py    # Gestione impiegati tramite CSV
├── impiegati.csv        # File CSV con gli impiegati
├── requirements.txt     # Dipendenze Python
└── README.md           # Questo file
```

## 🗄️ Database

L'applicazione utilizza SQLite con le seguenti tabelle:

- **impiegati**: Dati degli impiegati e reparti
- **stanze**: Stanze per reparto con capacità
- **pazienti**: Dati pazienti e assegnazione stanze
- **schede_cliniche**: Informazioni mediche dettagliate

## 👥 Gestione Impiegati

### Impiegati di Default

L'inizializzazione crea automaticamente questi impiegati:

**🏥 Cardiologia:**
- CARD001 - Mario Rossi
- CARD002 - Anna Bianchi  
- CARD003 - Giuseppe Verdi

**🧠 Neurologia:**
- NEUR001 - Laura Neri
- NEUR002 - Marco Gialli
- NEUR003 - Sofia Rosa

**🔪 Chirurgia:**
- CHIR001 - Roberto Blu
- CHIR002 - Elena Viola
- CHIR003 - Paolo Arancione

**👶 Pediatria:**
- PEDI001 - Francesca Verde
- PEDI002 - Luca Marrone
- PEDI003 - Chiara Grigio

**🚨 Pronto Soccorso:**
- PS001 - Antonio Nero
- PS002 - Maria Bianco
- PS003 - Davide Rosso

### Modificare gli Impiegati

1. **Modifica il file `impiegati.csv`**:
   ```csv
   id_impiegato,nome,cognome,reparto
   CARD001,Mario,Rossi,Cardiologia
   CARD002,Anna,Bianchi,Cardiologia
   # Aggiungi nuovi impiegati qui
   ```

2. **Ricarica nel database**:
   ```bash
   py load_impiegati.py
   ```

## 🔧 Personalizzazione

### Aggiungere Nuovi Reparti

Modifica il file `login.py` nella classe `GestioneImpiegatiWindow`:

```python
self.reparto_combo = ttk.Combobox(input_frame, 
    values=['Cardiologia', 'Neurologia', 'Chirurgia', 'Pediatria', 
            'Pronto Soccorso', 'Nuovo Reparto'], width=12)
```

### Modificare l'Interfaccia

L'applicazione utilizza colori moderni e un design pulito. I colori principali sono:

- `#2c3e50`: Blu scuro (header)
- `#3498db`: Blu (pulsanti primari)
- `#27ae60`: Verde (successo)
- `#e74c3c`: Rosso (eliminazione)
- `#f39c12`: Arancione (modifica)

## 📦 Packaging per Distribuzione

### Windows (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Linux (.AppImage)

```bash
pip install briefcase
briefcase new
briefcase create
briefcase build
```

### macOS (.app)

```bash
pip install py2app
python setup.py py2app
```

## 🐛 Risoluzione Problemi

### Errore "tkinter not found"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# macOS
brew install python-tk
```

### Errore Database
- Verifica i permessi di scrittura nella directory
- Controlla che SQLite sia installato
- Elimina il file `ospedale.db` per ricreare il database

### Problemi di Interfaccia
- Assicurati di avere una risoluzione minima di 1024x768
- Su sistemi Linux, prova a installare font aggiuntivi


## 🔄 Versioni

- **v1.0**: Versione iniziale con tutte le funzionalità base

