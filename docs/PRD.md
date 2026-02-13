# 🚀 PRODUCT REQUIREMENT DOCUMENT

## Project Name: **AgriGenius – Smart Crop Decision System**

---

## 1. Overview

**AgriGenius** is a web-based decision support system that recommends the most suitable crop and predicts future market price based on:

* Soil nutrients (N, P, K)
* Soil type
* Season
* Location-based weather data

The system uses:

* Random Forest → crop recommendation
* LSTM → price forecasting
* Weather API → environmental context

### Goal

> Help farmers choose the most profitable crop without requiring any IoT hardware.

---

## 2. Problem Statement

### Current Problems

* Farmers rely on intuition
* No data-driven crop selection
* Market price uncertainty
* Weather unpredictability
* No unified platform

### Our Solution

A software system that:

* Accepts basic soil inputs
* Fetches weather automatically
* Recommends best crop
* Shows expected yield & price

---

## 3. Target Users

* Farmers
* Agri students
* Extension officers
* Small agri startups

---

## 4. System Scope

### In Scope

✅ Crop recommendation
✅ Price prediction
✅ Weather integration
✅ User authentication
✅ Seed shop display
✅ Dataset training module

### Out of Scope

❌ IoT sensors
❌ Drone imagery
❌ Real-time soil probes

---

## 5. Functional Requirements

### 5.1 User Management

* Register
* Login
* Profile
* History

---

### 5.2 Input Module

User provides:

* Soil Type
* Season
* N value
* P value
* K value
* Location

System fetches:

* Temperature
* Humidity
* Rainfall

---

### 5.3 ML Module

1. Random Forest

* Input: NPK + soil + season + weather
* Output: recommended crops

2. LSTM

* Input: historical prices
* Output: future price

3. Model Evaluation & Robustness Module

```
The system must support evaluation of prediction reliability.

Capabilities:
• Run prediction under noisy inputs
• Run prediction with missing features
• Compare multiple algorithms
• Produce confidence score

The module does not only predict crops, but evaluates stability of predictions.
```

---

### Add Sub-features

#### 5.3.3.1 Noise Injection Engine

```
For each input sample, generate perturbed inputs:

N: ±10–40%
P: ±10–40%
K: ±10–40%
Random combined perturbations

Run prediction repeatedly and track if recommended crop changes.

Compute Recommendation Stability Score (RSS):
RSS = % of predictions unchanged across perturbations
```

---

#### 5.3.3.2 Multi-Model Evaluation

```
The system must support multiple algorithms:

• Random Forest
• XGBoost
• SVM
• Neural Network (MLP)

Each model produces prediction independently.
System compares models based on stability instead of only accuracy.
```

---

#### 5.3.3.3 Confidence Estimation

```
Each prediction returns a confidence score (0–1).

Confidence derived from:
• class probability
• agreement across models
• stability under perturbations
```

---

#### 5.3.3.4 Missing Data Simulation

```
System evaluates robustness when some features are unavailable:

Scenarios:
• No rainfall
• No humidity
• Wrong soil type
• Partial NPK

Measure performance degradation.
```

---

### 5.4 Output Module

Display:

* Top crops
* Yield %
* Predicted price
* Seed shops

---

## 6. Non-Functional Requirements

* Response < 3 sec
* Mobile friendly
* Secure login
* Scalable
* Python backend

---

## 7. Tech Stack

### Frontend

* React 
* Tailwind CSS

### Backend

* FastAPI

### ML

* Scikit-learn
* TensorFlow

### Database

* MySQL 

### External

* Weather API

---

## 8. System Flow


1. User enters input
2. System fetches weather
3. Base prediction generated
4. Robustness engine triggered:
   a. Noise injection tests
   b. Missing data tests
   c. Multi-model comparison
5. Confidence computed
6. Final recommendation generated
7. Stability report shown

---

## 9. Data Inputs

| Field     | Source |
| --------- | ------ |
| NPK       | user   |
| Soil type | user   |
| Season    | user   |
| Temp      | API    |
| Humidity  | API    |
| Rainfall  | API    |

---

## 10. UI Screens

1. Login
2. Register
3. Dashboard
4. Crop Form
5. Result
6. Seed Shops

---

## 11. Success Metrics

* Accurate crop suggestion
* Price RMSE low
* Fast response
* Usability

---

## 12. Risks

* Dataset quality
* API limits
* Price volatility

---


# 📌 1. API ENDPOINTS DOCUMENT

## Base URL

```
http://localhost:5000/api
```

---

## 1.1 Authentication APIs

### POST /auth/register

**Purpose:** Create new user

**Request**

```json
{
  "name": "",
  "email": "",
  "password": ""
}
```

**Response**

```json
{
  "message": "User created",
  "userId": 101
}
```

