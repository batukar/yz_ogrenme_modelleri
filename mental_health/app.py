from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("mental_logreg_model.pkl")

feature_names = [...]  # senin modelin için doğru feature isimlerini buraya yaz

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    df = pd.DataFrame([data], columns=feature_names)
    pred = model.predict(df)[0]
    proba = model.predict_proba(df)[0][1]
    return jsonify({
        "prediction": int(pred),
        "probability": round(proba, 4)
    })

if __name__ == "__main__":
    app.run(debug=True)