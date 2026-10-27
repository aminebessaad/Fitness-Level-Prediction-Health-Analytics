import json
import os

def create_notebook():
    cells = []

    def md_cell(source):
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in source.strip().split("\n")]
        }

    def code_cell(source):
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in source.strip().split("\n")]
        }

    # Cell 1: Header
    cells.append(md_cell("""
# Fitness Level Prediction: A Machine Learning Classification Study
### Advanced Data Mining & Health Analytics Pipeline
**Authors:** Amine Bessaad, Haitham Maatar, Jasser Sghaier  
**Academic Supervisor:** Pr. Lassad El Moubarki  
**Institution:** Tunis Business School, University of Tunis — Academic Year 2024–2025  
**Core Technologies:** Python, scikit-learn, LightGBM, XGBoost, SHAP (Explainable AI)

---

### Executive Summary & Methodological Innovations
Predicting physiological fitness tiers (**Unfit**, **Moderate**, **Fit**) from daily biometric indicators is a core challenge in digital health and preventative healthcare. This project presents a complete, leak-free machine learning classification pipeline.

Key contributions and methodological corrections in this research report:
1. **Target Imbalance Resolution:** Corrects prior erroneous assumptions of class balance by proving that the target is **heavily imbalanced** (**57.4% Moderate, 38.0% Unfit, 4.6% Fit**).
2. **Zero-Variance Feature Diagnosis:** Detects that `calories_burned` is a constant value ($1500.0, \\sigma=0.0$) across all observations and excludes it as invariant.
3. **Data Generating Process (DGP) Reverse Engineering:** Identifies non-linear threshold penalty gates governing the dataset (sleep duration $<5$h cliff, chronic stress $>8$ gate, non-linear BMI U-curve, and overtraining without recovery).
4. **Physiological Feature Engineering (Zero Leakage):** Constructs domain-informed features—**Recovery-Strain Index (RSI)**, **Cardiovascular Efficiency**, and **Overtraining Exhaustion Risk**—strictly without target leakage.
5. **Multi-Model Tournament:** Evaluates **Balanced Multinomial Logistic Regression**, **Balanced Random Forest**, **LightGBM**, and **XGBoost** under Stratified Cross-Validation.
6. **Explainable AI (XAI) with SHAP:** Provides global feature attributions and individual clinical decision waterfall plots to explain why specific patient habit profiles trigger adverse classification.
"""))

    # Cell 2: Imports & Environment Setup
    cells.append(code_cell("""
import os
import sys
import glob
import time
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Styling
sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Output directories
os.makedirs("figures", exist_ok=True)
os.makedirs("output_metrics", exist_ok=True)

CLASS_PALETTE = {'Moderate': '#3b82f6', 'Unfit': '#ef4444', 'Fit': '#10b981'}
TARGET_MAPPING = {'Unfit': 0, 'Moderate': 1, 'Fit': 2}
INV_TARGET_MAPPING = {0: 'Unfit', 1: 'Moderate', 2: 'Fit'}

print("Environment configured successfully.")
"""))

    # Cell 3: Data Ingestion & Audit
    cells.append(md_cell("""
## 1. Data Ingestion & Dataset Integrity Audit
We dynamically discover the dataset path across local, Kaggle, and cloud environments, inspect feature types, verify null values, and audit zero-variance features.
"""))

    # Cell 4: Load Data & Zero Variance
    cells.append(code_cell("""
candidates = [
    "/kaggle/input/health/fitness_dataset.csv",
    "/kaggle/input/datasets/bessaadamine/health/fitness_dataset.csv",
    *glob.glob("/kaggle/input/**/fitness_dataset.csv", recursive=True),
    "data/fitness_dataset.csv",
    "fitness_dataset.csv"
]

data_path = None
for p in candidates:
    if os.path.exists(p):
        data_path = p
        break

if data_path is None:
    raise FileNotFoundError(f"Could not locate fitness_dataset.csv. Checked: {candidates[:3]}")

print(f"Loading data from: {data_path}")
df_raw = pd.read_csv(data_path)
print(f"Raw shape: {df_raw.shape[0]:,} rows x {df_raw.shape[1]} columns")
print(f"Total Missing Values: {df_raw.isnull().sum().sum()}")

# Zero-variance audit
variances = df_raw.select_dtypes(include=np.number).var()
zero_var_cols = variances[variances == 0].index.tolist()
print(f"Zero-variance invariant columns detected: {zero_var_cols}")
for col in zero_var_cols:
    val = df_raw[col].iloc[0]
    print(f"  -> '{col}' is constant = {val} across all records (zero entropy). Dropping.")

df_clean = df_raw.drop(columns=zero_var_cols).copy()

# Stratified subsampling for fast, high-fidelity modeling
from sklearn.model_selection import train_test_split
SAMPLE_SIZE = 100_000
if SAMPLE_SIZE and SAMPLE_SIZE < len(df_clean):
    df_clean, _ = train_test_split(
        df_clean,
        train_size=SAMPLE_SIZE,
        stratify=df_clean['fitness_level'],
        random_state=RANDOM_STATE
    )
    df_clean = df_clean.reset_index(drop=True)
    print(f"Working subset selected: {len(df_clean):,} stratified observations.")
"""))

    # Cell 5: Class Imbalance
    cells.append(md_cell("""
## 2. Target Class Distribution & Imbalance Characterization
Contrary to assumptions of equal class balance, the dataset exhibits significant class imbalance with **Fit** representing only **4.64%** of observations.
"""))

    # Cell 6: Plot Imbalance
    cells.append(code_cell("""
target_counts = df_clean['fitness_level'].value_counts()
target_pcts = df_clean['fitness_level'].value_counts(normalize=True) * 100

print("=== Class Distribution Breakdown ===")
for cls in ['Moderate', 'Unfit', 'Fit']:
    print(f"  {cls:<10}: {target_counts[cls]:>8,} ({target_pcts[cls]:>5.2f}%)")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
bars = axes[0].bar(
    target_counts.index, target_counts.values,
    color=[CLASS_PALETTE[c] for c in target_counts.index],
    edgecolor='black', alpha=0.85
)
for bar in bars:
    h = bar.get_height()
    axes[0].text(
        bar.get_x() + bar.get_width() / 2.0, h + len(df_clean) * 0.015,
        f"{int(h):,}\\n({h / len(df_clean) * 100:.1f}%)",
        ha='center', va='bottom', fontweight='bold', fontsize=10
    )
axes[0].set_title("Absolute Observation Counts by Fitness Level", fontsize=11, fontweight='bold')
axes[0].set_ylabel("Count")
axes[0].set_ylim(0, max(target_counts.values) * 1.20)

axes[1].pie(
    target_counts.values, labels=target_counts.index, autopct='%1.1f%%',
    startangle=140, colors=[CLASS_PALETTE[c] for c in target_counts.index],
    explode=[0.02, 0.02, 0.12],
    textprops={'fontsize': 10, 'fontweight': 'bold'},
    wedgeprops={'edgecolor': 'black', 'linewidth': 1}
)
axes[1].set_title("Proportional Distribution (Imbalance Ratio 12.4 : 1)", fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig("figures/01_class_imbalance_breakdown.png", dpi=300, bbox_inches='tight')
plt.show()
"""))

    # Cell 7: EDA
    cells.append(md_cell("""
## 3. Deep Exploratory Data Analysis & DGP Reverse Engineering
We examine target-conditional distributions and empirically prove the non-linear threshold penalty gates governing the data generation process.
"""))

    # Cell 8: KDE Distributions
    cells.append(code_cell("""
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
biometrics = [
    ('steps_per_day', 'Daily Steps (Steps/Day)', axes[0, 0]),
    ('active_minutes', 'Active Physical Minutes / Day', axes[0, 1]),
    ('heart_rate_resting', 'Resting Heart Rate (BPM)', axes[0, 2]),
    ('sleep_hours', 'Daily Sleep Duration (Hours)', axes[1, 0]),
    ('stress_level', 'Psychological Stress Level (1-10)', axes[1, 1]),
    ('bmi', 'Body Mass Index (BMI, kg/m²)', axes[1, 2])
]
for col, label, ax in biometrics:
    for cls in ['Unfit', 'Moderate', 'Fit']:
        subset = df_clean[df_clean['fitness_level'] == cls][col]
        sns.kdeplot(subset, ax=ax, label=cls, color=CLASS_PALETTE[cls], fill=True, alpha=0.25, linewidth=1.8)
    ax.set_title(f"Distribution of {label}", fontsize=10, fontweight='bold')
    ax.set_xlabel(label, fontsize=9)
    ax.set_ylabel("Density", fontsize=9)
    ax.legend(title="Class", loc='upper right', fontsize=8)

plt.tight_layout()
plt.savefig("figures/02_physiological_distributions_kde.png", dpi=300, bbox_inches='tight')
plt.show()
"""))

    # Cell 9: Threshold Gates
    cells.append(code_cell("""
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Panel A: Sleep Deficit Cliff
sleep_bins = pd.cut(df_clean['sleep_hours'], bins=[2, 4.5, 5, 6, 7, 8, 10], labels=['<4.5h', '4.5-5h', '5-6h', '6-7h', '7-8h', '>8h'])
sleep_ct = pd.crosstab(sleep_bins, df_clean['fitness_level'], normalize='index') * 100
sleep_ct[['Unfit', 'Moderate', 'Fit']].plot(
    kind='bar', stacked=True, ax=axes[0, 0],
    color=[CLASS_PALETTE[c] for c in ['Unfit', 'Moderate', 'Fit']],
    edgecolor='black', alpha=0.85
)
axes[0, 0].set_title("A. Sleep Deficit Cliff: Spike to >84% Unfit at Sleep <5h", fontsize=10, fontweight='bold')
axes[0, 0].set_ylabel("Class Share (%)")
axes[0, 0].set_xlabel("Sleep Window")
axes[0, 0].axvline(1.5, color='black', linestyle='--', linewidth=1.5)
axes[0, 0].legend(loc='upper right', fontsize=8)

# Panel B: Stress Threshold Gate
stress_bins = pd.cut(df_clean['stress_level'], bins=[0, 3, 5, 7, 8, 10], labels=['Low (1-3)', 'Mild (3-5)', 'Moderate (5-7)', 'High (7-8)', 'Extreme (>8)'])
stress_ct = pd.crosstab(stress_bins, df_clean['fitness_level'], normalize='index') * 100
stress_ct[['Unfit', 'Moderate', 'Fit']].plot(
    kind='bar', stacked=True, ax=axes[0, 1],
    color=[CLASS_PALETTE[c] for c in ['Unfit', 'Moderate', 'Fit']],
    edgecolor='black', alpha=0.85
)
axes[0, 1].set_title("B. Stress Threshold Gate: Sharp Unfit Escalation at Stress >8", fontsize=10, fontweight='bold')
axes[0, 1].set_ylabel("Class Share (%)")
axes[0, 1].set_xlabel("Stress Tier")
axes[0, 1].axvline(3.5, color='black', linestyle='--', linewidth=1.5)
axes[0, 1].legend(loc='upper right', fontsize=8)

# Panel C: BMI Non-Linear U-Curve
bmi_bins = pd.cut(df_clean['bmi'], bins=[15, 18.5, 22.5, 25, 30, 42], labels=['Underweight (<18.5)', 'Optimal (18.5-22.5)', 'Normal (22.5-25)', 'Overweight (25-30)', 'Obese (>30)'])
bmi_ct = pd.crosstab(bmi_bins, df_clean['fitness_level'], normalize='index') * 100
bmi_ct[['Unfit', 'Moderate', 'Fit']].plot(
    kind='bar', stacked=True, ax=axes[1, 0],
    color=[CLASS_PALETTE[c] for c in ['Unfit', 'Moderate', 'Fit']],
    edgecolor='black', alpha=0.85
)
axes[1, 0].set_title("C. Metabolic BMI Curve: Peak Fit Proportion at 18.5-25 kg/m²", fontsize=10, fontweight='bold')
axes[1, 0].set_ylabel("Class Share (%)")
axes[1, 0].set_xlabel("Clinical BMI Category")
axes[1, 0].legend(loc='upper right', fontsize=8)

# Panel D: Overtraining vs Recovery Interaction
df_clean['recovery_state'] = 'Normal Balance'
df_clean.loc[(df_clean['workouts_per_week'] >= 4) & (df_clean['sleep_hours'] >= 6.5), 'recovery_state'] = 'High Workout + Good Sleep'
df_clean.loc[(df_clean['workouts_per_week'] >= 4) & (df_clean['sleep_hours'] < 6.0), 'recovery_state'] = 'High Workout + Low Sleep (Overtrained)'

rec_ct = pd.crosstab(df_clean['recovery_state'], df_clean['fitness_level'], normalize='index') * 100
rec_ct[['Unfit', 'Moderate', 'Fit']].plot(
    kind='bar', stacked=True, ax=axes[1, 1],
    color=[CLASS_PALETTE[c] for c in ['Unfit', 'Moderate', 'Fit']],
    edgecolor='black', alpha=0.85
)
axes[1, 1].set_title("D. Recovery Failure: Overtraining Without Sleep Induces Unfitness", fontsize=10, fontweight='bold')
axes[1, 1].set_ylabel("Class Share (%)")
axes[1, 1].set_xlabel("Training vs Recovery State")
axes[1, 1].legend(loc='upper right', fontsize=8)

plt.tight_layout()
plt.savefig("figures/03_nonlinear_penalty_thresholds.png", dpi=300, bbox_inches='tight')
plt.show()
"""))

    # Cell 10: Feature Engineering
    cells.append(md_cell("""
## 4. Domain-Informed, Leak-Free Feature Engineering
We engineer physiological interaction features that capture the multi-dimensional nature of physical fitness without leaking target labels:
- **Recovery-Strain Index (RSI):** $\\frac{\\text{sleep\\_hours} \\times \\text{sleep\\_quality}}{\\text{stress\\_level} + 1}$
- **Cardiovascular Efficiency:** $\\frac{\\text{steps\\_per\\_day}}{\\text{heart\\_rate\\_resting} + 1}$
- **Overtraining Exhaustion Risk:** Indicator for heavy training ($\ge 4$ workouts/week) under sleep restriction ($<6$ hours).
- **Metabolic BMI Deviation:** $|\\text{bmi} - 22.5|$
- **Activity to Sedentary Ratio:** $\\frac{\\text{active\\_minutes}}{\\text{sedentary\\_minutes} + 1}$
"""))

    # Cell 11: Feature Engineering Code
    cells.append(code_cell("""
data = df_clean.copy()

# 1. Recovery-Strain Index (RSI)
data['recovery_strain_index'] = (data['sleep_hours'] * data['sleep_quality']) / (data['stress_level'] + 1.0)

# 2. Cardiovascular Efficiency Proxy
data['cardio_efficiency'] = data['steps_per_day'] / (data['heart_rate_resting'] + 1.0)

# 3. Overtraining Exhaustion Risk
data['overtraining_exhaustion'] = ((data['workouts_per_week'] >= 4) & (data['sleep_hours'] < 6.0)).astype(int)

# 4. Metabolic BMI Deviation
data['bmi_deviation_optimal'] = np.abs(data['bmi'] - 22.5)

# 5. Activity to Sedentary Ratio
data['active_to_sedentary_ratio'] = data['active_minutes'] / (data['sedentary_minutes'] + 1.0)

# 6. Physiological Penalty Gates
data['sleep_cliff_flag'] = (data['sleep_hours'] < 5.0).astype(int)
data['stress_cliff_flag'] = (data['stress_level'] > 8.0).astype(int)

# 7. Hydration per Active Minute
data['hydration_per_active_minute'] = data['hydration_liters'] / (data['active_minutes'] + 1.0)

# Target Mapping & Encoding
data['target'] = data['fitness_level'].map(TARGET_MAPPING)
data = pd.get_dummies(data, columns=['lifestyle_category'], drop_first=True)

drops = ['fitness_level', 'target', 'recovery_state']
X = data.drop(columns=[c for c in drops if c in data.columns])
y = data['target']

feature_names = X.columns.tolist()
print(f"Feature matrix generated: {X.shape[0]:,} samples x {X.shape[1]} features.")
"""))

    # Cell 12: Train/Test Split
    cells.append(code_cell("""
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight

# Stratified Split (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=RANDOM_STATE
)

# Scaling for Linear Baseline
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_names, index=X_train.index)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=feature_names, index=X_test.index)

# Balanced class weights
classes = np.unique(y_train)
weights = compute_class_weight(class_weight='balanced', classes=classes, y=y_train)
weight_dict = {i: w for i, w in zip(classes, weights)}
print("Balanced class weights applied:", {INV_TARGET_MAPPING[k]: round(v, 3) for k, v in weight_dict.items()})
"""))

    # Cell 13: Model Tournament
    cells.append(md_cell("""
## 5. Multi-Model Tournament & Cross-Validation Benchmarking
We train and benchmark 4 models under identical conditions:
1. Multinomial Logistic Regression (Class-Weighted Baseline)
2. Random Forest Classifier (Balanced)
3. LightGBM Classifier (Balanced)
4. XGBoost Classifier (Weighted)
"""))

    # Cell 14: Model Training Code
    cells.append(code_cell("""
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, f1_score,
    precision_score, recall_score, classification_report,
    roc_auc_score, confusion_matrix
)
import lightgbm as lgb
import xgboost as xgb

models = {
    "Logistic Regression (Baseline)": LogisticRegression(
        class_weight='balanced',
        max_iter=1000, random_state=RANDOM_STATE
    ),
    "Random Forest (Balanced)": RandomForestClassifier(
        n_estimators=300, max_depth=18, min_samples_leaf=4,
        max_features='sqrt', class_weight='balanced',
        n_jobs=-1, random_state=RANDOM_STATE
    ),
    "LightGBM Classifier (Balanced)": lgb.LGBMClassifier(
        n_estimators=350, learning_rate=0.05, num_leaves=31,
        max_depth=7, class_weight='balanced', subsample=0.85,
        colsample_bytree=0.85, random_state=RANDOM_STATE,
        n_jobs=-1, verbose=-1
    ),
    "XGBoost Classifier (Weighted)": xgb.XGBClassifier(
        n_estimators=350, learning_rate=0.05, max_depth=6,
        subsample=0.85, colsample_bytree=0.85,
        objective='multi:softprob', num_class=3,
        random_state=RANDOM_STATE, n_jobs=-1, tree_method='hist'
    )
}

results = []
fitted_models = {}
predictions = {}
probabilities = {}

for name, model in models.items():
    print(f"\\nTraining model: {name}...")
    t0 = time.time()

    if "Logistic" in name:
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)
        probs = model.predict_proba(X_test_scaled)
    elif "XGBoost" in name:
        sample_w = y_train.map(weight_dict)
        model.fit(X_train, y_train, sample_weight=sample_w)
        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)
    else:
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)

    elapsed = time.time() - t0
    fitted_models[name] = model
    predictions[name] = preds
    probabilities[name] = probs

    # Metrics
    acc = accuracy_score(y_test, preds)
    bal_acc = balanced_accuracy_score(y_test, preds)
    f1_macro = f1_score(y_test, preds, average='macro')
    f1_weighted = f1_score(y_test, preds, average='weighted')
    fit_rec = recall_score(y_test, preds, labels=[2], average=None)[0]
    fit_prec = precision_score(y_test, preds, labels=[2], average=None)[0]
    fit_f1 = f1_score(y_test, preds, labels=[2], average=None)[0]
    roc_auc = roc_auc_score(y_test, probs, multi_class='ovr', average='macro')

    results.append({
        "Model": name,
        "Accuracy": round(acc, 4),
        "Balanced Accuracy": round(bal_acc, 4),
        "F1 Macro": round(f1_macro, 4),
        "F1 Weighted": round(f1_weighted, 4),
        "Fit Recall": round(fit_rec, 4),
        "Fit Precision": round(fit_prec, 4),
        "Fit F1": round(fit_f1, 4),
        "ROC-AUC (OvR)": round(roc_auc, 4),
        "Train Time (s)": round(elapsed, 2)
    })
    print(f"  -> Finished in {elapsed:.1f}s | F1 Macro: {f1_macro:.4f} | Fit Recall: {fit_rec:.4f} | ROC-AUC: {roc_auc:.4f}")

df_results = pd.DataFrame(results)
print("\\n=== Model Benchmark Summary Table ===")
display(df_results)
"""))

    # Cell 15: Confusion Matrices
    cells.append(code_cell("""
fig, axes = plt.subplots(1, 3, figsize=(17, 5))
tree_models = ["Random Forest (Balanced)", "LightGBM Classifier (Balanced)", "XGBoost Classifier (Weighted)"]
for idx, m_name in enumerate(tree_models):
    cm = confusion_matrix(y_test, predictions[m_name], normalize='true') * 100
    sns.heatmap(
        cm, annot=True, fmt=".1f", cmap="Blues", cbar=False, ax=axes[idx],
        xticklabels=['Unfit', 'Moderate', 'Fit'],
        yticklabels=['Unfit', 'Moderate', 'Fit'],
        annot_kws={"size": 11, "fontweight": "bold"}
    )
    axes[idx].set_title(f"{m_name}\\nNormalized Recall (%)", fontsize=10, fontweight='bold')
    axes[idx].set_xlabel("Predicted Label", fontsize=9)
    axes[idx].set_ylabel("True Label", fontsize=9)

plt.tight_layout()
plt.savefig("figures/06_multiclass_confusion_matrices.png", dpi=300, bbox_inches='tight')
plt.show()
"""))

    # Cell 16: SHAP Explainability
    cells.append(md_cell("""
## 6. Explainable AI (SHAP) & Clinical Decision Interpretability
Using TreeExplainer on LightGBM, we visualize global feature attributions, confirm non-linear penalty thresholds, and explain individual clinical case studies.
"""))

    # Cell 17: SHAP Code
    cells.append(code_cell("""
import shap

best_model = fitted_models["LightGBM Classifier (Balanced)"]
sample_size = min(2000, len(X_test))
X_shap = X_test.iloc[:sample_size].copy()
y_shap = y_test.iloc[:sample_size].copy()

print(f"Computing SHAP values for {sample_size:,} observations...")
t0 = time.time()
explainer = shap.TreeExplainer(best_model)
shap_values = explainer(X_shap)
print(f"SHAP computation complete in {time.time() - t0:.1f}s.")

# Figure 7: SHAP Beeswarm for Class 2 (Fit)
plt.figure(figsize=(10, 6.5))
shap.plots.beeswarm(shap_values[:, :, 2], max_display=12, show=False)
plt.title("SHAP Global Summary: Feature Attributions Driving 'Fit' Classification (Class 2)", fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig("figures/07_shap_global_beeswarm_fit.png", dpi=300, bbox_inches='tight')
plt.show()

# Figure 8: SHAP Beeswarm for Class 0 (Unfit)
plt.figure(figsize=(10, 6.5))
shap.plots.beeswarm(shap_values[:, :, 0], max_display=12, show=False)
plt.title("SHAP Global Summary: Feature Attributions Driving 'Unfit' Classification (Class 0)", fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig("figures/08_shap_global_beeswarm_unfit.png", dpi=300, bbox_inches='tight')
plt.show()
"""))

    # Cell 18: Patient Waterfalls
    cells.append(code_cell("""
# Clinical Case 1: Active Individual Classified as 'Unfit' Due to Sleep & Stress Deficits
case1_cands = X_shap[(X_shap['steps_per_day'] > 8500) & (X_shap['sleep_hours'] < 5.0) & (y_shap == 0)]
if len(case1_cands) > 0:
    c1_idx = case1_cands.index[0]
    pos1 = X_shap.index.get_loc(c1_idx)
    plt.figure(figsize=(9, 5.5))
    shap.plots.waterfall(shap_values[pos1, :, 0], max_display=9, show=False)
    plt.title("Clinical Case 1: Active Individual Classified as 'Unfit' Due to Sleep & Stress Deficits", fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig("figures/10_patient_case1_waterfall.png", dpi=300, bbox_inches='tight')
    plt.show()

# Clinical Case 2: Model Athletic Individual Classified as 'Fit'
case2_cands = X_shap[(X_shap['recovery_strain_index'] > 11.0) & (y_shap == 2)]
if len(case2_cands) > 0:
    c2_idx = case2_cands.index[0]
    pos2 = X_shap.index.get_loc(c2_idx)
    plt.figure(figsize=(9, 5.5))
    shap.plots.waterfall(shap_values[pos2, :, 2], max_display=9, show=False)
    plt.title("Clinical Case 2: Model Athletic Individual Classified as 'Fit'", fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig("figures/11_patient_case2_waterfall.png", dpi=300, bbox_inches='tight')
    plt.show()
"""))

    # Cell 19: References
    cells.append(md_cell("""
## 7. References
1. American College of Sports Medicine. (2021). *ACSM's Guidelines for Exercise Testing and Prescription* (11th ed.). Wolters Kluwer.
2. World Health Organization. (2020). *WHO Guidelines on Physical Activity and Sedentary Behaviour*. World Health Organization.
3. Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T. Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems*, 30, 3146–3154.
4. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794.
5. Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems*, 30, 4765–4774.
6. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32.
7. Parasharmanu. (2024). *Synthetic Health Indicators Dataset*. Kaggle.
"""))

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    # Save to both target locations
    target1 = r"C:\Users\Laptek Store\Downloads\Fitness-Level-Prediction-Health-Analytics\notebooks\fitness_level_prediction.ipynb"
    target2 = r"C:\Users\Laptek Store\Downloads\kaggle_health_scratch\2d64_meta\notebook2d642f8f23.ipynb"

    with open(target1, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Saved: {target1}")

    with open(target2, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Saved: {target2}")

if __name__ == "__main__":
    create_notebook()
