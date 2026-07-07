import pandas as pd

# Read your Excel file
df = pd.read_excel("C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\data\\politifact.xlsx")

# Map 6 labels into 2 labels
label_map = {
    "true": "true",
    "false": "false",
    "mostly-true": "true",
    "half-true": "true",
    "mostly-false": "false",
    "pants-fire": "false"
}

# Clean labels first, then map them
df["label"] = (
    df["label"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map(label_map)
)

# Save the new Excel file
df.to_excel("C:\\Users\\tzwrakos\\Υπολογιστής\\Projects\\Fake-News-Detection-Using-Agentic-AI\\experiments\\data\\politifact_mapped.xlsx", index=False)