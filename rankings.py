# -*- coding: utf-8 -*-
"""
GP211

Ranking system
"""
# import pickle
# import sqlite3
from fuzzywuzzy import process
import pandas as pd
import numpy as np
import operator
# associer à chaque club le chpt

def dicfixtures(team,chp):
    nfixture = next_fixture(team,chp)
    prevfixtures,nbmatchs = last_fixture(team,chp)
    
    isEmpty = nfixture.empty
    if isEmpty == False :
        dffixt = pd.concat([prevfixtures,nfixture])
    else:
        dffixt = prevfixtures

    team_fixtures = {}
    i = 0
    for index, row in dffixt.iterrows():
        try:
            i+=1

            HeureGMT = row['Time']
            h,ms = HeureGMT.rsplit(':',2)[0],HeureGMT.rsplit(':',2)[1]
            h = int(h)+1
            HeureLocale = str(h)+':'+ms
            dt = row['Date']
            # print(dt)
            try:
                an = (dt.rsplit('-',2)[0])
                mois = (dt.rsplit('-',2)[1])
                jour = dt.rsplit('-',1)[1]
                dt = jour+'/'+mois+'/'+an
            except:
                pass

            team_fixtures[str(i)] = [dt,HeureLocale,row['HomeTeam'],row['AwayTeam'],row['FTHG'],row['FTAG']]
        except:
            pass

    return(team_fixtures,nbmatchs)
    
def last_fixture(team,chp):
    team = find_best_match(team,chp)
    df,Teams = prepair_df(chp)
    nbMatchs = len(df[np.logical_or(df['HomeTeam']== team ,df['AwayTeam']== team)]) 
        
    last_fixture = df[np.logical_or(df['HomeTeam']== team ,df['AwayTeam']== team)][['Date','Time','HomeTeam','AwayTeam','FTHG','FTAG','FTR']]#.iloc[match_index]

    return(last_fixture,nbMatchs)
    

def next_fixture(team,chp):
    
    team = find_best_match(team,chp)
    chpt = chp
    if chpt != 'DNK' and chpt != 'ARG' and chpt != 'BRA' and chpt != 'SWZ' and chpt != 'MEX' and chpt != 'IRL' and chpt != 'USA' and chpt != 'RUS' and chpt != 'CHN'and chpt != 'JPN'and chpt != 'AUT' and chpt != 'SWE' and chpt != 'NOR' and chpt != 'ROU' and chpt != 'POL' :
        fixtures = pd.read_excel('databases/csv/fixtures.xlsx', index_col=None)
        fixtures.to_csv('databases/csv/fixtures.csv', encoding='utf-8', index = False)
        dfixtures = pd.read_csv("databases/csv/fixtures.csv", sep = ',')
        fixture = dfixtures[np.logical_and(dfixtures['Div'] == chpt,np.logical_or(dfixtures['HomeTeam']==team,dfixtures['AwayTeam']==team))][['Date','Time','HomeTeam','AwayTeam']]
    else:
        extrafixtures = pd.read_excel('databases/csv/extrafixtures.xlsx', index_col=None)
        extrafixtures.to_csv('databases/csv/extrafixtures.csv', encoding='utf-8', index = False)
        extradf = pd.read_csv("databases/csv/extrafixtures.csv", sep = ',')
        extradf = extradf.rename(columns={'League': 'Div', 'Home': 'HomeTeam', 'Away':'AwayTeam'})
        extradf.loc[extradf['Country'] == 'China', 'League'] = 'CHN'
        extradf.loc[extradf['Country'] == 'Argentina', 'League'] = 'ARG'
        extradf.loc[extradf['Country'] == 'Sweden', 'League'] = 'SWE'
        extradf.loc[extradf['Country'] == 'Switzerland', 'League'] = 'SWZ'
        extradf.loc[extradf['Country'] == 'Romania', 'League'] = 'ROU'
        extradf.loc[extradf['Country'] == 'Russia', 'League'] = 'RUS'
        extradf.loc[extradf['Country'] == 'Poland', 'League'] = 'POL'
        extradf.loc[extradf['Country'] == 'Norway', 'League'] = 'NOR'
        extradf.loc[extradf['Country'] == 'Japan', 'League'] = 'JPN'
        extradf.loc[extradf['Country'] == 'Denmark', 'League'] = 'DNK'
        extradf.loc[extradf['Country'] == 'Austria', 'League'] = 'AUT'
        extradf.loc[extradf['Country'] == 'Ireland', 'League'] = 'IRL'
        extradf.loc[extradf['Country'] == 'Mexico', 'League'] = 'MEX'
        extradf.loc[extradf['Country'] == 'Brazil', 'League'] = 'BRA'
        extradf.loc[extradf['Country'] == 'USA', 'League'] = 'USA'
        fixture = extradf[np.logical_and(extradf['League'] == chpt,np.logical_or(extradf['HomeTeam']==team,extradf['AwayTeam']==team))][['Div','Date','Time','HomeTeam','AwayTeam']]
    # isempty = fixture.empty
    # team_nfixture = {}
    # if isempty == False:
    return(fixture)

