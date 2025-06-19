# Ride2Gather

Ride2Gather is a web application that connects users for shared rides. It features a **Flask RESTful API backend** and a **Vue frontend**.

## 🚀 Project Structure

```
Ride2Gather/
├── backend/     # Flask RESTful API
└── frontend/    # Vue frontend
```

---

## 🐳 Option 1: Run with Docker (Recommended)

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed

### Steps

```bash
git clone https://github.com/JasonOw718/Ride2Gather.git
cd Ride2Gather
```

1. Create a `.env` file inside the `/frontend` folder with the following content:

   ```
   VITE_API_BASE_URL=http://127.0.0.1:5000/api
   ```

2. Run the application:

   ```bash
   docker compose up
   ```

---

## 🧪 Option 2: Run Without Docker (Manual Setup)

### Prerequisites

- Python 3.x
- Node.js and npm

### Steps

```bash
git clone https://github.com/JasonOw718/Ride2Gather.git
cd Ride2Gather
```

1. Create a `.env` file inside the `/frontend` folder with the following content:

   ```
   VITE_API_BASE_URL=http://127.0.0.1:5000/api
   ```

2. Run the **backend**:

   ```bash
   cd backend
   python -m venv venv
   venv/Scripts/activate  # Use `source venv/bin/activate` on macOS/Linux
   pip install -r requirements.txt
   python run.py
   ```

3. Run the **frontend**:

   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

---

## 🗂 Folder Overview

- `/backend`: Flask RESTful API
- `/frontend`: Vue frontend application

---

## 📬 API Base URL

Make sure the `VITE_API_BASE_URL` in `.env` points to your backend API:

```
VITE_API_BASE_URL=http://127.0.0.1:5000/api
```
