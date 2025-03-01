Here’s a **detailed `README.md`** for your **fraud detection system**. It includes an overview, setup instructions, deployment steps, and usage guidelines.

---

## **🚀 Credit Card Fraud Detection System**
This project implements a **real-time fraud detection system** using **machine learning and Flask**, with AWS **Lambda** and **Docker**.

**Key Features:**
- 🏦 **Credit card transaction fraud detection**
- 🔗 **Flask API** for fraud prediction
- 🐍 **Python-based machine learning model**
- 📦 **Dockerized deployment**
- ☁️ **AWS Lambda for real-time processing**
- 📊 **Jupyter Notebook for model training**

---

## **📂 Project Structure**
```
FRAUDDETECTION/
│── flask-ml-api/            # Flask API for Fraud Prediction
│   │── app.py               # API entry point
│   │── Dockerfile           # Docker setup for deployment
│   │── preprocessor.pkl     # Data preprocessing pipeline
│   │── rf_model.pkl         # Trained ML model (Random Forest)
│   │── requirements.txt     # Dependencies for Flask API
│── lambda/                  # AWS Lambda Function
│   │── lambda_handler.py    # AWS Lambda fraud detection script
│── model_training/          # Jupyter Notebook for ML training
│   │── credit-card-fraud-detection.ipynb
│── producer/                # Simulation of transactions
│   │── producer.py
│── README.md                # Documentation
```

---

## **⚡ Quick Start**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/fraud-detection.git
cd fraud-detection
```

### **2️⃣ Install Dependencies**
#### **For Flask API**
```bash
cd flask-ml-api
pip install -r requirements.txt
```

#### **For Jupyter Notebook**
```bash
cd model_training
pip install -r requirements.txt
jupyter notebook
```

---

## **🚀 Running the Flask API Locally**
1. Navigate to the Flask API directory:
   ```bash
   cd flask-ml-api
   ```

2. Run the API:
   ```bash
   python app.py
   ```

3. The API should be available at:  
   ```
   http://127.0.0.1:5000/predict
   ```

4. Test it using `curl`:
   ```bash
   curl -X POST "http://127.0.0.1:5000/predict" -H "Content-Type: application/json" -d '{"amount": 100, "card_type": "Visa"}'
   ```

---

## **🐳 Running the Flask API in Docker**
1. **Build the Docker Image:**
   ```bash
   docker build -t fraud-detection-api .
   ```

2. **Run the Container:**
   ```bash
   docker run -p 5000:5000 fraud-detection-api
   ```

---

## **📡 Deploying to AWS Lambda**
1. **Zip the Lambda function**
   ```bash
   cd lambda
   zip lambda_handler.zip lambda_handler.py
   ```

2. **Upload to AWS Lambda**
   ```bash
   aws lambda update-function-code --function-name fraudDetectionLambda --zip-file fileb://lambda_handler.zip
   ```

---

## **📊 Model Training**
1. Open the Jupyter Notebook:
   ```bash
   cd model_training
   jupyter notebook
   ```
2. Run `credit-card-fraud-detection.ipynb` to **train the model**.

---

## **🛠 Technologies Used**
- **Python** 🐍 (Machine Learning & API)
- **Flask** 🚀 (Web API)
- **Docker** 🐳 (Containerization)
- **AWS Lambda** ☁️ (Serverless Function)
- **Jupyter Notebook** 📓 (ML Model Training)
- **scikit-learn** 🤖 (Machine Learning)

---

## **📜 API Endpoints**
| Method | Endpoint             | Description |
|--------|----------------------|-------------|
| `POST` | `/predict`           | Predicts if a transaction is fraud |



