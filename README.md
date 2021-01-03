# Football-Manag-Air-IPSA-GP211

> **ATTENTION : Ce programme nécessite 'tensorflow probability', cette librairire peut abîmer ou détruire votre installation python. Il est préférable de créer un environnement spécifique au préalable.**

Football Manag'Air en 5 points c'est :

[a] Une VAE qui crée des joueurs de football réalistes

[x] Un système de transfert

[v] La prédiction des résultats des matchs à venir

[] Des fiches statistiques sur des centaines d'équipes

[] Des statistiques sur des milliers de joueurs



## Résumé

Le programme « Football Manag’Air » (FM) est une version 2.0 de « Football Datas » (https://github.com/milnerLFC/FOOTBALL-DATAS-IPSA) qui fut déjà l’année dernière orienté sur l’analyse de données footballistiques et particulièrement sur la prédiction des résultats des futurs matchs. Si cette fonctionnalité a été réintroduite cette année, ce n’est pas le but premier de ce projet. L’objectif premier de FM est de générer de nouveaux joueurs aux statistiques réalistes et donc fidèles à celles de FIFA sur le principe de la VAE afin d’alimenter une base de données accessible via SQL3. Les données exploitées permettent une approche précise du niveau des joueurs et ainsi d’au mieux définir de futurs transferts pour améliorer la qualité d’une équipe. Un autre défi était de trouver une bonne approche pour disséquer l’effectif et en faire ressortir les caractéristiques les plus importantes.
Un objectif secondaire de ce projet était de rendre l’interface tkinter basiquement statique plus dynamique afin de rendre l’expérience plus agréable pour l’utilisateur et lui offrir une meilleure immersion.

### Mots clés : VAE – Prédiction – Base de Données – Dynamisme – Statistiques


## Sum-Up

The new “Football Manag’Air” program (FM) is a 2.0 version of “Football Data” (https://github.com/milnerLFC/FOOTBALL-DATAS-IPSA) which was already oriented on football data analysis last year and in particular on football match results prediction. If this functionality is once again accessible, it is not the first goal of this project. The main objective of FM is to generate new football players with realistic statistics that are close to the ones made by FIFA games to supply a database of true football players accessible with SQL3. The different data offer a precise approach of the true level of the players and then allow people (like us) to find out what are the best possible transfers to improve the quality of a team. Another challenge was to find the best approach to dissect workforces and to bring out the most relevant information.
An auxiliar objective was to make the tkinter’s interface more accessible for everyone with more dynamism than usual to make the experience greater for users and give to them a better immersion.

### Keywords: VAE – Prediction – Databases – Dynamism – Statistics

*Football Datas : https://github.com/milnerLFC/FOOTBALL-DATAS-IPSA*

*Initial Dataset : https://www.kaggle.com/ekrembayar/fifa-21-complete-player-dataset*

# Packages / Librairies

#### Name                    Version                   Build  Channel

absl-py                   0.11.0                   pypi_0    pypi

amply                     0.1.4                      py_0    conda-forge

astroid                   2.4.2                    py38_0

astunparse                1.6.3                    pypi_0    pypi

backcall                  0.2.0                      py_0

blas                      1.0                         mkl

ca-certificates           2020.10.14                    0

cachetools                4.1.1                    pypi_0    pypi

certifi                   2020.11.8        py38haa95532_0

chardet                   3.0.4                    pypi_0    pypi

cloudpickle               1.6.0                    pypi_0    pypi

colorama                  0.4.4                      py_0

cycler                    0.10.0                   py38_0

decorator                 4.4.2                      py_0

dm-tree                   0.1.5                    pypi_0    pypi

docutils                  0.16             py38h9bdc248_2    conda-forge

freetype                  2.10.4               hd328e21_0

fuzzywuzzy                0.18.0             pyhd8ed1ab_0    conda-forge

gast                      0.3.3                    pypi_0    pypi

glpk                      4.65              h8ffe710_1003    conda-forge

google-auth               1.23.0                   pypi_0    pypi

google-auth-oauthlib      0.4.2                    pypi_0    pypi

google-pasta              0.2.0                    pypi_0    pypi

grpcio                    1.34.0                   pypi_0    pypi

h5py                      2.10.0                   pypi_0    pypi

icu                       58.2                 ha925a31_3

idna                      2.10                     pypi_0    pypi

intel-openmp              2020.2                      254

ipython                   7.19.0           py38hd4e2768_0

ipython_genutils          0.2.0              pyhd3eb1b0_1

isort                     5.6.4                      py_0

jedi                      0.17.2           py38haa95532_1

jpeg                      9b                   hb83a4c4_2

keras-preprocessing       1.1.2                    pypi_0    pypi

kiwisolver                1.3.0            py38hd77b12b_0

lazy-object-proxy         1.4.3            py38he774522_0

libpng                    1.6.37               h2a8f88b_0

libtiff                   4.1.0                h56a325e_1

lz4-c                     1.9.2                hf4a77e7_3

markdown                  3.3.3                    pypi_0    pypi

matplotlib                3.3.2                         0

matplotlib-base           3.3.2            py38hba9282a_0

mccabe                    0.6.1                    py38_1

mkl                       2020.2                      256

mkl-service               2.3.0            py38h196d8e1_0

mkl_fft                   1.2.0            py38h45dec08_0

mkl_random                1.1.1            py38h47e9c7a_0

numpy                     1.18.5                   pypi_0    pypi

oauthlib                  3.1.0                    pypi_0    pypi

olefile                   0.46                       py_0

openssl                   1.1.1h               he774522_0

opt-einsum                3.3.0                    pypi_0    pypi

pandas                    1.1.3            py38ha925a31_0

parso                     0.7.0                      py_0

pickleshare               0.7.5           pyhd3eb1b0_1003

pillow                    8.0.1            py38h4fa10fc_0

pip                       20.3             py38haa95532_0

prompt-toolkit            3.0.8                      py_0

protobuf                  3.14.0                   pypi_0    pypi

pulp                      2.3.1            py38h32f6830_0    conda-forge

pyasn1                    0.4.8                    pypi_0    pypi

pyasn1-modules            0.2.8                    pypi_0    pypi

pygame                    2.0.0                    pypi_0    pypi

pygments                  2.7.2              pyhd3eb1b0_0

pylint                    2.6.0                    py38_0

pyparsing                 2.4.7                      py_0

pyqt                      5.9.2            py38ha925a31_4

python                    3.8.5                h5fd99cc_1

python-dateutil           2.8.1                      py_0

python-levenshtein        0.12.0          py38h1e8a9f7_1004    conda-forge

python_abi                3.8                      1_cp38    conda-forge

pytz                      2020.4             pyhd3eb1b0_0

pywin32                   227              py38he774522_1

qt                        5.9.7            vc14h73c81de_0

reportlab                 3.5.51           py38h71be502_0

requests                  2.25.0                   pypi_0    pypi

requests-oauthlib         1.3.0                    pypi_0    pypi

rsa                       4.6                      pypi_0    pypi

setuptools                50.3.2           py38haa95532_2

sip                       4.19.13          py38ha925a31_0

six                       1.15.0           py38haa95532_0

sqlite                    3.33.0               h2a8f88b_0

tensorboard               2.4.0                    pypi_0    pypi

tensorboard-plugin-wit    1.7.0                    pypi_0    pypi

tensorflow                2.3.1                    pypi_0    pypi

tensorflow-estimator      2.3.0                    pypi_0    pypi


tensorflow-probability    0.11.1                   pypi_0    pypi

termcolor                 1.1.0                    pypi_0    pypi

tk                        8.6.10               he774522_0

toml                      0.10.1                     py_0

tornado                   6.1              py38h2bbff1b_0

traitlets                 5.0.5                      py_0

tzdata                    2020d                h14c3975_0

urllib3                   1.26.2                   pypi_0    pypi

vc                        14.1                 h0510ff6_4

vs2015_runtime            14.16.27012          hf0eaf9b_3

wcwidth                   0.2.5                      py_0

werkzeug                  1.0.1                    pypi_0    pypi

wheel                     0.36.0             pyhd3eb1b0_0

wincertstore              0.2                      py38_0

wrapt                     1.11.2           py38he774522_0

xlrd                      1.2.0                      py_0

xlsxwriter                1.3.7                      py_0

xz                        5.2.5                h62dcd97_0

zlib                      1.2.11               h62dcd97_4

zstd                      1.4.5                h04227a9_0