def prepair_df(chp):
    c = chp
    dict_df = {}
    Teams = {} 
    dict_df = pd.read_csv(f"databases/csv/{c}2021.csv", sep = ',')
    
    df = dict_df
    
    if c == 'DNK' or c == 'ARG' or c == 'BRA' or c == 'SWZ' or c == 'MEX' or c == 'IRL' or c == 'USA' or c == 'RUS' or c == 'CHN'or c == 'JPN'or c == 'AUT' or c == 'SWE' or c == 'NOR' or c == 'ROU' or c == 'POL' :
        df = df.rename(columns={'Home': 'HomeTeam', 'Away' : 'AwayTeam', 'HG' : 'FTHG', 'AG' : 'FTAG', 'Res': 'FTR'})
        dict_df= df[np.logical_or(df['Season'].astype('str')== '2020',df['Season']== '2020/2021')]
        df = (df[np.logical_or(df['Season'].astype('str')== '2020',df['Season']== '2020/2021')][['Date','Time','HomeTeam','AwayTeam','FTHG','FTAG','FTR']])
    
    J1domi = sorted(df['HomeTeam'].unique())
    J1exte = sorted(df['AwayTeam'].unique())
    Teams = sorted(np.unique(J1domi + J1exte))
    return(df,Teams)
    
def TeamsResults(chp):
    dictdf,Teams = prepair_df(chp)
    # global maxmatchs
    results = []
    # maxmatchs=0
    nbMatchs = 0

    for t in Teams:
        df = dictdf
        
        nbMatchs = len(df[np.logical_or(df['HomeTeam']== t ,df['AwayTeam']== t)]) 
        TeamWins = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['FTR']=='H'),np.logical_and(df['AwayTeam']== t,df['FTR']=='A'))])
        TeamDraws = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['FTR']=='D'),np.logical_and(df['AwayTeam']== t,df['FTR']=='D'))])
        TeamLosses = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['FTR']=='A'),np.logical_and(df['AwayTeam']== t,df['FTR']=='H'))])
        
        ButsPourDomi = int(df[df['HomeTeam']== t][['FTHG']].sum())
        ButsPourExte = int(df[df['AwayTeam']== t][['FTAG']].sum())
        Buts_Pour = ButsPourDomi + ButsPourExte
        
        ButsContreDomi = int(df[df['HomeTeam']== t][['FTAG']].sum())
        ButsContreExte = int(df[df['AwayTeam']== t][['FTHG']].sum())
        Buts_Contre = ButsContreDomi + ButsContreExte
        
        Diff_Buts = Buts_Pour - Buts_Contre
        
        Points = int(TeamWins*3 + TeamDraws)

        results.append([t,Points, nbMatchs, TeamWins, TeamDraws, TeamLosses, Buts_Pour, Buts_Contre, Diff_Buts])
        
        # if nbMatchs > maxmatchs:
        #     maxmatchs = nbMatchs
    return results
 
