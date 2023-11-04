from functools import reduce
import json


class warehouse():  
    def __init__(self):  
        try:
            with open('./db.json','r') as json_file:
                self.list_item=json.load(json_file)
        except:
            print("Db non presente.")
            self.list_item=[]



    def add_item(self):  
        '''Adds an item to the warehouse.'''

        name=input("Nome del prodotto:")
        while 1>0:
            qta_in=input("Quantità:")
            try:
                qta=int(qta_in)
                if qta > 0 :
                    break
                else:
                    print("Valore negativo!.Riprovare.")
            except ValueError:
                print("Valore non intero!. Riprovare.")

        check_availability = False
        for elem in self.list_item:
            if elem["Name_product"]==name:
                check_availability = True
                elem['Qta']=elem['Qta'] + qta
                
        if not check_availability:
            while 1>0:
                purchase_price_in = input("Prezzo di acquisto:")
                selling_price_in = input("Prezzo di vendita:")
                
                try:
                    purchase_price = float(purchase_price_in)
                    selling_price = float(selling_price_in)
                    if purchase_price > 0 and selling_price > 0:    
                        break
                    else:
                        print("Valori negativi inseriti!.Riprovare.")
                except ValueError:
                    print("Controllare i valori di acquisto e vendita inseriti!. Riprovare.")

            product={
                "Name_product":name,
                "Qta":qta,
                "Purchase_price": purchase_price,
                "Selling_price": selling_price
            }
            self.list_item.append(product)

        print(f"AGGIUNTO: {qta} X {name}" )
        self.save_on_file()      



    def sell_item(self):
        '''Delete item from warehouse'''
        if len(self.list_item)!=0:
            feed="si"
            while feed=="si":

                name=input("Nome del prodotto:")
                while 1>0:
                    qta_in=input("Quantità:")
                    try:
                        qta=int(qta_in)
                        if qta > 0 :
                            break
                        else:
                            print("Valore negativo!.Riprovare.")
                    except ValueError:
                        print("Valore non intero!. Riprovare.")
                    
                item={"Name_product":name,"Qta":qta}
                
                check_availability=False
                for item_in_list in self.list_item:
                    if item['Name_product'] == item_in_list['Name_product'] and item_in_list['Qta']>0:
                        item_in_list['Qta'] -= qta
                        if item_in_list['Qta'] == 0 or item_in_list['Qta'] < 0:
                            self.list_item.remove(item_in_list)
                        check_availability = True
                        print("VENDITA REGISTRATA")    

                if not check_availability :
                    print("Prodotto non disponibile nel magazzino")

                feed=input("Aggiungere un altro prodotto ? (si/no):")
            
            self.save_on_file()
        else:
            print("Db non presente")



    def return_gross_profit(self):  
        '''Returns the gross profit of the total sales.'''
        if len(self.list_item)!=0:
            tot = reduce(lambda x,y: x +y, map(lambda q: q['Qta'] * q['Purchase_price'], self.list_item))
            sell =  reduce(lambda x,y: x +y, map(lambda q: q['Qta'] * q['Selling_price'], self.list_item))
            print(f"Profitto: lordo=€{sell} netto=€{sell-tot}")
        else:
            print("Db non presente")


    def return_all_items(self):
        '''Returns all items of warehouse'''
        if len(self.list_item)!=0:
            print("PRODOTTO QUANTITA' PREZZO")
            for item in self.list_item:
                print(f"{item['Name_product']} {item['Qta']} €{item['Selling_price']}")
        else:
            print("Db non presente")
   

    def get_help(self):

        '''
        Get the list of the command available
        '''
        print("I comandi disponibili sono i seguenti:")
        print(" - aggiungi: aggiungi un prodotto al magazzino")
        print(" - elenca: elenca i prodotti in magazzino")
        print(" - vendita: registra una vendita effettuata")
        print(" - profitti: mostra i profitti totali")
        print(" - aiuto: mostra i possibili comandi")
        print(" - chiudi: esci dal programma")
        


    def save_on_file(self):  
        '''Save to file'''

        with open('./db.json',"w+") as json_file:
            json.dump(self.list_item,json_file)



def check_input(input): 

    '''Check user input'''

    if input in ('aggiungi','elenca','vendita','profitti','aiuto','chiudi'):
        return True
    else:
        return False



if __name__ == "__main__":
    
    warehouse_item = warehouse()
    while 1>0:

       
        inp= input("Inserisci un comando:")

        if(check_input(inp)):
            
            if (inp=="aggiungi"):
                warehouse_item.add_item()
            elif (inp=="elenca"):
                warehouse_item.return_all_items()
            elif (inp=="vendita"):
                warehouse_item.sell_item()
            elif (inp=="profitti"):
                warehouse_item.return_gross_profit()
            elif (inp=="aiuto"):
                warehouse_item.get_help()
            elif (inp=="chiudi"):
               print("Bye bye")
               break

        else:
            print("Comando non valido")
            warehouse_item.get_help()