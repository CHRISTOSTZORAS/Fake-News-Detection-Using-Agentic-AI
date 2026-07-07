import argparse
import json
import re
import time
from pathlib import Path

import pandas as pd
import requests
from sklearn.metrics import accuracy_score, f1_score, classification_report
from tqdm import tqdm

FLOWISE_URL = "http://localhost:3000/api/v1/prediction/1f705796-571c-400c-9e93-f835e4e44c3f"
SLEEP_BETWEEN_CALLS = 0.5
MAX_RETRIES = 3
TIMEOUT = 120

def load_input_file(input_file: str) -> pd.DataFrame:
    input_path = Path(input_file)

    if input_path.suffix.lower() == ".csv":
        return pd.read_csv(input_file)
    elif input_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(input_file)
    else:
        raise ValueError("Supported input formats: .csv, .xlsx, .xls")
    
def extract_final_decision(text: str) -> str:
    if not isinstance(text, str):
        return "ERROR"

    match = re.search(r"FINAL DECISION:\s*(REAL|FAKE|SUSPICIOUS)", text, re.IGNORECASE)
    if match:
        return match.group(1).upper()

    return "ERROR"


def extract_confidence_level(text: str) -> str:
    if not isinstance(text, str):
        return ""

    match = re.search(r"CONFIDENCE LEVEL:\s*(High|Medium|Low)", text, re.IGNORECASE)
    if match:
        return match.group(1).capitalize()

    return ""


def extract_all_fields(text: str) -> dict:
    if not isinstance(text, str):
        return {
            "verdict": "",
            "confidence_percent": "",
            "sources_primary": "",
            "reasoning": "",
            "bias_score": "",
            "bias_label": "",
            "emotion_score": "",
            "emotion_label": "",
            "credibility_score": "",
            "credibility_label": "",
            "time_score": "",
            "time_label": "",
            "scoring_reasoning": "",
            "timestamp": "",
            "secondary_verdict": "",
            "search_summary": "",
            "sources_secondary": "",
            "source_score": "",
            "source_quality": "",
            "source_notes": "",
            "final_decision": "",
            "final_confidence_level": "",
            "final_explanation": "",
        }

    def find(pattern, default=""):
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else default

    return {
        "verdict": find(r"Verdict:\s*(REAL|FAKE|SUSPICIOUS)"),
        "confidence_percent": find(r"Confidence:\s*(\d+)%"),
        "sources_primary": find(r"Sources:\s*(.*?)\n\nReasoning:"),
        "reasoning": find(r"Reasoning:\s*(.*?)\n\n📊"),
        "bias_score": find(r"Bias Score:\s*(\d+)/100"),
        "bias_label": find(r"Bias Score:\s*\d+/100\s*—\s*([A-Z]+)"),
        "emotion_score": find(r"Emotion Score:\s*(\d+)/100"),
        "emotion_label": find(r"Emotion Score:\s*\d+/100\s*—\s*([A-Z]+)"),
        "credibility_score": find(r"Credibility Score:\s*(\d+)/100"),
        "credibility_label": find(r"Credibility Score:\s*\d+/100\s*—\s*([A-Z]+)"),
        "time_score": find(r"Time Relevance Score:\s*(\d+)/100"),
        "time_label": find(r"Time Relevance Score:\s*\d+/100\s*—\s*([A-Z]+)"),
        "scoring_reasoning": find(r"📋 Scoring Reasoning:\s*(.*?)\n\n🕒"),
        "timestamp": find(r"🕒 Timestamp of Evaluation:\s*(.*?)\n\n🌐"),
        "secondary_verdict": find(r"Secondary Verdict Hint:\s*([A-Z_]+)"),
        "search_summary": find(r"Search Summary:\s*(.*?)\n\nSources:"),
        "sources_secondary": find(r"🌐 Secondary Web Search Summary:.*?Sources:\s*(.*?)\n\n📎", ""),
        "source_score": find(r"Average Source Score:\s*(\d+)/100"),
        "source_quality": find(r"Average Source Score:\s*\d+/100\s*—\s*([A-Za-z]+)"),
        "source_notes": find(r"Notes:\s*(.*?)\n\n📢"),
        "final_decision": find(r"FINAL DECISION:\s*(REAL|FAKE)"),
        "final_confidence_level": find(r"CONFIDENCE LEVEL:\s*(High|Medium|Low)"),
        "final_explanation": find(r'EXPLANATION:\s*"(.*?)"\s*\\?===================='),
    }



