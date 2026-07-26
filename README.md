# 🌱 AgriLink – AI Smart Farming Assistant

> 🤖 A full-stack AI-powered agriculture platform for disease detection, crop recommendation, and smart farming guidance.

---

## 📌 Overview

AgriLink is an intelligent farming assistant designed to help farmers identify crop diseases, receive treatment suggestions, and make informed decisions about crop selection. It integrates AI-based disease detection, rule-based crop recommendation, and detailed farming roadmaps.

---

## 🎯 Features

### 🌿 Disease Detection

* Detect diseases using image upload (TensorFlow model)
* Supports multiple crops (Rice, Cotton, Chilli, Maize, Tomato, etc.)
* Provides:

  * Disease name
  * Confidence score
  * Chemical treatment
  * Organic treatment
  * Product recommendation

---

### 📋 Symptom-Based Detection

* Users can select symptoms manually
* Instant disease identification without image

---

### 🌾 Crop Recommendation

* Suggests best crops based on:

  * Soil type
  * Weather (Temperature & Humidity)
  * Location
  * Budget
  * Water source

---

### 📊 Crop Roadmap

* Step-by-step farming guidance:

  * Sowing
  * Fertilization
  * Irrigation
  * Harvest timeline

---

### 🗺️ Nearby Shops Finder

* Uses map integration to find fertilizer shops
* Helps farmers access required products easily

---

### 🌐 Multi-language Support

* English
* Telugu

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **AI Model:** TensorFlow / Keras
* **Frontend:** HTML, CSS, JavaScript
* **Image Processing:** PIL, NumPy
* **APIs:** REST APIs
* **Maps Integration:** Google Maps

---
## System Architecture
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/a75fb25a-157c-4ad9-b6c3-585e02bb5205" />



## 🧠 How It Works

1. User uploads crop image or selects symptoms
2. AI model predicts disease
3. Backend validates prediction using crop logic
4. System returns treatment + product suggestions
5. Crop recommendation engine suggests suitable crops
6. Roadmap provides step-by-step farming guidance

---

## 📂 Project Structure

```
AgriLink/
│── main.py
│── keras_model.h5
│── labels.txt
│── templates/
│── static/
│── screenshots/
```

---

## 🚀 How to Run

```bash
git clone https://github.com/sathish-00/agrilink.git
cd agrilink
pip install -r requirements.txt
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 📸 Screenshots

### 🏠 Home Page
<img width="2048" height="1034" alt="home1" src="https://github.com/user-attachments/assets/4e952c87-c605-45d2-8374-48a45edb0711" />


### 🔍 Disease Detect
<img width="1916" height="969" alt="dease detect" src="https://github.com/user-attachments/assets/49ff12a1-4410-44de-bb9e-c83433e8e62a" />
<img width="902" height="421" alt="detect-disease" src="https://github.com/user-attachments/assets/073ffe6e-4318-45e7-bb4f-666c5ec18ba9" />
<img width="928" height="549" alt="d1" src="https://github.com/user-attachments/assets/2aceb180-27f7-4757-946b-f4e0671c7652" />

### 🧪 Disease Result & Treatment

<img width="923" height="793" alt="results1" src="https://github.com/user-attachments/assets/f2a8bd14-20b5-4667-90e3-2b44c1f07e64" />
<img width="919" height="726" alt="r" src="https://github.com/user-attachments/assets/44c8d238-791d-4209-85bd-3f910df22a5f" />

### 🌾 Crop Recommendation
<img width="1911" height="943" alt="crop-recomendation" src="https://github.com/user-attachments/assets/fd0198ec-cba9-4636-813e-f5ab2c315558" />

### 📊 Recommended Crops

<img width="1674" height="864" alt="crop-recomendation-1" src="https://github.com/user-attachments/assets/0e631799-0011-4ead-9cba-9009d2551376" />
d.png)

### 📈 Crop Roadmap
<img width="1899" height="863" alt="crop-roadmap" src="https://github.com/user-attachments/assets/9be3b9e1-6cae-43b1-9605-86c69645eaa6" />

### 🗺️ Nearby Shops
<img width="1576" height="704" alt="near-by-fertilizers" src="https://github.com/user-attachments/assets/5826789b-d5a2-4ce8-8d62-383c465f89c4" />

### 🌐 Telugu Support
<img width="1632" height="953" alt="tel" src="https://github.com/user-attachments/assets/773050c2-32c8-48bc-ad67-a6ad9a0ab0bb" />

###Contact US

<img width="1651" height="941" alt="co" src="https://github.com/user-attachments/assets/912ad534-912d-4c9b-b218-92292c0187ac" />

---

## 🔐 Key Highlights

* AI + Agriculture integration 🤖🌾
* Real-world farmer problem solving
* Multi-language support
* Smart fallback system
* End-to-end full stack project

---

## 🎯 Future Improvements

* Mobile application
* Real-time weather API
* Voice assistant for farmers
* More crop support

---

## 🙌 Author

**Sathish**
GitHub: https://github.com/sathish-00

---

## ⭐ Contribution

Feel free to fork and improve this project!
