---
title: TP 3: Data Access Objet (DAO)
author: Rémi Pépin
subject: Complément informatique
keywords: [webservices, DAO]
header:  ${title} - ${author} - Page ${pageNo} / ${totalPages}


---

# TP 3: Data Access Objet (DAO)

> :scream: Comme vous pouvez le constater le sujet de ce TP est lui aussi long. Cela ne doit pas vous effrayer. Il mélange explications complètes et manipulations pour être au maximum autosuffisant. **Vous n'allez surement pas terminer le sujet, ce n'est pas grave. Il est là pour vous aider lors du projet informatique.**
>
> :exclamation: Il est possible que les copiés/collés fonctionnent étrangement (caractère de fin de ligne qui disparaissent, indentation qui change). Faites-y attention !
>
> Ce TP mêle explications pour vous faire comprendre ce qui est fait, et phase de manipulation ou code. Ces phases sont appelées "**:writing_hand:Hands on**". C'est à ce moment-là que vous devez faire ce qui est écrit dans le TP. Les explications de ce TP ne doivent pas prendre le pas sur celles de votre intervenant. Prenez-les comme une base de connaissance pour plus tard, mais préférez toujours les explications orales, surtout pour poser des questions.

Dans ce TP vous allez :

- Revoir des notions de base de données relationnelles ;

- Implémenter le patron de conception DAO ;
- Voir si votre programme fonctionne avec des tests unitaires reproductibles.

## 1 Mise en place

- Récupérez le code de base pour le TP3

  ````shell
  git pull
  git add .
  git commit -m "TP 2"
  git checkout Tp3_base
  
  # si vous n'avez pas le code du TP
  git clone https://gitlab.com/remi2J/complement_info_ensai_2021_2022.git
  cd complement_info_ensai_2021_2022
  git checkout Tp3_base
  ````
  
- Ou prenez l'archive sur Moodle

- Installez toutes les dépendances nécessaires au TP

  ```shell
pip install -r requirements.txt 
  ```
  
  (potentiellement il faut mettre pip3 en fonction de votre installation)

- Dans le fichier `.env` à la racine du projet fixez les valeurs suivantes :

  - host = sgbd-eleves.domensai.ecole
  - port = 5432
  - database = votre idep
  - user = votre idep
  - password = votre idep

