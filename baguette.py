import re

variables = {}
fonctions = {}

def evaluer_expression(expr):
    expr = expr.strip()
    for nom in variables:
        if isinstance(variables[nom], str):
            expr = re.sub(rf"\b{nom}\b", f'"{variables[nom]}"', expr)
        else:
            expr = re.sub(rf"\b{nom}\b", str(variables[nom]), expr)
    try:
        return eval(expr)
    except Exception:
        return expr.strip('"')

def interpreter_lignes(lignes):
    i = 0
    pile_blocs = []

    while i < len(lignes):
        ligne = lignes[i].strip()

                # Importer un module Python
        if ligne.startswith("importer "):
            nom_module = ligne.split(" ")[1].strip()
            try:
                globals()[nom_module] = __import__(nom_module)
            except ImportError:
                print(f"Erreur : le module '{nom_module}' est introuvable.")
            i += 1
            continue

        if ligne == "" or ligne.startswith("#"):
            i += 1
            continue

        # Variables
        if ligne.startswith("var "):
            nom, valeur = ligne[4:].split(" = ")
            variables[nom.strip()] = evaluer_expression(valeur)

        # Affectation
        elif "=" in ligne and not ligne.startswith(("si ", "tantque ", "pour ")):
            nom, valeur = ligne.split(" = ")
            variables[nom.strip()] = evaluer_expression(valeur)

        # Affichage
        elif ligne.startswith("montrer ") or ligne.startswith("écrire "):
            contenu = ligne.split(" ", 1)[1]
            print(evaluer_expression(contenu))

        # Condition SI
        elif ligne.startswith("si "):
            condition = ligne[3:].split(" alors")[0]
            if evaluer_expression(condition):
                pile_blocs.append("si")
            else:
                while not lignes[i].strip().startswith(("sinon", "sinon si", "fin")):
                    i += 1
                continue

        # SINON SI
        elif ligne.startswith("sinon si "):
            if pile_blocs and pile_blocs[-1] == "si":
                i += 1
                continue  # Si un "si" a déjà été exécuté, on saute
            condition = ligne[9:].split(" alors")[0]
            if evaluer_expression(condition):
                pile_blocs.append("si")
            else:
                while not lignes[i].strip().startswith(("sinon", "fin")):
                    i += 1
                continue

        # SINON
        elif ligne.startswith("sinon"):
            if pile_blocs and pile_blocs[-1] == "si":
                i += 1
                continue  # Si un bloc si a été traité, on saute
            else:
                pile_blocs.append("si")

        # FIN (si, boucle, fonction)
        elif ligne == "fin":
            if pile_blocs:
                pile_blocs.pop()

        # Tant que
        elif ligne.startswith("tantque "):
            condition = ligne[8:].split(" faire")[0]
            bloc = []
            i += 1
            while lignes[i].strip() != "fin":
                bloc.append(lignes[i])
                i += 1
            while evaluer_expression(condition):
                interpreter_lignes(bloc)

        # Fonction - définition
        elif ligne.startswith("fonction "):
            nom_fct = re.findall(r"fonction\s+(\w+)", ligne)[0]
            params = re.findall(r"\((.*?)\)", ligne)
            params = params[0].split(",") if params else []
            params = [p.strip() for p in params]
            bloc = []
            i += 1
            while lignes[i].strip() != "fin":
                bloc.append(lignes[i])
                i += 1
            fonctions[nom_fct] = (params, bloc)

        # Appel de fonction
        elif "(" in ligne and ")" in ligne:
            nom_fct = ligne.split("(")[0]
            args = ligne.split("(", 1)[1].rstrip(")").split(",")
            args = [evaluer_expression(a.strip()) for a in args]
            if nom_fct in fonctions:
                params, bloc = fonctions[nom_fct]
                sauvegarde = variables.copy()
                for p, a in zip(params, args):
                    variables[p] = a
                interpreter_lignes(bloc)
                variables.update(sauvegarde)

        i += 1

def charger_et_executer(fichier_bgsc):
    with open(fichier_bgsc, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    interpreter_lignes(lignes)

# Exemple d'exécution : charger_et_executer("exemple.bgsc")
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Utilisation : python baguette.py fichier.bgsc")
    else:
        charger_et_executer(sys.argv[1])
