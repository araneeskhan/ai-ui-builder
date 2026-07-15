# UI Architect: Multi-Agent Local UI Generator

A Master's level AI portfolio project that autonomously generates and iteratively refines pixel-perfect React/Tailwind UI components without relying on external APIs. 

Built entirely locally using **Ollama**, **NestJS**, **React**, **Playwright**, and a highly advanced **Custom Machine Learning Ensemble Pipeline**.

## 🧠 Architecture

The system operates on an iterative agentic loop:
1. **Scaffold Injection**: The user prompt is matched against pre-built UI scaffolds (pricing cards, navbars, etc.) to inject structural skeletons and high-quality few-shot examples into the LLM context.
2. **Coder Model (Qwen)**: A local `qwen2.5-coder` model generates raw HTML/Tailwind code based on the prompt and scaffold.
3. **Post-Processing**: Deterministic rules fix common LLM mistakes (unclosed tags, generic colors, missing transitions).
4. **Rendering**: Playwright renders the code in a headless browser, waiting for network-idle to ensure CDNs load.
5. **Master Ensemble Critic**: The generated HTML is evaluated by a custom-trained ML pipeline. If the score is low, it returns deterministic, mathematically-backed feedback to the Coder Model for a retry.

## 🔬 The ML Pipeline (High-Level Ensemble Architecture)

This project features a ~1,400-line, production-grade custom Machine Learning backend:
* **Procedural Data Engineering**: Automatically synthesizes 3,000 unique HTML components across 20 distinct UI patterns (Good and Bad) for training data.
* **Heterogeneous Feature Extraction**: Parses the DOM tree to calculate 30 numerical structural metrics (e.g., Semantic Ratio, Layout Cohesion, Tailwind Density) AND extracts an NLP corpus of CSS classes.
* **The Ensemble Model**: Uses a `ColumnTransformer` to route numeric data through a `StandardScaler` and text data through a `TfidfVectorizer`. The unified data is then fed into a **Soft Voting Classifier** that fuses the intelligence of:
  * **Random Forest** (Structural analysis)
  * **Logistic Regression** (Semantic NLP analysis of Tailwind patterns)
  * **Gradient Boosting** (Robustness against edge cases)
* **Evaluation Suite**: Automatically generates Confusion Matrices, ROC Curves, and Feature Importance charts using `matplotlib` and `seaborn`.

## 🛠 Tech Stack
* **Frontend**: React 19, Vite, Tailwind CSS v4 (Clean, Premium UI)
* **Backend**: NestJS, Node.js, Playwright
* **AI Models**: Ollama (Qwen2.5-coder:1.5b)
* **Custom ML Engineering**: Python 3, scikit-learn, BeautifulSoup, pandas, numpy, seaborn, matplotlib

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

### 4. Train the Custom Ensemble ML Critic
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
*Note: Training will generate the models, datasets, and evaluation charts dynamically.*
