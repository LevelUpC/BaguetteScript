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

    while i < len(lignes):
        ligne = lignes[i].strip()

        if ligne == "" or ligne.startswith("#"):
            i += 1
            continue

        # Importer un module Python
        if ligne.startswith("importer "):
            nom_module = ligne.split(" ")[1].strip()
            try:
                globals()[nom_module] = __import__(nom_module)
            except ImportError:
                print(f"Erreur : le module '{nom_module}' est introuvable.")
            i += 1
            continue

        # Bloc conditionnel
        if ligne.startswith("si "):
            bloc_complet = [ligne]
            i += 1
            while i < len(lignes) and lignes[i].strip() != "fin":
                bloc_complet.append(lignes[i])
                i += 1
            i += 1

            bloc_exécuté = False
            j = 0
            while j < len(bloc_complet):
                ligne_cond = bloc_complet[j].strip()

                if ligne_cond.startswith("si "):
                    condition = ligne_cond[3:].split(" alors")[0]
                    if evaluer_expression(condition):
                        j += 1
                        while j < len(bloc_complet) and not bloc_complet[j].strip().startswith(("sinon si", "sinon")):
                            interpreter_lignes([bloc_complet[j]])
                            j += 1
                        bloc_exécuté = True
                        break

                elif ligne_cond.startswith("sinon si "):
                    condition = ligne_cond[9:].split(" alors")[0]
                    if not bloc_exécuté and evaluer_expression(condition):
                        j += 1
                        while j < len(bloc_complet) and not bloc_complet[j].strip().startswith(("sinon si", "sinon")):
                            interpreter_lignes([bloc_complet[j]])
                            j += 1
                        bloc_exécuté = True
                        break

                elif ligne_cond.startswith("sinon"):
                    if not bloc_exécuté:
                        j += 1
                        while j < len(bloc_complet):
                            interpreter_lignes([bloc_complet[j]])
                            j += 1
                        break

                j += 1
            continue

        # Variables
        if ligne.startswith("var "):
            nom, valeur = ligne[4:].split(" = ")
            variables[nom.strip()] = evaluer_expression(valeur)

        # Affectation
        elif "=" in ligne and not ligne.startswith(("tantque ", "pour ", "avec ")):
            nom, valeur = ligne.split(" = ")
            variables[nom.strip()] = evaluer_expression(valeur)

        # Affichage
        elif ligne.startswith("montrer ") or ligne.startswith("écrire "):
            contenu = ligne.split(" ", 1)[1]
            print(evaluer_expression(contenu))

        # tantque
        elif ligne.startswith("tantque "):
            condition = ligne[8:].split(" faire")[0]
            bloc = []
            i += 1
            while lignes[i].strip() != "fin":
                bloc.append(lignes[i])
                i += 1
            while evaluer_expression(condition):
                interpreter_lignes(bloc)

        # pour i de ... à ...
        elif re.match(r"pour\s+\w+\s+de\s+.+\s+à\s+.+\s+faire", ligne):
            match = re.match(r"pour\s+(\w+)\s+de\s+(.+?)\s+à\s+(.+?)\s+faire", ligne)
            var_name = match.group(1)
            start = int(evaluer_expression(match.group(2)))
            end = int(evaluer_expression(match.group(3)))
            bloc = []
            i += 1
            while lignes[i].strip() != "fin":
                bloc.append(lignes[i])
                i += 1
            for val in range(start, end + 1):
                variables[var_name] = val
                interpreter_lignes(bloc)
            del variables[var_name]
            i += 1
            continue

        # pour x dans liste
        elif re.match(r"pour\s+\w+\s+dans\s+\w+\s+faire", ligne):
            match = re.match(r"pour\s+(\w+)\s+dans\s+(\w+)\s+faire", ligne)
            var_name = match.group(1)
            list_name = match.group(2)
            liste = variables.get(list_name, [])
            if not isinstance(liste, list):
                print(f"Erreur : {list_name} n’est pas une liste.")
                i += 1
                continue
            bloc = []
            i += 1
            while lignes[i].strip() != "fin":
                bloc.append(lignes[i])
                i += 1
            for element in liste:
                variables[var_name] = element
                interpreter_lignes(bloc)
            del variables[var_name]
            i += 1
            continue

        # avec ... comme ... faire
        elif re.match(r"avec\s+(.+?)\s+comme\s+(\w+)\s+faire", ligne):
            match = re.match(r"avec\s+(.+?)\s+comme\s+(\w+)\s+faire", ligne)
            contexte_expr = match.group(1)
            var_name = match.group(2)
            bloc = []
            i += 1
            while lignes[i].strip() != "fin":
                bloc.append(lignes[i])
                i += 1
            with eval(evaluer_expression(contexte_expr)) as ctx:
                variables[var_name] = ctx
                interpreter_lignes(bloc)
                del variables[var_name]
            i += 1
            continue

        # fonction
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

        # appel de fonction
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

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Utilisation : python baguette.py fichier.bgsc")
    else:
        charger_et_executer(sys.argv[1])
