# 🌾 AgripredictAI1

**Empowering Farmers with AI-Driven Crop Predictions & Market Intelligence**

Farmers currently grow crops without knowing future prices or demand, which leads to significant losses. Our **AI system predicts market trends** and suggests the most profitable crops, helping farmers make better decisions before cultivation.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

AgripredictAI1 is an intelligent agricultural prediction platform that leverages machine learning and AI to:

- **Predict crop prices** using historical market data
- **Forecast demand trends** across regions
- **Recommend profitable crops** based on current market conditions
- **Provide multilingual support** for farmers in different regions
- **Send real-time alerts** via SMS and email
- **Enable voice-based interactions** for accessibility

This system bridges the gap between farmers and market intelligence, enabling data-driven decision-making in agriculture.

---

## ��� Features

### 🤖 AI & ML Capabilities
- **Market Trend Analysis** - Analyzes historical crop prices and market patterns
- **Crop Recommendation Engine** - Suggests most profitable crops based on location and season
- **Price Prediction** - Forecasts future crop prices using ML models
- **Demand Forecasting** - Predicts market demand for various crops

### 📱 User Communication
- **SMS Alerts** - Real-time notifications via Twilio or Fast2SMS
- **Email Notifications** - Market updates and crop recommendations
- **Voice Interface** - Accessibility for non-tech-savvy farmers
- **Multilingual Support** - Supports multiple languages via Google Translate API

### 🤝 Integration
- **Weather API Integration** - Real-time weather data for crop planning
- **Market Data APIs** - Live market price feeds
- **OpenAI Integration** - Chatbot for farmer support
- **CORS Enabled** - Frontend-backend integration ready

### 🔐 Security
- **JWT Authentication** - Secure user authentication
- **Role-Based Access Control** - Different access levels for users
- **Secure Configuration** - Environment-based secrets management

---

## 🏗️ Project Architecture

```
AgripredictAI1/
├── app/                          # FastAPI Application
│   ├── main.py                  # Application entry point
│   ├── api/                     # API endpoints
│   │   ├── auth_api.py         # Authentication routes
│   │   ├── prediction_api.py   # Prediction endpoints
│   │   ├── market_api.py       # Market data endpoints
│   │   └── alert_api.py        # Alert management
│   ├── core/
│   │   ├── config.py           # Configuration & settings
│   │   └── security.py         # Security utilities
│   ├── db.py                    # Database connection
│   ├── models/                  # Pydantic models (schemas)
│   └── services/                # Business logic
│
├── ml_models/                   # Machine Learning Models
│   ├── price_prediction/        # Price forecasting models
│   ├── demand_forecast/         # Demand prediction models
│   └── crop_recommendation/     # Recommendation engine
│
├── pipelines/                   # Data Processing Pipelines
│   ├── data_ingestion.py       # Data collection
│   ├── preprocessing.py         # Data cleaning
│   └── model_training.py        # ML model training
│
├── frontend/                    # React Frontend (optional)
│   └── [React components]
│
├── Data/                        # Training & Historical Data
│   └── [Datasets]
│
├── alerts/                      # Alert Management
│   ├── sms_alerts.py           # SMS notifications
│   └── email_alerts.py         # Email notifications
│
├── logs/                        # Application Logs
├── tests/                       # Unit & Integration Tests
├── docs/                        # API Documentation
├── scripts/                     # Utility Scripts
├── simulation/                  # Testing & Simulation
├── requirements.txt             # Python Dependencies
├── .env.example                 # Environment template
├── .env                         # Local environment (gitignored)
└── README.md                    # This file
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Python 3.10+** - Programming language
- **SQLite** - Default database (configurable)
- **Pydantic** - Data validation & settings management
- **Pydantic Settings** - Environment configuration

### Machine Learning
- **Scikit-learn** - ML algorithms
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **TensorFlow/Keras** - Deep learning (optional)

### Integrations
- **Twilio** - SMS messaging
- **Fast2SMS** - SMS (India-specific)
- **Gmail SMTP** - Email notifications
- **OpenAI** - Chatbot & AI features
- **Google Translate** - Multilingual support
- **Weather API** - Real-time weather data
- **Market Data APIs** - Live price feeds

### Frontend (Optional)
- **React** - UI framework
- **Axios** - HTTP client
- **Redux** - State management

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip or conda package manager
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/Ariyan-Sitansu1115/AgripredictAI1.git
cd AgripredictAI1
```

### Step 2: Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# (See Configuration section below)
```

---

## ⚙️ Configuration

### Step 1: Environment Variables
Create a `.env` file in the project root with the following configuration:

```env
# Server Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=sqlite:///./agripredict.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# External APIs
WEATHER_API_KEY=your-weather-api-key
MARKET_DATA_API_KEY=your-market-data-api-key

# Email Configuration (Gmail SMTP)
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password

# SMS Provider: "twilio" or "fast2sms"
SMS_PROVIDER=twilio

