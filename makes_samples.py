import pandas as pd
from pathlib import Path

# 📂 Paths
sample_path = r"C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\data\\test1.xlsx"
results_path = r"C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\results\\test1_results.csv"

output_dir = r"C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\data"

# 📥 Load
sample_df = pd.read_excel(sample_path)
results_df = pd.read_csv(results_path)

# 🔥 Ensure matching type
sample_df["text"] = sample_df["text"].astype(str)
results_df["text"] = results_df["text"].astype(str)

# ✅ 1. Sample_367 (successful)
sample_367 = results_df[
    (results_df["status"] == "OK") &
    (results_df["prediction"].isin(["REAL", "FAKE", "SUSPICIOUS"]))
].copy()
sample_367_results = sample_367.copy()
# 🔹 texts που πέτυχαν
successful_texts = set(sample_367["text"])

# ✅ 2. Sample_Rest (failed)
sample_rest = sample_df[
    ~sample_df["text"].isin(successful_texts)
].copy()

# ✅ 3. Sample_200 (next test από failed)
sample_200 = sample_rest.sample(
    n=min(200, len(sample_rest)),
    random_state=42
)

# 📁 Save
Path(output_dir).mkdir(parents=True, exist_ok=True)

sample_367.to_excel(f"{output_dir}\\Sample_367.xlsx", index=False)
sample_rest.to_excel(f"{output_dir}\\Sample_Rest.xlsx", index=False)
sample_200.to_excel(f"{output_dir}\\Sample_200.xlsx", index=False)
sample_367_results.to_excel(f"{output_dir}\\Sample_367_results.xlsx", index=False)
# 📊 Logs
print(f"Sample_367: {len(sample_367)} rows")
print(f"Sample_Rest: {len(sample_rest)} rows")
print(f"Sample_200: {len(sample_200)} rows")
