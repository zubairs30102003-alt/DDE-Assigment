"""
Bremen Company Analysis
- Merge BREMEN.xlsx + agent data
- Clean & normalize fields
- Filter >10 employees
- Logistic regression: what predicts scaling?
- Export merged dataset for chatbot
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────

bremen = pd.read_excel('BREMEN.xlsx')
bremen.columns = bremen.columns.str.replace('\n', ' ')
bremen.replace('n.a.', np.nan, inplace=True)

agent = pd.read_csv(
    '/Users/zubair_s/Downloads/df_agent_progress final(Sheet1).csv',
    encoding='latin-1', sep=';', engine='python', on_bad_lines='skip'
)

print(f"BREMEN: {bremen.shape} | Agent: {agent.shape}")

# ── 2. CLEAN AGENT DATA ────────────────────────────────────────────────────────

# Normalize B2B_or_B2C
def clean_b2b(val):
    if pd.isna(val): return 'Not found'
    val = str(val).strip().lower()
    if val.startswith('b2b') or val == 'business': return 'B2B'
    if val.startswith('b2c'): return 'B2C'
    if 'both' in val or ('b2b' in val and 'b2c' in val): return 'Both'
    return 'Not found'

agent['B2B_or_B2C_clean'] = agent['B2B_or_B2C'].apply(clean_b2b)

# Normalize Legal_Form → broad categories
def clean_legal(val):
    if pd.isna(val): return 'Other'
    val = str(val).strip()
    if 'GmbH & Co' in val or 'GmbH& Co' in val: return 'GmbH & Co. KG'
    if 'GmbH' in val or 'mbH' in val or 'beschränkter' in val: return 'GmbH'
    if val in ['AG', 'Aktiengesellschaft']: return 'AG'
    if 'KG' in val: return 'KG'
    if 'e.V.' in val or 'eV' in val: return 'e.V.'
    if 'e.G.' in val or 'eG' in val or 'Genossenschaft' in val: return 'e.G.'
    if val == 'Not found': return 'Other'
    return 'Other'

agent['Legal_Form_clean'] = agent['Legal_Form'].apply(clean_legal)

print("\nB2B_or_B2C cleaned:")
print(agent['B2B_or_B2C_clean'].value_counts())
print("\nLegal_Form cleaned:")
print(agent['Legal_Form_clean'].value_counts())

# ── 3. MERGE ───────────────────────────────────────────────────────────────────

agent_slim = agent[[
    'company_name', 'Legal_Form_clean', 'B2B_or_B2C_clean',
    'Industry', 'Company_Description', 'Key_Activities_Product_Offerings'
]].copy()
agent_slim.columns = [
    'Company name Latin alphabet', 'Legal_Form', 'B2B_or_B2C',
    'Industry', 'Company_Description', 'Key_Activities'
]

df = bremen.merge(agent_slim, on='Company name Latin alphabet', how='left')
print(f"\nMerged dataset: {df.shape}")

# ── 4. FILTER: > 10 EMPLOYEES ─────────────────────────────────────────────────

emp_cols = [c for c in df.columns if 'Number of employees' in c]
for col in emp_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['max_employees'] = df[emp_cols].max(axis=1)
df_filtered = df[df['max_employees'] > 10].copy()
print(f"After >10 employees filter: {df_filtered.shape}")

# ── 5. FEATURE ENGINEERING ────────────────────────────────────────────────────

# Company age
current_year = 2024
df_filtered['Founded_Year'] = pd.to_numeric(
    df_filtered['Founded Year'], errors='coerce'
)
df_filtered['Company_Age'] = current_year - df_filtered['Founded_Year']

# Employee growth (2019 → 2024)
df_filtered['emp_2019'] = pd.to_numeric(df_filtered['Number of employees 2019'], errors='coerce')
df_filtered['emp_2024'] = pd.to_numeric(df_filtered['Number of employees 2024'], errors='coerce')
df_filtered['Emp_Growth'] = (
    (df_filtered['emp_2024'] - df_filtered['emp_2019']) / df_filtered['emp_2019']
).replace([np.inf, -np.inf], np.nan)

# NACE broad sector
df_filtered['NACE_Section'] = df_filtered['NACE Rev. 2 main section'].str.extract(r'^([A-Z])')

# Target variables
df_filtered['Scaler_2024'] = pd.to_numeric(df_filtered['Scaler 2024'], errors='coerce').fillna(0).astype(int)
df_filtered['Gazelle_2024'] = pd.to_numeric(df_filtered['Gazelle 2024'], errors='coerce').fillna(0).astype(int)

print(f"\nScaler rate: {df_filtered['Scaler_2024'].mean():.1%}")
print(f"Gazelle rate: {df_filtered['Gazelle_2024'].mean():.1%}")

# ── 6. STATISTICAL ANALYSIS ───────────────────────────────────────────────────

print("\n" + "="*60)
print("LOGISTIC REGRESSION: Predictors of Scaling (Scaler 2024)")
print("="*60)

# Encode categorical vars
features = ['Legal_Form', 'B2B_or_B2C', 'NACE_Section', 'Company_Age']
target = 'Scaler_2024'

ml_df = df_filtered[features + [target]].dropna()

# One-hot encode categoricals
ml_encoded = pd.get_dummies(ml_df[['Legal_Form', 'B2B_or_B2C', 'NACE_Section']], drop_first=True)
ml_encoded['Company_Age'] = ml_df['Company_Age'].values

X = ml_encoded
y = ml_df[target].values

print(f"Training on {len(X)} companies")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
coef_df = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_[0]
}).sort_values('Coefficient', ascending=False)

print("\nTop positive predictors (more likely to scale):")
print(coef_df.head(8).to_string(index=False))
print("\nTop negative predictors (less likely to scale):")
print(coef_df.tail(5).to_string(index=False))

# ── 7. DESCRIPTIVE STATS ──────────────────────────────────────────────────────

print("\n" + "="*60)
print("DESCRIPTIVE: Scaler rate by Legal Form")
print("="*60)
legal_scaler = df_filtered.groupby('Legal_Form')['Scaler_2024'].agg(['mean','count'])
legal_scaler.columns = ['Scale_Rate', 'Count']
legal_scaler = legal_scaler[legal_scaler['Count'] >= 10].sort_values('Scale_Rate', ascending=False)
print(legal_scaler.round(3))

print("\n" + "="*60)
print("DESCRIPTIVE: Scaler rate by B2B/B2C")
print("="*60)
b2b_scaler = df_filtered.groupby('B2B_or_B2C')['Scaler_2024'].agg(['mean','count'])
b2b_scaler.columns = ['Scale_Rate', 'Count']
print(b2b_scaler.round(3))

print("\n" + "="*60)
print("DESCRIPTIVE: Scaler rate by NACE Section")
print("="*60)
nace_scaler = df_filtered.groupby('NACE_Section')['Scaler_2024'].agg(['mean','count'])
nace_scaler.columns = ['Scale_Rate', 'Count']
nace_scaler = nace_scaler[nace_scaler['Count'] >= 5].sort_values('Scale_Rate', ascending=False)
print(nace_scaler.round(3))

# ── 8. SAVE MERGED DATASET ────────────────────────────────────────────────────

output_cols = [
    'Company name Latin alphabet', 'NACE Rev. 2 main section', 'NACE_Section',
    'Founded_Year', 'Company_Age', 'Status',
    'Number of employees 2024', 'Number of employees 2023',
    'Number of employees 2022', 'Number of employees 2021',
    'Number of employees 2020', 'Number of employees 2019',
    'Emp_Growth', 'max_employees',
    'Scaler 2024', 'Scaler 2023', 'Gazelle 2024', 'Gazelle 2023',
    'HighGrowthFirm 2024', 'aagr 2024',
    'Legal_Form', 'B2B_or_B2C', 'Industry',
    'Company_Description', 'Key_Activities',
    'Scaler_2024', 'Gazelle_2024'
]
output_cols = [c for c in output_cols if c in df_filtered.columns]

df_final = df_filtered[output_cols].copy()
df_final.to_csv('bremen_merged_final.csv', index=False)
df_final.to_excel('bremen_merged_final.xlsx', index=False)
print(f"\n✅ Saved bremen_merged_final.csv & .xlsx ({df_final.shape})")
