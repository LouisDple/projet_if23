import pandas as pd

def augment_data(input_file, output_file):
    """
    Lit le fichier CSV en entrée et pour chaque ligne :
      - Crée une ligne avant avec les mêmes labels et les valeurs multipliées par 1.1,
      - Garde la ligne originale,
      - Crée une ligne après avec les mêmes labels et les valeurs multipliées par 0.9.
    Le résultat est sauvegardé dans output_file.
    
    :param input_file: Chemin du fichier CSV d'entrée.
    :param output_file: Chemin du fichier CSV de sortie.
    """
    # Lecture du CSV d'entrée
    df = pd.read_csv(input_file)
    
    augmented_rows = []
    
    # Itération sur chaque ligne du dataframe
    for index, row in df.iterrows():
        # La première colonne contient le label (ne pas modifier)
        label = row.iloc[0]
        # Les autres colonnes contiennent les mesures (on suppose qu'elles sont numériques)
        measurements = row.iloc[1:]
        
        # Créer une ligne avec les mesures multipliées par 1.1
        row_before = row.copy()
        row_before.iloc[1:] = measurements * 1.1
        
        # Créer une ligne avec les mesures multipliées par 0.9
        row_after = row.copy()
        row_after.iloc[1:] = measurements * 0.9
        
        # Ajout des lignes dans l'ordre : ligne avant, ligne originale, ligne après
        augmented_rows.append(row_before)
        augmented_rows.append(row)
        augmented_rows.append(row_after)
    
    # Création d'un nouveau DataFrame avec les lignes augmentées
    df_augmented = pd.DataFrame(augmented_rows, columns=df.columns)
    
    # Sauvegarde dans un nouveau fichier CSV
    df_augmented.to_csv(output_file, index=False)
    print(f"Le fichier augmentée a été sauvegardé sous : {output_file}")

if __name__ == "__main__":
    # Spécifiez ici le chemin de votre fichier CSV d'entrée et le chemin de sortie souhaité.
    input_csv = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\version11_filtre50_pasrempli1.csv"          # Exemple: "C:\\Users\\Depelley Louis\\Desktop\\data.csv"
    output_csv = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\version12_filtre50_pasrempli1_augmente.csv"  # Exemple: "C:\\Users\\Depelley Louis\\Desktop\\data_augmente.csv"
    
    augment_data(input_csv, output_csv)
