import pandas as pd

# Paths
gossipcop_file = r"C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\data\\gossipcop.csv"

existing_excel = r"C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\results\\Sample_942_results_gossipcop.xlsx"

output_file = r"C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\data\\gossipcop_new_1200_sample.xlsx"

# Read files
gossipcop_df = pd.read_csv(gossipcop_file, encoding="latin1")
existing_df = pd.read_excel(existing_excel)

# Keep only rows where text is not empty
gossipcop_df = gossipcop_df.dropna(subset=["text"])
existing_df = existing_df.dropna(subset=["text"])

# Clean text for safer comparison
gossipcop_df["text_clean"] = gossipcop_df["text"].astype(str).str.strip()
existing_df["text_clean"] = existing_df["text"].astype(str).str.strip()

# Remove from gossipcop rows that already exist in Sample 942
new_rows = gossipcop_df[~gossipcop_df["text_clean"].isin(existing_df["text_clean"])]

# Remove duplicate texts inside the new sample source
new_rows = new_rows.drop_duplicates(subset=["text_clean"], keep="first")

# Keep only REAL and FAKE labels
new_rows = new_rows[new_rows["label"].isin(["REAL", "FAKE"])]

# Split by label
real_rows = new_rows[new_rows["label"] == "REAL"]
fake_rows = new_rows[new_rows["label"] == "FAKE"]

print("Available REAL rows:", len(real_rows))
print("Available FAKE rows:", len(fake_rows))

# Take 600 REAL and 600 FAKE
real_sample = real_rows.sample(n=600, random_state=42)
fake_sample = fake_rows.sample(n=600, random_state=42)

# Merge balanced sample
sample_1200 = pd.concat([real_sample, fake_sample], ignore_index=True)

# Shuffle final dataset
sample_1200 = sample_1200.sample(frac=1, random_state=42).reset_index(drop=True)

# Remove helper column
sample_1200 = sample_1200.drop(columns=["text_clean"])

# Save
sample_1200.to_excel(output_file, index=False)

print("Final rows saved:", len(sample_1200))
print("\nFinal label counts:")
print(sample_1200["label"].value_counts())

print("\nSaved to:")
print(output_file)