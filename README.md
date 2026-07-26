<<<<<<< HEAD
# CyberGuardian AI

## AI-Based Cybersecurity Threat Detection and Monitoring System

---

## Problem Statement

Modern organizations generate a huge amount of security logs every day, making it difficult for security teams to manually identify suspicious activities and cyber threats.

CyberGuardian AI is developed to automatically monitor user behavior, detect anomalies, classify possible attacks, calculate threat risk, and provide security insights through an interactive SOC dashboard.

The system helps security analysts identify threats faster and supports incident investigation using machine learning and security intelligence.

---

## Features

### 1. Live Threat Monitor
- Real-time monitoring of security events
- Machine learning based anomaly detection
- Attack type identification
- Risk score calculation
- Threat level classification
- SOC status monitoring
- AI-generated security recommendations

### 2. Incident Dashboard
- View detected security incidents
- Filter incidents based on attack type and severity
- Incident history tracking
- Detailed incident analysis
- Download incident information

### 3. Risk Analytics
- Threat severity visualization
- Attack distribution analysis
- Security event trends
- Risk-based monitoring charts

### 4. MITRE ATT&CK Panel
- Maps detected attacks to MITRE ATT&CK techniques
- Displays:
  - Technique ID
  - Technique Name
  - Attack Tactic

Example:

Technique ID : T1021  
Technique    : Remote Services  
Tactic       : Lateral Movement

### 5. Security Reports
- Automatic incident report generation
- Root cause analysis
- Threat intelligence details
- Security recommendations
- Downloadable reports

### 6. Email Security Alerts
- Sends notifications for detected high-risk activities
- Provides attack details and risk information

---

# Architecture

                        User Activity Logs
                                |
                                |
                                v
                    Data Collection Layer
                                |
                                |
                                v
                    Data Preprocessing Layer
                                |
                                |
                                v
                Machine Learning Detection Engine
                                |
                --------------------------------
                |                              |
                v                              v
    Anomaly Detection Model        Attack Classification Model
    (Isolation Forest)             (Random Forest)
                |
                |
                v
                    Risk Assessment Engine
                (Risk Score + Threat Level)
                                |
                                |
                                v
                    Incident Response Engine
                --------------------------------
                |              |               |
                v              v               v
        Root Cause      MITRE ATT&CK    Threat Intelligence
        Analysis        Mapping            Analysis
                |
                |
                v
        Security Report Generator
                                |
                                |
                                v
                    Database Storage
                        (SQLite)
                                |
                                |
                                v
                    SOC Dashboard
                --------------------------------
                |              |               |
                v              v               v
        Live Threat Monitor  Incident     Risk Analytics
                            Dashboard
                                |
                                |
                                v
                        Email Alert System


## Architecture Components

### 1. Data Collection Layer
- Collects user activity and security event logs.
- Captures information such as:
  - Login activity
  - IP address
  - Location
  - Session duration
  - Device information

### 2. Data Processing Layer
- Cleans and prepares raw security data.
- Converts logs into a format suitable for machine learning models.

### 3. Machine Learning Detection Engine
- **Isolation Forest**
  - Detects abnormal user behavior and anomalies.

- **Random Forest**
  - Classifies detected attacks into categories such as:
    - Brute Force
    - Credential Stuffing
    - Lateral Movement
    - Impossible Travel
    - Device Spoofing

### 4. Risk Assessment Engine
- Calculates a risk score based on:
  - Anomaly score
  - Attack type
  - User behavior
  - Security indicators

- Assigns threat levels:
  - LOW
  - MEDIUM
  - HIGH
  - CRITICAL

### 5. Incident Analysis Layer
Provides additional security investigation:

- Root Cause Analysis
- MITRE ATT&CK technique mapping
- Threat Intelligence information
- AI-based recommendations

### 6. Database Layer
- Stores detected incidents and security reports.
- Uses SQLite for incident history management.

### 7. SOC Dashboard Layer
Provides security visualization:

