# Program do komunikacji z przystawka Linkam
# Dzieki programowi mozna sterowac programem NIS w celu zapisu zdjec
# Program przy sterowaniu NIS zapisuje aktualny czas zdjecia i temperature
# Tworzy plik LOG z potrzebnymi informacjami

# Import bibliotek
import serial
from pywinauto import application
import time
import os
import os.path
import matplotlib.pyplot as plt
import warnings
import random

# Wylaczenie ostrzerzen od GUI
# Jest to konieczne do wyswietlania wykresu
warnings.filterwarnings("ignore",".*GUI is implemented.*")


# ------- Klasy i funkcj edo komunikacji z przystawka -------#

# klasa nazwy portu i czestosci odczytu
class Configure:
    def __init__(self, name, baud):
        self.a = serial.Serial()
        self.a.port = str(name)
        self.a.baudrate = int(baud)

# klasa portu
class Connection(Configure):
    def __init__(self, port, baud):
        super().__init__(port, baud)
        self.line = port

# Funkcja polaczenia z przystawka
def conecttodevice(line):
    # zmienna polaczenia
    global conect
    conect = line

    try:
	# Otwarcie portu
        conect.a.open()
        print("Port open - ", str(conect.a.isOpen()))
	
	# Powrot do menu
        comandportmenu()

    # Obsluga bledow
    except serial.SerialException:
        print("Sth Wrong! Try agin.")
        try:
	    # Zamkniecie portu
            conect.a.close()
            linkammenu()
        except Exception:
            print("Can not close port")

# Funkcja odczytu i wyswietlenia wszystkich informacji z portu
def readall():
    if conect.a.inWaiting() != 0:
        msg = conect.a.read(conect.a.inWaiting())
        print(msg)
	# Funkcja do wysylania wiadomosci
        manualsent()
    else:
        print("Nothing to read")
        manualsent()

# Funkcja odczytu i wyswietlenia temperatury
def getbytes():
    while True:
        if conect.a.inWaiting() == 11:
            msg = conect.a.read(conect.a.inWaiting())
	    # funkcja wewnatrz odczytuje teperature i transformuje do int
            print(readTemperature(msg))
            comandportmenu() # menu
            break
        if conect.a.inWaiting() != 11:
            continue
        if conect.a.inWaiting() == 0:
            comandportmenu() # menu
            break

# Odczyt temperarura-zwraca jako int
def readTemperature(bytestoread):
    temp = "".join(map(chr, bytestoread))
    temp = temp[:-1]
    temp = temp[8:]
    return(int(temp, 16) / 10)


# Menu-wysylanie bitow do przystawki
def manualsent():
    while True:
        print("-------------Manual Message sender---------------")
        print("-------Write message as string without CR--------")
        print("-------------------------------------------------")
        print("##      Set Ramp R{number}{C/min *100}         ##")
        print("##      Ramp Limit L{number}{limit *100}       ##")
        print("##      Ramp hold I{number}{t min}             ##")
        print("You can set two ramp for profile (number 1 and 2)")
        print("        For manual start profile sent S          ")
        print("        For manual  profile sent E               ")
        print("        Read in waiting send IW                  ")
        print("        Sent Q to back to main menu              ")

        message = input("Command: ")

	# Wyjscie
        if message == "Q":
            mainmenu()
            break

	# Odczyt bitow inWaiting
        if message == "IW":
            try:
                readall()
                break
            except:
                print("Nothing to read!")
                continue

        elif message != 0:
            toSent = message + "\r"
            try:
                conect.a.write(str.encode(toSent))
                time.sleep(0.1)
                readall()


            except:
                print("Sth Wrong! ", serial.writeTimeoutError)
                print("WARNING! Not send!")
                continue


# Obsluga portu
def comandportmenu():
    while True:
        print("--Lincam Conection Menu--")
        if conect.a.isOpen():
            message = input("T - Read Temperature\nW - Write message manual\nQ - Exit to Main\nC - Close Port")
	   
            # Wyjscie
            if message == "Q":
                mainmenu()
                break

	    # Wyslanie do kontrolera dowolnej wiadomosci
            if message == "W":
                try:
                    if conect.a.isOpen():
			# przekazanie do funkcji wyslania
                        manualsent()
                        break
                except:
                    print("WARNING! Port is not open!")

	    # Odczyt temperatury
            if message == "T":
                try:
                    conect.a.write(b'T\r')
                    time.sleep(0.1)
                    getbytes()
                    continue
                except serial.writeTimeoutError:
                    print("Sth Wrong! ")
                    print("WARNING! Not send!")
	
	    # Close port
            if message == "C":
                try:
                    if conect.a.isOpen():
                        conect.a.close()
                        print("Port open - ", conect.a.isOpen())
                except Exception.args:
                    print("Port open - ", conect.a.isOpen())

        else:
            print("Port is not open!")
            mainmenu() # menu glowne
            break


