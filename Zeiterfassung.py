import matplotlib
matplotlib.use('TkAgg', force=True)
from matplotlib import pyplot as p
#print("Switched to:", matplotlib.get_backend())
import csv
import tkinter as tk
from tkinter import messagebox as mb
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector as dbcon
import hashlib
import datetime as dt
from datetime import datetime, timedelta
import re
from PIL import Image, ImageTk as pil
import os
import pandas as pd


def center_window(win, x , y):
    """
    Fenster zentrieren und anpassen von Fenster.geometry
    
    Erwartet:  win - Name des Fensters
               x - Abstand von Desktopkante
               y - Abstand von Desktopkante
    """
    desktop_width = win.winfo_screenwidth() # Bekommen Desktop Breite
    desktop_height = win.winfo_screenheight() # Bekommen Desktop Höhe
    rest_width = (desktop_width - (desktop_width - x)) / 2 # Berechnen von Seiten Abstand
    rest_height = (desktop_width - (desktop_width - y)) / 2 # Berechnen von Seiten Abstand
    
    # Ändern Fenster.geometry
    win.geometry("%dx%d+%d+%d" % ((desktop_width - x), (desktop_height - y), rest_width, rest_height))
    # Fenster darf nicht Vergrößert wwerden
    win.resizable(0, 0)

def open_ini():
    """
    Offnet ini-file and erstellt eine liste aus Inhalt
    
    Gibt zuruck die liste
    """
    # Lese ini-file und einsetze erste 3 stellen als host, user und password
    with open("ini", "r") as file:
        for line in file:
            temp = line.strip().split(";")
    return temp

def connect_db():
    """
    Konnekt zu Localhost und Datenbank mit Daten aus ini
    """
    temp = open_ini()
    host = temp[0]
    user = temp[1]
    # Wenn password zu DB ist * --> der soll leer sein
    if temp[2] == "*" : password = ""
    else: password = temp[2]
    
    # Erstelle eine globale variable mit DB-Connection
    global myDB
    try:
        myDB = dbcon.connect(
            host = host,
            user = user,
            password = password
            )
    
    # Wenn Zeit ausreichen wird - alle print Warnungen mit Warnfenster ersetzen
    except dbcon.Error as err:
        print("Something went wrong: {}".format(err))
        try:
            print( "MySQL Error [%d]: %s" % (err.args[0], err.args[1]))
            return None
        except IndexError:
            print ("MySQL Error: %s" % str(err))
            return None
    except TypeError:
        print(err)
        return None
    except ValueError:
        print(err)
        return None
    return myDB

global countter
countter = 0

def loggin():
    """
    Wenn Connection mit DB existiert - nimmt Eingaben aus Login und
    Pass Felder und vergleicht dies mit Daten aus DB.
    Wenn es klappt - startet automatisch choose_gui() Function.
    Es gibt 3 Versuche sich zu Anmelden, wenn nicht - Schlisst sich Fenster
    """
    global validate_user
    global user_id
    countter = 0
    
    if myDB and countter < 3:
        mycursor = myDB.cursor()
        temp = open_ini()
  
        way_to_pass = "USE " + temp[3]  
        mycursor.execute(way_to_pass)
        
        way_to_pass2 = "SELECT * FROM " + temp[4]
        mycursor.execute(way_to_pass2)
 
        # Vergleiche Login und Pass mit Daten aus DB
        for x in mycursor:
            xtemp = str(x)
            xlog = xtemp.split("'")[1]
            xpass = xtemp.split("'")[3]
            # Wenn Login und Pass(in MD5 Form) stimmen
            if ein_login.get() == xlog and (hashlib.md5(ein_pass.get().encode('utf-8')).hexdigest()) == xpass: 
                # Setze Validate User auf True
                validate_user = True
                # Holle User_ID
                user_id = xtemp.split("'")[0]
                user_id = user_id.split("(")[1]
                user_id = user_id.split(",")[0]
                # Zerstörre Fenster mit Login
                fenster.destroy()
                # Starte GUI-Auswal Function
                choose_gui(validate_user, user_id)
                break
            else:
                # Setze Label über Fehlversuch
                lb_fehlschlag.place(x = 50, y = 10)
                fenster.update()
                validate_user = False
        # Incrementiere Countter
        countter += 1
    elif countter >= 3:
        # Schlisse MySQL Connection
        myDB.close()
        # Zerstörre gesamte Programm
        root.destroy()
    else: print("Hier else")
    
def choose_gui(validate_user, user_id):
    """
    Bekommt aus DB Kontotype_ID - für GUI Variante Laden
    1 - für Admin
    2 - für Erweiterte Benutzer
    3 - für Normale Benutzer
    
    4 - ist für Kontospeere ausgedacht, aber alles anderes außer 1, 2, 3 führ zum Sperrung
    """
    global realy_thisuser_id
    global temporaly
    global user_type
    
    connect_db()
    mycursor = myDB.cursor()
    temp = open_ini()
    way_to_pass = "USE " + temp[3]
    mycursor.execute(way_to_pass)
    
    way_to_user = "SELECT Kontotype_ID FROM mitarbeiter WHERE Login_ID = " + user_id + ";"
    mycursor.execute(way_to_user)
    temporaly_var = mycursor.fetchone()[0]
    
    way_to_id = "SELECT * FROM mitarbeiter WHERE Login_ID = " + user_id + ";"
    mycursor.execute(way_to_id)
    temporaly = mycursor.fetchall()
    realy_user_name = temporaly[0][1] + " " + temporaly[0][2]
    realy_thisuser_id = temporaly[0][0]
    
    if validate_user == True and temporaly_var != 0:
        
        if temporaly_var == 3:
            user_type = "no_admin"
            load_b_gui(realy_user_name)
        elif temporaly_var == 2:
            user_type = "no_admin"
            load_eb_gui()
        elif temporaly_var == 1:
            user_type = "admin"
            load_adm_gui()
        else: lb_hallo = ttk.Label(root, text = (" " * 30) + "Ihre Konto ist Gesperrt." + "\nBitte wenden Sie zu Geschäftsführung oder zum Administrator.", font="Verdana 16 bold").pack()
    else: print("Something is WRONG!")

def load_b_gui(value):
    """
    Erstellung Benutzer GUI
    """
    
    # Einstellungen von Menu
    men = ttk.Menu(root, background="#c9c9c9")
    root.config(menu=men, background="#c9c9c9")

    datei_m = ttk.Menu(men, tearoff=0, background="#c9c9c9")
    men.add_cascade(label="Datei", menu=datei_m)
    datei_m.add_command(label="Neu")
    datei_m.add_command(label="Schließen", command=root.quit)

    show_user_info(value)
    show_zieterf(realy_thisuser_id)
    
def load_eb_gui():
    """
    Erstellung Erweiterter Benutzer GUI
    """
    # Einstellungen von Menu
    men = ttk.Menu(root, background="#c9c9c9")
    root.config(menu=men, background="#c9c9c9")

    datei_m = ttk.Menu(men, tearoff=0, background="#c9c9c9")
    men.add_cascade(label="Datei", menu=datei_m)
    datei_m.add_command(label="Neu Anmelden")
    datei_m.add_command(label="Schließen", command=root.quit)

    lb_get_users = ttk.Label(root, text = "Mitarbeiter Liste laden: ", font= "Verdana 10", background="#c9c9c9").place(x = 20, y = 22)
    butt = ttk.Button(root, text="Get Liste", command=getdbuser)
    butt.place(x = 200, y = 20)
    
    show_zieterf(realy_thisuser_id)
    
def load_adm_gui():
    """
    Erstellung Admin GUI
    """
    # Einstellungen von Menu
    men = ttk.Menu(root, background="#c9c9c9")
    root.config(menu=men, background="#c9c9c9")

    datei_m = ttk.Menu(men, tearoff=0, background="#c9c9c9")
    men.add_cascade(label="Datei", menu=datei_m)
    datei_m.add_command(label="Neu Anmelden")
    datei_m.add_command(label="Schließen", command=root.quit)

    def show_buttons(event):
        butt_neu_user.place(x = 20, y = 470)
        butt_del_user.place(x = 140, y = 470)

    lb_get_users = ttk.Label(root, text = "Mitarbeiter Liste laden: ", font= "Verdana 10", background="#c9c9c9").place(x = 20, y = 22)
    butt = ttk.Button(root, text="Get Liste", command=getdbuser)
    butt.bind("<Button-1>", show_buttons)
    butt.place(x = 200, y = 20)

    show_zieterf(realy_thisuser_id)
    
def getdbuser():
    """
    Funktion erstellt Mitarbeiter Liste
    """
    connect_db()
    mycursor = myDB.cursor()
    temp = open_ini()
    way_to_pass = "USE " + temp[3]  
    mycursor.execute(way_to_pass)
    way_to_all = "SELECT * FROM mitarbeiter ORDER BY Mitarbeiter_ID;"
    mycursor.execute(way_to_all)
    global temporaly
    temporaly = mycursor.fetchall()
    for_list = []
    for line in temporaly:
        for_list.append(str(line[1] + " " + line[2]))
        
    listbox = tk.Listbox(root)
    [listbox.insert(END, item) for item in for_list]
    listbox.place(x = 20, y = 70, height= 380, width=250)
    listbox.bind('<<ListboxSelect>>', onselect)
    
def onselect(evt):
    """
    On Select in Mitarbeiter Liste +++
    +++ Startet Show User Info Function
    """
    try:
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        show_user_info(value)
        global selectet_user
        selectet_user = value
    except IndexError:
        pass    

