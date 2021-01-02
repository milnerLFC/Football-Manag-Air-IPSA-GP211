# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 19:21:19 2020

@author: benja
"""
import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, Label, Canvas, Button, Toplevel, PhotoImage, messagebox
from PIL import Image, ImageTk, ImageEnhance
from fuzzywuzzy import process
from module_classes import AutocompleteCombobox, hover_button,cursor_entry_int,cursor_entry_str
from definitions import testpost,testsubposte,prepair_global_team,levelcolor
import pandas as pd
import pygame
import matplotlib.pyplot as plt
import math
from math import pi

import os
import tensorflow as tf
import tensorflow_probability as tfp

tfd = tfp.distributions
# from player_gen import 

import datetime

#%%

def database_update(Teams,dic_clubs_id,fenetremain,main_menu_font,lnationalities,lpostes,selected_players):
        plotsavepathspider = "temp/spider_new_player.png"
        dico_cat = {"Buteur": ['LS','ST','RS'],"Ailier":['LW','RW'],"Attaquant":['LF','CF','RF'],
                    "Milieu Offensif":['LAM','CAM','RAM'],"Milieu Latéral":['LM','RM'],"Milieu Central":['LCM','CM','RCM'],
                    "Milieu Défensif":['LDM','CDM','RDM'],"Latéral":['LWB','RWB'],"Défenseur Central":['LCB','CB','RCB'],
                    "Défenseur Latéral":['LB','RB'],"Gardien":['GK']}
        dico_num = {'Buteur' : 10,'Ailier':7,'Attaquant':9,'Milieu Offensif':8,'Milieu Latéral':6,'Milieu Central':5,'Milieu Défensif':4,'Latéral':3,'Défenseur Central':1,'Défenseur Latéral':2,'Gardien':0}
        
        encoded_size = 4
        label_size = len(dico_num)+1
        prior = tfd.Independent(tfd.Normal(loc=tf.zeros(encoded_size,1), scale=1),
                                    reinterpreted_batch_ndims=1)
        lpostes = sorted(lpostes, reverse = False)

        conn = sqlite3.connect('databases/alldata.db')
        cursor = conn.execute('select * from Players')
        all_columns = list(map(lambda x: x[0], cursor.description))

        column_to_remove_list = ['ID', 'Name', 'Age', 'OVA', 'Nationality', 'Club', 'BOV', 'BP', 'Position', 'PlayerPhoto', 
                                'ClubLogo', 'FlagPhoto', 'Team&Contract', 'Height', 'Weight', 'foot', 'Joined', 
                                'LoanDateEnd', 'Value', 'Wage', 'ReleaseClause', 'Contract','Attacking','Skill','Movement',
                                'Power','Mentality','Defending','Goalkeeping','A/W','D/W','Hits',
                                'BaseStats','TotalStats','team_jersey_number','TruePlayer','TITU','championnat']
        columns = list(set(all_columns) - set(column_to_remove_list))
        columns = sorted(columns)

        conn.close()
        
        def new_chp(team):
            chp = ''
            conn = sqlite3.connect(f'databases/alldata.db')
            c = conn.cursor()
            joueurs = c.execute(f"SELECT championnat FROM Players WHERE Club = ? AND TITU IS NOT NULL AND TruePlayer = 0",(team,))
            
            for j in joueurs.fetchall():
                if chp == '':
                    chp = j[0]
                else:
                    conn.close()
                    return(chp)
        
        def getplayerid():
            joueur = combojtr.get()
            exclub = lab_exclub.cget("text")
            conn = sqlite3.connect('databases/alldata.db')
            c = conn.cursor()
            precommit = c.execute("SELECT ID FROM Players WHERE Name = ? AND Club = ? AND NOT(TITU IS NULL)",(joueur,exclub,))
            try:
                player_id = precommit.fetchone()[0]
            except:
                player_id = 0
            conn.close()
            return(player_id)


        def sort_player(poste):
            if poste == 'Attaquant':
                attaquants.append(infojoueur)
            elif poste == 'Milieu':
                milieux.append(infojoueur)
            elif poste == 'Défenseur':
                défenseurs.append(infojoueur)
            else:
                gardiens.append(infojoueur)   
                
        def team_evolution(club, sup_player_id):
            dictpostes = {'Attaquant':(['LS','ST','RS','LW','LF','CF','RF','RW']),'Milieu':(['LAM','CAM','RAM','LM','LCM','CM','RCM','RM','LDM','CDM','RDM']),
                          'Défenseur' : (['LWB','RWB','LB','LCB','CB','RCB','RB']),'Gardien':(['GK']),'Remplaçant':(['SUB']),'Réserviste':(['RES'])}
            dictlenpostes = {'LS':0,'ST':0,'RS':0,'LW':0,'LF':0,'CF':0,'RF':0,'RW':0,'LAM':0,'CAM':0,'RAM':0,'LM':0,'LCM':0,'CM':0,'RCM':0,'RM':0,'LDM':0,'CDM':0,'RDM':0,
                              'LWB':0,'RWB':0,'LB':0,'LCB':0,'CB':0,'RCB':0,'RB':0,'GK':0}
            dictsubpost = {'Buteurs' : (['LS','ST','RS']),'Ailiers':(['LW','RW']), 'Forwards':(['LF','CF','RF']), 'Off.' : (['LAM','CAM','RAM']),
                            'Equi.':(['LM','LCM','CM','RCM','RM']),'Déf.':(['LDM','CDM','RDM']),'Latéraux':(['LWB','RWB','LB','RB']),'Centraux':(['LCB','CB','RCB']),' ':(['GK'])}
            dictlensubp = {'Buteurs':0,'Ailiers':0,'Forwards':0,'Off.':0,'Equi.':0,'Déf.':0,'Latéraux':0,'Centraux':0,' ':0}
            
            global attaquants,milieux,défenseurs,gardiens
            attaquants,milieux,défenseurs,gardiens = [],[],[],[]
        
            conn = sqlite3.connect(f'databases/alldata.db')
            c = conn.cursor()
            joueurs = c.execute(f"SELECT Name,OVA,POT,TITU,BP,championnat FROM Players WHERE Club = ? AND TITU IS NOT NULL {selected_players}",(club,))
            
            try:
                for j in joueurs.fetchall():
                    nom = j[0]
                    note = j[1]
                    potentiel = j[2] - note
                    global infojoueur
                    infojoueur = [nom,note,potentiel]
                    titu = j[3]
                    if titu == 'SUB' or titu == 'RES':
                        bpost = j[4]
                        dictlenpostes[f'{bpost}'] +=1
                        poste = testpost(dictpostes,bpost)
                        testsubposte(dictsubpost,dictlensubp,bpost)
                        sort_player(poste)
                    else:
                        dictlenpostes[f'{titu}'] +=1
                        poste = testpost(dictpostes,titu)
                        testsubposte(dictsubpost,dictlensubp,titu)
                        sort_player(poste)
        
            except : pass
            if sup_player_id != 0:
                joueur = c.execute(f"SELECT Name,OVA,POT,TITU,BP,championnat FROM Players WHERE ID = ? AND TITU IS NOT NULL {selected_players}",(sup_player_id,))
                for j in joueur.fetchall():
                    nom = j[0]
                    note = j[1]
                    try:
                        potentiel = j[2] - note
                    except:
                        potentiel = 0
                    infojoueur = [nom,note,potentiel]
                    titu = j[3]
                    if titu == 'SUB' or titu == 'RES':
                        bpost = j[4]
                        dictlenpostes[f'{bpost}'] +=1
                        poste = testpost(dictpostes,bpost)
                        testsubposte(dictsubpost,dictlensubp,bpost)
                        sort_player(poste)
                    else:
                        dictlenpostes[f'{titu}'] +=1
                        poste = testpost(dictpostes,titu)
                        testsubposte(dictsubpost,dictlensubp,titu)
                        sort_player(poste)
            conn.close()
            
            dfliste = []
            global_team = prepair_global_team(attaquants,milieux,défenseurs,gardiens)
            for squad in global_team:
                try:
                    dicdata = {'group': ['Notes']}
                    somme = 0

                    if squad[0][0] != 0:
                        dicdata['ATT'] = squad[0][0]
                        somme = somme + squad[0][0]
                    if squad[1][0] != 0:
                        dicdata['MIL'] = squad[1][0]
                        somme = somme + squad[1][0]
                    if squad[2][0] != 0:
                        dicdata['DEF'] = squad[2][0]
                        somme = somme + squad[2][0]
                    if squad[3][0] != 0:
                        dicdata['GAR'] = squad[3][0]
                        somme = somme + squad[3][0]
    
            
                    dfteam = pd.DataFrame(dicdata)
                    dfliste.append(dfteam)
                except:
                    pass
            return(dfliste)
        
        def update_notes(bigdf,bigdf2):
            # Premiere Colonne Titus
            try:
                labTitusatt['text'] = bigdf[0]['ATT'][0]
            except: labTitusatt['text'] = "N/C"
            try:
                labTitusmil['text'] = bigdf[0]['MIL'][0]
            except: labTitusmil['text'] = "N/C"
            try:
                labTitusdef['text'] = bigdf[0]['DEF'][0]
            except: labTitusdef['text'] = "N/C"
            try:
                labTitusgar['text'] = bigdf[0]['GAR'][0]
            except:labTitusgar['text'] = "N/C"
            # Premiere Colonne Subs
            try:
                labSubsatt['text'] = bigdf[1]['ATT'][0]
            except: labSubsatt['text'] = 'N/C'
            try:
                labSubsmil['text'] = bigdf[1]['MIL'][0]
            except: labSubsmil['text'] = 'N/C'
            try:
                labSubsdef['text'] = bigdf[1]['DEF'][0]
            except: labSubsdef['text'] = 'N/C'
            try:
                labSubsgar['text'] = bigdf[1]['GAR'][0]
            except: labSubsgar['text'] = 'N/C'

            # Deuxieme Colonne Titus
            try:
                lab2Titusatt['text'] = bigdf2[0]['ATT'][0]
            except:
                lab2Titusatt['text'] = 'N/C'
            try:
                if (labTitusatt.cget('text') == 'N/C' and lab2Titusatt.cget('text') != 'N/C'):
                    flechetitatt['image'] = fleche_vert
                elif bigdf2[0]['ATT'][0] > bigdf[0]['ATT'][0]:
                    flechetitatt['image'] = fleche_vert
                elif bigdf2[0]['ATT'][0] < bigdf[0]['ATT'][0]:
                    flechetitatt['image'] = fleche_rouge
                else:
                    flechetitatt['image'] = fleche_default
            except: flechetitatt['image'] = fleche_default
                            
            try:
                lab2Titusmil['text'] = bigdf2[0]['MIL'][0]
            except:
                lab2Titusmil['text'] = 'N/C'
            try:
                if (labTitusmil.cget('text') == 'N/C' and lab2Titusmil.cget('text') != 'N/C'):
                    flechetitmil['image'] = fleche_vert
                elif bigdf2[0]['MIL'][0] > bigdf[0]['MIL'][0]:
                    flechetitmil['image'] = fleche_vert
                elif bigdf2[0]['MIL'][0] < bigdf[0]['MIL'][0]:
                    flechetitmil['image'] = fleche_rouge
                else:
                    flechetitmil['image'] = fleche_default
            except: flechetitmil['image'] = fleche_default
                
                
            try:
                lab2Titusdef['text'] = bigdf2[0]['DEF'][0]
            except:
                lab2Titusdef['text'] = "N/C" 
            try:
                if (labTitusdef.cget('text') == 'N/C' and lab2Titusdef.cget('text') != 'N/C'):
                    flechetitdef['image'] = fleche_vert
                elif bigdf2[0]['DEF'][0] > bigdf[0]['DEF'][0]:
                    flechetitdef['image'] = fleche_vert
                elif bigdf2[0]['DEF'][0] < bigdf[0]['DEF'][0]:
                    flechetitdef['image'] = fleche_rouge
                else:
                    flechetitdef['image'] = fleche_default
            except: flechetitdef['image'] = fleche_default


            try:
                lab2Titusgar['text'] = bigdf2[0]['GAR'][0]
            except:
                lab2Titusgar['text'] = "N/C"
            try:
                if (labTitusgar.cget('text') == 'N/C' and lab2Titusgar.cget('text') != 'N/C'):
                    flechetitgar['image'] = fleche_vert
                elif bigdf2[0]['GAR'][0] > bigdf[0]['GAR'][0]:
                    flechetitgar['image'] = fleche_vert
                elif bigdf2[0]['GAR'][0] < bigdf[0]['GAR'][0]:
                    flechetitgar['image'] = fleche_rouge
                else:
                    flechetitgar['image'] = fleche_default
            except: flechetitgar['image'] = fleche_default

            # Deuxieme Colonne Subs
            try:
                lab2Subsatt['text'] = bigdf2[1]['ATT'][0]
            except:
                lab2Subsatt['text'] = 'N/C'
            try:
                if (labSubsatt.cget('text') == 'N/C' and lab2Subsatt.cget('text') != 'N/C') or bigdf2[1]['ATT'][0] > bigdf[1]['ATT'][0]:
                    flechesubatt['image'] = fleche_vert
                elif bigdf2[1]['ATT'][0] < bigdf[1]['ATT'][0]:
                    flechesubatt['image'] = fleche_rouge
                else:
                    flechesubatt['image'] = fleche_default
            except: flechesubatt['image'] = fleche_default


            try:
                lab2Subsmil['text'] = bigdf2[1]['MIL'][0]
            except:
                lab2Subsmil['text'] = 'N/C'
            try:
                if (labSubsmil.cget('text') == 'N/C' and lab2Subsmil.cget('text') != 'N/C') or bigdf2[1]['MIL'][0] > bigdf[1]['MIL'][0]:
                    flechesubmil['image'] = fleche_vert
                elif bigdf2[1]['MIL'][0] < bigdf[1]['MIL'][0]:
                    flechesubmil['image'] = fleche_rouge
                else:
                    flechesubmil['image'] = fleche_default
            except: flechesubmil['image'] = fleche_default

            
            try:
                lab2Subsdef['text'] = bigdf2[1]['DEF'][0]
            except:
                lab2Subsdef['text'] = 'N/C'
            try:
                if (labSubsdef.cget('text') == 'N/C' and lab2Subsdef.cget('text') != 'N/C') or bigdf2[1]['DEF'][0] > bigdf[1]['DEF'][0]:
                    flechesubdef['image'] = fleche_vert
                elif bigdf2[1]['DEF'][0] < bigdf[1]['DEF'][0]:
                    flechesubdef['image'] = fleche_rouge
                else:
                    flechesubdef['image'] = fleche_default
            except: flechesubdef['image'] = fleche_default


            try:
                lab2Subsgar['text'] = bigdf2[1]['GAR'][0]
            except:
                lab2Subsgar['text'] = 'N/C'
            try:
                if (labSubsgar.cget('text') == 'N/C' and lab2Subsgar.cget('text') != 'N/C') or bigdf2[1]['GAR'][0] > bigdf[1]['GAR'][0]:
                    flechesubgar['image'] = fleche_vert
                elif bigdf2[1]['GAR'][0] < bigdf[1]['GAR'][0]:
                    flechesubgar['image'] = fleche_rouge
                else:
                    flechesubgar['image'] = fleche_default
            except: flechesubgar['image'] = fleche_default        
        def rootdynam(event):
            # comboOldteam['state'] = 'normal'   
            global imageblas
            
            equipe = comboNewteam.get()
            club = process.extractOne(equipe,Teams)[0]
            lab_newclub['text'] = club
            id_ecu = dic_clubs_id[f'{club}']
            # sorted_joueurs,players,id_ecu,wages,sellplayersvalues = calc_team_global(club,selected_players,dic_clubs_id)
            
            
            bigdf = team_evolution(club,0)
            sup_player_id = getplayerid()
            if sup_player_id != 0:
                bigdf2 = team_evolution(club,sup_player_id)
            else:
                bigdf2 = bigdf
         
            imblas = Image.open(f'images/ecussons/{id_ecu}.png')
            imblas = imblas.resize((340,340))
            imblas = imblas.rotate(25)
            imblas = imblas.crop((75,75,275,275))
            imblas = ImageEnhance.Brightness(imblas)
            imblas = imblas.enhance(0.75)
            imageblas = ImageTk.PhotoImage(imblas)
            cantrans.itemconfig(canblason, image = imageblas)
            
            try:
                update_notes(bigdf,bigdf2)
            except:
                pass
            try:
                add_p_dynam(sup_player_id)
            except:
                pass
            
        def updatecombojoueurs(event):
            oldteam = comboOldteam.get()
            exclub = process.extractOne(oldteam,Teams)[0]
            lab_exclub["text"] = exclub
            conn = sqlite3.connect(f'databases/alldata.db')
            c = conn.cursor()
            joueurs = c.execute("SELECT Name,OVA,ID,Club FROM Players WHERE Club = ?  AND NOT(TITU IS NULL)",(exclub,))
            ljoueurstr = []
            
            for row in joueurs.fetchall():
                joueur = str(row[0])
                note = row[1]
                idjoueur = row[2]
                ljoueurstr.append([idjoueur,joueur,note])
            conn.close()
            playerstr = sorted(ljoueurstr, key = lambda x: int(x[2]),reverse = True)
            sorted_joueurstr = [adress[1] for adress in playerstr]
            try:
                combojtr['values'] = sorted_joueurstr
                combojtr['state'] = 'readonly'
                combojtr.current(0)
            except:pass
            set_image_transfer(None)
            rootdynam(None)
#%%
         #!!! TRANSFERT JOUEUR

        def newtransfer():
            Btransfer["state"] = tk.DISABLED
            Baddplayer["state"] = tk.NORMAL
            for w in labname, labcountry,labage,labposit,lab_couloir,labtaille,labfoot,labpoids,labcontrat,labniveau,Ename,Cpays,Eage,comboposit,Etaille,Epoids,combofoot,Econtrat,Eniveau,combo_poste,Bphoto,Bdata:
                w.place_forget()

            x,y = 100, 350
            for w in laboldteam,labtrjoueur:
                w.place(x=x,y=y)
                y += 50
            # lab_upd_values.place(x=x,y=600)
            
            x = 350
            y= 358
            for w in comboOldteam,combojtr :
                w.place(x = x, y =y)
                y += 50
            # combo_upd_values.place(x=x,y=608)
            # E_upd_value.place(x=x,y=650)
                
            
            Bcommittransfer.place(x = 160, y = 500)
            # Bcommit_value.place(x=200, y =745)

        def set_image_transfer(event):
            try:
                player_id = getplayerid()
            
                imagepath = f'images/players/{player_id}.png'
                global Playerpic
                Playerpic = ImageTk.PhotoImage(Image.open(imagepath).resize((180,180)))
                cantrans.itemconfig(canplayer, image = Playerpic)
                rootdynam(None)
            except:pass


        def committransfer():
            joueur = combojtr.get()
            if len(joueur) == 0:
                MsgBox = messagebox.showinfo('Pas de joueur sélectionné',f"Veuillez choisir un joueur au préalable !", icon = 'warning')
                return
            exclub = lab_exclub.cget("text")
            newclub = lab_newclub.cget("text")
            if exclub == newclub:
                MsgBox = messagebox.showinfo('Transfer Impossible',f"Veuillez choisir deux clubs différents.", icon = 'warning')
                return             
            chp = new_chp(newclub)
            MsgBox = messagebox.askokcancel('Alerte Transfert',f"{joueur} va être transféré de {exclub} à {newclub}.\nContinuer ?", icon = 'warning', default = 'ok')#, parent = fenetre)
            if MsgBox == True:
                conn = sqlite3.connect('databases/alldata.db')
                c = conn.cursor()
                precommit = c.execute("SELECT ID FROM Players WHERE Name = ? AND Club = ? AND NOT(TITU IS NULL)",(joueur,exclub,))
                player_id = precommit.fetchone()[0]

                c.execute('''UPDATE Players
                SET Club = ?, championnat = ?
                WHERE ID = ?''',(newclub,chp,player_id,))
                conn.commit()
                conn.close()
                pygame.mixer.Channel(2).play(pygame.mixer.Sound("sounds/airplane.wav"))
                MsgBox = messagebox.showinfo('Transfert Effectué',f"{joueur} vient d'être transféré de {exclub} à {newclub} !", icon = 'warning')#, parent = fenetre)
                updatecombojoueurs(None)
#%%
        #!!! NOUVEAU JOUEUR

        def addnewplayer():
            Btransfer["state"] = tk.NORMAL
            Baddplayer["state"] = tk.DISABLED
            
            for w in Bcommittransfer,comboOldteam,combojtr,laboldteam,labtrjoueur:#,combo_upd_values,E_upd_value,Bcommit_value,lab_upd_values :
                w.place_forget()
            
            x,y = 100,250
            for w in labname,labcountry,labage,labposit,lab_couloir,labtaille,labpoids,labfoot,labcontrat,labniveau:
                w.place(x=x,y=y)
                y += 50
            
            
            x = 350
            y= 200
            for w in Ename,Cpays,Eage,comboposit,combo_poste,Etaille,Epoids,combofoot,Econtrat,Eniveau:
                if y == 250 or y == 350 or y == 400 or y ==550:
                    y += 50
                    w.place(x=x, y = y+8)
                elif y < 750:
                    y += 50
                    w.place(x = x, y =y)
                else:
                    y += 100
                    w.place(x = x, y =y)
                    
            Bphoto.place(x=350,y=775)
            
            Bdata.place(x=200,y=850)
            
                
        def pictdl():
            global picturepath
            path = filedialog.askopenfilename(initialdir = "images",title = "Photo du Joueur",filetypes = (("PNG","*.png"),("all files","*.*")))
            if path != '':
                picturepath = str(path)

                global NewPlayerpic
                NewPlayerpic = ImageTk.PhotoImage(Image.open(picturepath).resize((180,180)))
                cantrans.itemconfig(canplayer, image = NewPlayerpic)
            else:pass
 
        def generation(poste,niveau):
            num_cat = dico_num[f"{poste}"]

            path = os.path.dirname(os.path.abspath(__file__))
            decoder = tf.keras.models.load_model(os.path.join(path,f"models/player_model/Players_CVAE_decoder.h5"))

            level = niveau/100

            hot_cat = tf.tile([tf.one_hot(num_cat,len(dico_num))],[1,1])
            score =  tf.tile([[level]],[1,1])
            code=prior.sample(1)
            player_info = tf.concat([hot_cat,score],-1)
            code = code.numpy()
            player_info = player_info.numpy()
            dist_player = decoder([code, player_info])
            assert isinstance(dist_player, tfd.Distribution)
            player_gen = (100*(dist_player.mean())).numpy().astype('i')
            df_gen = pd.DataFrame(player_gen, columns = columns)
            df_gen[['WF','SM','IR']] = (df_gen[['WF','SM','IR']]*0.05).astype('i').astype(str)
            return(df_gen)

        def add_p_dynam(player_id):
            conn = sqlite3.connect(f'databases/alldata.db')
            c = conn.cursor()
            stats = c.execute('''SELECT PAC,SHO,PAS,DRI,DEF,PHY
                                FROM Players
                                WHERE ID = ?
                                ''',(player_id,))
            PAC,SHO,PAS,DRI,DEF,PHY = 0,0,0,0,0,0
            for row in stats.fetchall():
                PAC,SHO,PAS,DRI,DEF,PHY = row[0],row[1],row[2],row[3],row[4],row[5]
            conn.close()
            player_mean = (PAC+SHO+PAS+DRI+DEF+PHY)//6
            color = levelcolor(player_mean)
            df = pd.DataFrame({'group': ['stats'],'PAC': [PAC],'SHO': [SHO],'PAS': [PAS],'DRI': [DRI],'DEF': [DEF],'PHY': [PHY], })
            categories=list(df)[1:]
            N = len(categories)

            values=df.loc[0].drop('group').values.flatten().tolist()
            values += values[:1]
            angles = [n / float(N) * 2 * pi for n in range(N)]
            angles += angles[:1]
            
            ax = plt.subplot(111, polar=True)
            plt.xticks(angles[:-1], categories, color='white', size=8)
            ax.set_rlabel_position(0)
            plt.yticks([20,40,60,80], ["20","40","60","80"], color="white", size=7)
            plt.ylim(0,100)
            ax.plot(angles, values, linewidth=1, linestyle='solid', color = color)
            ax.fill(angles, values, 'b', alpha=0.1, facecolor = color)
            plt.savefig(plotsavepathspider, transparent=True, dpi=144)
            # plt.show()
            plt.close() 
            global jchart_spi
            jchart_spi = ImageTk.PhotoImage(Image.open(rf"{plotsavepathspider}").resize((700,505)))
            cantrans.itemconfigure(spider, image = jchart_spi)

        def infosget():

            # def add_p_dynam():
            #     conn = sqlite3.connect(f'databases/alldata.db')
            #     c = conn.cursor()
            #     lastrow = c.execute('''SELECT ID 
            #             FROM Players 
            #             ORDER BY ID DESC LIMIT 1;
            #             ''')
            #     stats = c.execute('''SELECT PAC,SHO,PAS,DRI,DEF,PHY
            #                         FROM Players
            #                         ORDER BY ID DESC LIMIT 1;
            #                         ''')

            #     for row in stats.fetchall():
            #         PAC,SHO,PAS,DRI,DEF,PHY = row[0],row[1],row[2],row[3],row[4],row[5]
            #     conn.close()
            #     player_mean = (PAC+SHO+PAS+DRI+DEF+PHY)//6
            #     color = levelcolor(player_mean)
            #     df = pd.DataFrame({'group': ['stats'],'PAC': [PAC],'SHO': [SHO],'PAS': [PAS],'DRI': [DRI],'DEF': [DEF],'PHY': [PHY], })
            #     categories=list(df)[1:]
            #     N = len(categories)

            #     values=df.loc[0].drop('group').values.flatten().tolist()
            #     values += values[:1]
            #     angles = [n / float(N) * 2 * pi for n in range(N)]
            #     angles += angles[:1]
                
            #     ax = plt.subplot(111, polar=True)
            #     plt.xticks(angles[:-1], categories, color='white', size=8)
            #     ax.set_rlabel_position(0)
            #     plt.yticks([20,40,60,80], ["20","40","60","80"], color="white", size=7)
            #     plt.ylim(0,100)
            #     ax.plot(angles, values, linewidth=1, linestyle='solid', color = color)
            #     ax.fill(angles, values, 'b', alpha=0.1, facecolor = color)
            #     plt.savefig(plotsavepathspider, transparent=True, dpi=144)
            #     # plt.show()
            #     plt.close() 
            #     global jchart_spi
            #     jchart_spi = ImageTk.PhotoImage(Image.open(rf"{plotsavepathspider}").resize((700,505)))
            #     cantrans.itemconfigure(spider, image = jchart_spi)
            try:
                picturepath
            except NameError:
                MsgBox = messagebox.askokcancel('PAS DE PHOTO DU JOUEUR',"Attention, vous n'avez pas sélectionné de photo\npour votre joueur. Continuer ?", icon = 'warning', default = 'cancel')#, parent = fenetre)
                if MsgBox == True:
                    imNewPlayer = Image.open("images/icones/player_icone.png").resize((120,120))
                else:
                    return
            else:pass

            newclub = lab_newclub.cget("text")
            try:
                joueur,nationalite,age,poste,taillecm,poids,pied,contrat = Ename.get(),Cpays.get(),int(Eage.get()),comboposit.get(),int(Etaille.get()),int(Epoids.get()),combofoot.get(),int(Econtrat.get())
                niveau = int(Eniveau.get())
            except:
                messagebox.showinfo('Données Incomplètes',"Attention, vous n'avez pas saisi toutes\nles informations concernant votre joueur.", icon = 'warning')#, parent = fenetre)
                return
            if len(comboNewteam.get()) < 1:
                messagebox.showinfo('Pas de club sélectionné',f"{joueur} n'a pas de destination sélectionnée !", icon = 'warning')
            
            df_gen = generation(poste,niveau)
            postes = dico_cat[f'{poste}']
            positions = ''
            for p in postes:
                positions = positions + p + ' '
            
            taillecm = 175
            ft = taillecm//30.48
            feets = int(round(ft,0))
            inches = int(round((taillecm*0.3937) - 12*feets,0))
            
            taille = str(feets)+"'"+str(inches)+'"'
            poidslbs = str(int(round(poids*2.205,0)))+'lbs'  
            
            if pied == 'Droit':
                foot = 'Right'
            else:
                foot = 'Left'
            now = datetime.datetime.now()
            year = now.strftime("%Y")
            month = now.strftime("%B")
            day = now.strftime("%d")
            date = month[:3] + ' ' + day + ', ' + year
            endcontrat = int(year)+contrat
            contract = year + ' ~ ' + str(endcontrat)
            chp = new_chp(newclub)

            conn = sqlite3.connect(f'databases/alldata.db')
            c = conn.cursor()
            lastrow = c.execute('''SELECT ID 
                      FROM Players 
                      ORDER BY ID DESC LIMIT 1;
                      ''')
            last_id = int(lastrow.fetchone()[0])
            newplayer_id = last_id+1
            fictiveinfo = 1
            
            c.execute('''INSERT INTO Players (ID,Club,Name,Age,Nationality,Position,Height,Weight,foot,Joined,Contract,TruePlayer,championnat)
                      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                      ''',(newplayer_id,newclub,joueur,age,nationalite,positions,taille,poidslbs,foot,date,contract,fictiveinfo,chp,))
            conn.commit()
            for col in df_gen.columns:
                value = int(df_gen[col].values[0])
                c.execute(f'''UPDATE Players
                SET {col} = ?
                WHERE ID = ?''',(value,newplayer_id,))
            conn.commit()

            best_post = ''
            if poste == 'Gardien':
                best_post = 'GK'
            else:
                couloir = combo_poste.get()
                if couloir == 'Gauche':
                    best_post = postes[0]
                elif couloir == 'Droit':
                    best_post = postes[-1]
                else:
                    best_post = postes[1]

            ova = c.execute(f'''SELECT {best_post} FROM Players WHERE ID = ? ''',(newplayer_id,))
            player_ova = ova.fetchone()[0]
            c.execute(f'''UPDATE Players
            SET OVA = ?, BP = ?, TITU = ?
            WHERE ID = ?''',(player_ova,best_post,best_post,newplayer_id,))
            conn.commit()

            conn.close()
            
            try:
                imNewPlayer = Image.open(picturepath).resize((120,120))
            except:
                  imNewPlayer = Image.open("images/icones/player_icone.png").resize((120,120))
            
            imNewPlayer = imNewPlayer.save(f"images/players/{newplayer_id}.png")
            MsgBox = messagebox.showinfo('Nouveau Joueur',f"L'espoir {joueur} vient de rejoindre les rangs de {newclub} !", icon = 'warning')#, parent = fenetre)
            for entry in Ename,Eage,Etaille,Epoids,Econtrat,Eniveau:
                entry.deleter()
            Cpays.current(49)
            combofoot.current(0)
            comboposit.current(0)
            add_p_dynam(newplayer_id)
            bigdf = team_evolution(newclub,0)
            bigdf2 = team_evolution(newclub,newplayer_id)
            update_notes(bigdf,bigdf2)

        def set_couloirs(event):
            poste_type = comboposit.get()
            postes_tot = len(dico_cat[f'{poste_type}'])
            if postes_tot == 1:
                combo_poste['values'] = ''
                combo_poste.set('Gardien')
            elif postes_tot == 2:
                combo_poste['values'] = ['Gauche','Droit']
            else:
                combo_poste['values'] = ['Gauche','Central','Droit']
            combo_poste.current(0)



#%%            
        # def player_attribute_update():
        #     joueur = combojtr.get()
        #     if len(joueur) == 0:
        #         MsgBox = messagebox.showinfo('Pas de joueur sélectionné',f"Veuillez choisir un joueur au préalable !", icon = 'warning')
        #         return            
        #     attribut = combo_upd_values.get()
        #     value_attr = int(E_upd_value.get())
        #     if value_attr < 1 or value_attr >100:
        #         return
        #     club = lab_exclub.cget("text")
        #     MsgBox = messagebox.askokcancel('Evolution Joueur',f"{joueur} va changer sa capacité en {attribut} !.\nContinuer ?", icon = 'warning', default = 'ok')#, parent = fenetre)
        #     if MsgBox == True:
        #         conn = sqlite3.connect('databases/alldata.db')
        #         c = conn.cursor()
        #         precommit = c.execute("SELECT ID FROM Players WHERE Name = ? AND Club = ?",(joueur,club,))
        #         player_id = precommit.fetchone()[0]
        #         c.execute(f'''UPDATE Players
        #         SET {attribut} = ?
        #         WHERE ID = ?''',(value_attr,player_id,))
        #         new_value = c.execute("SELECT ? FROM Players WHERE ID = ?",(value_attr,player_id,))
        #         nvattr = new_value.fetchone()[0]
        #         print(attribut,nvattr)


#%%
        fenetre_transfers = Toplevel(fenetremain)
        fenetre_transfers.title("Management")
        fenetre_transfers.geometry('1920x1080')
        fenetre_transfers.iconphoto(True, PhotoImage(file='images/icones/root_icone.png'))
        fenetre_transfers.resizable(0, 0) 
        fenetre_transfers.bind("<F11>", lambda event: fenetre_transfers.attributes("-fullscreen",
                                        not fenetre_transfers.attributes("-fullscreen")))
        fenetre_transfers.bind("<Escape>", lambda event: fenetre_transfers.attributes("-fullscreen", False))
        fenetre_transfers.transient(fenetremain)
        background_image_trans = PhotoImage(file = r"images/backgrounds/transfers.png")
        
        fleche_default = PhotoImage(file = r"images/icones/fleche_blanc.png")
        fleche_vert = PhotoImage(file = r"images/icones/fleche_vert.png")
        fleche_rouge = PhotoImage(file = r"images/icones/fleche_rouge.png")
        
        cantrans= Canvas(fenetre_transfers, width = 1920, height = 1080)
        cantrans.pack()
        cantrans.create_image(0,0, image = background_image_trans, anchor = tk.NW)

        spider = cantrans.create_image(595,530, anchor = tk.NW)
        
        #datateams
        labTitus = Label(fenetre_transfers,text = "Titulaires",font = (main_menu_font,26), bg = '#2B0C47', fg = 'white',justify='center')
        labTitus.place(x = 1520, y=225)

        lab_spid = Label(fenetre_transfers,text = "Profil du Joueur",font = (main_menu_font,22), bg = '#2B0C47', fg = 'white',justify='center')
        lab_spid.place(x = 850, y=520)
        
        x,y = 1520,225
        addy = 65
        
        labatt = Label(fenetre_transfers,text = 'ATT',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labatt.place(x = x-190, y = y+addy)
        labTitusatt = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labTitusatt.place(x = x-100, y = y+addy)
        flechetitatt = Label(fenetre_transfers,image = fleche_default, bg = '#2B0C47')
        flechetitatt.place(x = x+30, y = y+addy)
        
        labmil = Label(fenetre_transfers,text = 'MIL',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labmil.place(x = x-190, y = y+addy*2)
        labTitusmil = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labTitusmil.place(x = x-100, y = y+addy*2)
        flechetitmil = Label(fenetre_transfers,image = fleche_default, bg = '#2B0C47')
        flechetitmil.place(x = x+30, y = y+addy*2)
        
        labdef = Label(fenetre_transfers,text = 'DEF',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labdef.place(x = x-190, y = y+addy*3)
        labTitusdef = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labTitusdef.place(x = x-100, y = y+addy*3)
        flechetitdef = Label(fenetre_transfers,image = fleche_default, bg = '#2B0C47')
        flechetitdef.place(x = x+30, y = y+addy*3)
        
        labgar = Label(fenetre_transfers,text = 'GAR',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labgar.place(x = x-190, y = y+addy*4)
        labTitusgar = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labTitusgar.place(x = x-100, y = y+addy*4)
        flechetitgar = Label(fenetre_transfers,image = fleche_default, bg = '#2B0C47')
        flechetitgar.place(x = x+30, y = y+addy*4)
        
        y+=30
        labSubs = Label(fenetre_transfers,text = "Remplaçants",font = (main_menu_font, 26), bg = '#2B0C47', fg = 'white', justify = 'center')
        labSubs.place(x = x-30, y = y+addy*5)
        y+=15
        labatt2 = Label(fenetre_transfers,text = 'ATT',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labatt2.place(x = x-190, y = y+addy*6)
        labSubsatt = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labSubsatt.place(x = x-100, y = y+addy*6)
        
        labmil2 = Label(fenetre_transfers,text = 'MIL',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labmil2.place(x = x-190, y = y+addy*7)
        labSubsmil = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labSubsmil.place(x = x-100, y = y+addy*7)
        
        labdef2 = Label(fenetre_transfers,text = 'DEF',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labdef2.place(x = x-190, y = y+addy*8)
        labSubsdef = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labSubsdef.place(x = x-100, y = y+addy*8)
        
        labgar2 = Label(fenetre_transfers,text = 'GAR',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labgar2.place(x = x-190, y = y+addy*9)
        labSubsgar = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        labSubsgar.place(x = x-100, y = y+addy*9)
        
        
        y = 225
        
        lab2Titusatt = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        lab2Titusatt.place(x = x+200, y = y+addy)
        
        lab2Titusmil = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        lab2Titusmil.place(x = x+200, y = y+addy*2)
        
        lab2Titusdef = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        lab2Titusdef.place(x = x+200, y = y+addy*3)
        
        lab2Titusgar = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        lab2Titusgar.place(x = x+200, y = y+addy*4)
        
        y+= addy+45
        lab2Subsatt = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        lab2Subsatt.place(x = x+200, y = y+addy*5)

        flechesubatt = Label(fenetre_transfers,image = fleche_default, bg = '#2B0C47')
        flechesubatt.place(x = x+30, y = y+addy*5)
        
        lab2Subsmil = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        lab2Subsmil.place(x = x+200, y = y+addy*6)

        flechesubmil = Label(fenetre_transfers,image = fleche_default, bg = '#2B0C47')
        flechesubmil.place(x = x+30, y = y+addy*6)
        
        lab2Subsdef = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        lab2Subsdef.place(x = x+200, y = y+addy*7)
        
        flechesubdef = Label(fenetre_transfers,image = fleche_default, bg = '#2B0C47')
        flechesubdef.place(x = x+30, y = y+addy*7)
        
        lab2Subsgar = Label(fenetre_transfers,text = '',font = (main_menu_font,22), bg = '#2B0C47', fg = 'white')
        lab2Subsgar.place(x = x+200, y = y+addy*8)
        
        flechesubgar = Label(fenetre_transfers,image = fleche_default, bg = '#2B0C47')
        flechesubgar.place(x = x+30, y = y+addy*8)

        x,y = 950,303
        cantrans.create_rectangle(x-103,303-103,x+103,303+103, fill = 'white')
        canblason = cantrans.create_image(x,y)
        canplayer = cantrans.create_image(x,y+10)

        lab_newclub = Label(fenetre_transfers)
        lab_exclub = Label(fenetre_transfers)

        Btransfer = hover_button(fenetre_transfers,command = newtransfer, height = 3, width = 35, text = "Manager un Joueur",font = main_menu_font,  bg ='#5DFEE6',activebackground='#2B0C47', fg = '#1E1A1A', activeforeground='snow')
        Btransfer.place(x=960-370,y=70)
        
        Baddplayer = hover_button(fenetre_transfers,command = addnewplayer, height = 3, width = 35, text = "Ajouter un Joueur", font = main_menu_font,  bg ='#5DFEE6',activebackground='#2B0C47', fg = '#1E1A1A', activeforeground='snow',state = tk.DISABLED)
        Baddplayer.place(x=960,y=70)
        

        
        
        xlab,ylab = 100,200
        widthlab,bd = 20,8
        fg,bg = 'white','#37115D'
        
        labNewteam = Label(fenetre_transfers, text ="Futur Club", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labNewteam.place(x=xlab,y=ylab)
        
        #Transfer Player
        laboldteam = Label(fenetre_transfers, text = "Club Actuel",justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labtrjoueur = Label(fenetre_transfers, text = "Joueur Managé",justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        # lab_upd_values = Label(fenetre_transfers, text = "Modifier Valeur",justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        

        #Nouveau Joueur        
        labname = Label(fenetre_transfers, text ="Nom du Joueur", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labname.place(x=xlab,y=ylab+50)
        
        labcountry = Label(fenetre_transfers, text ="Nationalité du Joueur", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labcountry.place(x=xlab,y=ylab+100)
        
        labage = Label(fenetre_transfers, text ="Age du Joueur", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labage.place(x=xlab,y=ylab+150)
        
        labposit = Label(fenetre_transfers, text ="Poste du Joueur", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labposit.place(x=xlab,y=ylab+200)
        
        lab_couloir = Label(fenetre_transfers, text ="Couloir Préférentiel", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        lab_couloir.place(x=xlab,y=ylab+250)

        labtaille = Label(fenetre_transfers, text ="Taille du Joueur (cm)", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labtaille.place(x=xlab,y=ylab+300)
        
        labpoids = Label(fenetre_transfers, text ="Poids du Joueur (kg)", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labpoids.place(x=xlab,y=ylab+350)
        
        labfoot = Label(fenetre_transfers, text ="Pied Fort", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labfoot.place(x=xlab,y=ylab+400)
        
        labcontrat = Label(fenetre_transfers, text ="Durée Contrat (Années)", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labcontrat.place(x=xlab,y=ylab+450)

        labniveau = Label(fenetre_transfers, text ="Niveau du Joueur", justify = 'center', width = widthlab, bd = bd, font = main_menu_font, fg = fg, bg = bg)
        labniveau.place(x=xlab,y=ylab+500)
    
        x,y = 350,200
        width = 30
        bd = 8

        
        comboNewteam = AutocompleteCombobox(fenetre_transfers,justify='center', update_form = rootdynam)
        comboNewteam.configure(width = 30)
        comboNewteam.set_completion_list(Teams)
        comboNewteam.bind("<<ComboboxSelected>>",rootdynam)
        comboNewteam.place(x=x, y=y+8)


        # Transferts
        comboOldteam = AutocompleteCombobox(fenetre_transfers,justify='center', update_form = updatecombojoueurs)
        comboOldteam.configure(width = 30)
        comboOldteam.set_completion_list(Teams)
        comboOldteam.bind("<<ComboboxSelected>>",updatecombojoueurs)
        
        combojtr = ttk.Combobox(fenetre_transfers, width = 60, justify='center',state = "disabled")
        combojtr.configure(width = 30)
        combojtr.bind("<<ComboboxSelected>>",set_image_transfer)
        
        Bcommittransfer = hover_button(fenetre_transfers,command = committransfer, height = 3, width = 35, text = "Effectuer Transfert",bg ='#5DFEE6',activebackground="#E8FFFF", activeforeground = "blue",font = main_menu_font)
        
        # combo_upd_values = ttk.Combobox(fenetre_transfers, values = columns, width = width,justify='center', state = 'readonly')
        # combo_upd_values.current(0)
        
        # E_upd_value = cursor_entry_int(fenetre_transfers, width = width,justify='center', bd = bd, default_text='Nouvelle Valeur')
        
        # Bcommit_value = Button(fenetre_transfers,command = player_attribute_update, height = 3, width = 35, text = "Modifier Attribut")

        # Nouveau Joueur
        
        Ename = cursor_entry_str(fenetre_transfers, width = width,justify='center', bd = bd, default_text = 'Nom du Joueur')
        Ename.place(x=x,y=y+50)
        
        Cpays = ttk.Combobox(fenetre_transfers, values = lnationalities, width = width,justify='center', state = 'readonly')
        Cpays.current(49)
        Cpays.place(x=x,y=y+105)

        Eage = cursor_entry_int(fenetre_transfers, width = width,justify='center', bd = bd, default_text='Age du Joueur (15 à 41)',minvalue = 15, maxvalue = 41)
        Eage.place(x=x,y=y+150)
        
        comboposit = ttk.Combobox(fenetre_transfers, values = list(dico_num.keys()), width = width,justify='center', state = 'readonly')
        comboposit.current(0)
        comboposit.bind("<<ComboboxSelected>>",set_couloirs)
        comboposit.place(x=x,y=y+208)

        combo_poste = ttk.Combobox(fenetre_transfers,values = ['Gauche','Central','Droit'],justify='center',state = 'readonly',width = width)
        combo_poste.current(0)
        combo_poste.place(x=x,y=y+258)

        Etaille = cursor_entry_int(fenetre_transfers, width = width,justify='center', bd = bd,default_text ='Taille (150 à 210)',minvalue = 150, maxvalue = 210)
        Etaille.place(x=x,y=y+300)

        Epoids = cursor_entry_int(fenetre_transfers, width = width,justify='center', bd = bd,default_text ='Poids (50 à 110)',minvalue = 50, maxvalue = 110)
        Epoids.place(x=x,y=y+350)
        
        combofoot = ttk.Combobox(fenetre_transfers, values = ['Droit','Gauche'], width = width,justify='center', state = 'readonly')
        combofoot.current(0)
        combofoot.place(x=x,y=y+408)
        
        Econtrat = cursor_entry_int(fenetre_transfers, width = width,justify='center', bd = bd,default_text ='Durée Contrat (1 à 7)',minvalue = 1, maxvalue = 7)
        Econtrat.place(x=x,y=y+450)
        
        Eniveau = cursor_entry_int(fenetre_transfers, width = width,justify='center', bd = bd,default_text ='Note (1 à 100)',minvalue = 1, maxvalue = 100)
        Eniveau.place(x=x,y=y+500)
                
        Bphoto = hover_button(fenetre_transfers, width =27, height =3,text = "Ajouter Photo", command = pictdl,bg ='#5DFEE6',activebackground="#E8FFFF", activeforeground = "blue")
        Bphoto.place(x=x,y = y+575)


        Bdata = hover_button(fenetre_transfers, width =27, height =3,text = "Générer Joueur", command = infosget,bg ='#5DFEE6',activebackground="#E8FFFF", activeforeground = "blue",font = main_menu_font)
        Bdata.place(x=x-150,y=y+650)

        fenetre_transfers.protocol("WM_DELETE_WINDOW", lambda:(fenetre_transfers.destroy()))
        fenetre_transfers.mainloop()

        