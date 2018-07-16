#MW Analiza Petli Histerezy Magnetycznej#

import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
from matplotlib import style
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

Font = ("Verdana", 12)
style.use("ggplot")

T = 50.7  #  temperatura pomiaru
Tp = '50p7'
Type = 'heat'  #  pomiar wzrostowy i opadajacy temperatury

wspy = 2.0
wspxy = 0.2

#  Dane
S = 25*10**(-6)  # 25mm2
dS = 0.5 * S  # niepewnosc powierzchni

C0 = 0.2*10**(-6)  # 2 mikro Farada
dC0 = 0.1 * C0 # niepewnosc kondensatora

dk = 2*10**(-3)  # 2mm
ddk = 0.4 * dk   #  niepewnosc grubosci krysztalu

Upp = 3.0 * 2  #  podwojna amplituda
dUpp = 0.0002 #  niepewnosc 2*amplitudy

f = plt.Figure(figsize=(20, 10), dpi=80)
a = f.add_subplot(111)
a.set_xlabel('Voltage Generator and Bridge[V]')
a.set_ylabel('Voltage on Capacity Bridge [V]')
a.set_title('Plot Voltage from Generator')

g = Figure(figsize=(20, 10), dpi=80)
b = g.add_subplot(121)
b.set_xlabel('Time [s]')
b.set_ylabel('Voltage [V]')
b.set_title('Voltage from Generator in Time')
b.text(0.1, 0.9, 'T= '  '%s ' r'$C^{\circ}$' '%s'% (str(T), Type), verticalalignment='bottom', horizontalalignment='right'
       , transform=a.transAxes, color='black', fontsize=20)

c = g.add_subplot(122)
c.set_xlabel('Time [s]')
c.set_ylabel('Voltage [V]')
c.set_title('Voltage from Bridge')

h = Figure(figsize=(20, 10), dpi=80)
d = h.add_subplot(111)
d.set_xlabel('Electric Field ' r'$\frac{V}{m}$')
d.set_ylabel('Polarization ' r'$\frac{C}{m^2}$')
d.set_title('Dielectric Polarization and Electric Field')


CH1 = open("CH1%s%s.txt" % (Tp, Type), "r").read()  # Kanal casu i napiecia podawanego z generatora
CH1 = CH1.split('\n')
xList1 = []
yList1 = []
ExList1 = []
EyList1 = []

for eachLine in CH1:
    if len(eachLine) > 1:
        x, y = eachLine.split(',')
        xList1.append(float(x))
        yList1.append(float(y))


CH2 = open("CH2%s%s.txt" % (Tp, Type), "r").read()  # Kanal czasu i napiecia z badanego krysztalu
CH2 = CH2.split('\n')
xList2 = []
yList2 = []
ExList2 = []
EyList2 = []

for eachLine in CH2:
    if len(eachLine) > 1:
        x, y = eachLine.split(',')
        xList2.append(float(x))
        yList2.append(float(y))
        EyList2.append((C0 / S) * float(y))  #  Polaryzacja w badanym materiale

Ascal = 3 / max(yList1) # skalowanie amplitudy

for i in range(0, len(yList1), 1):
    EyList1.append(Ascal * (100 / dk) * yList1[i]) #  Skalowanie wartosci pola do amplitudy z generatora


b.plot(xList1, yList1, 'o-', markersize='4', c='pink') #  wykres czasowy sygnalu z mostka oporowego
c.plot(xList2, yList2, 'o-', markersize='4', c='r') #  wykres czasowy sygnalu z mostka pojemnosciowego


a.plot(yList1, yList2, 'go-') #  histereza napiec
d.plot(EyList1, EyList2, 'go-') #  histereza pol

d.text(0.2, 1, 'T= '  '%s ' r'$C^{\circ}$' '%s' % (str(T), Type ), verticalalignment='bottom', horizontalalignment='right'
       , transform=a.transAxes, color='black', fontsize=20)

#  tworzenie sredniego rpzesuniecia y oraz sredniego wektora przesuniecia
deltap = []
deltapxy = []
for i in range(0, len(yList1)-1, 1):
    deltapxy.append(np.sqrt((yList1[i + 1] - yList1[i]) ** 2 + (yList2[i + 1] - yList2[i]) ** 2))
    deltap.append(np.sqrt(((yList2[i + 1] - yList2[i]) ** 2)))
deltay = (sum(deltap)/len(deltap)) * wspy
deltaxy = (sum(deltapxy)/len(deltapxy)) * wspxy


