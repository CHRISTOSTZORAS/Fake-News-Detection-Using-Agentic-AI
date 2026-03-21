import pandas as pd
from pathlib import Path

input_path = r"C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\data\\gossipcop.csv"
output_path = r"C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\data\\test2.xlsx"

df = pd.read_csv(input_path, encoding="latin1")

df = df.dropna(subset=["text", "label"]).copy()

sample_df = df.sample(n=5, random_state=42)

Path(output_path).parent.mkdir(parents=True, exist_ok=True)
sample_df.to_excel(output_path, index=False)

print(f"Saved {len(sample_df)} rows to {output_path}")