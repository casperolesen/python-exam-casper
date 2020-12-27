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
