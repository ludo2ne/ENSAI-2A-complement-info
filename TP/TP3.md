# TP 3: Data Access Objet (DAO)

## :arrow_forward: 0. Avant de commencer

> :scream: Comme vous pouvez le constater le sujet de ce TP est lui aussi long. Cela ne doit pas vous effrayer. Il mélange explications complètes et manipulations pour être au maximum autosuffisant. **Vous n'allez surement pas terminer le sujet, ce n'est pas grave. Il est là pour vous aider lors du projet informatique.**
>
> Ce TP mêle explications pour vous faire comprendre ce qui est fait, et phases de manipulation ou code. Ces phases sont appelées "**:writing_hand:Hands on**". C'est à ce moment-là que vous devez faire ce qui est écrit dans le TP. Les explications de ce TP ne doivent pas prendre le pas sur celles de votre intervenant. Prenez-les comme une base de connaissances pour plus tard, mais préférez toujours les explications orales.

Dans ce TP vous allez :

* Revoir des notions de base de données relationnelles ;
* Implémenter le patron de conception DAO ;
* Voir si votre programme fonctionne avec des tests unitaires reproductibles.


## :arrow_forward: 1. Mise à jour de votre dépôt local

Comme lors du précédent TP, vous avez 2 possibilités pour récupérer le code de base du TP3 : 

#### :arrow_right: Si vous voulez repartir du code du TP2 

* Ouvrez **Visual Studio Code**
    * File > Open Folder
        * Allez dans `/p/Cours2A/UE3_Complements_informatique/TP/TP2`
        * cliquez une fois sur **ENSAI-2A-complement-info-TP**
        * puis sur le bouton **Sélectionner un dossier**
    * Ouvrez un Terminal Git Bash dans VSCode (Terminal > New terminal)
    * Créez un point de sauvegarde de vos travaux de la semaine dernière
        * `git add .`
        * `git commit -m "Mon super code du TP2"`
    * Mettez à jour votre dépôt local
        * `git pull`

#### :arrow_right: Si vous n'avez pas le code du TP2 sur votre machine

* Ouvrez le logiciel **Git Bash**
    * Créez un dossier pour stocker le code du TP
        * par exemple, copiez la ligne ci-dessous, et collez là dans Git Bash (clic droit > Paste)
        * `mkdir -p /p/Cours2A/UE3_Complements_informatique/TP/TP3 && cd $_`
    * Clonez le dépôt
        * `git clone https://github.com/ludo2ne/ENSAI-2A-complement-info-TP.git`
    * Fermez **Git Bash**
* Ouvrez **Visual Studio Code**
    * File > Open Folder
        * Allez dans `/p/Cours2A/UE3_Complements_informatique/TP/TP2`
        * cliquez une fois sur **ENSAI-2A-complement-info-TP**
        * puis sur le bouton **Sélectionner un dossier**
    * Ouvrez un Terminal Git Bash dans VSCode (Terminal > New terminal)

---

#### :warning: Attention quand vous faites Open Folder dans VSCode

Le dossier parent de l'explorer de VSCode (à gauche) doit être : **ENSAI-2A-complement-info-TP**. 
Si c'est TP1, TP2, TP3, TP ou autre chose ce n'est pas bon ! Vous allez avoir des soucis d'imports par la suite.

---

#### :arrow_right: Dans les 2 cas

* Passez sur la branche du TP3
    * `git checkout tp3_base`
* Si ce n'est pas déjà fait, installez les dépendances nécessaires (voir fichier README)
    * `pip install -r requirements.txt`
* pour pour vérifier que tout fonctionne bien
    * lancez le fichier `__main__.py`
    * lancez les tests unitaires
        * dans terminal : `python -m unittest`
* Pour pouvoir vous connecter à votre base de données, renseignez les variables du fichier **.env** avec votre id : 
    * `DATABASE=id????`
    * `USER=id????`
    * `PASSWORD=id????`
* Lancez le script `utils/reset_database.py`
    * cela crée un schéma et des données utiles pour ce TP
* Ouvrez **DBeaver** pour une remise en jambes en SQL
    * Si vous n'êtes pas familier avec DBeaver, suivez ces [instructions](https://github.com/ludo2ne/ENSAI-2A-remise-a-niveau/blob/main/SQL/DBeaver.md)
    * observez ces tables et leurs liens : `tp.pokemon`, `tp.pokemon_type`, `tp.attack`, `tp.attack_type`, `tp.pokemon_attack` (schéma dans TP/images/)
    * écrivez des requêtes pour : 
        * [ ] lister toutes les attaques, ainsi que le nom du type d'attaque 
        * [ ] lister tous les pokemon, ainsi que le nom du type de Pokemon
        * [ ] lister toutes les attaques de Pikachu 
    * gardez ces requêtes de coté, elles seront utiles plus loin


---


## :arrow_forward: 2. Data Access Objet (DAO)