def query_flowise(claim_text: str) -> dict:
    payload = {"question": claim_text}

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(FLOWISE_URL, json=payload, timeout=TIMEOUT)
            response.raise_for_status()
            result = response.json()

            raw_text = result.get("text", "")
            parsed = extract_all_fields(raw_text)

            return {
                "prediction": extract_final_decision(raw_text),
                "confidence_level": extract_confidence_level(raw_text),
                "raw_text": raw_text,
                "raw_json": json.dumps(result, ensure_ascii=False),
                "status": "OK",
                "parsed": parsed,
            }

        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                return {
                    "prediction": "ERROR",
                    "confidence_level": "",
                    "raw_text": "",
                    "raw_json": "",
                    "status": f"ERROR: {e}",
                    "parsed": {
                        "verdict": "",
                        "confidence_percent": "",
                        "sources_primary": "",
                        "reasoning": "",
                        "bias_score": "",
                        "bias_label": "",
                        "emotion_score": "",
                        "emotion_label": "",
                        "credibility_score": "",
                        "credibility_label": "",
                        "time_score": "",
                        "time_label": "",
                        "scoring_reasoning": "",
                        "timestamp": "",
                        "secondary_verdict": "",
                        "search_summary": "",
                        "sources_secondary": "",
                        "source_score": "",
                        "source_quality": "",
                        "source_notes": "",
                        "final_decision": "",
                        "final_confidence_level": "",
                        "final_explanation": "",
                    },
                }
            time.sleep(2)


def run_experiment(input_file: str, output_file: str):
    df = load_input_file(input_file)

    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("Input file must contain columns: text,label")

    predictions = []
    confidence_levels = []
    raw_texts = []
    raw_jsons = []
    statuses = []

    parsed_columns = {
        "verdict": [],
        "confidence_percent": [],
        "sources_primary": [],
        "reasoning": [],
        "bias_score": [],
        "bias_label": [],
        "emotion_score": [],
        "emotion_label": [],
        "credibility_score": [],
        "credibility_label": [],
        "time_score": [],
        "time_label": [],
        "scoring_reasoning": [],
        "timestamp": [],
        "secondary_verdict": [],
        "search_summary": [],
        "sources_secondary": [],
        "source_score": [],
        "source_quality": [],
        "source_notes": [],
        "final_decision": [],
        "final_confidence_level": [],
        "final_explanation": [],
    }

    for text in tqdm(df["text"].astype(str).tolist(), desc="Running claims"):
        result = query_flowise(text)

        predictions.append(result["prediction"])
        confidence_levels.append(result["confidence_level"])
        raw_texts.append(result["raw_text"])
        raw_jsons.append(result["raw_json"])
        statuses.append(result["status"])

        for key in parsed_columns:
            parsed_columns[key].append(result["parsed"].get(key, ""))

        time.sleep(SLEEP_BETWEEN_CALLS)

    df["prediction"] = predictions
    df["confidence_level"] = confidence_levels
    df["status"] = statuses
    df["raw_text"] = raw_texts
    df["raw_json"] = raw_jsons

    for key, values in parsed_columns.items():
        df[key] = values

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix.lower() == ".csv":
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
    elif output_path.suffix.lower() in [".xlsx", ".xls"]:
        df.to_excel(output_file, index=False)
    else:
        raise ValueError("Supported output formats: .csv, .xlsx, .xls")

    valid_df = df[df["prediction"].isin(["REAL", "FAKE"])].copy()

    print("\n===== RESULTS =====")
    print(f"Total samples: {len(df)}")
    print(f"Valid predictions: {len(valid_df)}")
    print(f"Errors: {len(df) - len(valid_df)}")

    if len(valid_df) == 0:
        print("No valid predictions found.")
        return

    acc = accuracy_score(valid_df["label"], valid_df["prediction"])
    f1 = f1_score(valid_df["label"], valid_df["prediction"], average="macro")

    print(f"Accuracy: {acc:.4f}")
    print(f"Macro F1: {f1:.4f}")
    print("\nClassification Report:\n")
    print(classification_report(valid_df["label"], valid_df["prediction"], digits=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input file (.csv or .xlsx) with columns text,label")
    parser.add_argument("--output", default="experiments/results/results.csv", help="Path to output file (.csv or .xlsx)")

    args = parser.parse_args()
    run_experiment(args.input, args.output)
