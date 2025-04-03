import pandas as pd
import re  # Pour utiliser des expressions régulières

def supprimer_colonnes_mac(fichier_entree, fichier_sortie):
    """
    Lit un fichier CSV, supprime les colonnes contenant des adresses MAC avec une présence < 75%, et enregistre le résultat.

    Args:
        fichier_entree (str): Chemin du fichier CSV d'entrée.
        fichier_sortie (str): Chemin du fichier CSV de sortie.
    """
#prend un csv avec des virgules
    # 1. Lire le fichier CSV
    df = pd.read_csv(fichier_entree, delimiter=';', quotechar='"')

    # 2. Identifier les colonnes contenant des adresses MAC
    # Une adresse MAC typique suit le format XX:XX:XX:XX:XX:XX
    pattern_mac = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    colonnes_mac = [col for col in df.columns if pattern_mac.match(col)]

    # 3. Calculer le pourcentage de présence de chaque colonne MAC
    pourcentages_presence = {}
    for col in colonnes_mac:
        presence = df[col].count()  # Compte les valeurs non nulles
        pourcentages_presence[col] = (presence / len(df)) * 100

    # 4. Identifier et conserver les colonnes avec une présence >= 75%
    colonnes_a_garder = [col for col in df.columns if col not in colonnes_mac or pourcentages_presence.get(col, 0) >= 75]
    df_filtre = df[colonnes_a_garder]

    # 5. Enregistrer le DataFrame résultant dans un nouveau fichier CSV
    df_filtre.to_csv(fichier_sortie, index=False)

# Exemple d'utilisation
fichier_entree = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\dataframe_final.csv"  # Remplacez par le chemin de votre fichier d'entrée
fichier_sortie = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\vversion4_filtre75_remplissage.csv"  # Remplacez par le chemin où vous souhaitez enregistrer le fichier de sortie

supprimer_colonnes_mac(fichier_entree, fichier_sortie)

print(f"Les colonnes avec une présence >= 75% ont été conservées dans '{fichier_sortie}'.")