- Dans le fichier `script_bdd.sql` dans le dossier ressources vous trouverez un script sql à exécuter pour initialisez votre base. Ce script est à lancer sur votre base de postgres de l'Ensai (accessible uniquement depuis votre VM ou le wifi Ensai) disponible sur l'ENT ou le lien suivant [postgresEnsai](http://sgbd-eleves.domensai.ecole/phppgadmin) ou via DBeaver. Pour rappel votre nom d'utilisateur et votre mot de passe pour accéder au service sont tous deux votre IDEP Ensai.

  - Pour utiliser DBeaver (client de base de données), dans la barre de recherche de votre VM tapez DBeaver. Si un fenêtre vous demande d'installer des maj, fermez-la. Ensuite cliquez sur `Base de données` (dans le bandeau du haut), puis `nouvelle connexion`. Choisissez PostgreSQL, installer les drivers, puis dans la fenêtre Connection Settings rentrez :
    - Host : sgbd-eleves.domensai.ecole

    - Database : votre idep

    - Nom d'utilisateur :votre idep

    - Mot de passe : votre idep

  - Pour avoir accès à une fenêtre de code SQL, appuyer sur F3. Pour lancer une requête appuyer sur le bouton play ou `ctrl+entrée`

- Vérifiez que l'interpréteur est bien configuré et lancez les tests du projet en tapant dans le terminal de VS code

  ```shell
  python -m unittest
  ```


## 2 Data Access Objet (DAO)

###  2.1 Modélisation

Reprenons le diagramme de classe du TP 1et limitons nous à la partie "attaque" (pas les *Pokémons*) et réfléchissons où mettre une méthode qui permet de persister les attaques.

````mermaid
classDiagram

class AbstractAttack{
	<<abstract>>
	+ DATABASE_TYPE_LABEL : str
	# _id : int
	# _power : int
	# _name : str
	# _description : str
	+compute_damage(APkm, APkm)$  int
	}
	class FixedDamageAttack{
		+ compute_damage(APkm,APkm )  int
	}
    class AbstractFormulaAttack{
    <<abstract>>
		-get_attack_stat(APkm)$  float
		-get_defense_stat(APkm)$  float
		+compute_damage(APkm,APkm)  int
	}
	
    class PhysicalAttack{
		-get_attack_stat(APkm)  float
		-get_defense_stat(APkm)  float
	}
	
    class SpecialAttack{
		-get_attack_stat(APkm)  float
		-get_defense_stat(APkm)  float
	}
	
	FixedDamageAttack--|>AbstractAttack
	AbstractFormulaAttack--|>AbstractAttack
	SpecialAttack--|>AbstractFormulaAttack
	PhysicalAttack--|>AbstractFormulaAttack


````

Vu que les attributs de nos attaques sont similaires on ne va pas coder ça dans les classes spécifiques des attaques. On pourrait mettre les méthodes dans `AbstractAttack`.  Ça fonctionnerait bien d'ailleurs. On aurait une classe unique avec nos méthodes pour interagir avec la base. Mais on ne va pas faire ça !

Et là vous êtes en droit de vous demander 

>  :scream: Mais pourquoi ???

Et la réponse est

> :stuck_out_tongue: Car ça n'a aucun sens !

Revenons sur la phrase : **faible couplage, forte cohésion**. Si on met toutes les méthodes de persistance de nos attaques dans la classe `AbstractAttack` on va avoir une classe qui :

 - :heavy_check_mark: Détermine le comportement des attaques. C'est exactement ce que l'on souhaite (**forte cohésion**).
 - :x: Détermine comment on persiste une attaques.

  Mais ça, **ce n'est pas de la responsabilité d'une attaque, mais du système de persistance choisi, **ou du moins de **l'intermédiaire entre nos objets et le système de persistance** ! Je n'ai personnellement pas envie d'aller modifier ma classe `AbstractAttack` uniquement car j'ai décidé de changer de système de gestion de la persistance. Je risque de modifier quelque chose que je ne devrais pas et créer des régressions (= faire apparaitre des erreurs sur un code qui n'en avait pas avant) dans mon code. Or j'aimerais bien limiter les sources d'erreur car je sais que j'en commets facilement.

À la place on va créer une classe qui va s'occuper uniquement de cette tâche. Et on appelle ce type de classe DAO pour **Data Access Object**. C'est une classe technique qui va faire **l'interface entre nos données stockées et notre application**. Voilà ce que cela donne en terme de diagramme de classe

````mermaid
classDiagram

class AbstractAttack{
	<<abstract>>
	+ DATABASE_TYPE_LABEL : str
	# _id : int
	# _power : int
	# _name : str
	# _description : str
	+compute_damage(APkm, APkm)$  int
	}
	class FixedDamageAttack{
		+ compute_damage(APkm,APkm )  int
	}
    class AbstractFormulaAttack{
    <<abstract>>
		-get_attack_stat(APkm)$  float
		-get_defense_stat(APkm)$  float
		+compute_damage(APkm,APkm)  int
	}
	
    class PhysicalAttack{
		-get_attack_stat(APkm)  float
		-get_defense_stat(APkm)  float
	}
	
    class SpecialAttack{
		-get_attack_stat(APkm)  float
		-get_defense_stat(APkm)  float
	}
	
	FixedDamageAttack--|>AbstractAttack
	AbstractFormulaAttack--|>AbstractAttack
	SpecialAttack--|>AbstractFormulaAttack
	PhysicalAttack--|>AbstractFormulaAttack


class AttackDao{
<<Singleton>>
 +create(AbstractAttack) AbstractAttack
 +find_by_id(str) AbstractAttack
 +find_all() List[AbstractAttack]
 +update(AbstractArme) AbstractAttack
 +delete(AbstractArme) bool
}

class DBConnection{
<<Singleton>>
-__connection : Connection

+connection() Connection
}

AbstractAttack<.. AttackDao: create
AttackDao..> DBConnection: use

````

### 2.2 Gestion des connexions et patern singleton

Pour vous connecter à la base de données nous allons utiliser la bibliothèque python `psycopg2` ([doc](https://www.psycopg.org/docs/index.html)). C'est elle qui va établir la connexion avec la base, envoyer nos requêtes et nous retourner les résultats. Mais il faut faire un peu attention à la gestion des connexions. Car on pourrait se retrouver à ouvrir des centaines de connexions rapidement et dégrader les performances de notre application. C'est le travail de la classe `DBConnection`. Comme c'est un singleton, il y aura une seule instance de cette classe dans toute notre application, et comme c'est elle qui se connecte à la base on s'assure de l'unicité de la connexion.

>  Cette classe est une solution purement technique alors n'hésitez pas à la réutiliser pour votre projet. Le code de la classe est bien documenté pour les personnes intéressées. Elle introduit un concept avancé de POO, à savoir les méta classes. Une méta classe permet de modifier le comportement d'une classe à un niveau poussé (par exemple modifier comment les objets sont construits par python). À moins que vous ayez une appétence tout particulière pour l'informatique, ne passez pas de temps sur ce sujet.

### 2.3 DAO et CRUD

Si vous faites attention, les méthodes de notre DAO ressemblent à celles du CRUD. C'est normal car c'est dans ces méthodes que le code SQL va être stocké, donc il nous faut les méthodes de bases. Néanmoins pour gagner du temps rien n'empêche de créer des méthodes plus complexes. Par exemple il y a deux méthodes pour lire des données :

- `find_by_id()` : qui retourne juste l'enregistrement avec l'id souhaité ;
- `find_all()` : qui va retourner toute une table.

Mais on pourrait imaginer plus de méthode si elles nous sont utiles. Ainsi la liste proposée n'est en rien absolue, elle doit être adaptée à vos besoins.

Voici la fonctionnement général d'une des méthodes de la DAO (avec un exemple de code)

````python
def create_attack(attack) -> AbstractAttack:
    # Etape 1 : On récupère une connexion en utilisant la classe DBConnection. La connexion permet la communication avec la base
    connection = DBConnection().connection 
    # Etape 2 : à partir de la connexion on fait un curseur pour la requête (cf doc). Le curseur permet à python de communiquer avec la base
    with connection.cursor() as cursor : 
        # Etape 3 : on exécute notre requête SQL. Les %()s vont être remplacés par les valeurs passées dans la seconde partie du execute. On laisse psycopg faire l'échappement des caractères pour nous.
        curseur.execute(
            "INSERT INTO arme (power, attack_name, attack_description)"
            " VALUES (%(power)s, %(name)s, %(description)s) RETURNING id_attack;"
            , {
                "power" : attack.power,
                "name" : attack.name
                "description" : attack.description
            })
        # Etape 4 (optionnelle) : on récupère le résultat de la requête
        attack.id = curseur.fetchone()[0]
    return attack

````

```python
def find_attack_by_id(self, id: int) -> AbstractAttack:
    # Etape 1 : On récupère une connexion
    connection = DBConnection().connection
    # Etape 2 : à partir de la connexion on fait un curseur pour la requête (cf doc)
    with connection.cursor() as cursor : 
     	# Etape 3 : on exécute notre requête SQL. Les %()s vont être remplacé par les valeurs passé dans la seconde partie du execute. On laisse psycopg faire l'échappement des caractères pour nous.
        cursor.execute(
            "SELECT id_attack,attack_type_name, power,accuracy, element, attack_name, attack_description"
            "\n\tFROM attack JOIN attack_type type ON attack.id_attack_type=type.id_type_attack"
            "\n\t WHERE id_attack=%(id)s"
                , {"id": id})
        # Etape 4 (optionnelle) : on récupère le résultat de la requête
        res = cursor.fetchone()
	# Etape 5 (optionnelle) : on fait des choses avec le résultat de la requête qui se présente tout la forme d'un dictionnaire python avec comme clef les noms des colonnes
    attack = None
    if res is not None:
        # /!\ ce code ne fonctionne pas !
        attack = Attack(
            name=res["attack_name"]
            , id=res["id_attack"]
            , power=res["power"]
            , description=res["attack_description"]
            )
	return attack
```

Pour simplifier vos requêtes vont se présenter sous la forme suivante :

```` python
connection = DBConnection().connection
with connection.cursor() as cursor : 
	cursor.execute(requete_sql)
	res = cursor.fetchone()

#Code métier
    
return something
````

L'objet `cursor` contient un pointeur vers les résultats de votre requête. Ce résultat n'est pas encore rapatrié sur votre machine, mais est stocké par la base de donnée. Vous avez 3 méthodes pour récupérer le résultat :

- `cursor.fetchall()` : retourne l'intégralité des résultats sous forme d'une liste de dictionnaires. Les dictionnaires sont les lignes récupérées. Les clefs du dictionnaire sont les colonnes récupérées. Cette méthode fonctionne très bien quand on veut tous les résultats en une fois et qu'il y en a peu. Quand on a des millions d'enregistrements cela va poser problème car :

  - Le transfert de données sur internet va prendre du temps et bloquer notre application ;
  - Notre application va devoir gérer une grande quantité de données, et elle en est peut-être incapable.

  Dans le cas des projets `cursor.fetchall()` ne devrait pas poser de problème, mais garder ce genre de problématique en tête.

   Pour traiter ce tableau :

  ````python
  records = curseur.fetchall()
  attacks = [] 
  for row in records : # boucle sur les lignes du tableau
      armes.append(Attack(row["id"], row["name"]...)) #row["key"] = la valeur pour la colonne key
  ````

- `curseur.fetchmany(size)`: retourne autant d'enregistrements que demandé sous forme d'une liste de dictionnaires. Elle permet de contrôler le volume de données que l'on traite. Si vous appelez de nouveau `fetchmany(size)` sur votre curseur vous allez récupérer les lignes suivantes (vous obtenez un système de pagination). La contrepartie est que cela demande de garder le curseur ouvert. Le résultat ce traite de la même manière que précédemment ; 

- `curseur.fetchone()` : retourne uniquement un enregistrement sous forme de dictionnaire Si vous appelez de nouveau  `fetchone()` sur le même curseur vous obtiendrez la ligne suivante.

Pour plus d'information : [article de pynative](https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/)

### ✍Hand on 1 : DAO avec des types d'attaque

![](image tp3/table attaque.png)

- Créez une classe `TypeAttackDao` pour récupérer les id des attaques. Vous créerez deux méthodes :
  - `find_id_by_label` pour retourner l'id d'un type d’attaque ;
  - `find_all`pour retourner le tableau de tous les types d'attaque ;
- Créez la classe `AttaqueDao` avec les méthodes :
  - `find_all_attack(limit:int, offset:int) -> List[AbsractAttack]` : retourne qui fait une requête SELECT à la base de donnée avec un paramètre LIMITE égale à `limit` et un paramètre `OFFSET`  égale à `offset`.
  - `find_attack_by_id(id:int) -> Optional[AbsractAttack]` : retourne l'attaque avec l'id en paramètre ou retourne None si l'attaque n'est pas trouvée.
  - `add_attack(attack : AbstractAttack) -> bool` : ajoute une attaque en base et retourne si l'ajout s'est bien passé.
  - `update_attack(attack : AbstractAttack) -> bool` : met à jour les données de l'attaques passée en paramètre et retourne si la modification s'est bien passée.

Voici quelques conseils :

- Vous pouvez utiliser l'attribut la property  `type` de chaque attaque pour avoir son label en base ;
- Vous trouverez une classe `AttackFactory` pour instancier facilement des attaques
- Pensez à faire des tests pour voir si votre code fonctionne.

### ✍Hand on 2 : Pokémon DAO

Créez la classe Pokémon DAO avec les méthodes suivantes :

- `find_all_pokemon()->List[AbstractPokemon]` : retourne tous les pokémons dans la base
- `find_pokemon_by_name(name:str)->AbstractPokemon` : retourne un pokémon avec le nom donné. Ce pokémon doit être le plus complet possible et donc avoir sa liste d'attaques. Pour faire cela :
  - Récupérez toutes les informations possibles de la table pokémon
  - Faites une requête en joignant les tables `attack` et `pokemon_attack` en filtrant avec l'id du pokémon
  - Générez les attaques à partir de là

![](image tp3/schéma de base.png)

### ✍Hand on 3 : DAO et webservice

Vous allez maintenant rendre accessible les données de votre base à des d'autres utilisateurs en réalisant un webservice REST. En vous basant sur ce code implémentez un webservice qui expose les endpoints suivants :

```python
# Import classique
from fastapi import FastAPI
import uvicorn

# On instancie le webservice
app = FastAPI()

# Défintion du endpoint get /attack?limit=100
@app.get("/attack/")
async def get_all_attacks(limit:int):
    # Vous devez récupérer les attaques en base en utilisant votre DAO
    return attacks

# Défintion du endpoint get /pokemon?limit=100
@app.get("/pokemon/")
async def get_all_pokemons(limit:int):
    # Vous devez récupérer les pokemons en base en utilisant votre DAO
    return pokemons

# Défintion du endpoint get /pokemon`/{name}
@app.get("/pokemon/{name}")
async def get_pokemon_by_name(name:str):
    # Vous devez récupérer le pokemon en base en utilisant votre DAO
    return pokemon

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
```

- `GET localhost:80/attack?limit=100` renverra une liste de 100 attaques par défaut. Il est possible de moduler cette valeur via le paramètre de requête `limit`
- `GET localhost:80/pokemon?limit=100`. Il renverra une liste de 100 *pokémons* par défaut, mais peut être modulé avec le paramètre de requête `limite`. 
- `GET localhost:80/pokemon/{nom}`. Il renverra un json représentant un *pokémon*.

Pour retourner des objets, vous allez devoir définir des classes héritant de `BaseModel`. Vous trouverez toutes les infos dans la documentation de FastAPI.

## 4 Conclusion

Dans ce TP vous avez implémenté votre première DAO. C'est une classe technique qui sert à communiquer avec votre système de persistance de données. L'avantage premier de faire une classe à part est de découpler au maximum la gestion du système de persistance et le code métier de votre application. Si vous décidez d'arrêter d'utiliser une base de données relationnelle et préférez désormais une base de données *no SQL* vous allez devoir changer uniquement les classes DAO tout en exposant toujours les mêmes méthodes.
