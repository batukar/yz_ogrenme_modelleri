from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

model = joblib.load("deployment/mental_logreg_model.pkl")
encoders = joblib.load("deployment/mental_encoders.pkl")
scaler = joblib.load("deployment/mental_scaler.pkl")

feature_names = list(model.feature_names_in_)
optimal_threshold = 0.63
output_file = "datasets/output.csv"

default_values = {
    "Country": "United States",
    "remote_work": "No",
    "seek_help": "No",
    "leave": "Very easy",
    "mental_health_consequence": "No",
    "phys_health_consequence": "No",
    "mental_health_interview": "No",
    "phys_health_interview": "No",
    "mental_vs_physical": "Dont know",
    "obs_consequence": "No"
}

def preprocess_input(data):
    completed_data = {col: data.get(col, default_values.get(col, "No")) for col in feature_names}
    df = pd.DataFrame([completed_data])

    for col in df.columns:
        if col != "Age" and col in encoders:
            le = encoders[col]
            try:
                df[col] = le.transform([df[col].values[0]])
            except Exception as e:
                return None, f"Encoder hatası: '{col}' sütununda '{df[col].values[0]}' değeri tanımlı değil!"
    df = df[feature_names]
    df_scaled = scaler.transform(df)
    return df_scaled, None

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        print("📥 Gelen veri:", data)

        email = data.get("email")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        X_processed, error = preprocess_input(data)
        if error:
            return jsonify({"error": error})

        proba = model.predict_proba(X_processed)[0][1]
        pred = int(proba > optimal_threshold)
        probability_percent = round(proba * 100, 2)

        print(f"📊 Olasılık: {probability_percent}% | Tahmin (Threshold {optimal_threshold}): {pred}")

        # CSV'ye yazma:
        new_row = pd.DataFrame([[timestamp, email, probability_percent, pred]],
                               columns=["Tarih", "Email", "Olasılık (%)", "Sonuç (0-1)"])

        if not os.path.exists(output_file):
            new_row.to_csv(output_file, index=False)
        else:
            new_row.to_csv(output_file, mode='a', header=False, index=False)

        return jsonify({
            "prediction": pred,
            "probability": proba,
            "threshold": optimal_threshold
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

    # 🧪 Test verisi --> 1 (Destek almalı örneği)
    # test_input = {
    #     "Age": 29,
    #     "Gender": "Male",
    #     "Country": "United States",
    #     "family_history": "Yes",
    #     "work_interfere": "Sometimes",
    #     "no_employees": "26-100",
    #     "remote_work": "No",
    #     "tech_company": "Yes",
    #     "benefits": "Yes",
    #     "care_options": "Yes",
    #     "wellness_program": "No",
    #     "seek_help": "Yes",
    #     "anonymity": "Yes",
    #     "leave": "Somewhat difficult",
    #     "mental_health_consequence": "Yes",
    #     "phys_health_consequence": "Yes",
    #     "coworkers": "Some of them",
    #     "supervisor": "Yes",
    #     "mental_health_interview": "Yes",
    #     "phys_health_interview": "Yes",
    #     "mental_vs_physical": "Yes",
    #     "obs_consequence": "Yes"
    # }

    # 🧪 Test verisi --> 0 (Destek almasına gerek yok örneği)
    # test_input = {
    #     "Age": 35,
    #     "Gender": "Male",
    #     "Country": "United States",
    #     "family_history": "No",
    #     "work_interfere": "Never",
    #     "no_employees": "6-25",
    #     "remote_work": "Yes",
    #     "tech_company": "No",
    #     "benefits": "Yes",
    #     "care_options": "Yes",
    #     "wellness_program": "Yes",
    #     "seek_help": "Yes",
    #     "anonymity": "Yes",
    #     "leave": "Very easy",
    #     "mental_health_consequence": "No",
    #     "phys_health_consequence": "No",
    #     "coworkers": "Yes",
    #     "supervisor": "Yes",
    #     "mental_health_interview": "No",
    #     "phys_health_interview": "No",
    #     "mental_vs_physical": "No",
    #     "obs_consequence": "No"
    # }

    # X_processed, error = preprocess_input(test_input)
    # if error:
    #     print(f"HATA: {error}")
    # else:
    #     proba = model.predict_proba(X_processed)[0][1]
    #     pred = int(proba > optimal_threshold)

    #     print("🚀 TEST VERİSİ İÇİN TAHMİN (Threshold ile):")
    #     print(f"Prediction: {pred} (0: Destek Gerekmiyor, 1: Destek Gerekli)")
    #     print(f"Probability: {proba:.4f}")
    #     print(f"Threshold (Eşik): {optimal_threshold}")