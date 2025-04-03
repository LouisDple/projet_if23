import os
import subprocess
import time
import csv
import sys
import msvcrt  # Permet de détecter une touche sous Windows

def verifier_executable(executable):
    """ Vérifie si l'exécutable spécifié existe. """
    if not os.path.isfile(executable):
        print(f"Erreur : {executable} n'a pas été trouvé. Vérifiez que WifiInfoView est installé et accessible.")
        sys.exit(1)

def scan_wifi(executable):
    """ Exécute WifiInfoView en mode commande et récupère la sortie brute. """
    try:
        result = subprocess.check_output([executable, "/scomma"], universal_newlines=True)
        return result
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'exécution de WifiInfoView:", e)
        return None

def extraire_donnees(csv_data):
    """ Extrait uniquement le nom du réseau WiFi (SSID) et son RSSI (Signal). """
    lignes = csv_data.strip().splitlines()
    if len(lignes) < 2:
        return []  # Pas de données exploitables
    reader = csv.DictReader(lignes)
    mesures = []
    for row in reader:
        mesure = {
            "SSID": row.get("SSID", "").strip(),
            "RSSI": row.get("RSSI", "").strip(),  # RSSI = puissance du signal
            "MAC Address": row.get("MAC Address", "").strip()
        }
        mesures.append(mesure)
    return mesures

def sauvegarder_mesures(room_number, position, mesures):
    """ Enregistre les mesures dans un fichier CSV. """
    dossier_principal = f"Salle_{room_number}"
    sous_dossier = os.path.join(dossier_principal, f"Position_{position}")
    os.makedirs(sous_dossier, exist_ok=True)
    print("ok")
    chemin_fichier = os.path.join(sous_dossier, "mesures.csv")
    
    ecrire_en_tete = not os.path.isfile(chemin_fichier)

    try:
        with open(chemin_fichier, mode="a", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["SSID", "RSSI", "Mac Address"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if ecrire_en_tete:
                writer.writeheader()
            
            for mesure in mesures:
                ligne = {
                    
                    "SSID": mesure.get("SSID", ""),
                    "RSSI": mesure.get("RSSI", ""),
                    "Mac Address": mesure.get("MAC Address", "")
                }
                writer.writerow(ligne)
    except Exception as e:
        print("Erreur lors de la sauvegarde des mesures :", e)

def choisir_salle():
    """ Demande et retourne un numéro de salle valide. """
    while True:
        room_number = input("Entrez le numéro de la salle : ").strip()
        if room_number:
            return room_number
        print("⚠ Le numéro de salle ne peut pas être vide.")

def choisir_position():
    """ Demande et retourne un numéro de position valide. """
    while True:
        position = input("Entrez la position dans la salle : ").strip()
        if position:
            return position
        print("⚠ La position ne peut pas être vide.")

def main():
    wifiinfo_exe = r"C:\Users\Depelley Louis\Desktop\if23\projet_if23\WifiInfoView.exe"  # Adapter le chemin
    verifier_executable(wifiinfo_exe)

    room_number = choisir_salle()
    position = choisir_position()

    print("\n📡 Démarrage des mesures des réseaux WiFi. Appuyez sur une touche pour changer de position ou de salle.")
    
    try:
        while True:
            # Début des mesures en continu pour la position actuelle
            while True:
                sortie = scan_wifi(wifiinfo_exe)
                time.sleep(0.5)  # Pause de 1 seconde
                if sortie:
                    mesures = extraire_donnees(sortie)
                    if mesures:
                        sauvegarder_mesures(room_number, position, mesures)
                        print(f"✔ Mesure enregistrée pour la salle {room_number}, position {position}.")
                    else:
                        print("⚠ Aucune donnée WiFi extraite.")
                else:
                    print("❌ Impossible d'effectuer le scan WiFi.")

                # Vérifier si une touche a été pressée
                if msvcrt.kbhit():  
                    print("\n🔄 Interruption détectée. Choisissez une action :")
                    print("1️⃣ Changer de position")
                    print("2️⃣ Changer de salle")
                    print("3️⃣ Quitter le programme")
                    
                    choix = input("👉 Entrez votre choix (1, 2, 3) : ").strip()
                    
                    if choix == "1":
                        position = choisir_position()
                    elif choix == "2":
                        room_number = choisir_salle()
                        position = choisir_position()
                    elif choix == "3":
                        print("🛑 Arrêt du programme.")
                        sys.exit(0)
                    else:
                        print("❌ Choix invalide, retour aux mesures.")
                
                # Pause de 2 secondes entre les mesures
                

    except KeyboardInterrupt:
        print("\n🛑 Interruption par Ctrl+C. Arrêt du programme.")
        sys.exit(0)
    except Exception as e:
        print("❌ Erreur inattendue :", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
