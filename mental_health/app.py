from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from flask_cors import CORS
from datetime import datetime
import os
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# === Model ve yardımcı dosyalar ===
model = load_model("deployment/mental_ann_model.keras")

# Encoder dosyalarını yükleme
try:
    encoders = joblib.load("deployment/mental_encoders.pkl")
    original_values = joblib.load("deployment/mental_encoder_cat.pkl")
    country_map = joblib.load("deployment/country_map.pkl")
    print("✅ Encoder yapısı, metinsel değerler ve country map başarıyla yüklendi.")
except FileNotFoundError:
    raise RuntimeError("❌ Gerekli dosyalar bulunamadı. Lütfen dosya yollarını kontrol edin.")
except Exception as e:
    raise RuntimeError(f"❌ Encoder veya metinsel değer yükleme hatası: {str(e)}")

# ✅ Optimal Threshold Yükleme
threshold_path = "deployment/optimal_threshold.txt"
try:
    with open(threshold_path, "r") as f:
        optimal_threshold = float(f.read().strip())
        print(f"✅ Optimal threshold yüklendi: {optimal_threshold}")
except Exception as e:
    optimal_threshold = 0.5
    print(f"❌ Threshold yüklenemedi, varsayılan kullanılıyor: {optimal_threshold}")

# === Özellik isimleri ===
feature_names = [
    "Age", "Gender", "Country", "family_history", "treatment", "work_interfere",
    "no_employees", "remote_work", "tech_company", "benefits", "care_options",
    "wellness_program", "seek_help", "anonymity", "leave",
    "mental_health_consequence", "phys_health_consequence", "coworkers",
    "supervisor", "mental_health_interview", "phys_health_interview",
    "mental_vs_physical", "obs_consequence"
]

# 🔄 Encode işlemi
def encode_features(df):
    for col in df.columns:
        if col in encoders:
            try:
                le = encoders[col]
                # Bilinmeyen değer kontrolü
                if df[col].iloc[0] not in le.classes_:
                    # "Unknown" değerine varsayılan bir indeks verelim
                    if "Unknown" not in le.classes_:
                        le.classes_ = np.append(le.classes_, "Unknown")
                    df[col] = le.transform(df[col].apply(lambda x: x if x in le.classes_ else "Unknown"))
                    print(f"⚠️ Bilinmeyen değer algılandı: {df[col].iloc[0]} → {col}. 'Unknown' olarak işaretlendi.")
                else:
                    df[col] = le.transform(df[col])
                print(f"✅ Encode işlemi: {col} sütunu başarılı.")
            except Exception as e:
                error_msg = f"🚫 Encode hatası: {col} - {str(e)}"
                print(f"⚠️ {error_msg}")
                return None, error_msg
    return df, None

# Ön işleme fonksiyonu
def preprocess_input(data):
    try:
        # Ülke ismini country_map ile dönüştürme
        data["Country"] = country_map.get(data.get("Country", "Unknown"), "Unknown")
        df = pd.DataFrame([{col: data.get(col, "Unknown") for col in feature_names}])
        encoded_df, error = encode_features(df)
        if error:
            return None, error
        encoded_df = encoded_df[feature_names]
        X_processed = encoded_df.values.astype(np.float32)
        return X_processed, None
    except Exception as e:
        return None, f"🚫 Ön işleme hatası: {str(e)}"

# === Tahmin API ===
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Gelen veriyi al ve yazdır
        data = request.get_json(force=True)
        print("📥 Gelen ham veri (React):", data)

        email = data.get("email", "bilinmiyor@example.com")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Veriyi işleme (sayısala dönüştürme)
        print("📝 Encode öncesi ham veri:")
        for key, value in data.items():
            print(f" - {key}: {value}")

        # Encode edilmeden önceki DataFrame oluşturma
        df = pd.DataFrame([{col: data.get(col, "Unknown") for col in feature_names}])
        print("📝 Encode işlemi öncesi DataFrame:")
        print(df)

        X_processed, error = preprocess_input(data)
        if error:
            print(f"🚫 Ön işleme hatası: {error}")
            return jsonify({"error": error})

        # Modelden tahmin al
        proba = float(model.predict(X_processed)[0][0])
        pred = int(proba > optimal_threshold)
        probability_percent = round(proba * 100, 2)

        # Encode sonrası veriyi yazdır
        print(f"📊 Tahmin Sonucu: {pred} | Olasılık: %{probability_percent} (Eşik: {optimal_threshold})")
        print("🔍 Encode edilmiş veriler:")
        print(X_processed)

        # Sonucu kaydetme
        new_row = pd.DataFrame([[timestamp, email, probability_percent, pred]],
                               columns=["Tarih", "Email", "Olasılık (%)", "Sonuç (0-1)"])
        os.makedirs("datasets", exist_ok=True)
        new_row.to_csv("datasets/output.csv", mode='a', header=not os.path.exists("datasets/output.csv"), index=False)

        # Yanıt oluşturma
        return jsonify({
            "prediction": pred,
            "probability": proba,
            "threshold": optimal_threshold,
            "message": "Tahmin işlemi başarılı."
        })

    except Exception as e:
        print(f"❌ Tahmin hatası: {str(e)}")
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("🚀 Uygulama başlatılıyor...")
    app.run(host="0.0.0.0", port=5001, debug=True)

    # Test verisi
    # test_input = {
    #     "Age": 36,
    #     "Gender": "Male",
    #     "Country": "United States",
    #     "family_history": "Yes",
    #     "work_interfere": "Often",
    #     "no_employees": "6-25",
    #     "remote_work": "Yes",
    #     "tech_company": "Yes",
    #     "benefits": "No",
    #     "care_options": "No",
    #     "wellness_program": "No",
    #     "seek_help": "No",
    #     "anonymity": "Yes",
    #     "leave": "Very easy",
    #     "mental_health_consequence": "No",
    #     "phys_health_consequence": "No",
    #     "coworkers": "Yes",
    #     "supervisor": "No",
    #     "mental_health_interview": "No",
    #     "phys_health_interview": "Yes",
    #     "mental_vs_physical": "No",
    #     "obs_consequence": "No"
    # }

    # X_processed, error = decode_features(test_input)
    # if error:
    #     print(f"HATA: {error}")
    # else:
    #     # ANN modeli predict doğrudan sigmoid çıktısı verir
    #     proba = float(model.predict(X_processed)[0])
    #     pred = int(proba > optimal_threshold)

    #     print("🚀 TEST VERİSİ İÇİN TAHMİN (Threshold ile):")
    #     print(f"Prediction: {pred} (0: Destek Gerekmiyor, 1: Destek Gerekli)")
    #     print(f"Probability: {proba:.4f}")
    #     print(f"Threshold (Eşik): {optimal_threshold}")