# Znajdywanie punktow dodatnich przecinających się z osią X
pex = []
pey = []
Epex = []
Epey = []
i3 = []
for i in range(0, len(yList1), 1):
    if len(pex) < 30:
        if (yList1[i] > 0 and yList2[i] > -deltaxy and yList2[i] < deltaxy):
            pex.append(yList1[i])
            pey.append(yList2[i])
            Epex.append( Ascal * (100 / dk) * yList1[i])
            Epey.append((C0 / S) * yList2[i])
            i3.append(i)
a.plot(pex, pey, 'ro--')
d.plot(Epex, Epey, 'ro--')

# Znajdywanie punktow ujemnych przecinających się z osią X
mex = []
mey = []
Emex = []
Emey = []
i4 = []
for i in range(0, len(yList1), 1):
    if len(mex) < 30:
        if (yList1[i]<0 and yList2[i] > -deltaxy and yList2[i] < deltaxy):
            mex.append(yList1[i])
            mey.append(yList2[i])
            Emex.append(Ascal * (100 / dk) * yList1[i])
            Emey.append((C0 / S) * yList2[i])
            i4.append(i)
a.plot(mex, mey, 'bo--')
d.plot(Emex, Emey, 'bo--')

# Znajdywanie punktow dodatnich napiecia nasycenia
npex = []
npey = []
Enpx = []
Enpy = []
i1 = []
for i in range(0, len(yList2), 1):
    if len(npex) < 200:
        if (yList1[i]>0 and yList2[i] > max(yList2) - deltay):
            npex.append(yList1[i])
            npey.append(yList2[i])
            Enpx.append(Ascal * (100/dk)*yList1[i])
            Enpy.append((C0/S)*yList2[i])
            i1.append(i)
a.plot(npex, npey, 'ro--')
d.plot(Enpx, Enpy, 'ro--')


# Znajdywanie punktow ujemnych napiecia nasycenia
nmex = []
nmey = []
Ennx = []
Enny = []
i2 = []
for i in range(0, len(yList2), 1):
    if len(nmex) < 200:
        if (yList1[i]<0 and yList2[i] < min(yList2) + deltay):
            nmex.append(yList1[i])
            nmey.append(yList2[i])
            Ennx.append(Ascal * (100 / dk) * yList1[i])
            Enny.append((C0 / S) * yList2[i])
            i2.append(i)

a.plot(nmex, nmey, 'bo-- ')
d.plot(Ennx, Enny, 'bo-- ')

Ay = []
By = []
imaxy = []
imaxx = []
iminy = []
iminx = []
leni = min(len(i1), len(i2))
for i in range (0, leni, 1):
    imaxx.append(xList2[i1[i]])
    imaxy.append(yList2[i1[i]])
    Ay.append(yList1[i1[i]])
    iminx.append(xList2[i2[i]])
    iminy.append(yList2[i2[i]])
    By.append(yList1[i2[i]])
c.plot(imaxx, imaxy, '^', markersize='8', c='b', label="Points B")
c.plot(iminx, iminy, '^', markersize='8', c='black', label="Points A")
b.plot(imaxx, Ay, '^', markersize='8', c='b', label="Points B")
b.plot(iminx, By, '^', markersize='8', c='black', label="Points A")

Cy = []
Dy = []
ipzy = []
ipzx = []
imzy = []
imzx = []
leni = min(len(i3), len(i4))

for i in range (0, leni, 1):
    ipzx.append(xList2[i4[i]])
    ipzy.append(yList2[i4[i]])
    Cy.append(yList1[i4[i]])
    imzx.append(xList2[i3[i]])
    imzy.append(yList2[i3[i]])
    Dy.append(yList1[i3[i]])

c.plot(ipzx, ipzy, '^', markersize='8', c='g', label="Points C")
c.plot(imzx, imzy, '^', markersize='8', c='y', label="Points D")
c.legend(bbox_to_anchor=(0, 1.02, 0.5, .102), loc=1, ncol=4, borderaxespad=0)
b.plot(ipzx, Cy, '^', markersize='8', c='g', label="Points C")
b.plot(imzx, Dy, '^', markersize='8', c='y', label="Points D")

# Napiecie nasycenia polaryzacji
nxm = sum(nmex) / len(nmex)  # PUNKT A srednia z wybranych punktow
nxp = sum(npex) / len(npex)  # PUNKT B

pym = sum(nmey) / len(nmey)  # NAPIECIE K'
pyp = sum(npey) / len(npey)  # NAPIECIE K
KK = abs(pym) + abs(pyp)     # Napiecie K' - K



# Napiecie koercji
xm = sum(mex) / len(mex)  #  C srednia wartosc x dla napiecia koercji + i -
xp = sum(pex) / len(pex)  #  D
#  ym = sum(mey) / len(mey)  #  srednia wartosc x dla napiecia koercji + i -
#  yp = sum(pey) / len(pey)

