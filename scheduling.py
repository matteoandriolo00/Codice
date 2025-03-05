from datetime import time, timedelta, datetime
from class_Slot import Slot
from geopy import distance
import pandas as pd
import difflib
import os
import re

# percorso cartella csv anche se cambio pc
csv_dir = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(csv_dir, "Indirizzi.csv")

vie = pd.read_csv(csv_path, sep=",")

n=70 # numero slot orari

max_pizze = int(input("Inserisci il numero massimo di pizze che si può gestire ogni 5 minuti: "))

ordini = [Slot() for i in range(n)]

# impostazione orari e max_pizze slot
ora_inizio = time(17,00)
ordini[0].setOrarioCliente(ora_inizio)
ordini[0].set_max_pizze(max_pizze)
start, end = 1, n
curr = ora_inizio
for i in range(start, end):
    curr = (datetime.combine(datetime.today(), curr) + timedelta(hours=0, minutes=5)).time()
    ordini[i].setOrarioCliente(curr)
    ordini[i].set_max_pizze(max_pizze)

def clean_text(text):
    """
    Pulisce la stringa mantenendo solo caratteri alfabetici e spazi,
    convertendo tutto in minuscolo.
    """
    return re.sub(r'[^a-zA-Z\s]', '', text).lower()

def find_most_similar_index(df, column, query):
    """
    Restituisce l'indice della riga nella colonna specificata in df che più
    assomiglia alla query, ignorando differenze tra maiuscole e minuscole.
    
    Parametri:
      - df: DataFrame contenente il dataset.
      - column: nome della colonna in cui cercare.
      - query: stringa da confrontare.
    
    Restituisce:
      - best_index: l'indice della riga con il punteggio di similarità più alto.
    """
    cleaned_query = clean_text(query)
    best_score = 0
    best_index = None

    for idx, row in df.iterrows():
        cleaned_value = clean_text(str(row[column]))
        score = difflib.SequenceMatcher(None, cleaned_query, cleaned_value).ratio()
        if score > best_score:
            best_score = score
            best_index = idx

    return best_index


def getProposta():
    print("-" * 10 + " Info cliente " + "-" * 10)
    # ordine proposto
    ordineProposto = Slot()
    # Lista orari validi
    orari_validi = [ordini[i].getOrarioCliente() for i in range(n)] 
    # orario
    while True:
        try:
            orario = datetime.strptime(input("Inserisci un orario (HH:MM): "), "%H:%M").time()
            if orario in orari_validi:
                break
            else:
                print("Orario non valido. Inserisci un orario tra quelli disponibili.")
        except ValueError:
            print("Formato orario non valido. Inserisci un orario nel formato HH:MM.")
    ordineProposto.setOrarioCliente(orario)
    # consegna
    while True:
        x = input("Consegna a casa? (s/n) ").strip().lower()  # Rimuove spazi e converte in minuscolo
        if x in ["s", "n"]:
            break
        else:
            print("Input non valido. Inserisci 's' per sì o 'n' per no.")
    consegna = x == "s"  # True se l'utente scrive "s", False altrimenti
    if consegna:
        ordineProposto.setConsegna()
        indirizzo = input("Inserire indirizzo: ")
        ordineProposto.setLuogo(indirizzo)
    # pizze
    while True:
        try:
            pizze = int(input("Numero pizze normali: "))
            if pizze >= 0:
                break
            else:
                print("Il numero di pizze non può essere negativo.")
        except ValueError:
            print("Inserisci un numero valido.")
    ordineProposto.setPizze(pizze)
    
    while True:
        try:
            pizzeFam = int(input("Numero pizze famiglia: "))
            if pizzeFam >= 0:
                break
            else:
                print("Il numero di pizze famiglia non può essere negativo.")
        except ValueError:
            print("Inserisci un numero valido.")
    ordineProposto.setPizzeFamiglia(pizzeFam)
    # calcolo orario forno
    ordineProposto.calcolo_anticipo_forno()
    print("-" * 10 + " Proposta cliente " + "-" * 10)
    return ordineProposto

# funzione da scrivere 
def assegna_slot(ordine):
    return 0

ordine_cliente = getProposta().info()