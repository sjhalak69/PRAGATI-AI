import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def get_audited_data():
    # 1. Generate Synthetic MPLAD Dataset
    np.random.seed(42)
    n_projects = 100

    project_ids = [f"MPLAD-{i:03d}" for i in range(1, n_projects + 1)]
    asset_types = np.random.choice(["Community Hall", "Drinking Water Plant", "Rural Road", "Public Library"], n_projects)
    
    # Generate baseline costs
    sanctioned_amount = np.random.randint(500000, 2000000, n_projects)
    for i in range(n_projects):
        if asset_types[i] == "Rural Road":
            sanctioned_amount[i] += 1500000

    # Normal variations
    spent_amount = sanctioned_amount * np.random.uniform(0.9, 1.05, n_projects)
    days_delayed = np.random.randint(0, 90, n_projects)

    # --- INJECTING FRAUD & INEFFICIENCY TRAPS ---
    # Project 12: Cost Inflation Fraud (4.5x over budget)
    spent_amount[11] = sanctioned_amount[11] * 4.5 
    # Project 45: Extreme Stagnation Inefficiency
    days_delayed[44] = 450 

    df = pd.DataFrame({
        "Project_ID": project_ids,
        "Asset_Type": asset_types,
        "Sanctioned_Amount": sanctioned_amount,
        "Spent_Amount": spent_amount.astype(int),
        "Days_Delayed": days_delayed
    })

    # 2. Train AI Engine (Isolation Forest)
    features = df[["Sanctioned_Amount", "Spent_Amount", "Days_Delayed"]]
    ai_model = IsolationForest(contamination=0.03, random_state=42)
    df['Anomaly_Status'] = ai_model.fit_predict(features)
    
    # Status flags
    df['Status'] = df['Anomaly_Status'].apply(lambda x: '🚨 RED FLAG' if x == -1 else '✅ NORMAL')
    return df

if __name__ == "__main__":
    df = get_audited_data()
    print("\n=== AI AUDITING SYSTEM ACTIVE ===")
    print(df[df['Status'] == '🚨 RED FLAG'][["Project_ID", "Asset_Type", "Sanctioned_Amount", "Spent_Amount", "Days_Delayed", "Status"]])