---

### POST /auth/login

**Request**

```json
{
  "email": "",
  "password": ""
}
```

**Response**

```json
{
  "token": "",
  "user": {}
}
```

---

## 1.2 Weather API Wrapper

### GET /weather?location=city

**Response**

```json
{
  "temperature": 32,
  "humidity": 70,
  "rainfall": 120
}
```

👉 This internally calls OpenWeather.

---

## 1.3 Crop Recommendation

### POST /predict/crop

**Request**

```json
{
  "soilType": "Black",
  "season": "Kharif",
  "N": 90,
  "P": 42,
  "K": 43,
  "location": "Hyderabad"
}
```

**Process**

1. Fetch weather
2. Preprocess
3. Call RF model

**Response**

```json
{
  "recommendedCrops": [
    {
      "crop": "Rice",
      "yield": 73,
      "price": 2100
    }
  ]
}
```

---

## 1.4 Price Prediction

### POST /predict/price

**Request**

```json
{
  "crop": "Rice",
  "months": 6
}
```

**Response**

```json
{
  "futurePrices": [2100, 2150, 2200]
}
```

---

## 1.5 Seed Shops

### GET /seeds?crop=Rice

---

## 1.6 Evaluation APIs

### POST /evaluate/noise

Runs perturbation experiment

```
input: crop parameters
output:
{
  "rss": 0.82,
  "prediction_changes": 9,
  "total_runs": 50
}
```

---

### POST /evaluate/missing

```
Simulates missing feature scenarios

output:
{
  "baseline_accuracy": 0.91,
  "missing_rainfall": 0.74,
  "missing_humidity": 0.69
}
```

---

### GET /evaluate/models

```
Returns predictions of all models

{
 "rf":"Rice",
 "xgb":"Rice",
 "svm":"Maize",
 "nn":"Rice"
}
```

---

### POST /evaluate/confidence

```
{
 "crop":"Rice",
 "confidence":0.82,
 "agreement":0.75,
 "stability":0.80
}
```

--- 

## 1.6 Evaluation APIs

### POST /evaluate/noise

Runs perturbation experiment

```
input: crop parameters
output:
{
  "rss": 0.82,
  "prediction_changes": 9,
  "total_runs": 50
}
```

---

### POST /evaluate/missing

```
Simulates missing feature scenarios

output:
{
  "baseline_accuracy": 0.91,
  "missing_rainfall": 0.74,
  "missing_humidity": 0.69
}
```

---

### GET /evaluate/models

```
Returns predictions of all models

{
 "rf":"Rice",
 "xgb":"Rice",
 "svm":"Maize",
 "nn":"Rice"
}
```

---

### POST /evaluate/confidence

```
{
 "crop":"Rice",
 "confidence":0.82,
 "agreement":0.75,
 "stability":0.80
}
```

---
# 📌 2. REACT PAGES DOCUMENT

## 2.1 Pages List

### 1. LoginPage

* email
* password
* validation
* JWT store

---

### 2. RegisterPage

* name
* email
* password
* confirm

---

### 3. Dashboard

Components:

* Navbar
* PredictionForm
* ResultCard
* History

---

### 4. CropFormPage

Fields:

* Soil Type → dropdown
* Season → dropdown
* N → number
* P → number
* K → number
* Location → text

Button → CALL /predict/crop

---

### 5. ResultPage

Show:

* Crop name
* Yield %
* Price
* Graph (LSTM)

---

### 6. SeedShopsPage

---

## 2.2 Component Structure

```
src/
├── pages/
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Dashboard.jsx
│
├── components/
│   ├── CropForm.jsx
│   ├── ResultCard.jsx
│   ├── Navbar.jsx
│
├── services/
│   └── api.js
```

---

# 📌 3. ML LAYER (PRD TEXT)

## 3.1 Model 1 – Crop Recommendation

### Algorithm

Random Forest Classifier

### Inputs

* N
* P
* K
* Soil Type
* Season
* Temp
* Humidity
* Rainfall

### Output

* Crop class
* Yield probability

### Preprocessing

* One-hot encode soil
* normalize NPK
* merge weather

---

## 3.2 Model 2 – Price Prediction

### Algorithm

LSTM

### Input

* historical price
* months

### Output

* future price sequence

---

## 3.3 Training Strategy

* 80% train
* 20% test
* Metrics:

  * Accuracy
  * RMSE

---

## 3.4 Inference Flow

1. Receive input
2. fetch weather
3. vectorize
4. RF → crop
5. LSTM → price

---

Additionally evaluate:
• stability across perturbations
• robustness across missing features
• inter-model agreement



# ➕ SECTION 13 – DATA PIPELINE

## 13.1 Dataset Source

