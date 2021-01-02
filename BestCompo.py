# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 16:14:58 2020

@author: benja
"""
import sqlite3
from PIL import ImageTk
from tkinter import ttk, Toplevel, Canvas, PhotoImage
import pandas as pd
from pulp import *
import numpy as np 
import pandas as pd

prob = LpProblem("BestTeam", LpMaximize)

def build_team(joueurs_notes,tactique):
    players = len(joueurs_notes)
    names = []
    for p in players:
        names.append(p[0])
    # df 
    # array = np.array([])
    # c = match_info.values()
def best_tactic(fenetremain,teamdata,selected_players):
    def updatetactic(event):
        tactique = combodispo.get()
        disp_compo(tactique)

    players, team, imEcusson,imJersey_home,imJersey_away,jersey_home = teamdata()
    
    fenetre_team_maker = Toplevel(fenetremain)
    fenetre_team_maker.title("Créateur")
    fenetre_team_maker.geometry('1920x1080')
    fenetre_team_maker.resizable(0, 0) 
    fenetre_team_maker.iconphoto(True, PhotoImage(file='images/icones/root_icone.png'))
    fenetre_team_maker.bind("<F11>", lambda event: fenetre_team_maker.attributes("-fullscreen",
                                    not fenetre_team_maker.attributes("-fullscreen")))
    fenetre_team_maker.bind("<Escape>", lambda event: fenetre_team_maker.attributes("-fullscreen", False))
    
    can = Canvas(fenetre_team_maker, width = 1920, height = 1080, bg = '#370F58')   
    pitch = PhotoImage(file = r"images/backgrounds/pitch_vertical.png")
    can.create_image(1920/2,1080/2,image = pitch)
    
    cote = 130
    recotex = 135
    recotey = 150
    x1 = 625
    x2 = x1 +cote
    y1 = 40
    y2 = y1 + cote
    
    jersey_H = jersey_home.resize((int(78/100*cote),int(78/100*cote)))
    jerseyH = ImageTk.PhotoImage(jersey_H)
                    
    dispos = []
    conn = sqlite3.connect(f'databases/alldata.db')
    c = conn.cursor()
    tactics = c.execute("SELECT * FROM Dispositifs")
    for col in tactics.fetchall():
        dispositif = col[0]
        GK = col[1]
        LB = col[2]
        LCB = col[3]
        CB = col[4]
        RCB = col[5]
        RB = col[6]
        LWB = col[7]
        LDM = col[8]
        CDM = col[9]
        RDM = col[10]
        RWB = col[11]
        LM = col[12]
        LCM = col[13]
        CM = col[14]
        RCM = col[15]
        RM = col[16]
        LAM = col[17]
        CAM = col[18]
        RAM = col[19]
        LW = col[20]
        LF = col[21]
        CF = col[22]
        RF = col[23]
        RW = col[24]
        LS = col[25]
        ST = col[26]
        RS = col[27]
        dispo = [dispositif,GK,LB,LCB,CB,RCB,RB,LWB,LDM,CDM,RDM,RWB,LM,LCM,CM,RCM,RM,LAM,CAM,RAM,LW,LF,CF,RF,RW,LS,ST,RS]
        dispos.append(dispo)
        
    dftactic = pd.DataFrame(dispos, columns =['dispositif','GK','LB','LCB','CB','RCB','RB','LWB','LDM','CDM','RDM','RWB','LM','LCM','CM','RCM','RM','LAM','CAM','RAM','LW','LF','CF','RF','RW','LS','ST','RS'])
    dftactic = dftactic.set_index('dispositif')
    compo = dftactic.index.values.tolist() 
            
    ids = []
    for j in players:
        ids.append(j[-1])

    joueurs_notes = []
    for i in ids:
        conn = sqlite3.connect(f'databases/alldata.db')
        c = conn.cursor()
        stats = c.execute(f'''SELECT LS,ST,RS,LW,LF,CF,RF,RW,LAM,CAM,RAM,LM,LCM,CM,RCM,RM,LWB,LDM,CDM,RDM,RWB,LB,LCB,CB,RCB,RB,GK, Name,OVA,BP
                              FROM Players
                              WHERE ID = ? {selected_players}''',(i,))

        for row in stats.fetchall():
            LS = row[0].rsplit('+', 1)[0]
            ST = row[1].rsplit('+', 1)[0]
            RS = row[2].rsplit('+', 1)[0]
            LW = row[3].rsplit('+', 1)[0]
            LF = row[4].rsplit('+', 1)[0]
            CF = row[5].rsplit('+', 1)[0]
            RF = row[6].rsplit('+', 1)[0]
            RW = row[7].rsplit('+', 1)[0]
            LAM = row[8].rsplit('+', 1)[0]
            CAM = row[9].rsplit('+', 1)[0]
            RAM = row[10].rsplit('+', 1)[0]
            LM = row[11].rsplit('+', 1)[0]
            LCM = row[12].rsplit('+', 1)[0]
            CM = row[13].rsplit('+', 1)[0]
            RCM = row[14].rsplit('+', 1)[0]
            RM = row[15].rsplit('+', 1)[0]
            LWB = row[16].rsplit('+', 1)[0]
            LDM = row[17].rsplit('+', 1)[0]
            CDM = row[18].rsplit('+', 1)[0]
            RDM = row[19].rsplit('+', 1)[0]
            RWB = row[20].rsplit('+', 1)[0]
            LB = row[21].rsplit('+', 1)[0]
            LCB = row[22].rsplit('+', 1)[0]
            CB = row[23].rsplit('+', 1)[0]
            RCB = row[24].rsplit('+', 1)[0]
            RB = row[25].rsplit('+', 1)[0]
            GK = row[26].rsplit('+', 1)[0]
            Name,OVA,BP = row[27],row[28],row[29]
            
            joueurdetail = [Name,OVA,BP,LS,ST,RS,LW,LF,CF,RF,RW,LAM,CAM,RAM,LM,LCM,CM,RCM,RM,LWB,LDM,CDM,RDM,RWB,LB,LCB,CB,RCB,RB,GK]
        joueurs_notes.append(joueurdetail)
        conn.close()   
            
    dfpostes = pd.DataFrame(joueurs_notes, columns =['Name', 'OVA','BP','LS','ST','RS','LW','LF','CF','RF','RW','LAM','CAM','RAM','LM','LCM','CM','RCM','RM','LWB','LDM','CDM','RDM','RWB','LB','LCB','CB','RCB','RB','GK'])
    print(dfpostes)
    
    # titus = []
    # postes_titus = []
    # subs = []
    # n = 0
    # for i in dfpostes.index:
    #     maxValueBP = pd.to_numeric(dfpostes['OVA']).argmax()    
    #     jname, pbp, pova = dfpostes.iloc[maxValueBP]['Name'],dfpostes.iloc[maxValueBP]['BP'],dfpostes.iloc[maxValueBP]['OVA']
    #     joueur =[jname,pbp,pova]
    #     dfpostes=dfpostes.drop([dfpostes.index[maxValueBP]])
    #     if n<=11 and ('j'+joueur[1]) not in postes_titus:
    #         titus.append(joueur)
    #         postes_titus.append('j'+joueur[1])
    #         n = n+1

    #     else:
    #         subs.append(joueur)


    x,y = 50,50
    for p in players:
        can.create_text(x,y, text = p[0], fill = 'white')
        y = y+50
        if y > 900:
            x,y = 150,50
    
    
    def disp_compo(tactique):
        tactinfo = dftactic.loc[tactique]
        can.delete("jersey")
        if tactinfo[26] == 1.0:
            rs = can.create_image((x1+2*recotex+x2)//2-45, (y1+y2)//2+30, image = jerseyH, tags ='jersey')
        if tactinfo[25] == 1.0:
            st = can.create_image((x1+2*recotex+x2+2*recotex)//2, (y1+y2)//2+20, image = jerseyH, tags ='jersey')
        if tactinfo[24] == 1.0:
            ls = can.create_image((x1+3*recotex+x2+3*recotex)//2+45, (y1+y2)//2+30, image = jerseyH, tags ='jersey')
        
        if tactinfo[23] == 1.0:
            rw = can.create_image((x1+x2)//2,(y1+recotey+y2+recotey)//2+30, image = jerseyH,tags ='jersey')
        if tactinfo[22] == 1.0:
            rf = can.create_image((x1+recotex+x2+recotex)//2+10, (y1+recotey+y2+recotey)//2-18, image = jerseyH, tags ='jersey')
        if tactinfo[21] == 1.0:
            cf = can.create_image((x1+2*recotex+x2+2*recotex)//2,(y1+recotey+y2+recotey)//2-35, image = jerseyH, tags ='jersey')
        if tactinfo[20] == 1.0:
            lf =can.create_image((x1+3*recotex+x2+3*recotex)//2-10,(y1+recotey+y2+recotey)//2-18, image = jerseyH, tags ='jersey')
        if tactinfo[19] == 1.0:
            lw = can.create_image((x1+4*recotex+x2+4*recotex)//2,(y1+recotey+y2+recotey)//2+30, image = jerseyH, tags ='jersey')
        
        if tactinfo[18] == 1.0:
            ram = can.create_image((x1+recotex+x2+recotex)//2,(y1+2*recotey+y2+2*recotey)//2-10, image = jerseyH, tags ='jersey')
        if tactinfo[17] == 1.0:
            cam = can.create_image((x1+2*recotex+x2+2*recotex)//2,(y1+2*recotey+y2+2*recotey)//2-10, image = jerseyH, tags ='jersey')
        if tactinfo[16] == 1.0:
            lam = can.create_image((x1+3*recotex+x2+3*recotex)//2,(y1+2*recotey+y2+2*recotey)//2-10, image = jerseyH, tags ='jersey')
        
        
        if tactinfo[15] == 1.0:
            rm = can.create_image((x1+x2)//2-10,(y1+3*recotey+y2+3*recotey)//2-15, image = jerseyH, tags ='jersey')
        if tactinfo[14] == 1.0:
            rcm = can.create_image((x1+recotex+x2+recotex)//2-9,(y1+3*recotey+y2+3*recotey)//2, image = jerseyH, tags ='jersey')
        if tactinfo[13] == 1.0:
            cm =can.create_image((x1+2*recotex+x2+2*recotex)//2, (y1+3*recotey+y2+3*recotey)//2+18, image = jerseyH, tags ='jersey')
        if tactinfo[12] == 1.0:
            lcm = can.create_image((x1+3*recotex+x2+3*recotex)//2+9,(y1+3*recotey+y2+3*recotey)//2, image = jerseyH, tags ='jersey')
        if tactinfo[11] == 1.0:
            lm = can.create_image((x1+4*recotex+x2+4*recotex)//2+10,(y1+3*recotey+y2+3*recotey)//2-15, image = jerseyH, tags ='jersey') 
        
        
        if tactinfo[10] == 1.0:   
            rwb = can.create_image((x1+x2)//2,(y1+4*recotey+y2+4*recotey)//2-20, image = jerseyH, tags ='jersey')
        if tactinfo[9] == 1.0:
            rdm = can.create_image((x1+recotex+x2+recotex)//2,(y1+4*recotey+y2+4*recotey)//2-10, image = jerseyH, tags ='jersey')
        if tactinfo[8] == 1.0:    
            lcm = can.create_image((x1+2*recotex+x2+2*recotex)//2, (y1+4*recotey+y2+4*recotey)//2-5, image = jerseyH, tags ='jersey')
        if tactinfo[7] == 1.0:    
            ldm = can.create_image((x1+3*recotex+x2+3*recotex)//2,(y1+4*recotey+y2+4*recotey)//2-10, image = jerseyH, tags ='jersey')
        if tactinfo[6] == 1.0:   
            lwb = can.create_image((x1+4*recotex+x2+4*recotex)//2,(y1+4*recotey+y2+4*recotey)//2-20, image = jerseyH, tags ='jersey')
        
        
        if tactinfo[5] == 1.0:
            can.create_image((x1+x2)//2-15,(y1+5*recotey+y2+5*recotey)//2-30, image = jerseyH, tags ='jersey')#rb
        if tactinfo[4] == 1.0:
            can.create_image((x1+recotex+x2+recotex)//2-10,(y1+5*recotey+y2+5*recotey)//2-10, image = jerseyH, tags ='jersey')#rcb
        if tactinfo[3] == 1.0:
            can.create_image((x1+2*recotex+x2+2*recotex)//2, (y1+5*recotey+y2+5*recotey)//2+10, image = jerseyH, tags ='jersey')#cb
        if tactinfo[2] == 1.0:
            can.create_image((x1+3*recotex+x2+3*recotex)//2+10,(y1+5*recotey+y2+5*recotey)//2-10, image = jerseyH, tags ='jersey')#lcb
        if tactinfo[1] == 1.0:
            can.create_image((x1+4*recotex+x2+4*recotex)//2+15,(y1+5*recotey+y2+5*recotey)//2-30, image = jerseyH, tags ='jersey')#lb
        if tactinfo[0] == 1.0:
            can.create_image((x1+2*recotex+x2+2*recotex)//2, (y1+6*recotey+y2+6*recotey)//2-20, image = jerseyH, tags ='jersey')#gk
            
    can.pack()
    
    combodispo = ttk.Combobox(fenetre_team_maker, values = compo,state = "readonly")
    combodispo.bind("<<ComboboxSelected>>", updatetactic)
    combodispo.place(x=300,y=100)
    
    fenetre_team_maker.mainloop()