# Ustawinie numeru portu
def portnumber():
    while True:
        try:
            comnum = int(input("COM number? "))
        except ValueError:
            print("Only port number int 1-255 !")
            continue
        else:
            if comnum < 1 or comnum > 255:
                print("Only port number int 1-255 !")
                continue
            else:
                return "COM" + str(comnum)


# Ustawienie czestsci odczytu
def portrate():
    while True:
        try:
            rate = int(input("Baud? "))
        except ValueError:
            print("Baudrate must be int from the list:")
            print("9600, 14400, 19200")
            continue
        else:
            try:
                [9600, 14400, 19200].index(rate)
            except ValueError:
                print("Baudrate must be int from the list:")
                print("9600, 14400, 19200")
                continue
            else:
                return rate

# Obsluga zamkniecia programu
def getout():
    global getout

    while True:
        try:
            getout = int(input("YES - 1\nNO - 2\n"))
        except TypeError:
            print("There is no case ", getout)
            continue
        else:
            try:
                if getout == 1:
                    exit() # wyjsce
                if getout == 2:
                    getout = 0
                    mainmenu() # powrot do menu glownego
                    break
                else:
                    print("There is no case ", getout)
            except TypeError:
                print("Error!")
                input("Press any key!")

# Menu konfiguracji portu 
def linkammenu():
    global menuitem2
    global portnum, ratevalue
    global comline
    print("--Lincam Menu--")
    while True:
        try:
	    # wyswietlanie informacji
            menuitem2 = int(input("0 - Configurate Port\n1 - open port\n2 - close port\n3 - Send message\n4 - back\n"))
        except ValueError:
            print("There is no case ", menuitem2)
            continue
        else:
	    # Konfiguracja portu
            if menuitem2 == 0:
                portnum = portnumber()
                ratevalue = portrate()
                print("You choose ", portnum, " ", ratevalue)
                comline = Connection(portnum, ratevalue)
                linkammenu()
                break
	    # otwarcie portu
            if menuitem2 == 1:
                try:
                    conecttodevice(comline)
                except NameError:
                    print("Port is not configurated!")
                    mainmenu()
                break
	    # zamkniecie portu
            if menuitem2 == 2:
                try:
                    if conect.a.isOpen():
                        conect.a.close()
                except NameError:
                    print("Port closed")
                    mainmenu()
                    break
	    # wysylanie bitow
            if menuitem2 == 3:
                try:
                    if conect.a.isOpen():
			# Wywolanie funkcji do wysylania
                        comandportmenu()
                except NameError:
                    print("Port is not open!")
                    mainmenu()
                    break
	    # powrot do menu glownego
            if menuitem2 == 4:
                mainmenu()
                break


# ------------------- MAIN MENU -------------------#

# menu glowne
def mainmenu():
    global menuitem2
    i = 0

    print("--Main--")
    while True:
        try:
            menuitem2 = int(input("0 - Coneect Linkam\n1 - Coneect NIS\n2 - Make Log file\n3 - Start Loop\n4 - EXIT\n"))
        except ValueError:
            print("Wrong input!")
            continue
        else:
	    # menu polaczenia z kontrolerem
            if menuitem2 == 0:
                linkammenu()
                break

	    # menu laczenia z programem NIS
            if menuitem2 == 1:
                nismenu()
                break

	    # Menu tworzenia pliku LOG
            if menuitem2 == 2:
                makefile()
                break

	    # Startowanie petli pomiarowej
            if menuitem2 == 3:
                try:
                    if  loop_ready: #isstarted and conect.a.isOpen() and
                        while True:
                            try:
				# Wyslanie do programu NIS instrukcji przechwycenia zdjecia
                                wind.TypeKeys("{0}{1}".format("^", "{TAB}"))
                                mainloop(i)
				# Opoznienie petli o ustalony czas
                                time.sleep(time_sleep)
                                i = i+1
                                continue
                            except Exception:
                                print("Main Loop Error")
                                continue
                        break
                except Exception:
		    # Wyswietlenie instrukcji w przypadku braku konfiguracji 
                    print("Open port, Start application and set loop before start!")
                    continue

	    # wywolanie menu wyjscia z programu
            if menuitem2 == 4:
                getout()
                break


# ------------------- NIS MENU -------------------#

