# 🎓 Fake News Detection on Social Media (Flowise + LLMs)

**Author:** Christos Tzoras  
**Degree:** MSc in Applied Statistics (specialization in Data Science) — University of Piraeus  
**Year:** 2025

> A transparent, modular, and explainable fake news detection system built with **Flowise** and  **LLMs** in a **multi-agent** architecture.

## 🧭 Overview

This repository contains:
- **Flowise pipeline JSON** for the end-to-end AI workflow
- **Thesis PDF** and **presentation slides**
- Documentation for setup, import, and experimentation

The system emphasizes **explainability** and **traceability**: each agent contributes a structured signal (verdict, confidence, source quality, bias/emotion/time scores), and a **Supervisor** composes the final decision.

## 📂 Repository Contents

| Path | Description |
|---|---|
| `flowise/flowise_pipeline.json` | Exported Flowise pipeline (import into Flowise) |
| `thesis/Tzoras_23006.pdf` | Full MSc thesis (PDF) |
| `thesis/Thesis Presentation.pptx` | Slide deck (optional) |
| `assets/architecture.png` | System/graph diagram (optional) |

## 🧱 System Architecture (Flowise, multi-agent)

**Key agents (high-level):**
- **Input Agent** — normalizes incoming input (URL/text/file), language detection/translation, cleaning.
- **Fake News Classifier** — searches the web for evidence; outputs `verdict` (REAL/FAKE/SUSPICIOUS), `confidence`, `sources`.
- **Second Search Agent** — independent cross-check (fresh sources); returns `verdict_hint` and supporting URLs.
- **Scoring Agent** — rates **bias**, **emotion**, **credibility**, **time relevance** (0–100 + labels).
- **Source Quality Checker** — scores domain credibility and computes an average source-quality score.
- **Supervisor Agent** — fuses all signals with rule-based logic and produces the **final decision** with explanation.

> Import the JSON and you’ll see the exact nodes/edges in Flowise.

## 🚀 Getting Started

### 1) Install Flowise
- Follow the official docs to run Flowise locally (Docker or Node).  
- Start the UI (usually at `http://localhost:3000`).

### 2) Import the pipeline
1. Open Flowise → **Import**  
2. Select `flowise/flowise_pipeline.json`  
3. Confirm nodes and environment variables

### 3) Configure environment variables (examples)
- `OPENAI_API_KEY` (or provider of choice)
- Search provider keys (e.g., Tavily / Serper)
- Any additional API keys used by your tools

> Keep secrets out of the repo. Use a local `.env` (not committed).

### 4) Run
- In Flowise UI, paste a claim/headline (or URL)  
- Trigger the flow and inspect the **Supervisor** output:
  - Final **verdict** + **confidence**
  - **Evidence** with URLs
  - **Bias/Emotion/Credibility/Time** scores
  - **Source quality** assessment

## 🧠 Methods & Design Highlights

- **Multi-Agent** decomposition for transparency and modularity  
- **Explainability** via structured JSON outputs from each agent  
- **Statistical/NLP signals** (bias, emotion, credibility, timeliness) augment verdicts

## 📊 Datasets & Evaluation (high-level)

The prototype was manually tested on a set of claims (titles and full texts) from well-known fake-news datasets to validate **accuracy** and **explainability**. The focus is on **traceable reasoning** (evidence links, confidence, semantic alignment) rather than opaque black-box classification.

## 🔧 Tech Stack

- **Flowise**, **OpenAI** ,**Serper API**, **Tavily** 

## 📥 How to Reproduce (Quick Checklist)

- [ ] Clone the repo  
- [ ] Install & run Flowise  
- [ ] Import `flowise/flowise_pipeline.json`  
- [ ] Add API keys in Flowise (env)  
- [ ] Run the flow with sample claims  
- [ ] Inspect final verdict + intermediate agent outputs  

## 🔄 Recent Updates

- Replaced Google Custom Search with Tavily API  
- Added batch experimentation pipeline  
- Enabled automated evaluation on datasets  
- Stored full reasoning traces and structured outputs  

---

## 🧪 Batch Experiments

Install dependencies:

pip install requests pandas tqdm scikit-learn python-dotenv

Run:

python experiments/scripts/run_experiments.py --input dataset.csv --output results.csv

---

## 📊 Output

- Accuracy  
- Macro F1  
- Classification report  
- Full explainability logs  

---

## 🔮 Next Steps

- Fix Tavily integration  
- Use real datasets (LIAR, FakeNewsNet)  
- Convert Supervisor output to JSON  
- Run large-scale experiments  
- Add experiment tracking  

---

## 🧠 Contribution

Explainable multi-agent fake news detection with reproducible evaluation.
