from scipy.stats import norm

def z_value(confidence_level):
    alpha = 1 - confidence_level  # Niveau de risque
    z = norm.ppf(1 - alpha / 2)  # Valeur critique pour une distribution normale
    return z

# Exemple : Z value pour un intervalle de confiance de 90%
print("Z value pour 90% : ", z_value(0.30))