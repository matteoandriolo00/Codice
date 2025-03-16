from datetime import time, timedelta, datetime

class Slot:
    # Costruttore
    def __init__(self):
        self.pizze = 0
        self.indirizzi_consegne = []
        self.orari_clienti = ""
        self.orario_forno = None
        self.occupato = False
        self.doppia = False

    def info(self):
        if self.occupato:
            print(f"Orario forno: {self.orario_forno}")
            print("Occupato/Pausa")
            return
        # orario cliente e forno coincidono per lo stesso slot
        print(f"Orario forno: {self.orario_forno}")
        print(f"Pizze: {self.pizze}")
        print("Ordini corrispondenti:")
        print(self.orari_clienti)
        if self.indirizzi_consegne:
            print("Indirizzi di consegna: ")
            print(self.indirizzi_consegne)
            if self.doppia: print("Doppia: sì")
            else: print("Doppia: no")

    def isEmpty(self):
        return self.pizze == 0

    def set_max_pizze(self, max_pizze):
        self.max_pizze = max_pizze 

    def aggiungiPizze(self,n):
        if isinstance(n, int) and n >= 0:
            self.pizze += n # aggiunge il numero di pizze al totale
        else:
            raise ValueError("Il numero di pizze deve essere un numero intero non negativo")

    def modificaPizze(self, n):
        if isinstance(n, int) and n >= 0:
            self.pizze = n

    def getPizze(self):
        return self.pizze

    def isOccupato(self):
        return self.occupato
    
    def setOccupato(self):
        self.occupato = True
        self.disponibile = False

    def aggiungiOrarioCliente(self, dati_cliente):
        self.orari_clienti += (f"Cliente: {dati_cliente["nome_cliente"]}, orario: {dati_cliente["orario_cliente"]}\n")

    def setOrarioForno(self, new_orario_forno):
        if isinstance(new_orario_forno, time):
            self.orario_forno = new_orario_forno
        else:
            raise ValueError("L'orario cliente deve essere un'istanza di datetime.time")
    
    def getOrarioForno(self):
        return self.orario_forno

    def aggiungiIndirizzoConsegna(self, indirizzo_da_aggiungere):
        if isinstance(indirizzo_da_aggiungere, str):
                self.indirizzi_consegne.append(indirizzo_da_aggiungere)
        else: raise ValueError("L'indirizzo deve essere una stringa")

    def getIndirizzi(self):
        return self.indirizzi_consegne

    def setDoppia(self):
        self.doppia = True

    def slot_disponibile(self, dati_cliente):
        total_pizze = self.pizze + dati_cliente["pizze"]
        if total_pizze > self.max_pizze:
            return False
        return True