# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:45:44 2020

@author: benja
"""
from rankings import prepair_df

import numpy as np
import pandas as pd
from pandas.plotting import table 
import matplotlib.pyplot as plt

from tkinter import messagebox
import subprocess, operator

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as ImReport
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from fuzzywuzzy import process

savepath = 'saves/'


def results_season(t,imEcusson,chp,fenetre_stats):
    results = []

    def Classementdefault():
        sorted_teams = sorted(results, key=operator.itemgetter(1,8,6,3), reverse=True) #tri par Points (si égalité, par Goal Average et si encore égalité par Buts Pour). ordre de priorité conservé par la suite
        taillechp = len(sorted_teams)
        dftable = pd.DataFrame(sorted_teams, columns =['TEAM', 'POINTS', 'J','V','N','D','BP','BC','+/-'],index=np.arange(len(sorted_teams))+1)
        return(dftable, taillechp)
    
    df, teams = prepair_df(chp)
    for clubs in teams: 
        team = process.extractOne(t,teams)[0]
    
    print(t,team)
    try:
        if chp != 'DNK' and chp != 'ARG' and chp != 'BRA' and chp != 'SWZ' and chp != 'MEX' and chp != 'IRL' and chp != 'USA' and chp != 'RUS' and chp != 'CHN'and chp != 'JPN'and chp != 'AUT' and chp != 'SWE' and chp != 'NOR' and chp != 'ROU' and chp != 'POL' :
        #exclusion de ces championnats car absence de données dans les fichiers CSV sur 'HTR'
            dfFull = (df[np.logical_or(df['HomeTeam']== team,df['AwayTeam']== team)][['Date','Time','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTR']]) #df correspond à notre dataframe, np.logical sont des portes logiques permettant la comparaison et/ou de données du tableau (dataframe) créé
            dfForme = dfFull.tail(5)
        else:
            dfPartial = (df[np.logical_or(df['HomeTeam']== team,df['AwayTeam']== team)][['Date','Time','HomeTeam','AwayTeam','FTHG','FTAG','FTR']])
            dfForme = dfPartial.tail(5)

        print(dfForme)
        
        nbMatchs = len(df[np.logical_or(df['HomeTeam']== team ,df['AwayTeam']== team)]) #calcul du nbre de matchs joués par une équipe en testant la présence ou non de l'équipe itérée avec les colonnes HomeTeam & AwayTeam
        TeamWins = len(df[np.logical_or(np.logical_and(df['HomeTeam']== team,df['FTR']=='H'),np.logical_and(df['AwayTeam']== team,df['FTR']=='A'))])
        TeamDraws = len(df[np.logical_or(np.logical_and(df['HomeTeam']== team,df['FTR']=='D'),np.logical_and(df['AwayTeam']== team,df['FTR']=='D'))])
        TeamLosses = len(df[np.logical_or(np.logical_and(df['HomeTeam']== team,df['FTR']=='A'),np.logical_and(df['AwayTeam']== team,df['FTR']=='H'))])
        
        ##FORME##
        
        FormeButsPourDomi = int(dfForme[dfForme['HomeTeam']== team][['FTHG']].sum())          #somme des buts marqués à domicile
        FormeButsPourExte = int(dfForme[dfForme['AwayTeam']== team][['FTAG']].sum())
        FormeButs_Pour = FormeButsPourDomi + FormeButsPourExte                             #somme des buts marqués total
        
        FormeButsContreDomi = int(dfForme[dfForme['HomeTeam']== team][['FTAG']].sum())
        FormeButsContreExte = int(dfForme[dfForme['AwayTeam']== team][['FTHG']].sum())
        FormeButs_Contre = FormeButsContreDomi + FormeButsContreExte
        
        forme = []
        lastplayed = 0
        if nbMatchs > 5:
            lastplayed = 5
        else:
            lastplayed = nbMatchs
            
        for m in range(1,lastplayed+1):
            dfLast = dfForme.tail(1)
            if len(dfLast[np.logical_or(np.logical_and(dfLast['HomeTeam']== team,dfLast['FTR']=='H'),np.logical_and(dfLast['AwayTeam']== team,dfLast['FTR']=='A'))]) == 1:
                forme.append('V')
            elif len(dfLast[np.logical_or(np.logical_and(dfLast['HomeTeam']== team,dfLast['FTR']=='D'),np.logical_and(dfLast['AwayTeam']== team,dfLast['FTR']=='D'))]) == 1:
                forme.append('N')
            else:
                forme.append('D')
            
            dfForme = dfForme.head(lastplayed-m)
        formeWins = forme.count('V')
        formeDraws = forme.count('N')
        formeLosses = forme.count('D')
        # print(forme)
        # print(f"{lastplayed} derniers matchs de {t} : ", formeWins, "Victoires", formeDraws, "Nuls", formeLosses, "Défaites" + "\n" + str(FormeButs_Pour), "Buts Marqués, ", str(FormeButs_Contre), "Buts Concédés")



        if chp != 'DNK' and chp != 'ARG' and chp != 'BRA' and chp != 'SWZ' and chp != 'MEX' and chp != 'IRL' and chp != 'USA' and chp != 'RUS' and chp != 'CHN'and chp != 'JPN'and chp != 'AUT' and chp != 'SWE' and chp != 'NOR' and chp != 'ROU' and chp != 'POL' :
            TeamHTWins = len(df[np.logical_or(np.logical_and(df['HomeTeam']== team,df['HTR']=='H'),np.logical_and(df['AwayTeam']== team,df['HTR']=='A'))])
            TeamHTDraws = len(df[np.logical_or(np.logical_and(df['HomeTeam']== team,df['HTR']=='D'),np.logical_and(df['AwayTeam']== team,df['HTR']=='D'))])
            TeamHTLosses = len(df[np.logical_or(np.logical_and(df['HomeTeam']== team,df['HTR']=='A'),np.logical_and(df['AwayTeam']== team,df['HTR']=='H'))])
            
            TeamHTscoredHome = int(df[df['HomeTeam']== team][['HTHG']].sum())
            TeamHTscoredAway = int(df[df['AwayTeam']== team][['HTAG']].sum())

            TeamHTconcededHome = int(df[df['HomeTeam']== team][['HTAG']].sum())
            TeamHTconcededAway = int(df[df['AwayTeam']== team][['HTHG']].sum())

            totscoredHT = TeamHTscoredHome + TeamHTscoredAway
            totconcededHT = TeamHTconcededHome + TeamHTconcededAway

            #+ faire stats selon domicile ou extérieur

            ShotsHome = int(df[df['HomeTeam']== team][['HS']].sum())
            ShotsAway = int(df[df['AwayTeam']== team][['AS']].sum())
            ShotsHomeTarg = int(df[df['HomeTeam']== team][['HST']].sum())
            ShotsAwayTarg = int(df[df['AwayTeam']== team][['AST']].sum())
            
            ShotsTot = ShotsHome + ShotsAway
            ShotsTargTot = ShotsHomeTarg + ShotsAwayTarg
            if ShotsTot == 0:
                ShotsTot = 1e-12
            if ShotsTargTot == 0:
                ShotsTargTot = 1e-12
            
            probTarget = ShotsTargTot/ShotsTot
            offTarget = (1 - probTarget)
            
            moyTarget = probTarget*100
            MoyOffTarget = (offTarget*100)



            def newpoint_ON():
                return np.random.randint(175,1000), np.random.randint(86, 350)
                                        #(min_x, max_x)              #(min_y, max_y)
            
            pointsOn = (newpoint_ON() for p in range(int(moyTarget)))
            LonTarget = []
            for point in pointsOn:
                LonTarget.append(point)
            # print(LonTarget)
            zip(*LonTarget)

            def newpoint_OFF():
                # nboffpoint =0
                
                offpoint = np.random.randint(10,1170), np.random.randint(10, 350)
                if (offpoint[0]<165) or (offpoint[0]>1015) or (offpoint[1]<75):
                    okpoint=True
                else:
                    okpoint=False
                return okpoint,offpoint

            LoffTarget = []
            nboff=0
            while nboff<int(MoyOffTarget):
                okpoint, offpoint = newpoint_OFF()
                if okpoint:
                    nboff+=1
                    LoffTarget.append(offpoint)
            
            Ldensity = LonTarget + LoffTarget
            w = [i[0] for i in Ldensity]
            z = [i[1] for i in Ldensity]
                    
        
            img = plt.imread("images/backgrounds/ShotsRatioBG.png")
            x = 1183
            y = 467
            plt.figure(figsize=(12, 12))
            fig, ax = plt.subplots()
            ax.imshow(img)
            if len(LonTarget) != 0 :
                plt.scatter(*zip(*LonTarget), c = '#99CC00')
            if len(LoffTarget) != 0 :
                plt.scatter(*zip(*LoffTarget), c = '#FF4B4B')
            # plt.hist2d(w,z,bins=(100, 100),cmap=plt.cm.jet)            
            plt.xlim(right=x)
            plt.xlim(left=0)
            plt.ylim(top=0)
            plt.ylim(bottom=y)
            plt.axis('off')
            plt.title(f'Ratio de tirs cadrés de {t}')
            ratiosavepath = f"temp/ratio{t}.png"
            plt.savefig(ratiosavepath, transparent=True, dpi = 128)
            plt.close()

        
        ButsPourDomi = int(df[df['HomeTeam']== team][['FTHG']].sum())          #somme des buts marqués à domicile
        ButsPourExte = int(df[df['AwayTeam']== team][['FTAG']].sum())
        Buts_Pour = ButsPourDomi + ButsPourExte                             #somme des buts marqués total
        
        ButsContreDomi = int(df[df['HomeTeam']== team][['FTAG']].sum())
        ButsContreExte = int(df[df['AwayTeam']== team][['FTHG']].sum())
        Buts_Contre = ButsContreDomi + ButsContreExte
        
        Diff_Buts = Buts_Pour - Buts_Contre
        
        Points = int(TeamWins*3 + TeamDraws)
        results.append([t,Points, nbMatchs, TeamWins, TeamDraws, TeamLosses, Buts_Pour, Buts_Contre, Diff_Buts])

        classement, taillechp = Classementdefault()

        
        # Mpourcentage = [TeamWins, TeamLosses, TeamDraws]
        # labels = 'Victoires', 'Défaites', 'Matchs Nuls'
        # colors = ['#00FFFF','#0000FF', '#3366FF']
        # explode = (0.15, 0, 0)
        # plt.pie(Mpourcentage, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=165)
        # plt.title("Statistiques de " + t)
        # plt.legend(labels, title="Résultats", loc="center right", bbox_to_anchor = (1.15, 0.4))
        # plotsavepath = f"temp/plot{t}.png"
        # plt.savefig(plotsavepath)
        # # plt.show()
        # plt.close()
        
        fig, ax = plt.subplots(figsize=(22, ((nbMatchs+4)/3))) # set size frame
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
        if chp != 'DNK' and chp != 'ARG' and chp != 'BRA' and chp != 'SWZ' and chp != 'MEX' and chp != 'IRL' and chp != 'USA' and chp != 'RUS' and chp != 'CHN'and chp != 'JPN'and chp != 'AUT' and chp != 'SWE' and chp != 'NOR' and chp != 'ROU' and chp != 'POL' :
            print(dfFull)
            print(len(dfFull.columns))
            tabla = table(ax, dfFull, loc='upper center', colWidths=[0.10225]*len(dfFull.columns))
        else:
            tabla = table(ax, dfPartial, loc='upper center', colWidths=[0.10225]*len(dfPartial.columns))
        tabla.auto_set_font_size(False) # Activate set fontsize manually
        tabla.set_fontsize(12) # if ++fontsize is necessary ++colWidths
        tabla.scale(1.4, 1.8) # change size table
        matchssavepath = f"temp/stats{t}.png"
        plt.savefig(matchssavepath, transparent=True)
        plt.close()

        fig, ax2 = plt.subplots(figsize=(20, taillechp/3.5)) # set size frame
        ax2.xaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        ax2.set_frame_on(False)
        cellcol=[['#FFCC99' if classement['TEAM'].iloc[i]==team else 'white' for j in range(len(classement.columns))] for i in range(taillechp)]
        clst = table(ax2, classement, loc='upper center', colWidths=[0.1]*len(classement.columns),cellColours=cellcol)
        clst.auto_set_font_size(False)
        clst.set_fontsize(12)
        clst.scale(1.25, 1.3)
        clstsavepath = f"temp/classement{t}.png"
        plt.savefig(clstsavepath, transparent=True)
        plt.close()
        
        doctitle = ("Statistiques de " +t)
        doc = SimpleDocTemplate(f"saves/{doctitle}.pdf",pagesize=letter,rightMargin=72,leftMargin=72,topMargin=18,bottomMargin=18)
        Story=[]
        
        im = ImReport(imEcusson, 1.5*inch, 1.5*inch)
        Story.append(im)
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        Story.append(Spacer(1, 24))
        ptext = f'<font size="18"> Statistiques du club de {t} après {nbMatchs} journées :</font>'
        story_style = styles["Justify"]
        Story.append(Paragraph(ptext, story_style))
        Story.append(Spacer(1, 32))
        ptext = '<font size="16">------------------- Statistiques à la Fin des Matchs -------------------</font>'
        story_style = styles["Justify"]
        story_style.alignment = 1
        Story.append(Paragraph(ptext, story_style))
        Story.append(Spacer(1, 20))
        
        ptext = (f'<font size="12">{t} a gagné {TeamWins} matchs soit {(TeamWins/nbMatchs)*100.:.2f}% de victoires.<br/>\
                {t} a fait {TeamDraws} matchs nuls soit {(TeamDraws/nbMatchs)*100.:.2f}% de matchs nuls.<br/>\
                {t} a perdu {TeamLosses} matchs soit {(TeamLosses/nbMatchs)*100.:.2f}% de défaites.<br/><br/>\
                {t} a marqué {Buts_Pour} buts depuis le début de saison.<br/>\
                {t} a concédé {Buts_Contre} buts depuis le début de saison.<br/>\
                {t} a ainsi une différence de {Diff_Buts} buts depuis le début de saison.<br/><br/>\
                {t} a une moyenne de {(Buts_Pour/nbMatchs):.1f} buts marqués par match.<br/>\
                {t} a une moyenne de {(Buts_Contre/nbMatchs):.1f} buts concédés par match.</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))
        
        if chp != 'DNK' and chp != 'ARG' and chp != 'BRA' and chp != 'SWZ' and chp != 'MEX' and chp != 'IRL' and chp != 'USA' and chp != 'RUS' and chp != 'CHN'and chp != 'JPN'and chp != 'AUT' and chp != 'SWE' and chp != 'NOR' and chp != 'ROU' and chp != 'POL' :
            Story.append(Spacer(1, 24))
            ptext = '<font size="16">-------------- Statistiques à la Mi-Temps des Matchs --------------</font>'
            story_style = styles["Justify"]
            story_style.alignment = 1
            Story.append(Paragraph(ptext, story_style))
            Story.append(Spacer(1, 20))
            ptext = (f'<font size="12">{t} a mené lors de {TeamHTWins} rencontres soit {(TeamHTWins/nbMatchs)*100.:.2f} % de victoires à la pause.<br/>\
            {t} faisait match nul {TeamHTDraws} fois soit {(TeamHTDraws/nbMatchs)*100.:.2f} % de matchs nuls à la pause.<br/>\
            {t} a été menée {TeamHTLosses} fois soit {(TeamHTLosses/nbMatchs)*100.:.2f} % de défaites à la pause.<br/>\
            {t} a marqué {(totscoredHT)} buts à la mi-temps soit {(totscoredHT/Buts_Pour)*100.:.2f} % de ses buts totaux.<br/>\
            {t} a concédé {(totconcededHT)} buts à la mi-temps soit {(totconcededHT/Buts_Contre)*100.:.2f} % des buts encaissés totaux.<br/></font>')
            Story.append(Paragraph(ptext, styles["Normal"]))

            Story.append(Spacer(1, 24))
            ptext = '<font size="16">------------------------------- Stats Tirs -------------------------------</font>'
            story_style = styles["Justify"]
            story_style.alignment = 1
            Story.append(Paragraph(ptext, story_style))
            Story.append(Spacer(1, 20))
            ptext = (f'<font size="12">{t} tire en moyenne {(ShotsTot/nbMatchs):.1f} fois au but par match.<br/>\
            {t} cadre en moyenne {(ShotsTargTot/nbMatchs):.1f} tirs par match.<br/>\
            {t} cadre donc {(probTarget)*100:.1f}% de ses tirs.<br/>\
            {t} marque sur {(Buts_Pour/ShotsTot)*100:.1f}% de ses tirs et {(Buts_Pour/ShotsTargTot)*100:.1f}% de ses tirs cadrés.</font>')
            Story.append(Paragraph(ptext, styles["Normal"]))
        
        Story.append(Spacer(1, 24))
        ptext = '<font size="16">------------------------------- Bilan Points -------------------------------</font>'
        story_style = styles["Justify"]
        story_style.alignment = 1
        Story.append(Paragraph(ptext, story_style))
        Story.append(Spacer(1, 20))
        ptext = (f'<font size="12">{t} a ainsi un total de {Points} Points après {nbMatchs} matchs.<br/>\
        Soit une moyenne {(Points/nbMatchs):.2f} points pris par match pour {t}.</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))
        if Points/nbMatchs < 0.9:
            text = "Le bilan est très insuffisant. La situation est alarmante."
        elif Points/nbMatchs >= 0.9 and Points/nbMatchs < 1.15:
            text = "Le bilan est insuffisant. Attention à ne pas sombrer."
        elif Points/nbMatchs >= 1.15 and Points/nbMatchs < 1.48:
            text = "Le bilan est mitigé. Il faut encore faire des efforts."
        elif Points/nbMatchs >= 1.48 and Points/nbMatchs < 1.68:
            text = "Le bilan est globalement satisfaisant. Bonnes performances."
        elif Points/nbMatchs >= 1.68 and Points/nbMatchs < 2:
            text = "Le bilan est très satisfaisant. Il faut continuer ainsi."
        else:
            text = "Le bilan est excellent. Félicitations."
        ptext = (f'<font size="12">{text}</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 30))        
        ptext = ('<font size="10">Données extraites grâce à FOOTBALL DATA<br/>\
            Base de données provenant de : https://www.football-data.co.uk/</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(PageBreak())
        
        Story.append(Spacer(1, 10))
        ptext = f'<font size="16">Matchs joués par {t}</font>'
        story_style = styles["Justify"]
        story_style.alignment = 1
        Story.append(Paragraph(ptext, story_style))
        Story.append(Spacer(1, 6))
        im = ImReport(matchssavepath, 9*inch ,6*inch)
        Story.append(im)
        # Story.append(Spacer(1, 6))
        # im = ImReport(plotsavepath,2.75*inch ,2.75*inch)
        # Story.append(im)
        
        Story.append(Spacer(1, 10))        
        ptext = ('<font size="10">Données extraites grâce à FOOTBALL DATA<br/>\
            Base de données provenant de : https://www.football-data.co.uk/</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(PageBreak())

        
        try :
            if chp != 'DNK' and chp != 'ARG' and chp != 'BRA' and chp != 'SWZ' and chp != 'MEX' and chp != 'IRL' and chp != 'USA' and chp != 'RUS' and chp != 'CHN'and chp != 'JPN'and chp != 'AUT' and chp != 'SWE' and chp != 'NOR' and chp != 'ROU' and chp != 'POL' :
                Story.append(Spacer(1, 78))
                ptext = f'<font size="14">Tirs Cadrés de {t}</font>'
                story_style = styles["Justify"]
                story_style.alignment = 1
                Story.append(Paragraph(ptext, story_style))
                im = ImReport(ratiosavepath, 9*inch ,6*inch)
                Story.append(im)
        
                Story.append(Spacer(1, 2))        
                ptext = ('<font size="10">Données extraites grâce à FOOTBALL DATA<br/>\
                    Base de données provenant de : https://www.football-data.co.uk/</font>')
                Story.append(Paragraph(ptext, styles["Normal"]))
        except: pass
        
        doc.build(Story)
        
        subprocess.Popen([f"saves/{doctitle}.pdf"],shell=True)
        return
    except:
        messagebox.showinfo("Données Indisponibles", f"Désolé, nous n'avons pas les données\n nécessaires pour {t}.", parent = fenetre_stats)
