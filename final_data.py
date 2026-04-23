import pandas as pd
import os

folder = "."

files = {
    "glucose": "GLU_J.csv",
    "cholesterol": "TCHOL_J.csv",
    "hdl": "HDL_J.csv",
    "vitamin_d": "VID_J.csv",
    "hemoglobin": "CBC_J.csv"
}

final_data = []

for key, file in files.items():
    path = os.path.join(folder, file)
    
    if not os.path.exists(path):
        print(f"❌ Missing {file}")
        continue
    
    df = pd.read_csv(path)

    # pick first numeric column (NHANES has many columns)
    value_col = df.select_dtypes(include=['float64', 'int64']).columns[0]

    for _, row in df.head(50).iterrows():  # limit rows
        final_data.append({
            "date": "2026-04-01",
            "type": key,
            "value": row[value_col]
        })

final_df = pd.DataFrame(final_data)

final_df.to_csv("health_data.csv", index=False)

print("✅ Combined CSV created!")