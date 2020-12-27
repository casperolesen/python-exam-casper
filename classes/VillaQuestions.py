import json

from classes.Validator import NumberValidator, ZipValidator, YearBuildValidator
uniques = None

def loadUniques():
    global uniques
    with open('./data/villa_uniques.txt') as json_file:
        uniques = json.load(json_file)

def getEnergySelects():
    if (uniques is None):
        loadUniques()

    energy_uniques = [cat['uniques'] for cat in uniques if cat['name'] == 'Energimærke']
    energy_select = [e for e in energy_uniques[0]]
    return energy_select

def getWallSelects():
    if (uniques is None):
        loadUniques()
    
    walls_uniques = [cat['uniques'] for cat in uniques if cat['name'] == 'Ydervæg']
    walls_select = [w for w in walls_uniques[0]]
    return walls_select

def getRoofSelects():
    if (uniques is None):
        loadUniques()

    roofs_uniques = [cat['uniques'] for cat in uniques if cat['name'] == 'Tag']
    roofs_select = [r for r in roofs_uniques[0]]
    return roofs_select

def getHeatingSelects():
    if (uniques is None):
        loadUniques()

    heatings_uniques = [cat['uniques'] for cat in uniques if cat['name'] == 'Varmeinstallation']
    heatings_select = [h for h in heatings_uniques[0]]
    return heatings_select

def getVillaFactorIndex(name, value):
    if (name == 'Energimærke'):
        index = getEnergySelects().index(value)
        return index
    elif (name == 'Ydervæg'):
        index = getWallSelects().index(value)
        return index
    elif (name == 'Tag'):
        index = getRoofSelects().index(value)
        return index
    elif (name == 'Varmeinstallation'):
        index = getHeatingSelects().index(value)
        return index
    else:
        return None
    

def getVillaQuestions():
    if (uniques is None):
        loadUniques()
    
    questions = [
        {
            "type": "text",
            "name": "Adresse",
            "message": "Postnummer",
            "validate": ZipValidator(),
        },
        {
            "type": "text",
            "name": "Year build",
            "message": "Byggeår",
            "validate": YearBuildValidator(),
        },
        {
            "type": "select",
            "name": "Energimærke",
            "message": "Vælg energimærkning",
            "choices": getEnergySelects(),
        },
        {
            "type": "text",
            "name": "Ejerudgift",
            "message": "Ejerudgift i kroner",
            "validate": NumberValidator(),
        },
        {
            "type": "text",
            "name": "Enhedsareal",
            "message": "Boligstørrelse",
            "validate": NumberValidator(), 
        },
        {
            "type": "text",
            "name": "Værelser",
            "message": "Antal Værelser",
            "validate": NumberValidator(),
        },
        {
            "type": "text",
            "name": "Antal Toiletter",
            "message": "Antal Toiletter",
            "validate": NumberValidator(),
        },
        {
            "type": "text",
            "name": "Antal badeværelser",
            "message": "Antal badeværelser",
            "validate": NumberValidator(),
        },
        {
            "type": "select",
            "name": "Ydervæg",
            "message": "Vælg ydervæg",
            "choices": getWallSelects(),
        },
        {
            "type": "select",
            "name": "Tag",
            "message": "Vælg tag",
            "choices": getRoofSelects(),
        },
        {
            "type": "text",
            "name": "Etager",
            "message": "Antal etager",
            "validate": NumberValidator(),
        },
        {
            "type": "text",
            "name": "Seneste ombygning",
            "message": "Seneste ombygning (brug byggeår, hvis ingen ombygning)",
            "validate": YearBuildValidator(),
        },
        {
            "type": "select",
            "name": "Varmeinstallation",
            "message": "Vælg varmeinstallation",
            "choices": getHeatingSelects(),
        },
        {
            "type": "text",
            "name": "Grundstørrelse",
            "message": "Grundstørrelse",
            "validate": NumberValidator(),
        }
    ]

    return questions