def Classementdefault(chp):
    results = TeamsResults(chp)
    sorted_teams = sorted(results, key=operator.itemgetter(1,8,6,3), reverse=True)
    taillechp = len(sorted_teams)
    dftable = pd.DataFrame(sorted_teams, columns =['TEAM', 'POINTS', 'J','V','N','D','BP','BC','+/-'],index=np.arange(len(sorted_teams))+1)
    return(dftable,taillechp)

def extract_data(data,indexes):
    teamsrank = []
    i = 0
    for row in data:
        team = [row[0][0],row[0][1],row[0][2],row[0][3],row[0][4],row[0][5],row[0][6],row[0][7],row[0][8],indexes[i]]
        teamsrank.append(team)
        i+=1
    return(teamsrank)

def focus_ranking(equipe,chp):
    team = find_best_match(equipe,chp)
    df,taille = Classementdefault(chp)
    idx = (df[df['TEAM'] == team].index[0])
    row1,row2,row3,row4,row5 = idx-2,idx-1,idx,idx+1,idx+2
    if row1<1:
        while row1<1:
            row1,row2,row3,row4,row5 = row1+1,row2+1,row3+1,row4+1,row5+1
        
    elif row5>taille:
        while row5>taille:
            row1,row2,row3,row4,row5 = row1-1,row2-1,row3-1,row4-1,row5-1
    else:pass
    indexes = [row1,row2,row3,row4,row5]
    
    datarow = []
    # print(df.loc[[row1,row2,row3,row4,row5], :])
    for row in [row1,row2,row3,row4,row5]:
        datarow.append(df.loc[[row]].values)
    data = extract_data(datarow,indexes)
    
    return(data)

def find_best_match(equipe,chp):
    df,Teams = prepair_df(chp)
    team = process.extractOne(equipe,Teams)[0]
    return(team)
        
# focus_ranking('Lyon','F1')
# next_fixture('Real Madr','SP1')
# last_fixture('Lyon','F1',4)
# dicfixtures('Lyon','F1')
# next_fixture('Botagogo','BRA')

# preTeams = []
# teamscount= []
# Teams = []
# Joueurs = []

# dic_clubs_id = {}

# conn = sqlite3.connect(f'databases/alldata.db')
# c = conn.cursor()
# data = c.execute(f"SELECT ID,Name,Club,ClubLogo,BP,Nationality FROM Players WHERE TITU IS NOT NULL")

# for row in data.fetchall():
#     try:
#         Club = row[2]
#         EcuClub = row[3]
        
#         if Club not in preTeams:
#             preTeams.append(str(Club))
#             pre_id_ecu = EcuClub.rsplit('/', 2)[1]
#             id_ecu = pre_id_ecu.rsplit('/',1)[0]
#             dic_clubs_id[f'{Club}'] = id_ecu
#         teamscount.append(Club)

#     except:pass

# for pt in preTeams:
#     freq = teamscount.count(pt)
#     if freq >= 11:
#         Teams.append(pt)
        
# conn.close()

# chpnts = ['E0','E1','E2','E3','F1','F2','SP1', 'SP2','D1','D2','I1','I2','N1','P1','SC0','SC1', 'T1','B1','G1',
#           'ARG','BRA','SWZ','MEX','IRL','USA','RUS','CHN','JPN','AUT','SWE','NOR','ROU','POL','DNK']
# def create_data():
#     import pandas as pd
#     import numpy as np

#     dict_df = {}
#     bigdict = {}
#     AllTeams = {}  
#     for c in chpnts:            #boucle permettant la lecture de tous les fichiers dans chpnts
    
