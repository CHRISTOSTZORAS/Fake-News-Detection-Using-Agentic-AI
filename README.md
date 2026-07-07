# 🎓 Fake News Detection Using Agentic AI

**Author:** Christos Tzoras  
**Degree:** MSc in Applied Statistics (specialization in Data Science) — University of Piraeus  
**Year:** 2025

> This project implements an explainable fake-news detection system built with Flowise, large language models, and a multi-agent workflow. The goal is not only to classify a claim as real, fake, or suspicious, but also to show the reasoning path, evidence sources, and supporting signals behind the decision.

## 🧭 Project Overview

This repository contains:
- A Flowise-based multi-agent workflow exported as a pipeline file
- A set of experiment scripts for evaluation and batch processing
- Documentation, backup scripts, and supporting assets for running the system

The system is designed around transparency and traceability. Each agent produces structured outputs such as a verdict, confidence, evidence URLs, and quality/score signals, and a supervisor agent combines these into the final decision.

## 🧱 System Architecture

The workflow is built as a set of cooperating agents in Flowise:

| Agent | Role |
|---|---|
| Input Agent | Receives the claim, URL, or text input; normalizes the content and prepares it for analysis |
| Research / Classifier Agent | Searches the web for evidence and produces an initial verdict, confidence, and supporting sources |
| Cross-Check Agent | Performs an independent second-pass search for additional evidence and a verification hint |
| Scoring Agent | Evaluates signals such as bias, emotion, credibility, and timeliness |
| Source Quality Agent | Assesses the reliability of the sources and computes an aggregated source-quality score |
| Supervisor Agent | Combines all intermediate signals into a final decision with explanation |

The exported Flowise pipeline is stored in:
- flowise/fake news detector Agents.json

## 🛠️ Tools Used by the Agents

The agents are designed to work with a set of tools commonly configured in Flowise:

- LLM reasoning tools for agent decision-making and explanation generation
- Web search tools such as Tavily and/or Serper for evidence retrieval
- HTTP/URL fetch tools for reading and processing source content
- Text-processing tools for cleaning, translation, and language handling
- Python-based evaluation scripts for batch testing and scoring

In practice, the agents rely on:
- An OpenAI-compatible LLM provider or similar model endpoint
- Search providers for external evidence
- Structured output generation for explainability

## 📂 Repository Structure

| Path | Description |
|---|---|
| flowise/fake news detector Agents.json | Exported Flowise agent workflow |
| docker-compose.yml | Docker Compose file for running Flowise |
| backup_flowise.bat | Windows backup script for the Flowise database |
| requirements.txt | Python dependencies for experiment scripts |
| experiments/scripts | Batch evaluation and helper scripts |
| thesis | Thesis PDF and presentation files |
| assets | Images and supporting assets |

## 🚀 Running the Project

### Prerequisites

You need:
- Docker Desktop (recommended) or a local Node/Flowise installation
- API keys for your LLM provider and any search tool provider you use
- A local environment file with secrets such as .env

### Option 1: Run with Docker (recommended)

The repository already includes a Docker Compose configuration.

1. Make sure Docker Desktop is running.
2. Open a terminal in the project root.
3. Start Flowise:

```bash
docker compose up -d
```

4. Open the Flowise UI in your browser:

```text
http://localhost:3000
```

5. Import the exported workflow from:
- flowise/fake news detector Agents.json

6. Configure the required environment variables in Flowise or in your local .env file.

### Docker Compose Details

The current compose file uses the Flowise Docker image:
- flowiseai/flowise:3.0.1
- Port mapping: 3000:3000
- Persistent volume mapping for Flowise data

This is the simplest way to reproduce the setup on a local machine.

### Option 2: Run Flowise locally

If you prefer a non-Docker setup:
1. Install Flowise following the official documentation.
2. Start the Flowise server.
3. Import the exported pipeline JSON.
4. Configure the environment variables for the agents.

## 🔐 Environment Variables

Set the following values before running the workflow:

- OPENAI_API_KEY or the key for your chosen LLM provider
- Search provider keys such as Tavily or Serper
- Any extra credentials required by the tools you attach to the agents

Keep secrets local and do not commit them to the repository. A local .env file is the recommended approach.

## ▶️ How to Use the Workflow

Once Flowise is running:
1. Open the imported agent flow.
2. Paste a claim, headline, or article URL into the input node.
3. Run the workflow.
4. Inspect the outputs from the supervisor node:
   - Final verdict
   - Confidence score
   - Evidence URLs
   - Bias, emotion, credibility, and timeliness signals
   - Source quality assessment

## 🧪 Batch Experiments

The repository also includes Python scripts for reproducible experiments.

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the experiment script

```bash
python experiments/scripts/run_experiments.py --input <dataset.csv> --output <results.csv>
```

The experiment scripts are intended to:
- Load datasets
- Run the workflow or evaluate predictions in batches
- Produce metrics such as accuracy and macro F1
- Save structured explanations and outputs

## 💾 Backup and Restore

### Backup Flowise data

The repository includes a Windows backup helper:
- backup_flowise.bat

This script creates a timestamped copy of the Flowise SQLite database into a backups folder under the Flowise data directory.

### Recommended backup practice

Keep backups of:
- The Flowise database file
- The Flowise data directory
- The exported pipeline JSON file
- Your .env file
- Any result CSV files generated during experiments

### Restore

To restore a backup:
1. Stop Flowise.
2. Replace the current Flowise database with the backup copy.
3. Restart Flowise.
4. Re-import the pipeline if needed.

### Running the backup script

To manually create a backup of the Flowise database:

```powershell
.\backup_flowise.bat
```

The script creates a timestamped SQLite backup under:

```text
C:\Users\tzwrakos\.flowise\backups
```

It is recommended to run the backup script before:
- Updating Flowise
- Changing Flowise versions
- Modifying the database
- Making major changes to the agent workflow

## Example

```bash
python experiments/scripts/run_experiments.py ^
    --input datasets/gossipcop_sample.xlsx ^
    --output experiments/results/results_gossipcop.xlsx
```

The script:

1. Loads a dataset containing at least the columns:
   - `text`
   - `label`
2. Sends each claim to the deployed Flowise workflow through its REST API.
3. Parses the structured response.
4. Stores:
   - Final prediction
   - Confidence level
   - Intermediate agent outputs
   - Source information
   - Raw JSON response
5. Computes evaluation metrics:
   - Accuracy
   - Macro F1-score
   - Classification Report
6. Exports all results to Excel or CSV.

## Python Experiment Configuration

The experiment scripts read the Flowise API endpoint from the local `.env` file.

Example:

```env
FLOWISE_URL=http://localhost:3000/api/v1/prediction/1f705796-571c-400c-9e93-f835e4e44c3f
```

This allows changing the deployed Flowise workflow without modifying the Python source code.

## 📊 Output and Evaluation

The workflow produces both prediction outputs and explainability artifacts such as:
- Verdict
- Confidence
- Evidence links
- Bias/emotion/credibility/timeliness scores
- Source quality summaries
- Structured logs for analysis

This makes the system suitable for both qualitative inspection and quantitative evaluation.

## 📌 Notes

- The project is experimental and intended for research, prototyping, and academic demonstration.
- The focus is on explainability, modularity, and traceable reasoning rather than only raw classification accuracy.
- The Flowise pipeline is the central artifact for the workflow definition.

## 🔮 Future Work

Possible next steps include:
- Improving the integration with search providers
- Expanding evaluation on larger datasets such as LIAR or FakeNewsNet
- Enhancing supervisor logic and structured JSON output
- Adding experiment tracking and better reproducibility
