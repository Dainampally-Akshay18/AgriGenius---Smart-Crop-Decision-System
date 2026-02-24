# FRONTEND PRODUCT REQUIREMENT DOCUMENT (PRD)

## Product Name: AGRI-GENIUS

AI-Based Crop Recommendation & Model Evaluation Platform

---

## 1. Product Overview

AGRI-GENIUS is a web application that helps users predict suitable crops based on soil nutrients and weather conditions.
It also provides AI model evaluation tools including noise stability, missing feature impact, and model agreement comparison.

The frontend must provide a guided workflow:
Login → Dashboard → Input Soil & City → Prediction Workspace → Model Evaluations

---

## 2. Target Users

* Farmers
* Agricultural Researchers
* Students
* Agritech Analysts

---

## 3. Core Features

### 3.1 Authentication

Users must authenticate before accessing any feature.

Functions:

* User Signup
* User Login
* Secure session using JWT
* Auto redirect unauthorized users to login page

Pages:

* Login Page
* Signup Page

---

### 3.2 Dashboard

Purpose:
Introduce the platform and start prediction process.

Contents:

* Brief description of AGRI-GENIUS
* "Start Predicting" button

Action:
Redirects user to prediction input form

---

### 3.3 Prediction Input Form

User provides soil data and location.

Inputs:

* Nitrogen (N)
* Phosphorus (P)
* Potassium (K)
* City (Dropdown)

Auto-Fetched Weather Data:

* Temperature
* Humidity
* Rainfall

Action:
User clicks "Predict" → opens Evaluation Workspace

---

### 3.4 Evaluation Workspace

Layout:
Persistent sidebar + dynamic content area

Sidebar Options:

1. Crop Prediction
2. Noise Stability Evaluation
3. Missing Feature Evaluation
4. Model Agreement Evaluation

Each option loads its own page and calls respective backend API.

---

## 4. Feature Details

### 4.1 Crop Prediction

Displays:

* Recommended crop
* Confidence score
* Input parameters used

---

### 4.2 Noise Stability Evaluation

Runs model multiple times with noisy inputs.

Displays:

* Stability score
* Prediction variations table

---

### 4.3 Missing Feature Evaluation

Evaluates model behavior when some features are missing.

Displays:

* Feature importance impact
* Model robustness explanation

---

### 4.4 Model Agreement Evaluation

Compares multiple algorithms:

* Random Forest
* XGBoost
* SVM
* MLP

Displays:

* Predictions from each algorithm
* Agreement percentage
* Final consensus prediction

---

## 5. Navigation Flow

Login → Dashboard → Input Form → Evaluation Workspace

Inside Workspace:
Sidebar switches between 4 evaluation modules without leaving layout

---

## 6. UI/UX Requirements

* Clean modern interface
* Responsive (mobile + desktop)
* Sidebar navigation
* Loading indicators for API calls
* Error messages for failed requests
* Consistent theme across pages

---

## 7. Security Requirements

* Store JWT securely in browser storage
* Protect all routes except login/signup
* Redirect to login if token invalid

---

## 8. Non-Functional Requirements

* Fast loading
* Reusable components
* Modular JavaScript
* Clear API error handling

---

## 9. Expected Output From Frontend

* Multi-page responsive UI
* Proper API integration
* Dynamic rendering of prediction results
* No hardcoded AI outputs


# FRONTEND ARCHITECTURE CONTRACT (MANDATORY)

You must STRICTLY follow the existing project structure.
Do NOT create new root folders.
Do NOT restructure the project.
Do NOT convert to another framework.
Do NOT modify Vite configuration.

Framework: React (Vite) + Tailwind CSS

Existing Structure:

/src
/assets
/Components
/Pages
/Services
App.jsx
main.jsx
App.css
index.css

---

FILE RESPONSIBILITIES

Pages folder = Full Screens / Routes only
Components folder = Reusable UI pieces
Services folder = API logic only (fetch/axios calls)
assets = images/icons only

NO API CALLS inside Pages or Components
All API calls MUST go inside Services

---

REQUIRED FILE CREATION

Create the following files exactly:

/src/Pages
Login.jsx
Signup.jsx
Dashboard.jsx
PredictForm.jsx
Prediction.jsx
Noise.jsx
Missing.jsx
Agreement.jsx

