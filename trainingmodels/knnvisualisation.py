import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

def load_data(input_file):
    """
    Charge le fichier CSV.
    La première colonne contient les labels (ex : 'Salle'),
    les autres colonnes contiennent les mesures des MACs.
    """
    df = pd.read_csv(input_file)
    # On suppose que la première colonne est le label (Salle)
    X = df.iloc[:, 1:].values  # Caractéristiques (mesures des MACs)
    y = df.iloc[:, 0].values   # Labels (Salle)
    return X, y

def preprocess_labels(y):
    """
    Encode les labels textuels en valeurs numériques.
    Retourne les labels encodés ainsi que l'encodeur (pour décodage éventuel).
    """
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    return y_encoded, le

def main():
    # Modifiez le chemin ci-dessous pour pointer vers votre fichier CSV d'entrée.
    input_file = r"C:\Users\Depelley Louis\Desktop\if23\projet_if23\dataframes\version8_filtre50_remplissage_zvalue30.csv"
    
    # Chargement des données
    X, y = load_data(input_file)
    
    # Encodage des labels (Salle)
    y_encoded, label_encoder = preprocess_labels(y)
    
    # Partitionnement des données : 70% entraînement, 30% test
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)
    
    # Liste pour stocker les nombres de voisins et les précisions correspondantes
    neighbors_range = range(2, 21)  # Exemple : de 2 à 20 voisins
    accuracy_list = []

    for k in neighbors_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        accuracy_list.append(acc)
        print(f"n_neighbors = {k} => Accuracy = {acc:.4f}")
    
    # Visualisation de la courbe : Accuracy en fonction du nombre de voisins
    plt.figure(figsize=(8, 5))
    plt.plot(neighbors_range, accuracy_list, marker='o', linestyle='-', color='b')
    plt.xlabel("Nombre de voisins (n_neighbors)")
    plt.ylabel("Taux de réussite (accuracy)")
    plt.title("Courbe de précision du modèle KNN")
    plt.grid(True)
    
    # Sauvegarde de la courbe
    output_plot = r"C:\Users\Depelley Louis\Desktop\if23\projet_if23\trainingmodels\knn\accuracy_curves\knn_accuracy_curved8.png"
    plt.savefig(output_plot)
    print(f"Courbe sauvegardée sous : {output_plot}")
    plt.show()

if __name__ == "__main__":
    main()
