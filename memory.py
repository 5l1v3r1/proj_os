#!/usr/bin/python
import sys, random, time, datetime
from prettytable import PrettyTable

class Processo:
   ''' 
   La classe Processo e' utilizzata per rappresentare un singolo processo.

   -Il metodo _genera_referenza genera casualmente la sequenza di esecuzione del processo.
   -Il metodo _set_table invoca il metodo della classe Gestione_Memoria per 
   generare la tablepage del processo.
   '''
   def __init__(self,id,dimensione):
      self.id = id
      self.dimensione = dimensione
      self.referenze = []

   def _genera_referenza(self,l_riferimenti):
      for i in range(0,l_riferimenti):
         self.referenze.append(random.randrange(0, self.dimensione, 1))
   
   def _set_table(self):
      self.tabella_processi = Gestione_Memoria()._crea_tablepage(self)


class Frame:
   '''
   La classe Frame e' utilizzata per rappresentare un singolo elemento della Ram,
   ciascun elemento e' associato ad un processo tramite il parametro id, conosce 
   il numero di pagine e la propria "eta" nel caso venga utilizzato l'algoritmo LRU.

   -Il metodo _free_inc_eta viene utilizzato per aumentare di un unita' l' "eta" del frame.
   -Il metodo _frame_reset_eta viene utilizzato per resettare l' "eta" del frame.
   '''
   def __init__(self,id_processo,n_pagine):
      self.id = id_processo
      self.page = n_pagine
      self.eta = 0

   def _frame_inc_eta(self):
      self.eta += 1

   def _frame_reset_eta(self):
      self.eta = 0


class Ram:
   '''
   La classe Ram e' utlizzata per rappresentare la memoria fisica ed emula lo "shifting"
   degli indirizzi di memoria come in un sistema operativo reale.

   -Il metodo _aggiungi_frame aggiunge un frame alla lista "lista_frame" (Che rappresenta
   l'indice delle posizioni di memoria libere).

   -Il metodo _free_frame rimuove l'ultimo frame dalla lista "lista_frame" in caso
   contrario ritorna -1.
   '''

   def __init__(self,valore):
      self.maxframe = valore
      self.frames = [Frame(0,0) for x in range(0,self.maxframe)]
      self.lista_frame = [x for x in range(0,self.maxframe)]


   def _aggiungi_frame(self,valore):
      self.lista_frame.append(valore)


   def _free_frame(self):
         if(self.lista_frame):
            return self.lista_frame.pop()
         else:
            return -1


class Gestione_Memoria:
   '''
   La classe Gestione_Memoria e' il "motore di questa simulazione"
   ed e' utilizzata per calcolare il numero di frame assegnabili
   ad ogni processo e per creare la table-page di ciascun processo. 

   -Il metodo _rimuovi_proc rimuove un processo dalla Ram al suo termine.

   -Il metodo _inc_eta e' invocato solo dall'algoritmo LRU e serve a definire quanto
   e' "vecchio" un processo.

   -Il metodo _n_frames_assegnabili calcola il numero di frame assegnabili ad ogni processo.

   -Il metodo _crea_tablepage e' utilizzato per generare la tablepage di ciasun processo
   mappando le pagine virtuali sui vari frame.
   '''
   global ram 

   def _rimuovi_proc(self,p_rimuovere):
      for i in range(p_rimuovere.dimensione):
         f_posizione = p_rimuovere.tabella_processi[i][0]

         if (f_posizione!=-1):
            ram._aggiungi_frame(f_posizione)
            p_rimuovere.tabella_processi[i][0]=-1
            p_rimuovere.tabella_processi[i][1]=0


   def _inc_eta(self,eta):
      for r in ram.frames:
         if(r != eta):
            r._frame_inc_eta() 
         

   def _n_frames_assegnabili(self,proc):
      return round((proc.dimensione / s) * ram.maxframe) 


   def _crea_tablepage(self,proc):
      global p_min_frame

      max_f_assegnabili = round(self._n_frames_assegnabili(proc))
      tablepage=[[0 for j in range(2)] for k in range(0,proc.dimensione)]

      if(max_f_assegnabili < p_min_frame):
         max_f_assegnabili = p_min_frame

      cont = 0
      for l in range (0,proc.dimensione):

         if(cont <= max_f_assegnabili):
            loc = ram._free_frame()
            tablepage[l][0]=loc

            if(loc!=-1):
               ram.frames[loc] = Frame(proc.id,l)
               self._inc_eta(ram.frames[loc])
               tablepage[l][1] = 1
               cont += 1

            else:
               tablepage[l][1] = 0
               cont += 1

         else:
            loc =- 1
            tablepage[l][0] = loc  
            tablepage[l][1] = 0
            cont += 1

      return tablepage
      