/src/Components
Navbar.jsx
Sidebar.jsx
ProtectedRoute.jsx
Loading.jsx
ErrorMessage.jsx
WeatherAutoFill.jsx

/src/Services
api.js
authService.js
predictionService.js
evaluationService.js

---

ROUTING RULES

* Use React Router
* Routing defined only inside App.jsx
* Protected routes must wrap all pages except Login & Signup
* After login → redirect to /dashboard
* After form submit → redirect to /prediction

---

STATE MANAGEMENT RULES

* Use React hooks only
* Do NOT use Redux / Context API unless required for auth
* Store JWT in localStorage
* Global auth state handled via custom hook in authService

---

API RULES

Backend endpoints are already defined.
You must:

* Read backend folder
* Map each endpoint into Services layer
* Never hardcode response
* Handle loading and error states

---

UI RULES

* Tailwind only (no CSS frameworks)
* Sidebar layout for evaluation pages
* Fully responsive
* Consistent spacing and typography

---

CRITICAL RULE

You are NOT generating a new project.
You are implementing features INSIDE an existing project.

Only create files listed above and fill them with code.
Do not add extra folders.
Do not rename folders.
Do not change case sensitivity.


# API CONTRACT — AGRI-GENIUS FRONTEND INTEGRATION

Base URL:
http://127.0.0.1:5000

All protected routes require header:
Authorization: Bearer <JWT_TOKEN>

Content-Type: application/json

====================================================
AUTHENTICATION
==============

POST /api/auth/register

Request Body:
{
"name": string,
"email": string,
"password": string
}

Success Response (201):
{
"message": string,
"token": string,
"user": object
}

---

POST /api/auth/login

Request Body:
{
"email": string,
"password": string
}

Success Response (200):
{
"message": string,
"token": string,
"user": object
}

Frontend Rule:
Save token in localStorage as "token"

====================================================
WEATHER (NO AUTH REQUIRED)
==========================

GET /api/weather?location=<CITY>

Response (200):
{
"temperature": number,
"humidity": number,
"rainfall": number
}

Frontend Rule:
Auto-fill weather fields when user selects city

====================================================
CROP PREDICTION
===============

POST /api/predict/crop

Headers:
Authorization: Bearer <token>

Request Body:
{
"soilType": string,
"season": string,
"N": number,
"P": number,
"K": number,
"location": string
}

Response:
{
"recommendedCrops": [
{
"crop": string,
"yield": number,
"price": number
}
]
}

Frontend Rule:
Display top recommended crop

====================================================
NOISE STABILITY EVALUATION
==========================

POST /api/evaluate/noise

Request Body:
(Same as predict request)

Response:
{
"predicted_crop": string,
"rss": number,
"prediction_changes": number,
"total_runs": number,
"noise_percentage": number,
"prediction_distribution": object
}

Frontend Rule:
Show RSS score and prediction distribution table

====================================================
MISSING FEATURE EVALUATION
==========================

POST /api/evaluate/missing

Request Body:
(Same as predict request)

Response:
{
"predicted_crop": string,
"baseline_confidence": number,
"stability_score": number,
"total_tests": number,
"prediction_changes": number,
"feature_results": object
}

Frontend Rule:
Display feature impact list

====================================================
MODEL AGREEMENT EVALUATION
==========================

POST /api/evaluate/agreement

Request Body:
(Same as predict request)

Response:
{
"predicted_crop": string,
"total_models": number,
"agreement_ratio": number,
"all_agree": boolean,
"predictions": object,
"prediction_distribution": object
}

Frontend Rule:
Compare predictions from RF, XGB, SVM, MLP

====================================================
FULL EVALUATION (OPTIONAL PAGE)
===============================

POST /api/evaluate/full

Request Body:
(Same as predict request)

Response:
{
"predicted_crop": string,
"confidence": number,
"confidence_level": string,
"probability": number,
"stability": number,
"agreement": number,
"rss_score": number,
"missing_feature_stability": number,
"model_agreement_ratio": number,
"noise_test": object,
"missing_feature_test": object,
"model_agreement_test": object
}

Frontend Rule:
Display overall confidence dashboard

====================================================
ERROR RESPONSE (ALL APIS)
=========================

422 Validation Error:
{
"detail": [
{
"msg": string
}
]
}

Frontend must show error message toast