### :small_orange_diamond:  2.1 Modélisation


Reprenons le diagramme de classe du TP1. Limitons nous à la partie "attaque" et réfléchissons où mettre une méthode qui permet de persister les attaques.

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

Vu que les attributs de nos attaques sont similaires, on ne va pas coder ça dans les classes spécifiques des attaques. On pourrait mettre les méthodes dans `AbstractAttack`.  Ça fonctionnerait bien d'ailleurs. On aurait une classe unique avec nos méthodes pour interagir avec la base. Mais on ne va pas faire ça !

Et là vous vous demandez : 

>  :scream: Mais pourquoi ???

Et la réponse est :

> :stuck_out_tongue: Car ça n'a aucun sens !

Revenons sur la phrase : **faible couplage, forte cohésion**. Si l'on met toutes les méthodes de persistance de nos attaques dans la classe `AbstractAttack` on va avoir une classe qui :

 - :heavy_check_mark: Détermine le comportement des attaques. C'est exactement ce que l'on souhaite (**forte cohésion**).
 - :x: Détermine comment on persiste une attaques.

  Mais ça, **ce n'est pas de la responsabilité d'une attaque, mais du système de persistance choisi,** ou du moins de **l'intermédiaire entre nos objets et le système de persistance** ! 
  
  Je n'ai personnellement pas envie d'aller modifier ma classe `AbstractAttack` uniquement car j'ai décidé de changer de système de gestion de la persistance. Je risque de modifier quelque chose que je ne devrais pas et créer des régressions (faire apparaitre des erreurs sur un code qui n'en avait pas avant) dans mon code. Or j'aimerais bien limiter les sources d'erreurs.

À la place, nous allons créer une classe qui va s'occuper uniquement de cette tâche. Et on appelle ce type de classe DAO pour **Data Access Object**. C'est une classe technique qui va faire **l'interface entre nos données stockées et notre application**. Voilà ce que cela donne en terme de diagramme de classe

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
 +find_by_id(int) AbstractAttack
 +find_all() List[AbstractAttack]
 +update(AbstractAttack) AbstractAttack
 +delete(AbstractAttack) bool
}

class DBConnection{
<<Singleton>>
-__connection : Connection

+connection() Connection
}

AbstractAttack<.. AttackDao: create
AttackDao..> DBConnection: use

````

### :small_orange_diamond: 2.2 Gestion des connexions et patern singleton

