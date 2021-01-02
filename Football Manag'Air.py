# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 17:35:21 2020

@author: benja
"""

# MODULES & LIBRAIRIES

import sqlite3

import tkinter as tk
from tkinter import font as tkFont
from tkinter import tix, ttk, Label, Canvas, Button, messagebox,PhotoImage, Toplevel
from PIL import Image, ImageTk
import datetime as dt

from module_classes import AutocompleteCombobox,hover_button,Clock
from definitions import levelcolor,calc_team_global

from fuzzywuzzy import process
import os,shutil,threading

import random

from GlobalTeam import team_global
from StatsPlayer import players_stats
from BestCompo import best_tactic
from Transfers import database_update
from param import DataUpdate,update_predic_model #download_ecu,download_pic,updatePOS

import pygame

# from tqdm import tqdm


# PROGRAMME
selected_players = 'AND TruePlayer = 0'

blasons_id = [f.rsplit('.',1)[0] for f in os.listdir("images/ecussons")]
blasons_id.remove('desktop')
blasons = {}

# chpts = ['E0','E1','E2','E3','F1','F2','SP1', 'SP2','D1','D2','I1','I2','N1','P1','SC0','SC1', 'T1','B1','G1','ARG','BRA','SWZ','MEX','IRL','USA','RUS']
chpts = []
preTeams = []
teamscount= []
Teams = []
Joueurs = []
Liste_ecussons = []

lpostes = []
lnationalities = []

dic_clubs_id = {}
dic_clubs_div = {}

conn = sqlite3.connect(f'databases/alldata.db')
c = conn.cursor()
data = c.execute(f"SELECT ID,Name,Club,ClubLogo,BP,Nationality,championnat FROM Players WHERE TITU IS NOT NULL AND championnat IS NOT NULL {selected_players}")
for row in data.fetchall():
    try:
        Club = row[2]
        EcuClub = row[3]
        position = row[4]
        country = row[5]
        div = row[6]
        
        if Club not in preTeams:
            preTeams.append(str(Club))
            pre_id_ecu = EcuClub.rsplit('/', 2)[1]
            id_ecu = pre_id_ecu.rsplit('/',1)[0]
            dic_clubs_id[f'{Club}'] = id_ecu
            dic_clubs_div[f'{Club}'] = div
        teamscount.append(Club)
        
        if EcuClub not in Liste_ecussons:
            Liste_ecussons.append(EcuClub)
            
        if position not in lpostes:
            lpostes.append(position)
            
        if country not in lnationalities:
            lnationalities.append(country)
            
        if div not in chpts:
            chpts.append(div)
        joueur = row[1]
        Joueurs.append(joueur)
    except:pass
for pt in preTeams:
    freq = teamscount.count(pt)
    if freq >= 4:
        Teams.append(pt)
# print(len(Teams))
lnationalities = sorted(lnationalities, reverse = False)

jerseys_home = [f for f in os.listdir("images/jerseys/home")]
jerseys_away = [f for f in os.listdir("images/jerseys/away")]
# jerseys_third = [f for f in os.listdir("images/jerseys/third")]
musics = ["musics/ambiance/"+m for m in os.listdir("musics/ambiance")]
flags = [f.rsplit('.',1)[0] for f in os.listdir("images/flags")]    
    

ldivs = []
dic_div_w_clubs = {}
for k,v in dic_clubs_div.items():
    if v not in ldivs:
        ldivs.append(v)

for div in ldivs:
    teams = []
    for equipe, chp in dic_clubs_div.items():
        if chp != None:
            if dic_clubs_div[f'{equipe}'] == div:
                # print(equipe,chp)
                teams.append(equipe)
                dic_div_w_clubs[f'{div}'] = teams
    # print(div,teams,len(teams),'\n')
            
#!!! 90% match

def remover():
    folder = 'temp/'
    for filename in os.listdir(folder):
        # print(filename)
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Echec à la suppression de %s. Raison: %s' % (file_path, e))

def main():
    def ExitApplication(fenetre):
        pygame.mixer.Channel(0).pause()
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("sounds/notif.wav"))
        MsgBox = messagebox.askquestion ('Exit Application',"Etes-vous sûr de vouloir quitter l'application ?", icon = 'warning', default = 'no', parent = fenetre)
        if MsgBox == 'yes':
            pygame.mixer.Channel(0).set_volume(1)
            cMusique.current(1)
            pygame.mixer.stop()
            fenetre.destroy()
            remover()
        else:
            pygame.mixer.Channel(0).unpause()
    
    playedmusics=[]
    def playmusic():
        songname =random.choice(musics)
        while songname in playedmusics:
            songname =random.choice(musics)
        currentmusic = (songname.rsplit('/',1)[1]).rsplit('.',1)[0]
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(songname))
        playedmusics.append(songname)
        Labmusique['text'] = 'Musique : ' + currentmusic
        if len(playedmusics) == len(musics):
            playedmusics.clear()

    def checkmusic():
        try:
            cMusique.get() 
            try:
                cMusique.get() == 'GO'
                if pygame.mixer.Channel(0).get_busy() == False:# and pygame.mixer.Channel(1).get_busy() == False:
                    playmusic()   
                timer()
            except:
                pass
        except:
            pass
        
    def timer():      
        cMusique.get()    
        try: 
            cMusique.get() == 'GO'
            tim = threading.Timer(12.0, checkmusic)
            tim.start()
        except:
            pygame.mixer.stop()
            tim.cancel()
            
    def ToggleSound():
        if Bmute['text'] == 'on':
            pygame.mixer.Channel(0).set_volume(0)
            Bmute['text'] = 'off'
            Bmute['relief'] = tk.SUNKEN

        else:
            pygame.mixer.Channel(0).set_volume(1)
            Bmute['text'] = 'on'
            Bmute['relief'] = tk.FLAT
            
    def TogglePause():
        if Bpause['text'] == 'on':
            pygame.mixer.Channel(0).pause()
            Bpause['text'] = 'off'
            Bpause['relief'] = tk.SUNKEN

        else:
            pygame.mixer.Channel(0).unpause()
            Bpause['text'] = 'on'
            Bpause['relief'] = tk.FLAT        
            
    def transfairlogo():
        blas1 = random.choice(blasons_id)
        blas2 = random.choice(blasons_id)
        while blas1==blas2:
            blas2 = random.choice(blasons_id)
        
        global blastrans1, blastrans2, fleche,contrat, interrogation
        blastrans1 = Image.open(f"images/ecussons/{blas1}.png").resize((140,140))
        blastrans1 = ImageTk.PhotoImage(blastrans1)
        blastrans2 = Image.open(f"images/ecussons/{blas2}.png").resize((175,175))
        blastrans2 = ImageTk.PhotoImage(blastrans2)
        
        fleche = Image.open(f"images/icones/fleche_default.png").resize((220,110)).rotate(-28)
        fleche = ImageTk.PhotoImage(fleche)
    
        contrat = Image.open(f"images/icones/contrat_default.png").resize((200,200))
        contrat = ImageTk.PhotoImage(contrat)
    
        interrogation = Image.open(f"images/icones/interrogation_default.png").resize((150,150)).rotate(-25)
        interrogation = ImageTk.PhotoImage(interrogation)
        
        canmain.create_image(1530,650, image = blastrans1)
        canmain.create_image(1795,865, image = blastrans2)
        canmain.create_image(1702,707, image = fleche)
        canmain.create_image(1575,900, image = contrat)
        canmain.create_image(1720,620, image = interrogation)
    
    def switch():
        global selected_players

        if Bbdd["text"] == 'off':
            Bbdd.configure(image = on_im, text ='on')
            selected_players = ''
        else:
            Bbdd.configure(image = off_im, text ='off')
            selected_players = 'AND TruePlayer = 0'
        club = label_disp.cget("text")
        upd_data_main(club)
    
    def set_new_fav():
        conn = sqlite3.connect(f'databases/alldata.db')
        c = conn.cursor()
        new_fav = label_disp.cget('text')
        id_ecu = dic_clubs_id[f'{new_fav}']
        
        c.execute(f"UPDATE Config SET default_team = ?",(new_fav,))
        conn.commit()
        conn.close()        
        global new_fav_path
        global new_fav_blason
        new_fav_path = f"images/ecussons/{id_ecu}.png"
        new_fav_blason = ImageTk.PhotoImage(Image.open(new_fav_path).resize((70,70)))     
        canmain.itemconfig(fav_ecu, image = new_fav_blason)
                   
    def parameters(Liste_ecussons):
        DW = int((fenetremain.winfo_screenwidth()))
        DH = int((fenetremain.winfo_screenheight()))
        fenetre_parameters = Toplevel(fenetremain)
        fenetre_parameters.title("Paramètres")
        fenetre_parameters.geometry(f'1280x720+{DW//6}+{DH//6}')
        fenetre_parameters.resizable(0, 0)
        fenetre_parameters.transient(fenetremain)
        background_image_param = PhotoImage(file = r"images/backgrounds/settings.png")
        
        canparam= Canvas(fenetre_parameters, width = 1280, height = 720)
        canparam.pack()
        canparam.create_image(0,0, image = background_image_param, anchor = tk.NW)

        # But_pic = hover_button(fenetre_parameters, text = "Download Players Pictures", font = main_menu_font,command = lambda:download_pic(Teams), width = 25, activebackground="#E8FFFF", activeforeground = "blue")
        # But_ecu = hover_button(fenetre_parameters, text = "Download Ecussons", font = main_menu_font,command = lambda: download_ecu(Liste_ecussons), width = 25, activebackground="#E8FFFF", activeforeground = "blue")
        # But_posi = hover_button(fenetre_parameters, text = "Update Players Positions", font = main_menu_font,command = updatePOS, width = 25, activebackground="#E8FFFF", activeforeground = "blue")
        
        But_data = hover_button(fenetre_parameters, text = "Update DATA FILES", font = main_menu_font,command = DataUpdate, width = 25, activebackground="#E8FFFF", activeforeground = "blue")
        But_data.place(relx=0.5, rely=0.4, anchor='center')
        
        But_learn = hover_button(fenetre_parameters, text = "Update Learning Model", font = main_menu_font,command = update_predic_model, width = 25, activebackground="#E8FFFF", activeforeground = "blue")
        But_learn.place(relx=0.5, rely=0.5, anchor='center')
        
        But_set_fav = hover_button(fenetre_parameters, text = "Actual Team to Fav Team", font = main_menu_font,command = set_new_fav, width = 25, activebackground="#E8FFFF", activeforeground = "blue")
        But_set_fav.place(relx=0.5, rely=0.6, anchor='center')
        
        fenetre_parameters.mainloop()


    def compair():
        equipe = combot.get()
        tCompair = process.extractOne(equipe,Teams)[0]
        label_disp['text'] = tCompair
        return(tCompair)
    
    def compairdiff(event):
        diff = labdiffteam.cget("text")
        club = compair()
        if diff == club:
            return
        upd_data_main(club)
    
    

    def upd_data_main(club):
        sorted_joueurs,players,id_ecu,wages,sellplayersvalues = calc_team_global(club,selected_players,dic_clubs_id)
        labsellv['text']= str(int(sellplayersvalues)) + "€"
        labwages['text']= str(int(wages)) + "€"
        try:
            comboj['values'] = sorted_joueurs
            comboj.current(0)
        except:pass
                 
        global myblason
        global blason_path
        try:
            blason_path = f"images/ecussons/{id_ecu}.png"
            myblason = ImageTk.PhotoImage(Image.open(blason_path))
            canmain.itemconfig(blas, image = myblason)
        except:pass
        
        squad = []
        basesquad = []
        for p in players:
            if p[6] != "RES":
                basesquad.append(p)
            squad.append(p)
        canmain.delete('data')
        agemoyen = 0
        notemoyenne = 0
        
        y=615
        # print(len(squad))
        try:
            for p in basesquad:
                notemoyenne = notemoyenne + p[2]
                agemoyen = agemoyen + p[3]
                
            for p in squad[:15]:
                if p[3]>32:
                    agecolor = 'red'
                elif p[3]>= 29:
                    agecolor = 'orange'
                elif p[3]>= 26:
                    agecolor = 'yellow'
                else:
                    agecolor = 'green yellow'
                
                notecolor =levelcolor(p[2])
                    
                canmain.create_text(40,y, width = 550,text = f'{p[1]}', font = main_menu_font, fill = 'white', tags = 'data', anchor = tk.W)
                canmain.create_text(230,y, width = 550,text = f'{p[2]}', font = main_menu_font, fill = notecolor, tags = 'data')
                canmain.create_text(290,y, width = 550,text = f'{p[3]}', font = main_menu_font, fill = agecolor, tags = 'data')
                canmain.create_text(345,y, width = 550,text = f'{p[4]}', font = main_menu_font, fill = 'white', tags = 'data')
                canmain.create_text(420,y, width = 550,text = f'{p[5]}', font = main_menu_font, fill = 'white', tags = 'data')
                y+=30
            
            agemoyensquad = round(agemoyen/len(basesquad),1)
            notemoyennesquad = round(notemoyenne/len(basesquad),1)
            labage["text"] = agemoyensquad
            
            if agemoyensquad <= 26:
                voyantcolor = 'vert'
            elif agemoyensquad <= 30:
                voyantcolor = 'orange'
            else:
                voyantcolor = 'rouge'
            
            global myvoyant, mystars
            myvoyant = ImageTk.PhotoImage(Image.open(f"images/icones/voyant{voyantcolor}.png"))
            canmain.itemconfig(canvoyant, image = myvoyant)
            if notemoyennesquad <= 65:
                coefrate = 0.8
            elif notemoyennesquad <= 70:
                coefrate = 0.86            
            elif notemoyennesquad <= 75:
                coefrate = 0.92
            elif notemoyennesquad <= 80:
                coefrate = 0.95
            else:
                coefrate = 1.1
            right = 1.25*(notemoyennesquad*coefrate)
            mystars =Image.open(f"images/icones/stars.png").resize((125,25))
            mystars =ImageTk.PhotoImage(mystars.crop((0,0,right,25)))
            canmain.itemconfig(etoiles, image = mystars)
        except:pass
      
        jersey_home = Image.open("images/jerseys/jersey_default.png")
        jersey_ratio_home = process.extractOne(club,jerseys_home)[1]
        if jersey_ratio_home >= 75:
            try:
                jersey_home_compair = process.extractOne(club,jerseys_home)[0]
                jersey_home = Image.open(f"images/jerseys/home/{jersey_home_compair}")
            except: pass
        
        jersey_home =  jersey_home.resize((250,250))
        
        jersey_away = Image.open("images/jerseys/jersey_default_exte.png")
        jersey_ratio_away = process.extractOne(club,jerseys_away)[1]
        if jersey_ratio_away >= 75:
            try:
                jersey_away_compair = process.extractOne(club,jerseys_away)[0]
                jersey_away = Image.open(f"images/jerseys/away/{jersey_away_compair}")
            except: pass            
        
        jersey_away =  jersey_away.resize((250,250))
        
        global myjerseyhome
        global myjerseyaway
        myjerseyhome = ImageTk.PhotoImage(jersey_home)
        myjerseyaway = ImageTk.PhotoImage(jersey_away)
        
        canmain.create_image(800,290, image = myjerseyhome)
        canmain.create_image(1100,290, image = myjerseyaway)
        
        
        setdata(players,0)
        transfairlogo()
        
        labdiffteam['text'] = club

        
    def pre_setdata(event):
        club = compair()
        conn = sqlite3.connect(f'databases/alldata.db')
        c = conn.cursor()
        joueurs = c.execute(f"SELECT Name,OVA,ID FROM Players WHERE Club = ?  AND NOT(TITU IS NULL) {selected_players}",(club,))
        ljoueurs = []
        
        for row in joueurs.fetchall():
            joueur = str(row[0])
            note = row[1]
            idjoueur = row[2]
            ljoueurs.append([idjoueur,joueur,note])
        players = sorted(ljoueurs, key = lambda x: x[2],reverse = True)
        sorted_joueurs = [adress[1] for adress in players]
        player_name = comboj.get()
        index = sorted_joueurs.index(f"{player_name}")
        setdata(players,index)
        transfairlogo()
        
    def setdata(players, option):
        try:
            idplayer = players[option][0]
            global myplayer
            canmain.delete('pdata')
            try:
                try:
                    implayer = (Image.open(f"images/players/{idplayer}.png").resize((160,160)))
                except:
                    implayer = (Image.open(f"images/icones/player_icone.png").resize((160,160)))
                myplayer = ImageTk.PhotoImage(implayer)
                canmain.itemconfig(play, image = myplayer)
            except:pass
            conn = sqlite3.connect(f'databases/alldata.db')
            c = conn.cursor()
            joueur = c.execute("SELECT Name,OVA,Height,Weight,foot,Joined,Contract,Nationality FROM Players WHERE ID = ?",(idplayer,))
            for row in joueur.fetchall():
                nom = row[0]
                note = row[1]
                taille = row[2]
                poids = row[3]
                pied = row[4]
                arrclub = row[5]
                contrat = row[6]
                pays = row[7]
                conn.close()
                
                inches = taille[:-1].rsplit("'",1)[1]
                feet2cm = float(taille.rsplit("'",1)[0])*30.48
                inch2cm = int(inches)*2.54
                taillecm = str(round(feet2cm +  inch2cm,2))
                
                poidslbs = int(poids.rsplit('lbs',1)[0])
                poidskg = str(round(poidslbs/2.205,2))
                
                global imageFlag
                flag =  process.extractOne(pays,flags)[0]
                imFlag = Image.open(f'images/flags/{flag}.png')
                imFlag = imFlag.resize((100,100))
                imageFlag = ImageTk.PhotoImage(imFlag)
                
                if pied == 'Right':
                    piedfr = 'Droit'
                else:
                    piedfr = 'Gauche'
                
                
                notecolor = levelcolor(note)
                
                x,y = 920, 775
                canmain.create_text(x,y, text = nom, font = dis_player_font, fill ='white', anchor =tk.E,tags ='pdata')
                canmain.create_text(x,y+40, text = str(note)+'/100', font = dis_player_font, fill = notecolor, anchor =tk.E, tags ='pdata')
                canmain.create_text(x,y+80, text = taillecm+' cm', font = dis_player_font, fill ='white', anchor =tk.E, tags ='pdata')
                canmain.create_text(x,y+120, text = poidskg+' kg', font = dis_player_font, fill ='white', anchor =tk.E, tags ='pdata')
                canmain.create_text(x,y+160, text = piedfr, font = dis_player_font, fill ='white', anchor =tk.E, tags ='pdata')
                canmain.create_text(x,y+200, text = arrclub, font = dis_player_font, fill ='white', anchor =tk.E, tags ='pdata')
                canmain.create_text(x,y+240, text = contrat, font = dis_player_font, fill ='white', anchor =tk.E, tags ='pdata')
                canmain.create_image(850, 650, image = imageFlag, tags ='pdata')
                conn.close()
        except:pass

    def teamdata():
        if len(combot.get())>0:
            team = compair()
            conn = sqlite3.connect(f'databases/alldata.db')
            c = conn.cursor()

            
            jersey_home = Image.open("images/jerseys/jersey_default.png")
            jersey_away = Image.open("images/jerseys/jersey_default.png")
            jersey_ratio_home = process.extractOne(team,jerseys_home)[1]
            jersey_ratio_away= process.extractOne(team,jerseys_away)[1]
            
            if jersey_ratio_home >= 75:
                try:
                    jersey_home_compair = process.extractOne(team,jerseys_home)[0]
                    jersey_home = Image.open(f"images/jerseys/home/{jersey_home_compair}")
                except: pass
            
            if jersey_ratio_away >= 75:
                try:
                    jersey_away_compair = process.extractOne(team,jerseys_away)[0]
                    jersey_away = Image.open(f"images/jerseys/away/{jersey_away_compair}")
                except: pass
            
            imEcusson = myblason
            
            jersey_home =  jersey_home.resize((207,207))
            imJersey_home = ImageTk.PhotoImage(jersey_home)
            jersey_away =  jersey_away.resize((207,207))
            imJersey_away = ImageTk.PhotoImage(jersey_away)
                
            joueurs = c.execute(f"SELECT Name,OVA,PlayerPhoto,BP,TITU,ID FROM Players WHERE Club = ? AND TITU IS NOT NULL {selected_players}",(team,))
    
            players = []
            
            for row in joueurs.fetchall():
                joueur_name = str(row[0])
                joueur_note = row[1]
                # joueur_photo = row[2]
                joueur_position = row[3]
                joueur_titu = row[4]
                joueur_ID = row[5]
                
                try:
                    imPlayer = Image.open(f'images/players/{joueur_ID}.png')
                except:
                    imPlayer = Image.open(f'images/icones/player_icone.png')
                
                imPlayer = imPlayer.resize((120,120))
                imagePlayer = ImageTk.PhotoImage(imPlayer)   
                
                
                players.append([joueur_name, joueur_note, joueur_position, joueur_titu,imagePlayer,joueur_ID])
            conn.close()
            return(players,team, imEcusson,imJersey_home,imJersey_away,jersey_home)



    def stats_display(team):
        # imEcusson = myblason
        # team_global(team,fenetremain,imEcusson,selected_players,main_menu_font,dic_clubs_id,blason_path)
        try: 
            imEcusson = myblason           
            try:team_global(team,fenetremain,imEcusson,selected_players,main_menu_font,dic_clubs_id,blason_path)
            except:pass
        except:pass
        
    def team_maker():
        try:
            players, team, imEcusson,imJersey_home,imJersey_away,jersey_home = teamdata()
            best_tactic(fenetremain,teamdata,selected_players)
        except:pass

    def player_attributes():
        if len(comboj.get()) >1:
            players_stats(fenetremain,Joueurs,label_disp, comboj,dic_clubs_id,main_menu_font)
            
    def transfers():
        database_update(Teams,dic_clubs_id,fenetremain,main_menu_font,lnationalities,lpostes,'')

    if first_use == True:
        fenetre.destroy()
        pygame.mixer.stop()
    
    conn = sqlite3.connect(f'databases/alldata.db')
    c = conn.cursor()
    c.execute(f"SELECT default_team FROM Config")
    row = c.fetchone()
    conn.close()
    favourite_team = row[0]
    favourite_team_id = dic_clubs_id[f'{favourite_team}']
    

    pygame.mixer.Channel(2).play(pygame.mixer.Sound("sounds/load.wav"))

    fenetremain = tix.Tk()
    fenetremain.title("Football Manag'Air")
    fenetremain.iconphoto(False, PhotoImage(file='images/icones/root_icone.png'))
    DW = int((fenetremain.winfo_screenwidth()))
    DH = int((fenetremain.winfo_screenheight()))
    fenetremain.geometry(f"{DW}x{DH}+0+0")
    fenetremain.resizable(0, 0)
    fenetremain.bind("<F11>", lambda event: fenetremain.attributes("-fullscreen",
                                    not fenetremain.attributes("-fullscreen")))
    fenetremain.bind("<Escape>", lambda event: fenetremain.attributes("-fullscreen", False))
    
    Lcmusique = ["GO", "STOP"]
    cMusique = ttk.Combobox(fenetremain, values = Lcmusique)
    cMusique.current(0)
        
    main_menu_font = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
    dis_player_font = tkFont.Font(family='Helvetica', size=16, weight=tkFont.BOLD)

    canmain = Canvas(fenetremain, width= DW,height=DH)
    canmain.pack()
    background_image = PhotoImage(file = r"images/backgrounds/accueil.png")
    
    favourite_team_ecu = ImageTk.PhotoImage(Image.open(f"images/ecussons/{favourite_team_id}.png").resize((68,68)))

    blason = PhotoImage(file = r"images/icones/default_blason.png")
    playerimg = PhotoImage(file = r"images/icones/player_icone.png")

    canmain.create_image(0,0, image = background_image, anchor = tk.NW)
    fav_ecu= canmain.create_image(5,5, image = favourite_team_ecu, anchor = tk.NW)
    blas = canmain.create_image(150,274, image = blason, tags ='blason')
    play = canmain.create_image(625,648, image = playerimg, tags ='player')

    stars = ImageTk.PhotoImage(Image.open(f"images/icones/stars.png").resize((125,25)))
    etoiles = canmain.create_image(1750, 360, image = stars)
    
    voyant = ImageTk.PhotoImage(Image.open(f"images/icones/voyantrouge.png").resize((50,50)))
    canvoyant = canmain.create_image(1775, 310, image = voyant, tags="voyant")
    
    canmain.create_text(240,575, width = 550,text = '       Name                             NOTE      AGE        BP      POSITIONS', font = main_menu_font, fill = 'white')

    x,y = 515, 775
    canmain.create_text(x,y, text = 'Nom du Joueur :', fill='white', font = dis_player_font, anchor = tk.W)
    canmain.create_text(x,y+40, text = 'Note :', fill='white', font = dis_player_font, anchor = tk.W)
    canmain.create_text(x,y+80, text = 'Taille :', fill='white', font = dis_player_font, anchor = tk.W)
    canmain.create_text(x,y+120, text = 'Poids :', fill='white', font = dis_player_font, anchor = tk.W)
    canmain.create_text(x,y+160, text = 'Pied Fort :', fill='white', font = dis_player_font, anchor = tk.W)
    canmain.create_text(x,y+200, text = 'Arrivé le :', fill='white', font = dis_player_font, anchor = tk.W)
    canmain.create_text(x,y+240, text = 'Contrat :', fill='white', font = dis_player_font, anchor = tk.W)


    Labmusique = Label(fenetremain, text = '', width = 50,font = main_menu_font, fg = 'white', bg = '#2F55B5')
    Labmusique.place(x = 600, y = 25)
    playmusic()
    
    nextmusic = PhotoImage(file = r'images/icones/next.png')
    Bnext = Button(fenetremain, image = nextmusic, command = playmusic,bg = '#2F55B5', activebackground = '#2F55B5', relief = tk.GROOVE)
    Bnext.place(x=1050, y = 20)

    mutemusic = PhotoImage(file = r'images/icones/mute.png')
    Bmute = Button(fenetremain, image = mutemusic, command = ToggleSound,bg = '#2F55B5', activebackground = '#2F55B5', relief = tk.FLAT, text ='on')
    Bmute.place(x=628, y = 20)

    pausemusic = PhotoImage(file = r'images/icones/pause.png')
    Bpause = Button(fenetremain, image = pausemusic, command = TogglePause,bg = '#2F55B5', activebackground = '#2F55B5', relief = tk.FLAT, text ='on')
    Bpause.place(x=582, y = 20)
    
 
    #Dynam Team info
    labinfowages = Label(fenetremain, text = 'Coût Salaires Hebdomadaires :', bg = '#2B0C47', fg = 'white', font = main_menu_font)
    labinfowages.place(x = 1400, y = 200)
    labinfosellv= Label(fenetremain, text = 'Valeur Totale des Joueurs :', bg = '#2B0C47', fg = 'white', font = main_menu_font)
    labinfosellv.place(x=1400, y = 250)
    labinfoage = Label(fenetremain, text = 'Age Moyen Joueurs Titulaires :', bg = '#2B0C47', fg = 'white', font = main_menu_font)
    labinfoage.place(x=1400, y = 300)
    labinfonote = Label(fenetremain, text = 'Note Moyenne Joueurs Titulaires :', bg = '#2B0C47', fg = 'white', font = main_menu_font)
    labinfonote.place(x=1400, y = 350)
    
    labwages= Label(fenetremain, text = 'N/C', bg = '#2B0C47', fg = 'white', font = main_menu_font)
    labwages.place(x = 1700, y = 200)
    labsellv= Label(fenetremain, text = 'N/C', bg = '#2B0C47', fg = 'white', font = main_menu_font)
    labsellv.place(x=1700, y = 250)
    labage= Label(fenetremain, text = 'N/C', bg = '#2B0C47', fg = 'white', font = main_menu_font)
    labage.place(x = 1700, y = 300)
    

    #Switch Database
    on_im = PhotoImage(file = r'images/icones/on.png')
    off_im = PhotoImage(file = r'images/icones/off.png')
    Bbdd = Button(fenetremain, text='off',image = off_im, bg ='#2F55B5', activebackground ='#2F55B5',relief = tk.FLAT,command = switch)
    Bbdd.place(x=250,y=15.5)

    # Combo and labels
    y = 215
    labselecteam = Label(fenetremain,text="Equipe", justify='center', width = 20, bg ='#2B0C47', fg = 'white', font = main_menu_font)
    labselecteam.place(x=320, y= y)
    combot = AutocompleteCombobox(fenetremain,justify='center', update_form = compairdiff)
    combot.configure(width = 30)
    combot.set_completion_list(Teams)
    combot.set(favourite_team)
    combot.bind("<<ComboboxSelected>>",compairdiff)
    combot.place(x=320, y=y+35)
 
    label_disp = Label(fenetremain,text = favourite_team, width = 20, bg ='#2B0C47', fg = 'white', font = main_menu_font)
    label_disp.place(x=45, y= 405)
    
    labdiffteam = Label(fenetremain)

    labselecj = Label(fenetremain,text="Joueur", justify='center', width = 20, bg ='#2B0C47', fg = 'white', font = main_menu_font)
    labselecj.place(x=320, y= y+75)    
    comboj = ttk.Combobox(fenetremain, width = 60, justify='center',state = "readonly")
    comboj.place(x=320, y=y+110)
    comboj.configure(width = 30)
    comboj.bind("<<ComboboxSelected>>", pre_setdata)
    
    bouton_team = hover_button(fenetremain, text = 'Saison Equipe', command = lambda:stats_display(label_disp.cget("text")), bg ='#5DFEE6',activebackground="#E8FFFF", activeforeground = "blue",height = 3,width = 40, font = main_menu_font)
    bouton_team.place(x=35, y= 470)
    
    bouton_player = hover_button(fenetremain, text = 'Statistiques du Joueur', command = player_attributes, bg ='#5DFEE6', activebackground="#E8FFFF", activeforeground = "blue",height = 3,width = 40, font = main_menu_font)
    bouton_player.place(x=515, y= 470)
    
    bouton_tactic = hover_button(fenetremain, text = 'Coach Virtuel', command = team_maker, bg ='#5DFEE6', activebackground="#E8FFFF", activeforeground = "blue", height = 3,width = 40, font = main_menu_font)
    bouton_tactic.place(x=985, y= 470)

    tactical = PhotoImage(file = r"images/icones/tactics_default.png")
    labtact = Label(fenetremain, image = tactical, relief = tk.RIDGE, bg='#1F2025')
    labtact.place(x=1025,y=575)
   
    bouton_transfers = hover_button(fenetremain, text = "Management", command = transfers, bg ='#5DFEE6', activebackground="#E8FFFF", activeforeground = "blue",height = 3,width = 40, font = main_menu_font)
    bouton_transfers.place(x=1455, y= 470)
    
    settings = PhotoImage(file = r"images/icones/options.png")
    bouton_param = hover_button(fenetremain, text = 'Paramètres', command = lambda:parameters(Liste_ecussons), image = settings,relief = tk.FLAT, bg = '#360F58', activebackground='#360F58')
    bouton_param.place(x=1752, y= 16)
    
    clockdate = Clock(fenetremain)
    clockdate.configure(bg = '#360F58', fg='white',font=("helvetica",14))
    clockdate.place(x=1628, y= 14)
    w = Label(fenetremain, text=f"{dt.datetime.now():%a, %b %d %Y}", fg="white", bg = '#360F58',font=("helvetica", 9))
    w.place(x=1615, y= 40)

    upd_data_main(favourite_team)
    transfairlogo()
    timer()

    fenetremain.protocol("WM_DELETE_WINDOW", lambda:ExitApplication(fenetremain))
    fenetremain.mainloop()

if __name__=='__main__':
    def upd_team(event):
        team = comboteams.get()
        if team != "Choisis Ton Club Préféré":
            comparaison = process.extractOne(team,Teams)[0]
            lab_team["text"] = comparaison
            id_ecu = dic_clubs_id[f'{comparaison}']
            global ecu_path
            global favblason
            ecu_path = f"images/ecussons/{id_ecu}.png"
            favblason = ImageTk.PhotoImage(Image.open(ecu_path).resize((290,290)))
            can_launch.itemconfig(ecusson, image = favblason)

        
    def pre_launch():
        favourite_team = lab_team.cget('text')
        c.execute(f"UPDATE Config SET default_team = ?, first_use = ?",(favourite_team,0,))
        conn.commit()
        conn.close()
        main()
    
    favourite_team = ''
    first_use = False
    conn = sqlite3.connect(f'databases/alldata.db')
    c = conn.cursor()
    config = c.execute(f"SELECT default_team,first_use FROM Config")
    for row in config.fetchall():
        favourite_team = row[0]
        uses = row[1]
        if uses == 1:
            first_use = True
            
    if first_use == True:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("musics/Main Menu.wav"))
        
        fenetre = tix.Tk()
        fenetre.title("Football Manag'Air")
        fenetre.iconphoto(False, PhotoImage(file='images/icones/root_icone.png'))
        
        DW = fenetre.winfo_screenwidth()
        DH = fenetre.winfo_screenheight()
        
        fenetre.geometry(f"{DW}x{DH}+0+0")
        fenetre.minsize(DW//2, DH//2)
        fenetre.bind("<F11>", lambda event: fenetre.attributes("-fullscreen",
                                        not fenetre.attributes("-fullscreen")))
        fenetre.bind("<Escape>", lambda event: fenetre.attributes("-fullscreen", False))
                
        
        can_launch = Canvas(fenetre,width = DW, height = DH)
        can_launch.pack()
        bg_image = ImageTk.PhotoImage(Image.open(r"images/backgrounds/test.png"))
        
        can_launch.create_image(0,0,anchor = tk.NW, image = bg_image)        
        ecusson = can_launch.create_image(DW//2, DH//2-120, anchor = 'center')
        # print(DW//2-125,DH//2-275)

        first_screen_font = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        bt_width = 38
        
        comboteams = AutocompleteCombobox(fenetre,justify='center', update_form = upd_team)
        comboteams.configure(width = 60)
        comboteams.set_completion_list(Teams)
        comboteams.set('Choisis Ton Club Préféré')
        comboteams.bind("<<ComboboxSelected>>",upd_team)
        comboteams.place(relx=0.5, rely=0.58, anchor='center')
        
        lab_team = Label(fenetre)
        button_start = hover_button(fenetre, text="Start", font = first_screen_font,command = pre_launch, bg = '#274A6E', fg = 'white',activebackground="#E8FFFF", activeforeground = "blue", width = bt_width, height = 3)
        button_start.place(relx=0.5, rely=0.65, anchor='center')
        
        fenetre.protocol("WM_DELETE_WINDOW", lambda:(pygame.mixer.stop(), fenetre.destroy()))
        fenetre.mainloop()
    else:
        c = conn.close()
        main()
        