from datetime import time, timedelta, datetime
from class_Slot import Slot
import pandas as pd
import distanza
import math
import os

# percorso cartella csv anche se cambio pc
csv_dir = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(csv_dir, "Indirizzi.csv")

vie = pd.read_csv(csv_path, sep=",")

n=70 # numero slot orari

margine = 2 # margine di pizze per non dire di no al cliente
max_pizze = int(input("Inserisci il numero massimo di pizze che si può gestire ogni 5 minuti: ")) + margine 

time_slot = [Slot() for i in range(n)]

# impostazione orari e max_pizze slot
ora_inizio = time(17,00)
# anche se gli slot hanno gli "orari cliente" tra le info uso solo quelli del forno perché è di quello che 
# mi interessa sapere la disponibilità, gli orari cliente li aggiungerò solo nella stringa per info e 
# li prenderò da input per calcolarci l'anticipo ma per gli slot considero solo il forno
time_slot[0].setOrarioForno(ora_inizio)

time_slot[0].set_max_pizze(max_pizze)

start, end = 1, n
curr = ora_inizio
for i in range(start, end):
    curr = (datetime.combine(datetime.today(), curr) + timedelta(hours=0, minutes=5)).time()
    time_slot[i].setOrarioForno(curr)
    time_slot[i].set_max_pizze(max_pizze)

# orari validi
orari_validi = [time_slot[i].getOrarioForno() for i in range(n)]

def getProposta():

    dati_cliente = {
    "nome_cliente": None,
    "orario_cliente": None,
    "consegna": False,
    "famiglia": False,
    "pizze": 0,
    "anticipo": 0,
    "indirizzo": None
    }
    dati_cliente["nome_cliente"] = input("Nome cliente: ")
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
    dati_cliente["orario_cliente"] = orario
    # consegna
    while True:
        x = input("Consegna a casa? (s/n) ").strip().lower()  # Rimuove spazi e converte in minuscolo
        if x in ["s", "n"]:
            break
        else:
            print("Input non valido. Inserisci 's' per sì o 'n' per no.")
    consegna = x == "s"  # True se l'utente scrive "s", False altrimenti
    if consegna:
        dati_cliente["consegna"] = True
        indirizzo = input("Inserire indirizzo: ")
        dati_cliente["indirizzo"] = indirizzo
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
    
    while True:
        try:
            pizzeFam = int(input("Numero pizze famiglia: "))
            if pizzeFam >= 0:
                break
            else:
                print("Il numero di pizze famiglia non può essere negativo.")
        except ValueError:
            print("Inserisci un numero valido.")
    
    if pizzeFam > 0: dati_cliente["famiglia"] = True

    dati_cliente["pizze"] = pizze + pizzeFam*2

    dati_cliente["anticipo"] = calcolo_anticipo_forno(dati_cliente)
    
    return dati_cliente

def calcolo_anticipo_forno(dati_cliente):
    
    slot_richiesti = math.ceil(dati_cliente["pizze"] / max_pizze)
    capienza_borsa = 9
    giri_di_consegna = math.ceil(dati_cliente["pizze"] / (2*capienza_borsa)) 

    intervalli = [
        (datetime.strptime("18:00", "%H:%M").time(), datetime.strptime("19:15", "%H:%M").time(), 10),
        (datetime.strptime("19:15", "%H:%M").time(), datetime.strptime("20:00", "%H:%M").time(), 15),
        (datetime.strptime("20:00", "%H:%M").time(), None, 20)  # Nessun limite superiore
    ]

    # anticipo standard - ordini entro 1 time slot
    anticipo_forno = next((anticipo for inizio, fine, anticipo in intervalli 
                                    if inizio <= dati_cliente["orario_cliente"] and (fine is None or dati_cliente["orario_cliente"] < fine)), None)

    grosso = 0
    if slot_richiesti > 1: grosso = 1
    anticipo_forno += 5*(slot_richiesti-1) + 5*grosso 

    if anticipo_forno is None:
        print("Non è stato possibile calcolare l'anticipo per il forno.")
        return
    
    if dati_cliente["famiglia"]:
        anticipo_forno += 5

    if dati_cliente["consegna"]:
            anticipo_forno += 15*giri_di_consegna

    return anticipo_forno

def assegna_slot_standard(dati_cliente):
    ora_forno_cliente = (datetime.combine(datetime.today(), dati_cliente["orario_cliente"]) - timedelta(hours=0, minutes=dati_cliente["anticipo"])).time()
    for i in range(len(time_slot)):
        indice_slot_richiesto = 0
        if ora_forno_cliente == time_slot[i].getOrarioForno():
            indice_slot_richiesto = i
            if time_slot[i].slot_disponibile(dati_cliente):
                time_slot[i].aggiungiPizze(dati_cliente["pizze"])
                time_slot[i].aggiungiOrarioCliente(dati_cliente)
                if dati_cliente["consegna"]:
                    time_slot[i].aggiungiIndirizzoConsegna(dati_cliente["indirizzo"])               
            else: # se l'orario non è disponibile
                print(f"\n{dati_cliente["orario_cliente"]} non disponibile.\nOrari disponibili:")
                for k in range(indice_slot_richiesto+1, indice_slot_richiesto+7): # 6 slot successivi
                    if time_slot[k].slot_disponibile(dati_cliente):
                        orario_cliente_da_proporre = (datetime.combine(datetime.today(), time_slot[k].getOrarioForno()) + timedelta(hours=0, minutes=dati_cliente["anticipo"])).time()
                        print(orario_cliente_da_proporre)
                print("\n")
                while True:
                    x = input("Reimpostare l'ordine? (s/n) ").strip().lower()  # Rimuove spazi e converte in minuscolo
                    if x in ["s", "n"]:
                        break
                    else:
                        print("Input non valido. Inserisci 's' per sì o 'n' per no.")
                        print("\n")
                reimpostare = x == "s"  # True se l'utente scrive "s", False altrimenti
                if reimpostare:
                    dati_cliente_aggiornati = getProposta()
                    assegna_slot_standard(dati_cliente_aggiornati)

