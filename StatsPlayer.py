# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 16:25:03 2020

@author: benja
"""
import sqlite3
# from tkinter import *
import tkinter as tk
from tkinter import Toplevel, Canvas, PhotoImage
from tkinter import font as tkFont
from PIL import Image, ImageTk, ImageEnhance
import pandas as pd
import math
from math import pi

import matplotlib.pyplot as plt

from definitions import imageEnhancer,levelcolor

def players_stats(fenetremain,Joueurs,label_disp, comboj,dic_clubs_id,main_menu_font):

    club = label_disp["text"]
    joueur = comboj.get()
    fenetre_player = Toplevel(fenetremain)
    fenetre_player.title(f"Fiche détaillée de {joueur}")
    width = 1920
    height = 1080
    fenetre_player.geometry(f'{width}x{height}+0+0')
    fenetre_player.minsize(width//2, 1080//2)
    fenetre_player.resizable(0, 0)
    fenetre_player.bind("<F11>", lambda event: fenetre_player.attributes("-fullscreen",
                                    not fenetre_player.attributes("-fullscreen")))
    fenetre_player.bind("<Escape>", lambda event: fenetre_player.attributes("-fullscreen", False))
    fenetre_player.iconphoto(True, PhotoImage(file='images/icones/root_icone.png'))
    
    background_image = PhotoImage(file = r"images/backgrounds/pitch_vertical.png")

    can = Canvas(fenetre_player, width= width,height=height, bg = "#1B0C43")
    can.pack()
    can.create_image(1920-400,1080//2, image = background_image)
    
    conn = sqlite3.connect(f'databases/alldata.db')
    c = conn.cursor()
    stats = c.execute('''SELECT LS,ST,RS,LW,LF,CF,RF,RW,LAM,CAM,RAM,LM,LCM,CM,RCM,RM,LWB,LDM,CDM,RDM,RWB,LB,LCB,CB,RCB,RB,GK, PAC,SHO,PAS,DRI,DEF,PHY, ID,
                          Crossing,Finishing,HeadingAccuracy,ShortPassing,Volleys,Dribbling,Curve,FKAccuracy,LongPassing,BallControl,Acceleration,SprintSpeed,
                          Agility,Reactions,Balance,ShotPower,Jumping,Stamina,Strength,LongShots,Aggression,Interceptions,Positioning,Vision,Penalties,Composure,
                          Marking,StandingTackle,SlidingTackle ,Nationality, Club, WF,SM,IR
                          FROM Players
                          WHERE Club = ? AND Name = ?''',(club,joueur,))

    for row in stats.fetchall():
        LS = [row[0].rsplit('+', 1)[0]]
        ST = [row[1].rsplit('+', 1)[0]]
        RS = [row[2].rsplit('+', 1)[0]]
        LW = [row[3].rsplit('+', 1)[0]]
        LF = [row[4].rsplit('+', 1)[0]]
        CF = [row[5].rsplit('+', 1)[0]]
        RF = [row[6].rsplit('+', 1)[0]]
        RW = [row[7].rsplit('+', 1)[0]]
        LAM = [row[8].rsplit('+', 1)[0]]
        CAM = [row[9].rsplit('+', 1)[0]]
        RAM = [row[10].rsplit('+', 1)[0]]
        LM = [row[11].rsplit('+', 1)[0]]
        LCM = [row[12].rsplit('+', 1)[0]]
        CM = [row[13].rsplit('+', 1)[0]]
        RCM = [row[14].rsplit('+', 1)[0]]
        RM = [row[15].rsplit('+', 1)[0]]
        LWB = [row[16].rsplit('+', 1)[0]]
        LDM = [row[17].rsplit('+', 1)[0]]
        CDM = [row[18].rsplit('+', 1)[0]]
        RDM = [row[19].rsplit('+', 1)[0]]
        RWB = [row[20].rsplit('+', 1)[0]]
        LB = [row[21].rsplit('+', 1)[0]]
        LCB = [row[22].rsplit('+', 1)[0]]
        CB = [row[23].rsplit('+', 1)[0]]
        RCB = [row[24].rsplit('+', 1)[0]]
        RB = [row[25].rsplit('+', 1)[0]]
        GK = [row[26].rsplit('+', 1)[0]]
        
        PAC,SHO,PAS,DRI,DEF,PHY = row[27],row[28],row[29],row[30],row[31],row[32]
        
        joueur_ID = row[33]
        
        # pays = row[63]
        club = row[64]
        id_ecu = dic_clubs_id[f'{club}']
        
        weakfoot = row[65].rsplit('★',1)[0]
        skillmoves =row[66].rsplit('★',1)[0]
        reputation =row[67].rsplit('★',1)[0]
            
                    
        dicstats = {"Centres":int(row[34]),"Finition":int(row[35]),"Têtes":int(row[36]),"Passes Courtes":int(row[37]),"Volées":int(float(row[38])),"Dribbles":int(row[39]),"Tirs Enroulés":int(float(row[40])),"Précision CF":int(row[41]),
                    "Passes Longues":int(row[42]),"Contrôles":int(row[43]),"Accélérations":int(row[44]),"Sprints":int(row[45]),"Agilité":int(float(row[46])),"Réactivité":int(row[47]),"Equilibre":int(float(row[48])),"Puissance Tirs":int(row[49]),"Sauts":int(float(row[50])),
                    "Stamina":int(row[51]),"Force":int(row[52]),"Tirs Lointains":int(row[53]),"Aggressivité":int(row[54]),"Interceptions":int(float(row[55])),"Positionnement":int(float(row[56])),"Vista":int(float(row[57])),"Tirs Aux Buts":int(row[58]), "Calme":int(float(row[59])),
                    "Marquage":int(row[60]),"Tacles Debout":int(row[61]),"Tacles Glissés":int(float(row[62]))}
        

        l= len(dicstats)
        r=int(math.floor(math.sqrt(28)))+3
        t1,t2 = divmod(l,r)
        c = t1+(1 if t2!=0 else 0)
        # print(r,c)
        fig1, axes = plt.subplots( nrows= r, ncols = c,figsize=(3.8,5.5))
        fig1.subplots_adjust(hspace=1.1)
        fig1.subplots_adjust(wspace=1.35)
        plt.rcParams['axes.titlecolor'] = 'white'
        
        colors = ['none','none']
        for n, k in enumerate(dicstats.keys()):
            sizes = [100-dicstats[f'{k}'],dicstats[f'{k}']]


            if sizes[1] > 80:
                colors[1] = "#96DC02"
            elif sizes[1] > 70:
                colors[1] = "#D29834"
            else:
                colors[1] = "#9C3C4A"
            
            i, j = divmod(n,c)
            ax = axes[i][j]
            ax.pie(sizes,colors=colors,shadow=False, startangle=90)
            centre_circle = plt.Circle((0,0),0.75,edgecolor='none',fill=False,linewidth=0)
            my_circle=plt.Circle((0,0), 0.75, color='#1B0C43')
            ax.add_artist(centre_circle)
            ax.add_artist(my_circle)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title(k, fontsize = 8)
            ax.set_frame_on(False)
            ax.text(-0.50, -0.25, str(dicstats[f'{k}']), color ='white', fontsize = 7)
        n0=n+1
        for n in range(n0,r*c):
            i, j = divmod(n,c)
            ax = axes[i][j]     
            fig1.delaxes(ax)

        plotsavepathbarh = f"temp/attributs_de_{joueur}.png"
        plt.savefig(plotsavepathbarh, transparent=True, dpi=192)
        plt.close()
        
        
                    
        postes = [LS,ST,RS,LW,LF,CF,RF,RW,LAM,CAM,RAM,LM,LCM,CM,RCM,RM,LWB,LDM,CDM,RDM,RWB,LB,LCB,CB,RCB,RB,GK]
        for p in postes:
            if int(p[0]) >= 90:
                color = "green"
            elif int(p[0]) >= 84:
                color = "#5BAE00"
            elif int(p[0]) >= 80:
                color = "#95CA00"   
            elif int(p[0]) >= 77:
                color = "#AFD700"
            elif int(p[0]) >= 75:
                color = "#BFDF00"
            elif int(p[0]) >= 70:
                color = "#D9EC00"
            elif int(p[0]) >= 65:
                color = "#FFDF00"
            elif int(p[0]) >= 50:
                color = "#FFB200"
            elif int(p[0]) >= 35:
                color = "#FF7B00"
            elif int(p[0]) >= 20:
                color = "#EB0000"
            else:
                color = "#A60000"
            p.append(color)
                
        
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
        plotsavepathspider = f"temp/spider_plot_de_{joueur}.png"
        plt.savefig(plotsavepathspider, transparent=True, dpi=128)
        # plt.show()
        plt.close()
        

        LCx1, LCy1, LCx2, LCy2 = 1280, 130, 1360, 210
        Cx1, Cy1, Cx2, Cy2 = LCx1 +200, LCy1, LCx2 +200, LCy2
        RCx1, RCx2 = Cx1 + 200, Cx2 +200


        imageFlag = imageEnhancer(f'images/ecussons/{id_ecu}.png',340)
        
        try:
            imPlayer = Image.open(f'images/players/{joueur_ID}.png')
        except:
            imPlayer = Image.open(f'images/icones/player_icone.png')
        imPlayer = ImageEnhance.Brightness(imPlayer)
        imPlayer = imPlayer.enhance(1.1)
    
        imPlayer = imPlayer.resize((200,200))
        imagePlayer = ImageTk.PhotoImage(imPlayer)   
        
        can.create_rectangle(0,0,420,1080, fill = '#3C1B94')
        can.create_rectangle(210-103,175-103,210+103,175+103, fill = 'white')
        # can.create_rectangle(145-100,145-100,145+100,145+100, fill = '#322654')
        can.create_image(210,175, image = imageFlag)
        can.create_image(210,175, image = imagePlayer)
        
        roundschart = ImageTk.PhotoImage(Image.open(f"{plotsavepathbarh}"))
        can.create_image(758,560, image = roundschart)
        jchart_spi = ImageTk.PhotoImage(Image.open(rf"{plotsavepathspider}").resize((615,445)))
        can.create_image(202,500, image = jchart_spi)
        
        
        # PAC,SHO,PAS,DRI,DEF,PHY
        x = 285
        y = 740
        stas_font2 = tkFont.Font(family='Helvetica', size=20)
        can.create_text(x,y, text = f'Vitesse : {PAC}', font = stas_font2, fill = '#E8E6EC', anchor = tk.E)
        can.create_text(x,y+50, text = f'Frappes : {SHO}', font = stas_font2, fill = '#E8E6EC', anchor = tk.E)
        can.create_text(x,y+100, text = f'Passes : {PAS}', font = stas_font2, fill = '#E8E6EC', anchor = tk.E)
        can.create_text(x,y+150, text = f'Dribbles : {DRI}', font = stas_font2, fill = '#E8E6EC', anchor = tk.E)
        can.create_text(x,y+200, text = f'Défense : {DEF}', font = stas_font2, fill = '#E8E6EC', anchor = tk.E)
        can.create_text(x,y+250, text = f'Physique : {PHY}', font = stas_font2, fill = '#E8E6EC', anchor = tk.E)
        
        stats_font = tkFont.Font(family='DejaVu Sans', size=16)

        can.create_text(682+5,881, text = 'Pied Faible', font = stats_font,fill = '#E8E6EC')
        can.create_text(848+5,881, text = 'Gestes Techniques', font = stats_font,fill = '#E8E6EC')
        can.create_text(1014+5,881, text = 'Réputation', font = stats_font,fill = '#E8E6EC')
        star = ImageTk.PhotoImage(Image.open(f"images/icones/star.png").resize((75,75)))
        can.create_image(682+5,930, image = star)
        can.create_image(848+5,930, image = star)
        can.create_image(1014+5,930, image = star)
        can.create_text(683+5,930.5, text = weakfoot, font = main_menu_font)
        can.create_text(849+5,930.5, text = skillmoves, font = main_menu_font)
        can.create_text(1015+5,930.5, text = reputation, font = main_menu_font)
        
        
        can.create_oval(LCx1, LCy1,LCx2,LCy2, outline = 'white', width = 2, fill = LS[1])
        can.create_text((LCx2+LCx1)//2, (LCy2+LCy1)//2, text = LS[0], fill = 'white', font = main_menu_font)
        
        can.create_oval(Cx1, 100,Cx2,180, outline = 'white', width = 2,fill = ST[1])
        can.create_text((Cx2+Cx1)//2, 140, text = ST[0], fill = 'white', font = main_menu_font)

        can.create_oval(RCx1, LCy1,RCx2,LCy2, outline = 'white', width = 2, fill = RS[1])
        can.create_text((RCx2+RCx1)//2, (LCy2+LCy1)//2, text = RS[0], fill = 'white', font = main_menu_font)

        can.create_oval(LCx1 - 80, (Cy1+Cy2)//2 + 0.75*LCy1,LCx1,(Cy1+Cy2)//2 + 0.75*LCy1 +80, outline = 'white', width = 2, fill = LW[1])
        can.create_text(LCx1 - 40, (LCy2+LCy1)//2 +0.75*LCy1 +40, text = LW[0], fill = 'white', font = main_menu_font)
        
        can.create_oval(LCx1+60, (Cy1+Cy2)//2 + LCy1,LCx2+60,(Cy1+Cy2)//2 + LCy1 +80, outline = 'white', width = 2, fill = LF[1])
        can.create_text(LCx1+100, (LCy2+LCy1)//2 +LCy1 +40, text = LF[0], fill = 'white', font = main_menu_font)

        can.create_oval(Cx1, (Cy1+Cy2)//2 + 0.75*LCy1,Cx2,(Cy1+Cy2)//2 + 0.75*LCy1 +80, outline = 'white', width = 2, fill = CF[1])
        can.create_text((Cx2+Cx1)//2, (LCy2+LCy1)//2 + 0.75*LCy1 +40, text = CF[0], fill = 'white', font = main_menu_font)

        can.create_oval(Cx2+60, (Cy1+Cy2)//2 + LCy1,Cx2+140,(Cy1+Cy2)//2 + LCy1 +80, outline = 'white', width = 2, fill = RF[1])
        can.create_text(Cx2+100, (LCy2+LCy1)//2 +LCy1 +40, text = RF[0], fill = 'white', font = main_menu_font)
        
        can.create_oval(RCx1 +80, (Cy1+Cy2)//2 + 0.75*LCy1,RCx2+80,(Cy1+Cy2)//2 + 0.75*LCy1 +80, outline = 'white', width = 2, fill = RW[1])
        can.create_text(RCx1 +120, (LCy2+LCy1)//2+ 0.75*LCy1 +40, text = RW[0], fill = 'white', font = main_menu_font)

        can.create_oval(LCx1, (Cy1+Cy2)//2 + 2*LCy1,LCx2,(Cy1+Cy2)//2 + 2*LCy1 +80, outline = 'white', width = 2, fill = LAM[1])
        can.create_text((LCx2+LCx1)//2, (LCy2+LCy1)//2+ 2*LCy1 +40, text = LAM[0], fill = 'white', font = main_menu_font)

        can.create_oval(Cx1, (Cy1+Cy2)//2 + 2*LCy1,Cx2,(Cy1+Cy2)//2 + 2*LCy1 +80, outline = 'white', width = 2, fill = CAM[1])
        can.create_text((Cx2+Cx1)//2, (LCy2+LCy1)//2+ 2*LCy1 +40, text = CAM[0], fill = 'white', font = main_menu_font)
        
        can.create_oval(RCx1, (Cy1+Cy2)//2 + 2*LCy1,RCx2,(Cy1+Cy2)//2 + 2*LCy1 + 80, outline = 'white', width = 2, fill = RAM[1])
        can.create_text((RCx2+RCx1)//2, (LCy2+LCy1)//2+ 2*LCy1 +40, text = RAM[0], fill = 'white', font = main_menu_font)

        can.create_oval(LCx1 - 80, (Cy1+Cy2)//2 + 2.75*LCy1,LCx1,(Cy1+Cy2)//2 + 2.75*LCy1 +80, outline = 'white', width = 2, fill = LM[1])
        can.create_text(LCx1 - 40, (LCy2+LCy1)//2+ 2.75*LCy1 +40, text = LM[0], fill = 'white', font = main_menu_font)
        
        can.create_oval(LCx1+60, (Cy1+Cy2)//2 + 3*LCy1,LCx2+60,(Cy1+Cy2)//2 + 3*LCy1 +80, outline = 'white', width = 2, fill = LCM[1])
        can.create_text(LCx1+100, (LCy2+LCy1)//2+ 3*LCy1 +40, text = LCM[0], fill = 'white', font = main_menu_font)

        can.create_oval(Cx1, (Cy1+Cy2)//2 + 3*LCy1,Cx2,(Cy1+Cy2)//2 + 3*LCy1 +80, outline = 'white', width = 2, fill = CM[1])
        can.create_text((Cx2+Cx1)//2, (LCy2+LCy1)//2+ 3*LCy1 +40, text = CM[0], fill = 'white', font = main_menu_font)

        can.create_oval(Cx2+60, (Cy1+Cy2)//2 + 3*LCy1,Cx2+140,(Cy1+Cy2)//2 + 3*LCy1 +80, outline = 'white', width = 2, fill = RCM[1])
        can.create_text(Cx2+100, (LCy2+LCy1)//2+ 3*LCy1 +40, text = RCM[0], fill = 'white', font = main_menu_font)
        
        can.create_oval(RCx1 +80, (Cy1+Cy2)//2 + 2.75*LCy1,RCx2+80,(Cy1+Cy2)//2 + 2.75*LCy1 +80, outline = 'white', width = 2, fill = RM[1])
        can.create_text(RCx1 +120, (LCy2+LCy1)//2+ 2.75*LCy1 +40, text = RM[0], fill = 'white', font = main_menu_font)

        can.create_oval(LCx1 - 80, (Cy1+Cy2)//2 + 3.75*LCy1,LCx1,(Cy1+Cy2)//2 + 3.75*LCy1 +80, outline = 'white', width = 2, fill = LWB[1])
        can.create_text(LCx1 - 40, (LCy2+LCy1)//2+ 3.75*LCy1 +40, text = LWB[0], fill = 'white', font = main_menu_font)
        
        can.create_oval(LCx1+60, (Cy1+Cy2)//2 + 4*LCy1,LCx2+60,(Cy1+Cy2)//2 + 4*LCy1 +80, outline = 'white', width = 2, fill = LDM[1])
        can.create_text(LCx1+100, (LCy2+LCy1)//2+ 4*LCy1 +40, text = LDM[0], fill = 'white', font = main_menu_font)

        can.create_oval(Cx1, (Cy1+Cy2)//2 + 4*LCy1,Cx2,(Cy1+Cy2)//2 + 4*LCy1 +80, outline = 'white', width = 2, fill = CDM[1])
        can.create_text((Cx2+Cx1)//2, (LCy2+LCy1)//2+ 4*LCy1 +40, text = CDM[0], fill = 'white', font = main_menu_font)

        can.create_oval(Cx2+60, (Cy1+Cy2)//2 + 4*LCy1,Cx2+140,(Cy1+Cy2)//2 + 4*LCy1 +80, outline = 'white', width = 2, fill = RDM[1])
        can.create_text(Cx2+100, (LCy2+LCy1)//2+ 4*LCy1 +40, text = RDM[0], fill = 'white', font = main_menu_font)
        
        can.create_oval(RCx1 +80, (Cy1+Cy2)//2 + 3.75*LCy1,RCx2+80,(Cy1+Cy2)//2 + 3.75*LCy1 +80, outline = 'white', width = 2, fill = RWB[1])
        can.create_text(RCx1 +120, (LCy2+LCy1)//2+ 3.75*LCy1 +40, text = RWB[0], fill = 'white', font = main_menu_font)

        can.create_oval(LCx1 - 80, (Cy1+Cy2)//2 + 5*LCy1,LCx1,(Cy1+Cy2)//2 + 5*LCy1 +80, outline = 'white', width = 2, fill = LB[1])
        can.create_text(LCx1 - 40, (LCy2+LCy1)//2+ 5*LCy1 +40, text = LB[0], fill = 'white', font = main_menu_font)
        
        can.create_oval(LCx1+60, (Cy1+Cy2)//2 +  5.2*LCy1,LCx2+60,(Cy1+Cy2)//2 +  5.2*LCy1 +80, outline = 'white', width = 2, fill = LCB[1])
        can.create_text(LCx1+100, (LCy2+LCy1)//2+  5.2*LCy1 +40, text = LCB[0], fill = 'white', font = main_menu_font)

        can.create_oval(Cx1, (Cy1+Cy2)//2 +  5.2*LCy1,Cx2,(Cy1+Cy2)//2 +  5.2*LCy1 +80, outline = 'white', width = 2, fill = CB[1])
        can.create_text((Cx2+Cx1)//2, (LCy2+LCy1)//2+  5.2*LCy1 +40, text = CB[0], fill = 'white', font = main_menu_font)

        can.create_oval(Cx2+60, (Cy1+Cy2)//2 +  5.2*LCy1,Cx2+140,(Cy1+Cy2)//2 + 5.2*LCy1 +80, outline = 'white', width = 2, fill = RCB[1])
        can.create_text(Cx2+100, (LCy2+LCy1)//2+  5.2*LCy1 +40, text = RCB[0], fill = 'white', font = main_menu_font)
        
        can.create_oval(RCx1 +80, (Cy1+Cy2)//2 + 5*LCy1,RCx2+80,(Cy1+Cy2)//2 + 5*LCy1 +80, outline = 'white', width = 2, fill = RB[1])
        can.create_text(RCx1 +120, (LCy2+LCy1)//2+ 5*LCy1 +40, text = RB[0], fill = 'white', font = main_menu_font)

        can.create_oval(Cx1, (Cy1+Cy2)//2 + 6.1*LCy1,Cx2,(Cy1+Cy2)//2 + 6.1*LCy1 +80, outline = 'white', width = 2, fill = GK[1])
        can.create_text((Cx2+Cx1)//2, (LCy2+LCy1)//2+ 6.1*LCy1 +40, text = GK[0], fill = 'white', font = main_menu_font)      
    conn.close()

    fenetre_player.mainloop()