- Live Threat Monitoring
- Incident Management
- Risk Analytics
- MITRE ATT&CK Panel
- Security Reports

### 8. Alert System
- Sends email notifications for high-risk security incidents.
- Helps security teams respond quickly.

---

# Technologies Used

## Programming Language

### Python
Used for:
- Machine learning model development
- Data processing
- Backend logic
- Security analysis pipeline


## Machine Learning

### Scikit-learn

Models implemented:

### Isolation Forest
Used for:
- Behavioral anomaly detection
- Identifying unusual user activities
- Detecting suspicious security events


### Random Forest Classifier

Used for:
- Attack classification
- Categorizing detected threats

Supported attack categories:

- Brute Force
- Credential Stuffing
- Device Spoofing
- Impossible Travel
- Insider Drift
- Lateral Movement
- Low and Slow


## Data Processing

### Pandas

Used for:

- Security log processing
- Feature extraction
- Data analysis


### NumPy

Used for:

- Numerical operations
- Machine learning computations


## Dashboard Development

### Streamlit

Used for:

- SOC dashboard interface
- Real-time security monitoring
- Interactive analytics


### Plotly

Used for:

- Threat visualization
- Security graphs
- Risk charts
- Attack analytics


## Database

### SQLite

Used for:

- Incident storage
- Security report history
- Threat tracking


## Security Framework

### MITRE ATT&CK

Used for:

- Attack technique mapping
- Threat investigation
- Security analyst support


---

# Machine Learning Pipeline


Security Logs

↓

Data Preprocessing

↓

Feature Extraction

↓

Anomaly Detection

(Isolation Forest)

↓

Attack Classification

(Random Forest)

↓

Risk Score Calculation

↓

Threat Level Assignment

↓

Incident Generation

↓

SOC Dashboard Visualization



---

# Model Evaluation

CyberGuardian AI evaluates model performance using:


## Anomaly Detection Metrics

Metrics used:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix


Example:

    Accuracy : 98%
    Precision : 59%
    Recall : 59%
    F1 Score : 59%



## Attack Classification Metrics

Metrics used:

- Accuracy
- Balanced Accuracy
- Precision
- Recall
- F1 Score
- Classification Report


Evaluation includes:

- Attack category performance
- Class-wise analysis
- Confusion matrix visualization


---

# Handling Imbalanced Dataset

Security datasets usually contain a large number of normal events compared to attacks.

CyberGuardian AI handles this challenge by:

- Separating attack events from normal activity
- Training attack classification only on malicious samples
- Applying balanced machine learning techniques
- Monitoring false positive rates


Attack categories supported:

    - Brute Force
    - Credential Stuffing
    - Device Spoofing
    - Impossible Travel
    - Insider Drift
    - Lateral Movement
    - Low and Slow



---

# False Positive Analysis

The system includes SOC alert budget analysis.

Implemented metrics:

- Total Events
- Alert Budget
- True Attacks
- False Positives
- False Positive Rate


Example:
 
    Total Events : 100000
    Alert Budget (1%) : 1000
    True Attacks : 990
    False Positives : 10
    False Positive Rate : 1%



This helps security analysts evaluate realistic alert workloads.


---

# Model Health Monitoring

CyberGuardian AI includes model monitoring capabilities.

Features:

- Feature drift detection
- Data distribution monitoring
- Model health analysis
- Concept drift identification


Example Output:
    Features Checked : 22
    Average Drift : 53.30%
    Model Status : DRIFT DETECTED



This helps security teams identify changing attack patterns and decide when model retraining is required.


---