def aggiungi_pausa():
    soglia_pausa = (max_pizze - 1)*4 # un  po' meno del massimo in 4 infornate perché è troppo in pratica
    slot_index = 0
    while slot_index < len(time_slot):
            
        # a ogni set di 4 slot CONSECUTIVI, i contatori vengono resettati
        total_pizze = 0
        slot_count = 0

        # se sono in questa condizione posso cominciare a contare da questo indice
        if time_slot[slot_index].getPizze() > 0 and not time_slot[slot_index].isOccupato():
            
            # ciclo per contare le pizze in 4 slot consecutivi
            while (slot_count <= 4):

                slot_count += 1
                total_pizze += time_slot[slot_index].getPizze()
                slot_index += 1 # all'ultima iterazione slot_index è già allo slot successivo al quarto
            
            if total_pizze >= soglia_pausa:
                pausa_index = slot_index
                if pausa_index < len(time_slot):
                    time_slot[pausa_index].setOccupato()
                    # ora che la pausa è stata impostata nello slot giusto si può avanzare con l'indice
                    slot_index += 1

        # se nello slot non c'è niente si passa al successivo
        else: slot_index += 1

# modificare coi nuovi dati cliente
def assegna_slot_superior(dati_cliente):

    ora_forno_cliente = (datetime.combine(datetime.today(), dati_cliente["orario_cliente"]) - timedelta(hours=0, minutes=dati_cliente["anticipo"])).time()
    slot_start = 0
    for i in range(len(time_slot)):
        if ora_forno_cliente == time_slot[i].getOrarioForno():
            slot_start = i
            break
    
    slot_richiesti = math.ceil(dati_cliente["pizze"] / max_pizze) + 1 # +1 per pausa
    
    # ricerca sequenza slot completamente vuoti all'orario richiesto
    check = 0
    for i in range(slot_start, slot_start + slot_richiesti):
        if time_slot[i].isEmpty():
            check += 1
    
    # se c'è spazio allora posso inserire l'ordine come richiesto
    if check == slot_richiesti:
        p = dati_cliente["pizze"]
        end = slot_start + slot_richiesti - 1
        for i in range(slot_start, end+1):
            if i < (end-1):
                time_slot[i].aggiungiPizze(max_pizze)
                time_slot[i].aggiungiOrarioCliente(dati_cliente)
                if p>max_pizze: p = p-max_pizze 
                if dati_cliente["consegna"]:
                    time_slot[i].aggiungiIndirizzoConsegna(dati_cliente["indirizzo"])
            elif i == (end-1):
                time_slot[i].aggiungiPizze(p)
                time_slot[i].aggiungiOrarioCliente(dati_cliente)
                if dati_cliente["consegna"]:
                    time_slot[i].aggiungiIndirizzoConsegna(dati_cliente["indirizzo"])
            elif i > end-1:
                time_slot[i].setOccupato()
    else: # se non c'è spazio cerco di inserirlo appena posso
        end = slot_start + slot_richiesti - 1
        print(f"\n{dati_cliente["orario_cliente"]} non disponibile.\nOrari disponibili:")
        for i in range(end+1, len(time_slot)-slot_richiesti):
            if time_slot[i].isEmpty():
                check = 0
                for k in range(i, i + slot_richiesti):
                    if time_slot[k].isEmpty():
                        check += 1
                        if check == slot_richiesti:
                            orario_cliente_da_proporre = (datetime.combine(datetime.today(), time_slot[k].getOrarioForno()) + timedelta(hours=0, minutes=dati_cliente["anticipo"])).time()
                            print(orario_cliente_da_proporre)
        print("\n")
        while True:
            x = input("Reimpostare l'ordine? (s/n) ").strip().lower()  # Rimuove spazi e converte in minuscolo
            if x in ["s", "n"]:
                break
            else:
                print("Input non valido. Inserisci 's' per sì o 'n' per no.")
                print("\n")
            
        reimpostare = x == "s"  # True se l'utente scrive "s", False altrimenti
        if reimpostare:
            dati_cliente_aggiornati = getProposta()
            assegna_slot_superior(dati_cliente_aggiornati)

# prova
for i in range(2):
    
    cliente = getProposta()
    if cliente["pizze"] <= max_pizze:
        assegna_slot_standard(cliente)
        aggiungi_pausa()
    else: assegna_slot_superior(cliente)

    # stampa risultati 
    

for i in range(len(time_slot)):
    print("*" * 40)
    
    ind = time_slot[i].getIndirizzi()
    if len(ind) >= 2:
        if distanza.dist(ind[0], ind[1]) < 1:
            time_slot[i].setDoppia()
    
    time_slot[i].info()