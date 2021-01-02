# %%
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.constraints import MaxNorm
# Helper libraries
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from fuzzywuzzy import process
# from learn_db import build_match_features, build_database, build_all_database
l1 = ['E0','E1','E2','B1','F1','SC0','SP1','P1','T1','N1','D1','I1']
# l2 = ['SP2','D2','F2','SC1','G1']
ls = ['ARG','AUT','BRA','SWZ','MEX','IRL','USA','RUS','SWE','CHN','DNK','NOR','ROU','POL','AUT','JPN']
pd.set_option('mode.chained_assignment', None)
# %%
def build_match_features(chpt, hometeam, awayteam, short=4):
    path = os.path.dirname(os.path.abspath(__file__))
    loc="databases/csv"
    data_path = os.path.join(path,loc)
    db_keys = []
    dict_keys = {}
    for file in os.listdir(data_path):
        if file.startswith(chpt):
            key=os.path.splitext(file)[0]
            dict_keys[key] = os.path.join(data_path, file)#pd.read_csv(os.path.join(data_path, file))
            db_keys.append(key)
    db_keys=sorted(db_keys)
    key = db_keys[-1]
    
    columns_req = ['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR']
    df = pd.read_csv(dict_keys[key])
    
    for k in ls:
        if k in key:
            df = df.rename(columns={'Home': 'HomeTeam', 'Away' : 'AwayTeam', 'HG' : 'FTHG', 'AG' : 'FTAG', 'Res': 'FTR'})
            break
    
    db = df[columns_req]
    teams = db['HomeTeam'].unique()
    hometeam = process.extractOne(hometeam, teams)[0]
    awayteam = process.extractOne(awayteam, teams)[0]
    # print(f"{hometeam} vs {awayteam} :")
    teams_db = {}
    teams = [hometeam,awayteam]
    dc_last={}
    # nb_teams = len(teams)
    for t in teams:
        dt = db[np.logical_or(db['HomeTeam']==t,db['AwayTeam']==t)]
        # print(key,t)
        ht = (dt['HomeTeam']==t).values
        at = (dt['AwayTeam']==t).values
        ################### long term ********************
        HGS=np.cumsum(dt['FTHG'].values*ht) #total ft home goals scored
        AGS=np.cumsum(dt['FTAG'].values*at) #total ft away goals scored
        TGS=HGS+AGS
        HGC=np.cumsum(dt['FTAG'].values*ht) #total ft home goals conceded
        AGC=np.cumsum(dt['FTHG'].values*at) #total ft away goals conceded
        TGC=HGC+AGC #total goals conceded
        HP=np.cumsum(((dt['FTR']=='H').values*3+(dt['FTR']=='D').values)*ht) #total points home
        AP=np.cumsum(((dt['FTR']=='A').values*3+(dt['FTR']=='D').values)*at) #total points away
        TP=HP+AP
        norm=np.arange(len(dt))+1.
        normh=np.cumsum(ht)
        norma=np.cumsum(at)
        TPL = TP/norm
        HPL = HP/(normh+1e-12)
        APL = AP/(norma+1e-12)
        TGSL = TGS/norm
        HGSL = HGS/(normh+1e-12)
        AGSL = AGS/(norma+1e-12)
        TGCL = TGC/norm
        HGCL = HGC/(normh+1e-12)
        AGCL = AGC/(norma+1e-12)
        ################ short term *********************
        norms = norm-np.r_[np.zeros(short),norm[:-short]]
        normhs = normh-np.r_[np.zeros(short),normh[:-short]]
        normas = norma-np.r_[np.zeros(short),norma[:-short]]
        TPS = (TP-np.r_[np.zeros(short),TP[:-short]])/(norms+1e-12)
        HPS =  (HP-np.r_[np.zeros(short),HP[:-short]])/(normhs+1e-12)
        APS =  (AP-np.r_[np.zeros(short),AP[:-short]])/(normas+1e-12)
        TGSS = (TGS-np.r_[np.zeros(short),TGS[:-short]])/(norms+1e-12)
        HGSS = (HGS-np.r_[np.zeros(short),HGS[:-short]])/(normhs+1e-12)
        AGSS = (AGS-np.r_[np.zeros(short),AGS[:-short]])/(normas+1e-12)
        TGCS = (TGC-np.r_[np.zeros(short),TGC[:-short]])/(norms+1e-12)
        HGCS = (HGC-np.r_[np.zeros(short),HGC[:-short]])/(normhs+1e-12)
        AGCS = (AGC-np.r_[np.zeros(short),AGC[:-short]])/(normas+1e-12)
        ################################################
        dc_last[t] = {'TPL':TPL[-1],'HPL':HPL[-1],'APL':APL[-1], 'TGSL':TGSL[-1],'HGSL':HGSL[-1],'AGSL':AGSL[-1],'TGCL':TGCL[-1],'HGCL':HGCL[-1],'AGCL':AGCL[-1],
            'TPS':TPS[-1],'HPS':HPS[-1],'APS':APS[-1], 'TGSS':TGSS[-1],'HGSS':HGSS[-1],'AGSS':AGSS[-1],'TGCS':TGCS[-1],'HGCS':HGCS[-1],'AGCS':AGCS[-1]}
        # teams_transit[key][t] = dc_last
        ################################################
        # print(list(enumerate(df['HomeTeam'])))
    cols = ['HPL','APL', 'HTPL','ATPL','HGSL','AGSL','HTGSL','ATGSL','HGCL','AGCL','HTGCL','ATGCL',
    'HPS','APS', 'HTPS','ATPS','HGSS','AGSS','HTGSS','ATGSS','HGCS','AGCS','HTGCS','ATGCS']
    df = pd.DataFrame([np.zeros(len(cols))], columns=cols)
    df['HPL']=dc_last[hometeam]['HPL'] #list(map(lambda i,t: teams_db[t].loc[i,'HPL'],np.arange(len(df)),df['HomeTeam'].values))
    df['APL']=dc_last[awayteam]['APL'] #list(map(lambda i,t: teams_db[t].loc[i,'APL'],np.arange(len(df)),df['AwayTeam'].values))
    df['HTPL']=dc_last[hometeam]['TPL'] #list(map(lambda i,t: teams_db[t].loc[i,'TPL'],np.arange(len(df)),df['HomeTeam'].values))
    df['ATPL']=dc_last[awayteam]['TPL']#list(map(lambda i,t: teams_db[t].loc[i,'TPL'],np.arange(len(df)),df['AwayTeam'].values))
        # #
    df['HGSL']=dc_last[hometeam]['HGSL']#list(map(lambda i,t: teams_db[t].loc[i,'HGSL'],np.arange(len(df)),df['HomeTeam'].values))
    df['AGSL']=dc_last[awayteam]['AGSL']#list(map(lambda i,t: teams_db[t].loc[i,'AGSL'],np.arange(len(df)),df['AwayTeam'].values))
    df['HTGSL']=dc_last[hometeam]['TGSL']#list(map(lambda i,t: teams_db[t].loc[i,'TGSL'],np.arange(len(df)),df['HomeTeam'].values))
    df['ATGSL']=dc_last[awayteam]['TGSL']#list(map(lambda i,t: teams_db[t].loc[i,'TGSL'],np.arange(len(df)),df['AwayTeam'].values))
        #
    df['HGCL']=dc_last[hometeam]['HGCL']#list(map(lambda i,t: teams_db[t].loc[i,'HGCL'],np.arange(len(df)),df['HomeTeam'].values))
    df['AGCL']=dc_last[awayteam]['AGCL']#list(map(lambda i,t: teams_db[t].loc[i,'AGCL'],np.arange(len(df)),df['AwayTeam'].values))
    df['HTGCL']=dc_last[hometeam]['TGCL']#ist(map(lambda i,t: teams_db[t].loc[i,'TGCL'],np.arange(len(df)),df['HomeTeam'].values))
    df['ATGCL']=dc_last[awayteam]['TGCL']#list(map(lambda i,t: teams_db[t].loc[i,'TGCL'],np.arange(len(df)),df['AwayTeam'].values))
        #    
    df['HPS']=dc_last[hometeam]['HPS'] #list(map(lambda i,t: teams_db[t].loc[i,'HPL'],np.arange(len(df)),df['HomeTeam'].values))
    df['APS']=dc_last[awayteam]['APS'] #list(map(lambda i,t: teams_db[t].loc[i,'APL'],np.arange(len(df)),df['AwayTeam'].values))
    df['HTPS']=dc_last[hometeam]['TPS'] #list(map(lambda i,t: teams_db[t].loc[i,'TPL'],np.arange(len(df)),df['HomeTeam'].values))
    df['ATPS']=dc_last[awayteam]['TPS']#list(map(lambda i,t: teams_db[t].loc[i,'TPL'],np.arange(len(df)),df['AwayTeam'].values))
        # #
    df['HGSS']=dc_last[hometeam]['HGSS']#list(map(lambda i,t: teams_db[t].loc[i,'HGSL'],np.arange(len(df)),df['HomeTeam'].values))
    df['AGSS']=dc_last[awayteam]['AGSS']#list(map(lambda i,t: teams_db[t].loc[i,'AGSL'],np.arange(len(df)),df['AwayTeam'].values))
    df['HTGSS']=dc_last[hometeam]['TGSS']#list(map(lambda i,t: teams_db[t].loc[i,'TGSL'],np.arange(len(df)),df['HomeTeam'].values))
    df['ATGSS']=dc_last[awayteam]['TGSS']#list(map(lambda i,t: teams_db[t].loc[i,'TGSL'],np.arange(len(df)),df['AwayTeam'].values))
        #
    df['HGCS']=dc_last[hometeam]['HGCS']#list(map(lambda i,t: teams_db[t].loc[i,'HGCL'],np.arange(len(df)),df['HomeTeam'].values))
    df['AGCS']=dc_last[awayteam]['AGCS']#list(map(lambda i,t: teams_db[t].loc[i,'AGCL'],np.arange(len(df)),df['AwayTeam'].values))
    df['HTGCS']=dc_last[hometeam]['TGCS']#ist(map(lambda i,t: teams_db[t].loc[i,'TGCL'],np.arange(len(df)),df['HomeTeam'].values))
    df['ATGCS']=dc_last[awayteam]['TGCS']#list(map(lambda i,t: teams_db[t].loc[i,'TGCL'],np.arange(len(df)),df['AwayTeam'].values))
    # print(df)
    return df

