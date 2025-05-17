# YZ Öğrenme Modelleri

Bu proje, makine öğrenmesi ve yapay zeka modellerini uygulamaya yönelik olarak geliştirilmiştir. GitHub deposu, zihinsel sağlık tahmini üzerine yapay zeka modellerinin uygulanması ve değerlendirilmesini içermektedir. Projede kullanılan veri seti ve modeller, literatürdeki mevcut çalışmalarla karşılaştırılarak daha iyi bir başarı elde etmek amacıyla optimize edilmiştir.

## Proje Yapısı

Bu depoda aşağıdaki dosya ve klasör yapısı bulunmaktadır:

```
YZ_Öğrenme_Modelleri/
├── mental_health/
│   ├── data/
│   ├── notebooks/
│   ├── models/
│   ├── scripts/
├── deployment/
├── README.md
```

### Klasörlerin İçeriği
- **mental_health/**: Zihinsel sağlık tahmini projesine ait dosyalar.
  - **data/**: Eğitim ve test veri setleri.
  - **notebooks/**: Model eğitimi ve değerlendirme süreçlerinin yer aldığı Jupyter notebook dosyaları.
  - **models/**: Eğitilmiş modellerin saklandığı klasör.
  - **scripts/**: Veri işleme ve model eğitimi için kullanılan Python betikleri.
- **deployment/**: Flask tabanlı API uygulaması için kodlar.

## Kullanılan Veri Seti

Bu projede "Mental Health in Tech Survey" veri seti kullanılmıştır. Veri seti, teknoloji çalışanlarının zihinsel sağlık durumlarına yönelik bilgileri içermektedir. Veriyi işlemek için çeşitli ön işleme teknikleri uygulanmıştır.

## Uygulanan Modeller
Proje kapsamında aşağıdaki modeller uygulanmıştır:

- **Logistic Regression:** Temel sınıflandırma modeli olarak kullanıldı.
- **ANN (Artificial Neural Network):** Yapay sinir ağı yapısı kullanılarak daha karmaşık ilişkiler öğrenildi.
- **SVM (Support Vector Machine):** Ayrık veri sınıflandırma işlemi için kullanıldı.
- **Decision Trees ve Naive Bayes:** Temel karar verme ve olasılıksal sınıflandırma modelleri olarak denendi.
- **KNN (K-Nearest Neighbors):** Veriye en yakın komşulara göre sınıflandırma yapıldı.

## Nasıl Çalıştırılır?

### Eğitim

1. Gerekli kütüphaneleri yükleyin:
```
pip install -r requirements.txt
```

2. Jupyter Notebook'u çalıştırın ve notebookları sırayla çalıştırarak modeli eğitin:
```
jupyter notebook
```

### Deploy

Flask tabanlı API'yi çalıştırmak için:
```
python deployment/app.py
```

API, varsayılan olarak `localhost:5000` adresinde çalışır.

## Sonuçlar

Her model için başarı oranları, doğruluk, F1 skoru, ROC eğrisi gibi metriklerle değerlendirilmiş ve karşılaştırılmıştır. Sonuçlar, modellenen veri setine göre optimize edilerek elde edilmiştir.

## İletişim
Projeyle ilgili sorularınız için GitHub üzerinden iletişime geçebilirsiniz.