class Algoritmi:

   '''
   La classe Algoritmi contiene il codice necessario all'esecuzione dell'algoritmo
   scelto dall'utente.

   -Il metodo _FIFO implementa l'algoritmo FIFO (First in First Out)
   -Il metodo _LRU implementa l'algoritmo LRU (Least Recently Used)
   '''

   def __init__(self,scelta):
      self.algoritmo_scelta=scelta

   def _FIFO(self,processo_p,attuale):
      rimosso = ram.frames.pop()
      for controllo in proc:

         if(controllo.id == rimosso.id):
            ram._aggiungi_frame(controllo.tabella_processi[rimosso.page][0])
            controllo.tabella_processi[rimosso.page][0] =- 1
            controllo.tabella_processi[rimosso.page][1] = 0

      loc = ram._free_frame()
      processo_p.tabella_processi[attuale][0] = loc
      processo_p.tabella_processi[attuale][1] = 1
      ram.frames.insert(0,Frame(processo_p.id,attuale))

      return None          

      
   def _LRU(self,processo_p,attuale):
      vecchio = ram.frames[0]
      for r in ram.frames:

         if(r.eta > vecchio.eta):
            vecchio = r

      ram.frames.pop(processo_p.tabella_processi[vecchio.page][0]) 
      processo_p.tabella_processi[vecchio.page][0] =- 1
      processo_p.tabella_processi[vecchio.page][1] = 0

      loc = ram._free_frame()

      processo_p.tabella_processi[attuale][0] = loc 
      processo_p.tabella_processi[attuale][1] = 1
      ram.frames.insert(loc,Frame(processo_p.id,attuale))
      ram.frames[loc]._frame_reset_eta 
      Gestione_Memoria()._inc_eta(ram.frames[loc]) 
      return None


def _crea_proc(valore):
   global s,p_dimensione,l_riferimenti,f
   for i in range(0,valore):
      proc.append(Processo(i,p_dimensione[i]))
      s = s + proc[i].dimensione
      proc[i]._genera_referenza(l_riferimenti)