def build_database(chpt, short, train_ratio):
    # chpt = 'E0'
    path = os.path.dirname(os.path.abspath(__file__))
    loc="databases/csv"
    data_path = os.path.join(path,loc)
    dict_db = {}
    db_keys = []
    for file in os.listdir(data_path):
        if file.startswith(chpt):
            key=os.path.splitext(file)[0]
            # print(key)
            dict_db[key] = pd.read_csv(os.path.join(data_path, file))
            db_keys.append(key)
    db_keys=sorted(db_keys)
    print(db_keys)

    columns_req = ['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR']
    # short = 5
    dfl=[]
    teams_transit = {}
    prkey = ""
    for key in db_keys:
        db = dict_db[key]
        for k in ls:
            if k in key:
                db = db.rename(columns={'Home': 'HomeTeam', 'Away' : 'AwayTeam', 'HG' : 'FTHG', 'AG' : 'FTAG', 'Res': 'FTR'})
                break
        df = db[columns_req]
        teams_db = {}
        teams = sorted(df['HomeTeam'].unique())
        nb_teams = len(teams)
        print(key)
        teams_transit[key] = {}
        for t in teams:
            dt = df[np.logical_or(df['HomeTeam']==t,df['AwayTeam']==t)]
            # print(key,t)
            ht = (dt['HomeTeam']==t).values
            at = (dt['AwayTeam']==t).values
            ################### long term ********************
            HGS=np.cumsum(dt['FTHG'].values*ht)
            AGS=np.cumsum(dt['FTAG'].values*at)
            TGS=HGS+AGS
            HGC=np.cumsum(dt['FTAG'].values*ht)
            AGC=np.cumsum(dt['FTHG'].values*at)
            TGC=HGC+AGC
            HP=np.cumsum(((dt['FTR']=='H').values*3+(dt['FTR']=='D').values)*ht)
            AP=np.cumsum(((dt['FTR']=='A').values*3+(dt['FTR']=='D').values)*at)
            TP=HP+AP
            norm=np.arange(len(dt))+1.
            normh=np.cumsum(ht)
            norma=np.cumsum(at)
            TPL = TP/norm
            HPL = HP/(normh+1e-12)
            APL = AP/(norma+1e-12)
            TGSL = TGS/norm
            HGSL = HGS/(normh+1e-12)
            AGSL = AGS/(norma+1e-12)
            TGCL = TGC/norm
            HGCL = HGC/(normh+1e-12)
            AGCL = AGC/(norma+1e-12)
            ################ short term *********************
            norms = norm-np.r_[np.zeros(short),norm[:-short]]
            normhs = normh-np.r_[np.zeros(short),normh[:-short]]
            normas = norma-np.r_[np.zeros(short),norma[:-short]]
            TPS = (TP-np.r_[np.zeros(short),TP[:-short]])/(norms+1e-12)
            HPS =  (HP-np.r_[np.zeros(short),HP[:-short]])/(normhs+1e-12)
            APS =  (AP-np.r_[np.zeros(short),AP[:-short]])/(normas+1e-12)
            TGSS = (TGS-np.r_[np.zeros(short),TGS[:-short]])/(norms+1e-12)
            HGSS = (HGS-np.r_[np.zeros(short),HGS[:-short]])/(normhs+1e-12)
            AGSS = (AGS-np.r_[np.zeros(short),AGS[:-short]])/(normas+1e-12)
            TGCS = (TGC-np.r_[np.zeros(short),TGC[:-short]])/(norms+1e-12)
            HGCS = (HGC-np.r_[np.zeros(short),HGC[:-short]])/(normhs+1e-12)
            AGCS = (AGC-np.r_[np.zeros(short),AGC[:-short]])/(normas+1e-12)
            ################################################
            if prkey in teams_transit.keys() and t in teams_transit[prkey].keys():
                dc_first = teams_transit[prkey][t]
                # print('transit', key, prkey,t,dc_first)
            else:
                dc_first = {'TPL':0,'HPL':0,'APL':0, 'TGSL':0,'HGSL':0,'AGSL':0,'TGCL':0,'HGCL':0,'AGCL':0,
                'TPS':0,'HPS':0,'APS':0, 'TGSS':0,'HGSS':0,'AGSS':0,'TGCS':0,'HGCS':0,'AGCS':0}
            dc_last = {'TPL':TPL[-1],'HPL':HPL[-1],'APL':APL[-1], 'TGSL':TGSL[-1],'HGSL':HGSL[-1],'AGSL':AGSL[-1],'TGCL':TGCL[-1],'HGCL':HGCL[-1],'AGCL':AGCL[-1],
                'TPS':TPS[-1],'HPS':HPS[-1],'APS':APS[-1], 'TGSS':TGSS[-1],'HGSS':HGSS[-1],'AGSS':AGSS[-1],'TGCS':TGCS[-1],'HGCS':HGCS[-1],'AGCS':AGCS[-1]}
            teams_transit[key][t] = dc_last
            ################################################
            dt['TPL']=np.r_[dc_first['TPL'],TPL[:-1]]
            dt['HPL']=np.r_[dc_first['HPL'],HPL[:-1]]
            dt['APL']=np.r_[dc_first['APL'],APL[:-1]]
            dt['TGSL'] = np.r_[dc_first['TGSL'],TGSL[:-1]]
            dt['HGSL'] = np.r_[dc_first['HGSL'],HGSL[:-1]]
            dt['AGSL'] = np.r_[dc_first['AGSL'],AGSL[:-1]]
            dt['TGCL'] = np.r_[dc_first['TGCL'],TGCL[:-1]]
            dt['HGCL'] = np.r_[dc_first['HGCL'],HGCL[:-1]]
            dt['AGCL'] = np.r_[dc_first['AGCL'],AGCL[:-1]]
            #
            dt['TPS'] = np.r_[dc_first['TPS'],TPS[:-1]]
            dt['HPS'] = np.r_[dc_first['HPS'],HPS[:-1]]
            dt['APS'] = np.r_[dc_first['APS'],APS[:-1]]
            dt['TGSS'] = np.r_[dc_first['TGSS'],TGSS[:-1]]
            dt['HGSS'] = np.r_[dc_first['HGSS'],HGSS[:-1]]
            dt['AGSS'] = np.r_[dc_first['AGSS'],AGSS[:-1]]
            dt['TGCS'] = np.r_[dc_first['TGCS'],TGCS[:-1]]
            dt['HGCS'] = np.r_[dc_first['HGCS'],HGCS[:-1]]
            dt['AGCS'] = np.r_[dc_first['AGCS'],AGCS[:-1]]
            #
            teams_db[t] = dt
            # print(teams_db[t].index)
        # print(list(enumerate(df['HomeTeam'])))
        df['HPL']=list(map(lambda i,t: teams_db[t].loc[i,'HPL'],np.arange(len(df)),df['HomeTeam'].values))
        df['APL']=list(map(lambda i,t: teams_db[t].loc[i,'APL'],np.arange(len(df)),df['AwayTeam'].values))
        df['HTPL']=list(map(lambda i,t: teams_db[t].loc[i,'TPL'],np.arange(len(df)),df['HomeTeam'].values))
        df['ATPL']=list(map(lambda i,t: teams_db[t].loc[i,'TPL'],np.arange(len(df)),df['AwayTeam'].values))
        # #
        df['HGSL']=list(map(lambda i,t: teams_db[t].loc[i,'HGSL'],np.arange(len(df)),df['HomeTeam'].values))
        df['AGSL']=list(map(lambda i,t: teams_db[t].loc[i,'AGSL'],np.arange(len(df)),df['AwayTeam'].values))
        df['HTGSL']=list(map(lambda i,t: teams_db[t].loc[i,'TGSL'],np.arange(len(df)),df['HomeTeam'].values))
        df['ATGSL']=list(map(lambda i,t: teams_db[t].loc[i,'TGSL'],np.arange(len(df)),df['AwayTeam'].values))
        #
        df['HGCL']=list(map(lambda i,t: teams_db[t].loc[i,'HGCL'],np.arange(len(df)),df['HomeTeam'].values))
        df['AGCL']=list(map(lambda i,t: teams_db[t].loc[i,'AGCL'],np.arange(len(df)),df['AwayTeam'].values))
        df['HTGCL']=list(map(lambda i,t: teams_db[t].loc[i,'TGCL'],np.arange(len(df)),df['HomeTeam'].values))
        df['ATGCL']=list(map(lambda i,t: teams_db[t].loc[i,'TGCL'],np.arange(len(df)),df['AwayTeam'].values))
        #    
        df['HPS']=list(map(lambda i,t: teams_db[t].loc[i,'HPS'],np.arange(len(df)),df['HomeTeam'].values))
        df['APS']=list(map(lambda i,t: teams_db[t].loc[i,'APS'],np.arange(len(df)),df['AwayTeam'].values))
        df['HTPS']=list(map(lambda i,t: teams_db[t].loc[i,'TPS'],np.arange(len(df)),df['HomeTeam'].values))
        df['ATPS']=list(map(lambda i,t: teams_db[t].loc[i,'TPS'],np.arange(len(df)),df['AwayTeam'].values))
        #
        df['HGSS']=list(map(lambda i,t: teams_db[t].loc[i,'HGSS'],np.arange(len(df)),df['HomeTeam'].values))
        df['AGSS']=list(map(lambda i,t: teams_db[t].loc[i,'AGSS'],np.arange(len(df)),df['AwayTeam'].values))
        df['HTGSS']=list(map(lambda i,t: teams_db[t].loc[i,'TGSS'],np.arange(len(df)),df['HomeTeam'].values))
        df['ATGSS']=list(map(lambda i,t: teams_db[t].loc[i,'TGSS'],np.arange(len(df)),df['AwayTeam'].values))
        #
        df['HGCS']=list(map(lambda i,t: teams_db[t].loc[i,'HGCS'],np.arange(len(df)),df['HomeTeam'].values))
        df['AGCS']=list(map(lambda i,t: teams_db[t].loc[i,'AGCS'],np.arange(len(df)),df['AwayTeam'].values))
        df['HTGCS']=list(map(lambda i,t: teams_db[t].loc[i,'TGCS'],np.arange(len(df)),df['HomeTeam'].values))
        df['ATGCS']=list(map(lambda i,t: teams_db[t].loc[i,'TGCS'],np.arange(len(df)),df['AwayTeam'].values))
        #
        # df['HW']=(df['FTR']=='H').values.astype('i')
        # df['D']=(df['FTR']=='D').values.astype('i')
        # df['AW']=(df['FTR']=='A').values.astype('i')
        df['FTR'] = (df['FTR']=='A').values.astype('i')*2+(df['FTR']=='D').values.astype('i')
        dfl.append(df)
        prkey = key

    # %%
    db=pd.concat(dfl, ignore_index=True)
    db=db.drop(['Date','HomeTeam','AwayTeam','FTHG','FTAG'],axis=1)#,'FTR'
    arr = np.arange(len(db))
    np.random.shuffle(arr)
    lratio = int(len(db)*train_ratio)
    idx_train=np.sort(arr[:lratio])
    idx_test=np.sort(arr[lratio:])
    db_train = db.iloc[idx_train]
    db_test = db.iloc[idx_test]
    # db_train = db[:int(len(db)*train_ratio)]
    # db_test = db[int(len(db)*train_ratio):]
    db_train.to_csv(os.path.join(path, "models/prediction/"+ chpt+"_train_dataset.csv"),index=None)
    db_test.to_csv(os.path.join(path, "models/prediction/"+ chpt+"_test_dataset.csv"),index=None)
    print(db_train)
    print(db_test)
