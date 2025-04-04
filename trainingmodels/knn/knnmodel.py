import pandas as pd
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
    input_file = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\version2_filtre25_remplissage3.csv"       # Exemple : "C:\\Users\\Depelley Louis\\Desktop\\if23\\data.csv"
    #output_model = "modele_knn.pkl"  # Optionnel : chemin pour sauvegarder le modèle
    
    # Chargement des données
    X, y = load_data(input_file)
    
    # Encodage des labels (Salle)
    y_encoded, label_encoder = preprocess_labels(y)
    
    # Partitionnement des données : 80% entraînement, 20% test
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)
    
    # Instanciation et entraînement du modèle KNN (vous pouvez ajuster n_neighbors selon vos besoins)
    knn = KNeighborsClassifier(n_neighbors=12 )
    knn.fit(X_train, y_train)
    
    # Prédictions sur l'ensemble de test
    y_pred = knn.predict(X_test)
    
    # Calcul du taux de réussite
    accuracy = accuracy_score(y_test, y_pred)
    print("Taux de réussite (accuracy) sur l'ensemble de test :", accuracy)
    
    # Optionnel : sauvegarde du modèle entraîné
    # from joblib import dump
    # dump(knn, output_model)
    # print(f"Modèle sauvegardé sous : {output_model}")

if __name__ == "__main__":
    main()
