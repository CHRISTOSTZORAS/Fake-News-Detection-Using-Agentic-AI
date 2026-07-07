import pandas as pd 

#1. Put your file paths here
file1="C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\results\\Sample_942_results_gossipcop.xlsx"
file2="C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\results\\Sample_1200_results_gossipcop.csv"

#2. Put where you want to save the merged Excel
output_file="C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\results\\Full_Sample_results.xlsx"

# 3. Read the two Excel files
df1 = pd.read_excel(file1)
df2 = pd.read_csv(file2)

# 4. Keep only the columns we need
df1 = df1[["text", "label", "prediction"]]
df2 = df2[["text", "label", "prediction"]]

# 5. Change prediction SUSPICIOUS to FAKE
df1["prediction"] = df1["prediction"].astype(str).str.strip().str.upper()
df2["prediction"] = df2["prediction"].astype(str).str.strip().str.upper()

df1["prediction"] = df1["prediction"].replace("SUSPICIOUS", "FAKE")
df2["prediction"] = df2["prediction"].replace("SUSPICIOUS", "FAKE")

# Delete rows where prediction is not FAKE or REAL
df1 = df1[df1["prediction"].isin(["FAKE", "REAL"])]
df2 = df2[df2["prediction"].isin(["FAKE", "REAL"])]

# Merge the two files
merged_df = pd.concat([df1, df2], ignore_index=True)

# Keep only unique text rows
merged_df = merged_df.drop_duplicates(subset=["text"], keep="first")

# Save final Excel
merged_df.to_excel(output_file, index=False)

print("File 1 rows after cleaning:", len(df1))
print("File 2 rows after cleaning:", len(df2))
print("Merged unique rows:", len(merged_df))

print("\nLabel counts:")
print(merged_df["label"].value_counts(dropna=False))

print("\nPrediction counts:")
print(merged_df["prediction"].value_counts(dropna=False))

print("\nSaved merged file to:")
print(output_file)