# =============================================================================
# Project: Fitness Level Prediction — Advanced Data Mining & Health Analytics
# Authors: Amine Bessaad, Haitham Maatar, Jasser Sghaier
# Academic Supervisor: Pr. Lassad El Moubarki
# Institution: Tunis Business School, University of Tunis
# =============================================================================

import os
import sys
import glob
import time
import argparse
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, f1_score,
    precision_score, recall_score, classification_report,
    roc_auc_score, confusion_matrix
)
from sklearn.utils.class_weight import compute_class_weight

import lightgbm as lgb
import xgboost as xgb
import shap

# Visualization Configuration
sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Output directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIG_DIR = os.path.join(BASE_DIR, "figures")
METRIC_DIR = os.path.join(BASE_DIR, "output_metrics")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(METRIC_DIR, exist_ok=True)

CLASS_PALETTE = {'Moderate': '#3b82f6', 'Unfit': '#ef4444', 'Fit': '#10b981'}
TARGET_MAPPING = {'Unfit': 0, 'Moderate': 1, 'Fit': 2}
INV_TARGET_MAPPING = {0: 'Unfit', 1: 'Moderate', 2: 'Fit'}

# =============================================================================
# 1. DATA LOADING & INTEGRITY AUDIT
# =============================================================================
def load_and_audit_data(sample_size=100000):
    print("=" * 70)
    print("1. INGESTION & DATASET INTEGRITY AUDITING")
    print("=" * 70)

    candidates = [
        os.path.join(BASE_DIR, "data", "fitness_dataset.csv"),
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
    print(f"Missing values: {df_raw.isnull().sum().sum()}")

    # Zero-variance check
    variances = df_raw.select_dtypes(include=np.number).var()
    zero_var_cols = variances[variances == 0].index.tolist()
    print(f"Zero-variance invariant columns detected: {zero_var_cols}")
    for col in zero_var_cols:
        val = df_raw[col].iloc[0]
        print(f"  -> '{col}' is constant = {val} across all records (zero entropy). Dropping.")

    df_clean = df_raw.drop(columns=zero_var_cols).copy()

    # Stratified subsampling for fast, high-fidelity modeling if requested
    if sample_size and sample_size < len(df_clean):
        df_clean, _ = train_test_split(
            df_clean,
            train_size=sample_size,
            stratify=df_clean['fitness_level'],
            random_state=RANDOM_STATE
        )
        df_clean = df_clean.reset_index(drop=True)
        print(f"Working subset selected: {len(df_clean):,} stratified observations.")

    return df_clean

# =============================================================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
def perform_eda(df):
    print("\n" + "=" * 70)
    print("2. EXPLORATORY DATA ANALYSIS & DGP REVERSE-ENGINEERING")
    print("=" * 70)

    target_counts = df['fitness_level'].value_counts()
    target_pcts = df['fitness_level'].value_counts(normalize=True) * 100

    print("Class Distribution Breakdown:")
    for cls in ['Moderate', 'Unfit', 'Fit']:
        print(f"  {cls:<10}: {target_counts[cls]:>8,} ({target_pcts[cls]:>5.2f}%)")

    # Figure 1: Class Imbalance Breakdown
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    bars = axes[0].bar(
        target_counts.index, target_counts.values,
        color=[CLASS_PALETTE[c] for c in target_counts.index],
        edgecolor='black', alpha=0.85
    )
    for bar in bars:
        h = bar.get_height()
        axes[0].text(
            bar.get_x() + bar.get_width() / 2.0, h + len(df) * 0.015,
            f"{int(h):,}\n({h / len(df) * 100:.1f}%)",
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
    p1 = os.path.join(FIG_DIR, "01_class_imbalance_breakdown.png")
    plt.savefig(p1, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {p1}")

    # Figure 2: Target-Conditional Continuous Distributions (KDE)
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
            subset = df[df['fitness_level'] == cls][col]
            sns.kdeplot(subset, ax=ax, label=cls, color=CLASS_PALETTE[cls], fill=True, alpha=0.25, linewidth=1.8)
        ax.set_title(f"Distribution of {label}", fontsize=10, fontweight='bold')
        ax.set_xlabel(label, fontsize=9)
        ax.set_ylabel("Density", fontsize=9)
        ax.legend(title="Class", loc='upper right', fontsize=8)

    plt.tight_layout()
    p2 = os.path.join(FIG_DIR, "02_physiological_distributions_kde.png")
    plt.savefig(p2, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {p2}")

    # Figure 3: Empirical Proof of Non-Linear Threshold Penalty Gates
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # Panel A: Sleep Deficit Cliff
    sleep_bins = pd.cut(df['sleep_hours'], bins=[2, 4.5, 5, 6, 7, 8, 10], labels=['<4.5h', '4.5-5h', '5-6h', '6-7h', '7-8h', '>8h'])
    sleep_ct = pd.crosstab(sleep_bins, df['fitness_level'], normalize='index') * 100
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
    stress_bins = pd.cut(df['stress_level'], bins=[0, 3, 5, 7, 8, 10], labels=['Low (1-3)', 'Mild (3-5)', 'Moderate (5-7)', 'High (7-8)', 'Extreme (>8)'])
    stress_ct = pd.crosstab(stress_bins, df['fitness_level'], normalize='index') * 100
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
    bmi_bins = pd.cut(df['bmi'], bins=[15, 18.5, 22.5, 25, 30, 42], labels=['Underweight (<18.5)', 'Optimal (18.5-22.5)', 'Normal (22.5-25)', 'Overweight (25-30)', 'Obese (>30)'])
    bmi_ct = pd.crosstab(bmi_bins, df['fitness_level'], normalize='index') * 100
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
    df['recovery_state'] = 'Normal Balance'
    df.loc[(df['workouts_per_week'] >= 4) & (df['sleep_hours'] >= 6.5), 'recovery_state'] = 'High Workout + Good Sleep'
    df.loc[(df['workouts_per_week'] >= 4) & (df['sleep_hours'] < 6.0), 'recovery_state'] = 'High Workout + Low Sleep (Overtrained)'

    rec_ct = pd.crosstab(df['recovery_state'], df['fitness_level'], normalize='index') * 100
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
    p3 = os.path.join(FIG_DIR, "03_nonlinear_penalty_thresholds.png")
    plt.savefig(p3, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {p3}")

    # Figure 4: Hierarchical Correlation Clustermap
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    corr_matrix = df[numeric_cols].corr()
    g = sns.clustermap(
        corr_matrix, cmap="vlag", vmin=-0.8, vmax=0.8,
        linewidths=0.5, figsize=(10, 9), annot=True, fmt=".2f",
        annot_kws={"size": 7}
    )
    g.fig.suptitle("Hierarchical Correlation Clustermap of Biometric Indicators", y=1.02, fontsize=11, fontweight='bold')
    p4 = os.path.join(FIG_DIR, "04_correlation_clustermap.png")
    g.savefig(p4, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {p4}")

# =============================================================================
# 3. DOMAIN-INFORMED FEATURE ENGINEERING (ZERO LEAKAGE)
# =============================================================================
def engineer_features(df):
    print("\n" + "=" * 70)
    print("3. DOMAIN-INFORMED FEATURE ENGINEERING (LEAK-FREE)")
    print("=" * 70)

    data = df.copy()

    # 1. Recovery-Strain Index (RSI)
    data['recovery_strain_index'] = (data['sleep_hours'] * data['sleep_quality']) / (data['stress_level'] + 1.0)

    # 2. Cardiovascular Efficiency Proxy
    data['cardio_efficiency'] = data['steps_per_day'] / (data['heart_rate_resting'] + 1.0)

    # 3. Overtraining Exhaustion Risk
    data['overtraining_exhaustion'] = ((data['workouts_per_week'] >= 4) & (data['sleep_hours'] < 6.0)).astype(int)

    # 4. Metabolic BMI Deviation from Optimal Setpoint (22.5 kg/m²)
    data['bmi_deviation_optimal'] = np.abs(data['bmi'] - 22.5)

    # 5. Activity to Sedentary Ratio
    data['active_to_sedentary_ratio'] = data['active_minutes'] / (data['sedentary_minutes'] + 1.0)

    # 6. Physiological Penalty Gates
    data['sleep_cliff_flag'] = (data['sleep_hours'] < 5.0).astype(int)
    data['stress_cliff_flag'] = (data['stress_level'] > 8.0).astype(int)

    # 7. Hydration per Active Minute
    data['hydration_per_active_minute'] = data['hydration_liters'] / (data['active_minutes'] + 1.0)

    # Target Mapping
    data['target'] = data['fitness_level'].map(TARGET_MAPPING)

    # Categorical Encoding
    data = pd.get_dummies(data, columns=['lifestyle_category'], drop_first=True)

    drops = ['fitness_level', 'target', 'recovery_state']
    X = data.drop(columns=[c for c in drops if c in data.columns])
    y = data['target']

    print(f"Feature matrix generated: {X.shape[0]:,} samples x {X.shape[1]} features.")
    return X, y

# =============================================================================
# 4. MULTI-MODEL TOURNAMENT & CROSS-VALIDATION
# =============================================================================
def train_and_benchmark_models(X, y):
    print("\n" + "=" * 70)
    print("4. MULTI-MODEL TOURNAMENT & CROSS-VALIDATION")
    print("=" * 70)

    feature_names = X.columns.tolist()

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
        print(f"\nTraining model: {name}...")
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
    csv_path = os.path.join(METRIC_DIR, "model_benchmark_results.csv")
    df_results.to_csv(csv_path, index=False)
    print(f"\nSaved metrics table: {csv_path}")
    print(df_results.to_string(index=False))

    # Figure 5: Model Tournament Benchmark Comparison
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    df_results.plot(
        x='Model', y=['F1 Macro', 'Balanced Accuracy', 'Fit Recall'],
        kind='bar', ax=axes[0], colormap='viridis', edgecolor='black', alpha=0.9
    )
    axes[0].set_title("A. Macro F1, Balanced Accuracy & Minority Fit Recall", fontsize=11, fontweight='bold')
    axes[0].set_ylabel("Score (0.0 - 1.0)")
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=20, ha='right', fontsize=9)
    axes[0].legend(loc='lower right', fontsize=8)

    df_results.plot(
        x='Model', y=['Accuracy', 'ROC-AUC (OvR)'],
        kind='bar', ax=axes[1], colormap='magma', edgecolor='black', alpha=0.9
    )
    axes[1].set_title("B. Overall Accuracy & Multi-Class ROC-AUC (OvR)", fontsize=11, fontweight='bold')
    axes[1].set_ylabel("Score (0.0 - 1.0)")
    axes[1].set_ylim(0.65, 1.02)
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=20, ha='right', fontsize=9)
    axes[1].legend(loc='lower right', fontsize=8)

    plt.tight_layout()
    p5 = os.path.join(FIG_DIR, "05_model_benchmark_comparison.png")
    plt.savefig(p5, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {p5}")

    # Figure 6: Confusion Matrices for Top Tree Ensembles
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
        axes[idx].set_title(f"{m_name}\nNormalized Recall (%)", fontsize=10, fontweight='bold')
        axes[idx].set_xlabel("Predicted Label", fontsize=9)
        axes[idx].set_ylabel("True Label", fontsize=9)

    plt.tight_layout()
    p6 = os.path.join(FIG_DIR, "06_multiclass_confusion_matrices.png")
    plt.savefig(p6, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {p6}")

    return fitted_models, X_test, y_test, feature_names

# =============================================================================
# 5. EXPLAINABLE AI (XAI) & CLINICAL DECISION INTERPRETABILITY
# =============================================================================
def perform_shap_analysis(fitted_models, X_test, y_test, feature_names):
    print("\n" + "=" * 70)
    print("5. EXPLAINABLE AI (SHAP) & CLINICAL INTERPRETABILITY")
    print("=" * 70)

    best_model = fitted_models["LightGBM Classifier (Balanced)"]

    # Background sample for TreeExplainer
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
    p7 = os.path.join(FIG_DIR, "07_shap_global_beeswarm_fit.png")
    plt.savefig(p7, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {p7}")

    # Figure 8: SHAP Beeswarm for Class 0 (Unfit)
    plt.figure(figsize=(10, 6.5))
    shap.plots.beeswarm(shap_values[:, :, 0], max_display=12, show=False)
    plt.title("SHAP Global Summary: Feature Attributions Driving 'Unfit' Classification (Class 0)", fontsize=11, fontweight='bold')
    plt.tight_layout()
    p8 = os.path.join(FIG_DIR, "08_shap_global_beeswarm_unfit.png")
    plt.savefig(p8, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {p8}")

    # Figure 9: SHAP Dependence Plots (Empirical Proof of Non-Linear Gates)
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    shap_vals_unfit = shap_values.values[:, :, 0]
    sleep_idx = feature_names.index('sleep_hours')
    stress_idx = feature_names.index('stress_level')

    sc1 = axes[0].scatter(
        X_shap['sleep_hours'], shap_vals_unfit[:, sleep_idx],
        alpha=0.6, c=X_shap['stress_level'], cmap='coolwarm', s=25
    )
    axes[0].axvline(5.0, color='black', linestyle='--', linewidth=1.5, label='5.0h Cliff Gate')
    axes[0].set_title("A. SHAP Dependence: Sleep Hours vs Unfit Risk", fontsize=10, fontweight='bold')
    axes[0].set_xlabel("Daily Sleep Hours", fontsize=9)
    axes[0].set_ylabel("SHAP Value (Contribution to Unfit)", fontsize=9)
    axes[0].legend(fontsize=8)
    fig.colorbar(sc1, ax=axes[0], label="Stress Level")

    sc2 = axes[1].scatter(
        X_shap['stress_level'], shap_vals_unfit[:, stress_idx],
        alpha=0.6, c=X_shap['sleep_hours'], cmap='viridis', s=25
    )
    axes[1].axvline(8.0, color='red', linestyle='--', linewidth=1.5, label='8.0 Stress Gate')
    axes[1].set_title("B. SHAP Dependence: Stress Level vs Unfit Risk", fontsize=10, fontweight='bold')
    axes[1].set_xlabel("Stress Level (1-10)", fontsize=9)
    axes[1].set_ylabel("SHAP Value (Contribution to Unfit)", fontsize=9)
    axes[1].legend(fontsize=8)
    fig.colorbar(sc2, ax=axes[1], label="Sleep Hours")

    plt.tight_layout()
    p9 = os.path.join(FIG_DIR, "09_shap_dependence_thresholds.png")
    plt.savefig(p9, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {p9}")

    # Figure 10: Patient Case 1 Waterfall Plot (Active but Sleep-Deprived & Stressed -> Unfit)
    case1_cands = X_shap[(X_shap['steps_per_day'] > 8500) & (X_shap['sleep_hours'] < 5.0) & (y_shap == 0)]
    if len(case1_cands) > 0:
        c1_idx = case1_cands.index[0]
        pos1 = X_shap.index.get_loc(c1_idx)
        plt.figure(figsize=(9, 5.5))
        shap.plots.waterfall(shap_values[pos1, :, 0], max_display=9, show=False)
        plt.title("Clinical Case 1: Active Individual Classified as 'Unfit' Due to Sleep & Stress Deficits", fontsize=10, fontweight='bold')
        plt.tight_layout()
        p10 = os.path.join(FIG_DIR, "10_patient_case1_waterfall.png")
        plt.savefig(p10, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved: {p10}")

    # Figure 11: Patient Case 2 Waterfall Plot (High Recovery Athletic Individual -> Fit)
    case2_cands = X_shap[(X_shap['recovery_strain_index'] > 11.0) & (y_shap == 2)]
    if len(case2_cands) > 0:
        c2_idx = case2_cands.index[0]
        pos2 = X_shap.index.get_loc(c2_idx)
        plt.figure(figsize=(9, 5.5))
        shap.plots.waterfall(shap_values[pos2, :, 2], max_display=9, show=False)
        plt.title("Clinical Case 2: Model Athletic Individual Classified as 'Fit'", fontsize=10, fontweight='bold')
        plt.tight_layout()
        p11 = os.path.join(FIG_DIR, "11_patient_case2_waterfall.png")
        plt.savefig(p11, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved: {p11}")

# =============================================================================
# MAIN PIPELINE
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="Run Fitness Level Prediction Pipeline")
    parser.add_argument("--sample_size", type=int, default=100000, help="Number of observations (default 100,000)")
    args = parser.parse_args()

    t_start = time.time()
    df = load_and_audit_data(sample_size=args.sample_size)
    perform_eda(df)
    X, y = engineer_features(df)
    fitted_models, X_test, y_test, feature_names = train_and_benchmark_models(X, y)
    perform_shap_analysis(fitted_models, X_test, y_test, feature_names)

    total_time = time.time() - t_start
    print("\n" + "=" * 70)
    print(f"PIPELINE COMPLETE IN {total_time:.1f} SECONDS ({total_time / 60:.1f} MINUTES)")
    print("=" * 70)

if __name__ == "__main__":
    main()
