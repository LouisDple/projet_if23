import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

def load_data(file_path):
    """
    Charge le fichier CSV.
    La première colonne contient les labels (ex: 'Salle'),
    les colonnes suivantes contiennent les mesures des MACs.
    """
    df = pd.read_csv(file_path)
    # Les features sont toutes les colonnes sauf la première
    X = df.iloc[:, 1:].values
    # Les labels sont dans la première colonne
    y = df.iloc[:, 0].values
    return X, y

def preprocess_labels(y):
    """
    Encode les labels textuels en entiers.
    """
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    return y_encoded, le

def main():
    # Chemin vers le fichier CSV d'entrée (modifiez ce chemin selon votre environnement)
    input_file = r"C:\Users\Depelley Louis\Desktop\if23\projet_if23\dataframes\version11_filtre50_pasrempli1.csv"  # ex: "C:\\Users\\Depelley Louis\\Desktop\\data.csv"
    
    # Chargement des données
    X, y = load_data(input_file)
    
    # Encodage des labels
    y_encoded, label_encoder = preprocess_labels(y)
    
    # Partitionnement des données (70% entraînement, 30% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)
    
    # Entraînement du modèle d'arbre de décision
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    
    # Prédictions et évaluation
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Taux de réussite (accuracy) sur l'ensemble de test :", accuracy)

if __name__ == "__main__":
    main()
