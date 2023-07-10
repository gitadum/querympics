# Querympics

version de l'API : `0.4.0` 

Une API pour trouver des infos sur les jeux olympiques
* un résultat sportif donné
* un athlète donné
* une région et un sport

## Installation

### Installer Querympics

version de Python : `3.8.x`

```bash
git clone https://github.com/gitadum/querympics.git
cd querympics
pip install -r requirements.txt
```

*N.B. : pour le développement lancer aussi*
*la commande suivante depuis le dossier projet :*
```bash
pip install -r requirements.dev.txt
```

Enfin installer le paquet `querympics`
avec la commande suivante (depuis le dossier projet):
```bash
pip install .
```

### Recréer la base de données

1. Installer PostGreSQL
2. Paramétrer l'utilisateur et le mot de passe
3. Recréer les tables et chargez les
données de base grâce au script `querympics/data/load.py`
```bash
python querympics/data/load.py
```

## Utilisation

### Lancement
Dans un terminal, depuis le dossier d'installation,
lancer la commande :
```bash
uvicorn querympics.api:app
```
### Requêtes

#### Pour un athlète

On peut rechercher un athlète par son nom,
pour cela il suffit de lancer une requête `GET`
sur le chemin `/search/athlete`, avec en paramètre
le nom de l'athlète.

**Exemple**

Depuis un terminal, si on lance la commande :

```bash
curl -X 'GET' \
  'http://localhost:8000/search/athlete?last_name=Manaudou'
```
l'API renverra une liste de cette forme :
```json
[
  {
    "id": "321029698527",
    "first_name": "Florent",
    "last_name": "MANAUDOU",
    "gender": "M",
    "birth_year": "1991",
    "nocs": [
      "FRA"
    ],
    "disciplines": [
      "Swimming"
    ],
    "n_medals": 4
  },
  {
    "id": "506160875731",
    "first_name": "Laure",
    "last_name": "MANAUDOU",
    "gender": "F",
    "birth_year": "1987",
    "nocs": [
      "FRA"
    ],
    "disciplines": [
      "Swimming"
    ],
    "n_medals": 3
  }
]
```

Si on s'intéresse uniquement à Laure Manaudou,
on peut aussi récupérer un résultat unique avec une requête par ID d'athlète :

```bash
curl -X 'GET' \
  'http://localhost:8000/athlete/506160875731'
```

sortie :

```json
{
  "id": "506160875731",
  "first_name": "Laure",
  "last_name": "MANAUDOU",
  "gender": "F",
  "birth_year": 1987,
  "lattest_noc": "FRA"
}
```

#### Pour une région

Il est aussi possible de requêter une région en particulier

**Exemple :**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/search/region?region=Japan'
```
l'API renvoie en sortie :
```json
[
  {
    "region": "Japan",
    "sport": "all",
    "season": "all",
    "year": null,
    "n_medals": 647
  }
]
```

Il est aussi possible de préciser un sport :

```bash
curl -X 'GET' \
  'http://localhost:8000/search/region?region=Japan&sport=Judo'
```

sortie :

```json
[
  {
    "region": "Japan",
    "sport": "Judo",
    "season": "all",
    "year": null,
    "n_medals": 13
  }
]
```
