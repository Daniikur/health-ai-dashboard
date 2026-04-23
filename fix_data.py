import pandas as pd
import os

# configuration
files = {
    "GLU_J.csv": ("Glucose", ["LBDGLUSI", "LBXGLU"], "mmol/L", 3.9, 5.5, "Metabolic Panel"),
    "HDL_J.csv": ("HDL", ["LBDHDDSI", "LBDHDD"], "mmol/L", 1.0, 2.0, "Lipid Panel"),
    "TCHOL_J.csv": ("Cholesterol", ["LBDTCSI", "LBXTC"], "mmol/L", 3.0, 5.2, "Lipid Panel"),
    "VID_J.csv": ("Vitamin D", ["LBXVIDMS"], "nmol/L", 50, 125, "Vitamins & Minerals"),
    "CBC_J.csv": ("Hemoglobin", ["LBXHGB"], "g/dL", 12, 17, "Complete Blood Count"),
}

# realistic max values (for cleaning garbage)
LIMITS = {
    "Glucose": 30,
    "HDL": 5,
    "Cholesterol": 15,
    "Vitamin D": 300,
    "Hemoglobin": 25,
}

def convert_value(name, col, val):
    """Auto unit conversion"""
    if col == "LBXGLU":           # mg/dL → mmol/L
        return val / 18
    elif col in ["LBXTC", "LBDHDD"]:
        return val / 38.67
    elif name == "Vitamin D":
        return val  # already nmol/L
    return val

all_data = []

for file, (name, cols, unit, low, high, category) in files.items():

    if not os.path.exists(file):
        print(f"❌ Missing {file}")
        continue

    print(f"📂 Processing {file}...")

    df = pd.read_csv(file)

    # detect column automatically
    col = next((c for c in cols if c in df.columns), None)

    if col is None:
        print(f"❌ No valid column in {file}")
        continue

    df = df[[col]].dropna()

    for val in df[col]:
        try:
            val = float(val)
        except:
            continue

        # convert units
        val = convert_value(name, col, val)

        # ❗ remove garbage values
        if val <= 0 or val > LIMITS[name]:
            continue

        # flag
        if val < low:
            flag = "L"
        elif val > high:
            flag = "H"
        else:
            flag = "N"

        all_data.append({
            "date": pd.Timestamp.today().strftime("%Y-%m-%d"),
            "test_name": name,
            "value": round(val, 2),
            "unit": unit,
            "reference_low": low,
            "reference_high": high,
            "category": category,
            "flag": flag,
            "source_file": file
        })

# create dataframe
df_final = pd.DataFrame(all_data)

# remove duplicates smartly
df_final = df_final.drop_duplicates(subset=["test_name", "value"])

# sort for charts
df_final = df_final.sort_values(by=["test_name", "value"])

# save
df_final.to_csv("health_data.csv", index=False)

print("✅ CLEAN + SMART dataset created!")
print(f"📊 Rows: {len(df_final)}")