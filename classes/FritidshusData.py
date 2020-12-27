import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

file_p ='./data/house_data.csv'

data = None
uniques = None
model_final = None
X_test_final = None
y_test_final = None


#Varmeinstallation
Varmeinstallation_unique=['Centralvarme med to fyringsenheder','Centralvarme med én fyringsenhed','Elvarme','Fjernvarme blokvarme','Gasradiator','Ingen varmeinstallation','Ovn til fast og flydende brændsel','Varmepumpe']

#Tag
Tag_unique =['Tegl','Tagpap med lille hældning','Fibercement herunder asbest','Tagpap med stor hældning','Andet materiale','Betontagsten','Metal','Fibercement uden asbest','Stråtag','Levende tage','Glas','Plastmaterialer']

#Ydervæg
Ydervæg_unique=['Mursten','Bindingsværk','Letbetonsten','Betonelementer','Andet materiale','Letbetonsten','Træ','Fibercement herunder asbest','Metal','Bindingsværk','Glas','Ingen','Fibercement uden asbest']

def getFritidshusDataRaw():
    t= pd.read_csv(file_p)
    t=t[t['Type'] == 'Fritidshus']
    return t

def getFritidshusData():
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
    data = getFritidshusData()

    y = data['Pris']
    
    data.drop(['Pris'], 'columns', inplace=True)
    X = data
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=101)

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
        filename = './data/fritidshus_model.pickle'
        pickle.dump(model_final, open(filename, 'wb'))
        print("Model saved!")
        return X_test_final, y_test_final

def loadModel(file_p):
    loaded_model = pickle.load(open(file_p, 'rb'))
    return loaded_model

def clean_data():
    #Reads the file
    t =pd.read_csv(file_p)
    #Specifies what type 
    t=t[t['Type']=='Fritidshus']

    #drops the feautures that are not relevant (theese feautes were found after analyzing the data)
    t.drop([
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
    'Bygningsnummer',
    'Beboelsesareal',
    'URL',
    'Boligydelse',
    'Anvendelse',
    'Type',
    'Energikode',
    'Energimærke',
    'Carport',
    'Udhus',
    'Boligenhed uden eget køkken',
    'Etager',
    'Boligtype',
    'Badeforhold',
    'Køkkenforhold',
    'Toiletforhold',
    'Boligstørrelse'
     ], 'columns', inplace=True)

    # formats to floats
    t['Year build'] = pd.to_numeric(t['Year build'], errors='coerce')
    t['Ejerudgift'] = pd.to_numeric(t['Ejerudgift'], errors='coerce')
    t['Enhedsareal'] = pd.to_numeric(t['Enhedsareal'], errors='coerce')
    t['Pris'] = pd.to_numeric(t['Pris'], errors='coerce')
    t['Grundstørrelse'] = pd.to_numeric(t['Grundstørrelse'], errors='coerce')

    #Adress to zipcode
    t['Adresse'] = t['Adresse'].str.extract(r'(\d{4})').astype('int64')

    #Dropping the abnormal high prices 
    t = t[t['Pris']<3000000]

    #Dropping high amount of rooms
    t=t[t['Værelser']<21.000000]

    #Dropping high number of groundsize
    t=t[t['Grundstørrelse']<2350.000000]
    
    
   #Dropping low number of groundsize 
    t=t[t['Grundstørrelse']>500]

    #Drops those with missing values 
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
  
    with open('./data/fritidshus_uniques.txt', 'w') as outfile:
        json.dump(uniques, outfile)

    return t


