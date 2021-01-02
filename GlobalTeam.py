# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 17:24:14 2020

@author: benja
"""

import sqlite3
import tkinter as tk
from tkinter import Toplevel, Canvas, PhotoImage, Button,Label,messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk
from rankings import focus_ranking,dicfixtures

import pandas as pd

from math import pi
import matplotlib.pyplot as plt

from resultspdf import results_season
from definitions import levelcolor,testpost,testsubposte,prepair_global_team

from fuzzywuzzy import fuzz
import os
import tensorflow as tf
from learning import build_match_features
import pygame

def team_global(team,fenetremain,imEcusson,selected_players,main_menu_font,dic_clubs_id,blason_path):
    
    def pronoGUI(team,chp):
        fixtures,nbmatchs = dicfixtures(team,chp)
        Team1 = fixtures[f'{len(fixtures)}'][2]
        Team2 = fixtures[f'{len(fixtures)}'][3]

        if Team1 != Team2:
            # if selected_model != str('') :
            #     # print('pas de modele selectionne')
            path = os.path.dirname(os.path.abspath(__file__))
            model = tf.keras.models.load_model(os.path.join(path,f"models/prediction/all_model.h5"))
            # model.summary()
            probability_model = tf.keras.Sequential([model, 
                                                        tf.keras.layers.Softmax()])
            one_input = build_match_features(chp,Team1,Team2).values
            one_prediction = probability_model.predict(one_input)
            prediction = one_prediction[0]
            
            HP = prediction[0]*100
            DP = prediction[1]*100
            AP = prediction[2]*100
            
            betadvice = ''
            if AP > 38 or HP+DP<=60:
                betadvice = f'Victoire {Team2}'
            elif HP >= 45 or AP+DP <= 60 :
                betadvice = f'Victoire {Team1}'
            elif HP-AP <= 5 or AP-HP<=5:
                if AP - HP > 3:
                    betadvice = f'{Team2} ou Nul'
                elif HP - AP <= 3:
                    betadvice = 'Match Nul'
                else:
                    betadvice = f'{Team1} ou Nul'
                    
            
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("Sounds/referee whistle.wav"))
            titre = ("Pronostic de : " + Team1 + " vs " + Team2)
            fenetre_prono = Toplevel(fenetre_stats)
            fenetre_prono.title(titre)
            # fenetre_prono.iconphoto(False, PhotoImage(file='Images/icones/icone.png'))
            fenetre_prono.resizable(0, 0)
            prono_bg = PhotoImage(file = r'images/backgrounds/Football_pitch.png')
            prono_cadran = PhotoImage(file = r"images/backgrounds/pronoBG.png")
            
            can = Canvas(fenetre_prono, width=1280,height=877)
            can.pack()
            can.create_image(0, 0, image = prono_bg, anchor = tk.NW)


            can.create_image(105,100, image = l_fixt[0])

            can.create_image(1175,100, image = l_fixt[1])
 
            can.create_image(630, 430, image = prono_cadran)
                                  #x0,   y0,   x1, y1
            can.create_rectangle(400, 600, 440, 600 - HP*6, fill = '#99CC00')
            can.create_text(420,620, text = f"{HP:.2f}%")
            
            can.create_rectangle(620, 600, 660, 600 - DP*6, fill = '#FF9900')
            can.create_text(640,620, text = f"{DP:.2f}%")
            
            can.create_rectangle(840, 600, 880, 600 - AP*6, fill = '#FF3800')
            can.create_text(860,620, text = f"{AP:.2f}%")
            
            can.create_text(630,250,text= 'Résultat le plus probable :', fill = 'snow',font = ("Purisa", 24))
            can.create_text(630,300,text= betadvice, fill = 'blue',font = ("Purisa", 36, 'bold'))
            
            fenetre_prono.mainloop()
        else:
            err = messagebox.showerror("Selections Invalides","L'une des deux équipes (ou les 2) n'ont pas joué suffisament de matchs.")
            return
                
    def sort_player(poste):
        if poste == 'Attaquant':
            attaquants.append(infojoueur)
        elif poste == 'Milieu':
            milieux.append(infojoueur)
        elif poste == 'Défenseur':
            défenseurs.append(infojoueur)
        else:
            gardiens.append(infojoueur)                

    l_fixt = []
    l_ecu = []
    
    def find_ecu(club_name,size,liste):
        pre_list = []
        if club_name == 'Spal':
            liste.append(ImageTk.PhotoImage(Image.open(rf"images/ecussons/112791.png").resize((size,size))))
        elif club_name == 'Los Angeles Galaxy':
            liste.append(ImageTk.PhotoImage(Image.open(rf"images/ecussons/697.png").resize((size,size))))
        elif club_name == 'Ath Madrid':
            liste.append(ImageTk.PhotoImage(Image.open(rf"images/ecussons/240.png").resize((size,size))))
        elif club_name == 'Ath Bilbao':
            liste.append(ImageTk.PhotoImage(Image.open(rf"images/ecussons/448.png").resize((size,size))))
        elif club_name == 'FC Steaua Bucuresti':
            liste.append(ImageTk.PhotoImage(Image.open(rf"images/ecussons/100761.png").resize((size,size))))
        elif club_name == 'FC Copenhagen':
            liste.append(ImageTk.PhotoImage(Image.open(rf"images/ecussons/819.png").resize((size,size))))
        elif club_name == 'Sp Lisbon':
            liste.append(ImageTk.PhotoImage(Image.open(rf"images/ecussons/237.png").resize((size,size))))
        elif club_name == 'Milan':
            liste.append(ImageTk.PhotoImage(Image.open(rf"images/ecussons/47.png").resize((size,size))))
        
        else:
            for clubs in lteams: 
                best = fuzz.partial_ratio(club_name,clubs)
                pre_list.append([clubs,best])
                
            tmplist = sorted(pre_list, key = lambda x: (int(x[1])),reverse = True)
            if tmplist[0][1] > 70:
                club = tmplist[0][0]
                club_idx = dic_clubs_id[f'{club}']
                liste.append(ImageTk.PhotoImage(Image.open(rf"images/ecussons/{club_idx}.png").resize((size,size))))
            else:
                liste.append(ImageTk.PhotoImage(Image.open(rf"images/icones/ecusson_default.png").resize((size,size))))
        
            
    def pre_donut(Liste,colorletter):
        m = 0.5
        for typesub in Liste:
           if dictlensubp[f'{typesub}']>0:
                subgroup_names.append(f'{typesub}')
                subgroup_size.append(dictlensubp[f'{typesub}'])
                colors.append(colorletter(m))
                m -= 0.1

    def next_matchday():
        actual_matchday = int(lab_mselect.cget('text'))
        if actual_matchday == 1:
            PrevMatch.place(x =570,y =305)
        if actual_matchday>nbmatchs:
            pronoGUI(team,chp)
            return
        elif actual_matchday==nbmatchs :
            if len(fixtures)>nbmatchs:
                actual_matchday += 1
                lab_mselect['text'] = str(actual_matchday)
                NextMatch['image'] = predicbut
            else:
                return
            
        elif actual_matchday<nbmatchs:
            actual_matchday += +1
            lab_mselect['text'] = str(actual_matchday)
        
        disp_fixture(team,actual_matchday)
        


    def prev_matchday():
        actual_matchday = int(lab_mselect.cget('text'))
        NextMatch['image'] = nextbut

        if actual_matchday == 1 :
            return
        else :
            actual_matchday -= 1
            if actual_matchday == 1:
                PrevMatch.place_forget()
        disp_fixture(team,actual_matchday)
        lab_mselect['text'] = str(actual_matchday)
    
    def disp_fixture(team,match_select):
        def disp_nfixture(team):
            Team1 = fixtures[f'{len(fixtures)}'][2]
            Team2 = fixtures[f'{len(fixtures)}'][3]
            can.create_text(x+225,y-85, width = 550,text = f'Journée {match_select}', font = main_menu_font, fill = 'white', tags = 'fixture')
            HeureGMT = fixtures[f'{len(fixtures)}'][1]
            for team in Team1,Team2:
                find_ecu(team,145,l_fixt)
                
            
            try:
                can.create_image(x,y, image = l_fixt[0], tags = 'fixture')
                can.create_image(x+450,y, image = l_fixt[1], tags = 'fixture')
                can.create_text(x,y+90, width = 550,text = Team1, font = main_menu_font, fill = 'white', tags = 'fixture')
                can.create_text(x+450,y+90, width = 550,text = Team2, font = main_menu_font, fill = 'white', tags = 'fixture')
            except:
                can.create_text(x,y, width = 550,text = Team1, font = dis_fixture_font, fill = 'white', tags = 'fixture')
                can.create_text(x+450,y, width = 550,text = Team2, font = dis_fixture_font, fill = 'white', tags = 'fixture')
            can.create_text(x+235,y+20, width = 550,text = 'VS', font = (dis_fixture_font,30), fill = 'white', tags = 'fixture')
            can.create_text(x+225,y+110, width = 550,text = fixtures[f'{len(fixtures)}'][0], font = dis_fixture_font, fill = 'white', tags = 'fixture')
            can.create_text(x+225,y+150, width = 550,text = HeureGMT, font = main_menu_font, fill = 'white', tags = 'fixture')
    
    
        def selected_fixtures(team,i):
            Team1 = fixtures[f'{i}'][2]
            Team2 = fixtures[f'{i}'][3]
            can.create_text(x+225,y-85, width = 550,text = f'Journée {match_select}', font = main_menu_font, fill = 'white', tags = 'fixture')
            HeureGMT = fixtures[f'{i}'][1]
            for team in Team1,Team2:
                find_ecu(team,145,l_fixt)
            try:
                can.create_image(x,y, image = l_fixt[0], tags = 'fixture')
                can.create_image(x+450,y, image = l_fixt[1], tags = 'fixture')
                can.create_text(x,y+90, width = 550,text = Team1, font = main_menu_font, fill = 'white', tags = 'fixture')
                can.create_text(x+450,y+90, width = 550,text = Team2, font = main_menu_font, fill = 'white', tags = 'fixture')
            except:
                can.create_text(x,y, width = 550,text = Team1, font = dis_fixture_font, fill = 'white', tags = 'fixture')
                can.create_text(x+450,y, width = 550,text = Team2, font = dis_fixture_font, fill = 'white', tags = 'fixture')
            can.create_text(x+185,y+20, width = 550,text = int(fixtures[f'{i}'][4]), font = (dis_fixture_font,30), fill = 'white', tags = 'fixture')
            can.create_text(x+235,y+20, width = 550,text = '-', font = (dis_fixture_font,30), fill = 'white', tags = 'fixture')
            can.create_text(x+285,y+20, width = 550,text = int(fixtures[f'{i}'][5]), font = (dis_fixture_font,30), fill = 'white', tags = 'fixture')
            can.create_text(x+225,y+110, width = 550,text = fixtures[f'{i}'][0], font = (dis_fixture_font,20), fill = 'white', tags = 'fixture')
            can.create_text(x+225,y+150, width = 550,text = HeureGMT, font = main_menu_font, fill = 'white', tags = 'fixture')        
        x = 725
        y = 200

        fixtures,nbmatchs = dicfixtures(team,chp)
        can.delete('fixture')
        l_fixt.clear()

        if match_select>nbmatchs:
            disp_nfixture(team)
        else:
            selected_fixtures(team,match_select)
        

    dictpostes = {'Attaquant':(['LS','ST','RS','LW','LF','CF','RF','RW']),'Milieu':(['LAM','CAM','RAM','LM','LCM','CM','RCM','RM','LDM','CDM','RDM']),
                  'Défenseur' : (['LWB','RWB','LB','LCB','CB','RCB','RB']),'Gardien':(['GK']),'Remplaçant':(['SUB']),'Réserviste':(['RES'])}
    dictlenpostes = {'LS':0,'ST':0,'RS':0,'LW':0,'LF':0,'CF':0,'RF':0,'RW':0,'LAM':0,'CAM':0,'RAM':0,'LM':0,'LCM':0,'CM':0,'RCM':0,'RM':0,'LDM':0,'CDM':0,'RDM':0,
                     'LWB':0,'RWB':0,'LB':0,'LCB':0,'CB':0,'RCB':0,'RB':0,'GK':0}
    dictsubpost = {'Buteurs' : (['LS','ST','RS']),'Ailiers':(['LW','RW']), 'Forwards':(['LF','CF','RF']), 'Off.' : (['LAM','CAM','RAM']),
                   'Equi.':(['LM','LCM','CM','RCM','RM']),'Déf.':(['LDM','CDM','RDM']),'Latéraux':(['LWB','RWB','LB','RB']),'Centraux':(['LCB','CB','RCB']),' ':(['GK'])}
    dictlensubp = {'Buteurs':0,'Ailiers':0,'Forwards':0,'Off.':0,'Equi.':0,'Déf.':0,'Latéraux':0,'Centraux':0,' ':0}
    
    attaquants,milieux,défenseurs,gardiens = [],[],[],[]

    chp = ''
    conn = sqlite3.connect(f'databases/alldata.db')
    c = conn.cursor()
    joueurs = c.execute(f"SELECT ID,Name,OVA,POT,TITU,BP,championnat FROM Players WHERE Club = ? AND TITU IS NOT NULL {selected_players}",(team,))
    
    try:
        for j in joueurs.fetchall():
            nom = j[1]
            note = j[2]
            potentiel = j[3] - note
            infojoueur = [nom,note,potentiel]
            titu = j[4]
            chp = j[6]
            if titu == 'SUB' or titu == 'RES':
                bpost = j[5]
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
    conn.close()
    
    global_team = prepair_global_team(attaquants,milieux,défenseurs,gardiens)

    # Datas et couleurs
    nba,nbm,nbd,nbg = len(attaquants),len(milieux),len(défenseurs),len(gardiens)
    nbtot = nba+nbm+nbd+nbg
 
    group_names=[f'Attaquants\n{nba*100//nbtot} %', f'Milieux\n{nbm*100//nbtot} %', f'Défenseurs\n{nbd*100//nbtot} %',f'Gardiens\n{nbg*100//nbtot} %']
    group_size=[nba,nbm,nbd,nbg]
    
    subgroup_names = []
    subgroup_size = []
    colors = []
    
    a, b, c, d =[plt.cm.Reds,plt.cm.Oranges,plt.cm.Greens,plt.cm.Blues]
                
    pre_donut(['Buteurs','Ailiers','Forwards'],a)
    pre_donut(['Off.','Equi.','Déf.'],b)
    pre_donut(['Latéraux','Centraux'],c)

    subgroup_names.append(' ')
    subgroup_size.append(dictlensubp[' '])
    colors.append(d(0.0))

    # Premier Donut (extérieur)
    fig, ax = plt.subplots()
    ax.axis('equal')
    mypie, texts = ax.pie(group_size, labels=group_names, labeldistance=1.2,radius=1.3, colors = [a(0.7), b(0.7), c(0.7), d(0.6)])
    for t in texts:
        t.set_horizontalalignment('center')
        t.font = ("helvetica",12)
        t.set_color('white')

    #Ajout cercle blanc
    plt.setp(mypie, width=0.3, edgecolor='white')
     
    # Second Donut (intérieur)
    mypie2, _ = ax.pie(subgroup_size, radius=1.3-0.3, labels=subgroup_names, labeldistance=0.7, colors=colors)
    #Ajout cercle blanc
    plt.setp(mypie2, width=0.4, edgecolor='white')
    plt.margins(0,0)
    ax.set_title('Répartition Effectif', color = 'white',fontsize = 14, pad=24)
    
    plotsavepatheffectif = f"temp/effectif_{team}.png"
    plt.savefig(plotsavepatheffectif, transparent=True, dpi=224)


    for squad in global_team:    
        dicdata = {'group': ['Notes','Potentiel']}
        somme = 0

            
        if squad[0][0] != 0:
            dicdata['ATT'] = squad[0][0], squad[0][0]+squad[0][1]
            somme = somme + squad[0][0]
        if squad[1][0] != 0:
            dicdata['MIL'] = squad[1][0], squad[1][0]+squad[1][1]
            somme = somme + squad[1][0]
        if squad[3][0] != 0:
            dicdata['GAR'] = squad[3][0], squad[3][0]+squad[3][1]
            somme = somme + squad[3][0]
        if squad[2][0] != 0:
            dicdata['DEF'] = squad[2][0], squad[2][0]+squad[2][1]
            somme = somme + squad[2][0]

        df = pd.DataFrame(dicdata)

        if len(dicdata)>3:
            squadmean = somme//(len(dicdata)-1)
            color = levelcolor(squadmean)
            categories=list(df)[1:]
            N = len(categories)
             
            # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
            angles = [n / float(N) * 2 * pi for n in range(N)]
            angles += angles[:1]
            # Initialise the spider plot
            ax = plt.subplot(111, polar=True)
            # If you want the first axis to be on top:
            ax.set_theta_offset(pi / 2)
            ax.set_theta_direction(-1)
            # Draw one axe per variable + add labels labels yet
            plt.xticks(angles[:-1], categories, color = 'white', size = 8)
            # Ylabels
            ax.set_rlabel_position(0)
            plt.yticks([20,40,60,80], ["20","40","60","80"], color='white', size=7)
            plt.ylim(0,100)

            # Ind1
            values=df.loc[0].drop('group').values.flatten().tolist()
            values += values[:1]
            ax.plot(angles, values, linewidth=1, linestyle='solid', color = color, label='Niveau Actuel')
            ax.fill(angles, values, alpha=0.25, facecolor=color)
             
            # Ind2
            values=df.loc[1].drop('group').values.flatten().tolist()
            values += values[:1]
            ax.plot(angles, values, linewidth=1, linestyle='dashed', color = 'grey', label="Marge de Progression")
            ax.fill(angles, values, facecolor = None,alpha=0)
             
            # Add legend
            ax.set_title(squad[-1], color = 'white')
            plt.legend(loc='upper right', bbox_to_anchor=(0.395, 0.011))

            
            plotsavepathspider = f"temp/{team}_{squad[-1]}.png"
            plt.savefig(plotsavepathspider, transparent=True, dpi=224)
            # plt.show()
            plt.close()
            
    
    # print(team,chp)
    data = focus_ranking(team,chp)
    
    lteams = []
    conn = sqlite3.connect(f'databases/alldata.db')
    c = conn.cursor()
    clubs = c.execute(f"SELECT Club FROM Players WHERE championnat = ? AND TITU IS NOT NULL",(chp,))
    for c in clubs.fetchall():
        locequipe = c[0]
        if locequipe not in lteams:
            lteams.append(locequipe)
    conn.close()
    lteams = sorted(lteams,reverse = False)
    
    # 
    
    ###
    
    fenetre_stats = Toplevel(fenetremain)
    fenetre_stats.title(f"Statistiques de {team}")
    fenetre_stats.iconphoto(True, PhotoImage(file='images/icones/root_icone.png'))
    width = 1920
    height = 1080
    fenetre_stats.geometry(f'{width}x{height}+0+0')
    fenetre_stats.minsize(width//2, height//2)
    fenetre_stats.resizable(0, 0)
    fenetre_stats.bind("<F11>", lambda event: fenetre_stats.attributes("-fullscreen",
                                    not fenetre_stats.attributes("-fullscreen")))
    fenetre_stats.bind("<Escape>", lambda event: fenetre_stats.attributes("-fullscreen", False))
        
    
    background_image = PhotoImage(file = r"images/backgrounds/pitch.png")

    can = Canvas(fenetre_stats, width= width,height=height)
    can.pack()
    can.create_image(0, 0, image = background_image, anchor = tk.NW)
    can.create_image(160,220, image = imEcusson)
    
    effectifchart = ImageTk.PhotoImage(Image.open(rf"{plotsavepatheffectif}").resize((720,520)))
    can.create_image(width-330,730, image = effectifchart)

    # teamAchart = ImageTk.PhotoImage(Image.open(rf"temp/{team}_Equipe Type.png").resize((784,522)))
    # can.create_image(width*(1/3)-330,775, image = teamAchart)
    # teamBchart = ImageTk.PhotoImage(Image.open(rf"temp/{team}_Equipe Remplaçants.png").resize((784,522)))
    # can.create_image(width*(2/3)-330,775, image = teamBchart)
    try:
        teamAchart = ImageTk.PhotoImage(Image.open(rf"temp/{team}_Equipe Type.png").resize((784,580)))
        can.create_image(width*(1/3)-330,730, image = teamAchart)
    except:pass
    try:
        teamBchart = ImageTk.PhotoImage(Image.open(rf"temp/{team}_Equipe Remplaçants.png").resize((784,580)))
        # teamCchart = ImageTk.PhotoImage(Image.open(rf"temp/{team}_Equipe Réserve.png").resize((784,522)))
    except:pass
    try:
        can.create_image(width*(2/3)-330,730, image = teamBchart)
        # can.create_image(width-330,775, image = teamCchart)
    except:pass
   
    dis_fixture_font = tkFont.Font(family='Helvetica', size=24, weight=tkFont.BOLD)
    

    x = 1480
    y = 105
    can.create_rectangle(x-80,130,x+385,170,fill ='#6A21B4')
    can.create_rectangle(x-80,128+90,x+385,170+90,fill ='#6A21B4')
    can.create_rectangle(x-80,128+180,x+385,170+180,fill ='#6A21B4')
    can.create_text(x-30,y, width = 550,text = 'P', font = main_menu_font, fill = 'white', tags = 'data', anchor = tk.W)
    can.create_text(x,y, width = 550,text = 'Equipe', font = main_menu_font, fill = 'white', tags = 'data', anchor = tk.W)
    can.create_text(x+150,y, width = 550,text = 'Pts', font = main_menu_font, fill = 'white', tags = 'data')
    can.create_text(x+180,y, width = 550,text = 'J', font = main_menu_font, fill = 'white', tags = 'data')
    can.create_text(x+210,y, width = 550,text = 'V', font = main_menu_font, fill = 'white', tags = 'data')
    can.create_text(x+240,y, width = 550,text = 'N', font = main_menu_font, fill = 'white', tags = 'data')
    can.create_text(x+270,y, width = 550,text = 'D', font = main_menu_font, fill = 'white', tags = 'data')
    can.create_text(x+300,y, width = 550,text = 'BP', font = main_menu_font, fill = 'white', tags = 'data')
    can.create_text(x+330,y, width = 550,text = 'BC', font = main_menu_font, fill = 'white', tags = 'data')
    can.create_text(x+360,y, width = 550,text = '+/-', font = main_menu_font, fill = 'white', tags = 'data')

    for t in data:
        find_ecu(t[0],31,l_ecu)

    y = 150
    i = 0

    for d in range(len(data)):
        try:
            ecurank = l_ecu[i]
        except:
            ecurank = ImageTk.PhotoImage(Image.open(rf"images/icones/ecusson_default.png").resize((31,31)))
            
        can.create_image(x-55,y, image = ecurank)
        can.create_text(x-30,y, width = 550,text = f'{data[d][9]}', font = main_menu_font, fill = 'white', tags = 'data', anchor = tk.W)
        cname = data[d][0][:13] + (data[d][0][13:] and '..')
        can.create_text(x,y, width = 550,text = f'{cname}', font = main_menu_font, fill = 'white', tags = 'data', anchor = tk.W)
        can.create_text(x+150,y, width = 550,text = f'{data[d][1]}', font = main_menu_font, fill = 'white', tags = 'data')
        can.create_text(x+180,y, width = 550,text = f'{data[d][2]}', font = main_menu_font, fill = 'white', tags = 'data')
        can.create_text(x+210,y, width = 550,text = f'{data[d][3]}', font = main_menu_font, fill = 'white', tags = 'data')
        can.create_text(x+240,y, width = 550,text = f'{data[d][4]}', font = main_menu_font, fill = 'white', tags = 'data')
        can.create_text(x+270,y, width = 550,text = f'{data[d][5]}', font = main_menu_font, fill = 'white', tags = 'data')
        can.create_text(x+300,y, width = 550,text = f'{data[d][6]}', font = main_menu_font, fill = 'white', tags = 'data')
        can.create_text(x+330,y, width = 550,text = f'{data[d][7]}', font = main_menu_font, fill = 'white', tags = 'data')
        can.create_text(x+360,y, width = 550,text = f'{data[d][8]}', font = main_menu_font, fill = 'white', tags = 'data')
        i +=1
        y += 45
    
    fixtures,nbmatchs = dicfixtures(team,chp)
    
    lab_mselect = Label(fenetre_stats, text = str(nbmatchs))
        
    # lab_nbmatch = Label(fenetre_stats, text = str(nbmatchs))
    disp_fixture(team,nbmatchs)
    
    nextbut = PhotoImage(file = r'images/icones/nbutton.png')
    prevbut = PhotoImage(file = r'images/icones/pbutton.png')
    predicbut = PhotoImage(file = r'images/icones/sifflet.png')
    
    season_stats = ImageTk.PhotoImage(Image.open(r'images/icones/contrat_default.png').resize((110,110)))
    
    x=725
    y=185
    NextMatch = Button(fenetre_stats, text = 'Match Suivant',command = next_matchday, image = nextbut, relief = tk.FLAT, bg = "#2B0C47", activebackground = "#2B0C47")
    NextMatch.place(x = x+425, y =y+120)
    PrevMatch = Button(fenetre_stats, text = 'Match Précédent',command = prev_matchday, image = prevbut, relief = tk.FLAT, bg = "#2B0C47", activebackground = "#2B0C47")
    PrevMatch.place(x = x-30, y =y+120)

    GlobSeason = Button(fenetre_stats,command = lambda :results_season(team,blason_path,chp,fenetre_stats), image = season_stats, relief = tk.FLAT, bg = "#2B0C47", activebackground = "#2B0C47")
    GlobSeason.place(x = 380, y =170)

    fenetre_stats.mainloop()
    