* **Dataset Name:** Crop Recommendation Dataset
* **Format:** CSV
* **Records:** 2200
* **Features:** 7 input + 1 target
* **Target Column:** `label` (crop name)

### Schema

| Column      | Type   | Description        |
| ----------- | ------ | ------------------ |
| N           | int    | Nitrogen content   |
| P           | int    | Phosphorus content |
| K           | int    | Potassium content  |
| temperature | float  | °C                 |
| humidity    | float  | %                  |
| ph          | float  | soil pH            |
| rainfall    | float  | mm                 |
| label       | string | crop class         |

---

## 13.2 Cleaning Rules

Since dataset contains no nulls:

* No row deletion required
* No imputation required
* Ensure:

  * NPK values between 0–140
  * pH between 0–14
  * temperature 0–60

### Validation Script

* Reject negative values
* Clip extreme outliers at 1st & 99th percentile

---

## 13.3 Feature Engineering

1. **Label Encoding**

   * `label → numeric class`

2. **Normalization**

   * StandardScaler for:

     * temperature
     * humidity
     * rainfall
     * pH

3. **Derived Features**

   * nutrient_ratio = (N+P+K)/3
   * climate_index = temperature × humidity

---

## 13.4 Model Training Pipeline

1. Load CSV
2. Validate schema
3. Split:

   * 80% train
   * 20% test
   * stratify by label
4. Train Random Forest
5. Save artifacts

```text
models/
 ├── rf_crop.pkl
 ├── scaler.pkl
 └── label_encoder.pkl
```

---

## 13.5 Versioning

* Dataset version: v1.0
* Model version: v1.0
* Use hash of dataset for reproducibility
* Log:

  * date
  * parameters
  * accuracy

---

# ➕ SECTION 14 – BUSINESS RULES

## 14.1 Ranking Logic

1. RF returns top 3 crops with probabilities
2. For each crop:

   * call LSTM price
   * compute profit score

### Final Score

```text
score = (yield_prob × 0.6) + (price_norm × 0.4)
```

Rank by score desc.

---

## 14.2 Profit Formula

```text
estimated_profit =
    predicted_price × yield_probability
```

---

## 14.3 Default Values

If user enters 0 for NPK:

* use soil-type averages:

| Soil     | N  | P  | K  |
| -------- | -- | -- | -- |
| Black    | 70 | 40 | 50 |
| Red      | 40 | 30 | 35 |
| Alluvial | 60 | 35 | 40 |

---

# ➕ SECTION 15 – API SPEC DETAILS

## 15.1 Validation

### /predict/crop

* N,P,K: 0–140
* location: non-empty
* season: enum
* soilType: enum

Return 400 if invalid.

---

## 15.2 Error Contract

```json
{
  "error": true,
  "code": 400,
  "message": ""
}
```

Codes:

* 400 bad input
* 401 unauthorized
* 500 server

---

## 15.3 Security

* JWT authentication
* bcrypt passwords
* CORS whitelist
* rate limit 30/min
* input sanitization

---

# ➕ SECTION 16 – ML EXPERIMENTS

## 16.1 Metrics

* Accuracy
* Precision
* Recall
* F1
* RMSE (price)

---

## 16.2 Confusion Matrix

* per-crop performance
* macro average

---

## 16.3 Acceptance Criteria

* RF accuracy ≥ 95%
* RMSE ≤ 10% of avg price

---

```
Robustness Metrics:
• RSS (Recommendation Stability Score)
• Prediction Flip Rate
• Model Agreement Ratio
• Confidence Calibration Error
• Missing Feature Performance Drop
```

# ➕ SECTION 17 – DEPLOYMENT

## 17.1 Environment (.env)

```
DB_HOST=
DB_USER=
DB_PASSWORD=
JWT_SECRET=
WEATHER_KEY=
```

---

## 17.2 Deployment Architecture

### Frontend – Netlify
- React application hosted on Netlify  
- Continuous deployment from GitHub  
- Environment variables configured in Netlify dashboard  
- Public URL for user access

### Backend – Render (OnRender)
- FastAPI service deployed on Render  
- Automatic builds from GitHub repository  
- HTTPS enabled by default  
- Environment variables managed via Render secrets  
- Persistent MySQL connection

---

## 17.3 Deployment Flow

1. Developer pushes code to GitHub  
2. Netlify builds React frontend  
3. Render builds FastAPI backend  
4. Frontend calls backend via Render API URL  
5. Weather API integrated through secure key

---

## 17.4 Rate Limits

- Weather API: 60 requests/hour  
- Prediction API: 30 requests/minute  
- Authentication: 10 attempts/minute

---

## 17.5 Monitoring

- Render logs for backend  
- Netlify analytics for frontend  
- Error tracking via FastAPI logs  