Pour vous connecter à la base de données nous allons utiliser la bibliothèque python [**psycopg2**](https://www.psycopg.org/docs/index.html). C'est elle qui va établir la connexion avec la base, envoyer nos requêtes et nous retourner les résultats. 

Mais il faut faire un peu attention à la gestion des connexions. Car nous pourrions nous retrouver à ouvrir des centaines de connexions rapidement et dégrader les performances de notre application. C'est le travail de la classe `DBConnection`. Comme c'est un singleton, il y aura une seule instance de cette classe dans toute notre application, et comme c'est elle qui se connecte à la base on s'assure de l'unicité de la connexion.

>  Cette classe est une solution purement technique alors n'hésitez pas à la réutiliser pour votre projet. Elle introduit un concept avancé de POO, à savoir les méta classes. Une méta classe permet de modifier le comportement d'une classe à un niveau poussé (par exemple modifier comment les objets sont construits par python). À moins que vous ayez une appétence tout particulière pour l'informatique, ne passez pas de temps sur ce sujet.

### :small_orange_diamond: 2.3 DAO et CRUD

Si vous faites attention, les méthodes de notre DAO ressemblent à celles du CRUD. C'est normal car c'est dans ces méthodes que le code SQL va être stocké, donc il nous faut les méthodes de base, généralement :

* `find_all()` : qui va retourner toute la table.
* `find_by_id()` : qui retourne un enregistrement à partir de son id
* `create()` : qui crée un nouvel enregistrement
* `delete()` : qui supprime un enregistrement
* `update()` : qui met à jour un enregistrement

Ces 5 méthodes suffisent pour communiquer avec votre base de données. Vous pouvez effectuer le reste des traitements dans vos classes **Service**. Néanmoins pour gagner du temps rien n'empêche de créer des méthodes plus complexes (ex : `find_by_type_and_level_order_by_name_desc()`)

Voici la fonctionnement général d'une des méthodes de la DAO :

```` python
# Etape 1 : On récupère une connexion en utilisant la classe DBConnection.
connection = DBConnection().connection

# Etape 2 : à partir de la connexion on fait un curseur pour la requête 
with connection.cursor() as cursor : 
    
    # Etape 3 : on exécute notre requête SQL.
    cursor.execute(requete_sql)
    
    # Etape 4 : on stocke le résultat de la requête
    res = cursor.fetchall()

if res:
    # Etape 5 : on agence les résultats selon la forme souhaitée (liste...)
    
return something
````

L'objet `cursor` contient un pointeur vers les résultats de votre requête. Ce résultat n'est pas encore rapatrié sur votre machine, mais est stocké par la base de données. Vous avez 3 méthodes pour récupérer le résultat :

- `curseur.fetchone()` : retourne uniquement un enregistrement sous forme de dictionnaire. Si vous appelez de nouveau `fetchone()` sur le même curseur vous obtiendrez la ligne suivante
- `cursor.fetchall()` : retourne l'intégralité des résultats sous forme d'une liste de dictionnaires. 
    - Les dictionnaires sont les lignes de la table récupérée. 
    - Les clés du dictionnaire sont les colonnes récupérées. 
    - Cette méthode fonctionne très bien quand on veut tous les résultats en une fois et qu'il y en a peu. Quand on a des millions d'enregistrements cela va poser problème car :
        - Le transfert de données sur internet va prendre du temps et bloquer notre application ;
        - Notre application va devoir gérer une grande quantité de données, et elle en est peut-être incapable.
- `curseur.fetchmany(size)`: retourne autant d'enregistrements que demandé sous forme d'une liste de dictionnaires. Cela permet de contrôler le volume de données que l'on traite. Si vous appelez de nouveau `fetchmany(size)` sur votre curseur, vous allez récupérer les lignes suivantes (système de pagination)

Pour plus d'information : [article de pynative](https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/)

---

### :small_orange_diamond: DAO avec des types d'attaque

**✍Hand on 1**

* [ ] Observez le fonctionnement de la classe AttaqueTypeDAO
    * cela va vous être utile pour la suite
* [ ] Dans DBeaver, créez une requête qui retourne le contenu de la table `tp.attack`, ainsi que le champ `attack_type_name` de la table `tp.attack_type`
    * Cette requête servira pour les 2 méthodes `find` ci-après, car pour créer nos objets métier **Attack**, nous avons besoin de connaitre le nom du type d'attaque
* [ ] Dans la classe `AttaqueDao`, créez les méthodes suivantes :
  * [ ] `update_attack(attack : AbstractAttack) -> bool` : met à jour les données de l'attaque passée en paramètre et retourne si la modification s'est bien passée
  * [ ] `find_attack_by_id(id:int) -> Optional[AbsractAttack]` : retourne l'attaque avec l'id en paramètre ou retourne None si l'attaque n'est pas trouvée.
  * [ ] `find_all_attacks() -> List[AbsractAttack]` : qui retourne la liste de toutes les attaques
      * [ ] Bonus : ajoutez à cette méthode les paramètres `limit` et `offset`

Voici quelques conseils :

- Vous pouvez utiliser l'attribut `type` de chaque attaque pour avoir son label en base
- Utilisez la classe `AttackFactory` pour instancier facilement des attaques
- Pensez à faire des tests pour voir si votre code fonctionne

---

### :small_orange_diamond: Pokémon DAO

**✍Hand on 2**

Créez la classe **PokémonDAO** avec les méthodes suivantes :

* [ ] `find_all_pokemon()->List[AbstractPokemon]` : retourne tous les pokémons dans la base
* [ ] `find_pokemon_by_name(name:str)->AbstractPokemon` : retourne un pokémon avec le nom donné. 
* [ ] Complétez la méthode ci-dessus en incorporant la liste des attaques du Pokemon :
  * [ ] Faites une requête en joignant les tables `attack` et `pokemon_attack` en filtrant avec l'id du pokémon
  * [ ] Générez les attaques à partir de là

---

### :small_orange_diamond: DAO et webservice

**✍Hand on 3**

Vous allez maintenant rendre accessible les données de votre base à d'autres utilisateurs en réalisant un webservice REST. 

Ajoutez dans le fichier `app.py` les endpoints suivants :

```python
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
```

* `GET localhost:80/attack?limit=100` renverra une liste de 100 attaques par défaut. Il est possible de moduler cette valeur via le paramètre de requête `limit`
* `GET localhost:80/pokemon?limit=100`. Il renverra une liste de 100 *pokémons* par défaut, mais peut être modulé avec le paramètre de requête `limit`. 
* `GET localhost:80/pokemon/{nom}`. Il renverra un json représentant un *pokémon*.

Pour retourner des objets, vous allez devoir définir des classes héritant de `BaseModel`. Vous trouverez toutes les infos dans la documentation de FastAPI.

---

## :arrow_forward: 4. Conclusion

Dans ce TP vous avez implémenté votre première DAO. 

C'est une classe technique qui sert à communiquer avec votre système de persistance de données. L'avantage premier de faire une classe à part est de découpler au maximum la gestion du système de persistance et le code métier de votre application. 

Si vous décidez d'arrêter d'utiliser une base de données relationnelle et préférez désormais une base de données *no SQL* vous allez devoir changer uniquement les classes DAO tout en exposant toujours les mêmes méthodes.
