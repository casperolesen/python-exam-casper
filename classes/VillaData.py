import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import json

file_path = './data/house_data.csv'
data = None

model_final = None
X_test_final = None
y_test_final = None

uniques = None
# # energimærker
# energimærke_unique = ['F', 'D', 'E', 'C', 'G', 'B', 'A10', 'A15', 'A20', 'A', '0', 'A2', 'A1']

# # ydervægge
# Ydervæg_unique = ['Mursten', 'Letbetonsten', 'Bindingsværk', 'Træ', 'Betonelementer',
#  'Andet materiale', 'Fibercement herunder asbest', 'Fibercement uden asbest',
#  'Glas', 'Metal', 'Plastmaterialer']

# # tage
# Tag_unique = ['Fibercement herunder asbest', 'Tegl', 'Betontagsten', 'Metal',
#  'Tagpap med stor hældning', 'Fibercement uden asbest',
#  'Tagpap med lille hældning', 'Andet materiale', 'Stråtag', 'Levende tage',
#  'Glas', 'Plastmaterialer']

# # varmeinstallation
# Varmeinstallation_unique = ['Centralvarme med én fyringsenhed', 'Fjernvarme blokvarme', 'Elvarme',
#  'Varmepumpe', 'Centralvarme med to fyringsenheder',
#  'Ovn til fast og flydende brændsel', 'Ingen varmeinstallation', 'Blandet',
#  'Gasradiator']


def getVillaDataRaw():
    temp = pd.read_csv(file_path)
    temp = temp[temp['Type'] == 'Villa']
    return temp


def getVillaData():
    global data, uniques
    if data is None:
        print('Cleaning data')
        data = clean_data()
        return data
    else:
        print('Data was already cleaned')
        return data

def trainModel():
    global model_final, X_test_final, y_test_final
    data = getVillaData()

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
        filename = './data/villa_model.pickle'
        pickle.dump(model_final, open(filename, 'wb'))
        print("Model saved!")
        return X_test_final, y_test_final

def loadModel(filepath):
    loaded_model = pickle.load(open(filepath, 'rb'))
    return loaded_model

def clean_data():
    # read file
    temp = pd.read_csv(file_path)

    # select only types of villa
    temp = temp[temp['Type'] == 'Villa']

    # drop non-relevant columns (picked after analyzing the raw data)
    temp.drop([
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
        'Boligstørrelse',

        'Energikode',
        'Carport',
        'Udhus',
        'Boligenhed med eget køkken',
        'Boligenhed uden eget køkken',

        'Boligtype',
        'Badeforhold',
        'Køkkenforhold',
        'Toiletforhold',

        'Ejendomsværdiskat',
        'Grundskyld'
    ], 'columns', inplace=True)

    # format some values from objects to floats
    temp['Year build'] = pd.to_numeric(temp['Year build'], errors='coerce')
    temp['Pris'] = pd.to_numeric(temp['Pris'], errors='coerce')
    temp['Ejerudgift'] = pd.to_numeric(temp['Ejerudgift'], errors='coerce')
    temp['Enhedsareal'] = pd.to_numeric(temp['Enhedsareal'], errors='coerce')

    # convert address to only zipcode
    temp['Adresse'] = temp['Adresse'].str.extract(r'(\d{4})').astype('int64')

    # remove data with abnormal feature values
    temp = temp[temp['Enhedsareal']<300]
    temp = temp[temp['Værelser']<10]
    temp = temp[temp['Antal toiletter']<=3]
    temp = temp[temp['Antal badeværelser']<=3]
    temp = temp[temp['Grundstørrelse']<1500]
    temp = temp[ (temp['Year build']>1850) & (temp['Year build']<2020) ]
    
    # clean up 'Seneste ombygning'
    temp['Seneste ombygning'] = np.where(temp['Seneste ombygning'] < 1850, temp['Year build'], temp['Seneste ombygning'])

    # remove data with abnormal target value
    temp = temp[temp['Pris'] < 6000000]

    # remove data with Energimærke '0'
    temp = temp[temp.Energimærke != '0']

    # find missing values in the data and drop those rows:
    temp = temp.dropna()

    

    # column names split into numeric and categorial
    categ = list(set(temp.columns) - set(temp.corr()['Pris'].index))

    # bring categories into a numerical format:
    factorized = []
    for i in categ:
        codes_temp, uniques_temp = temp[i].factorize(sort=True)

        temp[i] = codes_temp
        factorized.append({'name': temp[i].name, 'uniques': uniques_temp.to_numpy().tolist()})
    
    uniques = factorized
    print(uniques)
    #filename = './data/villa_uniques.pickle'
    #pickle.dump(uniques, open(filename, 'wb'))
    with open('./data/villa_uniques.txt', 'w') as outfile:
        json.dump(uniques, outfile)

    return temp
