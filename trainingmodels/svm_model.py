import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def load_data(filename):
    """
    Charge les données depuis un fichier CSV.
    La première colonne doit contenir les labels (Salle)
    et les colonnes suivantes les mesures des MACs.
    """
    df = pd.read_csv(filename)
    # On suppose que la première colonne s'appelle "Salle"
    X = df.drop("Salle", axis=1)
    y = df["Salle"]
    return X, y

def partition_data(X, y, test_size=0.3, random_state=42):
    """
    Partitionne les données en ensembles d'entraînement et de test.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_and_evaluate(X_train, X_test, y_train, y_test):
    """
    Entraîne un classifieur SVM sur l'ensemble d'entraînement
    et évalue le taux de réussite sur l'ensemble de test.
    """
    clf = SVC()  # SVM avec paramètres par défaut
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return clf, acc

def main():
    # Chemin vers votre fichier CSV
    filename = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\version3_filtre50_remplissage3.csv"  # Remplacez par le chemin de votre fichier CSV
    X, y = load_data(filename)
    X_train, X_test, y_train, y_test = partition_data(X, y)
    clf, accuracy = train_and_evaluate(X_train, X_test, y_train, y_test)
    print("Taux de réussite (accuracy) sur l'ensemble de test :", accuracy)

if __name__ == "__main__":
    main()
 