def show_user_info(value):
    """
    Zeigt User Information
    """
    global user_name
    user_name = value.split(" ")

    for line in temporaly:
        global realy_user_id
        
        if user_name[0] == line[1] and user_name[1] == line[2]:
            realy_user_id = line[0]
            show_user_azeit(realy_user_id)
            abt_and_pos = get_abt_position(line[8], line[9])
            email = get_email(line[6])
            vertrag = get_vertrag(line[10])
            # Ziehe Adresse aus DB
            adresse_liste = get_adresse(line[5])
            # Konvertation von MySQL Geburtsdate Date in Normal Form
            geburtstag = []
            month_dict = {"01" : "Januar", "02" : "Februar", "03" : "März", "04" : "April", "05" : "Mai", "06" : "Juni", "07" : "Juli", "08" : "August", "09" : "September", "10" : "Oktober", "11" : "November", "12" : "Dezember"}
            geburtstag = str(line[3]).split("-")
            geburtstag_str = str(geburtstag[2]) + " " + str(month_dict[str(geburtstag[1])]) + " " + str(geburtstag[0])
            
            vertrag_start_str = str(vertrag[0][2]) + " " + str(month_dict[str(vertrag[0][1])]) + " " + str(vertrag[0][0])

            if vertrag[1][0] == "0000" and vertrag[1][1] == "00" and vertrag[1][2] == "00":
                vertrag_ende_str = "- kein -"
            else: vertrag_ende_str = str(vertrag[1][2]) + " " + str(month_dict[str(vertrag[1][1])]) + " " + str(vertrag[1][0])
            
            uber_st = get_uber(line[0])

            # Erstelle Frame für Info
            info_frame = ttk.Frame(root, relief= "flat")
            info_frame.place(x = 300, y = 20, width= 500, height= 480)
            # Mitarbeiter Information
            lb_ma_info = ttk.Label(info_frame, text = "Mitarbeiter Info:", font = "Verdana 10 bold").place(x=20, y=20)
            #lb_ma_nr = ttk.Label(info_frame, text = line[0], font = "Verdana 10").place(x=240, y=20)
            
            lb_ma_vorname = ttk.Label(info_frame, text = "Vorname:", font = "Verdana 8 bold").place(x=20, y=50)
            lb_ma_vorname_out = ttk.Label(info_frame, text = line[1], font = "Verdana 8").place(x=110, y=50)
            lb_ma_nachname = ttk.Label(info_frame, text = "Nachname:", font = "Verdana 8 bold").place(x=240, y=50)
            lb_ma_nachname_out = ttk.Label(info_frame, text = line[2], font = "Verdana 8").place(x=320, y=50)

            lb_ma_gebtag = ttk.Label(info_frame, text = "Geburtstag:", font = "Verdana 8 bold").place(x=20, y=80)
            lb_ma_gebtag_out = ttk.Label(info_frame, text = geburtstag_str, font = "Verdana 8").place(x=110, y=80)
            lb_ma_telefon = ttk.Label(info_frame, text = "Telefon Nr.:", font = "Verdana 8 bold").place(x=240, y=80)
            lb_ma_telefon_out = ttk.Label(info_frame, text = line[4], font = "Verdana 8").place(x=320, y=80)

            lb_ma_adresse = ttk.Label(info_frame, text = "Adresse:", font = "Verdana 8 bold").place(x=20, y=110)
            lb_ma_strasse_out = ttk.Label(info_frame, text = adresse_liste[0][1], font = "Verdana 8").place(x=110, y=110)
            lb_ma_haus_out = ttk.Label(info_frame, text = adresse_liste[0][2], font = "Verdana 8").place(x=200, y=110)
            lb_ma_ort_out = ttk.Label(info_frame, text = adresse_liste[0][3], font = "Verdana 8").place(x=110, y=130)
            lb_ma_plz_out = ttk.Label(info_frame, text = adresse_liste[0][4], font = "Verdana 8").place(x=110, y=150)
    
            lb_ma_abteilung = ttk.Label(info_frame, text = "Abteilung:", font = "Verdana 8 bold").place(x=20, y=180)
            lb_ma_abteilung_out = ttk.Label(info_frame, text = abt_and_pos[0], font = "Verdana 8").place(x=110, y=180)
            lb_ma_position = ttk.Label(info_frame, text = "Position:", font = "Verdana 8 bold").place(x=240, y=180)
            lb_ma_position_out = ttk.Label(info_frame, text = abt_and_pos[1], font = "Verdana 8").place(x=320, y=180)

            lb_ma_vertrag = ttk.Label(info_frame, text = "Vertrag:", font = "Verdana 8 bold").place(x=20, y=210)
            lb_ma_vertrag_out = ttk.Label(info_frame, text = vertrag[2], font = "Verdana 8").place(x=110, y=210)
            lb_ma_ver_art = ttk.Label(info_frame, text = "Art", font = "Verdana 8 bold").place(x=240, y=210)
            lb_ma_ver_art_out = ttk.Label(info_frame, text = vertrag[3], font = "Verdana 8").place(x=320, y=210)
            lb_ma_vertb = ttk.Label(info_frame, text = "Beginn:", font = "Verdana 8 bold").place(x=20, y=240)
            lb_ma_vertb_out = ttk.Label(info_frame, text = vertrag_start_str, font = "Verdana 8").place(x=110, y=240)
            lb_ma_verte = ttk.Label(info_frame, text = "Ende:", font = "Verdana 8 bold").place(x=240, y=240)
            lb_ma_verte_out = ttk.Label(info_frame, text = vertrag_ende_str, font = "Verdana 8").place(x=320, y=240)
            lb_ma_gehalt = ttk.Label(info_frame, text = "Gehalt:", font = "Verdana 8 bold").place(x=20, y=270)
            lb_ma_gehalt_out = ttk.Label(info_frame, text = vertrag[4], font = "Verdana 8").place(x=110, y=270)
            lb_ma_gehalt = ttk.Label(info_frame, text = "Email:", font = "Verdana 8 bold").place(x=20, y=300)
            lb_ma_gehalt_out = ttk.Label(info_frame, text = email, font = "Verdana 8").place(x=110, y=300)
            lb_ma_ubk = ttk.Label(info_frame, text = "Überstundenkonto:", font = "Verdana 8 bold").place(x=20, y=330)
            lb_ma_ubk_out = ttk.Label(info_frame, text = uber_st, font = "Verdana 8").place(x=170, y=330)
            
            if user_type == "admin":
                but_ma_edit = ttk.Button(info_frame, text = "Info Ändern", command=edit_user)
                but_ma_edit.place(x = 385, y = 430)
            else:pass
            
def show_user_azeit(value):
    
    def get_zeit_data(value):
        global way
        mycursor = myDB.cursor() 
        way = "SELECT `Tag`, `Startzeit`, `Endzeit`, `Tarif_ID`, `Überstunden` FROM `arbeitszeiten` WHERE `Mitarbeiter_ID` = " + str(value)
        mycursor.execute(way)
        global all_data
        all_data = mycursor.fetchall()
        
        month_lst = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
 
        def get_time_now(tag):
            t = tag
            new_t = str(t).split(" ")
            new_t = new_t[0].split("-")
            new_t = new_t[2] + " " + month_lst[int(new_t[1])-1] + " " + new_t[0]
            return new_t
        
        for data in all_data:
            tag = get_time_now(data[0])
            tab.insert("", "end", values=(tag, data[1], data[2], data[3], data[4]))
    
    # global show_swich
    # show_swich = True

    # def show_stat():
    #     global show_swich
        
    #     if show_swich:
    #         import_csv.place(x = 20, y = 595, width = 250)
    #         lb_show = ttk.Label(root, text="für Tagen:")
    #         lb_show.place(x = 20, y = 575, width = 250)
    #         ein_show = ttk.Entry(root)
    #         show_swich = False
            
    #     else:
    #         import_csv.place(x = 20, y = 552, width = 250)
    #         show_swich = True

    def show_stat():
        
        n = datetime.now()

        a_tagen = []
        a_zeiten = []
        k_tagen = []
        k_zeiten = []
        
        for data in all_data:
            if data[3] == 1:
                day_from_data = datetime.strptime(str(data[0]),'%Y-%m-%d')
                rest = n - day_from_data
                max_days = timedelta(days=31)
                if rest < max_days:
                    a_tagen.append(data[0])
                    z = str(data[2]).split(":")
                    x = z[0] + "." + z[1]
                    a_zeiten.append(float(x))
                
        for data in all_data:
            if data[3] == 3:
                day_from_data = datetime.strptime(str(data[0]),'%Y-%m-%d')
                rest = n - day_from_data
                max_days = timedelta(days=31)
                if rest < max_days:
                    k_tagen.append(data[0])
                    z = str(data[2]).split(":")
                    x = z[0] + "." + z[1]
                    k_zeiten.append(float(x))
        
        p.plot(a_tagen, a_zeiten, label = "Arbeitstage")
        p.plot(k_tagen, k_zeiten, label = "Krank")
        
        p.legend() 
        p.show()
        
    def to_pdf(): pass
        #df = pd.read_sql(way, myDB)
        #time_zp = datetime.now()
        #pdf_file =  "pdf_" + str(user_name) + str(time_zp) + ".pdf"
        #fig, ax = p.subplots()
        #ax.axis("tight")
        #ax.axis("off")
        #ax.table(cellText = df.values, collabels = df.columns, loc = "center")
        #p.savefig(pdf_file, format="pdf")


    def to_csv():
        time_zp = datetime.now()
        file_path = "arbeitszeiten" + str(user_name[0]) + str(user_name[1]) + ".csv"
        with open(file_path, mode='a', newline='') as file:
            csv_writer = csv.writer(file, dialect="excel", delimiter=",", quotechar='|')
            for row_id in tab.get_children():
                row_data = tab.item(row_id)["values"]
                csv_writer.writerow(row_data)

    show_graph = ttk.Button(root, text = "Statistik", command=show_stat)
    show_graph.place(x = 20, y = 522, width = 250)
    
    #import_pdf = ttk.Button(root, text = "Import to PDF", command=to_pdf)
    #import_pdf.place(x = 20, y = 552, width = 250)
    
    import_csv = ttk.Button(root, text = "Import to CSV", command=to_csv)
    import_csv.place(x = 20, y = 552, width = 250)

    tab_frame = ttk.Frame(root, relief= "flat")
    tab_frame.place(x = 300, y = 520, width= 836, height= 155)
    
    tab = ttk.Treeview(tab_frame, columns=(1,2,3,4,5), height=8, show="headings")
    
    tab.column(1, anchor=CENTER, stretch=NO, width=160)
    tab.column(2, anchor=CENTER, stretch=NO, width=180)
    tab.column(3, anchor=CENTER, stretch=NO, width=180)
    tab.column(4, anchor=CENTER, stretch=NO, width=160)
    tab.column(5, anchor=CENTER, stretch=NO, width=156)
    
    tab.heading(1, text = "Tag")
    tab.heading(2, text = "Start Zeit")
    tab.heading(3, text = "End Zeit")
    tab.heading(4, text = "Tarif")
    tab.heading(5, text = "Überstunden")
    
    get_zeit_data(value)
    
    tab.place(x = 0, y = 0)
           
def get_email(log_id):
    mycursor = myDB.cursor()
    temp = open_ini()
    way_to_pass = "USE " + temp[3]  
    mycursor.execute(way_to_pass)
    ask_db_vert = "SELECT E_Mail FROM login WHERE Login_ID = " + str(log_id)
    mycursor.execute(ask_db_vert)
    email = mycursor.fetchone()
    return email

def get_vertrag(vert_id):
    """
    Zieht User Alles über Vertrag aus DB
    """
    mycursor = myDB.cursor()
    temp = open_ini()
    way_to_pass = "USE " + temp[3]  
    mycursor.execute(way_to_pass)
    ask_db_vert = "SELECT * FROM arbeitsvertrag WHERE Arbeitsvertrag_ID = " + str(vert_id)
    mycursor.execute(ask_db_vert)
    
    result_vert = []
    for x in mycursor:
        result_vert.append(x)
        
    new_res = []
    new_res.append(str(result_vert[0][1]).split("-"))
    
    if result_vert[0][2] == None: new_res.append(["0000","00","00"])
    else: new_res.append(str(result_vert[0][2]).split("-"))
    
    ask_db_art = "SELECT Vertragsart_name FROM vertragsart WHERE Vertragsart_ID = " + str(result_vert[0][4])
    mycursor.execute(ask_db_art)
    result_art = []
    for x in mycursor:
        result_art.append(x)

    ask_db_be = "SELECT Beschäftigung_name FROM beschäftigung WHERE Beschäftigung_ID = " + str(result_vert[0][3])
    mycursor.execute(ask_db_be)
    result_be = []
    for x in mycursor:
        result_be.append(x)
    
    result = []
    result.append(str(result_art[0]).split("'"))
    result.append(str(result_be[0]).split("'"))
    new_res.append(str(result[0][1]))
    new_res.append(str(result[1][1]))
    new_res.append(result_vert[0][5])
    new_res.append(result_vert[0][3])
    new_res.append(result_vert[0][4])
    return new_res

def get_abt_position(ab_id, pos_id):
    """
    Zieht User Abteilung und Position aus DB
    """
    mycursor = myDB.cursor()
    temp = open_ini()
    way_to_pass = "USE " + temp[3]  
    mycursor.execute(way_to_pass)
    ask_db_abteilung = "SELECT Abteilung_name FROM abteilung WHERE Abteilung_ID = " + str(ab_id)
    mycursor.execute(ask_db_abteilung)
    result_abt = []
    for x in mycursor:
        result_abt.append(x)
        
    ask_db_pos = "SELECT Position_name FROM position WHERE Position_ID = " + str(pos_id)
    mycursor.execute(ask_db_pos)
    result_pos = []
    for x in mycursor:
        result_pos.append(x)
        
    result = []
    result.append(str(result_abt[0]).split("'"))
    result.append(str(result_pos[0]).split("'"))
    new_res = []
    new_res.append(str(result[0][1]))
    new_res.append(str(result[1][1]))
    return new_res

