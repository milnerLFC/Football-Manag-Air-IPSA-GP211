# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:03:47 2020

@author: benja
"""
import sqlite3
import requests
from tkinter import messagebox
import os
from learning import learn_model,build_all_database

leagues = ['E0','E1','E2','E3','B1','F1','F2','SC0','SC1','SP1','SP2','P1','T1','N1','D1','D2','I1','I2','G1']
extraleagues= ['DNK','ARG','BRA','SWZ','MEX','IRL','USA','RUS','CHN','JPN','AUT','SWE','NOR','ROU','POL']

ltot = leagues+extraleagues
# print(ltot)

def update_predic_model():
    msg = messagebox.askokcancel("ATTENTION","Cette action peut durer un certain temps et est irréversible", default = 'cancel')
    if msg == True:
        build_all_database(ltot, 4, .95)
        accuracy = learn_model('all')
        while accuracy <= 0.45:
            learn_model('all')
            
def DataUpdate():
    try:
        for l in leagues :
            reqfix = requests.get(f'https://www.football-data.co.uk/fixtures.xlsx')
            url_content = reqfix.content   
            xlsx_file = open(f'databases/csv/fixtures.xlsx', 'wb')
            xlsx_file.write(url_content)
            xlsx_file.close()
            try :
                req = requests.get(f'http://www.football-data.co.uk/mmz4281/2021/{l}.csv')
                url_content = req.content
                csv_file = open(f'databases/csv/{l}2021.csv', 'wb')
                csv_file.write(url_content)
                csv_file.close()
                
    
            except:
                req = requests.get(f'http://www.football-data.co.uk/mmz4281/1920/{l}.csv')
                url_content = req.content
                
                csv_file = open(f'databases/csv/{l}2020.csv', 'wb')
                csv_file.write(url_content)
                csv_file.close()
        
        for l in extraleagues : 
            req = requests.get(f'https://www.football-data.co.uk/new/{l}.csv')
            url_content = req.content
            csv_file = open(f'databases/csv/{l}2021.csv', 'wb')
            csv_file.write(url_content)
            csv_file.close()
            
            reqfix = requests.get(f'https://www.football-data.co.uk/new_league_fixtures.xlsx')
            url_content = reqfix.content
            xlsx_file = open(f'databases/csv/extrafixtures.xlsx', 'wb')
            xlsx_file.write(url_content)
            xlsx_file.close()
            
        messagebox.showinfo("Opération Terminée","La mise à jour des fichiers est terminée !")
    except:
        messagebox.showinfo("Opération Echouée","La mise à jour des fichiers n'a pas fonctionnée. Vérifiez votre connexion Internet.")
def updatePOS():
    msg = messagebox.askokcancel("ATTENTION","Cette est longue et peut durer plusieurs minutes !", default = 'cancel')
    if msg == True:
        conn = sqlite3.connect(f'databases/alldata.db')
        c = conn.cursor()
        conn_pos =sqlite3.connect('databases/players_pos.db')
        data2 = c.execute("SELECT ID,TITU FROM Players WHERE TITU IS NOT NULL AND TITU != 'RES' AND TITU !='SUB'")
        # cp = conn_pos.cursor()
        # data_pos = cp.execute("SELECT ID, team_position,team_jersey_number FROM Positions")
        # for row in data_pos.fetchall():
        for row in data2.fetchall():
            sofi_id = row[0]
            position = row[1]
            # number = row[2]
            c.execute("UPDATE Players SET BP = ? WHERE ID = ? ",(position, sofi_id,))
        conn.commit()
        conn.close()
        conn_pos.close()
        messagebox.showinfo("Opération Terminée","La mise à jour des informations est terminée !")

def download_pic(Teams):
    msg = messagebox.askokcancel("ATTENTION","Cette action peut durer près d'une heure !", default = 'cancel')
    if msg == True:
        conn = sqlite3.connect(f'databases/alldata.db')
        for t in Teams:
            c = conn.cursor()
            joueurs = c.execute("SELECT ID,PlayerPhoto  FROM Players WHERE Club = ?",(t,))
            for row in joueurs.fetchall():
                try:
                    player_id = row[0]
                    photo_path = row[1]
                    response = requests.get(f"{photo_path}", allow_redirects=True)
        
                    file = open(f"images/players/{player_id}.png", "wb")
                    file.write(response.content)
                    file.close()
                    try:
                        if os.stat(file).st_size == 0:
                            os.remove(file)
                    except:pass
                except: pass
        conn.close()
        messagebox.showinfo("Opération Terminée","Le téléchargement des photographies est terminé !")
        
def download_ecu(Liste_ecussons):
    msg = messagebox.askokcancel("ATTENTION","Cette action peut durer plusieurs minutes !", default = 'cancel')
    if msg == True:
        for e in Liste_ecussons:
            try:
                ecu = e.rsplit('/', 1)[0]
                quality = "/light_240.png"

                pre_id_ecu = e.rsplit('/', 2)[1]
                id_ecu = pre_id_ecu.rsplit('/',1)[0]
                
                ecusson= ecu+quality
                
                response = requests.get(ecusson, allow_redirects=True)
                
                file = open(f"images/ecussons/{id_ecu}.png", "wb")
                file.write(response.content)
                file.close()                
            except:pass
        messagebox.showinfo("Opération Terminée","Le téléchargement des écussons est terminé !")