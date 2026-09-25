# Social Media Impact Prediction

An end-to-end machine learning application that analyzes social media usage, lifestyle patterns, mental well-being, and academic factors to predict the overall impact of social media as **Beneficial, Neutral, or Negative**.

The project combines a modular machine learning pipeline with a **FastAPI backend** and a responsive web frontend for real-time prediction.

---

## Overview

Social media can affect different aspects of everyday life, including sleep, stress, mental well-being, and academic performance.

This project uses machine learning to identify patterns across these factors and classify the overall impact of social media usage into three categories:

* 🟢 **Beneficial**
* 🟡 **Neutral**
* 🔴 **Negative**

The application is designed as a complete ML product rather than only a model-training notebook.

---

## Features

* Multiclass classification
* Numerical and categorical feature processing
* Missing-value handling
* Class-imbalance handling using **SMOTENC**
* Logistic Regression model
* Modular ML training pipeline
* Saved preprocessing and model components
* FastAPI REST API
* Interactive web interface
* Real-time predictions
* Personalized result insights
* Responsive frontend

---

## Machine Learning Pipeline

The project follows a modular machine learning workflow:

```text
Raw Dataset
     │
     ▼
Data Ingestion
     │
     ▼
Train / Test Split
     │
     ▼
Data Transformation
     │
     ├── Numerical Features
     │       ├── Missing Value Imputation
     │       ├── Transformation
     │       └── Scaling
     │
     └── Categorical Features
             ├── Missing Value Imputation
             ├── Encoding
             └── Processing
     │
     ▼
SMOTENC
     │
     ▼
Logistic Regression
     │
     ▼
Model Evaluation
     │
     ▼
Saved Model + Preprocessors
     │
     ▼
FastAPI Prediction API
     │
     ▼
Web Application
```

---

## Input Features

The model uses the following information:

| Feature                     | Description                                |
| --------------------------- | ------------------------------------------ |
| Age                         | User age                                   |
| Gender                      | User gender                                |
| Academic Level              | Current academic level                     |
| Primary Platform            | Main social media platform                 |
| Daily Usage Hours           | Average daily social media usage           |
| Weekend Extra Hours         | Additional weekend usage                   |
| Device Type                 | Primary device used                        |
| Sleep Duration              | Average sleep duration                     |
| Sleep Quality Score         | Self-reported sleep quality                |
| Late Night Usage            | Whether social media is used late at night |
| Social Comparison Frequency | Frequency of social comparison             |
| Perceived Stress Score      | Perceived stress level                     |
| Mental Health Index         | Mental well-being indicator                |
| Academic Performance GPA    | Academic performance                       |

---

## Model

### Logistic Regression

The final classification model is **Logistic Regression**.

Because the target classes are imbalanced, **SMOTENC (Synthetic Minority Over-sampling Technique for Nominal and Continuous features)** is applied during training to improve representation of minority classes.

The sampling process is performed only on the training data to avoid data leakage.

---

## Backend

The prediction service is built using **FastAPI**.

### API Endpoint

```text
POST /
```

Example request:

```json
{
  "Age": 20,
  "Gender": "Male",
  "Academic_Level": "Undergraduate",
  "Primary_Platform": "YouTube",
  "Daily_Usage_Hours": 2.5,
  "Weekend_Extra_Hours": 1.5,
  "Device_Type": "Laptop",
  "Sleep_Duration_Hours": 7.5,
  "Sleep_Quality_Score": 8,
  "Late_Night_Usage": "No",
  "Social_Comparison_Frequency": "Rarely",
  "Perceived_Stress_Score": 3,
  "Mental_Health_Index": 8,
  "Academic_Performance_GPA": 8.5
}
```

Example response:

```json
{
  "predicted_classification": "Beneficial"
}
```

---

## Project Structure

```text
social-media-impact/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── src/
│   ├── Components/
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   └── model_evaluation.py
│   │
│   ├── Pipeline/
│   │   ├── train_pipeline.py
│   │   └── predict_pipeline.py
│   │
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
│
├── Notebook/
│   └── model_new.ipynb
│
├── app.py
├── setup.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Tech Stack

### Machine Learning

* Python
* NumPy
* Pandas
* Scikit-learn
* Imbalanced-learn
* SMOTENC
* Logistic Regression

### Backend

* FastAPI
* Pydantic
* Uvicorn

### Frontend

* HTML5
* CSS3
* JavaScript

### Development

* Git
* GitHub
* Jupyter Notebook

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/spandan9054/social-media-impact.git
cd social-media-impact
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI server

```bash
uvicorn app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Run the frontend

Open the `frontend` directory using a local server.

For example, with VS Code Live Server:

```text
http://127.0.0.1:5500/
```

---

## Prediction Flow

```text
User Input
    ↓
Frontend
    ↓
FastAPI
    ↓
Pydantic Validation
    ↓
Preprocessor
    ↓
Postprocessor
    ↓
Trained Logistic Regression
    ↓
Label Encoder
    ↓
Prediction
    ↓
Frontend Result
```

---

## Important Notes

SMOTENC is used **only during model training**.

During prediction, the input follows the saved preprocessing pipeline and is passed directly to the trained model.

The application is intended for **educational and analytical purposes**. Predictions represent patterns learned from the dataset and should not be interpreted as medical, psychological, or academic diagnoses.

---

## Author

**Spandan Sarkar**

B.Tech — Electronics & Communication Engineering

GitHub: [@spandan9054](https://github.com/spandan9054)

---

## License

This project is available for educational and personal use.
