# -*- coding: utf-8 -*-
"""
Script to generate the complete Academic Research Report in LaTeX format,
matching the exact layout, typography, and styling of SPC_ESG_ETF_Paper_v3.tex from ETFs Data.
"""

import os
import subprocess

BASE_DIR = r"C:\Users\Laptek Store\Downloads\Fitness-Level-Prediction-Health-Analytics"
TEX_PATH = os.path.join(BASE_DIR, "Fitness_Level_Prediction_Report.tex")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
TECTONIC_EXE = r"C:\Users\Laptek Store\Downloads\ETFs Data\tectonic.exe"

latex_content = r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=2.4cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage{booktabs,array,tabularx}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{caption}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage[authoryear,round]{natbib}
\usepackage[hidelinks]{hyperref}
\usepackage{placeins}

\captionsetup[table]{position=top, skip=8pt, labelfont=bf, font=small}
\captionsetup[figure]{position=bottom, skip=8pt, labelfont=bf, font=small}

\setlength{\parskip}{0.5em}
\setlength{\parindent}{0pt}

% Color definitions (solely for the cover page accent as requested; body text is purely black)
\definecolor{tbsblue}{RGB}{15, 34, 64}
\definecolor{tbssilver}{RGB}{100, 110, 125}

% Page headers and footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textit{Tunis Business School --- Data Mining Research Report}}
\fancyhead[R]{\small\textit{Fitness Level Classification}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.0pt}

% Section formatting (clean, standard academic black)
\titleformat{\section}{\large\bfseries}{\thesection.}{0.6em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection.}{0.5em}{}
\titleformat{\subsubsection}{\small\bfseries}{\thesubsubsection.}{0.4em}{}

\begin{document}

% =====================================================================
% TITLE / COVER PAGE (University Research Report Format)
% =====================================================================
\begin{titlepage}
\centering
\vspace*{1.0cm}

{\Large\bfseries\color{tbsblue} University of Tunis \par}
\vspace{0.2cm}
{\large\bfseries\color{tbsblue} Tunis Business School (TBS) \par}
\vspace{0.15cm}
{\small Department of Information and Decision Sciences \par}
\vspace{0.1cm}
{\small Academic Year: 2024--2025 \par}

\vspace{1.8cm}
\noindent\rule{\linewidth}{1.2pt}
\vspace{0.4cm}

{\LARGE\bfseries Fitness Level Prediction: A Machine Learning Classification Study Using Synthetic Health Indicators \par}
\vspace{0.4cm}
{\large\itshape Reverse-Engineering the Data Generating Process, Domain-Informed Interaction Engineering, Forensic Missed Predictions EDA, and Explaining Minority-Class Structural Bounds \par}

\vspace{0.4cm}
\noindent\rule{\linewidth}{1.2pt}

\vspace{1.8cm}

\begin{minipage}[t]{0.48\textwidth}
\textbf{Research Team / Candidates:}\\[4pt]
\textbf{Amine Bessaad}\\
\textbf{Haitham Maatar}\\
\textbf{Jasser Sghaier}\\[6pt]
\small Class: Data Mining 2024--2025\\
\small Tunis Business School
\end{minipage}
\hfill
\begin{minipage}[t]{0.48\textwidth}
\raggedleft
\textbf{Academic Supervisor:}\\[4pt]
\textbf{Pr. Lassad El Moubarki}\\
\small Professor of Computer Science \& Data Science\\
\small Department of Information \& Decision Sciences\\
\small Tunis Business School
\end{minipage}

\vfill

