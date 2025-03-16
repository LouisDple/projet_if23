import os
import pandas as pd

def charger_et_aggreguer_donnees(root_dir):
    """
    Parcourt la structure de dossiers sous root_dir.
    Chaque dossier représente une salle et contient plusieurs fichiers CSV répartis dans des sous-dossiers (positions).
    On agrège les mesures en regroupant par "Mac Address" et en collectant toutes les valeurs "RSSI" dans une liste.
    
    Retourne une liste de dictionnaires, un par fichier CSV (acquisition), avec le label "Salle".
    """
    acquisitions = []
    
    # Parcourir chaque dossier de salle
    for salle in os.listdir(root_dir):
        chemin_salle = os.path.join(root_dir, salle)
        if os.path.isdir(chemin_salle):
            salle_label = salle  # Utiliser le nom du dossier comme label de salle
            
            # Parcourir récursivement tous les fichiers CSV à l'intérieur des sous-dossiers
            for root, _, files in os.walk(chemin_salle):
                for fichier in files:
                    if fichier.lower().endswith('.csv'):
                        chemin_fichier = os.path.join(root, fichier)
                        try:
                            df = pd.read_csv(chemin_fichier, encoding="utf-8")
                            # Vérifier la présence des colonnes requises
                            if "Mac Address" in df.columns and "RSSI" in df.columns:
                                # Agréger les valeurs RSSI par "Mac Address"
                                aggregation = df.groupby("Mac Address")["RSSI"].apply(list).to_dict()
                                aggregation["Salle"] = salle_label  # Ajouter le label de salle
                                acquisitions.append(aggregation)
                            else:
                                print(f"⚠ Le fichier {chemin_fichier} ne contient pas les colonnes requises.")
                        except Exception as e:
                            print(f"Erreur lors de la lecture de {chemin_fichier} : {e}")
    return acquisitions

def creer_dataframe(acquisitions):
    """
    Construit un DataFrame à partir de la liste de dictionnaires.
    Chaque ligne correspond à un fichier CSV (acquisition) et possède :
      - Le label "Salle"
      - Pour chaque adresse MAC, une cellule contenant la liste des RSSI mesurés
    """
    df_final = pd.DataFrame(acquisitions)
    
    # Mettre "Salle" en première colonne si elle existe
    if "Salle" in df_final.columns:
        cols = ["Salle"] + [col for col in df_final.columns if col != "Salle"]
        df_final = df_final[cols]
    
    return df_final

def main():
    # Définissez ici le chemin vers vos données
    root_dir = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23"
    
    print("Chargement et agrégation des données...")
    acquisitions = charger_et_aggreguer_donnees(root_dir)
    
    if not acquisitions:
        print("Aucune donnée valide n'a été trouvée. Vérifiez la structure des dossiers et les fichiers CSV.")
        return
    
    print("Création du DataFrame final...")
    df_final = creer_dataframe(acquisitions)
    
    # Exporter le DataFrame final en CSV
    output_file = os.path.join(root_dir, "dataframe_final.csv")
    df_final.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Export terminé : {output_file}")

if __name__ == "__main__":
    main()
