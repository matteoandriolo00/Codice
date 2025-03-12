from datetime import time, timedelta, datetime

class Slot:
    def __init__(self):
        self.pizze = 0
        self.pizzeFamiglia = 0
        self.indirizzo1 = None 
        self.indirizzo2 = None
        self.indirizzo3 = None
        self.orario_cliente = None
        self.orario_forno = None
        self.disponibile = True 
        self.consegna = False
        self.anticipo_forno = 0
        self.pausa = False

    def set_max_pizze(self, max_pizze):
        self.max_pizze = max_pizze 

    def info(self):
        if self.pausa:
            print("Pausa")
            return
        # orario cliente e forno coincidono per lo stesso slot
        print(f"Orario forno: {self.orario_forno}")
        print(f"Pizze: {self.pizze}\nPizze famiglia: {self.pizzeFamiglia}")
        if self.isConsegna():
            print(f"Consegna/e a casa per le: {self.orario_cliente}")
            if self.indirizzo2 is None: print(f"Dove: {self.indirizzo1}")
            elif self.indirizzo3 is None: print(f"Dove: {self.indirizzo1}, {self.indirizzo2}")
            else: print(f"Dove: {self.indirizzo1}, {self.indirizzo2}, {self.indirizzo3}")
        else: print("Consegne: no")

    def setPizze(self,n):
        if isinstance(n, int) and n >= 0:
            self.pizze = self.pizze + n # aggiunge il numero di pizze al totale
        else:
            raise ValueError("Il numero di pizze deve essere un numero intero non negativo")

    def isPausa(self):
        return self.pausa
    
    def setPausa(self):
        self.pausa = True
        self.disponibile = False

    def getPizze(self):
        return self.pizze
    
    def getPizzeFamiglia(self):
        return self.pizzeFamiglia

    def setPizzeFamiglia(self,n):
        if isinstance(n, int) and n >= 0:
            self.pizzeFamiglia = self.pizzeFamiglia + n # aggiunge il numero di pizze famiglia al totale
        else:
            raise ValueError("Il numero di pizze famiglia deve essere un numero intero non negativo")

    def setOrarioCliente(self, new_orario_cliente):
        if isinstance(new_orario_cliente, time):
            self.orario_cliente = new_orario_cliente
        else:
            raise ValueError("L'orario cliente deve essere un'istanza di datetime.time")

    def setOrarioForno(self, new_orario_forno):
        if isinstance(new_orario_forno, time):
            self.orario_forno = new_orario_forno
        else:
            raise ValueError("L'orario cliente deve essere un'istanza di datetime.time")

    def getOrarioCliente(self):
        return self.orario_cliente
    
    def getOrarioForno(self):
        return self.orario_forno

    def setLuogo(self, new_indirizzo):
        if self.indirizzo1 is None:
            self.indirizzo1 = new_indirizzo
        elif self.indirizzo2 is None:
            self.indirizzo2 = new_indirizzo
        elif self.indirizzo3 is None:
            self.indirizzo3 = new_indirizzo
        else:
            raise ValueError("Tutti gli indirizzi sono già impostati")

    def getLuogo(self):
        return self.indirizzo1 # basta solo il primo perché questo metodo viene invocato solo durante la proposta cliente

    def hasFamily(self):
        if self.pizzeFamiglia > 0:
            return True
        
    def setConsegna(self):
        self.consegna = True

    def isConsegna(self):
        return self.consegna
        
    def calcolo_anticipo_forno(self):
        
        intervalli = [
            (datetime.strptime("18:00", "%H:%M").time(), datetime.strptime("19:15", "%H:%M").time(), 10),
            (datetime.strptime("19:15", "%H:%M").time(), datetime.strptime("20:00", "%H:%M").time(), 15),
            (datetime.strptime("20:00", "%H:%M").time(), None, 20)  # Nessun limite superiore
        ]

        self.anticipo_forno = next((anticipo for inizio, fine, anticipo in intervalli 
                                    if inizio <= self.orario_cliente and (fine is None or self.orario_cliente < fine)), None)

        if self.anticipo_forno is None:
            print("Non è stato possibile calcolare l'anticipo per il forno.")
            return

        self.orario_forno = (datetime.combine(datetime.today(), self.orario_cliente) - timedelta(minutes=self.anticipo_forno)).time()

        if self.hasFamily():
            self.orario_forno = (datetime.combine(datetime.today(), self.orario_forno) - timedelta(minutes=5)).time()
            self.anticipo_forno += 5

        if self.isConsegna():
            self.orario_forno = (datetime.combine(datetime.today(), self.orario_forno) - timedelta(minutes=15)).time()
            self.anticipo_forno += 15

    def getAnticipoForno(self):
        return self.anticipo_forno

    def slot_disponibile(self, other_slot):
        total_pizze = self.pizze + (self.pizzeFamiglia * 2) + other_slot.pizze + (other_slot.pizzeFamiglia * 2)
        if total_pizze > self.max_pizze: 
            self.disponibile = False # se il numero di pizze supera 9, non è possibile usare questo slot orario
        return self.disponibile