# %%
def build_all_database(ll, short, train_ratio):
    path = os.path.dirname(os.path.abspath(__file__))
    dftrain = []
    dftest = []
    for chpt in l1:
        build_database(chpt, short, train_ratio)
        dftrain.append(pd.read_csv(os.path.join(path, "models/prediction/"+ chpt+"_train_dataset.csv")))
        dftest.append(pd.read_csv(os.path.join(path, "models/prediction/"+ chpt+"_test_dataset.csv")))
    db_train=pd.concat(dftrain, ignore_index=True)
    db_train.to_csv(os.path.join(path, "models/prediction/all_train_dataset.csv"),index=None)
    db_test=pd.concat(dftest, ignore_index=True)
    db_test.to_csv(os.path.join(path, "models/prediction/all_test_dataset.csv"),index=None)

# %%
def learn_model(chpt, epoch= 1000):
    path = os.path.dirname(os.path.abspath(__file__))
    # print(tf.__version__)
    # chpt = 'E0'
    class_names = ['HW', 'D', 'AW']
    # %%
    # fashion_mnist = keras.datasets.fashion_mnist
    # (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    train_data=pd.read_csv(os.path.join(path,"models/prediction/"+chpt+"_train_dataset.csv"))
    # print(train_data) #print bien 16646 matchs
    test_data=pd.read_csv(os.path.join(path,"models/prediction/"+chpt+"_test_dataset.csv"))
    # print(test_data) #print bien 1579 matchs
    train_input=train_data.drop('FTR', axis=1).values#train_data.drop(['HW','D','AW'], axis=1).values
    # print(train_input) #print un tableau 882x25
    train_output=train_data['FTR'].values
    # print(train_output) #print un tableau 882x25

    test_input=test_data.drop('FTR', axis=1).values#.drop(['HW','D','AW'], axis=1).values
    test_output=test_data['FTR'].values

    # %%
    model = keras.Sequential([
        keras.layers.Dropout(0.25),
        keras.layers.Dense(train_input.shape[1]<<1, activation='relu', kernel_constraint=MaxNorm(3)),
        keras.layers.Dropout(0.25),
        # keras.layers.Dense(train_input.shape[1], activation='relu', kernel_constraint=MaxNorm(3)),
        # keras.layers.Dropout(0.25),
        keras.layers.Dense(train_input.shape[1]>>1, activation='relu', kernel_constraint=MaxNorm(3)),
        keras.layers.Dense(8, activation='relu'),
        keras.layers.Dense(4, activation='relu'),
        keras.layers.Dense(3)
    ])

    # %%
    # lstm_out = 256
    # timestep = 1
    # ltrain=(train_input.shape[0]//timestep)*timestep
    # ltest=(test_input.shape[0]//timestep)*timestep
    # train_input=train_input[:ltrain,:].reshape(train_input.shape[0]//timestep, timestep, train_input.shape[1])
    # test_input=test_input[:ltest,:].reshape(test_input.shape[0]//timestep, timestep, test_input.shape[1])
    # train_output=train_output[:ltrain]
    # test_output=test_output[:ltest]
    # model = keras.Sequential()
    # model.add(keras.layers.LSTM(lstm_out, return_sequences = True, input_shape = (timestep,train_input.shape[-1])))
    # model.add(keras.layers.Dropout(0.2))

    # model.add(keras.layers.LSTM(lstm_out, return_sequences = True))
    # model.add(keras.layers.Dropout(0.2))
    # model.add(keras.layers.LSTM(lstm_out, return_sequences = True, input_shape = (timestep,train_input.shape[-1])))
    # model.add(keras.layers.Dropout(0.2))

    # model.add(keras.layers.LSTM(lstm_out, return_sequences = True))
    # model.add(keras.layers.Dropout(0.2))

    # # model.add(keras.layers.LSTM(units = 50, return_sequences = True))
    # # model.add(keras.layers.Dropout(0.2))

    # # model.add(keras.layers.LSTM(units = 50))
    # # model.add(keras.layers.Dropout(0.2))

    # # model.add(keras.layers.Embedding(64, embed_dim,input_length = train_input.shape[1]))
    # # model.add(keras.layers.LSTM(lstm_out, input_shape=(1, 1)))
    # # model.add(keras.layers.LSTM(lstm_out))
    # model.add(keras.layers.Dense(3,activation='softmax'))
    # %%
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=5.e-3),
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

    # %%
    model.fit(x=train_input, y=train_output, batch_size = len(train_data), epochs=epoch)
    model.summary()
    model.save(os.path.join(path,"models/prediction/"+chpt+"_model.h5"))

    # %%
    test_loss, test_acc = model.evaluate(test_input,  test_output, verbose=2)
    print('\nTest accuracy:', test_acc)
    # %%
    probability_model = tf.keras.Sequential([model, 
                                            tf.keras.layers.Softmax()])
    predictions = probability_model.predict(test_input)
    # %%
    # test_output[0]
    test_res=list(map(lambda i: class_names[i],test_output))
    
    return(test_acc)
    # for i in range(len(test_res)):
    #     print(f"p H = {predictions[i][0]:.2f}, p D =  {predictions[i][1]:.2f}, p A =  {predictions[i][2]:.2f} - Result = {test_res[i]}")
    # one_input = build_match_features('E0','Liverpool','Watford',4).values
    # one_prediction = probability_model.predict(one_input)
    # print(one_prediction)
    # one_input = build_match_features('E0','Watford','Liverpool',4).values
    # one_prediction = probability_model.predict(one_input)
    # print(one_prediction)
# %%
# build_database('E0', 4, .95)
# learn_model('E0')
# build_all_database(l1, 4, .95)
# learn_model('all')