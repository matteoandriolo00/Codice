from datetime import time, timedelta, datetime
from class_Slot import Slot
from geopy import distance
import pandas as pd
import os

# percorso cartella csv anche se cambio pc
csv_dir = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(csv_dir, "Indirizzi.csv")

vie = pd.read_csv(csv_path, sep=",")

n=50 # numero slot orari

ordini = [Slot() for i in range(n)]

# impostazione orari slot
ora_inizio = time(18,00)
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
    # orario
    orario = datetime.strptime(input("Inserisci un orario: "), "%H:%M").time()
    ordineProposto.setOrarioCliente(orario)
    # consegna
    x = input("Consegna a casa? (s/n) ").strip().lower()  # Rimuove spazi e converte in minuscolo
    consegna = x == "s"  # True se l'utente scrive "s", False altrimenti
    if consegna:
        ordineProposto.setConsegna()
        indirizzo = input("Inserire indirizzo: ")
        ordineProposto.setIndirizzo(indirizzo)
    # pizze
    pizze = int(input("Numero pizze normali: "))
    ordineProposto.setPizze(pizze)
    pizzeFam = int(input("Numero pizze famiglia: "))
    ordineProposto.setPizzeFamiglia(pizzeFam)
    # calcolo orario forno
    ordineProposto.calcolo_anticipo_forno()
    print("-" * 10 + " Proposta cliente " + "-" * 10)
    return ordineProposto


ordine1 = getProposta().info()