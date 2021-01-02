# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 00:46:04 2020

@author: benja
"""
from PIL import Image, ImageTk, ImageEnhance
import sqlite3

def imageEnhancer(path,sizesquare):
    imFlag = Image.open(path)
    imFlag = imFlag.resize((sizesquare,sizesquare))
    imFlag = imFlag.rotate(15)
    imFlag = imFlag.crop((75,75,275,275))
    imFlag = ImageEnhance.Brightness(imFlag)
    imFlag = imFlag.enhance(0.75)
    imageFlag = ImageTk.PhotoImage(imFlag)            
    return(imageFlag)


def testpost(dicopostes,testedpost):
    for typejoueur, listepostes in dicopostes.items():
        for poste in listepostes:
            if poste == testedpost:
                return typejoueur

def testsubposte(dicosubp,dicolen,testedpost):
    for catsubposte, listepostes in dicosubp.items():
        for poste in listepostes:
            if poste == testedpost:
                dicolen[f'{catsubposte}'] += 1
                
def fill_players(typejoueur,titutypejoueur,subtypejoueur,restypejoueur,qty):
    typejoueur = sorted(typejoueur, key = lambda x: int(x[1]),reverse = True)
    titutypejoueur.append(typejoueur[:qty])
    del typejoueur[:qty]
    if qty!=1:
        subtypejoueur.append(typejoueur[:qty]) 
        del typejoueur[:qty]
    else:
        subtypejoueur.append(typejoueur[:1]) 
        del typejoueur[:1]            
    restypejoueur.append(typejoueur[:])
    typejoueur.clear()
    
def carac_type(postetype):
    nb = 0
    snote= 0
    spot = 0
    for p in postetype[nb][:]:
        try :
            nb += 1
            snote += p[1]
            spot += p[2]
        except :pass
    try : moy = round(snote/nb,2)
    except : moy = 0
    try : pot = round(spot/nb,2)
    except:pot = 0
    return [moy,pot]


def prepair_global_team(attaquants,milieux,défenseurs,gardiens):    

    tituatt,titumil,titudef,titugar = [],[],[],[]
    subatt,submil,subdef,subgar = [],[],[],[]
    resatt,resmil,resdef,resgar = [],[],[],[]

    fill_players(attaquants,tituatt,subatt,resatt,3)
    fill_players(milieux,titumil,submil,resmil,3)
    fill_players(défenseurs,titudef,subdef,resdef,4)
    fill_players(gardiens,titugar,subgar,resgar,1)    
    
        
    equipe_type = [carac_type(tituatt),carac_type(titumil),carac_type(titudef),carac_type(titugar),'Equipe Type']
    remplacants = [carac_type(subatt),carac_type(submil),carac_type(subdef),carac_type(subgar),'Equipe Remplaçants']
    reservistes = [carac_type(resatt),carac_type(resmil),carac_type(resdef),carac_type(resgar),'Equipe Réserve']

    global_team = [equipe_type,remplacants,reservistes]

    return(global_team)

def calc_team_global(club,selected_players,dic_clubs_id):
    conn = sqlite3.connect(f'databases/alldata.db')
    c = conn.cursor()
    joueurs = c.execute(f"SELECT Name,OVA,ID,Club,Value,Wage,ReleaseClause,Age,BP,Position,TITU FROM Players WHERE Club = ?  AND TITU IS NOT NULL {selected_players}",(club,))
    ljoueurs = []
    wages= 0
    sellplayersvalues = 0
    id_ecu = 1
    for row in joueurs.fetchall():
        joueur = str(row[0])
        note = row[1]
        idjoueur = row[2]
        agejoueur = row[7]
        bestpos = row[8]
        positions = row[9]
        titu = row[10]
        
        ljoueurs.append([idjoueur,joueur,note,agejoueur,bestpos,positions,titu])
        try:
            club = row[3]
            id_ecu = dic_clubs_id[f'{club}']
            value = row[4].rsplit('€', 1)[1]
            relclause = row[6].rsplit('€', 1)[1]
            wage = row[5].rsplit('€', 1)[1]

            coefs = {'K': 1000,'M':1000000}

            valeur,relp,wagep = coefficients(coefs,wage,value,relclause)
            wages += wagep
            playervalue = valeur+relp
            sellplayersvalues += playervalue
            
        except:
            pass

    conn.close()
    players = sorted(ljoueurs, key = lambda x: int(x[2]),reverse = True)
    sorted_joueurs = [adress[1] for adress in players]
    return(sorted_joueurs,players,id_ecu,wages,sellplayersvalues)

def coefficients(coefs,wage,value,relclause):

    if 'K' in wage:
        wagep = float(wage.rsplit('K',1)[0])
        wagep = wagep*coefs['K']
    elif 'M' in wage:
        wagep = float(wage.rsplit('M',1)[0])
        wagep = wagep*coefs['M']
    else:
        wagep = float(wage)
          
    if 'K' in value:
        valeur = float(value.rsplit('K',1)[0])
        valeur = valeur*coefs['K']
    elif 'M' in value:
        valeur = float(value.rsplit('M',1)[0])
        valeur = valeur*coefs['M']
    else:
        valeur = float(value)
    
    if 'K' in relclause:
        relp = float(relclause.rsplit('K',1)[0])
        relp = relp*coefs['K']
    elif 'M' in relclause:
        relp = float(relclause.rsplit('M',1)[0])
        relp = relp*coefs['M']
    else:
        relp = float(relclause)
        
    return(valeur,relp,wagep)
   
def levelcolor(note):
        
    if note >= 90:
        notecolor = "green"
    elif note >= 84:
        notecolor = "#5BAE00"
    elif note >= 80:
        notecolor = "#95CA00"   
    elif note >= 77:
        notecolor = "#AFD700"
    elif note >= 75:
        notecolor = "#BFDF00"
    elif note >= 70:
        notecolor = "#D9EC00"
    elif note >= 65:
        notecolor = "#FF7B00"
    elif note >=60:
        notecolor = "#EB0000"
    else:
        notecolor = "#A60000"
    return(notecolor)
