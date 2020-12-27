import questionary
import json
import numpy as np
from classes.VillaData import loadModel as loadVillaModel
from classes.VillaQuestions import getVillaQuestions, getVillaFactorIndex
from classes.RaekkehusData import loadModel as loadRaekkehusModel
from classes.RaekkehusQuestions import getRaekkehusQuestions, getRaekkehusFactorIndex
from classes.EjerlejlighedData import loadModel as loadEjerlejlighedModel
from classes.EjerlejlighedQuestions import getEjerlejlighedQuestions, getEjerlejlighedFactorIndex
from classes.FritidshusQuestions import getFritidshusQuestions, getFritidshusFactorIndex
from classes.FritidshusData import loadModel as loadFritidshusModel


model = None
housetypes = ["Villa", "Ejerlejlighed", "Rækkehus", "Fritidshus"]

def predictPrice(answers):
    global model
    if (model is None):
        return "No model available"
    else:
        return model.predict(answers.reshape(1,-1))

def loadModel(type):
    global model
    if (type == 'Villa'):
        model = loadVillaModel('data/villa_model.pickle')
    elif (type == 'Ejerlejlighed'):
        model = loadEjerlejlighedModel('data/ejerlejlighed_model.pickle')
        
    elif (type == 'Rækkehus'):
        model = loadRaekkehusModel('data/raekkehus_model.pickle')
    elif (type == 'Fritidshus'):
        model = loadFritidshusModel('data/fritidshus_model.pickle')
          


def convertAnswers(type, answers):
    temp = []
    if (type == 'Villa'):
        cats = ['Energimærke', 'Ydervæg', 'Tag', 'Varmeinstallation']
        for a in answers:
            if (a in cats):
                temp.append(int(getVillaFactorIndex(a, answers[a])))
            else:
                temp.append(int(answers[a]))

    elif (type == 'Rækkehus'):
        cats = ['Energimærke', 'Ydervæg', 'Tag', 'Varmeinstallation']
        for a in answers:
            if (a in cats):
                temp.append(int(getRaekkehusFactorIndex(a, answers[a])))
            else:
                temp.append(int(answers[a]))

    elif (type == 'Ejerlejlighed'):
        cats = ['Energimærke','Ydervæg','Varmeinstallation','Tag']
        for a in answers:
            if (a in cats):
                temp.append(int(getEjerlejlighedFactorIndex(a, answer[a])))
                else:
                    temp.append(int(answers[a]))

    elif (type == 'Fritidshus'):
        cats = ['Varmeinstallation','Tag','Ydervæg']
        for a in answers:
            if (a in cats):
                temp.append(int(getFritidshusFactorIndex(a, answer[a])))
                else:
                    temp.append(int(answers[a]))
                        
        
    return np.array(temp)

def getQuestions(type):
    if (type == 'Villa'):
        return getVillaQuestions()
    elif (type == 'Rækkehus'):
        return getRaekkehusQuestions()
    elif (type == 'Ejerlejlighed'):
        return getEjerlejlighedQuestions()
    elif (type == 'Fritidshus'):
        return getFritidshusQuestions()       

if __name__ == "__main__":
    run = True

    while (run):

        type_q = questionary.select("Vælg en type", housetypes)
        type_a = type_q.ask()

        loadModel(type_a)

        answers = questionary.prompt(getQuestions(type_a))
        print('Estimeret pris: {pris}'.format(pris = predictPrice(convertAnswers(type_a, answers))))

        run_q = questionary.confirm("Vil du prøve igen?")
        run = run_q.ask()

    print("PriceMachine is closed")

