"""
import pandas as pd
import numpy as np
from scipy import stats

def remplacer_valeurs_hors_intervalle(fichier_entree, fichier_sortie):
   
    salles= ["Salle_c203","Salle_c205","Salle_c206","Salle_c207","Salle_c208","Salle_c210]"]

    # 1. Lire le fichier CSV
    df = pd.read_csv(fichier_entree, delimiter=';', quotechar='"')

    # 2. Parcourir chaque colonne et calculer l'intervalle de confiance
    for col in df.columns[1:]:  # Commencer à la deuxième colonne
        for salle in salles:  # Parcourir chaque salle unique
            valeurs_salle = df[df['Salle'] == salle][col].dropna()  # Récupérer les valeurs pour la salle
            if len(valeurs_salle) > 1:  # Calculer l'intervalle si plus d'une valeur
                moyenne = np.mean(valeurs_salle)
                ecart_type = np.std(valeurs_salle, ddof=1)  # ddof=1 pour l'écart-type d'échantillon
                intervalle = stats.t.interval(0.9, len(valeurs_salle) - 1, loc=moyenne, scale=ecart_type / np.sqrt(len(valeurs_salle)))
                borne_inf, borne_sup = intervalle

                # 3. Remplacer les valeurs hors intervalle
                for i in df[df[salle] == salle].index:
                    print("oui")
                    if pd.notna(df.loc[i, col]):
                        print("valeur aberrante ")
                        if df.loc[i, col] < borne_inf:
                            df.loc[i, col] = borne_inf 
                        elif df.loc[i, col] > borne_sup:
                            df.loc[i, col] = borne_sup 
                

    # 4. Enregistrer le DataFrame résultant dans un nouveau fichier CSV
    df.to_csv(fichier_sortie, index=False)

# Exemple d'utilisation
fichier_entree = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframemoyennerempli2.csv"  # Remplacez par le chemin de votre fichier d'entrée
fichier_sortie = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframe_pas_aberrant4.csv"
remplacer_valeurs_hors_intervalle(fichier_entree, fichier_sortie)

print(f"Les valeurs hors intervalle ont été remplacées dans '{fichier_sortie}'.")"
"""

import pandas as pd
import numpy as np

def clip_group(s, z=0.385):
    """
    Pour une série de mesures s (pour une colonne MAC et pour un groupe (salle)),
    calcule la moyenne, l'écart type et l'erreur standard (std/sqrt(n)).
    Détermine la borne inférieure et la borne supérieure de l'intervalle de confiance à 90 %.
    Puis, remplace les valeurs en dehors de cet intervalle par la borne correspondante.
    
    Si la série est vide ou ne contient qu'une seule valeur, elle est renvoyée inchangée.
    """
    n = s.count()  # nombre de valeurs non manquantes
    if n < 2:
        # Pas assez de données pour calculer une dispersion
        return s
    mean = s.mean()
    std = s.std()
    se = std / np.sqrt(n)
    lower = mean - z * se
    upper = mean + z * se
    # Remplacer les valeurs en dehors de l'intervalle par la borne correspondante
    return s.clip(lower=lower , upper=upper )

def process_csv(input_file, output_file):
    """
    Lit le fichier CSV d'entrée, traite chaque colonne (MAC) par groupe (Salle)
    en remplaçant les valeurs en dehors de l'intervalle de confiance (90 %) par
    la borne correspondante, puis enregistre le DataFrame résultant dans un fichier CSV.
    
    :param input_file: Chemin du fichier CSV d'entrée.
    :param output_file: Chemin du fichier CSV de sortie.
    """
    # Lire le fichier CSV. On suppose que la première colonne contient les labels de salle.
    df = pd.read_csv(input_file)
    
    # Identifier les colonnes MAC (toutes sauf la première)
    mac_columns = df.columns[1:]
    
    # Pour chaque colonne MAC, appliquer la transformation par groupe "Salle"
    for col in mac_columns:
        # Convertir la colonne en numérique (les cellules vides deviendront NaN)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Appliquer par groupe la fonction de clipping
        df[col] = df.groupby('Salle')[col].transform(lambda s: clip_group(s))
    
    # Enregistrer le DataFrame modifié dans un nouveau fichier CSV
    df.to_csv(output_file, index=False)
    print(f"Fichier traité enregistré sous : {output_file}")

if __name__ == '__main__':

    # MODIFIEZ ces chemins en fonction de l'emplacement de votre fichier CSV
    input_csv_path = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\version3_filtre50_remplissage3.csv"      # Par exemple : "C:\\Users\\Depelley Louis\\Desktop\\if23\\input.csv"
    output_csv_path = fichier_sortie = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\version5_filtre30_remplissage_zvalue50.csv"  # Par exemple : "C:\\Users\\Depelley Louis\\Desktop\\if23\\output.csv"
    
    process_csv(input_csv_path, output_csv_path)
