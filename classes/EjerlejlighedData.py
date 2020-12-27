import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import questionary

import sys
for path in sys.path:
    print(path)

file_p ='./data/house_data.csv'

data = None
uniques = None
X_test_final = None
y_test_final = None
model_final = None

#Energimærker
energi_unique =['0','A','A1','A2','A10','A15','A20','B','C','D','E','F','G']

#Varmeinstallation
Varmeinstallation_unique=['Blandet','Centralvarme med to fyringsenheder','Centralvarme med én fyringsenhed','Elvarme','Fjernvarme blokvarme','Gasradiator','Ingen varmeinstallation','Ovn til fast og flydende brændsel','Varmepumpe']

#Tag
Tag_unique =['Tegl','Tagpap med lille hældning','Fibercement herunder asbest','Tagpap med stor hældning','Andet materiale','Betontagsten','Metal','Fibercement uden asbest','Stråtag','Levende tage','Glas','Plastmaterialer']

#Ydervæg
Ydervæg_unique=['Mursten','Betonelementer','Andet materiale','Letbetonsten','Træ','Fibercement herunder asbest','Metal','Bindingsværk','Glas','Ingen','Fibercement uden asbest']

def getEjerlejlighedDataRaw():
    t= pd.read_csv(file_p)
    t=t[t['Type'] == 'Ejerlejlighed']
    return t

def getEjerlejlighedData():
    global data,uniques
    if data is None:
        print('Cleaning')
        data=clean_data()
        return data
    else:
        print('Data is already cleaned')
        return data

def trainModel():
    global model_final, X_test_final, y_test_final
    data = getEjerlejlighedData()

    y = data['Pris']
    
    data.drop(['Pris'], 'columns', inplace=True)
    X = data
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=101)

    lm = LinearRegression()
    lm.fit(X_train, y_train)

    model_final = lm
    X_test_final = X_test
    y_test_final = y_test

    print('Model trained')

def testModel():
    global model_final, X_test_final, y_test_final

    if (model_final is None or X_test_final is None or y_test_final is None):
        return "You need to first train a model"
    else:
        return model_final.score(X_test_final, y_test_final)

def saveModel():
    global model_final, X_test_final, y_test_final
    if (model_final is None):
        return "No model to save. Remember to train it first"
    else: 
        filename = './data/ejerlejlighed_model.pickle'
        pickle.dump(model_final, open(filename, 'wb'))
        print("Model saved!")
        return X_test_final, y_test_final

def loadModel(file_p):
    loaded_model = pickle.load(open(file_p, 'rb'))
    return loaded_model

def clean_data():
    #Læser fil
    t =pd.read_csv(file_p)
    #Specifies what type 
    t=t[t['Type']=='Ejerlejlighed']

    #drops de feautures der ikke er relevante (Disse fandt vi efter at have analyseret data)
    t.drop([
    'Boligtype',
    'Badeforhold',
    'Køkkenforhold',
    'Udhus',
    'Toiletforhold',
    'Boligenhed uden eget køkken',
    'Energikode',
    'Grundstørrelse',
    'Vejareal',
    'Lands ejerlav kode',
    'Kommunal ejerlav kode',
    'Ejendomsnummer',
    'Primær matrikel',
    'Lands ejerlav navn',
    'Kommunal ejerlav navn',
    'Matrikelnummer',
    'Afvigende etager',
    'Boligstørrelse tinglyst',
    'Objekt status',
    'Boligstørrelse BBR',
    'Boligstørrelse',
    'Bygningsnummer',
    'Beboelsesareal',
    'URL',
    'Carport',
    'Boligydelse',
    'Anvendelse',
    'Type'
     ], 'columns', inplace=True)

    # formaterer til floats
    t['Year build'] = pd.to_numeric(t['Year build'], errors='coerce')
    t['Ejerudgift'] = pd.to_numeric(t['Ejerudgift'], errors='coerce')
    t['Enhedsareal'] = pd.to_numeric(t['Enhedsareal'], errors='coerce')
    t['Pris'] = pd.to_numeric(t['Pris'], errors='coerce')

    #Adresse til zipcode
    t['Adresse'] = t['Adresse'].str.extract(r'(\d{4})').astype('int64')

    #Dropping de høje priser
    t = t[t['Pris']<9500000]

    #Drops dem med manglende value
    t= t.dropna()

    # column names split into numeric and categorial
    categ = list(set(t.columns) - set(t.corr()['Pris'].index))

    # bring categories into a numerical format:
    factorized = []
    for i in categ:
        codes_t, uniques_t = t[i].factorize(sort=True)

        t[i] = codes_t
        factorized.append({'name': t[i].name, 'uniques': uniques_t.to_numpy().tolist()})
    
    uniques = factorized
    print(uniques)
  
    with open('./data/ejerlejlighed_uniques.txt', 'w') as outfile:
        json.dump(uniques, outfile)

    return t



