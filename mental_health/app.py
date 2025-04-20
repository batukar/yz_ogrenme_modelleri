from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Flask uygulamasını başlat
app = Flask(__name__)

# Modeli yükle (bulunduğun dizinde olduğuna dikkat et!)
model = joblib.load("mental_health/deployment/mental_logreg_model.pkl")

# Özellik isimleri (X_train.columns ile birebir aynı olmalı!)
feature_names = [
    'Age', 'Gender', 'family_history', 'benefits',
    'care_options', 'anonymity', 'leave', 'work_interfere',
    'no_employees', 'remote_work', 'tech_company', 'wellness_program'
]

# Tahmin route'u
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        df = pd.DataFrame([data], columns=feature_names)
        pred = model.predict(df)[0]
        proba = model.predict_proba(df)[0][1]
        return jsonify({
            "prediction": int(pred),
            "probability": round(proba, 4)
        })
    except Exception as e:
        return jsonify({"error": str(e)})

# Uygulamayı çalıştır
if __name__ == "__main__":
    app.run(debug=True, port=5001)