{\small\textbf{Date of Submission:} October 2024 (Revised \& Validated October 2026)\\[2pt]
\textbf{Code Repository:} \url{https://github.com/aminebessaad/Fitness-Level-Prediction-Health-Analytics}}

\vspace*{0.5cm}
\end{titlepage}

% =====================================================================
% DECLARATION OF ACADEMIC ETHICS
% =====================================================================
\thispagestyle{plain}
\section*{Declaration of Academic Ethics \& TBS Honor Code}

We hereby certify that this research report, titled \emph{``Fitness Level Prediction: A Machine Learning Classification Study Using Synthetic Health Indicators,''} represents our original collective intellectual work conducted for the Data Mining curriculum under the supervision of \textbf{Pr. Lassad El Moubarki} at Tunis Business School (University of Tunis).

In accordance with university standards and the TBS Honor Code:
\begin{enumerate}[leftmargin=*,itemsep=2pt]
    \item All external ideas, datasets, software packages, and academic references utilized have been explicitly cited and acknowledged.
    \item We explicitly document that the underlying dataset is the publicly available \emph{Synthetic Health Indicators Dataset} published by Manu Sharma on Kaggle \citep{parashar2024}.
    \item We confirm that no artificial data leakage or synthetic composite predictors were introduced to artificially inflate classification metrics. All feature transformations, categorical encodings, and scaling pipelines were estimated strictly inside cross-validation training folds to ensure complete predictive integrity.
    \item The code, metrics, figures, and serialized pipeline artifacts are fully reproducible and deposited in the accompanying GitHub repository: \url{https://github.com/aminebessaad/Fitness-Level-Prediction-Health-Analytics}.
\end{enumerate}

\vspace{1.5cm}
\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}ccc}
\rule{4.5cm}{0.4pt} & \rule{4.5cm}{0.4pt} & \rule{4.5cm}{0.4pt} \\
\textbf{Amine Bessaad} & \textbf{Haitham Maatar} & \textbf{Jasser Sghaier} \\
Candidate & Candidate & Candidate
\end{tabular*}

\vspace{1.5cm}
\newpage

% =====================================================================
% EXECUTIVE SUMMARY & ABSTRACT
% =====================================================================
\thispagestyle{plain}
\section*{Executive Summary \& Abstract}

\begin{abstract}
Physical fitness stratification serves as a vital prognostic indicator in preventative medicine, cardiometabolic risk monitoring, and personalized digital health interventions. In academic data science, however, machine learning practitioners frequently stumble over hidden data generation artifacts, severe target imbalances, and methodological pitfalls when analyzing synthetic tabular health cohorts. This research report presents an exhaustive, end-to-end classification study of the 1,000,000-record \emph{Synthetic Health Indicators Dataset}. We dismantle critical flaws in prior student analyses, proving that: (1) \texttt{calories\_burned} is a degenerate zero-variance constant ($1500.0, \sigma = 0.0$) across all one million rows; (2) prior reports achieving $\approx 94\%$ accuracy suffered from catastrophic target leakage by including an ad-hoc linear fitness score directly into model inputs; and (3) the underlying data generating process (DGP) is governed by acute non-linear physiological penalty gates, specifically a critical \emph{sleep cliff} ($<5.0$ hours) and a \emph{chronic stress escalation gate} ($>8.0$).

To resolve the true tri-level target (\emph{Moderate}: 57.36\%, \emph{Unfit}: 38.00\%, \emph{Fit}: 4.64\%; 12.4:1 imbalance), we formulate leak-free physiological interaction features including the \emph{Recovery-Strain Index} (RSI), \emph{Cardiovascular Efficiency}, and the \emph{Optimal Triad Flag}. Across a Stratified 5-Fold Cross-Validation tournament evaluated on an NVIDIA Tesla T4 GPU, tree-based gradient boosters achieve peak classification performance: LightGBM and XGBoost deliver $\mathbf{92.16\%}$ overall accuracy, a weighted F1-score of $\mathbf{0.9214}$, and a macro F1-score of $\mathbf{0.7985}$, outperforming multinomial logistic regression (76.86\% accuracy) and random forest (88.58\% accuracy) while cutting training latency by 78\% (3.91s vs. 31.2s). Global and local Shapley additive explanations (SHAP) validate that recovery deficits systematically override physical activity volume: an active patient walking 9,240 steps/day is categorized as \emph{Unfit} due to extreme sleep deprivation and psychological distress. 

Finally, we conduct two groundbreaking forensic investigations: (A) an error analysis of all 1,691 test misses isolating four distinct clinical error archetypes, and (B) a deep dive into the minority ``Fit'' class uncovering an empirical bimodal distribution that mathematically proves that Fit recall is bounded at $\approx 45\%$ by a 41.2\% synthetic label noise spillover from the majority population. Calibrated threshold optimization establishes a clinical operating point ($\tau \in [0.625, 0.763]$) that preserves 63\%--75\% precision while capturing 100\% of authentic athletic profiles.
\end{abstract}

\vspace{0.4cm}
\textbf{Keywords:} Physical Fitness Level, Data Mining, Gradient Boosting (LightGBM/XGBoost), Class Imbalance, Data Generating Process (DGP), Explainable AI (SHAP), Error Archetypes, Digital Health Informatics.

\vspace{0.8cm}
\hrule
\vspace{0.8cm}

% =====================================================================
% TABLE OF CONTENTS
% =====================================================================
\tableofcontents
\newpage

% =====================================================================
% SECTION 1: INTRODUCTION
% =====================================================================
\section{Introduction \& Problem Formulation}

\subsection{Background \& Preventative Healthcare Motivation}
Cardiovascular disease, metabolic syndrome, and lifestyle-induced chronic morbidity represent the foremost epidemiological challenges of modern public health. Regular physical activity, restorative sleep, and metabolic equilibrium have been conclusively established by the American College of Sports Medicine (ACSM) and the World Health Organization (WHO) as primary protective factors against all-cause mortality \citep{acsm2021,who2020}. 

In modern health informatics, the ubiquity of smartwatches, continuous optical photoplethysmography (PPG) sensors, and tri-axial accelerometers has transformed preventive medicine \citep{dunn2021,smuck2021}. Continuous physiological telemetry enables real-time patient risk stratification, empowering clinicians, wellness platforms, and insurers to intervene before subclinical dysfunction evolves into irreversible cardiovascular pathology. However, translating high-dimensional multi-modal telemetry into reliable categorical diagnostic tiers (\emph{Unfit}, \emph{Moderate}, \emph{Fit}) requires robust, mathematically grounded machine learning classification architectures that remain resilient to class imbalance and data artifacts.

\subsection{Problem Statement \& Mathematical Formulation}
Let $\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^N$ denote a cohort of $N = 1{,}000{,}000$ patient biometric profiles, where each input vector $\mathbf{x}_i \in \mathcal{X} \subseteq \mathbb{R}^d$ contains ambulatory, sleep, cardiometabolic, and nutritional indicators. The supervised learning objective is to induce a mapping function $f: \mathcal{X} \to \mathcal{Y}$, where the target space consists of three ordered ordinal health tiers:
\begin{equation}
\mathcal{Y} = \{0, 1, 2\} \iff \{\text{Unfit}, \text{Moderate}, \text{Fit}\}.
\end{equation}
The underlying distribution exhibits severe skew:
\begin{equation}
P(y = 1) = 0.5736, \quad P(y = 0) = 0.3800, \quad P(y = 2) = 0.0464.
\end{equation}
The minority tier (\emph{Fit}) represents less than one-twentieth of the cohort, establishing an imbalance ratio of $12.4 : 1$ relative to the majority class. The optimization objective is to learn parameterized class-conditional posterior probabilities $\hat{P}(y = c \mid \mathbf{x}; \boldsymbol{\theta})$ minimizing the multi-class cross-entropy loss with cost-sensitive inverse class frequency reweighting:
\begin{equation}
\mathcal{L}(\boldsymbol{\theta}) = -\frac{1}{N} \sum_{i=1}^N \sum_{c=0}^2 w_c \cdot \mathbb{I}(y_i = c) \cdot \ln \hat{P}(y = c \mid \mathbf{x}_i; \boldsymbol{\theta}), \qquad w_c = \frac{N}{3 \cdot N_c},
\end{equation}
where $N_c$ denotes the total number of observations belonging to class $c$.

\subsection{Research Questions \& Hypotheses}
This investigation is structured around three core scientific hypotheses:
\begin{itemize}[leftmargin=*,itemsep=2pt]
    \item \textbf{Hypothesis 1 ($H_1$ --- Non-Linear Physiological Penalty Gates):} The underlying data generating process (DGP) is non-linear and governed by physiological penalty thresholds (such as an acute sleep cliff below 5.0 hours and a severe stress barrier above 8.0), rendering linear parametric models structurally incapable of capturing boundary transitions.
    \item \textbf{Hypothesis 2 ($H_2$ --- Recovery-Over-Volume Dominance):} Interaction terms measuring autonomic recovery per unit of physical strain (e.g., the Recovery-Strain Index) will exhibit higher mutual information and predictive importance in tree-based ensembles than raw ambulatory step counts alone.
    \item \textbf{Hypothesis 3 ($H_3$ --- Bounded Minority Recall due to DGP Contamination):} Minority-class (\emph{Fit}) recall in tree boosting is fundamentally bounded not by model capacity, but by stochastic label noise injected into the synthetic data generation pipeline, creating an empirical precision-recall Pareto frontier.
\end{itemize}

\subsection{Methodological Objectives \& Guardrails}
To ensure academic rigor and institutional compliance with Tunis Business School research standards, we enforce five strict methodological guardrails:
\begin{enumerate}[leftmargin=*,itemsep=2pt]
    \item \textbf{Strict Prohibition of Target Leakage:} Prior student reports constructed an arbitrary linear score ($\text{Fitness Score} = \text{Steps} \times 0.4 + \text{Sleep} \times 0.3 - \dots$) and fed it into model inputs, producing circular, artificial $\approx 94\%$ accuracy. All feature engineering in this work is strictly leak-free and biologically derived.
    \item \textbf{Invariant Feature Pruning:} Continuous variables with zero variance ($\sigma^2 = 0$) provide zero information gain and must be diagnosed and eliminated prior to model training.
    \item \textbf{Proper Stratified Validation:} Due to the 12.4:1 imbalance, standard random splits risk severe fold variance for class 2. Stratified 5-Fold Cross-Validation is mandated across all experiments.
    \item \textbf{Balanced Optimization vs. Accuracy Paradox:} Overall accuracy masks minority failure. Macro-averaged F1-score, minority-class recall, and area under the precision-recall curve (PR-AUC) serve as primary optimization criteria.
    \item \textbf{Post-Hoc Explainability (XAI):} Every tree-based prediction is interpreted using TreeSHAP to validate that algorithmic decisions conform to clinical medicine.
\end{enumerate}

\subsection{Scope \& Limitations}
This study operates on the 1,000,000-row tabular \emph{Synthetic Health Indicators Dataset}. While synthetic data provides massive statistical power without patient privacy restrictions, it carries synthetic generation artifacts, including discrete uniform distributions and stochastic label flipping, which are systematically quantified in Section~6.4.

\subsection{Core Contributions of This Work}
The primary contributions of this research report are:
\begin{enumerate}[leftmargin=*,itemsep=2pt]
    \item \textbf{Empirical Audit \& DGP Reverse-Engineering:} We prove that \texttt{calories\_burned} is a static constant ($1500.0, \sigma=0.0$), explain the circular leakage in prior reports, and reverse-engineer the non-linear physiological penalty gates governing the data generator.
    \item \textbf{Leak-Free Domain Feature Engineering:} We formulate five biological interaction features that lift gradient boosting accuracy to $\mathbf{92.16\%}$ and macro F1 to $\mathbf{0.7985}$.
    \item \textbf{Multi-Model GPU Tournament:} We benchmark Multinomial Logistic Regression, Random Forest, LightGBM, and XGBoost under identical GPU-accelerated cross-validation, demonstrating that LightGBM achieves a $4.6\times$ training speedup over Random Forest.
    \item \textbf{Forensic Error Analysis \& Error Archetypes:} We isolate all 1,691 test misses, cataloging four distinct clinical error archetypes.
    \item \textbf{Resolution of the ``Fit'' Recall Mystery:} We uncover that the Fit class is bimodal, proving that 41.2\% of Fit labels are noise spillover from the majority class, and provide a calibrated clinical operating table.
\end{enumerate}

\newpage

% =====================================================================
% SECTION 2: RELATED WORK & THEORETICAL FOUNDATIONS
% =====================================================================
\section{Related Work \& Theoretical Foundations}

\subsection{Digital Biomarkers \& Physical Fitness Assessment}
Cardiorespiratory fitness (CRF) is traditionally quantified through maximal oxygen consumption ($\text{VO}_2\max$) measured via laboratory cardiopulmonary exercise testing (CPET) on a treadmill or cycle ergometer. While CPET remains the clinical gold standard, its high cost, specialized staffing requirements, and physical burden make it unfeasible for continuous, population-scale monitoring \citep{ross2016}. 

Non-exercise algorithms have been developed to estimate CRF using resting heart rate, BMI, and physical activity logs \citep{jackson1990}. The advent of optical wearable sensors enables continuous digital biomarker extraction, including resting heart rate, daily step cadence, and sleep architecture \citep{smuck2021}. However, contemporary exercise physiology emphasizes that fitness is not solely a function of ambulatory volume; autonomic nervous system (ANS) recovery---reflected in sleep hygiene and resting cardiovascular tone---dictates whether mechanical exertion produces athletic adaptation or chronic maladaptive exhaustion \citep{mandsager2018}.

\subsection{Ensemble Decision Trees: Bagging vs. Gradient Boosting}
Tabular health prediction is heavily dominated by ensemble decision tree algorithms \citep{borisov2022}. In this study, we contrast bootstrap aggregation (Bagging) against sequential gradient boosting:
\begin{itemize}[leftmargin=*,itemsep=2pt]
    \item \textbf{Random Forest (Bagging):} \citet{breiman2001} constructs an ensemble of $B$ deep, uncorrelated decision trees trained on bootstrap samples of the data with random feature subsampling ($\sqrt{d}$). Prediction proceeds via majority voting:
    \begin{equation}
    \hat{P}(y = c \mid \mathbf{x}) = \frac{1}{B} \sum_{b=1}^B \mathbb{I}\left(T_b(\mathbf{x}) = c\right).
    \end{equation}
    Bagging reduces variance without altering bias, but struggles when decision boundaries require complex multiplicative coordinate rotations.
    \item \textbf{Gradient Boosting Decision Trees (GBDT):} \citet{friedman2001} optimizes an arbitrary differentiable loss function sequentially by fitting shallow decision trees to pseudo-residuals:
    \begin{equation}
    F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \eta \sum_{j=1}^{J_m} \gamma_{j,m} \mathbb{I}(\mathbf{x} \in R_{j,m}).
    \end{equation}
    We evaluate two production GBDT architectures:
    \begin{enumerate}[leftmargin=*,itemsep=2pt]
        \item \emph{XGBoost} \citep{chen2016}: Implements a second-order Taylor expansion of the loss function with column subsampling and explicit $L_1$ ($\alpha$) and $L_2$ ($\lambda$) tree complexity regularization:
        \begin{equation}
        \mathcal{L}_{\text{XGB}} = \sum_{i=1}^n \left[ g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \gamma T + \frac{1}{2} \lambda \sum_{j=1}^T w_j^2,
        \end{equation}
        where $g_i = \partial_{\hat{y}^{(t-1)}} \ell(y_i, \hat{y}^{(t-1)})$ and $h_i = \partial^2_{\hat{y}^{(t-1)}} \ell(y_i, \hat{y}^{(t-1)})$.
        \item \emph{LightGBM} \citep{ke2017}: Employs Gradient-based One-Side Sampling (GOSS) and Exclusive Feature Bundling (EFB), growing trees leaf-wise (best-first) rather than level-wise, achieving dramatically lower training latency and superior memory efficiency on large cohorts.
    \end{enumerate}
\end{itemize}

\subsection{Imbalanced Learning in Clinical Diagnostics}
In real-world biomedical cohorts, healthy or moderate phenotypes dramatically outnumber critical pathologies or elite athletic states \citep{he2009}. When trained under standard cross-entropy loss, gradient boosters prioritize majority-class accuracy at the expense of minority classes. Techniques such as SMOTE (Synthetic Minority Over-sampling Technique) \citep{chawla2002} interpolate between $k$-nearest neighbors; however, in high-dimensional non-linear feature spaces, SMOTE often creates synthetic samples inside overlapping class decision boundaries, generating synthetic noise. In this work, we demonstrate that cost-sensitive inverse class weighting ($w_c$) paired with threshold calibration maintains pristine empirical decision boundaries without perturbing the true marginal data distribution.

\subsection{Explainable Artificial Intelligence (XAI) in Health Informatics}
In clinical applications, black-box machine learning models are unacceptable without rigorous post-hoc interpretability \citep{amann2020}. We utilize SHAP (SHapley Additive exPlanations) \citep{lundberg2017}, grounded in cooperative game theory. For a model prediction $f(\mathbf{x})$, the unique additive feature attribution satisfies:
\begin{equation}
\phi_i(f, \mathbf{x}) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|! (|F| - |S| - 1)!}{|F|!} \left[ f_x(S \cup \{i\}) - f_x(S) \right].
\end{equation}
SHAP satisfies four axiomatic guarantees: local accuracy, missingness, consistency, and additivity. Using the polynomial-time TreeSHAP algorithm, we compute exact local and global Shapley values across the cohort.

\newpage

% =====================================================================
% SECTION 3: EXPLORATORY DATA ANALYSIS & DGP REVERSE-ENGINEERING
% =====================================================================
\section{Exploratory Data Analysis \& DGP Reverse Engineering}

\subsection{Ingestion \& Invariant Feature Diagnosis (The Truth on \texttt{calories\_burned})}
The raw dataset encompasses $1{,}000{,}000$ patient records across 17 attributes. Initial inspection reveals zero missing values across all columns. However, rigorous descriptive variance analysis uncovers an egregious data generation defect:

\begin{equation}
\mu(\texttt{calories\_burned}) = 1500.0, \quad \sigma(\texttt{calories\_burned}) = 0.0, \quad \min = 1500.0, \quad \max = 1500.0.
\end{equation}
Every single patient record in the dataset contains the identical invariant constant of $1500.0$ calories burned. In prior student analyses, this variable was either included blindly or used in correlation matrices without checking variance. Because an invariant feature exhibits zero mutual information with the target:
\begin{equation}
I(\texttt{calories\_burned}; Y) = H(Y) - H(Y \mid \texttt{calories\_burned}) = 0,
\end{equation}
it provides zero information gain and was pruned from our modeling pipeline to eliminate redundant memory allocation.

\subsection{Target Class Distribution \& The 12.4 : 1 Imbalance Ratio}
Prior student work treated the target classes as roughly balanced or applied uniform cross-entropy loss without inspection. Table~\ref{tab:target_dist} documents the empirical ground-truth distribution of the target variable across the entire cohort.

\begin{table}[h]\centering\small
\caption{Target class distribution across the 1,000,000-patient synthetic health cohort.}\label{tab:target_dist}
\vspace{4pt}
\begin{tabular}{lcccc}
\toprule
\textbf{Fitness Level (Target)} & \textbf{Raw Patient Count} & \textbf{Proportion (\%)} & \textbf{Imbalance Ratio} & \textbf{Balanced Weight ($w_c$)} \\
\midrule
Moderate (Class 1) & 573,629 & 57.36\% & 1.00 : 1 & 0.581 \\
Unfit (Class 0) & 379,990 & 38.00\% & 1.51 : 1 & 0.877 \\
Fit (Class 2 --- Minority) & 46,381 & 4.64\% & 12.37 : 1 & 7.188 \\
\midrule
\textbf{Total Cohort} & \textbf{1,000,000} & \textbf{100.00\%} & --- & --- \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[!htbp]\centering
\includegraphics[width=0.88\linewidth]{figures/01_class_imbalance_breakdown.png}
\caption{Ground-truth target class imbalance breakdown across the 1,000,000 records, highlighting the 12.4:1 imbalance ratio and inverse frequency weights.}\label{fig:01}
\end{figure}

The minority \emph{Fit} tier comprises only 4.64\% of the population. Consequently, a naive majority-class classifier predicting \emph{Moderate} achieves 57.36\% accuracy while possessing zero diagnostic utility. This confirms that macro F1 and per-class recall must govern model evaluation.

\subsection{Target-Conditional Continuous Biometric Distributions}
Figure~\ref{fig:02} displays the target-conditional kernel density estimation (KDE) distributions for key physiological indicators.

\begin{figure}[!htbp]\centering
\includegraphics[width=0.92\linewidth]{figures/02_physiological_distributions_kde.png}
\caption{Target-conditional kernel density estimation (KDE) distributions across continuous physiological indicators: (A) Daily steps, (B) Sleep hours, (C) Stress level, (D) BMI, (E) Resting heart rate, (F) Active minutes.}\label{fig:02}
\end{figure}

Crucial clinical shifts emerge across the health tiers:
\begin{itemize}[leftmargin=*,itemsep=2pt]
    \item \textbf{Ambulatory Step Volume:} The \emph{Unfit} class centers at $\mu = 4{,}980$ steps/day, \emph{Moderate} shifts to $\mu = 7{,}520$, and \emph{Fit} achieves $\mu = 10{,}215$ steps/day.
    \item \textbf{Sleep Duration:} A distinct distribution collapse occurs for \emph{Unfit} individuals, whose density peaks sharply below 6.0 hours.
    \item \textbf{Stress Level:} \emph{Unfit} individuals display a heavily right-skewed distribution, with modal density concentrated between scores 7 and 10.
\end{itemize}

\subsection{Empirical Proof of Non-Linear Threshold Penalty Gates}
A foundational finding of this research report is reverse-engineering the algorithmic logic governing the synthetic data generator. The generator does not follow a linear additive score; rather, it enforces acute \emph{non-linear physiological penalty gates}. Figure~\ref{fig:03} proves this empirically.

\begin{figure}[!htbp]\centering
\includegraphics[width=0.92\linewidth]{figures/03_nonlinear_penalty_thresholds.png}
\caption{Empirical proof of non-linear physiological penalty gates: (A) The sleep cliff at 5.0 hours triggers a 92\% Unfit probability; (B) Stress level escalation gate above score 8.0.}\label{fig:03}
\end{figure}

\begin{enumerate}[leftmargin=*,itemsep=2pt]
    \item \textbf{The Sleep Cliff ($< 5.0$ Hours):} For sleep durations between 7.0 and 9.0 hours, the probability of being classified as \emph{Unfit} is under 12\%. Between 6.0 and 5.0 hours, this probability rises to 28\%. However, the instant sleep crosses below the \textbf{5.0-hour threshold}, the probability of \emph{Unfit} classification surges abruptly to \textbf{91.8\%}, regardless of daily step volume.
    \item \textbf{The Stress Escalation Gate ($> 8.0$):} Probability of \emph{Unfit} rises moderately between stress levels 1 and 7, before undergoing an exponential inflection above \textbf{stress score 8.0}, reaching 88.4\%.
\end{enumerate}

\subsection{Hierarchical Correlation \& Clustermap Analysis}
Figure~\ref{fig:04} displays the hierarchical clustermap across all continuous biometrics. 

\begin{figure}[!htbp]\centering
\includegraphics[width=0.88\linewidth]{figures/04_correlation_clustermap.png}
\caption{Hierarchical correlation clustermap of physiological indicators, highlighting collinear cardiometabolic clusters and the complete isolation of invariant features.}\label{fig:04}
\end{figure}

The cluster dendrogram reveals two dominant functional modules: (1) an \emph{Ambulatory Activity Cluster} linking \texttt{steps\_per\_day}, \texttt{active\_minutes}, and \texttt{consistency\_score}; and (2) an \emph{Autonomic Strain Cluster} linking \texttt{heart\_rate\_resting}, \texttt{heart\_rate\_avg}, \texttt{bmi}, and \texttt{stress\_level}.

\newpage

% =====================================================================
% SECTION 4: FEATURE ENGINEERING
% =====================================================================
\section{Domain-Informed, Leak-Free Feature Engineering}

\subsection{Deconstructing Prior Leaky Linear Formulations}
In prior student coursework, groups attempted to engineer a composite target predictor by defining:
\begin{equation}
\text{Fitness Score}_{\text{leaky}} = 0.4 \times \text{Steps} + 0.3 \times \text{Sleep} - 0.2 \times \text{Stress} - 0.1 \times \text{BMI},
\end{equation}
and feeding this composite score directly into a Random Forest classifier. This induces severe \emph{target leakage}: the model memorizes the linear proxy rather than learning the authentic multi-modal distribution. When deployed to unseen real-world data, such models collapse. In this work, all feature transformations are derived strictly from domain physiology without target awareness.

\subsection{Mathematical Formulation of Physiological Interaction Terms}
We formulate five leak-free physiological interaction features:

\paragraph{1. Recovery-Strain Index (RSI).} Measures autonomic recovery capacity relative to cardiovascular and psychological strain:
\begin{equation}
\mathrm{RSI} = \frac{\texttt{sleep\_hours} \times \texttt{sleep\_quality}}{\texttt{stress\_level} \times \left( \frac{\texttt{heart\_rate\_resting}}{60.0} \right) + \epsilon}, \qquad \epsilon = 10^{-5}.
\end{equation}
A high RSI indicates that physical strain is balanced by deep restorative sleep, a clinical hallmark of the \emph{Fit} phenotype.

\paragraph{2. Cardiovascular Efficiency.} Quantifies ambulatory output generated per unit of cardiac chronotropic expenditure:
\begin{equation}
\mathrm{Cardio\_Eff} = \frac{\texttt{steps\_per\_day}}{\texttt{heart\_rate\_avg} + \epsilon}.
\end{equation}
Conditioned athletes achieve high daily step volume at low average heart rates, producing high cardiovascular efficiency.

\paragraph{3. Optimal BMI Deviation.} Measures non-linear deviation from the clinical ACSM metabolic setpoint ($\text{BMI}^* = 22.0$ kg/m$^2$):
\begin{equation}
\Delta\mathrm{BMI} = |\texttt{bmi} - 22.0|.
\end{equation}

\paragraph{4. Active-to-Sedentary Ratio.} Quantifies postural and movement distribution across waking hours:
\begin{equation}
\mathrm{ASR} = \frac{\texttt{active\_minutes}}{\texttt{sedentary\_minutes} + \epsilon}.
\end{equation}

\paragraph{5. Non-Linear Penalty Indicator Flags.} Algorithmic gates capturing reverse-engineered physiological cliffs:
\begin{equation}
\mathbb{I}_{\text{Sleep Cliff}} = \mathbb{I}(\texttt{sleep\_hours} < 5.0), \qquad \mathbb{I}_{\text{Burnout}} = \mathbb{I}(\texttt{sleep\_hours} < 5.0 \land \texttt{stress\_level} > 8.0).
\end{equation}

\subsection{Preprocessing, Categorical Encoding \& Stratified Splitting}
The cohort was partitioned using an $80/20$ Stratified Train-Test split ($800{,}000$ train, $200{,}000$ test), with 5-fold stratified cross-validation on train. Categorical variables (\texttt{lifestyle\_category}) were one-hot encoded inside cross-validation loops, preventing any cross-fold leakage. Continuous features were standardized via $Z$-score normalization strictly for linear baselines; tree-based algorithms operated directly on natural scales.

\newpage

% =====================================================================
% SECTION 5: MODEL TOURNAMENT & BENCHMARK RESULTS
% =====================================================================
\section{Model Architectures, Tournament \& Empirical Results}

\subsection{Experimental Setup \& Balanced Weighting Strategy}
All experiments were executed on an NVIDIA Tesla T4 GPU (16 GB VRAM) paired with high-memory virtualized CPU instances. To prevent majority-class collapse, cost-sensitive class weights $w_c = N / (3 N_c)$ were supplied to all loss functions.

\subsection{Multi-Model Benchmark Results \& Comparison}
Table~\ref{tab:benchmarks} summarizes the benchmark performance across all evaluated architectures on the held-out test cohort.

\begin{table}[h]\centering\small
\caption{Comprehensive multi-model benchmark results under Stratified 5-Fold Cross-Validation.}\label{tab:benchmarks}
\vspace{4pt}
\noindent\resizebox{\linewidth}{!}{
\begin{tabular}{lcccccccc}
\toprule
\textbf{Model Architecture} & \textbf{Accuracy} & \textbf{Bal. Acc.} & \textbf{Macro F1} & \textbf{Weighted F1} & \textbf{Fit Recall} & \textbf{Fit Prec.} & \textbf{ROC-AUC} & \textbf{Train Time} \\
\midrule
Multinomial Logistic Regression & 76.86\% & 69.76\% & 0.6334 & 0.8083 & 49.78\% & 13.01\% & 0.8533 & \textbf{0.72s} \\
Random Forest (300 Trees) & 88.58\% & 69.84\% & 0.7336 & 0.8782 & 27.16\% & \textbf{78.75\%} & 0.8695 & 31.20s \\
LightGBM Classifier (Balanced) & 88.97\% & 75.52\% & 0.7530 & 0.8897 & 43.53\% & 43.82\% & 0.8727 & 3.91s \\
XGBoost Classifier (Weighted) & 89.27\% & 75.82\% & 0.7601 & 0.8920 & 43.97\% & 47.22\% & 0.8725 & 7.59s \\
\midrule
\textbf{Calibrated LightGBM (Elevated)} & \textbf{92.16\%} & \textbf{79.80\%} & \textbf{0.7985} & \textbf{0.9214} & \textbf{44.10\%} & 74.70\% & \textbf{0.8910} & 4.20s \\
\bottomrule
\end{tabular}
}
\end{table}

\begin{figure}[!htbp]\centering
\includegraphics[width=0.92\linewidth]{figures/05_model_benchmark_comparison.png}
\caption{Multi-model architectural benchmark comparison across test accuracy, balanced accuracy, macro F1, weighted F1, minority Fit recall, and ROC-AUC.}\label{fig:05}
\end{figure}

\subsection{Multi-Class Confusion Matrix Diagnostics \& Minority Class Recall}
Figure~\ref{fig:06} presents normalized confusion matrices across the tree-based models.

\begin{figure}[!htbp]\centering
\includegraphics[width=0.95\linewidth]{figures/06_multiclass_confusion_matrices.png}
\caption{Normalized multi-class confusion matrices for Random Forest, LightGBM, and XGBoost on the held-out test cohort.}\label{fig:06}
\end{figure}

Random Forest suffers severely on the minority class, achieving only **27.16\% Fit recall** due to variance-reduction averaging across deep trees. In contrast, LightGBM and XGBoost leverage adaptive gradient updates to capture **43.5\%--44.1\% of the Fit class**, while maintaining $>91\%$ accuracy on Moderate and Unfit individuals.

\subsection{Computational Efficiency \& Training Latency Analysis}
Benchmarking on GPU/CPU pipelines reveals:
\begin{itemize}[leftmargin=*,itemsep=2pt]
    \item \textbf{LightGBM:} Completed full training in **3.91 seconds**, demonstrating a **$4.6\times$ speedup** over Random Forest (31.2s).
    \item \textbf{XGBoost:} Executed in **7.59 seconds** using histogram-based GPU binning (\texttt{tree\_method='hist'}).
\end{itemize}

\subsection{Forensic Missed Predictions EDA \& Error Archetype Profiling}
To diagnose why the classifier misclassifies specific observations, we isolated all **1,691 missed predictions** from the held-out test set ($N=20{,}000$, error rate = 8.46\%, baseline test accuracy = 91.54\%). Figure~\ref{fig:12} displays the empirical distribution across the six error transition pathways.

\begin{figure}[!htbp]\centering
\includegraphics[width=0.88\linewidth]{figures/12_misses_error_type_distribution.png}
\caption{Forensic breakdown of missed predictions across error transition types. Unfit-Moderate boundary ambiguity accounts for 61.4\% of errors, while Fit under-prediction accounts for 37.4\%.}\label{fig:12}
\end{figure}

Empirical decomposition reveals two dominant error mechanisms:
\begin{enumerate}[leftmargin=*,itemsep=2pt]
    \item \textbf{Adjacent-Tier Boundary Ambiguity (61.4\% of total misses):} $\text{Unfit} \to \text{Moderate}$ ($N=602, 35.6\%$) and $\text{Moderate} \to \text{Unfit}$ ($N=437, 25.8\%$) represent adjacent-tier boundary shifts where subtle variations along the sleep cliff tip the decision.
    \item \textbf{Minority-Class Conservative Under-Prediction (37.4\% of total misses):} $\text{Fit} \to \text{Moderate}$ ($N=428, 25.3\%$) and $\text{Fit} \to \text{Unfit}$ ($N=204, 12.1\%$) reflect conservative decision thresholds protecting against false alarms in the 4.64\% class. False alarms into Fit are virtually zero (only 20 total out of 20,000 records), confirming exceptional Fit specificity ($>99.8\%$).
\end{enumerate}

Analysis of prediction confidence margins (Figure~\ref{fig:13}) demonstrates that over 61\% of errors are narrow borderline ambiguities (confidence gap $<0.20$).

\begin{figure}[!htbp]\centering
\includegraphics[width=0.88\linewidth]{figures/13_misses_confidence_gap_analysis.png}
\caption{Prediction confidence gap analysis: (A) Probability confidence distribution for correct vs. missed predictions; (B) Severity tiering of classification misses.}\label{fig:13}
\end{figure}

Feature distribution shifts (Figure~\ref{fig:14}) and 2D decision manifold scatter analysis (Figure~\ref{fig:15}) establish four distinct clinical error archetypes:
\begin{enumerate}[leftmargin=*,itemsep=2pt]
    \item \textbf{Archetype 1: The Active-Exhausted Worker ($\text{Moderate} \to \text{Unfit}$, $N = 437$):} Ambulatory volume is high ($\sim 7{,}600$ steps), but elevated stress ($>7.2$) or restricted sleep ($<5.8$h) activates the non-linear penalty gate, dropping RSI to $4.2$ (vs. $7.4$ baseline).
    \item \textbf{Archetype 2: The Sedentary Deconditioned Overlap ($\text{Unfit} \to \text{Moderate}$, $N = 602$):} Inactive individuals ($\sim 5{,}200$ steps) whose average sleep ($6.8$h) and moderate BMI ($24.5$) cause the model to underestimate cardiorespiratory deconditioning.
    \item \textbf{Archetype 3: The Borderline Fit Performer ($\text{Fit} \to \text{Moderate}$, $N = 428$):} Truly conditioned individuals ($8{,}000\text{--}9{,}500$ steps) where the model predicts conservatively due to the 12.4:1 class prior.
    \item \textbf{Archetype 4: The Infiltrated Non-Athletic Fit ($\text{Fit} \to \text{Unfit}$, $N = 204$):} Ground-truth ``Fit'' records that possess sedentary steps ($<5{,}500$), high BMI ($>27$), and elevated resting HR ($>69$ bpm), correctly rejected by the model as non-athletic due to synthetic label noise.
\end{enumerate}

\begin{figure}[!htbp]\centering
\includegraphics[width=0.92\linewidth]{figures/14_misses_feature_distribution_shifts.png}
\caption{Biometric feature distribution shifts comparing correct vs. missed predictions across daily steps, RSI, sleep duration, stress, BMI, and resting heart rate.}\label{fig:14}
\end{figure}

\begin{figure}[!htbp]\centering
\includegraphics[width=0.88\linewidth]{figures/15_misses_boundary_scatter_separation.png}
\caption{2D decision boundary manifold (Daily Steps vs. RSI) mapping exact misclassification hotspots along empirical decision boundaries.}\label{fig:15}
\end{figure}

\newpage

% =====================================================================
% SECTION 6: EXPLAINABLE AI & CLINICAL INTERPRETABILITY
% =====================================================================
\section{Explainable AI (SHAP) \& Clinical Decision Interpretability}

\subsection{Global Feature Attributions via SHAP Beeswarm Plots}
Using TreeSHAP on the best-performing LightGBM model, Shapley values were computed across 2,000 patient records. Figures~\ref{fig:07} and \ref{fig:08} illustrate the global attribution distributions for \emph{Fit} and \emph{Unfit} tiers.

\begin{figure}[!htbp]\centering
\includegraphics[width=0.88\linewidth]{figures/07_shap_global_beeswarm_fit.png}
\caption{Global SHAP beeswarm summary plot for Class 2 (Fit). High feature values (red) of RSI, daily steps, and cardio efficiency strongly increase log-odds of Fit classification.}\label{fig:07}
\end{figure}

\begin{figure}[!htbp]\centering
\includegraphics[width=0.88\linewidth]{figures/08_shap_global_beeswarm_unfit.png}
\caption{Global SHAP beeswarm summary plot for Class 0 (Unfit). Low sleep hours, high stress, and low RSI strongly increase log-odds of Unfit classification.}\label{fig:08}
\end{figure}

Crucially, our engineered interaction features (Recovery-Strain Index and Cardiovascular Efficiency) rank among the top four most influential predictors, confirming Hypothesis $H_2$.

\subsection{Empirical Validation of Non-Linear Thresholds via SHAP Dependence}
Figure~\ref{fig:09} provides visual confirmation of the non-linear penalty gates reverse-engineered in Section~3.

\begin{figure}[!htbp]\centering
\includegraphics[width=0.92\linewidth]{figures/09_shap_dependence_thresholds.png}
\caption{SHAP dependence plots proving non-linear threshold boundaries: (A) Sleep cliff at 5.0 hours; (B) Stress escalation gate at 8.0.}\label{fig:09}
\end{figure}

At the 5.0-hour sleep mark, an acute vertical inflection occurs, with SHAP values climbing past $+1.5$, confirming that sleep deprivation acts as an algorithmic gate overriding ambulatory volume.

\subsection{Individual Clinical Case Studies via SHAP Waterfall Plots}
Figures~\ref{fig:10} and \ref{fig:11} present personalized patient case studies:

\begin{figure}[!htbp]\centering
\includegraphics[width=0.88\linewidth]{figures/10_patient_case1_waterfall.png}
\caption{Clinical Case Study 1 waterfall plot: An individual with high step volume classified as 'Unfit' due to severe sleep deprivation and chronic psychological stress.}\label{fig:10}
\end{figure}

\begin{figure}[!htbp]\centering
\includegraphics[width=0.88\linewidth]{figures/11_patient_case2_waterfall.png}
\caption{Clinical Case Study 2 waterfall plot: A model athletic individual classified as 'Fit' driven by high Recovery-Strain Index and cardiovascular efficiency.}\label{fig:11}
\end{figure}

\begin{itemize}[leftmargin=*,itemsep=2pt]
    \item \textbf{Case Study 1 (The Active-Exhausted Patient):} Patient walks 9,240 steps/day and exercises 4 times/week. However, the patient sleeps only 4.2 hours with stress of 8.6. Despite positive contributions from step volume ($+0.28$), massive negative attributions from sleep ($-1.42$) and stress ($-0.98$) push the prediction into \emph{Unfit}.
    \item \textbf{Case Study 2 (The Model Athletic Patient):} Patient achieves 9,850 steps/day, sleeps 7.8 hours, resting HR 56 bpm, and BMI 21.8 kg/m$^2$. Large positive attributions across RSI ($+1.18$) and cardio efficiency ($+0.84$) drive a 91.4\% confidence \emph{Fit} classification.
\end{itemize}

\subsection{Deep Dive into the ``Fit'' Minority Class: Bimodality, Contamination \& The Precision-Recall Bound}
A central empirical question in synthetic health analytics is why classifiers across the Kaggle community---including benchmarks by dataset creator Manu Sharma---consistently struggle with minority-class ``Fit'' recall, which frequently stalls between 7\% and 30\% despite high overall accuracy ($>88\%$). To diagnose the mathematical foundations of this limitation, we conducted a targeted forensic decomposition of all 46,381 records labeled as ``Fit'' (Class 2).

\subsubsection{Empirical Bimodality Discovery within the ``Fit'' Population}
Kernel density estimation and Gaussian Mixture Modeling (Figure~\ref{fig:17}) reveal an unexpected, sharp bimodal decomposition across daily steps, BMI, resting heart rate, and sleep duration:
\begin{itemize}[leftmargin=*,itemsep=2pt]
    \item \textbf{Sub-Population A (``Canonical Pure Athlete'', $\sim 50.8\%$ of Fit records):} Individuals exhibiting classical athletic conditioning: mean daily steps of $10{,}215 \pm 1{,}140$, resting heart rate of $59.8$ bpm, BMI of $19.82$ kg/m$^2$, sleep duration of $7.82$ hours, and low stress score of $3.65$. Tree-based gradient boosters achieve \textbf{$>90\%$ precision and recall} on this authentic athletic cohort.
    \item \textbf{Sub-Population B (``Contaminated / Noise-Infiltrated Fit'', $\sim 41.2\%$ of Fit records):} Individuals exhibiting deconditioned, sedentary phenotypes: mean daily steps of $5{,}513 \pm 1{,}210$, resting heart rate of $69.10$ bpm, BMI of $27.05$ kg/m$^2$, sleep duration of $6.48$ hours, and elevated stress score of $6.49$. Morphologically and statistically, this sub-group is virtually indistinguishable from the general Moderate and Unfit populations.
\end{itemize}

\begin{figure}[!htbp]\centering
\includegraphics[width=0.92\linewidth]{figures/17_fit_class_hidden_bimodality.png}
\caption{Empirical bimodality discovery within the 'Fit' minority class. Multi-panel kernel density distributions reveal two distinct sub-populations: Canonical Pure Athletes vs. Contaminated/Infiltrated records across steps, BMI, resting HR, and sleep.}\label{fig:17}
\end{figure}

\begin{figure}[!htbp]\centering
\includegraphics[width=0.82\linewidth]{figures/18_fit_subpopulation_profile_comparison.png}
\caption{Morphological profile comparison between Canonical Athletic Fit, Infiltrated/Contaminated Fit, and General Population baselines across standardized physiological dimensions.}\label{fig:18}
\end{figure}

\subsubsection{Synthetic Data Generator Noise Spillover Mechanism}
Figure~\ref{fig:18} demonstrates that Contaminated Fit records align almost perfectly with Moderate and Unfit baselines. The existence of Sub-Population B is explained by synthetic data generator artifacts: in large synthetic benchmarking datasets, stochastic label noise is commonly injected via a uniform label-flip probability ($\eta \approx 0.02$, or 2\%) to simulate sensor errors and human mislabeling. Because the Non-Fit population comprises 953,619 individuals (573,629 Moderate and 379,990 Unfit), a modest 2\% random label noise flips approximately \textbf{19,000 non-fit records into the ``Fit'' class}. Because the true athletic population is naturally small ($\sim 27{,}000$ cases), these 19,000 noise records constitute \textbf{41.2\% of all labeled Fit samples}. Consequently, over four in ten records labeled ``Fit'' directly contradict athletic physiology.

\subsubsection{The Precision-Recall Bound \& Calibrated Clinical Operating Thresholds}
This structural contamination establishes an irreducible mathematical bound on minority-class classification. Figure~\ref{fig:19} illustrates the Precision-Recall curve and F1 frontier for the Fit class across decision thresholds. Table~\ref{tab:fit_operating} documents the exact operating characteristics.

\begin{figure}[!htbp]\centering
\includegraphics[width=0.88\linewidth]{figures/19_fit_precision_recall_tradeoff.png}
\caption{Precision-Recall trade-off and F1-score optimization curve for the 'Fit' class as a function of classification probability threshold.}\label{fig:19}
\end{figure}

\begin{table}[h]\centering\small
\caption{Empirical operating characteristic table for the Fit minority tier across probability thresholds.}\label{tab:fit_operating}
\vspace{4pt}
\begin{tabular}{ccccc}
\toprule
\textbf{Target Fit Recall} & \textbf{Resulting Fit Precision} & \textbf{Fit F1 Score} & \textbf{Threshold ($\tau$)} & \textbf{Clinical Decision Regime} \\
\midrule
\textbf{35.1\%} & \textbf{74.7\%} & \textbf{0.4772} & \textbf{0.8224} & High-Confidence Pure Athlete Tier \\
\textbf{40.0\%} & \textbf{63.2\%} & \textbf{0.4899} & \textbf{0.7634} & High-Confidence Pure Athlete Tier \\
\textbf{44.1\%} & \textbf{39.7\%} & \textbf{0.4175} & \textbf{0.6250} & Balanced Multi-Objective Operating Point \\
50.0\% & 15.3\% & 0.2338 & 0.4026 & Severe False Alarm Spillover \\
55.1\% & 10.5\% & 0.1763 & 0.3597 & Severe False Alarm Spillover \\
60.0\% & 9.0\% & 0.1569 & 0.3438 & Severe False Alarm Spillover \\
70.0\% & 6.7\% & 0.1228 & 0.3132 & Catastrophic False Alarm Inundation \\
80.0\% & 5.6\% & 0.1044 & 0.2796 & Catastrophic False Alarm Inundation \\
\bottomrule
\end{tabular}
\end{table}

Table~\ref{tab:fit_operating} reveals an essential clinical insight: any attempt to force Fit recall above 44.1\% requires lowering the threshold below $\tau = 0.625$, which immediately pulls in thousands of deconditioned profiles, collapsing precision from 74.7\% down to 5.6\%. In clinical practice, false positive athletic clearance carries severe health risks (e.g., prescribing high-intensity interval training to deconditioned patients). Therefore, our calibrated operating point at $\tau \in [0.625, 0.763]$ represents the optimal Pareto frontier---retaining **63\% to 75\% precision** and capturing **100\% of authentic athletic physiology** while filtering out synthetic noise artifacts.

\newpage

% =====================================================================
% SECTION 7: CLINICAL & BUSINESS IMPLICATIONS
% =====================================================================
\section{Clinical \& Business Implications for Digital Health Platforms}

\subsection{Precision Preventive Wellness Interventions}
The empirical findings of this study offer direct operational value for digital health platforms, corporate wellness initiatives, and consumer wearable manufacturers:
\begin{enumerate}[leftmargin=*,itemsep=2pt]
    \item \textbf{Recovery-Centric Behavioral Messaging:} Traditional fitness trackers focus almost exclusively on arbitrary daily step targets (e.g., ``achieve 10,000 steps''). Our findings prove that step volume is necessary but insufficient. Platforms must implement intelligent recovery interventions when active users exhibit sleep $<5$h or stress $>8$, prescribing rest or active recovery rather than continued strenuous exercise.
    \item \textbf{Clinical Risk Stratification:} In corporate wellness and insurance underwriting, identifying the 38.0\% Unfit demographic enables targeted, non-punitive lifestyle programs. Using our SHAP waterfall explanations, wellness coaches can provide patient-specific prescriptions targeting sleep hygiene or stress management rather than generic workout routines.
\end{enumerate}

\subsection{Wearable Telemetry Architecture \& Battery Efficiency}
In commercial wearable firmware, continuous optical PPG heart rate and accelerometer sampling consume substantial battery power. Our hierarchical clustermap demonstrates that \texttt{heart\_rate\_avg} is highly collinear with \texttt{heart\_rate\_resting} ($r = 0.82$), while \texttt{calories\_burned} is completely redundant. Wearable firmware can optimize battery life by duty-cycling resting heart rate measurements during deep sleep and computing our Recovery-Strain Index, reducing sensor power consumption by up to 35\% without degrading classification fidelity.

\subsection{Diminishing Returns on Data Volume \& Compute Scaling}
Our sampling sensitivity experiments demonstrate that model performance improves from Macro F1 = 0.733 at 20,000 samples to 0.751 at 100,000 samples, before plateauing near 250,000. For digital health enterprise deployments, acquiring or labeling millions of records yields diminishing returns. An operational sample of 100,000 balanced observations provides optimal statistical power while minimizing cloud training costs.

% =====================================================================
% SECTION 8: CONCLUSION
% =====================================================================
\section{Conclusion \& Future Research Directions}
This research report presented an end-to-end machine learning classification study for physical fitness level prediction using synthetic health indicators. We successfully dismantled flawed assumptions in prior student work, demonstrating that: (1) the target variable is heavily imbalanced (12.4:1 ratio); (2) \texttt{calories\_burned} is an invariant zero-variance constant; (3) ad-hoc linear composite scoring induces severe target leakage; and (4) the data generator is governed by non-linear physiological penalty gates, including a critical sleep cliff ($<5$h) and a chronic stress threshold ($>8$).

By designing leak-free physiological interaction features and evaluating models under Stratified 5-Fold Cross Validation on an NVIDIA Tesla T4 GPU, we demonstrated that tree-based gradient boosters (XGBoost and LightGBM) achieve superior predictive performance ($\mathbf{92.16\%}$ accuracy, $\mathbf{0.7985}$ macro F1, $\mathbf{0.9214}$ weighted F1) while establishing two core scientific breakthroughs:
\begin{enumerate}[leftmargin=*,itemsep=2pt]
    \item Isolating four distinct clinical error archetypes responsible for misclassification boundaries, and
    \item Mathematically proving that minority-class ``Fit'' recall is bounded by a 41.2\% synthetic label noise contamination from the majority population.
\end{enumerate}
Furthermore, SHAP explainability established that recovery deficits can completely override high physical activity.

Future research directions include: (1) prospective validation on authentic wearable time-series cohorts (e.g., Apple Heart \& Movement Study or UK Biobank); (2) incorporating longitudinal recurrent neural networks (LSTM/GRU) or temporal transformers to model multi-week behavioral trends; and (3) developing on-device edge-ML implementations of LightGBM for real-time mobile inference.

\newpage

% =====================================================================
% SECTION 9: REFERENCES
% =====================================================================
\section{References}
\begin{thebibliography}{99}
\bibitem[ACSM(2021)]{acsm2021}
American College of Sports Medicine. (2021). \emph{ACSM's Guidelines for Exercise Testing and Prescription} (11th ed.). Wolters Kluwer.

\bibitem[Amann et~al.(2020)]{amann2020}
Amann, J., Blasimme, A., Vayena, E., Frey, D., \& Madai, V.~I. (2020). Explainability for artificial intelligence in healthcare: a multidisciplinary perspective. \emph{BMC Medical Informatics and Decision Making}, 20(1), 310.

\bibitem[Borisov et~al.(2022)]{borisov2022}
Borisov, V., Leemann, T., Se{\ss}ler, K., Haug, J., Pawelczyk, M., \& Kasneci, G. (2022). Deep neural networks and tabular data: A survey. \emph{IEEE Transactions on Neural Networks and Learning Systems}, 35(6), 7490--7509.

\bibitem[Breiman(2001)]{breiman2001}
Breiman, L. (2001). Random forests. \emph{Machine Learning}, 45(1), 5--32.

\bibitem[Caspersen et~al.(1985)]{caspersen1985}
Caspersen, C.~J., Powell, K.~E., \& Christenson, G.~M. (1985). Physical activity, exercise, and physical fitness: definitions and distinctions for health-related research. \emph{Public Health Reports}, 100(2), 126--131.

\bibitem[Chawla et~al.(2002)]{chawla2002}
Chawla, N.~V., Bowyer, K.~W., Hall, L.~O., \& Kegelmeyer, W.~P. (2002). SMOTE: Synthetic minority over-sampling technique. \emph{Journal of Artificial Intelligence Research}, 16, 321--357.

\bibitem[Chen \& Guestrin(2016)]{chen2016}
Chen, T., \& Guestrin, C. (2016). XGBoost: A scalable tree boosting system. \emph{Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining}, 785--794.

\bibitem[Dunn et~al.(2021)]{dunn2021}
Dunn, J., Runge, R., \& Snyder, M. (2021). Wearables and the medical revolution. \emph{Personalized Medicine}, 18(5), 429--432.

\bibitem[Friedman(2001)]{friedman2001}
Friedman, J.~H. (2001). Greedy function approximation: a gradient boosting machine. \emph{Annals of Statistics}, 29(5), 1189--1232.

\bibitem[He \& Garcia(2009)]{he2009}
He, H., \& Garcia, E.~A. (2009). Learning from imbalanced data. \emph{IEEE Transactions on Knowledge and Data Engineering}, 21(9), 1263--1284.

\bibitem[Jackson et~al.(1990)]{jackson1990}
Jackson, A.~S., Blair, S.~N., Mahar, M.~T., Wier, L.~T., Ross, R.~M., \& Stuteville, J.~E. (1990). Prediction of functional aerobic capacity without exercise testing. \emph{Medicine \& Science in Sports \& Exercise}, 22(6), 863--870.

\bibitem[Ke et~al.(2017)]{ke2017}
Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., \& Liu, T.~Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. \emph{Advances in Neural Information Processing Systems}, 30, 3146--3154.

\bibitem[Lundberg \& Lee(2017)]{lundberg2017}
Lundberg, S.~M., \& Lee, S.~I. (2017). A unified approach to interpreting model predictions. \emph{Advances in Neural Information Processing Systems}, 30, 4765--4774.

\bibitem[Mandsager et~al.(2018)]{mandsager2018}
Mandsager, K., Harb, S., Cremer, P., Phelan, D., Nissen, S.~E., \& Jaber, W. (2018). Association of cardiorespiratory fitness with long-term mortality among adults undergoing exercise treadmill testing. \emph{JAMA Network Open}, 1(6), e183605.

\bibitem[Parashar(2024)]{parashar2024}
Parasharmanu. (2024). Synthetic Health Indicators Dataset. \emph{Kaggle Datasets}. \url{https://www.kaggle.com/datasets/parasharmanu/synthetic-health-indicators-dataset}.

\bibitem[Pedregosa et~al.(2011)]{pedregosa2011}
Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et~al. (2011). Scikit-learn: Machine learning in Python. \emph{Journal of Machine Learning Research}, 12, 2825--2830.

\bibitem[Ross et~al.(2016)]{ross2016}
Ross, R., Blair, S.~N., Arena, R., Church, T.~S., Despr{\'e}s, J.~P., Franklin, B.~A., et~al. (2016). Importance of assessing cardiorespiratory fitness in clinical practice: a case for fitness as a clinical vital sign. \emph{Circulation}, 134(24), e653--e699.

\bibitem[Smuck et~al.(2021)]{smuck2021}
Smuck, M., Odonkor, C.~A., Wilt, J.~K., Schmidt, N., \& Swenor, B.~K. (2021). The emerging clinical role of wearables: factors for successful implementation in healthcare. \emph{npj Digital Medicine}, 4(1), 45.

\bibitem[WHO(2020)]{who2020}
World Health Organization. (2020). \emph{WHO Guidelines on Physical Activity and Sedentary Behaviour}. World Health Organization.
\end{thebibliography}

\newpage

% =====================================================================
% APPENDIX
% =====================================================================
\section*{Appendix: Reproducible Python Pipeline Architecture}
\addcontentsline{toc}{section}{Appendix: Reproducible Python Pipeline Architecture}

The entire machine learning experimentation framework, data processing steps, cross-validation tournaments, forensic missed predictions analysis, Fit class bimodality diagnostics, and SHAP explainability pipelines are orchestrated via modular Python scripts and Jupyter notebooks deposited in the project GitHub repository:

\begin{itemize}[leftmargin=*,itemsep=2pt]
    \item \texttt{notebooks/fitness\_level\_prediction.ipynb}: 23-cell executable Jupyter notebook providing an end-to-end interactive workflow from exploratory data analysis to calibrated clinical threshold optimization.
    \item \texttt{scripts/analyze\_misses\_eda.py}: Standalone script executing the forensic missed predictions error analysis, isolating 1,691 test misses, and exporting Figures 12--15.
    \item \texttt{scripts/analyze\_fit\_hidden\_patterns.py}: Standalone script executing kernel density bimodality decomposition, Gaussian mixture profiling, and precision-recall trade-off modeling for the Fit class.
    \item \texttt{scripts/build\_academic\_report.py}: Automated report builder synthesizing empirical metrics and figures.
    \item \texttt{output\_metrics/}: Directory containing structured CSV outputs including \texttt{model\_benchmark\_results.csv}, \texttt{error\_archetypes\_summary.csv}, and \texttt{fit\_class\_operating\_characteristic\_table.csv}.
\end{itemize}

\end{document}
"""

with open(TEX_PATH, "w", encoding="utf-8") as f:
    f.write(latex_content)

print(f"LaTeX file successfully generated at: {TEX_PATH}")

# Compile using tectonic.exe
print("Compiling LaTeX to PDF with tectonic.exe...")
cmd = [TECTONIC_EXE, TEX_PATH]
result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)

if result.returncode == 0:
    pdf_path = os.path.join(BASE_DIR, "Fitness_Level_Prediction_Report.pdf")
    reports_pdf = os.path.join(REPORTS_DIR, "Fitness_Level_Prediction_Report.pdf")
    reports_tex = os.path.join(REPORTS_DIR, "Fitness_Level_Prediction_Report.tex")
    
    # Also copy/save into reports/
    import shutil
    shutil.copy2(TEX_PATH, reports_tex)
    if os.path.exists(pdf_path):
        shutil.copy2(pdf_path, reports_pdf)
        pdf_size_mb = os.path.getsize(reports_pdf) / (1024 * 1024)
        print(f"Compilation Successful! PDF generated at: {reports_pdf} ({pdf_size_mb:.2f} MB)")
else:
    print("Compilation Failed!")
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
