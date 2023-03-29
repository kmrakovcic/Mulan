import matplotlib
import sys
matplotlib.use('TkAgg')
import scipy
import numpy 
import matplotlib.backends.backend_tkagg #import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.figure 
import tkinter  # Ivica zamjena Tkinter u tkinter
import scipy.optimize 
import re
from tkinter import filedialog  # Ivica zamjena tkFileDialog u from tkinter import filedialog
from pylab import *
from scipy.sparse.csgraph import _validation
#--------------------------------------------------------  
master = tkinter.Tk() #Ivica zamjena Tkinter.Tk() u tkinter.Tk()
master.title("Vrijeme zivota kozmickih miona")
file = filedialog.askopenfile(parent=master,mode='rt',title='Izaberi tekstualnu datoteku s podacima')
# Ivica zamjena tkFileDialog u filedialog
# Ivica zamjena mode='rb' u mode='rt'
#--------------------------------------------------------
def podaci(uvjet,korak):
  #  return [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 200, 200, 200, 200, 200, 200, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 350, 350, 350, 350, 350, 350, 350, 350, 350, 350, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 450, 450, 450, 450, 450, 450, 450, 450, 450, 450, 450, 450, 450, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 550, 550, 550, 550, 550, 550, 550, 550, 550, 550, 550, 550, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 650, 650, 650, 650, 650, 650, 650, 650, 700, 700, 700, 700, 700, 750, 750, 750, 750, 750, 750, 750, 750, 750, 750, 750, 750, 750, 750, 750, 750, 750, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 850, 850, 850, 850, 850, 850, 850, 850, 850, 850, 850, 850, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 950, 950, 950, 950, 950, 950, 950, 950, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1050, 1050, 1050, 1050, 1050, 1050, 1050, 1050, 1050, 1050, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1150, 1150, 1150, 1150, 1150, 1150, 1150, 1150, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1250, 1250, 1250, 1250, 1250, 1250, 1300, 1300, 1300, 1300, 1300, 1300, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1450, 1450, 1450, 1450, 1450, 1450, 1450, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1550, 1550, 1550, 1550, 1550, 1550, 1550, 1550, 1550, 1550, 1550, 1550, 1600, 1600, 1600, 1600, 1650, 1650, 1650, 1650, 1650, 1650, 1650, 1650, 1650, 1650, 1700, 1700, 1700, 1700, 1700, 1750, 1750, 1750, 1750, 1750, 1750, 1750, 1750, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1850, 1850, 1850, 1850, 1850, 1850, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1950, 1950, 2000, 2000, 2050, 2050, 2050, 2050, 2050, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2150, 2150, 2150, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2250, 2250, 2250, 2250, 2300, 2300, 2300, 2300, 2300, 2300, 2350, 2350, 2350, 2350, 2400, 2400, 2450, 2450, 2450, 2450, 2450, 2500, 2500, 2500, 2500, 2500, 2550, 2550, 2550, 2550, 2600, 2600, 2600, 2600, 2600, 2600, 2600, 2600, 2650, 2650, 2650, 2650, 2650, 2650, 2700, 2700, 2750, 2750, 2800, 2800, 2800, 2800, 2850, 2850, 2900, 2900, 2900, 2900, 2950, 2950, 2950, 2950, 2950, 2950, 2950, 3000, 3000, 3000, 3000, 3050, 3050, 3050, 3050, 3050, 3150, 3150, 3150, 3200, 3200, 3200, 3200, 3250, 3300, 3300, 3300, 3350, 3350, 3350, 3400, 3450, 3450, 3450, 3450, 3450, 3500, 3550, 3550, 3600, 3650, 3700, 3750, 3800, 3850, 3850, 3850, 3850, 3850, 3900, 3950, 4000, 4000, 4000, 4050, 4100, 4100, 4200, 4250, 4250, 4250, 4300, 4300, 4350, 4350, 4400, 4450, 4450, 4450, 4500, 4500, 4500, 4550, 4550, 4550, 4650, 4650, 4750, 4800, 4850, 4850, 4850, 4900, 4900, 4900, 5000, 5050, 5050, 5050, 5100, 5100, 5150, 5250, 5300, 5300, 5300, 5350, 5350, 5400, 5400, 5500, 5550, 5550, 5600, 5700, 5700, 5800, 5800, 6050, 6050, 6150, 6200, 6200, 6250, 6350, 6450, 6550, 6600, 6650, 6700, 6750, 6750, 6800, 6950, 7000, 7100, 7200, 7200, 7200, 7250, 7300, 7550, 7650, 7650, 7650, 7750, 7850, 7950, 7950]
    y=[]
    uvjetna_razlika=[] #razlika 2 vremena ako zadovolje uvjet
    while 1:
        lines = file.readlines(250000) #citaju se blokovi od 250kB 
        if not lines:
            break #kad vise nema podataka izlazi se iz petlje
        for line in lines:
            if 'B' in line:
                
                lista = re.findall('\w+', line) #makiva razmake iz stringa
                lista.pop(0) #makiva slovo B iz stringa
                x=int(lista.pop(0)) #uzima x vrijednost
                if y.__len__() > 1: #moraju biti barem 2 vremena da bi se racunala razlika
                    for i in range (y.__len__() -1):
                        deltat=y[i+1]-y[i]
                        if (deltat<uvjet)&(deltat>0):#razlika vremena manja od uvjeta
                            uvjetna_razlika.append(deltat)#ako je onda se dodaje
                y=[]
            elif line.__len__()<3: #kraj datoteke=izlaz iz petlje
                break
            else: #formula za dobivanje vremena iz podataka koje daje sustav
                vrijeme=((2**32)*(x-1)+(int(line)))*50 #vrijeme u ns
                y.append(vrijeme) # lista 16 vremena
    uvjetna_razlika.sort() #sortiranje razlika vremena
    print(uvjetna_razlika)
    return uvjetna_razlika #f-ja vraca sortiranu uvjetnu razliku