def get_adresse(adrs_id):
    """
    Zieht User Adresse aus DB
    """
    mycursor = myDB.cursor()
    temp = open_ini()
    way_to_pass = "USE " + temp[3]  
    mycursor.execute(way_to_pass)
    ask_db_adress = "SELECT * FROM adresse WHERE Adresse_ID = " + str(adrs_id)
    mycursor.execute(ask_db_adress)
    result = []
    for x in mycursor:
        result.append(x)
    return result

def get_uber(realy_thisuser_id):
    mycursor = myDB.cursor()
    temp = open_ini()
    way_to_pass = "USE " + temp[3]  
    mycursor.execute(way_to_pass)
    ask_db_uber = "SELECT `Überstunden` FROM `arbeitszeiten` WHERE `Mitarbeiter_ID` = " + str(realy_thisuser_id)
    mycursor.execute(ask_db_uber)
    answ_db = []
    answ_db_uber = 0
    for x in mycursor:
        answ_db.append(x)

    for y in range(len(answ_db)):
        answ_db_uber += answ_db[y][0]

    return answ_db_uber

class add_user_gui(ttk.Toplevel):
    """
    Subclass von Toplevel - Neu Mitarbeiter Hinzufügen
    Erstellt ein Fenster mit eingaben möglichkeiten
    """
 
    def __init__(self, master):

        def way_to_somewehere(tab):
            way_to_temp = "SELECT * FROM " + str(tab)
            mycursor.execute(way_to_temp)
            some = []
            for line in mycursor:
                some.append(line[1])
            return some
        
        def abteilung_ausgeben(event):
            global abteilung
            abteilung = ein_ten.get()
            return abteilung
    
        def position_ausgeben(event):
            global position
            position = ein_elf.get()
            return position

        def vertrag_ausgeben(event):
            global vertrag
            vertrag = ein_zwo.get()
            return vertrag
    
        def beschaf_ausgeben(event):
            global beschaf
            beschaf = ein_dre.get()
            return beschaf
    
        def rolle_ausgeben(event):
            global rolle
            rolle = ein_she.get()
            return rolle
            
        def email_value(event):
            if ein_uno.get() != "" and ein_duo.get() != "":
                fname = ein_uno.get()
                sname = ein_duo.get()
                global email
                email = fname.lower() + "." + sname.lower() + "@finck-maier-consulting.de"
                lb_lk.config(text = email)
                return email
                
        def password_check(password):
            """
            Verify the strength of 'password'
            Returns a dict indicating the wrong criteria
            A password is considered strong if:
                8 characters length or more
                1 digit or more
                1 symbol or more
                1 uppercase letter or more
                1 lowercase letter or more
            """

            # calculating the length
            length_error = len(password) < 8

            # searching for digits
            digit_error = re.search(r"\d", password) is None

            # searching for uppercase
            uppercase_error = re.search(r"[A-Z]", password) is None

            # searching for lowercase
            lowercase_error = re.search(r"[a-z]", password) is None

            # searching for symbols
            symbol_error = re.search(r"\W", password) is None

            # overall result
            password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

            return {
                'password_ok' : password_ok,
                'length_error' : length_error,
                'digit_error' : digit_error,
                'uppercase_error' : uppercase_error,
                'lowercase_error' : lowercase_error,
                'symbol_error' : symbol_error,
            }
            
        def pass_check(event):
            if len(ein_akt.get()) != 0:
                temp = ein_akt.get()
                passwort = password_check(temp)
                if passwort["password_ok"] == True: 
                    mb.showinfo(title="Its OK", message="Passwort is Gut!", parent=self)
                    global new_pass
                    new_pass = hashlib.md5(temp.encode('utf-8')).hexdigest()
                    return new_pass
                elif passwort["length_error"] == True: mb.showwarning(title="Error", message="Passwort soll mindestens 8 Zeichen lang sein", parent=self)
                elif passwort["digit_error"] == True or passwort["uppercase_error"] == True or passwort["lowercase_error"] == True or passwort["symbol_error"] == True:
                    mb.showwarning(title="Error", message="Passwort soll aus Groß- und Kleinbuchstaben, Ziffern sowie Sonderzeichen bestehen", parent=self)
                else: print("Was war das?")
            else: return None
            
        def condate(test):
            """
            Konvertiere Date in DB Format
            """
            import datetime

            def conv_date(test, x):
                test = test.split(x)
                date = datetime.datetime(int(test[2]), int(test[1]), int(test[0]))
                return date

            if len(test.split(",")) > 2 : d = conv_date(test, ",")
            elif len(test.split(".")) > 2: d = conv_date(test, ".")
            elif len(test.split("/")) > 2: d = conv_date(test, "/")
            else: d = None

            return d
            
        def samle_all():
            """
            all_in_one :
            #vorname = [0]
            #nachname = [1]
            #geburt = [2]
            #telefon = [3]
            #strasse = [4]
            #hausnr = [5]
            #plz = [6]
            #ort = [7]
            #abteilung_id = [8]
            #position_id = [9]
            #vertrag_id = [10]
            #beschaf_id = [11]
            #rolle_id = [12]
            #email = [13]
            #passwort = [14]
            #gehalt = [15]
            #vertragsbeginn = [16]
            #vertragsende = [17]
            """
            all_in_one = []
            all_in_one.append(ein_uno.get())
            all_in_one.append(ein_duo.get())
            
            # Umwandle Datum
            test = ein_tre.get()
            bdate = condate(test)
            all_in_one.append(bdate)
            
            #all_in_one.append()
            all_in_one.append(ein_qwa.get())
            
            all_in_one.append(ein_qwi.get())
            all_in_one.append(ein_sex.get())
            all_in_one.append(ein_che.get())
            all_in_one.append(ein_nen.get())

            # Get Abteilung_ID
            get_abt = "SELECT Abteilung_ID FROM abteilung WHERE Abteilung_name = '" + abteilung + "';"
            mycursor.execute(get_abt)
            abteilung_id = mycursor.fetchone()
            all_in_one.append(abteilung_id)
            
            # Get Position_ID
            get_pos = "SELECT `Position_ID` FROM `position` WHERE `Position_name` = '" + position + "';"
            mycursor.execute(get_pos)
            position_id = mycursor.fetchone()
            all_in_one.append(position_id)
            
            # Get Vertrag_ID
            get_ver = "SELECT `Vertragsart_ID` FROM `vertragsart` WHERE `Vertragsart_name` = '" + vertrag + "';"
            mycursor.execute(get_ver)
            vertrag_id = mycursor.fetchone()
            all_in_one.append(vertrag_id)
            
            # Get Beschäftigung_ID
            get_bes = "SELECT `Beschäftigung_ID` FROM `beschäftigung` WHERE `Beschäftigung_name` = '" + beschaf + "';"
            mycursor.execute(get_bes)
            beschaf_id = mycursor.fetchone()
            all_in_one.append(beschaf_id)
            
            # Get Rolle
            get_roll = "SELECT `Kontotype_ID` FROM `kontotype` WHERE `Kontotype_name` = '" + rolle + "';"
            mycursor.execute(get_roll)
            rolle_id = mycursor.fetchone()
            all_in_one.append(rolle_id)
            
            all_in_one.append(email)
            all_in_one.append(new_pass)

            all_in_one.append(ein_non.get())
            
            test2 = ein_vie.get()
            vdate = condate(test2)
            all_in_one.append(vdate)
            test3 = ein_fun.get()
            edate = condate(test3)
            all_in_one.append(edate)

            return all_in_one

        def send_an_db():

            all_for_send = samle_all()
            check_bereitschaft = mb.askyesno(title="Bereitschaft", message="Sind Sie sicher?", parent=self)
            if check_bereitschaft and all_for_send:
                 
                # Get Last Mitarbeiter_ID
                get_last_ma_id = "SELECT * FROM `mitarbeiter` ORDER BY mitarbeiter.Mitarbeiter_ID DESC LIMIT 1;"
                mycursor.execute(get_last_ma_id)
                last_ma_id_old = mycursor.fetchone()
                
                # Send Adresse
                send_adress = "INSERT INTO `Adresse` (`Straße`, `HausNr`, `Ort`, `PLZ`) VALUES ('" + str(all_for_send[4]) + "'," + str(all_for_send[5]) + ",'" + str(all_for_send[7]) + "','" + str(all_for_send[6]) + "');"
                try:
                    # Execute the SQL command
                    mycursor.execute(send_adress)
                    # Commit your changes in the database
                    myDB.commit()
                except:
                    # Roll back in case there is any error
                    myDB.rollback()
                # Get Last Adresse_ID
                get_last_id = "SELECT * FROM adresse ORDER BY `Adresse_ID` DESC LIMIT 1;"
                mycursor.execute(get_last_id)
                adress_id = mycursor.fetchone()
                
                # Send Arbeitsvertrag
                send_vert = "INSERT INTO `arbeitsvertrag` (`Vertragsbeginn`, `Vertragsende`, `Beschäftigung_ID`, `Vertragsart_ID`, `Gehalt`) VALUES ('" + str(all_for_send[16]) + "','" + str(all_for_send[17]) + "'," + str(all_for_send[11][0]) + "," + str(all_for_send[10][0]) + "," + str(all_for_send[15]) + ");"
                try:
                    # Execute the SQL command
                    mycursor.execute(send_vert)
                    # Commit your changes in the database
                    myDB.commit()
                except:
                    # Roll back in case there is any error
                    myDB.rollback()
                # Get Last Arbeitsvertrag_ID
                get_last_id = "SELECT * FROM arbeitsvertrag ORDER BY `Arbeitsvertrag_ID` DESC LIMIT 1;"
                mycursor.execute(get_last_id)
                vertrag_id = mycursor.fetchone()
                
                # Send Login
                send_log = "INSERT INTO `login`(`E_Mail`, `Password`) VALUES ('" + str(all_for_send[13]) + "','" + str(all_for_send[14]) + "');"
                try:
                    # Execute the SQL command
                    mycursor.execute(send_log)
                    # Commit your changes in the database
                    myDB.commit()
                except:
                    # Roll back in case there is any error
                    myDB.rollback()
                # Get Last Arbeitsvertrag_ID
                get_last_id = "SELECT * FROM login ORDER BY `Login_ID` DESC LIMIT 1;"
                mycursor.execute(get_last_id)
                log_id = mycursor.fetchone()
                
                # Send Login
                send_mit = "INSERT INTO `mitarbeiter`(`Vorname`, `Nachname`, `Geburtsdatum`, `Telefonnummer`, `Adresse_ID`, `Login_ID`, `Kontotype_ID`, `Abteilung_ID`, `Position_ID`, `Arbeitsvertrag_ID`) VALUES ('" + str(all_for_send[0]) + "','" + str(all_for_send[1]) + "','" + str(all_for_send[2]) + "'," + str(all_for_send[3]) + "," + str(adress_id[0]) + "," + str(log_id[0]) + "," + str(all_for_send[12][0]) + "," + str(all_for_send[8][0]) + "," + str(all_for_send[9][0]) + "," + str(vertrag_id[0]) + ");"
                try:
                    # Execute the SQL command
                    mycursor.execute(send_mit)
                    # Commit your changes in the database
                    myDB.commit()
                except:
                    # Roll back in case there is any error
                    myDB.rollback()
                    
                # Get New Last Mitarbeiter_ID
                mycursor.execute(get_last_ma_id)
                last_ma_id_new = mycursor.fetchone()

                we_mad_it = last_ma_id_old[0] < last_ma_id_new[0]
                
                if we_mad_it:
                    its_ok = mb.showinfo(title="Its OK", message="Its OK!", parent=self)
                else: mb.showinfo(title="Trubbles", message="We Have Trubbles!", parent=self)
                
                if we_mad_it and its_ok: self.destroy()

        connect_db()
        mycursor = myDB.cursor()
        temp = open_ini()
        way_to_pass = "USE " + temp[3]  
        mycursor.execute(way_to_pass)
        
        rollen_liste = []
        rollen_liste = way_to_somewehere("kontotype")
            
        vertrag_liste = []
        vertrag_liste = way_to_somewehere("vertragsart")

        beschaf_liste = []
        beschaf_liste = way_to_somewehere("beschäftigung")
        
        abteilung_liste = []
        abteilung_liste = way_to_somewehere("abteilung")
        
        position_liste = []
        position_liste = way_to_somewehere("position")

        self = ttk.Toplevel()
        self.title("Add New User")
        center_window(self, 1100, 140)
        self.attributes("-topmost", "True")

        # Erstellen des Label für die Überschrift
        title_label = ttk.Label(self, text="Neuer Mitarbeiter Information", font=("Verdana", 10, "bold"))
        title_label.place(x = 30, y = 20)

        # Erstellen der Labels für die Mitarbeiterinformationen
        fields = ["Vorname:", "Nachname:", "Geburtstag:", "Telefonnummer:", "Straße:", "Hausnummer:", "PLZ:", "Ort:", "Abteilung:", "Position:", "Vertragsart:", "Beschäftigung:", "Vertragsbeginn:", "Vertragsende:", "Kontotyp:", "Email:", "Passwort:", "Gehalt:"]

        label_uno = ttk.Label(self, text=fields[0], font = "Verdana 8 bold")
        label_duo = ttk.Label(self, text=fields[1], font = "Verdana 8 bold")
        label_tre = ttk.Label(self, text=fields[2], font = "Verdana 8 bold")
        label_qwa = ttk.Label(self, text=fields[3], font = "Verdana 8 bold")
        label_qwi = ttk.Label(self, text=fields[4], font = "Verdana 8 bold")
        label_sex = ttk.Label(self, text=fields[5], font = "Verdana 8 bold")
        label_che = ttk.Label(self, text=fields[6], font = "Verdana 8 bold")
        label_nen = ttk.Label(self, text=fields[7], font = "Verdana 8 bold")
        label_ten = ttk.Label(self, text=fields[8], font = "Verdana 8 bold")
        label_elf = ttk.Label(self, text=fields[9], font = "Verdana 8 bold")
        label_zwo = ttk.Label(self, text=fields[10], font = "Verdana 8 bold")
        label_dre = ttk.Label(self, text=fields[11], font = "Verdana 8 bold")
        label_vie = ttk.Label(self, text=fields[12], font = "Verdana 8 bold")
        label_fun = ttk.Label(self, text=fields[13], font = "Verdana 8 bold")
        label_she = ttk.Label(self, text=fields[14], font = "Verdana 8 bold")
        label_sib = ttk.Label(self, text=fields[15], font = "Verdana 8 bold")
        label_akt = ttk.Label(self, text=fields[16], font = "Verdana 8 bold")
        label_non = ttk.Label(self, text=fields[17], font = "Verdana 8 bold")
        
        label_uno.place(x = 30, y = 50)
        label_duo.place(x = 250, y = 50)
        label_tre.place(x = 30, y = 100)
        label_qwa.place(x = 250, y = 100)
        label_qwi.place(x = 30, y = 150)
        label_sex.place(x = 250, y = 150)
        label_che.place(x = 30, y = 200)
        label_nen.place(x = 250, y = 200)
        label_ten.place(x = 30, y = 250)
        label_elf.place(x = 250, y = 250)
        label_zwo.place(x = 30, y = 300)
        label_dre.place(x = 250, y = 300)
        label_vie.place(x = 30, y = 350)
        label_fun.place(x = 250, y = 350)
        label_she.place(x = 30, y = 400)
        label_sib.place(x = 30, y = 450)
        label_akt.place(x = 30, y = 500)
        label_non.place(x = 30, y = 550)

        ein_uno = ttk.Entry(self)
        ein_duo = ttk.Entry(self)
        ein_tre = ttk.Entry(self)
        ein_qwa = ttk.Entry(self)
        ein_qwi = ttk.Entry(self)
        ein_sex = ttk.Entry(self)
        ein_che = ttk.Entry(self)
        ein_nen = ttk.Entry(self)

        ein_ten = ttk.Combobox(self, value = abteilung_liste)
        ein_ten.current(0)
        ein_ten.config(state="readonly")
        ein_ten.bind("<<ComboboxSelected>>", abteilung_ausgeben)

        ein_elf = ttk.Combobox(self, value = position_liste)
        ein_elf.current(0)
        ein_elf.config(state="readonly")
        ein_elf.bind("<<ComboboxSelected>>", position_ausgeben)

        ein_zwo = ttk.Combobox(self, value = vertrag_liste)
        ein_zwo.current(0)
        ein_zwo.config(state="readonly")
        ein_zwo.bind("<<ComboboxSelected>>", vertrag_ausgeben)

        ein_dre = ttk.Combobox(self, value = beschaf_liste)
        ein_dre.current(0)
        ein_dre.config(state="readonly")
        ein_dre.bind("<<ComboboxSelected>>", beschaf_ausgeben)

        ein_vie = ttk.Entry(self)
        ein_fun = ttk.Entry(self)

        ein_she = ttk.Combobox(self, value = rollen_liste)
        ein_she.current(0)
        ein_she.config(state="readonly")
        ein_she.bind("<<ComboboxSelected>>", rolle_ausgeben)

        ein_akt = ttk.Entry(self)
        ein_non = ttk.Entry(self)

        ein_uno.place(x = 30, y = 70)
        ein_duo.place(x = 250, y = 70)
        ein_tre.place(x = 30, y = 120)
        ein_qwa.place(x = 250, y = 120)
        ein_qwi.place(x = 30, y = 170)
        ein_sex.place(x = 250, y = 170)
        ein_che.place(x = 30, y = 220)
        ein_nen.place(x = 250, y = 220)
        ein_ten.place(x = 30, y = 270)
        ein_elf.place(x = 250, y = 270)
        ein_zwo.place(x = 30, y = 320)
        ein_dre.place(x = 250, y = 320)
        ein_vie.place(x = 30, y = 370)
        ein_fun.place(x = 250, y = 370)
        ein_she.place(x = 30, y = 420)
        ein_akt.place(x = 30, y = 520)
        ein_non.place(x = 30, y = 570)
        
        lb_lk = ttk.Label(self, text = "")
        lb_lk.place(x = 30, y = 470)
        ein_duo.bind('<Return>', email_value)
        ein_akt.bind('<Return>', pass_check)
        
        but_send = ttk.Button(self, text = "Anlegen", command=send_an_db)
        but_send.place(x = 30, y = 650)

