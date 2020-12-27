import json

uniques = None

def loadUniques():
    global uniques
    with open('./data/ejerlejlighed_uniques.txt') as json_file:
        uniques = json.load(json_file)

#Energimærke
def getEnergySelects():
    if (uniques is None):
        loadUniques()

    energy_uniques = [cat['uniques'] for cat in uniques if cat['name'] == 'Energimærke']
    energy_select = [e for e in energy_uniques[0]]
    return energy_select

#Ydervæg
def getWallSelects():
    if (uniques is None):
        loadUniques()
    
    walls_uniques = [cat['uniques'] for cat in uniques if cat['name'] == 'Ydervæg']
    walls_select = [w for w in walls_uniques[0]]
    return walls_select
#Tag
def getRoofSelects():
    if (uniques is None):
        loadUniques()

    roofs_uniques = [cat['uniques'] for cat in uniques if cat['name'] == 'Tag']
    roofs_select = [r for r in roofs_uniques[0]]
    return roofs_select

#Varmeinstallation
def getHeatingSelects():
    if (uniques is None):
        loadUniques()

    heatings_uniques = [cat['uniques'] for cat in uniques if cat['name'] == 'Varmeinstallation']
    heatings_select = [h for h in heatings_uniques[0]]
    return heatings_select

def getEjerlejlighedFactorIndex(name, value):
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
    
#Henter spørgsmål 
def getEjerlejlighedQuestions():
    if (uniques is None):
        loadUniques()
    
    questions = [
        {
            "type": "text",
            "name": "Adresse",
            "message": "Indtast Postnummer",
        },
        {
            "type": "text",
            "name": "Year build",
            "message": "Indtast Byggeår",
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
            "message": "Indtast månedlig ejerudgift",
        },
        {
            "type": "text",
            "name": "Enhedsareal",
            "message": "Indtast Boligstørrelse", 
        },
        {
            "type": "text",
            "name": "Værelser",
            "message": "Indtast antal Værelser",
        },
        {
            "type": "text",
            "name": "Antal Toiletter",
            "message": "Indtast antal Toiletter",
        },
        {
            "type": "text",
            "name": "Antal badeværelser",
            "message": "Indtast antal badeværelser",
        },
        {
            "type": "select",
            "name": "Ydervæg",
            "message": "Hvilken ydervæg har boligen ?",
            "choices": getWallSelects(),
        },
        {
            "type": "select",
            "name": "Tag",
            "message": "Hvilket tag har boligen?",
            "choices": getRoofSelects(),
        }, 
        {
            "type": "text",
            "name": "Etager",
            "message": "Antal etager",
        },
        {
            "type": "text",
            "name": "Seneste ombygning",
            "message": "Seneste ombygning (brug byggeår, hvis ingen ombygning)",
        },
        {
            "type": "select",
            "name": "Varmeinstallation",
            "message": "Hvilken varmeinstallation har ejendommen?",
            "choices": getHeatingSelects(),
        },
        {
            "type": "text",
            "name": "Ejendomsværdiskat",
            "message": "Indtast ejendomsværdiskat",
        },
        {
            "type": "text",
            "name": "Grundskyld",
            "message": "Indtast Grundskyld",
        }
    ]

    return questions