# menu konfiguracji obslugi nis
def nismenu():
    global menuitem2, app
    global wind, isstarted
    global location, name

    # Lokalizacja NIS
    location = r"C:\Program Files (x86)\NIS-Elements Viewer F\nis-f.exe"
    name = 'NIS-Elements Viewer F - [Live - Fast]'
    
    # zmienna kontroli uruchomienia NIS
    isstarted = False

    print("--NIS Menu--")
    while True:
        try:
	    # zmienna do wyboru startNIS, Wyslanie do NIS klawiszy, powrot do menu
            menuitem2 = int(input("0 - Add  location of the application\n1 - Start Application\n2 - Send Keys\n3 - back\n"))
        except ValueError:
            print("There is no case ", menuitem2)
            continue
        else:
	    # Ustawienie lokalizacji programu NIS
            if menuitem2 == 0:
                location = input("Add Location as r'LOCATION' : ")
                name = input("Add name as ['NAME']")
                print("You saved", location, name)
                continue
            # Uruchomienie programu NIS
            if menuitem2 == 1:
                try:
                    app = application.Application().start(location)
                    wind = app[name]
                    wind.SetFocus()
                    isstarted = True
                    continue
                except NameError:
                    print("Cant find application! ")
                    isstarted = False
                    mainmenu()
                    break
	    # Wyslanie do NIS '^ ' 
            if menuitem2 == 2:
                if isstarted:
                    try:
                        wind.TypeKeys("{0}{1}".format("^", "{SPACE}"))
                        continue
                    except Exception:
                        print("Error! App not started!")
                        continue
                else:
                    print("App not started!")
	    # powrot do menu glownego
            if menuitem2 == 3:
                mainmenu()
                break


# ------------------ LOOP SET ------------------#

# Menu ustawiania petli pomiaru
def makefile():
    global log_dictionary, name
    global time_sleep, loop_ready, dir_ready

    # Deklaracja wykresu
    global plot
    plot = plt.subplot(111)
    #plt.ion()

    dir_ready = False
    loop_ready = False
    dir_ready = False

    while True:
        print("---Log Settings---")
        try:
            menuitem3 = int(input("0 - Check directory\n1 - Change name and location\n2 - Set Loop\n3 - Back to main menu\n"))
            print(dir_ready)
        except ValueError:
            print("Wrong input!")
            continue
        else:
	    # Sprawdzenie lokalizacji zapisu pliku LOG
            if menuitem3 == 0:
                try:
                    print(log_dictionary , loop_ready)
                except NameError:
                    print("Configurate dictionary and name first!")
                input("Press any key...")
                makefile()
                print(dir_ready)
                break

	    # Zmiana lokalizacji i nazwy pliku LOG
            if menuitem3 == 1:
                try:
                    menuitem4 = int(input("0 - Load default name\n1 - Change directory"))
                except ValueError:
                    print("Wrong input!")
                    continue
		# Zaladowanie domyslnych ustawien
                if menuitem4 == 0:
                    name = time.strftime("\%d %b %Y %H-%M-%S")
                    log_dictionary = os.path.expanduser("{0}{1}{2}{3}".format("~", "\Desktop", name, ".txt"))
                    dir_ready = True
                    print(dir_ready)
                    continue

	        # Zapis nazwy pliku i lokalizacji zapisu LOG
                if menuitem4 == 1:
                    name = input("Write namefile: ")
                    log_dictionary = input("Write location to save log: ")
                    dir_ready = True
                    continue
                else:
                    makefile()
                    print(dir_ready)

	    # Ustawienie czasu opoznienia petli
            if menuitem3 == 2:
                if dir_ready:
                    time_sleep = float(input("Set time sleep for loop (sec): "))
                    loop_ready = True
                    continue
                else:
                    print("Set directory first!")
                    continue

	    # Powrot do menu glownego
            if menuitem3 == 3:
                mainmenu()
                break

    # wyswietlenie zapisanej lokalizacji zapisu log
    print(log_dictionary)


# ------------------ MAIN LOOP ------------------#

# Glowna petla pomiaru
def mainloop(i):
    # macierze do zapizu temperatury
    global logfile
    global xarray, yarray
    xarray = []
    yarray = []

    try:
	
        dic = log_dictionary
        a = os.path.join(dic)
        logfile = open(a, "a")
        conect.a.write(b'T\r') # pytanie o temperature
        time.sleep(0.02)
        readTemperature(conect.a.read(conect.a.inWaiting())) # odczytanie temperatury
        print(temp) # wypisanie temperatury
	# uaktualnienie macierzy z temperatura
        xarray.append(i)
        yarray.append(temp)
	# zapis danych do pliku 
        logfile.write("{0}\t{1}\t{2}\n".format(time.strftime("%d %b %Y %H:%M:%S"), temp, i))
        logfile.close()
	# wywolanie wykresu
        plotlive(xarray, yarray)
    except:
        print("Directory error! ")


# ------------------ PLOT ------------------#

# Uaktualnienie wykresu
def plotlive(x, y):
    plt.plot(x, y, 'ro-')
    plt.pause(0.0001)


# wywolanie menu glownego
mainmenu()