def edit_user():
    
    class WPEntry(tk.Entry):
        def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
            super().__init__(master)

            self.placeholder = placeholder
            self.placeholder_color = color
            self.default_fg_color = self['fg']

            self.bind("<FocusIn>", self.foc_in)
            self.bind("<FocusOut>", self.foc_out)

            self.put_placeholder()

        def put_placeholder(self):
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

        def foc_in(self, *args):
            if self['fg'] == self.placeholder_color:
                self.delete('0', 'end')
                self['fg'] = self.default_fg_color

        def foc_out(self, *args):
            if not self.get():
                self.put_placeholder()
    
    class edit_user_gui(ttk.Toplevel):
        """
        
        """
 
        def __init__(self, master, user_lst, adress_lst, v_lst):

            import re
            from tkinter import messagebox as mb
         
            def way_to_somewehere(tab):
                way_to_temp = "SELECT * FROM " + str(tab)
                mycursor.execute(way_to_temp)
                some = []
                for line in mycursor:
                    some.append(line[1])
                return some
        
            def abteilung_ausgeben(event):
                global abteilung
                abteilung = ein_ten.get()
                return abteilung
    
            def position_ausgeben(event):
                global position
                position = ein_elf.get()
                return position

            def vertrag_ausgeben(event):
                global vertr
                vertr = ein_zwo.get()
                return vertr
    
            def beschaf_ausgeben(event):
                global beschaf
                beschaf = ein_dre.get()
                return beschaf
    
            def rolle_ausgeben(event):
                global rolle
                rolle = ein_she.get()
                return rolle
            
            def email_value(event):
                if ein_uno.get() != "" and ein_duo.get() != "":
                    fname = ein_uno.get()
                    sname = ein_duo.get()
                    global email
                    email = fname.lower() + "." + sname.lower() + "@finck-maier-consulting.de"
                    lb_lk.config(text = email)
                    return email
                
            def password_check(password):
                """
                Verify the strength of 'password'
                Returns a dict indicating the wrong criteria
                A password is considered strong if:
                    8 characters length or more
                    1 digit or more
                    1 symbol or more
                    1 uppercase letter or more
                    1 lowercase letter or more
                """

                # calculating the length
                length_error = len(password) < 8

                # searching for digits
                digit_error = re.search(r"\d", password) is None

                # searching for uppercase
                uppercase_error = re.search(r"[A-Z]", password) is None

                # searching for lowercase
                lowercase_error = re.search(r"[a-z]", password) is None

                # searching for symbols
                symbol_error = re.search(r"\W", password) is None

                # overall result
                password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

                return {
                    'password_ok' : password_ok,
                    'length_error' : length_error,
                    'digit_error' : digit_error,
                    'uppercase_error' : uppercase_error,
                    'lowercase_error' : lowercase_error,
                    'symbol_error' : symbol_error,
                }
            
            def pass_check(event):
                if len(ein_akt.get()) != 0:
                    temp = ein_akt.get()
                    passwort = password_check(temp)
                    if passwort["password_ok"] == True: 
                        mb.showinfo(title="Its OK", message="Passwort is Gut!", parent=self)
                        global new_pass
                        new_pass = hashlib.md5(temp.encode('utf-8')).hexdigest()
                        return new_pass
                    elif passwort["length_error"] == True: mb.showwarning(title="Error", message="Passwort soll mindestens 8 Zeichen lang sein", parent=self)
                    elif passwort["digit_error"] == True or passwort["uppercase_error"] == True or passwort["lowercase_error"] == True or passwort["symbol_error"] == True:
                        mb.showwarning(title="Error", message="Passwort soll aus Groß- und Kleinbuchstaben, Ziffern sowie Sonderzeichen bestehen", parent=self)
                    else: print("Was war das?")
                else: return None
            
            def condate(test):
                """
                Konvertiere Date in DB Format
                """
                #import datetime
                
                def conv_date(test, x):
                    test = test.split(x)
                    date = datetime(int(test[2]), int(test[1]), int(test[0]))
                    return date

                if type(test) is not datetime:
                    if len(test.split(",")) > 2 : d = conv_date(test, ",")
                    elif len(test.split(".")) > 2: d = conv_date(test, ".")
                    elif len(test.split("/")) > 2: d = conv_date(test, "/")
                    else: d = None
                else: return test
                return d
            
            def conv_date_new():
                if v_lst[1][0] == "0000": end_date = "- kein -"
                else: end_date = dt.date(int(v_lst[1][0]), int(v_lst[1][1]), int(v_lst[1][2]))
                return end_date

            def samle_all():
                """
                all_in_one :
                #realy_user_id = [0]
                #vorname = [1]
                #nachname = [2]
                #geburt = [3]
                #telefon = [4]
                #strasse = [5]
                #hausnr = [6]
                #plz = [7]
                #ort = [8]
                #abteilung_id = [9]
                #position_id = [10]
                #vertrag_id = [11]
                #beschaf_id = [12]
                #rolle_id = [13]
                #email = [14]
                #passwort = [15]
                #gehalt = [16]
                #vertragsbeginn = [17]
                #vertragsende = [18]
                #adresse_id = [19]
                #arbeitsvertrag_id = [20]
                """

                all_in_one = []
                all_in_one.append(realy_user_id)
                    
                try:
                    all_in_one.append(ein_uno.get())
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                
                try:
                    all_in_one.append(ein_duo.get())
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                
                # Umwandle Datum
                try:
                    test = ein_tre.get()
                    bdate = condate(test)
                    all_in_one.append(bdate)
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                
                try:
                    all_in_one.append(ein_qwa.get())
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                    
                try:
                    all_in_one.append(ein_qwi.get())
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
            
                try:
                    all_in_one.append(ein_sex.get())
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                    
                try:
                    all_in_one.append(ein_che.get())
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                    
                try:
                    all_in_one.append(ein_nen.get())
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                
                # Get Abteilung_ID
                try:
                    get_abt = "SELECT Abteilung_ID FROM abteilung WHERE Abteilung_name = '" + abteilung + "';"
                    mycursor.execute(get_abt)
                    abteilung_id = mycursor.fetchone()
                    all_in_one.append(abteilung_id[0])
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                
                # Get Position_ID
                try:
                    get_pos = "SELECT `Position_ID` FROM `position` WHERE `Position_name` = '" + position + "';"
                    mycursor.execute(get_pos)
                    position_id = mycursor.fetchone()
                    all_in_one.append(position_id[0])
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
        
                # Get Vertrag_ID
                try:
                    get_ver = "SELECT `Vertragsart_ID` FROM `vertragsart` WHERE `Vertragsart_name` = '" + vertr + "';"
                    mycursor.execute(get_ver)
                    vertrag_id = mycursor.fetchone()
                    all_in_one.append(vertrag_id[0])
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
            
                # Get Beschäftigung_ID
                try:
                    get_bes = "SELECT `Beschäftigung_ID` FROM `beschäftigung` WHERE `Beschäftigung_name` = '" + beschaf + "';"
                    mycursor.execute(get_bes)
                    beschaf_id = mycursor.fetchone()
                    all_in_one.append(beschaf_id[0])
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
            
                # Get Rolle
                try:
                    get_roll = "SELECT `Kontotype_ID` FROM `kontotype` WHERE `Kontotype_name` = '" + rolle + "';"
                    mycursor.execute(get_roll)
                    rolle_id = mycursor.fetchone()
                    all_in_one.append(rolle_id[0])
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                
                try:
                    all_in_one.append(email[0])
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                    
                try:
                    all_in_one.append(new_pass)
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                
                try:
                    all_in_one.append(ein_non.get())
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                
                try:
                    test2 = ein_vie.get()
                    vdate = condate(test2)
                    all_in_one.append(vdate)
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                
                try:
                    test3 = ein_fun.get()
                    edate = condate(test3)
                    all_in_one.append(edate)
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                    
                try:
                    str_get_adr_id = "SELECT `Adresse_ID` FROM `mitarbeiter` WHERE `Mitarbeiter_ID` = " + str(realy_user_id) + ";"
                    mycursor.execute(str_get_adr_id)
                    adressen_id = mycursor.fetchone()
                    all_in_one.append(adressen_id[0])
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)
                    
                try:
                    get_avid_id = "SELECT `Arbeitsvertrag_ID` FROM `mitarbeiter` WHERE `Mitarbeiter_ID` = " + str(realy_user_id) + ";"
                    mycursor.execute(get_avid_id)
                    av_id = mycursor.fetchone()
                    all_in_one.append(av_id[0])
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)

                try:
                    get_lid_id = "SELECT `Login_ID` FROM `mitarbeiter` WHERE `Mitarbeiter_ID` = " + str(realy_user_id) + ";"
                    mycursor.execute(get_lid_id)
                    l_id = mycursor.fetchone()
                    all_in_one.append(l_id[0])
                except (AttributeError, TypeError, NameError):
                    all_in_one.append(None)

                return all_in_one

            def send_and_db(): 

                all_for_send = samle_all()
                
                check_bereitschaft = mb.askyesno(title="Bereitschaft", message="Sind Sie sicher?", parent=self)
                
                if check_bereitschaft and all_for_send: 
                
                    # Send Adresse
                    if all_for_send[4] is None and all_for_send[5] is None and all_for_send[7] is None and all_for_send[6] is None: pass
                    else:
                        x = y = a = 0
                        
                        send_adress = "UPDATE `Adresse` SET "
                        if all_for_send[5] is not None:
                            x = 1
                            send_adress = send_adress + "`Straße`='" + str(all_for_send[5]) + "'"
                            
                        if all_for_send[6] is not None and x == 1:
                            y = 1
                            send_adress = send_adress + ", `HausNr`='" + str(all_for_send[6]) + "'"
                        elif all_for_send[6] is not None and x == 0:
                            y = 1
                            send_adress = send_adress + "`HausNr`=" + str(all_for_send[6])
                            
                        if all_for_send[8] is not None and (x == 1 or y == 1):
                            a = 1
                            send_adress = send_adress + ", `Ort`='" + str(all_for_send[8]) + "'"
                        elif all_for_send[8] is not None and (x == 0 and y == 0):
                            a = 1
                            send_adress = send_adress + "`Ort`='" + str(all_for_send[8]) + "'"
                            
                        if all_for_send[7] is not None and (x == 1 or y == 1 or a == 1):
                            send_adress = send_adress + ", `PLZ`='" + str(all_for_send[7]) + "'"
                        elif all_for_send[7] is not None and (x == 0 and y == 0 and a == 0):
                            send_adress = send_adress + "`PLZ`='" + str(all_for_send[7]) + "'"
                        
                        send_adress = send_adress + " WHERE `Adresse_ID` = " + str(all_for_send[19]) + ";"
                        
                        try:
                            # Execute the SQL command
                            mycursor.execute(send_adress)
                            # Commit your changes in the database
                            myDB.commit()
                        except:
                            # Roll back in case there is any error
                            myDB.rollback()

                    
                    # Send Arbeitsvertrag
                    if all_for_send[16] is None and all_for_send[17] is None and all_for_send[11] is None and all_for_send[10] is None and all_for_send[15] is None : pass
                    else:
                        x = y = a = s = 0
                        
                        send_vert = "UPDATE `arbeitsvertrag` SET "
                        if all_for_send[17] is not None:
                            x = 1
                            send_vert = send_vert + "`Vertragsbeginn`='" + str(all_for_send[17]) + "'"
                            
                        if all_for_send[18] is not None and x == 1:
                            y = 1
                            send_vert = send_vert + ", `Vertragsende`='" + str(all_for_send[18]) + "'"  
                        elif all_for_send[18] is not None and x == 0:
                            y = 1
                            send_vert = send_vert + "`Vertragsende`='" + str(all_for_send[18]) + "'"
                            
                        if all_for_send[12] is not None and (x == 1 or y == 1):
                            a = 1
                            send_vert = send_vert + ", `Beschäftigung_ID`=" + str(all_for_send[12])
                        elif all_for_send[12] is not None and (x == 0 and y == 0):
                            a = 1
                            send_vert = send_vert + "`Beschäftigung_ID`=" + str(all_for_send[12])

                        if all_for_send[11] is not None and (x == 1 or y == 1 or a == 1):
                            s = 1
                            send_vert = send_vert + ", `Vertragsart_ID`=" + str(all_for_send[11])
                        elif all_for_send[11] is not None and (x == 0 and y == 0 and a == 0):
                            s = 1
                            send_vert = send_vert + "`Vertragsart_ID`=" + str(all_for_send[11])

                        if all_for_send[16] is not None and (x == 1 or y == 1 or a == 1 or s == 1):
                            send_vert = send_vert + ", `Gehalt`='" + str(all_for_send[16]) + "'"
                        elif all_for_send[16] is not None and (x == 0 and y == 0 and a == 0 and s == 0):
                            send_vert = send_vert + "`Gehalt`='" + str(all_for_send[16]) + "'"

                        send_vert = send_vert + " WHERE `Arbeitsvertrag_ID` = " + str(all_for_send[20]) + ";"
                    
                    try:
                        # Execute the SQL command
                        mycursor.execute(send_vert)
                        # Commit your changes in the database
                        myDB.commit()
                    except:
                        # Roll back in case there is any error
                        myDB.rollback()
                
                    # Send Login
                    
                    if all_for_send[16] is None and all_for_send[17] is None: pass
                    else:
                        x = 0
                        
                        send_log = "UPDATE `login` SET "
                        if all_for_send[14] is not None:
                            x = 1
                            send_log = send_log + "`E_Mail`='" + str(all_for_send[14]) + "'"
                            
                        if all_for_send[15] is not None and x == 1:
                            send_log = send_log + ", `Password`='" + str(all_for_send[15]) + "'"  
                        elif all_for_send[15] is not None and x == 0:
                            send_log = send_log + "`Password`='" + str(all_for_send[15]) + "'"

                        send_log =  send_log + " WHERE `Login_ID` = " + str(all_for_send[21]) + ";"
                    
                    try:
                        # Execute the SQL command
                        mycursor.execute(send_log)
                        # Commit your changes in the database
                        myDB.commit()
                    except:
                        # Roll back in case there is any error
                        myDB.rollback()
                
                    # Send All Data
                    
                    if all_for_send[1] is None and all_for_send[2] is None and all_for_send[3] is None and all_for_send[4] is None and all_for_send[19] is None and all_for_send[21] is None and all_for_send[13] is None and all_for_send[9] is None and all_for_send[10] is None and all_for_send[20] is None: pass
                    else:
                        x = y = a = s = d = f = r = e = w = 0
                        
                        send_mit_all = "UPDATE `mitarbeiter` SET "
                        if all_for_send[1] is not None:
                            x = 1
                            send_mit_all = send_mit_all + "`Vorname`='" + str(all_for_send[1]) + "'"
                            
                        if all_for_send[2] is not None and x == 1:
                            y = 1
                            send_mit_all = send_mit_all + ", `Nachname`='" + str(all_for_send[2]) + "'"  
                        elif all_for_send[2] is not None and x == 0:
                            y = 1
                            send_mit_all = send_mit_all + "`Nachname`='" + str(all_for_send[2]) + "'"
                            
                        if all_for_send[3] is not None and (x == 1 or y == 1):
                            a = 1
                            send_mit_all = send_mit_all + ", `Geburtsdatum`='" + str(all_for_send[3]) + "'"
                        elif all_for_send[3] is not None and (x == 0 and y == 0):
                            a = 1
                            send_mit_all = send_mit_all + "`Geburtsdatum`='" + str(all_for_send[3]) + "'"

                        if all_for_send[4] is not None and (x == 1 or y == 1 or a == 1):
                            s = 1
                            send_mit_all = send_mit_all + ", `Telefonnummer`=" + str(all_for_send[4])
                        elif all_for_send[4] is not None and (x == 0 and y == 0 and a == 0):
                            s = 1
                            send_mit_all = send_mit_all + "`Telefonnummer`=" + str(all_for_send[4])

                        if all_for_send[19] is not None and (x == 1 or y == 1 or a == 1 or s == 1):
                            d = 1    
                            send_mit_all = send_mit_all + ", `Adresse_ID`=" + str(all_for_send[19])
                        elif all_for_send[19] is not None and (x == 0 and y == 0 and a == 0 and s == 0):
                            d = 1    
                            send_mit_all = send_mit_all + "`Adresse_ID`=" + str(all_for_send[19])
                            
                        if all_for_send[21] is not None and (x == 1 or y == 1 or a == 1 or s == 1 or d == 1):
                            f = 1    
                            send_mit_all = send_mit_all + ", `Login_ID`=" + str(all_for_send[21])
                        elif all_for_send[21] is not None and (x == 0 and y == 0 and a == 0 and s == 0 and d == 0):
                            f = 1    
                            send_mit_all = send_mit_all + "`Login_ID`=" + str(all_for_send[21])

                        if all_for_send[13] is not None and (x == 1 or y == 1 or a == 1 or s == 1 or d == 1 or f == 1):
                            r = 1    
                            send_mit_all = send_mit_all + ", `Kontotype_ID`=" + str(all_for_send[13])
                        elif all_for_send[13] is not None and (x == 0 and y == 0 and a == 0 and s == 0 and d == 0 and f == 0):
                            r = 1    
                            send_mit_all = send_mit_all + "`Kontotype_ID`=" + str(all_for_send[13])

                        if all_for_send[9] is not None and (x == 1 or y == 1 or a == 1 or s == 1 or d == 1 or f == 1 or r == 1):
                            e = 1    
                            send_mit_all = send_mit_all + ", `Abteilung_ID`=" + str(all_for_send[9])
                        elif all_for_send[9] is not None and (x == 0 and y == 0 and a == 0 and s == 0 and d == 0 and f == 0 and r == 0):
                            e = 1    
                            send_mit_all = send_mit_all + "`Abteilung_ID`=" + str(all_for_send[9])
                            
                        if all_for_send[10] is not None and (x == 1 or y == 1 or a == 1 or s == 1 or d == 1 or f == 1 or r == 1 or e == 1):
                            w = 1    
                            send_mit_all = send_mit_all + ", `Position_ID`=" + str(all_for_send[10])
                        elif all_for_send[10] is not None and (x == 0 and y == 0 and a == 0 and s == 0 and d == 0 and f == 0 and r == 0 and e == 0):
                            w = 1    
                            send_mit_all = send_mit_all + "`Position_ID`=" + str(all_for_send[10])

                        if all_for_send[20] is not None and (x == 1 or y == 1 or a == 1 or s == 1 or d == 1 or f == 1 or r == 1 or e == 1 or w == 1):
                            send_mit_all = send_mit_all + ", `Arbeitsvertrag_ID`=" + str(all_for_send[20])
                        elif all_for_send[20] is not None and (x == 0 and y == 0 and a == 0 and s == 0 and d == 0 and f == 0 and r == 0 and e == 0 and w == 0):    
                            send_mit_all = send_mit_all + "`Arbeitsvertrag_ID`=" + str(all_for_send[20])
                            
                        send_mit_all = send_mit_all + " WHERE `Mitarbeiter_ID` =" + str(realy_user_id) + ";"
                    
                    try:
                        # Execute the SQL command
                        mycursor.execute(send_mit_all)
                        # Commit your changes in the database
                        myDB.commit()
                    except:
                        # Roll back in case there is any error
                        myDB.rollback()
                        
                    self.destroy()

            connect_db()
            mycursor = myDB.cursor()
            temp = open_ini()
            way_to_pass = "USE " + temp[3]  
            mycursor.execute(way_to_pass)
        
            rollen_liste = []
            rollen_liste = way_to_somewehere("kontotype")
            
            vertrag_liste = []
            vertrag_liste = way_to_somewehere("vertragsart")

            beschaf_liste = []
            beschaf_liste = way_to_somewehere("beschäftigung")
        
            abteilung_liste = []
            abteilung_liste = way_to_somewehere("abteilung")
        
            position_liste = []
            position_liste = way_to_somewehere("position")

            self = ttk.Toplevel()
            self.title("Edit Mitarbeiter Information")
            center_window(self, 1100, 140)
            self.attributes("-topmost", "True")

            # Erstellen des Label für die Überschrift
            title_label = ttk.Label(self, text="Mitarbeiter Information", font=("Verdana", 10, "bold"))
            title_label.place(x = 30, y = 20)

            # Erstellen der Labels für die Mitarbeiterinformationen
            fields = ["Vorname:", "Nachname:", "Geburtstag:", "Telefonnummer:", "Straße:", "Hausnummer:", "PLZ:", "Ort:", "Abteilung:", "Position:", "Vertragsart:", "Beschäftigung:", "Vertragsbeginn:", "Vertragsende:", "Kontotyp:", "Email:", "Passwort:", "Gehalt:"]

            label_uno = ttk.Label(self, text=fields[0], font = "Verdana 8 bold")
            label_duo = ttk.Label(self, text=fields[1], font = "Verdana 8 bold")
            label_tre = ttk.Label(self, text=fields[2], font = "Verdana 8 bold")
            label_qwa = ttk.Label(self, text=fields[3], font = "Verdana 8 bold")
            label_qwi = ttk.Label(self, text=fields[4], font = "Verdana 8 bold")
            label_sex = ttk.Label(self, text=fields[5], font = "Verdana 8 bold")
            label_che = ttk.Label(self, text=fields[6], font = "Verdana 8 bold")
            label_nen = ttk.Label(self, text=fields[7], font = "Verdana 8 bold")
            label_ten = ttk.Label(self, text=fields[8], font = "Verdana 8 bold")
            label_elf = ttk.Label(self, text=fields[9], font = "Verdana 8 bold")
            label_zwo = ttk.Label(self, text=fields[10], font = "Verdana 8 bold")
            label_dre = ttk.Label(self, text=fields[11], font = "Verdana 8 bold")
            label_vie = ttk.Label(self, text=fields[12], font = "Verdana 8 bold")
            label_fun = ttk.Label(self, text=fields[13], font = "Verdana 8 bold")
            label_she = ttk.Label(self, text=fields[14], font = "Verdana 8 bold")
            label_sib = ttk.Label(self, text=fields[15], font = "Verdana 8 bold")
            label_akt = ttk.Label(self, text=fields[16], font = "Verdana 8 bold")
            label_non = ttk.Label(self, text=fields[17], font = "Verdana 8 bold")
        
            label_uno.place(x = 30, y = 50)
            label_duo.place(x = 250, y = 50)
            label_tre.place(x = 30, y = 100)
            label_qwa.place(x = 250, y = 100)
            label_qwi.place(x = 30, y = 150)
            label_sex.place(x = 250, y = 150)
            label_che.place(x = 30, y = 200)
            label_nen.place(x = 250, y = 200)
            label_ten.place(x = 30, y = 250)
            label_elf.place(x = 250, y = 250)
            label_zwo.place(x = 30, y = 300)
            label_dre.place(x = 250, y = 300)
            label_vie.place(x = 30, y = 350)
            label_fun.place(x = 250, y = 350)
            label_she.place(x = 30, y = 400)
            label_sib.place(x = 30, y = 450)
            label_akt.place(x = 30, y = 500)
            label_non.place(x = 30, y = 550)

            ein_uno = WPEntry(self, user_lst[1])
            ein_duo = WPEntry(self, user_lst[2])
            ein_tre = WPEntry(self, user_lst[3])
            ein_qwa = WPEntry(self, user_lst[4])
            ein_qwi = WPEntry(self, adress_lst[0][1])
            ein_sex = WPEntry(self, adress_lst[0][2])
            ein_che = WPEntry(self, adress_lst[0][4])
            ein_nen = WPEntry(self, adress_lst[0][3])

            ein_ten = ttk.Combobox(self, value = abteilung_liste)
            ein_ten.current(user_lst[8]-1)
            ein_ten.config(state="readonly")
            ein_ten.bind("<<ComboboxSelected>>", abteilung_ausgeben)

            ein_elf = ttk.Combobox(self, value = position_liste)
            ein_elf.current(user_lst[9]-1)
            ein_elf.config(state="readonly")
            ein_elf.bind("<<ComboboxSelected>>", position_ausgeben)

            ein_zwo = ttk.Combobox(self, value = vertrag_liste)
            ein_zwo.current(v_lst[6]-1)
            ein_zwo.config(state="readonly")
            ein_zwo.bind("<<ComboboxSelected>>", vertrag_ausgeben)

            ein_dre = ttk.Combobox(self, value = beschaf_liste)
            ein_dre.current(v_lst[5]-1)
            ein_dre.config(state="readonly")
            ein_dre.bind("<<ComboboxSelected>>", beschaf_ausgeben)

            ein_vie = WPEntry(self, dt.date(int(v_lst[0][0]), int(v_lst[0][1]), int(v_lst[0][2])))
            end_date = conv_date_new()
            ein_fun = WPEntry(self, end_date)

            ein_she = ttk.Combobox(self, value = rollen_liste)
            ein_she.current(user_lst[7]-1)
            ein_she.config(state="readonly")
            ein_she.bind("<<ComboboxSelected>>", rolle_ausgeben)

            ein_akt = ttk.Entry(self)
            ein_non = WPEntry(self, v_lst[4])

            ein_uno.place(x = 30, y = 70)
            ein_duo.place(x = 250, y = 70)
            ein_tre.place(x = 30, y = 120)
            ein_qwa.place(x = 250, y = 120)
            ein_qwi.place(x = 30, y = 170)
            ein_sex.place(x = 250, y = 170)
            ein_che.place(x = 30, y = 220)
            ein_nen.place(x = 250, y = 220)
            ein_ten.place(x = 30, y = 270)
            ein_elf.place(x = 250, y = 270)
            ein_zwo.place(x = 30, y = 320)
            ein_dre.place(x = 250, y = 320)
            ein_vie.place(x = 30, y = 370)
            ein_fun.place(x = 250, y = 370)
            ein_she.place(x = 30, y = 420)
            ein_akt.place(x = 30, y = 520)
            ein_non.place(x = 30, y = 570)
        
            lb_lk = ttk.Label(self, text = get_email(user_lst[6]))
            lb_lk.place(x = 30, y = 470)
            ein_duo.bind('<Return>', email_value)
            ein_akt.bind('<Return>', pass_check)
        
            but_send = ttk.Button(self, text = "Ändern", command=send_and_db)
            but_send.place(x = 30, y = 650)
                
    #realy_user_id

    for line in temporaly:
        if realy_user_id == line[0]:
            abt_and_pos = get_abt_position(line[8], line[9])
            email = get_email(line[6])
            vertrag = get_vertrag(line[10])
            # Ziehe Adresse aus DB
            adresse_liste = get_adresse(line[5])
            # Konvertation von MySQL Geburtsdate Date in Normal Form
            geburtstag = []
            month_dict = {"01" : "Januar", "02" : "Februar", "03" : "März", "04" : "April", "05" : "Mai", "06" : "Juni", "07" : "Juli", "08" : "August", "09" : "September", "10" : "Oktober", "11" : "November", "12" : "Dezember"}
            geburtstag = str(line[3]).split("-")
            geburtstag_str = str(geburtstag[2]) + " " + str(month_dict[str(geburtstag[1])]) + " " + str(geburtstag[0])
            
            vertrag_start_str = str(vertrag[0][2]) + " " + str(month_dict[str(vertrag[0][1])]) + " " + str(vertrag[0][0])

            if vertrag[1][0] == "0000" and vertrag[1][1] == "00" and vertrag[1][2] == "00":
                vertrag_ende_str = "- kein -"
            else: vertrag_ende_str = str(vertrag[1][2]) + " " + str(month_dict[str(vertrag[1][1])]) + " " + str(vertrag[1][0])
            
            #print(line)
            #print(vertrag)
            win = edit_user_gui(root, line, adresse_liste, vertrag)

