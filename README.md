# UI Architect: Multi-Agent Local UI Generator

A Master's level AI portfolio project that autonomously generates and iteratively refines pixel-perfect React/Tailwind UI components without relying on external APIs. 

Built entirely locally using **Ollama**, **NestJS**, **React**, **Playwright**, and a **Custom ML Critic Model**.

## 🧠 Architecture

The system operates on an iterative agentic loop:
1. **Scaffold Injection**: The user prompt is matched against pre-built UI scaffolds (pricing cards, navbars, etc.) to inject structural skeletons and high-quality few-shot examples into the LLM context.
2. **Coder Model (Qwen)**: A local `qwen2.5-coder` model generates raw HTML/Tailwind code based on the prompt and scaffold.
3. **Post-Processing**: Deterministic Python-esque rules fix common LLM mistakes (unclosed tags, generic colors, missing transitions).
4. **Rendering**: Playwright renders the code in a headless browser, waiting for network-idle to ensure CDNs load.
5. **Custom ML Critic**: A custom-trained Random Forest model extracts DOM features and evaluates the UI structure. If the score is low, it returns deterministic feedback to the Coder Model for a retry.

## 🛠 Tech Stack
* **Frontend**: React 19, Vite, Tailwind CSS v4 (Clean, Premium, Vercel-style UI)
* **Backend**: NestJS, Playwright
* **AI Models**: Ollama (Qwen2.5-coder:1.5b)
* **Custom ML Pipeline**: Python, scikit-learn, BeautifulSoup, Pandas, Joblib (Random Forest Classifier)

## 🚀 Setup Instructions

### 1. Prerequisites
* Node.js (v20+)
* Ollama installed locally with the coder model: `ollama pull qwen2.5-coder:1.5b`
* Python 3.10+

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Backend Setup
```bash
cd backend
npm install
npx playwright install
npm run start:dev
```

### 4. Train the Custom ML Critic Model
```bash
cd backend/ml
python -m venv venv

# Activate the venv (Windows)
.\venv\Scripts\activate
# Activate the venv (Mac/Linux)
# source venv/bin/activate

pip install -r requirements.txt
python train.py
```
