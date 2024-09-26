# Querympics

version de l'API : `0.5.0-beta`

Une API pour trouver des infos sur les jeux olympiques
* un résultat sportif donné
* un athlète donné
* une région et un sport

## Installation

### Installer Querympics

#### Prérequis

Pour installer querympics il est nécessaire de disposer des outils suivants :
- git
- docker
- docker-compose ([doc d'installation](https://docs.docker.com/compose/install/))

#### Pas à pas

```bash
git clone https://github.com/gitadum/querympics.git
cd querympics
docker-compose -f docker-compose.yaml --project-name 'querympics' up
```

### Pour le développement

#### Prérequis

Pour contribuer au développement de querympics, il est nécessaire de disposer des outils suivants :
- git
- python (version `3.8`)

#### Pas à pas 

```bash
git clone https://github.com/gitadum/querympics.git
cd querympics
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

Enfin installer le paquet `querympics`
avec la commande suivante (depuis le dossier projet):
```bash
pip install .
```

## Utilisation

### Lancement
Dans un terminal, depuis le dossier d'installation,
lancer la commande :
```bash
docker-compose up
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
