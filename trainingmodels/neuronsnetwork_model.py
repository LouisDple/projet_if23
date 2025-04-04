import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

def load_data(file_path):
    """
    Charge le fichier CSV. On suppose que la première colonne est "Salle" 
    et que les autres colonnes contiennent les mesures pour chaque MAC.
    """
    df = pd.read_csv(file_path)
    # Les features sont toutes les colonnes sauf "Salle"
    X = df.drop("Salle", axis=1).values
    # Les labels sont dans la colonne "Salle"
    y = df["Salle"].values
    return X, y

def preprocess_data(X, y):
    """
    Encode les labels (salles) en entiers puis en one-hot encoding.
    Retourne les données préparées, le nombre de classes et l'encodeur des labels.
    """
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    num_classes = len(np.unique(y_encoded))
    y_categorical = to_categorical(y_encoded, num_classes=num_classes)
    return X, y_categorical, num_classes, le

def build_model(input_dim, num_classes):
    """
    Construit et compile un modèle de réseau de neurones simple pour la classification multiclasse.
    """
    model = Sequential()
    model.add(Dense(64, input_dim=input_dim, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def main():
    # Modifiez ce chemin pour pointer vers votre fichier CSV d'entrée
    input_file = "C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\dataframes\\version11_filtre50_pasrempli1.csv"  # ex : "C:\\Users\\Depelley Louis\\Desktop\\if23\\data.csv"
    
    # Chargement des données
    X, y = load_data(input_file)
    
    # Prétraitement (encodage des labels)
    X, y, num_classes, label_encoder = preprocess_data(X, y)
    
    # Partitionnement des données (80% entraînement, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Construction et entraînement du modèle
    model = build_model(input_dim=X.shape[1], num_classes=num_classes)
    model.summary()
    model.fit(X_train, y_train, epochs=50, batch_size=8, validation_split=0.1)
    
    # Évaluation du modèle sur l'ensemble de test
    loss, accuracy = model.evaluate(X_test, y_test)
    print("Taux de réussite (accuracy) sur l'ensemble de test :", accuracy)
    
    # Optionnel : Sauvegarder le modèle entraîné
    #model.save("C:\\Users\\Depelley Louis\\Desktop\\if23\\projet_if23\\trainingmodels\\modele_salle.keras")
    print("Modèle sauvegardé sous 'modele_salle.h5'")

if __name__ == "__main__":
    main()