def add_neu_user():
    """
    Funktion für Neu Mitarbeiter Hinzufügen
    """
    win = add_user_gui(root)
    
def del_user():
    """
    Funktion Mitarbeiter Löschen
    """
    if myDB:
        mycursor = myDB.cursor()
        temp = open_ini()
        way_to_pass = "USE " + temp[3]
        mycursor.execute(way_to_pass)
        
        target = selectet_user.split(" ")
        
        for line in temporaly:
            if target[0] == line[1] and target[1] == line[2]:
                
                mitarbeiter_id = line[0]
                print(mitarbeiter_id)
                adresse_id = line[5]
                login_id = line[6]
                arbeits_vertrag_id = line[10]
                del_adresse = "DELETE FROM Adresse WHERE Adresse_ID = " + str(adresse_id)
                del_login = "DELETE FROM Login WHERE Login_ID = " + str(login_id)
                del_vertrag = "DELETE FROM Arbeitsvertrag WHERE Arbeitsvertrag_ID = " + str(arbeits_vertrag_id)
                del_mitarbeiter = "DELETE FROM Mitarbeiter WHERE Mitarbeiter_ID = " + str(mitarbeiter_id)
                # Delete Record aus Mitarbeiter Tabelle
                try:
                    # Execute the SQL command
                    mycursor.execute(del_mitarbeiter)
                    # Commit your changes in the database
                    myDB.commit()
                except:
                    # Roll back in case there is any error
                    myDB.rollback()
                # Delete Record aus Adresse Tabelle
                try:
                    # Execute the SQL command
                    mycursor.execute(del_adresse)
                    # Commit your changes in the database
                    myDB.commit()
                except:
                    # Roll back in case there is any error
                    myDB.rollback()
                # Delete Record aus Login Tabelle
                try:
                    # Execute the SQL command
                    mycursor.execute(del_login)
                    # Commit your changes in the database
                    myDB.commit()
                except:
                    # Roll back in case there is any error
                    myDB.rollback()
                # Delete Record aus Vertrag Tabelle
                try:
                    # Execute the SQL command
                    mycursor.execute(del_vertrag)
                    # Commit your changes in the database
                    myDB.commit()
                except:
                    # Roll back in case there is any error
                    myDB.rollback()
                   
            #getdbuser()   ? 

    else: print("Kann nicht ohne DB Konnektion.")
    
