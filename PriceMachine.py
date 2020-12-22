import questionary
import json
from classes.VillaData import loadModel as loadVillaModel
from classes.VillaQuestions import getVillaQuestions, getVillaFactorIndex
import numpy as np

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


def convertAnswers(type, answers):
    temp = []
    if (type == 'Villa'):
        cats = ['Energimærke', 'Ydervæg', 'Tag', 'Varmeinstallation']
        for a in answers:
            if (a in cats):
                temp.append(int(getVillaFactorIndex(a, answers[a])))
            else:
                temp.append(int(answers[a]))

        return np.array(temp)

def getQuestions(type):
    if (type == 'Villa'):
        return getVillaQuestions()

if __name__ == "__main__":
    type_q = questionary.select("Vælg en type", housetypes)
    type_a = type_q.ask()

    loadModel(type_a)

    answers = questionary.prompt(getQuestions(type_a))
    print(predictPrice(convertAnswers(type_a, answers)))

