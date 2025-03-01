from datetime import time, timedelta, datetime

class Slot:
    def __init__(self):
        self.pizze = 0
        self.pizzeFamiglia = 0
        self.indirizzo = None 
        self.orario_cliente = None
        self.orario_forno = None
        self.orario_occupato = False
        self.consegna = False

    def info(self):
        print(f"Pizze: {self.pizze}\nPizze famiglia: {self.pizzeFamiglia}")
        print(f"Orario cliente: {self.orario_cliente}")
        print(f"Orario forno: {self.orario_forno}")
        if self.isConsegna(): 
            print("Consegna: sì")
            print(f"Indirizzo: {self.indirizzo}")
        else: print("Consegna: no")

    def setPizze(self,n):
        self.pizze = n

    def setPizzeFamiglia(self,n):
        self.pizzeFamiglia = n

    def setOrarioCliente(self, new_orario_cliente):
        self.orario_cliente = new_orario_cliente

    def setOrarioForno(self, new_orario_forno):
        self.orario_forno = new_orario_forno

    def getOrarioCliente(self):
        return self.orario_cliente

    def setIndirizzo(self, new_indirizzo):
        self.indirizzo = new_indirizzo

    def hasFamily(self):
        if self.pizzeFamiglia > 0:
            return True
        
    def setConsegna(self):
        self.consegna = True

    def isConsegna(self):
        return self.consegna
        
    def calcolo_anticipo_forno(self):
        match self.orario_cliente:
            case t if datetime.strptime("18:00", "%H:%M").time() <= self.orario_cliente < datetime.strptime("19:15", "%H:%M").time():
                self.orario_forno = (datetime.combine(datetime.today(), self.orario_cliente) - timedelta(hours=0, minutes=10)).time()
                if self.hasFamily(): self.orario_forno = (datetime.combine(datetime.today(), self.orario_forno) - timedelta(hours=0, minutes=5)).time()
                if self.isConsegna(): self.orario_forno = (datetime.combine(datetime.today(), self.orario_forno) - timedelta(hours=0, minutes=15)).time()
            case t if datetime.strptime("19:15", "%H:%M").time() <= self.orario_cliente < datetime.strptime("20:00", "%H:%M").time():
                self.orario_forno = (datetime.combine(datetime.today(), self.orario_cliente) - timedelta(hours=0, minutes=15)).time()
                if self.hasFamily(): self.orario_forno = (datetime.combine(datetime.today(), self.orario_forno) - timedelta(hours=0, minutes=5)).time()
                if self.isConsegna(): self.orario_forno = (datetime.combine(datetime.today(), self.orario_forno) - timedelta(hours=0, minutes=15)).time()
            case t if datetime.strptime("20:00", "%H:%M").time() <= self.orario_cliente:
                self.orario_forno = (datetime.combine(datetime.today(), self.orario_cliente) - timedelta(hours=0, minutes=20)).time()
                if self.hasFamily(): self.orario_forno = (datetime.combine(datetime.today(), self.orario_forno) - timedelta(hours=0, minutes=5)).time()
                if self.isConsegna(): self.orario_forno = (datetime.combine(datetime.today(), self.orario_forno) - timedelta(hours=0, minutes=15)).time()
            case _:
                print("Non è stato possibile calcolare l'anticipo per il forno.")

    def slot_disponibile(self):
        total_pizze = self.pizze + (self.pizzeFamiglia * 2)
        if total_pizze >= 7: self.orario_occupato = True