def _scrivi_file ():
   timestamp = time.time()

   file_ = open("test_" + str(timestamp) + ".txt", "w")
   file_.write("Data Test: " + str(datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')) + "\n")

   file_.write("\nmax_frame: " + str(max_frame))
   file_.write("\np_min_frame: " + str(p_min_frame))
   file_.write("\nn_processi: " + str(n_processi))
   file_.write("\nl_riferimenti: " + str(l_riferimenti) + "\n")

   for k in range(len(p_dimensione)):
      file_.write("\nProcesso: " + str(k) + " Dimensione: " + str(p_dimensione[k]))

   file_.write("\n\nDimensione totale processi: " + str(dim_p_totale + 1) + "\n\n\n")

   if (Algoritmi.algoritmo_scelta == 1):
      file_.write("Algoritmo scelto: FIFO\n")
   elif (Algoritmi == 2):
      file_.write("Algoritmo scelto: LRU\n")
   else:
      file_.write("Algoitmo scelto: NON VALIDO\n")

   file_.write("\n\n" + str(t))
   file_.write("\n\nTotale PageFault: " + str(totale_pf) + "\n\n")

   file_.close()


#-------------------------------------------------MAIN-------------------------------------------------

global max_frame, p_min_frame, n_processi, l_riferimenti
global p_dimensione, proc, f, s

p_dimensione = []
proc = []
s = 0
max_frame = 0
p_min_frame = 0
n_processi = 0
l_riferimenti = 0

try:

   max_frame = int(sys.argv[1])
   p_min_frame = int(sys.argv[2])
   n_processi = int(sys.argv[3])
   l_riferimenti = int(sys.argv[4])

except Exception as e:

   rosso = '\033[91m'
   verde = '\033[92m'
   fine = '\033[0m'

   print rosso + "\nParametri non validi:" + fine
   print rosso + "python memory.py " + str(max_frame) + " " + str(p_min_frame) + " " + str(n_processi) + " " + str(l_riferimenti) + "\n" + fine

   print verde + "Parametri richiesti: \n" + fine
   print verde + "<max_frame>        Numero massimo di frame" + fine
   print verde + "<p_min_frame>      Numero minimo di frame per processo" + fine
   print verde + "<n_processi>       Numero dei processi" + fine
   print verde + "<l_riferimenti>    Lunghezza della successione dei riferimenti\n" + fine

   print verde + "Esempio:" + fine
   print verde + "python memory.py <max_frame> <p_min_frame> <n_processi> <l_riferimenti>\n" + fine

   print verde + "-----------------------------------------------------------------------------------" + fine
   print verde + "Progetto realizzato da: Salvatore Nitopi \n\n" + fine


   sys.exit(0)

max_frame = max_frame - 1

for i in range (n_processi):
   p_dimensione.append (input ("Inserisci la dimensione del processo " + str(i) + ": "))

print "\n1)Usa FIFO\n"
print "2)Usa LRU\n"
Algoritmi = Algoritmi(input("Quale Algoritmo vuoi usare? "))
_crea_proc(n_processi) 

dim_p_totale = 0

for i in range (len(p_dimensione)):

   dim_p_totale = dim_p_totale + p_dimensione[i]

print "\nCalcolo dimensione totale processi: " + str(dim_p_totale) + "\n"

totale_pf = 0
dim_p_totale = dim_p_totale - 1

t = PrettyTable(["ID", "Page", "Referenze", "Processo", "PageFault", "Frames", "Conclusioni"])

while (max_frame <= dim_p_totale):
   max_frame = max_frame+1
   ram = Ram(max_frame)

   for p_attuale in proc:
      p_attuale._set_table()

   for p_attuale in proc:

      p_fault = 0

      for i in range(l_riferimenti):
         richiesto = int(p_attuale.referenze[i])

         if(p_attuale.tabella_processi[richiesto][1]==0):#PF
            loc = ram._free_frame()

            if(loc !=- 1):
               p_attuale.tabella_processi[richiesto][0]=loc
               p_attuale.tabella_processi[richiesto][1]=1
               ram.frames[loc]=(Frame(p_attuale.id,richiesto))
               Gestione_Memoria()._inc_eta(ram.frames[loc])
               p_fault = p_fault + 1

            else:

               if(Algoritmi.algoritmo_scelta == 1):
                  p_fault = p_fault + 1 
                  Algoritmi._FIFO(p_attuale,richiesto)

               else:
                  Algoritmi._LRU(p_attuale,richiesto)
                  p_fault = p_fault + 1

         else:
            ram.frames[p_attuale.tabella_processi[richiesto][0]]._frame_reset_eta()
            Gestione_Memoria()._inc_eta(p_attuale.tabella_processi[richiesto][0])

      totale_pf += p_fault
      
      c_1 = ""
      c_2 = ""
      c_3 = ""
      c_4 = ""
      c_5 = ""
      c_6 = ""
      
      for k in range(len(ram.frames)):
         c_1 += str(ram.frames[k].id) + " "

      for k in range(len(ram.frames)):
         c_2 += str(ram.frames[k].page) + " "


      c_3 = str(p_attuale.referenze) 
      c_4 = str(p_attuale.id) 
      c_5 = str(p_fault) 
      c_6 = str(ram.maxframe)
      c_7 = "PageFault processo " + str(p_attuale.id) + ": " + str(p_fault) + " con " + str(ram.maxframe) + " frames"

      t.add_row([c_1, c_2, c_3, c_4, c_5, c_6, c_7])

      Gestione_Memoria()._rimuovi_proc(p_attuale)

t.align["ID"] = "l"
t.align["Page"] = "l"
print t

print "\nTotale PageFault: " + str(totale_pf) + "\n\n"

_scrivi_file()