#-----------------------------------------------------------------
def func(x, a, b, c): #funkcija
    return a * numpy.exp(-b * x*0.000001) + c
    
def inverzfunc(y,a,b,c): #inverzna funkcija
    return (numpy.log((y-c)/a))/(-1*b*0.000001)
#-------------------------------------------------------------------------------
def show_entry_fields():

   uvjet=int(e1.get()) #uvjet u ns = 10us
   korak=int(e2.get()) #korak od 0,5us  
   x = numpy.linspace(float(korak)/1000, float(uvjet-korak)/1000, uvjet//korak -2)
    #Ivica zamjena uvjet/korak -1 u uvjet//korak -2
   x = [xn-float(korak)/2000. for xn in x] #pomicanje tocke na sredinu intervala
   x = [float(xn) for xn in x]
   x = numpy.array(x)
   
   razlike=podaci(uvjet,korak)
   print(razlike)
       
   i=0   
   y=[] 
   fitanje_gore=korak
   fitanje_dolje=0

   for a in razlike: #brojanje broja dogadaja po intervalima
        if (a<=fitanje_gore)&(a>fitanje_dolje):
            i=i+1
        else :
            y.append(i)
            i=1
            fitanje_gore=fitanje_gore+korak
            fitanje_dolje=fitanje_dolje+korak
   
   #y = [129, 120, 93, 76, 54, 46, 26, 17, 19, 16, 19, 7, 8, 9, 6, 9, 7, 7, 3]
   y = [float(yn) for yn in y]
   y = numpy.array(y)
 #  print(*y, sep = "\n")  


   popt, pcov = scipy.optimize.curve_fit(func, x, y) #fittanje krivulje
   b=popt[1]
   pogreska_lambda = numpy.sqrt(pcov.diagonal()) #pogreska  konstante raspada 
   pogreska_tau = (pogreska_lambda[1])*(10**6)*(1./(popt[1]**2))#pogreska vremena zivota (iz fita)
   #racuna se kao: pogreska konst.raspada*1/(konst.raspada**2) i pretvori se u us
   e3.insert(0, b)
   e4.insert(0, 1./b*1000000)
   e5.insert(0, pogreska_tau)
   
   yerr=[] #odstupanje tocaka krivulje po y-osi
   for j in range(x.__len__()): #racunanje odstupanja
       yerr.append(math.sqrt(y[j]))
       
         
   f = matplotlib.figure.Figure(figsize=(5,4), dpi=100) 
   a = f.add_subplot(111)
   #a.plot(x,y,marker='o', linestyle=' ', color='r', label='Square')
   a.plot(x, func(x, *popt), label="Fitted Curve")#fittana krivulja
   a.errorbar(x, y, yerr=yerr, fmt='o')#pogreske tocaka od krivulje
   # Set common labels
   f.text(0.5, 0.04, 'Vrijeme izmedju detekcija [us]', ha='center', va='center')
   f.text(0.06, 0.5, 'Broj detekcija', ha='center', va='center', rotation='vertical')
   
   dataPlot = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(f, master=master)
   dataPlot.draw()  #Ivica zamjena show u draw
   dataPlot.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#-----------------------------------------------------------------
toolbar = tkinter.Frame(master)
button1 = tkinter.Button(toolbar, text='Start',command=show_entry_fields)
button1.grid(row=2, column=1) 
tkinter.Label(toolbar, text="Delta t [ns]").grid(row=0)
tkinter.Label(toolbar, text="Interval [ns]").grid(row=1)
tkinter.Label(toolbar, text='Lambda [1/s]').grid(row=3)
tkinter.Label(toolbar, text='Tau [us]').grid(row=4)
tkinter.Label(toolbar, text='Delta tau [us]').grid(row=5)
e1 = tkinter.Entry(toolbar,)
e2 = tkinter.Entry(toolbar,)
e3 = tkinter.Entry(toolbar,)
e4 = tkinter.Entry(toolbar,)
e5 = tkinter.Entry(toolbar,)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=3, column=1)
e4.grid(row=4, column=1)
e5.grid(row=5, column=1)
e1.insert(0, 10000)
e2.insert(0, 200)
toolbar.pack(side=tkinter.TOP, fill="x") # top of parent, the master window
#-------------------------------------------------------------------------------
master.mainloop()
