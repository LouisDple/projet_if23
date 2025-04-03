"""
import pandas as pd
import numpy as np

def remplacer_valeurs_manquantes(fichier_entree, fichier_sortie):
    
   # Lit un fichier CSV, remplace les valeurs manquantes par la moyenne des valeurs adjacentes,
   # et enregistre le résultat.

    #Args:
    #    fichier_entree (str): Chemin du fichier CSV d'entrée.
    #    fichier_sortie (str): Chemin du fichier CSV de sortie.
    

    # 1. Lire le fichier CSV
    df = pd.read_csv(fichier_entree)

    # 2. Parcourir chaque colonne et remplacer les valeurs manquantes
    for col in df.columns[1:]:  # Commencer à la deuxième colonne
        for i in range(len(df)):
            if pd.isna(df.loc[i, col]):
                # Rechercher la valeur remplie la plus proche
                valeur_proche = None
                for j in range(1, len(df)):
                    if i - j >= 0 and pd.notna(df.loc[i - j, col]):
                        valeur_proche = df.loc[i - j, col]
                        break
                    if i + j < len(df) and pd.notna(df.loc[i + j, col]):
                        valeur_proche = df.loc[i + j, col]
                        break
                if valeur_proche is not None:
                    df.loc[i, col] = valeur_proche

    # 3. Enregistrer le DataFrame résultant dans un nouveau fichier CSV
    df.to_csv(fichier_sortie, index=False)

# Exemple d'utilisation
fichier_entree = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframemoyenne2.csv"  # Remplacez par le chemin de votre fichier d'entrée
fichier_sortie = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframemoyennerempli2.csv"

remplacer_valeurs_manquantes(fichier_entree, fichier_sortie)

print(f"Les valeurs manquantes ont été remplacées dans '{fichier_sortie}'.")
"""
#prend un csv avec des virgules
import pandas as pd
import numpy as np

def fill_missing_in_series(series, threshold=0.6):
    """
    Remplit les valeurs manquantes d'une série numérique.
    Si le taux de valeurs manquantes est supérieur à 'threshold',
    toutes les valeurs manquantes seront remplacées par -95.
    Sinon, les valeurs manquantes sont remplacées par l'interpolation linéaire
    (c'est-à-dire la moyenne de la valeur précédente et de la valeur suivante non manquante).
    """
    missing_ratio = series.isna().mean()
    if missing_ratio > threshold:
        # Remplacer toutes les valeurs manquantes par -95
        return series.fillna(-95)
    else:
        # Interpolation linéaire pour combler les trous (en avant et en arrière)
        interpolated = series.interpolate(method='linear', limit_direction='both')
        # En cas de valeurs encore manquantes, les remplacer par -95
        return interpolated.fillna(-95)

def process_csv(input_file, output_file, threshold=0.6):
    """
    Lit le fichier CSV d'entrée, traite chaque colonne de MAC en remplaçant les valeurs manquantes,
    et enregistre le DataFrame nettoyé dans un nouveau fichier CSV.
    
    :param input_file: Chemin du fichier CSV d'entrée.
    :param output_file: Chemin du fichier CSV de sortie.
    :param threshold: Seuil de 60% pour décider du mode de remplissage.
    """
    # Lecture du fichier CSV
    df = pd.read_csv(input_file)
    
    # On suppose que la première colonne contient les labels de salle (on la laisse inchangée)
    for col in df.columns[1:]:
        # Convertir la colonne en numérique (les valeurs non convertibles deviennent NaN)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Appliquer le remplissage en fonction du taux de valeurs manquantes
        df[col] = fill_missing_in_series(df[col], threshold)
    
    # Enregistrer le DataFrame traité
    df.to_csv(output_file, index=False)
    print(f"Fichier traité enregistré sous : {output_file}")

if __name__ == "__main__":
    # Modifier ces chemins pour pointer vers votre fichier CSV d'entrée et définir le fichier de sortieversion2_filtre25_remplissage1
    input_file = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\version1_sans_modification.csv"       # Exemple : "C:\\Users\\Depelley Louis\\Desktop\\if23\\input.csv"
    output_file = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\version0_sansmodif_remplissage4.csv" # Exemple : "C:\\Users\\Depelley Louis\\Desktop\\if23\\output.csv"
    
    process_csv(input_file, output_file)