# Wspołczynniki skalowania
#  AB = 1.5*(abs(nxm) + abs(nxp))# stare

AB = abs(min(nmex)) + abs(max(npex))
CD = abs(xm) + abs(xp)
abcd = CD/AB


###############################OBLICZANIE BŁEDOW###########################################
#  odchylenia standardowe
#  odchylenie punktow składowych x
bA = []
bB = []
bC = []
bD = []
dKp = []
dKm = []

for i in range (0, len(nmex), 1):  # A
    bA.append((nmex[i] - nxm) ** 2)
for i in range(0, len(npex), 1):  # B
    bB.append((npex[i] - nxp) ** 2)

for i in range(0, len(mex), 1):  # C
    bC.append((mex[i] - xm) ** 2)
for i in range(0, len(pex), 1):  # D
    bD.append((pex[i] - xp) ** 2)

for i in range(0, len(npey), 1):  # Kp
    dKp.append((npey[i] - pyp) ** 2)
for i in range(0, len(nmey), 1):  # Km
    dKm.append((nmey[i] - pym) ** 2)

#  ####Obliczanie odchylen######
sC = np.sqrt((1/(len(mex)-1))*sum(bC))
sD = np.sqrt((1/(len(pex)-1))*sum(bD))
sdKp = np.sqrt((1/(len(npey)-1))*sum(dKp))
sdKm = np.sqrt((1/(len(nmey)-1))*sum(dKm))

#  #Blad srednich
dsC = sC / np.sqrt(len(mex))
dsD = sD / np.sqrt(len(pex))
dsdKp = sdKp / np.sqrt(len(npey))
dsdKm = sdKm / np.sqrt(len(nmey))
dsdKK = dsdKp + dsdKm # blad srednij wartoci KK'
dsabcd = np.sqrt(((xp/AB)*dsC)**2 + ((xm/AB)*dsD)**2) #  szacunkowy blad

#  Bledy wzgledne A B C D AB/CD
wdsC = 100 * dsC / xm
wdsD = 100 * dsD / xp
wdsdKp = 100 * dsdKp / pyp
wdsdKm = 100 * dsdKm / pym
wdsKK = 100 * dsdKK / KK
wdabcs = 100 * dsabcd / abcd


Uc = ((abcd)*100 * Upp)/2
Ec = Uc/dk  # Pole Koercji

Ps = (C0 * KK) / (2 * S)
dPs = np.sqrt(((KK/(2*S)*dC0))**2 + ((C0/(2*S)*dsdKK)**2 + ((C0*KK/(2*S**2))*dS)**2))
wdPs = 100 * dPs / Ps


#  Bledy uc i ec
dUc= np.sqrt(((100*Upp*dsabcd)**2+(100*abcd*dUpp)**2))
dEc = np.sqrt(((dUc/dk)**2+((Uc*ddk)/(dk**2))**2))

#  Bledny wzgledne UC i EC
wdUc = dUc * 100 / Uc
wdEc = dEc *100 / Ec



a.annotate('A', xy=(min(nmex), pym), xytext=(min(nmex), 0), arrowprops=dict(facecolor='black', shrink=0, width=2)) ## nxm - zamienione na min(nmex)

a.annotate('B', xy=(max(npex), pyp), xytext=(max(npex), 0), arrowprops=dict(facecolor='black', shrink=0, width=2)) ##   ## nxp - zamienione na max(npex)

a.annotate(s='K', xy=(0, pyp), xytext=(-5, pyp), arrowprops=dict(facecolor='black', shrink=0, width=2))

a.annotate(s='K' r'$\backprime$', xy=(0, pym), xytext=(5, pym), arrowprops=dict(facecolor='black', shrink=0, width=2))

a.annotate(s='C', xy=(xm, 0), xytext=(xm-1, pyp*0.8), arrowprops=dict(facecolor='black', shrink=0, width=2))

a.annotate(s='D', xy=(xp, 0), xytext=(xp+1, pym*0.8), arrowprops=dict(facecolor='black', shrink=0, width=2))

a.text(0.2, 0.01, "AB= %s" % str(round(AB, 2)), verticalalignment='bottom', horizontalalignment='right'
       , transform=a.transAxes, color='red', fontsize=20)

a.text(0.4, 0.01, "CD= %s" % str(round(CD, 2)), verticalalignment='bottom', horizontalalignment='right'
       ,transform=a.transAxes, color='black', fontsize=20)

a.text(0.7, 0.01, 'KK' r'$\backprime$' '= %s' 'V' % str(round(KK, 3)), verticalalignment='bottom'
       , horizontalalignment='right', transform=a.transAxes, color='black', fontsize=20)

