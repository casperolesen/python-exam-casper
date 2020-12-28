### Formål 
Vi vil hente data fra https://www.boliga.dk/salg/resultater?page=1&sort=date-d data er en liste over solgte boliger i Danmark med 1,4 millioner rækker data. Vi tænker at tage data fra perioden 2015-2020 for ikke at skulle tænke for meget på inflation.
Vi vil prøve at finde en sammenhæng mellem den tilgængelige data og prisen på boligen, for derefter at sammenligne vores resultat mod det reele resultat.


### How-to
Start programmet ved at køre `python PriceMachine.py`

### Struktur
Projektet indeholder en webcrawler, analyse og præsentation af data samt et CLI-program til estimering af en pris.

* [Webcrawler (Er kørt fra main.py)](tools/)
* Data-analyse
    - [Villa (Notebook)](villa.ipynb)
    - [Rækkehuse (Notebook)](raekkehus.ipynb)
    - [Ejerlejlighed (Notebook)](Ejerlejlighed.ipynb)
    - [Fritidshus (Notebook)](Fritidshus.ipynb)
* Data-præsentation
    - [Villa (Notebook)](villa_presentation.ipynb)
    - [Rækkehus (Notebook)](raekkehus_presentation.ipynb)
    - [Ejerlejlighed (Notebook)](EjerlejlighedCleaned.ipynb)
    - [Fritidshus (Notebook)](FritidshusCleaned.ipynb)
* Data-håndtering (Backend for data og machine-learning)
    - [VillaData](classes/VillaData.py)
    - [Rækkehus](classes/RaekkehusData.py)
    - [Ejerlejlighed](classes/EjerlejlighedData.py)
    - [Fritidshus](classes/FritidshusData.py)
* CLI
    - [PriceMachine](PriceMachine.py)
* Data
    - [Bolig-data](data/house_data.csv)
    - [Bolig-links](data/links.csv)

### Teknologier 
* Beautifulsoup
* Pandas 
* Numpy
* Matplotlib
* Seaborn
* Machine learning (supervised learning, regression, sklearn)
* Questionary
* Pickle