def show_zieterf(realy_thisuser_id):

    # Globale Variablen für Startzeit des Timers
    global start_time, summ_time, paused, flag, mez, select_data, first_lauf
    
    start_time = None
    summ_time  = timedelta(0)
    paused = False
    flag = False
    mez = False
    select_data = []
    first_lauf = 0
    month_lst = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    #summ_time = timedelta(seconds=float(0), minutes=float(0), hours=float(0))
 
    def get_time_now():
        t = datetime.now()
        new_t = str(t).split(" ")
        new_t = new_t[0].split("-")
        new_t = new_t[2] + " " + month_lst[int(new_t[1])-1] + " " + new_t[0]
        return new_t

    def get_tarif():
        global tarif_lst

        connect_db()
        mycursor = myDB.cursor()
        temp = open_ini()
        way_to_pass = "USE " + temp[3]  
        mycursor.execute(way_to_pass)
            
        way_to_tarif = "SELECT `Tarif_name` FROM `tarif`"
        mycursor.execute(way_to_tarif)
        tarif_lst = []
        for line in mycursor:
            tarif_lst.append(line[0])
            
        return tarif_lst

    # Funktion zum Starten des Timers und Erfassen 
    def start_timer():
        global start_time, summ_time, paused, flag, tick, first_lauf

        if flag == True:
            mb.showwarning("Warnung", "Timer is already gestartet")
        else:
            flag = True
            paused = False
            start_time = datetime.now() # Erstellen Start Zeitpunkt
            
            if mez == False and first_lauf == 0:
                first_lauf = 1
                select_data.append(realy_thisuser_id)

                new_t = str(start_time).split(" ")
                select_data.append(new_t[0])
                select_data.append(str(new_t[1]).split(".")[0])
                
            update_timer()  # Timer starten

    def pause_timer():
        global start_time, summ_time, paused, flag
        
        if start_time is None:
            mb.showwarning("Warnung", "Die Zeiterfassung wurde noch nicht gestartet!")
        if paused:
            mb.showwarning("Warnung", "Timer is already paused")

        if start_time:
            paused = True
            current_time = datetime.now()
            temp = current_time - start_time if start_time else timedelta(0)
            str_zeit = temp.__str__().split(".")
            str_zeit = str_zeit[0].split(":")
        
            t_delta = timedelta(
                seconds=float(str_zeit[2]),
                minutes=float(str_zeit[1]),
                hours=float(str_zeit[0])
                )
        
            summ_time += t_delta
            zeit_frame.after_cancel(tick)
            timer_label.config(text=summ_time)

            flag = False
            start_time = None  # Timer stoppen und zurücksetzen

    def stop_timer():
        """
        # Funktion zum Stoppen des Timers und zurücksetzen
        # Funktion zum Zurücksetzen des Timers, wenn der Benutzer die Zeiterfassung abbrechen möchte
        """
        global start_time, summ_time, paused, flag, first_lauf
        
        if first_lauf == 0:
            mb.showwarning("Warnung", "Die Zeiterfassung wurde noch nicht gestartet!") 
        if start_time and paused == False:
            mb.showwarning("Warnung", "Timer is not paused") 

        if paused:
            current_time = datetime.now()
            
            if mez == False and first_lauf ==1:
                new_t = str(current_time).split(" ")
                select_data.append(str(new_t[1]).split(".")[0])
                select_data.append(1)
                select_data.append(0)

            start_time = None
            summ_time = None
            paused = False
            flag = False
            first_lauf = 0

            timer_label.config(text="0:00:00")
 
    def update_timer():
        """
        # Funktion zur fortlaufenden Aktualisierung des Timers
        """
        global start_time, summ_time, paused, flag, tick
        
        current_time = datetime.now()
        elapsed_time = current_time - start_time if start_time else timedelta(0)
        elapsed_time += summ_time
        show_time = elapsed_time.__str__().split(".")
        timer_label.config(text=show_time[0])
        tick = zeit_frame.after(1000, update_timer)  # Timer jede Sekunde aktualisieren
            
    def manuell_zeit():
        global mez
        mez = True
    
        manu_button.place_forget()
        manu_clos_button.place(x=30, y=215, width=240)
        but_send.place(x=30, y=430, width=240)

        lb_tarif.place(x=30, y=260, width=120)
        box_tarif.place(x=70, y=260, width=120)

        lb_tag.place(x=30, y=300)
        lb_moth.place(x=100, y=300)
        lb_jahr.place(x=210, y=300)
        
        ein_tag.place(x=30, y=320, width=40)
        box_mont.place(x=100, y=320, width=80)
        ein_jahr.place(x=210, y=320, width=60)
        
        lb_start_zeit.place(x=30, y=360)
        lb_end_zeit.place(x=165, y=360)
 
        ein_start_time.place(x=30, y=380, width=105)
        ein_end_time.place(x=165, y=380, width=105)
    
    def manuell_close():
        global mez
        mez = False
    
        manu_button.place(x=30, y=215, width=240)
        manu_clos_button.place_forget()
        but_send.place(x=30, y=245, width=240)
        
        lb_tarif.place_forget()
        box_tarif.place_forget()

        lb_tag.place_forget()
        lb_moth.place_forget()
        lb_jahr.place_forget()
        
        lb_start_zeit.place_forget()
        lb_end_zeit.place_forget()
        
        ein_tag.place_forget()
        box_mont.place_forget()
        ein_jahr.place_forget()
 
        ein_start_time.place_forget()
        ein_end_time.place_forget()
    
    def monselect(event):           
        global month
        month_str = box_mont.get()
        for i in range(len(month_lst)):
            if month_str == str(month_lst[i]):
                month = i + 1
            else:pass
            i += 1
        return month

    def tonselect(event): pass

    def send_zeit():
        global select_data
        global ub_konto
        if mez == True:
            
            select_data.append(realy_thisuser_id)
            
            if len(ein_jahr.get()) > 0:
                select_data.append(ein_jahr.get())
            else: print("No DATA")
            if month > 0:
                select_data.append(month)
            elif month is None: pass
            else: print("No DATA")
            if len(ein_tag.get()) > 0:
                select_data.append(ein_tag.get())
            else: print("No DATA")
            if len(ein_start_time.get()) > 0:
                select_data.append(ein_start_time.get())
            else: print("No DATA")
            if len(ein_end_time.get()) > 0:
                select_data.append(ein_end_time.get())
            else: print("No DATA")
            if len(box_tarif.get()) > 0:
                select_data.append(int(box_tarif.current()) + 1)
            else: print("No DATA")
            select_data.append(int(0))
            
            tarif = select_data[6]

            if select_data[0] is not None and select_data[1] is not None and select_data[2] is not None and select_data[3] is not None and select_data[4] is not None and select_data[5] is not None and select_data[6] is not None:
                str_date = select_data[1] + "-" + str(select_data[2]) + "-" + select_data[3]
                str_date = datetime.strptime(str_date,'%Y-%m-%d').strftime('%Y-%m-%d')
                str_s_time = datetime.strptime(select_data[4],'%H:%M').strftime('%H:%M:%S')
                str_e_time = datetime.strptime(select_data[5],'%H:%M').strftime('%H:%M:%S')
                zeit_str = "INSERT INTO `arbeitszeiten`(`Mitarbeiter_ID`, `Tag`, `Startzeit`, `Endzeit`, `Tarif_ID`, `Überstunden`) VALUES (" + str(select_data[0]) + ",'" + str_date + "','" + str_s_time + "','" + str_e_time + "'," + str(select_data[6]) + ","

        elif mez == False:
            
            tarif = select_data[4]

            if select_data[0] is not None and select_data[1] is not None and select_data[2] is not None and select_data[3] is not None and select_data[4] is not None:
                zeit_str = "INSERT INTO `arbeitszeiten`(`Mitarbeiter_ID`, `Tag`, `Startzeit`, `Endzeit`, `Tarif_ID`, `Überstunden`) VALUES (" + str(select_data[0]) + ",'" + str(select_data[1]) + "','" + str(select_data[2]) + "','" + str(select_data[3]) + "'," + str(select_data[4]) + ","
                
        else: mb.showwarning("Warnung", "Nicht alles ist eingetragen")
        
        # Ausrechnen von Überstunden
        res_quest = get_vertrag(select_data[0])
        
        answ_d = get_uber(realy_thisuser_id)

        if res_quest[5] == 1 and tarif == 1:
            min_time = "6:00"
            mid_time = "9:00"
            if mez == True:
                str_min_time = datetime.strptime(min_time,'%H:%M').strftime('%H:%M:%S')
                str_mid_time = datetime.strptime(mid_time,'%H:%M').strftime('%H:%M:%S')

                str_min_time = datetime.strptime(str_min_time, '%H:%M:%S')
                str_mid_time = datetime.strptime(str_mid_time, '%H:%M:%S')

                str_s_time = datetime.strptime(str_s_time, '%H:%M:%S')
                str_e_time = datetime.strptime(str_e_time, '%H:%M:%S')

                temp = (str_e_time - str_s_time)
                temp = datetime.strptime(str(temp), "%H:%M:%S")
                
                if temp > str_min_time and temp < str_mid_time:
                    answer = mb.askyesno("Pause", "Haben Sie Pause gemacht?")
                    if answer == True:
                        zeit_str = zeit_str + str(select_data[7]) + ")"
                    else:
                        mb.showwarning("Pause", "Bitte machen Sie das nicht!\nAber: + 45 min Überstunden")
                        select_data[7] = answ_d + 45
                        zeit_str = zeit_str + str(select_data[7]) + ")"
                elif temp > str_mid_time:
                    temp2 = temp - str_mid_time
                    temp2 = str(temp2).split(":")
                    hours = int(temp2[0]) * 60
                    minuten = int(temp2[1]) + 1
                    ubs_result = hours + minuten

                    answer = mb.askyesno("Pause", "Haben Sie Pause gemacht?")
                    if answer == True:
                        ubs_result -= 60
                        select_data[7] = answ_d + ubs_result
                        zeit_str = zeit_str + str(select_data[7]) + ")"
                    else:
                        mb.showwarning("Pause", "Bitte machen Sie das nicht!\nAber: + 60 min Überstunden")
                        select_data[7] = answ_d + ubs_result
                        zeit_str = zeit_str + str(select_data[7]) + ")"
                else:
                    zeit_str = zeit_str + str(select_data[7]) + ")"
            else:
                str_min_time = datetime.strptime(min_time,'%H:%M').strftime('%H:%M:%S')
                str_mid_time = datetime.strptime(mid_time,'%H:%M').strftime('%H:%M:%S')

                str_min_time = datetime.strptime(str_min_time, '%H:%M:%S')
                str_mid_time = datetime.strptime(str_mid_time, '%H:%M:%S')

                str_s_time = datetime.strptime(select_data[2], '%H:%M:%S')
                str_e_time = datetime.strptime(select_data[3], '%H:%M:%S')

                temp = (str_e_time - str_s_time)
                temp = datetime.strptime(str(temp), "%H:%M:%S")
                
                if temp > str_min_time and temp < str_mid_time:
                    answer = mb.askyesno("Pause", "Haben Sie Pause gemacht?")
                    if answer == True:
                        zeit_str = zeit_str + str(select_data[5]) + ")"
                    else:
                        mb.showwarning("Pause", "Bitte machen Sie das nicht!\nAber: + 45 min Überstunden")
                        select_data[5] = answ_d + 45
                        zeit_str = zeit_str + str(select_data[5]) + ")"
                elif temp > str_mid_time:
                    temp2 = temp - str_mid_time
                    temp2 = str(temp2).split(":")
                    hours = int(temp2[0]) * 60
                    minuten = int(temp2[1]) + 1
                    ubs_result = hours + minuten

                    answer = mb.askyesno("Pause", "Haben Sie Pause gemacht?")
                    if answer == True:
                        ubs_result -= 60
                        select_data[5] = answ_d + ubs_result
                        zeit_str = zeit_str + str(select_data[5]) + ")"
                    else:
                        mb.showwarning("Pause", "Bitte machen Sie das nicht!\nAber: + 60 min Überstunden")
                        select_data[5] = answ_d + ubs_result
                        zeit_str = zeit_str + str(select_data[5]) + ")"
                else:
                    zeit_str = zeit_str + str(select_data[5]) + ")"
        elif res_quest[5] == 2 and tarif == 1:
            min_time = "3:00"
            mid_time = "6:00"
            if mez == True:
                str_min_time = datetime.strptime(min_time,'%H:%M').strftime('%H:%M:%S')
                str_mid_time = datetime.strptime(mid_time,'%H:%M').strftime('%H:%M:%S')

                str_min_time = datetime.strptime(str_min_time, '%H:%M:%S')
                str_mid_time = datetime.strptime(str_mid_time, '%H:%M:%S')

                str_s_time = datetime.strptime(str_s_time, '%H:%M:%S')
                str_e_time = datetime.strptime(str_e_time, '%H:%M:%S')

                temp = (str_e_time - str_s_time)
                temp = datetime.strptime(str(temp), "%H:%M:%S")
                
                if temp > str_min_time and temp < str_mid_time:
                    zeit_str = zeit_str + str(select_data[7]) + ")"
                elif temp > str_mid_time:
                    temp2 = temp - str_mid_time
                    temp2 = str(temp2).split(":")
                    hours = int(temp2[0]) * 60
                    minuten = int(temp2[1]) + 1
                    ubs_result = hours + minuten

                    select_data[7] = answ_d + ubs_result
                    zeit_str = zeit_str + str(select_data[7]) + ")"
            else:
                str_min_time = datetime.strptime(min_time,'%H:%M').strftime('%H:%M:%S')
                str_mid_time = datetime.strptime(mid_time,'%H:%M').strftime('%H:%M:%S')

                str_min_time = datetime.strptime(str_min_time, '%H:%M:%S')
                str_mid_time = datetime.strptime(str_mid_time, '%H:%M:%S')

                str_s_time = datetime.strptime(select_data[2], '%H:%M:%S')
                str_e_time = datetime.strptime(select_data[3], '%H:%M:%S')

                temp = (str_e_time - str_s_time)
                temp = datetime.strptime(str(temp), "%H:%M:%S")
                
                if temp > str_min_time and temp < str_mid_time:
                    zeit_str = zeit_str + str(select_data[5]) + ")"
                elif temp > str_mid_time:
                    temp2 = temp - str_mid_time
                    temp2 = str(temp2).split(":")
                    hours = int(temp2[0]) * 60
                    minuten = int(temp2[1]) + 1
                    ubs_result = hours + minuten

                    select_data[5] = answ_d + ubs_result
                    zeit_str = zeit_str + str(select_data[5]) + ")"
                else:
                    zeit_str = zeit_str + str(select_data[5]) + ")"
        elif res_quest[5] == 3 and tarif == 1:
            min_time = "1:00"
            mid_time = "2:00"
            if mez == True:
                str_min_time = datetime.strptime(min_time,'%H:%M').strftime('%H:%M:%S')
                str_mid_time = datetime.strptime(mid_time,'%H:%M').strftime('%H:%M:%S')

                str_min_time = datetime.strptime(str_min_time, '%H:%M:%S')
                str_mid_time = datetime.strptime(str_mid_time, '%H:%M:%S')

                str_s_time = datetime.strptime(str_s_time, '%H:%M:%S')
                str_e_time = datetime.strptime(str_e_time, '%H:%M:%S')

                temp = (str_e_time - str_s_time)
                temp = datetime.strptime(str(temp), "%H:%M:%S")
                
                if temp > str_min_time and temp < str_mid_time:
                    zeit_str = zeit_str + str(select_data[7]) + ")"
                elif temp > str_mid_time:
                    temp2 = temp - str_mid_time
                    temp2 = str(temp2).split(":")
                    hours = int(temp2[0]) * 60
                    minuten = int(temp2[1]) + 1
                    ubs_result = hours + minuten

                    select_data[7] = answ_d + ubs_result
                    zeit_str = zeit_str + str(select_data[7]) + ")"
            else:
                str_min_time = datetime.strptime(min_time,'%H:%M').strftime('%H:%M:%S')
                str_mid_time = datetime.strptime(mid_time,'%H:%M').strftime('%H:%M:%S')

                str_min_time = datetime.strptime(str_min_time, '%H:%M:%S')
                str_mid_time = datetime.strptime(str_mid_time, '%H:%M:%S')

                str_s_time = datetime.strptime(select_data[2], '%H:%M:%S')
                str_e_time = datetime.strptime(select_data[3], '%H:%M:%S')

                temp = (str_e_time - str_s_time)
                temp = datetime.strptime(str(temp), "%H:%M:%S")
                
                if temp > str_min_time and temp < str_mid_time:
                    zeit_str = zeit_str + str(select_data[5]) + ")"
                elif temp > str_mid_time:
                    temp2 = temp - str_mid_time
                    temp2 = str(temp2).split(":")
                    hours = int(temp2[0]) * 60
                    minuten = int(temp2[1]) + 1
                    ubs_result = hours + minuten

                    select_data[5] = answ_d + ubs_result
                    zeit_str = zeit_str + str(select_data[5]) + ")"
                else:
                    zeit_str = zeit_str + str(select_data[5]) + ")"
        elif res_quest[5] == 4:
            if mez == True:
                pass
            else:
                pass
        else: pass

        if tarif == 2:
            if mez == True:

                str_s_time = datetime.strptime(str_s_time, '%H:%M:%S')
                str_e_time = datetime.strptime(str_e_time, '%H:%M:%S')

                temp = (str_e_time - str_s_time)
                temp = datetime.strptime(str(temp), "%H:%M:%S")
                temp = str(temp).split(" ")
                temp2 = str(temp[1]).split(":")
                hours = int(temp2[0]) * 60
                minuten = int(temp2[1]) + 1
                ubs_result = hours + minuten
                select_data[7] = str("-" + str(ubs_result))
                zeit_str = zeit_str + str(select_data[7]) + ")"
            else:
                mb.showwarning("Warning", "Versuchen sie das über Manuelle Eingabe")

        try:      
            # Execute the SQL command
            mycursor = myDB.cursor()
            mycursor.execute(zeit_str)
            # Commit your changes in the database
            myDB.commit()
        except:
            # Roll back in case there is any error
            myDB.rollback()
            
    if realy_thisuser_id:
        # Erstelle Frame für Info
        zeit_frame = ttk.Frame(root, relief= "flat")
        zeit_frame.place(x = 835, y = 20, width=300, height=480)
        # Mitarbeiter Information
        lb_ma_info = ttk.Label(zeit_frame, text = "Arbeitszeit-Tracker:", font = "Verdana 10 bold").pack(pady= 20)
        
        # Buttons für die Steuerung der Zeiterfassung und Anwendung

        with pil.Image.open("stop.png") as img1:
            img_new_size1 = img1.resize((44, 44))
            img_stop = pil.PhotoImage(image = img_new_size1)
        
        with pil.Image.open("pause.png") as img2:
            img_new_size2 = img2.resize((50, 50))
            img_pause = pil.PhotoImage(image = img_new_size2)
        
        with pil.Image.open("play.png") as img3:
            img_new_size3 = img3.resize((50, 50))
            img_play = pil.PhotoImage(image = img_new_size3)

        stop_button = tk.Button(zeit_frame, image=img_stop, command=stop_timer)
        stop_button.image = img_stop
        stop_button.place(x=30, y=50, width=60, height=60)
        
        pause_button = tk.Button(zeit_frame, image = img_pause, command=pause_timer)
        pause_button.image = img_pause
        pause_button.place(x=120, y=50, width=60, height=60)

        start_button = tk.Button(zeit_frame, image = img_play, command=start_timer)
        start_button.image = img_play
        start_button.place(x=210, y=50, width=60, height=60)
 
        # Label zur Anzeige des Timers
        time_now = get_time_now()

        date_label = ttk.Label(zeit_frame, text=time_now, font = "Verdana 12 bold")
        timer_label = ttk.Label(zeit_frame, text="0:00:00", font = "Verdana 20 bold")
        date_label.place(x = 75, y = 130)
        timer_label.place(x = 95, y = 160)
 
        manu_button = ttk.Button(zeit_frame, text="Manuelle Eingabe", command=manuell_zeit)
        manu_button.place(x=30, y=215, width=240)
        manu_clos_button = ttk.Button(zeit_frame, text="Eingabe Schlißen", command=manuell_close)
        but_send = ttk.Button(zeit_frame, text = "Send Zeit", command=send_zeit)
        but_send.place(x=30, y=245, width=240)
        
        lb_tarif = ttk.Label(zeit_frame, text= "Tarif:")
        t_lst = get_tarif()
        box_tarif = ttk.Combobox(zeit_frame, value=t_lst)
        box_tarif.current(0)
        box_tarif.bind("<<ComboboxSelected>>", tonselect)
        
        lb_tag = ttk.Label(zeit_frame, text= "Tag")
        lb_moth = ttk.Label(zeit_frame, text= "Monat")
        lb_jahr = ttk.Label(zeit_frame, text= "Jahr")
        
        lb_start_zeit = ttk.Label(zeit_frame, text= "Start Zeit")
        lb_end_zeit = ttk.Label(zeit_frame, text= "End Zeit")
        
        ein_tag = ttk.Entry(zeit_frame)
        
        box_mont = ttk.Combobox(zeit_frame, value=month_lst)
        box_mont.current(0)
        box_mont.bind("<<ComboboxSelected>>", monselect)
        
        ein_jahr = ttk.Entry(zeit_frame) 
        ein_start_time = ttk.Entry(zeit_frame)
        ein_end_time = ttk.Entry(zeit_frame)


