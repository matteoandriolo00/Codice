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

slot_array = [Slot() for i in range(n)]

# impostazione orari e max_pizze slot
ora_inizio = time(17,00)
slot_array[0].setOrarioForno(ora_inizio)
slot_array[0].setOrarioCliente(ora_inizio)
slot_array[0].set_max_pizze(max_pizze)
start, end = 1, n
curr = ora_inizio
for i in range(start, end):
    curr = (datetime.combine(datetime.today(), curr) + timedelta(hours=0, minutes=5)).time()
    slot_array[i].setOrarioForno(curr)
    slot_array[i].setOrarioCliente(curr)
    slot_array[i].set_max_pizze(max_pizze)

# orari validi
orari_validi = [slot_array[i].getOrarioForno() for i in range(n)]

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
        via_ind = vie.loc[find_most_similar_index(vie, "Indirizzo", indirizzo), ["Indirizzo"]]
        ordineProposto.setLuogo(via_ind.iloc[0]) # setta la via senza avere le info sul contenuto dell'oggetto
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
    return ordineProposto

def assegna_slot(ordine: Slot):
    index = 0
    for i in range(n):
        if ordine.getOrarioForno() == slot_array[i].getOrarioForno():
            index = i
            if slot_array[i].slot_disponibile(ordine):
                slot_array[i].setPizze(ordine.getPizze())
                slot_array[i].setPizzeFamiglia(ordine.getPizzeFamiglia())
                if ordine.isConsegna():
                    slot_array[i].setConsegna()
                    slot_array[i].setLuogo(ordine.getLuogo())                
            else: # se l'orario non è disponibile
                print("\nOrari disponibili da proporre al cliente:")
                anticipo = ordine.getAnticipoForno()
                for k in range(index+1, index+7):
                    if slot_array[k].slot_disponibile(ordine):
                        orario = (datetime.combine(datetime.today(), slot_array[k].getOrarioCliente()) + timedelta(hours=0, minutes=anticipo)).time()
                        print(orario)
                print("\n")
                while True:
                    x = input("Reimpostare l'ordine? (s/n) ").strip().lower()  # Rimuove spazi e converte in minuscolo
                    if x in ["s", "n"]:
                        break
                    else:
                        print("Input non valido. Inserisci 's' per sì o 'n' per no.")
                reimpostare = x == "s"  # True se l'utente scrive "s", False altrimenti
                if reimpostare:
                    nuovo_ordine = getProposta()
                    assegna_slot(nuovo_ordine)

# istanza d'esempio
ordine_cliente = getProposta()
#print("-" * 10 + " Proposta cliente " + "-" * 10)
#ordine_cliente.info()

ordine_cliente2 = getProposta()
#print("-" * 10 + " Proposta cliente 2 " + "-" * 10)
#ordine_cliente2.info()

assegna_slot(ordine_cliente)
assegna_slot(ordine_cliente2)

# stampa per verifica assegnamento
for i in range(n):
    if slot_array[i].getPizze() > 0 or slot_array[i].getPizzeFamiglia() > 0 or slot_array[i].isConsegna():
        print("-" * 25)
        slot_array[i].info()