#         dict_df[c] = pd.read_csv(f"databases/csv/{c}2021.csv", sep = ',') #attribution de la variable d'itération "c" à tous nos fichiers que l'on souhaite analyser (ceux du type /...2019)
    
        
#         df = dict_df[c]         #simplification de la notation du dictionnaire
        
#         if c == 'DNK' or c == 'ARG' or c == 'BRA' or c == 'SWZ' or c == 'MEX' or c == 'IRL' or c == 'USA' or c == 'RUS' or c == 'CHN'or c == 'JPN'or c == 'AUT' or c == 'SWE' or c == 'NOR' or c == 'ROU' or c == 'POL' :
#             df = df.rename(columns={'Home': 'HomeTeam', 'Away' : 'AwayTeam', 'HG' : 'FTHG', 'AG' : 'FTAG', 'Res': 'FTR'})
#             dict_df[c] = df[np.logical_or(df['Season'].astype('str')== '2020',df['Season']== '2019/2020')]
#             df = (df[np.logical_or(df['Season'].astype('str')== '2020',df['Season']== '2019/2020')][['Date','Time','HomeTeam','AwayTeam','FTHG','FTAG','FTR']])
#             # print(df)
        
#         J1domi = sorted(df['HomeTeam'].unique())
#         J1exte = sorted(df['AwayTeam'].unique())
#         AllTeams[c] = sorted(np.unique(J1domi + J1exte))
#         print(AllTeams[c])
        
#         bigdict[f'{c}'] = AllTeams[c]
        
#         with open('bigdico.pkl', 'wb') as handle:
#             pickle.dump(bigdict, handle)
    
# # create_data()
# with open('bigdico.pkl', 'rb') as handle:
#     dicochpts = pickle.load(handle)        
    
# # for chp,clubs in dicochpts.items():
# #     print(chp,clubs, len(clubs),'\n')
            
# teams_from_csv = []
# for sublist in dicochpts.values():
#     for item in sublist:
#         teams_from_csv.append(item)

# teams_from_csv = sorted(teams_from_csv)

# def find_div(team):
#     for div, listeteam in dicochpts.items():
#         for t in listeteam:
#             if t == team:
#                 return(div)

# def deleter(t,compair):
#     chpt = find_div(t)
#     print(chpt,t,compair,dic_clubs_id[f'{compair}'])
#     conn = sqlite3.connect(f'databases/alldata.db')
#     c = conn.cursor()
#     c.execute('''UPDATE Players
#     SET championnat = ?
#     WHERE Club = ?''',(chpt,compair,))
#     conn.commit()
#     conn.close()
#     teams_from_csv.remove(t)
#     preTeams.remove(compair)
#     try:
#         Teams.remove(compair)
#     except:pass

# def team_association(ratiomin):
#     for t in teams_from_csv:
#         ratio = process.extractOne(t,preTeams)[1]
        
#         if ratio ==100:
#             print(t +' ' + str(ratio) + '/100')
#             compair = process.extractOne(t,preTeams)[0]
#             deleter(t,compair)
            
#         else:
#             if ratio >= ratiomin:
#                 print(t +' ' + str(ratio) + '/100')
#                 pre_list = []
#                 compairlist = process.extract(t,preTeams,limit=3)
#                 print(compairlist)
#                 best = process.extractBests(t,compairlist)
#                 print(best)

#                 for b in best:
#                     pre_list.append([b[0][0],b[0][1],b[1]])
#                 tmplist = sorted(pre_list, key = lambda x: (int(x[1]),int(x[2])),reverse = True)
#                 compair = tmplist[0][0]
#                 deleter(t,compair)


# def update_chp():
#     ratiodecrease = 100
#     while ratiodecrease>70:
#         print(ratiodecrease)
#         team_association(ratiodecrease)
#         ratiodecrease -= 1
#         print(len(teams_from_csv),len(preTeams))
    
#     print(preTeams)
# # update_chp()