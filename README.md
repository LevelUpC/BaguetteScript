# Baguette Script

**Baguette Script** est un langage de programmation conçu entièrement en français, offrant une approche intuitive et accessible à la programmation. Oubliez la barrière de la langue et codez dans votre langue maternelle avec des mots-clés familiers et une syntaxe claire.

Cette extension VS Code apporte le support du langage Baguette Script, incluant la coloration syntaxique pour rendre votre code plus lisible et agréable à écrire.

## Caractéristiques

* **Coloration Syntaxique :** Profitez d'une coloration syntaxique complète pour tous les éléments du langage Baguette Script, y compris :
    * Mots-clés (`var`, `si`, `tantque`, `fonction`, etc.)
    * Chaînes de caractères
    * Nombres
    * Opérateurs
    * Commentaires
* **Support des Fichiers `.bgsc` :** L'extension reconnaît automatiquement les fichiers avec l'extension `.bgsc` comme du code Baguette Script.

## Exemples de Syntaxe

Voici un aperçu de la syntaxe de Baguette Script :

### Déclaration et Variables

```baguette
var x = 5
var nom = "Jean"
x = x + 2
```

### Affichage Console

```baguette
montrer "Bonjour le monde"
montrer x
montrer "Le résultat est : " + x
```

### Conditions (Si/Sinon)

```baguette
si x > 10 alors
    écrire "x est grand"
sinon si x > 5 alors
    écrire "x est moyen"
sinon
    écrire "x est petit"
fin
```

### Boucles

#### `tantque`

```baguette
var x = 0

tantque x < 5 faire
    montrer x
    x = x + 1
fin
```

#### `pour`

```baguette
pour i de 1 à 5 faire
    écrire i
fin
```

### Opérateurs

  * **Mathématiques :** `+`, `-`, `*`, `/`, `%`, `**` (puissance), `//` (division entière)
  * **Comparaison :** `==`, `!=`, `>`, `<`, `>=`, `<=`
  * **Logiques :** `et`, `ou`, `non`

### Chaînes de Caractères

```baguette
var nom = "Marie"
montrer "Bonjour " + nom
```

### Fonctions

#### Définition

```baguette
fonction saluer(nom)
    montrer "Salut " + nom
fin
```

#### Appel

```baguette
saluer("Luc")
```

### Commentaires

```baguette
# Ceci est un commentaire
```

### Listes (Tableaux)

```baguette
var fruits = ["pomme", "banane", "raisin"]
montrer fruits[0] # Affiche "pomme"
```

## Installation

1.  Ouvrez VS Code.
2.  Allez dans la vue Extensions (`Ctrl+Shift+X` ou `Cmd+Shift+X`).
3.  Recherchez "Baguette Script".
4.  Cliquez sur "Installer".

Alternativement, si vous avez le fichier `.vsix` :

1.  Dans VS Code, allez dans la vue Extensions.
2.  Cliquez sur les trois points `...` en haut à droite.
3.  Sélectionnez "Install from VSIX...".
4.  Naviguez jusqu'à votre fichier `.vsix` et sélectionnez-le.
