# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 21:21:04 2020

@author: benja
"""


# %%
#@title Import { display-mode: "form" }
import os
import numpy as np
import pandas as pd
import sqlite3
import tensorflow as tf
import tensorflow_probability as tfp

tfk = tf.keras
tfkl = tf.keras.layers
tfpl = tfp.layers
tfd = tfp.distributions
tfm = tf.math

from tensorflow.keras.layers import Dense
#
from pathlib import Path
dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
# %%
# dictpostes = {'Buteur':['LS','ST','RS'],'Attaquant':['LW','LF','CF','RF','RW'],
#             'Milieu Offensif':['LAM','CAM','RAM'],'Milieu':['LM','LCM','CM','RCM','RM'],
#             'Milieu Défensif':['LWB','LDM','CDM','RDM','RWB'],
#             'Défenseur':['LB','LCB','CB','RCB','RB'],'Gardien':['GK']}
conn = sqlite3.connect(dir_path /'databases/alldata.db')
cursor = conn.execute('select * from Players')
all_columns = list(map(lambda x: x[0], cursor.description))
column_to_remove_list = ['ID', 'Name', 'Age', 'OVA', 'Nationality', 'Club', 'BOV', 'BP', 'Position', 'PlayerPhoto', 
                        'ClubLogo', 'FlagPhoto', 'Team&Contract', 'Height', 'Weight', 'foot', 'Joined', 
                        'LoanDateEnd', 'Value', 'Wage', 'ReleaseClause', 'Contract','Attacking','Skill','Movement',
                        'Power','Mentality','Defending','Goalkeeping','A/W','D/W','Hits',
                        'BaseStats','TotalStats','team_jersey_number','TruePlayer','TITU','championnat']#'SM','WF','IR',
columns = list(set(all_columns) - set(column_to_remove_list))
columns = sorted(columns)
print(columns)
# exit()
sql_sel = '''SELECT *
                    FROM Players   
                    WHERE TITU IS NOT NULL AND TruePlayer = 0'''
#!!! COLONNES DONT IL FAUT DETERMINER LA VALEUR ENTRE 0 ET 100
df = pd.read_sql(sql_sel, conn)[columns] #, columns=columns
conn.close()
for col in columns:
    try:
        df[col] = df[col].str.split('+').str[0].astype(float)#*.01
    except:
        # db[col] = db[col]*.01
        pass
for col in ['WF','IR','SM']:
     df[col] = df[col].str.rsplit('★',1).str[0].astype(float)
df = df.sample(frac=1)
colsg= ['GK','LAM', 'LB', 'LCB', 'LCM', 'LDM', 'LF', 'LM', 'LS', 'LW', 'LWB',
'RAM', 'RB', 'RCB', 'RCM', 'RDM', 'RF', 'RM', 'RS', 'RW', 'RWB','CAM', 'CB', 
'CDM', 'CF', 'CM','ST']
# dg = df[:,colsg]
# print(dg)
# print(dg)
# for i in range(10):
#     x = dg.iloc[i].values.astype('i')
#     y = np.bincount(x)
#     ii = np.nonzero(y)[0]
#     group = list(map(lambda v : np.array(colsg)[x==v].tolist(), ii))
#     print(group)
# exit()
dict_ = {"0":['GK'], "1":['LCB', 'RCB', 'CB'], "2":['LB', 'RB'], "3":['LWB', 'RWB'],
"4":['LDM', 'RDM', 'CDM'],"5":['LCM', 'RCM', 'CM'], "6":['LM', 'RM'], "7":['LW', 'RW'],
"8":['LAM', 'RAM', 'CAM'], "9":['LF', 'RF', 'CF'], "10":['LS', 'RS', 'ST']}
invert_dict_ = {}
for key in dict_:
    for val in dict_[key]:
        invert_dict_[val] = int(key)
# print(invert_dict_)
category = np.zeros(len(df))
score = np.zeros(len(df))
dg = df[colsg]
for i in range(len(df)):
    argmax = dg.iloc[i].values.argmax()
    score[i] = dg.iloc[i,argmax]
    category[i]=invert_dict_[colsg[argmax]]
    # print(invert_dict_[str(colsg[])])
df["category"]=category.astype('i')
df["score"]=score.astype('i')
# print(df[['WF','SM','IR']])
df[['WF','SM','IR']] = df[['WF','SM','IR']].values*20.
# print(df)
print(df[colsg+['category','score']])
# %%
dataset = tf.convert_to_tensor(df.values[:,:-2]*.0099+1e-6)
info = tf.convert_to_tensor(df.values[:,-2:])
label = tf.cast(tf.one_hot(tf.cast(info[:,0],tf.int32),len(dict_)), tf.float64)
cond = tf.concat([label,info[:,1:]*.01],-1)
# print(tf.slice(train_dataset,[0,0,0],[1,1,3]))
#
# %%
input_shape = len(columns)#datasets_info.features['image'].shape
encoded_size = 4
label_size = len(dict_)+1
# %%
prior = tfd.Independent(tfd.Normal(loc=tf.zeros(encoded_size,1), scale=1),
                        reinterpreted_batch_ndims=1)
# %%
def IndependentBeta(a,b):
    return tfd.Independent(tfd.Kumaraswamy(concentration0=tfm.exp(b)+2.,#Kumaraswamy
                                    concentration1=tfm.exp(a)+2.),
                           reinterpreted_batch_ndims=1)
# def IndependentTruncNormal(loc,scale):
#     return tfd.Independent(tfd.TruncatedNormal(loc=loc,
#                                     scale=scale, low=-.5,high=.5),
#                            reinterpreted_batch_ndims=1)
def make_encoder(label_size=0, length = 256, activation = 'relu'):
    x = tfkl.Input(input_shape,)
    cond = tfkl.Input(label_size,)
    x_cond = tfkl.Concatenate(-1)([x,cond]) 
    h_q = tfkl.Dense(length, activation=activation)(x_cond)
    h_q = tfkl.Dense(length>>1, activation=activation)(h_q)
    h_q = tfkl.Dense(length>>2, activation=activation)(h_q)
    h_q = tfkl.Dense(length>>3, activation=activation)(h_q)
    out_q = tfkl.Dense(tfpl.MultivariateNormalTriL.params_size(encoded_size), activation=None)(h_q)
    outputs = tfpl.MultivariateNormalTriL(encoded_size,
            activity_regularizer=tfpl.KLDivergenceRegularizer(prior, weight=1))(out_q)
    return tfk.Model(inputs=[x,cond], outputs = outputs)
#
def make_decoder(label_size=0, length = 256, activation = 'relu'):
    z = tfkl.Input(encoded_size,)
    cond = tfkl.Input(label_size,)
    z_cond = tfkl.Concatenate(-1)([z,cond]) 
    h_p = tfkl.Dense(length>>3, activation=activation)(z_cond)
    h_p = tfkl.Dense(length>>2, activation=activation)(h_p)
    h_p = tfkl.Dense(length>>1, activation=activation)(h_p)
    h_p = tfkl.Dense(length, activation=activation)(h_p)
    out_p = tfkl.Dense(input_shape+input_shape, activation=None)(h_p)
    outputs = tfpl.DistributionLambda(lambda t:  IndependentBeta(a=t[...,:input_shape], b=t[...,input_shape:]))(out_p)
    return tfk.Model(inputs=[z,cond], outputs = outputs)

# %%
encoder = make_encoder(activation = 'swish', length = 512, label_size=label_size)
decoder = make_decoder(activation = 'swish', length = 512, label_size=label_size)
print(encoder.summary())
print(decoder.summary())
def make_cvae():
    x = tfkl.Input(input_shape,)
    cond = tfkl.Input(label_size,)
    z = encoder([x,cond])
    xout = decoder([z,cond])
    return tfk.Model(inputs = [x,cond], outputs = xout)

cvae = make_cvae()
print(cvae.summary())
#
negloglik = lambda x, rv_x: -rv_x.log_prob(x)
cvae.compile(optimizer=tf.optimizers.Adam(learning_rate=3e-4), loss=negloglik)
# %%
# # #### Do inference.
_ = cvae.fit([dataset,cond],dataset, epochs=100)
#
# print(dataset[:2])
# print(cvae([dataset[:2],cond[:2]]).mean().numpy())
zc = encoder([dataset,cond]).sample().numpy()
print(f"code mean {np.mean(zc,axis=0)} std {np.std(zc,axis=0)}")

# %%
# Now, let's generate ten never-before-seen players.
nsamp = 20
level = .85
#
for cat in range(len(dict_)):
    print(f"***** {dict_[str(cat)]} *****")
    hot_cat = tf.tile([tf.one_hot(cat,len(dict_))],[nsamp,1])
    score =  tf.tile([[level]],[nsamp,1])
    code=prior.sample(nsamp)
    player_info = tf.concat([hot_cat,score],-1)
    code = code.numpy()
    player_info = player_info.numpy()
    dist_player = decoder([code, player_info])
    assert isinstance(dist_player, tfd.Distribution)
    player_gen = (100*(dist_player.mean())).numpy().astype('i')
    df_gen = pd.DataFrame(player_gen, columns = columns)
    df_gen[['WF','SM','IR']] = df_gen[['WF','SM','IR']]*0.05
    print(df_gen[colsg])
# %%
# save model
cvae.save(dir_path / "models/player_model/Players_CVAE_model.h5")
decoder.save(dir_path / "models/player_model/Players_CVAE_decoder.h5")