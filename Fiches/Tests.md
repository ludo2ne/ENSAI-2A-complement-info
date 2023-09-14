# Les Tests

## :arrow_forward: Pourquoi tester ?

* Pour vérifier que votre programme fonctionne
* Pour détecter  des erreurs
* Pour éviter les régressions (quand vous modifiez du code)

Aucun test n'est parfait, mais cela permet quand même d'écarter de nombreuses erreurs.

Des logiciels permettent de calculer **la couverture de tests** d'une application, c'est-à-dire approximativement le nombre de fonctions testées sur le nombre total de fonctions.  
Cette couverture de tests est un indicateur de qualité. Cependant, elle donne une tendance, plutôt qu'une valeur fiable. En effet, il est facile de tester toutes les méthodes élémentaires pour augmenter mécaniquement sa couverture et de mettre de côté  les tests sur les méthodes plus compliquées.

Préférez faire peu de tests, mais des tests utiles !

## :arrow_forward: Les types de tests

Il existe de très nombreux tests différents, voici les principaux :

* **Test unitaire** : teste une fonction pour vérifier son bon fonctionnement
* Test fonctionnel : teste les cas d'utilisation du logiciel
* Test de charge : évaluent la capacité d'un système à gérer un volume élevé de données ou de transactions
* Test d'intégration : vérifie que différents composants ou modules d'un système interagissent correctement ensemble
* Test d'intrusion : vérifie la sécurité du logiciel en recherchant des vulnérabilités et en simulant des attaques potentielles
* ...

## :arrow_forward: Les tests unitaires

Nous allons utiliser le framework `unittest` pour réaliser nos tests en Python.

Commençons par un exemple : vous souhaitez tester la méthode suivante :

```python
class OperationMathematiques:
    def diviser_cinq_par(self, nombre) -> float:
        if nombre != 0:
            return 5 / nombre
        else:
            return None
```

Pour cela, vous allez créer une classe de test.

Le premier test auquel on pense est le cas nominal : on choisit un nombre en entrée, par exemple 2, puis on vérifie que diviser_cinq_par(2) retourne bien la valeur attendue : 2.5

```python
from unittest import TestCase, TextTestRunner, TestLoader
from mathematiques.operation_mathematique import OperationMathematiques

class TestOperationMathematiques(TestCase):
    def test_diviser_cinq_par_nombre_non_nul(self):
        # GIVEN
        nombre = 2

        # WHEN
        resultat = OperationMathematiques().diviser_cinq_par(nombre)

        # THEN
        self.assertEqual(resultat, 2.5)
```

Mais ce n'est pas suffisant !

La méthode a également un autre retour possible : `None` :arrow_right: il faut aussi tester que la méthode renvoie bien None si le paramètre en entrée est 0

```python
from unittest import TestCase, TextTestRunner, TestLoader
from mathematiques.operation_mathematique import OperationMathematiques

class TestOperationMathematiques(TestCase):
    def test_diviser_cinq_par_nombre_non_nul(self):
        # GIVEN
        nombre = 2

        # WHEN
        resultat = OperationMathematiques().diviser_cinq_par(nombre)

        # THEN
        self.assertEqual(resultat, 2.5)

    def test_diviser_cinq_par_zero(self):
        # GIVEN
        nombre = 0

        # WHEN
        resultat = OperationMathematiques().diviser_cinq_par(nombre)

        # THEN
        self.assertIsNone(resultat)

if __name__ == "__main__":
    # Run the tests
    result = TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestOperationMathematiques)
    )
```

Voici le test complet avec à la fin un **main** optionnel qui permet de lancer la classe de test comme n'importe quel programme Python avec le bouton :arrow_forward:

Et si... on appelle la méthode avec ce paramètre : `diviser_cinq_par("a")` ?

Vous pouvez aussi écrire un test pour vérifier que votre méthode renvoie bien une exception `TypeError` dans ce cas.

```python
    def test_diviser_cinq_string(self):
        # GIVEN
        nombre = "a"

        # WHEN / THEN
        with self.assertRaises(TypeError):
            OperationMathematiques().diviser_cinq_par(nombre)
```

Mais il est quand même préférable de vérifier dans votre méthode que le paramètre est bien de type numérique et de décider quoi faire si ce n'est pas le cas.

:bulb: Ce qu'il faut retenir sur le test unitaire :

* vérifie qu'un méthode fait ce qu'elle doit faire
* il faut tester les cas nominaux, mais également les cas à la marge et les erreurs
* un test unitaire teste UNE et UNE seule chose
  * il faut autant de tests unitaires que de retours possibles
* il doit être le plus isolé possible *(pas de question sur ce point à l'examen)*
  * c'est-à-dire que si vous voulez tester une méthode A, qui elle-même appelle d'autres méthodes B, C, D...
  * le test ne doit se faire que sur la méthode A
  * Pour cela, il faut `mocker` le comportement des autres méthodes

## :arrow_forward: Les Test Driven Development (TDD)

Quand tester ?

...

La meilleure pratique lorsque l'on veut créer une fonction est de d'abord créer les tests qui permettront de vérifier que la fonction fait ce qu'elle doit faire.

Cela peut paraître  un peu étrange, mais en fait pas tant que ça. Lorsque vous codez une fonction, vous savez avant de commencer :

* quels seront les paramètres en entrée
* quels résultats vous attendez en sortie
* donc vous avez déjà quoi tester !

La pratique du TDD a le gros avantage que cela nous force à écrire des tests et de prendre le temps de bien faire les choses. Pour adhérer au TDD il faut vraiment se faire violence au début, mais au final cette pratique est très bénéfique.

Sinon, si l'on écrit la fonction en premier, une fois que l'on a terminé, il y a 9 chances sur 10 que l'on se dise : "c'est bon ça marche, pas la peine de tester...". Et ça c'est pas bien !!!