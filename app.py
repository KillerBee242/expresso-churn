import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# -------------------------------------------------
# 🔹 Modèle déjà entraîné en mémoire
# Remplacez 'rf' par le modèle que vous avez entraîné
# -------------------------------------------------
# rf = ... (RandomForest ou XGBoost)
# Pour cet exemple, on suppose que 'rf' est déjà défini

st.title("Prédiction de churn - Expresso")

st.markdown("""
Bienvenue dans l'application de prédiction de churn pour Expresso.
Remplissez les informations du client et cliquez sur **Prédire**.
""")

# -------------------------------------------------
# 🔹 Formulaire des caractéristiques
# -------------------------------------------------
REGION = st.selectbox("Région", ["DAKAR", "SAINT-LOUIS", "AUTRE"])
TENURE = st.number_input("Durée d'abonnement (mois)", min_value=0, max_value=120)
MRG = st.selectbox("Type de client", ["pilot_offer1", "pilot_offer2", "pilot_offer3", "pilot_offer4"])
TOP_PACK = st.selectbox("Pack principal", ["PackA", "PackB", "PackC", "PackD"])
DATA_VOLUME = st.number_input("Volume de data consommé (Go)", min_value=0.0)
REGULARITY = st.number_input("Régularité d'utilisation", min_value=0.0)
FREQUENCE = st.number_input("Fréquence d'utilisation", min_value=0.0)
FREQUENCE_RECH = st.number_input("Fréquence de recharge", min_value=0.0)
MONTANT = st.number_input("Montant dépensé", min_value=0.0)
REVENUE = st.number_input("Revenu généré", min_value=0.0)
ON_NET = st.number_input("Appels on-net", min_value=0.0)
ORANGE = st.number_input("Appels vers Orange", min_value=0.0)

# -------------------------------------------------
# 🔹 Encodage des variables catégorielles
# -------------------------------------------------
def encode_input(df, encoders):
    for col, le in encoders.items():
        df[col] = le.transform(df[col])
    return df

# ⚠️ Créez vos LabelEncoders comme ceux utilisés pour l'entraînement
encoders = {}
for col, classes in {
    'REGION': ["DAKAR", "SAINT-LOUIS", "AUTRE"],
    'MRG': ["pilot_offer1", "pilot_offer2", "pilot_offer3", "pilot_offer4"],
    'TOP_PACK': ["PackA", "PackB", "PackC", "PackD"]
}.items():
    le = LabelEncoder()
    le.fit(classes)
    encoders[col] = le

# -------------------------------------------------
# 🔹 Bouton de prédiction
# -------------------------------------------------
if st.button("Prédire"):
    new_data = pd.DataFrame({
        'REGION':[REGION],
        'TENURE':[TENURE],
        'MRG':[MRG],
        'TOP_PACK':[TOP_PACK],
        'DATA_VOLUME':[DATA_VOLUME],
        'REGULARITY':[REGULARITY],
        'FREQUENCE':[FREQUENCE],
        'FREQUENCE_RECH':[FREQUENCE_RECH],
        'MONTANT':[MONTANT],
        'REVENUE':[REVENUE],
        'ON_NET':[ON_NET],
        'ORANGE':[ORANGE]
    })

    # Encodage
    new_data = encode_input(new_data, encoders)

    # Prédiction
    prediction = rf.predict(new_data)[0]
    proba = rf.predict_proba(new_data)[0,1]

    st.success(f"Probabilité de churn : {proba:.2f}")
    st.info("Le client va probablement churn !" if prediction==1 else "Le client va probablement rester.")
