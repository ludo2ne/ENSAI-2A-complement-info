# TP 2 : Webservices et formats de données

## :arrow_forward: 0. Avant de commencer

> :scream: Comme vous pouvez le constater, le sujet de ce TP est lui aussi long. Cela ne doit pas vous effrayer. 
> Il mélange explications complètes et manipulations pour être au maximum autosuffisant. 
> **Vous n'allez surement pas terminer le sujet, ce n'est pas grave. Il est là pour vous aider lors du projet informatique.**
>
> :exclamation: Il est possible que les copier-coller fonctionnent étrangement (caractère de fin de ligne qui disparaissent, indentation qui change). Faites-y attention !
>
> Ce TP mêle explications pour vous faire comprendre ce qui est fait, et phases de manipulation ou code. 
> Ces phases sont appelées "**:writing_hand:Hands on**". C'est à ce moment là que vous devez faire ce qui est écrit dans le TP.
> Les explications de ce TP ne doivent pas prendre le pas sur celles de votre intervenant. Prenez les comme une base de connaissances pour plus tard, mais préférez toujours les explications orales, surtout pour poser des questions.


Dans ce TP vous allez : 

* Faire des appels à un webservice à la main avec Insomnia
* Faire des appels à un webservice avec la bibliothèque python **requests**
* Découvrir la page swagger d'un webservice
* Manipuler différents formats de données
* Créer un webservice avec le framework python **fastAPI**

## :arrow_forward: 1. Appeler un webservice à la main

La première partie de ce TP ne nécessite pas d'écrire du code, mais seulement de faire des requêtes à un webservice en utilisant **Insomnia**.


### Webservices

> :book: **Webservice** : le terme webservice est un terme vaste et il serait compliqué d'en donner une définition courte ([article wikipedia](https://en.wikipedia.org/wiki/Web_service)). 
> Dans le cadre du projet un webservice désigne une application accessible via le protocole HTTP (**H**yper**T**ext **T**ransfer **P**rotocol) qui respecte généralement l'architecture REST (* **RE**presentational **S**tate **T**ransfer). 
> Mais il en existe d'autre comme SOAP (**S**imple **O**bjet* **A**ccess **P**rotocol) ou RPC (**R**emote **P**rocedure **C**all)

En d'autres termes, un webservice est une application accessible via le web que l'on va pouvoir **requêter** soit pour obtenir des **ressources**, soit pour **modifier** les ressources accessibles. Un webservice peut seulement avoir pour but d'être une **point d'accès unique et normalisé** à des données (comme une interface à une base de données), mais il peut également être une **manière de contrôler un système d'information** (lancer des travaux, les mettre en attente, récupérer des résultats, etc)

Les webservices utilisent le protocole HTTP qui est le protocole du web (et pas d'internet). C'est celui que vous utilisez sans le savoir avec votre navigateur web. Requêter un webservice se fait presque comme requêter une page web. Pour cela il vous faut l'adresse de la ressource, son *Uniforme Resource Identifier*, ou URI (c'est une notion plus générale que les *Uniforme Resource Locator*, ou URL), une méthode (GET, POST, PUT, DELETE, [liste des méthodes](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods)), et potentiellement des données.

### :small_orange_diamond: Découverte d'Insomnia et premières requêtes `GET`

**:writing_hand:Hands on 1**

* [ ] Lancez le programme **Insomnia** (recherchez dans le menu démarrer)
* [ ] Créez une collection de requête 
    * bouton **Create** à droite
    * puis cliquez sur votre collection
* [ ] Créez une nouvelle requête 
    * en appuyant sur **CTRL+N**
    * donnez lui un nom 
    * vérifiez que c'est bien une requête de type **GET**
* [ ] Dans la barre d'adresse, testez les requêtes ci-dessous 
    * Regardez la réponse dans la partie droite de votre écran. 
    * Quelles sont les similarités entre les réponses ?

Requêtes à tester :