root = tk.Tk()
root.title("Mitarbeiterverwaltung und Zeiterfassun")
root.iconbitmap(default='TimeM.ico')
root.config(background="#dce7f7")
root.focus()
center_window(root, 380 , 150)

connect_db()

fenster = ttk.Toplevel()
fenster.title("Login")
fenster.attributes("-topmost", "True")
center_window(fenster, 1225 , 650)

lb_fehlschlag = ttk.Label(fenster, text = "     Ihre Anmeldedaten sind falsch \noder Ihr Konto ist nicht länger gültig!", font="Verdana 8", foreground="#870e18")
lb_login = ttk.Label(fenster, text = "Anmeldename: ").place(x = 30, y = 55)
lb_pass = ttk.Label(fenster, text = "Passwort: ").place(x = 30, y = 90)
ein_login = ttk.Entry(fenster)
ein_login.place(x = 140, y = 50)
ein_pass = ttk.Entry(fenster, show = "*")
ein_pass.place(x = 140, y = 85)

but_login = ttk.Button(fenster, text = "Senden", command=loggin)
but_login.place(x = 125, y = 140)

butt_neu_user = ttk.Button(root, text = "Neuer Mitarbeiter", command=add_neu_user)
butt_del_user = ttk.Button(root, text = "Mitarbeiter Löschen", command=del_user)

root.mainloop()