# SMS Configuration – Twilio
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# SMS Configuration – Fast2SMS (India)
FAST2SMS_API_KEY=your-fast2sms-api-key
FAST2SMS_ROUTE=q

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Logging
LOG_LEVEL=INFO
```

### Step 2: Obtain API Keys

#### Weather API
- Sign up at [OpenWeatherMap](https://openweathermap.org/api)
- Get your API key from dashboard

#### Market Data API
- Register at your preferred market data provider
- Obtain API credentials

#### SMS Provider (Choose One)

**Twilio:**
1. Sign up at [Twilio Console](https://console.twilio.com)
2. Get Account SID and Auth Token
3. Verify your phone number

**Fast2SMS (India):**
1. Register at [Fast2SMS](https://www.fast2sms.com)
2. Get your API key
3. Select route preference

#### Email (Gmail)
1. Enable 2-Factor Authentication on your Gmail account
2. Generate [App Password](https://myaccount.google.com/apppasswords)
3. Use the 16-character password in `.env`

#### OpenAI
1. Sign up at [OpenAI](https://platform.openai.com)
2. Generate API key from dashboard
3. Set usage limits for cost control

---

## 🚀 Usage

### Step 1: Run the Application
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 2: Access the Application

- **API Base URL:** `http://localhost:8000`
- **API Docs (Swagger UI):** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Step 3: Run Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app
```

### Step 4: Train ML Models (Optional)
```bash
python pipelines/model_training.py
```

---

## 📡 API Endpoints

### Authentication
- `POST /auth/register` - Register new farmer
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - User logout

### Predictions
- `GET /predictions/price` - Get price predictions
- `POST /predictions/crop-recommendation` - Get crop recommendations
- `GET /predictions/demand` - Get demand forecasts

### Market Data
- `GET /market/prices` - Current market prices
- `GET /market/trends` - Market trends analysis
- `GET /market/regions` - Regional market data

### Alerts
- `POST /alerts/subscribe` - Subscribe to alerts
- `GET /alerts/history` - Get alert history
- `DELETE /alerts/{alert_id}` - Unsubscribe from alert

### Chat/Support
- `POST /chat/message` - Send message to chatbot
- `GET /chat/history` - Get conversation history

---

## 📁 Project Structure

```
app/
├── main.py                      # FastAPI application setup
├── api/
│   ├── __init__.py
│   ├── auth_api.py             # /auth endpoints
│   ├── prediction_api.py        # /predictions endpoints
│   ├── market_api.py            # /market endpoints
│   └── alert_api.py             # /alerts endpoints
├── core/
│   ├── __init__.py
│   ├── config.py                # Settings & configuration
│   ├── security.py              # JWT, password hashing
│   └── constants.py             # App constants
├── db.py                        # Database session management
├── models/
│   ├── __init__.py
│   ├── user.py                  # User schema
│   ├── prediction.py            # Prediction schema
│   ├── market.py                # Market data schema
│   └── alert.py                 # Alert schema
└── services/
    ├── __init__.py
    ├── prediction_service.py     # Prediction logic
    ├── market_service.py         # Market data logic
    ├── alert_service.py          # Alert logic
    └── external_api_service.py   # External API calls

ml_models/
├── price_prediction/
│   ├── model.pkl
│   └── train.py
├── demand_forecast/
│   ├── model.pkl
│   └── train.py
└── crop_recommendation/
    ├── model.pkl
    └── train.py

pipelines/
├── data_ingestion.py            # Fetch market data
├── preprocessing.py              # Data cleaning
└── model_training.py            # Train models

alerts/
├── sms_alerts.py                # Twilio / Fast2SMS
└── email_alerts.py              # Gmail SMTP

tests/
├── test_auth.py
├── test_predictions.py
├── test_market.py
└── test_alerts.py
```

---

## 🔧 Troubleshooting

### Pydantic ValidationError
If you get `ValidationError: Extra inputs are not permitted`:
1. Ensure all variables in `.env` are defined in `app/core/config.py`
2. Or add `extra = "ignore"` to the `Settings.Config` class

### SMS Not Sending
- Verify Twilio/Fast2SMS credentials are correct
- Check if phone number format is valid (include country code)
- Ensure account has sufficient balance

### Email Not Sending
- Enable "Less secure app access" or use App Password
- Verify Gmail credentials in `.env`
- Check firewall/network settings

### Database Errors
- Ensure database file has write permissions
- Delete `.db` file to reset database
- Check `DATABASE_URL` in `.env`

---

## 🤝 Contributing

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AgripredictAI1.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes and commit**
   ```bash
   git add .
   git commit -m "Add your feature description"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**
   - Describe your changes clearly
   - Reference any related issues

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact & Support

- **GitHub Issues:** [Report bugs here](https://github.com/Ariyan-Sitansu1115/AgripredictAI1/issues)
- **Email:** Contact project maintainers
- **Discussions:** [GitHub Discussions](https://github.com/Ariyan-Sitansu1115/AgripredictAI1/discussions)

---

## 🙏 Acknowledgments

- FastAPI community for excellent documentation
- OpenAI for powerful AI models
- Twilio & Fast2SMS for reliable messaging
- All contributors and farmers using AgripredictAI

---

**Made with ❤️ by Ariyan-Sitansu1115**

*Empowering agriculture through AI innovation* 🌾🤖
