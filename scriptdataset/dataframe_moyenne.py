import pandas as pd
import ast
import numpy as np

def calculer_moyenne_et_remplacer_partiel(fichier_entree, fichier_sortie):
    """
    Lit un fichier CSV, calcule la moyenne des valeurs dans chaque liste à partir de la 2ème ligne et 2ème colonne,
    et remplace la liste par la moyenne.

    Args:
        fichier_entree (str): Chemin du fichier CSV d'entrée.
        fichier_sortie (str): Chemin du fichier CSV de sortie.
    """
#prend un csv sous forme de colonnes definies
    # 1. Lire le fichier CSV
    df = pd.read_csv(fichier_entree, delimiter=';', quotechar='"')

    # 2. Calculer la moyenne et remplacer les listes à partir de la 2ème ligne et 2ème colonne
    for col_index in range(1, len(df.columns)):  # Commencer à la 2ème colonne (index 1)
        for row_index in range(0, len(df)):  # Commencer à la 2ème ligne (index 1)
            valeur = df.iloc[row_index, col_index]
            if isinstance(valeur, str) and valeur.startswith('['):
                try:
                    liste_valeurs = ast.literal_eval(valeur)
                    if isinstance(liste_valeurs, list) and len(liste_valeurs) > 0:
                        moyenne = np.mean(liste_valeurs)
                        df.iloc[row_index, col_index] = moyenne
                    else:
                        df.iloc[row_index, col_index] = np.nan  # Remplacer les listes vides par NaN
                except (ValueError, SyntaxError):
                    print(f"Erreur de conversion pour la valeur : {valeur} à la ligne {row_index}, colonne {col_index}")
                    df.iloc[row_index, col_index] = np.nan  # Remplacer par NaN en cas d'erreur de conversion
            elif pd.isna(valeur):
                continue  # Ne rien faire si la case est déjà vide
            else:
                try:
                    df.iloc[row_index,col_index] = float(valeur) # Convertir les autres valeurs en float si possible
                except ValueError:
                    print(f"Erreur de conversion pour la valeur : {valeur} à la ligne {row_index}, colonne {col_index}")
                    df.iloc[row_index, col_index] = np.nan

    # 3. Enregistrer le DataFrame résultant dans un nouveau fichier CSV
    df.to_csv(fichier_sortie, index=False)

# Exemple d'utilisation
fichier_entree = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\vversion4_filtre75_remplissage.csv"  # Remplacez par le chemin de votre fichier d'entrée
fichier_sortie = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\version4_filtre75_remplissage1.csv"  # Remplacez par le chemin où vous souhaitez enregistrer le fichier de sortie

calculer_moyenne_et_remplacer_partiel(fichier_entree, fichier_sortie)

print(f"Les moyennes ont été calculées et remplacées (à partir de la 2ème ligne et colonne) dans '{fichier_sortie}'.")