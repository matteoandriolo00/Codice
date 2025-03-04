from datetime import time, timedelta, datetime
from class_Slot import Slot
from geopy import distance
import pandas as pd
import os

# percorso cartella csv anche se cambio pc
csv_dir = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(csv_dir, "Indirizzi.csv")

vie = pd.read_csv(csv_path, sep=",")

n=70 # numero slot orari

ordini = [Slot() for i in range(n)]

# impostazione orari slot
ora_inizio = time(17,00)
ordini[0].setOrarioCliente(ora_inizio)
start, end = 1, n
curr = ora_inizio
for i in range(start, end):
    curr = (datetime.combine(datetime.today(), curr) + timedelta(hours=0, minutes=5)).time()
    ordini[i].setOrarioCliente(curr)

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
        ordineProposto.setIndirizzo(indirizzo)
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

ordine1 = getProposta().info()

#def assegna_slot(ordine):