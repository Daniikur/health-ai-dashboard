import pandas as pd

# ========================
# STEP 1 — Load data
# ========================
df = pd.read_csv("health_data.csv")

df["test_id"] = df["test_name"].astype("category").cat.codes
df["is_abnormal"] = df["flag"].apply(lambda x: 1 if x != "N" else 0)
df["time"] = pd.factorize(df["date"])[0]

print("✅ Data prepared")
print(df.head())


# ========================
# STEP 2 — Classification
# ========================
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X = df[["value", "test_id"]]
y = df["is_abnormal"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)

print("\n🧠 Model Accuracy:", clf.score(X_test, y_test))


# ========================
# STEP 3 — Prediction
# ========================
from sklearn.linear_model import LinearRegression

print("\n🔮 Future predictions:")

for test in df["test_name"].unique():
    sub = df[df["test_name"] == test]

    if len(sub) < 2:
        continue

    X = sub[["time"]]
    y = sub["value"]

    model = LinearRegression()
    model.fit(X, y)

    next_time = [[sub["time"].max() + 1]]
    future_val = model.predict(next_time)[0]

    print(test, "→", round(future_val, 2))


# ========================
# STEP 4 — Risk Score
# ========================
def risk_score(row):
    if row["flag"] == "H":
        return 2
    elif row["flag"] == "L":
        return 1
    return 0

df["risk"] = df.apply(risk_score, axis=1)

total_risk = df["risk"].sum()

print("\n⚠️ Health Risk Score:", total_risk)