# ✅ Design Goals

* Clear separation of concerns
* ML isolated from API
* Easy testing
* Reproducible training
* No circular imports
* Config driven
* Agent friendly

---
# 🚀 FINAL COMPLETE FILE STRUCTURE (UPDATED)

```
agri-genius/
│
├── backend/                         # FastAPI service layer
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── config.py                # env loader
│   │   ├── dependencies.py
│   │
│   │   ├── routers/                 # HTTP endpoints
│   │   │   ├── auth.py
│   │   │   ├── predict.py           # normal prediction
│   │   │   ├── evaluation.py        # robustness experiments APIs
│   │   │   ├── weather.py
│   │   │   └── seeds.py
│   │   │
│   │   ├── schemas/                 # request/response models
│   │   │   ├── user.py
│   │   │   ├── crop.py
│   │   │   ├── price.py
│   │   │   └── evaluation.py        # rss, confidence, comparison schema
│   │   │
│   │   ├── services/                # business logic
│   │   │   ├── auth_service.py
│   │   │   ├── weather_service.py
│   │   │   ├── prediction_service.py
│   │   │   ├── evaluation_service.py   # calls ML evaluation layer
│   │   │   └── seed_service.py
│   │   │
│   │   ├── models/                  # DB models
│   │   │   └── user.py
│   │   │
│   │   ├── utils/
│   │   │   ├── jwt.py
│   │   │   ├── validators.py
│   │   │   └── logger.py
│   │   │
│   │   └── middleware/
│   │       └── rate_limit.py
│   │
│   ├── tests/
│   │   ├── test_predict.py
│   │   └── test_evaluation.py
│   │
│   ├── requirements.txt
│   └── run.py
│
│
├── ml/                              # pure ML layer (NO FastAPI imports)
│   │
│   ├── dataset/
│   │   └── Crop_recommendation.csv
│   │
│   ├── preprocessing/
│   │   ├── clean.py
│   │   ├── encode.py
│   │   └── scale.py
│   │
│   ├── features/
│   │   └── feature_builder.py
│   │
│   ├── models/                      # saved trained models
│   │   ├── rf.pkl
│   │   ├── xgb.pkl
│   │   ├── svm.pkl
│   │   ├── mlp.pkl
│   │   ├── lstm_price.h5
│   │   ├── scaler.pkl
│   │   └── encoder.pkl
│   │
│   ├── training/
│   │   ├── train_rf.py
│   │   ├── train_xgb.py
│   │   ├── train_svm.py
│   │   ├── train_mlp.py
│   │   ├── train_lstm.py
│   │   └── split.py
│   │
│   ├── inference/
│   │   ├── predict_crop.py
│   │   ├── predict_price.py
│   │   └── predict_all_models.py
│   │
│   ├── evaluation/                  # research capability layer
│   │   ├── noise_injection.py       # perturb inputs
│   │   ├── rss.py                   # recommendation stability score
│   │   ├── missing_data.py          # feature removal tests
│   │   ├── model_comparison.py      # agreement across models
│   │   ├── confidence.py            # confidence scoring
│   │   └── runner.py                # orchestrates evaluation pipeline
│   │
│   ├── experiments/
│   │   ├── run_noise_experiment.py
│   │   ├── run_missing_experiment.py
│   │   ├── run_comparison.py
│   │   └── generate_report.py
│   │
│   └── notebooks/
│       └── exploration.ipynb
│
│
├── frontend/                        # React UI
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Predict.jsx
│   │   │   ├── Result.jsx
│   │   │   ├── Models.jsx           # model comparison view
│   │   │   ├── Stability.jsx        # RSS charts
│   │   │   └── Confidence.jsx       # reliability report
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── CropForm.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   ├── ModelTable.jsx
│   │   │   ├── StabilityChart.jsx
│   │   │   └── ConfidenceMeter.jsx
│   │   │
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── predictApi.js
│   │   │   └── evaluationApi.js
│   │   │
│   │   ├── hooks/
│   │   │   └── usePrediction.js
│   │   │
│   │   └── App.jsx
│   │
│   └── package.json
│
│
├── docs/                            # documentation
│   ├── PRD.md
│   ├── API.md
│   ├── EXPERIMENTS.md
│   └── README.md
│
│
├── scripts/                         # automation helpers
│   ├── retrain_models.sh
│   └── run_evaluations.sh
│
├── .env
└── README.md
```




# 🔹 Key Files Explanation

### backend/app/main.py

* FastAPI app
* include routers
* CORS

---

### ml/training/train_rf.py

* load CSV
* preprocess
* train RF
* save model

---

### services/ml_service.py

* load pkl
* predict
* merge weather

---

### frontend/services/api.js

* axios calls
* base URL

---


