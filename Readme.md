# AgriGenius – Smart Crop Decision System 🌱

AgriGenius is a web-based decision support system that recommends the most suitable crop and predicts future market price using Machine Learning. The system uses soil nutrients (N, P, K), soil type, season, and location-based weather data to help farmers make profitable decisions — without requiring any IoT hardware.

---

## 🚀 Features

- Crop recommendation using Random Forest  
- Future price forecasting using LSTM  
- Weather integration via API  
- User authentication  
- Seed shop information  
- FastAPI backend with auto Swagger docs

---

## 📊 Dataset

- **Dataset:** Crop Recommendation Dataset  
- **Records:** 2200  
- **Features:** N, P, K, temperature, humidity, pH, rainfall  
- **Target:** Crop label  
- Minimal preprocessing required

---

## 🧠 Machine Learning

- **Model 1:** Random Forest – crop classification  
- **Model 2:** LSTM – price prediction  
- **Metrics:** Accuracy, F1-score, RMSE  
- **Train/Test Split:** 80/20

---

## 🛠 Tech Stack

- **Frontend:** React, Bootstrap  
- **Backend:** FastAPI (Python)  
- **ML:** Scikit-learn, TensorFlow  
- **Database:** MySQL  
- **External:** Weather API

---
## ⚙️ Setup

1. Install dependencies  
```bash
pip install -r requirements.txt
```

2. Start FastAPI server  
```bash
uvicorn main:app --reload
```

3. API Docs  
```
http://localhost:8000/docs
```

4. Start frontend  
```bash
npm start
```

---

## 📌 Inputs

- Soil Type  
- Season  
- N, P, K values  
- Location (for weather)

---

## 📤 Outputs

- Recommended crops  
- Yield probability  
- Predicted price  
- Nearby seed shops

---

## 🔐 Security

- JWT authentication  
- Pydantic validation  
- Rate limiting  
- CORS protection

---