# Real-Time Monitoring Workflow

                    ┌─────────────────────────┐
                    │   Security Event        │
                    │      Generated          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Live Stream           │
                    │   Simulator             │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Prediction Engine     │
                    │  (AI Processing Layer)  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Anomaly Detection     │
                    │   Isolation Forest      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Attack Classification │
                    │   Random Forest Model   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Risk Scoring Engine   │
                    │ Threat Level Analysis   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Incident Creation     │
                    │ Root Cause Analysis     │
                    │ MITRE Mapping           │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   SQLite Database       │
                    │ Incident Storage        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   SOC Dashboard Update  │
                    │ Live Monitoring &       │
                    │ Security Analytics      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Email Alert           │
                    │   Notification          │
                    └─────────────────────────┘



---

# How To Run

## 1. Clone Repository

```bash
git clone <repository-url>

Navigate to project folder:

cd CyberGuardian-AI

2. Create Virtual Environment

python -m venv .venv

Activate environment:

Windows
.venv\Scripts\activate

Linux / Mac

source .venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Train Machine Learning Models

Train anomaly detection:

python models/anomaly_model.py

Train attack classification model:

python models/attack_classifier.py

5. Start Real-Time Threat Simulation

Run:

python generator/live_stream.py

The simulator generates:

-> Normal security events
-> Suspicious activities
-> Attack scenarios

6. Start SOC Dashboard

Run:
## Access Dashboard

After starting the Streamlit application, open the browser and visit:

http://localhost:8501/

The CyberGuardian AI SOC Dashboard will be available with:

- Live Threat Monitoring
- Incident Reports
- Risk Analytics
- MITRE ATT&CK Mapping
- Model Health Monitoring
- Security Recommendations
- Threat Intelligence

For your own testing:

1. Start dashboard:

    streamlit run dashboard/app.py

2.Terminal will show something like:

    Local URL: http://localhost:8501
    Network URL: http://192.xxx.xxx.xxx:8501

3. Open:
    http://localhost:8501/

Output Screenshots

1. SOC Dashboard
    Shows:

    -> Live incident summary
    -> Current threat level
    -> Risk score gauge
    -> Security recommendations
    -> Attack analytics

2. Incident Report Dashboard

    Show:

    ✅ Incident details
    ✅ Root Cause Analysis
    ✅ MITRE ATT&CK Mapping
    ✅ Threat Intelligence
    ✅ Recommendation

3. Model Evaluation Dashboard

    Show:

    ✅ Accuracy
    ✅ Precision
    ✅ Recall
    ✅ F1 Score
    ✅ Classification report
    ✅ Graphs

4. Model Health Monitoring

    Show:

    ✅ Feature drift graph
    ✅ Drift percentage
    ✅ Model status

Future Improvements

1. Real Enterprise Security Log Integration

    Future versions can integrate with:

    SIEM platforms
    Authentication systems
    Cloud security services
    Enterprise monitoring tools

2. Advanced Real-Time Streaming

    Current system uses a simulated event stream.
    Future architecture:

            Security Logs

                    |

                    v

            Kafka / Message Queue

                    |

                    v

            Stream Processing Engine

                    |

                    v

            ML Threat Detection Pipeline

                    |

                    v

            SOC Dashboard


3. Deep Learning Based Detection

Future models:

-> Autoencoders
-> LSTM Networks
-> Transformer-based threat detection

These models can improve detection of complex behavioral patterns.

4. Advanced Threat Intelligence Integration

Future improvements:

-> Real-time IOC feeds
-> Malware intelligence sources
-> Vulnerability databases

5. Cloud Deployment

Future deployment options:

-> AWS
-> Microsoft Azure
-> Google Cloud Platform

Benefits:

-> Scalable security monitoring
-> Distributed processing
-> Enterprise-level deployment

Conclusion

CyberGuardian AI is an AI-powered cybersecurity monitoring platform that detects behavioral anomalies, classifies cyber attacks, calculates risk, and provides explainable security insights.

By combining machine learning, MITRE ATT&CK intelligence, risk analysis, and SOC visualization, the platform helps security analysts detect and investigate threats faster.

The system demonstrates the feasibility of using AI-driven behavioral analytics for modern cybersecurity operations.
                              =========================================================================================================================================