* [Webservice](https://carbon-intensity.github.io/api-definitions/#carbon-intensity-api-v2-0-0) sur les émissions carbone du Royaume-Uni :
  * `api.carbonintensity.org.uk/intensity`
  * `api.carbonintensity.org.uk/intensity/date/{date}` 
    * en remplaçant {date} par la date de votre choix au format YYYY-MM-DD
* [Webservice](https://data.rennesmetropole.fr/explore/?sort=modified) pour obtenir différents jeux de données ouverts de la ville de Rennes
  * `data.rennesmetropole.fr/api/records/1.0/search?dataset=menus-cantines`
  * Testez différentes valeurs pour dataset :`eco-counter-data`, `rva-bal`, `resultats-des-elections-municipales-2020-a-acigne`
  * Ajouter à la fin de l'URI le paramètre `rows` 
      * pour faire varier le nombre de lignes que vous recevez 
      * ajouter simplement `&rows=X` avec X le nombre de lignes
* Quelques méthodes du webservice utiles pour votre projet informatique (voyez cela avec votre tuteur)

---

### :small_orange_diamond: Requêtes avancées

**:writing_hand:Hands on 2** (toujours avec **Insomnia**)

* Faites une requête avec la méthode `GET` sur la ressource suivante. Qu'obtenez-vous ? 
    * `web-services.domensai.ecole/attack`
* Faites une requête avec la méthode `GET` sur la ressource suivante. Qu'obtenez-vous ? 
    * `web-services.domensai.ecole/attack/{identifier}`
    * en remplaçant `{identifier}` par le nom ou l'id d'une attaque que vous venez de récupérer
* Faites une requête avec la méthode `GET` sur la ressource suivante. Qu'obtenez-vous ?
    * `web-services.domensai.ecole/attack?type_attack_id={id_type}`
    * en remplaçant `{id_type}` par un entier entre 1 et 4. 
* Faites une requête avec la méthode `GET` sur la ressource suivante
    *  `web-services.domensai.ecole/attack?type_attack_name={type attack}`
    *  en remplaçant `{type attack}` par  `special attack` ou `physical attack` ou `fixed damage` ou `status attack`
* Faites une requête de type `POST` sur la ressource suivante 
    * `web-services.domensai.ecole/attack` 
    * Cliquer sur **Body**, puis **JSON**, coller le texte ci-dessous, puis remplacez les valeurs des attributs pour créer votre propre attaque
  ````json
  {
    "name": "An awesome name",
    "attack_type": "physical attack"/"physical attack"/"fixed damage"/"status attack",
    "power": 0,
    "accuracy": 0,
    "element": "An awesome element",
    "description": "An awesome description"
  }
  ````
* Faites une requête avec la méthode `GET` sur la ressource suivante
    * `web-services.domensai.ecole/attack/{identifier}`
    * en remplaçant `{identifier}` par le nom ou l'id de l'attaque que vous venez de créer

---

### :small_orange_diamond: Swagger

Dans votre navigateur web allez sur la page http://web-services.domensai.ecole/docs. 
Cela vous amène sur la page swagger du webservice. Cette page recense tous les endpoints du webservice, et comment les utiliser. Essayez via l'interface de :

* modifier une attaque
* supprimer une attaque
* afficher une liste de pokémon
* ajouter un pokémon

## :arrow_forward: 2. Appeler un webservice en python


Aujourd'hui, les plus grands consommateurs de webservices sont les machines. Et donc maintenant nous allons voir comment automatiser des appels à un webservice en python.

> :mag: Aujourd'hui beaucoup d'applications web (par exemple Facebook, Netflix, Dailymotion, Uber) utilisent ce que l'on appelle des architectures "micro services". 
> 
> Les échanges entre leurs composants applicatifs (par exemple entre leurs interface homme machine (IHM) et leurs services internes) se font via des webservices à but unique. Cela permet d'avoir des modules découplés les uns des autres car ils communiquent uniquement via requête HTTP, ou avec des systèmes de gestion d'évènements. Ils ont seulement à savoir comment ils doivent communiquer les uns avec les autres et pas le fonctionnement interne des autres modules. 
> 
> Le côté négatif c'est que cela demande de bien documenter ses webservices et de gérer ÉNORMÉMENT d'applications en parallèle. Amazon, Google, Facebook peuvent se le permettre, par contre une petite entreprise de 10 employés non.

---

### :small_orange_diamond: La bibliothèque `requests` - Comment ça fonctionne

Le principe va rester le même que faire une requête à la main, et on va utiliser la bibliothèque [**requests**](https://requests.readthedocs.io/en/master/) pour avoir seulement à remplir les parties intéressantes de nos requêtes.

Pour faire une requête `GET` vous allez seulement devoir faire : 

````python
import requests

response = requests.get("http://mon-webservice.com") 
````

Exécuter cette ligne de code va :

1. Envoyer la requête au serveur que vous contactez
2. Stockez le résultat dans la variable `response`

Cette variable `response` est un objet, et comme tout objet elle a des attributs et des méthodes, par exemple : 

* `response.text` : le corps du résultat sous forme de string en laissant `requests` inférer l'encodage (cela fonctionne souvent). Problème vous avez seulement un string, et ce n'est pas le meilleur format de données à manipuler
* **`response.json()`** : le corps du résultat comme un `dict`. C'est ce que vous allez faire le plus souvent car le format json est un format simple à manipuler
* `response.encoding` : l'encoding de votre requête (utile en cas de problème d'encoding)
* **`response.status_code`** : le statut de la requête. les principaux sont :
  * 200 : retour général pour dire que tout c'est bien passé
  * 201 : ressource créée avec succès
  * 202 : requête acceptée, sans garantie du résultat (par exemple dans un système asynchrone)
  * 400 : erreur de syntaxe dans la requête
  * 401 : erreur, une authentification est nécessaire
  * 403 : la ressource est interdite (droits insuffisants)
  * 404 : ressource non trouvée
  * 405 : une mauvaise méthode http a été utilisée
  * 500 : erreur côté serveur
  * 503 : service temporairement indisponible

Pour résumer, les résultats 2xx indiquent un succès, un résultat 4xx ou 5xx un problème. 

Exemple simple d'utilisation : 
```python
import requests
import json

response = requests.get("http://mon-webservice.com")

if response.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(response.status_code, response.text)
    )
else:    
    print(json.dumps(response.json(), indent=2))       # JSON Pretty print
```

### :small_orange_diamond: Mise à jour de votre dépôt git

2 possibilités **au choix**

#### :arrow_right: Si vous voulez repartir du code du TP1 

* Ouvrez **Visual Studio Code**
    * File > Open Folder
        * Allez dans `/p/Cours2A/UE3_Complements_informatique/TP/TP1`
        * cliquez une fois sur **ENSAI-2A-complement-info-TP**
        * puis sur le bouton **Sélectionner un dossier**
    * Ouvrez un Terminal Git Bash dans VSCode (Terminal > New terminal)
    * Créez un point de sauvegarde de vos travaux de la semaine dernière
        * `git add .`
        * `git commit -m "Mon super code du TP1"`
    * Mettez à jour votre dépôt local
        * `git pull`
    * Passez sur la branche du TP2
        * `git checkout tp2_base`

#### :arrow_right: Si vous n'avez pas le code du TP1 sur votre machine

* Ouvrez le logiciel **Git Bash**
    * Créez un dossier pour stocker le code du TP
        * par exemple, copiez la ligne ci-dessous, et collez là dans Git Bash (clic droit > Paste)
        * `mkdir -p /p/Cours2A/UE3_Complements_informatique/TP/TP2 && cd $_`
    * Clonez le dépôt
        * `git clone https://github.com/ludo2ne/ENSAI-2A-complement-info-TP.git`
    * Fermez **Git Bash**
* Ouvrez **Visual Studio Code**
    * File > Open Folder
        * Allez dans `/p/Cours2A/UE3_Complements_informatique/TP/TP2`
        * cliquez une fois sur **ENSAI-2A-complement-info-TP**
        * puis sur le bouton **Sélectionner un dossier**
    * Ouvrez un Terminal Git Bash dans VSCode (Terminal > New terminal)
    * Passez sur la branche du TP2
        * `git checkout tp2_base`

#### :warning: Attention quand vous faites Open Folder dans VSCode

Le dossier parent de l'explorer de VSCode (à gauche) doit être : **ENSAI-2A-complement-info-TP**. 
Si c'est TP1, TP2, TP ou autre chose ce n'est pas bon ! Vous allez avoir des soucis d'imports par la suite.

---

Pour pour vérifier que tout fonctionne :
* lancez le fichier `__main__.py`
* lancez les tests unitaires du package business_object
    * dans terminal : `python -m unittest -k test_business_object`

---

### :small_orange_diamond: Mes premières requêtes en Python

:writing_hand: **Hands on 3**

* Si ce n'est pas déjà fait (voir README.md), installez **dotenv**
    * `pip install python-dotenv`
* Ouvrez le fichier `/src/client/attack_client.py` 
* [ ] Complétez la méthode `get_attack(int)`
  * prend en paramètre un id d'attaque 
  * va chercher toutes les informations disponibles sur cette attaque
  * retourne un objet de type `AbstractAttack`
    * Pour vous aider, observez la méthode `instantiate_attack()` de la classe `AttackFactory`
    * Regardez le fonctionnement de cette méthode et utilisez la
* [ ] créez la méthode `get_all_attacks()` 
  * retourne la liste de tous les attaques disponibles sous la forme d'une liste d'objets `AbstractAttack`
* [ ] Vérifiez que vos 2 méthodes fonctionnent
    * Lancez les tests unitaitres du package test_client

---

### :small_orange_diamond: Les requêtes plus complexes

Pour le moment nous nous sommes concentrés sur les requêtes `GET` mais il est bien sûr possible d'en faire d'autre. Par exemple pour les requêtes `POST`, `PUT `ou `DELETE` voici la syntaxe :

```python
post = requests.post("http://example.org", json = {'key':'value'})
put = requests.put("http://example.org", json = {'key':'value'})
delete = requests.delete("http://example.org")
```

Comme vous le voyez, les syntaxes sont très proches de la syntaxe de la méthode `GET`. On a seulement ajouté pour certaines requêtes des données. C'est ce que vous avez fait plus tôt avec Insomnia. Pour passer des paramètres à votre requête je vous conseille néanmoins de préférer ce genre de syntaxe :

```python
url = "http://example.org"
data = {'key':'value'}
post = requests.post(url, json = data)
```

C'est la même chose fonctionnellement, mais il vaut mieux définir les éléments hors de la requête pour ne pas se perdre.

Il est également possible de passer des entêtes http en ajoutant l'attribut `headers` à la fonction utilisée.

```python
headers = {'accept': 'application/xml'}
requests.get('http://example.org', headers=headers)
```

### :small_orange_diamond: Requêtes avancées en python

:writing_hand: **Hands on 4**

* Dans le module `attack_client.py` implémentez les méthodes suivantes : 
  * [ ] `create_attack(AbstractAttack)` 
      * prend une `AbstractAttack` en paramètre
      * crée une nouvelle ressource dans notre webservice
  * [ ] `update_attack(AbstractAttack)` 
      * prend une `AbstractAttack` en paramètre
      * modifie la ressource associée dans notre webservice
  * [ ] `delete_attack(AbstractAttack)` 
      * prend une `AbstractAttack` en paramètre
      * supprime la ressource associée dans notre webservice
* [ ] Testez vos méthodes

## 🤖 Coder un webservice en python

Avec les outils à disposition aujourd'hui il est facile de faire un webservice soit même. 

Il y a trois leaders sur le marché actuellement pour faire un webservice REST en python: 
* [Django REST](https://www.django-rest-framework.org/), 
* [FlaskRESTful](https://flask-restful.readthedocs.io/en/latest/)
* [FastAPI](https://fastapi.tiangolo.com/)

Chacun à ses [avantages et inconvénients](https://www.section.io/engineering-education/choosing-between-django-flask-and-fastapi/). Django est sûrement le plus complet mais le plus lourd, Flask et FastApi sont plus légers et rapides à mettre en place. Le gros avantage de **FastApi** est la simplicité pour créer une page swagger de documentation.

Voici le code minimal d'un webservice REST avec FastAPI ([documentation officielle](https://fastapi.tiangolo.com/tutorial/first-steps/))

```python
from fastapi import FastAPI

# On instancie le webservice
app = FastAPI()

# Création d'un enpoint qui répond à la méthode GET à l'adresse "/" qui va retourne le message "Hello World"
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Lancement de l'application sur le le port 80
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
```

Appeler la ressource "/" du webservice va retourner le json : `{"message": "Hello World"}`

Voici un exemple plus complet inspiré de la [documentation officielle](https://flask-restful.readthedocs.io/en/latest/quickstart.html#resourceful-routing) (vous voulez créer un webservice pour exposer vos **todos**)

````python
from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status
import uvicorn

# On instancie le webservice
app = FastAPI()

class Todo(BaseModel):
    id : int
    content : str

todos = {1 : Todo(1,"Step 1 : Learn python")
        , 2 : Todo(2,"Step 2 : Work on the IT project")
        , 3 : Todo(3,"Step 3 : ???")
        , 4 : Todo(4,"Step 4 : Profit")}

# Définition du endpoint get /todo
@app.get("/todo")
async def get_all_todo():
    return todos.values()

# Définition du endpoint get /todo/{id_doto}
@app.get("/todo/{id_toto}")
async def get_todo_by_id(id_toto : int = Path(..., description = "The `id` of the todo you want to get")):
    if todos.get[id_toto] :
    	return todos.get[id_toto]
    else :
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

# Définition du endpoint post /todo
@app.post("/todo", todo, status_code=201)
async def post_todo(todo:Todo):
    if not todos.get(todo.id):
    	return JSONResponse(status_code=status.HTTP_409_CONFLICT)
    else :
        todos[todo.id] = todo
        return todo

# Lancement de l'application sur le le port 8XXX avec XXX les 3 derniers numéros de votre id
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8XXX)
````

Ce code va créer un web service qui va répondre aux requêtes suivantes :

* `GET host/todo` : retourne toutes les tâches à faire
* `GET host/todo/{todo_id}` : retourne la tâche derrière l'id en paramètre
* `POST host/todo/` : ajoute la tâche passée en corps de la rêquete

FastAPI sérialise pour vous les objets que vous retournez. Donc pas besoin de mettre en forme vos données. Néanmoins, pour plus de clarté, vous pouvez utiliser des classes `BaseModel`. Ce sont des classes qui ne vont contenir que des attributs que vous pouvez déclarer sans constructeur:

```python
class Todo(BaseModel):
    id : int
    content : str
```

Ces classes peuvent être utilisées en sortie de votre webservice, comme en entrée (ligne 33). FastApi va faire pour vous tout une série de contrôle sur les types des variables et renvoyer une erreur au client si sa requête n'est pas bien formatée.

Fondamentalement un webservice est une application comme les autres, mais au lieu d'avoir une interface graphique comme on en a l'habitude en tant qu'humain, l'interface est une interface HTTP qui va accepter des requêtes et envoyer des résultats. Ainsi le diagramme de séquence des différentes couches qui vont être impliquées dans une requête `GET` pour récupérer une ressource va ressembler à cela si je reprends le modèle 3 couches vu en cours.

```mermaid
sequenceDiagram
    participant U as User
    participant R as Webservice
    participant S as Service
    participant D as DAO
    participant B as Base de données
    U ->> R : HTTP requête
    R ->> S : get_by_id()
    S ->> D : find_by_id()
    D ->> B : requête SQL (psycopg)
    B ->> D : curseur SQL (psycopg)
    D ->> S : instance objet metier
    S ->> R : instance objet metier
    Note over S,R: l'objet est potentiellement altéré
    R ->> U : Réponse HTTP
```

### :small_orange_diamond: Mon premier webservice 

* Vérifiez que le module `fastapi` est installé (`pip list`)
    * Si ce n'est pas le cas : `pip install "fastapi[all]"`
* Ouvrez le fichier `app.py`
* Lancez ce fichier
    * testez les requêtes suivantes : 
        * `GET http://localhost/hello`
        * `GET http://localhost/hello/everybody`
* Arrétez le webservice
    * Cliquez dans le terminal de VSCode puis CTRL + C


:writing_hand: **Hands on 5**

En utilsant la liste de personnages définie dans le fichier `app.py`, ajoutez les endpoints suivants : 
* [ ] `GET localhost:80/character` : retournera un json contenant une liste des personnages
* [ ] `PUT localhost:80/character/{id}` qui modifiera le nom du personnage à l'index `{id}` à partir d'un body
* [ ] `DELETE localhost:80/character/{id}` qui supprimera l'élément à l'index `{id}`

Pour tester les endpoints nécessitant un body json, vous pouvez utiliser :-1: 

```json
{
  "nom":"Agneta",
  "age": 30
}
```