import json

uniques = None

def loadUniques():
    global uniques
    with open('./data/fritidshus_uniques.txt') as json_file:
        uniques = json.load(json_file)

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


def getFritidshusFactorIndex(name, value):
    if (name == 'Ydervæg'):
        index = getWallSelects.index(value)
        return index
    elif (name == 'Tag'):
        index = getRoofSelects().index(value)
        return index
    elif (name == 'Varmeinstallation'):
        index = getHeatingSelects().index(value)
        return index
    else:
        return None
    
#Spørgsmålene
def getFritidshusQuestions():
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
            "type": "text",
            "name": "Ejerudgift",
            "message": "Indtast månedlig ejerudgift",
        },
        {
            "type": "text",
            "name": "Enhedsareal",
            "message": "Indtast Enhedsareal", 
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
        },{
             "type": "text",
            "name": "Boligenhed med eget køkken",
            "message": "Hvor mange køkkener har boligenheden ? ",

        },
        {
            "type": "select",
            "name": "Ydervæg",
            "message": "Hvilken type ydervæg har boligenheden?",
            "choices": getWallSelects(),
        },
        {
            "type": "select",
            "name": "Tag",
            "message": "Hvilken type tag har boligenheden?",
            "choices": getRoofSelects(),
        },{
            "type": "text",
            "name": "Grundskyld",
            "message": "Indtast Grundskyld",

        },
        {
            "type": "text",
            "name": "Etager",
            "message": "Indtast antal etager",
        },
        {
            "type": "text",
            "name": "Seneste ombygning",
            "message": "Seneste ombygning (brug byggeår, hvis ingen ombygning)",
        },
        {
            "type": "select",
            "name": "Varmeinstallation",
            "message": "Hvilken type varmeinstallation har boligenheden?",
            "choices": getHeatingSelects(),
        },
        
        {
            "type": "text",
            "name": "Ejendomsværdiskat",
            "message": "Indtast ejendomsværdiskat",
        }
    ]

    return questions