a.text(0.1, 1, 'T= '  '%s ' r'$C^{\circ}$' '%s'% (str(T), Type), verticalalignment='bottom', horizontalalignment='right'
       , transform=a.transAxes, color='black', fontsize=20)

a.text(0.95, 0.2, r'$P_{S}$' "= %s" r'$\frac{C}{m^2}$' %str(round(Ps,6)), verticalalignment='bottom'
       , horizontalalignment='right', transform=a.transAxes, color='red', fontsize=20)

a.text(0.95, 0.01,r'$E_c$' "= %s " r'$\frac{C}{m^2}$' %str(int(Ec)), verticalalignment='bottom'
       , horizontalalignment='right', transform=a.transAxes, color='black', fontsize=20)

#######################################################################################################################
#  zapis danych do pliku

#  dane wykresow
Dpunkty=[]
lim = int(len(EyList1))
for i in range (0, lim, 1):
    Dpunkty.append({"Temp": T, "Type": Type, "PointsX": EyList1[i], "PointsY": EyList2[i]})

Dpunkty=json.dumps(Dpunkty)

Dane = open('Dane.txt', 'a')
Dane.write("{}\n".format(Dpunkty))
Dane.close()


#  wykresy polaryzacji
InfoData = {"Temp": T, "Type": Type, "Ec": Ec, "dEc": dEc, "Ps": Ps, "dPs": dPs }

InfoData=json.dumps(InfoData)
Info = open('Info.txt', 'a')
Info.write("{}\n".format(InfoData))
Info.close()


#  zestawienie bledow bezwzglednych i wzglednych
BledyData = []
BledyData.append({"Temp": T, "Type": Type, "Ec": Ec, "dEc": dEc, "wdEc": wdEc, "Ps": Ps, "dPs": dPs, "wdPs": wdPs, 'dUc': dUc,
                  'wdUc': wdUc, 'KK': KK, 'dKK': dsdKK, 'wdKK': wdsKK})

BledyData=json.dumps(BledyData)
Bledy = open('Bledy.txt', 'a')
Bledy.write("{}\n".format(BledyData))
Bledy.close()
#######################################################################################################################



class Ferro(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, "sea.ico")
        tk.Tk.wm_title(self, "Ferro")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, DaneCzasu, DanePomiaru, Histereza):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=Font)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Dane w funkcji czasu",
                            command=lambda: controller.show_frame(DaneCzasu))
        button1.pack(fill='x')

        button2 = ttk.Button(self, text="Dane z pomiaru",
                            command=lambda: controller.show_frame(DanePomiaru))
        button2.pack(fill='x')

        button3 = ttk.Button(self, text="Histereza",
                             command=lambda: controller.show_frame(Histereza))
        button3.pack(fill='x')


class DaneCzasu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Dane z oscyloskopu, w funkcji czasu", font=Font)
        label.pack()

        button1 = ttk.Button(self, text="Start",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack(fill='x')

        button2 = ttk.Button(self, text="Dane z pomiaru",
                             command=lambda: controller.show_frame(DanePomiaru))
        button2.pack(fill='x')

        button3 = ttk.Button(self, text="Histereza",
                             command=lambda: controller.show_frame(Histereza))
        button3.pack(fill='x')


        canvas = FigureCanvasTkAgg(g, self)
        g.savefig('1%s%s.png' %(str(T), Type))
        canvas.show()

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class DanePomiaru(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Dane z pomiarow", font=Font)
        label.pack()
        button1 = ttk.Button(self, text="Start",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack(fill='x')

        button2 = ttk.Button(self, text="Dane w funkcji czasu",
                             command=lambda: controller.show_frame(DaneCzasu))
        button2.pack(fill='x')

        button3 = ttk.Button(self, text="Histereza",
                             command=lambda: controller.show_frame(Histereza))
        button3.pack(fill='x')

        canvas = FigureCanvasTkAgg(f, self)
        f.savefig('2%s%s.png' % (str(T), Type))
        canvas.show()

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class Histereza(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Histereza", font=Font)
        label.pack()

        button1 = ttk.Button(self, text="Start",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack(fill='x')

        button2 = ttk.Button(self, text="Dane w funkcji czasu",
                             command=lambda: controller.show_frame(DaneCzasu))
        button2.pack(fill='x')

        button3 = ttk.Button(self, text="Dane z pomiaru",
                             command=lambda: controller.show_frame(DanePomiaru))
        button3.pack(fill='x')

        canvas = FigureCanvasTkAgg(h, self)
        h.savefig('3%s%s.png' % (str(T), Type))
        canvas.show()

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = Ferro()
app.geometry("1280x720")
app.mainloop()
