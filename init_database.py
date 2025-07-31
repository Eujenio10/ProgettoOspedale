#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per inizializzare il database con impiegati di default
"""

import sqlite3
import os
from datetime import datetime

def init_database():
    """Inizializza il database con impiegati di default"""
    
    # Rimuovi il database esistente se presente
    if os.path.exists("ospedale.db"):
        os.remove("ospedale.db")
        print("Database esistente rimosso")
    
    # Crea il database
    conn = sqlite3.connect("ospedale.db")
    cursor = conn.cursor()
    
    # Crea le tabelle
    print("Creazione tabelle...")
    
    # Tabella impiegati
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS impiegati (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_impiegato TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            cognome TEXT NOT NULL,
            reparto TEXT NOT NULL,
            data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabella stanze
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stanze (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_stanza TEXT NOT NULL,
            reparto TEXT NOT NULL,
            max_pazienti INTEGER NOT NULL,
            data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabella pazienti
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pazienti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cognome TEXT NOT NULL,
            codice_fiscale TEXT UNIQUE NOT NULL,
            data_nascita TEXT NOT NULL,
            stanza_id INTEGER,
            reparto TEXT NOT NULL,
            data_ricovero TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stanza_id) REFERENCES stanze (id)
        )
    ''')
    
    # Tabella schede cliniche
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schede_cliniche (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paziente_id INTEGER NOT NULL,
            diagnosi TEXT,
            terapie TEXT,
            farmaci TEXT,
            esami TEXT,
            medico_referente TEXT,
            annotazioni TEXT,
            data_aggiornamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (paziente_id) REFERENCES pazienti (id)
        )
    ''')
    
    # Inserisci impiegati di default
    print("Inserimento impiegati di default...")
    
    impiegati_default = [
        # Cardiologia
        ("CARD001", "Mario", "Rossi", "Cardiologia"),
        ("CARD002", "Anna", "Bianchi", "Cardiologia"),
        ("CARD003", "Giuseppe", "Verdi", "Cardiologia"),
        
        # Neurologia
        ("NEUR001", "Laura", "Neri", "Neurologia"),
        ("NEUR002", "Marco", "Gialli", "Neurologia"),
        ("NEUR003", "Sofia", "Rosa", "Neurologia"),
        
        # Chirurgia
        ("CHIR001", "Roberto", "Blu", "Chirurgia"),
        ("CHIR002", "Elena", "Viola", "Chirurgia"),
        ("CHIR003", "Paolo", "Arancione", "Chirurgia"),
        
        # Pediatria
        ("PEDI001", "Francesca", "Verde", "Pediatria"),
        ("PEDI002", "Luca", "Marrone", "Pediatria"),
        ("PEDI003", "Chiara", "Grigio", "Pediatria"),
        
        # Pronto Soccorso
        ("PS001", "Antonio", "Nero", "Pronto Soccorso"),
        ("PS002", "Maria", "Bianco", "Pronto Soccorso"),
        ("PS003", "Davide", "Rosso", "Pronto Soccorso"),
    ]
    
    for impiegato in impiegati_default:
        try:
            cursor.execute('''
                INSERT INTO impiegati (id_impiegato, nome, cognome, reparto)
                VALUES (?, ?, ?, ?)
            ''', impiegato)
            print(f"✓ Impiegato {impiegato[0]} ({impiegato[1]} {impiegato[2]}) - {impiegato[3]}")
        except sqlite3.IntegrityError:
            print(f"✗ Impiegato {impiegato[0]} già esistente")
    
    # Inserisci alcune stanze di default
    print("\nInserimento stanze di default...")
    
    stanze_default = [
        # Cardiologia
        ("Cardiologia 1", "Cardiologia", 4),
        ("Cardiologia 2", "Cardiologia", 3),
        ("Cardiologia 3", "Cardiologia", 2),
        
        # Neurologia
        ("Neurologia 1", "Neurologia", 3),
        ("Neurologia 2", "Neurologia", 4),
        ("Neurologia 3", "Neurologia", 2),
        
        # Chirurgia
        ("Chirurgia 1", "Chirurgia", 2),
        ("Chirurgia 2", "Chirurgia", 3),
        ("Chirurgia 3", "Chirurgia", 1),
        
        # Pediatria
        ("Pediatria 1", "Pediatria", 4),
        ("Pediatria 2", "Pediatria", 3),
        ("Pediatria 3", "Pediatria", 2),
        
        # Pronto Soccorso
        ("PS 1", "Pronto Soccorso", 6),
        ("PS 2", "Pronto Soccorso", 4),
        ("PS 3", "Pronto Soccorso", 3),
    ]
    
    for stanza in stanze_default:
        try:
            cursor.execute('''
                INSERT INTO stanze (nome_stanza, reparto, max_pazienti)
                VALUES (?, ?, ?)
            ''', stanza)
            print(f"✓ Stanza {stanza[0]} - {stanza[2]} posti")
        except sqlite3.IntegrityError:
            print(f"✗ Stanza {stanza[0]} già esistente")
    
    # Commit e chiudi
    conn.commit()
    conn.close()
    
    print("\n" + "="*50)
    print("✅ DATABASE INIZIALIZZATO CON SUCCESSO!")
    print("="*50)
    print("\n📋 IMPIEGATI DISPONIBILI:")
    print("-" * 30)
    
    # Mostra gli impiegati creati
    conn = sqlite3.connect("ospedale.db")
    cursor = conn.cursor()
    cursor.execute('SELECT id_impiegato, nome, cognome, reparto FROM impiegati ORDER BY reparto, cognome')
    impiegati = cursor.fetchall()
    
    reparto_corrente = ""
    for impiegato in impiegati:
        if impiegato[3] != reparto_corrente:
            print(f"\n🏥 {impiegato[3].upper()}:")
            reparto_corrente = impiegato[3]
        print(f"  • {impiegato[0]} - {impiegato[1]} {impiegato[2]}")
    
    conn.close()
    
    print("\n" + "="*50)
    print("🎯 PER ACCEDERE:")
    print("1. Avvia l'applicazione: py main.py")
    print("2. Clicca 'AVVIA APPLICAZIONE'")
    print("3. Inserisci uno degli ID impiegato sopra elencati")
    print("4. Clicca 'ACCEDI'")
    print("="*50)

if __name__ == "__main__":
    print("🏥 INIZIALIZZAZIONE DATABASE GESTIONE OSPEDALE")
    print("="*50)
    init_database() 