# Cross-Border Anti-Money Laundering (AML) Detection Engine

An end-to-end Machine Learning pipeline and graph visualization suite designed to identify suspicious cross-border financial activity on the IBM AML Synthetic Dataset.

---

## 5-Stage Relay Architecture

This project was built using a structured 5-stage relay methodology:

1. **Stage 1 — Domain, EDA & Framing**: Defined laundering patterns (Fan-Out, Fan-In, Cycles) and established an out-of-time temporal split to prevent data leakage.
2. **Stage 2 — Feature Engineering**: Extracted account-level transaction counts, in/out ratios, cross-border/currency flags, and rolling burstiness features.
3. **Stage 3 — Model Building**: Built and hyperparameter-tuned a class-weighted XGBoost baseline targeting maximum AUPRC under high class imbalance.
4. **Stage 4 — Evaluation & Explainability**: Conducted cost trade-off analysis (missed laundering vs. alert fatigue) and computed SHAP feature importance metrics.
5. **Stage 5 — Executive Report & Visualization**: Integrated all relay hand-offs into an executive report, created network topology graph visualizations, and finalized repository documentation.

---

## Workspace Structure

aml-cross-border-project/
├── README.md
└── stage_5_report/
├── final_report.ipynb
├── final_report.html
├── generate_network_viz.py
└── visualizations/
├── pattern_topology_1.png
└── pattern_topology_2.png


---

## Execution Instructions

### Environment Setup
```bash
# Activate workspace environment
source ~/Documents/2_AI_ML_Engineering/Vir_Env/bin/activate

# Install required packages
pip install matplotlib networkx jupyter

Generate Visualizations & Render Report
Bash

# Run topology generator script
python3 stage_5_report/generate_network_viz.py

# Export executive report to HTML
python3 -m jupyter nbconvert --to html stage_5_report/final_report.ipynb

EOF


---

#### 2. Git Staging, Commit & Push Workflow

Execute the following commands in your terminal to commit your work and push your branch to GitHub:

```bash
# 1. Stage all created files
git add README.md stage_5_report/

# 2. Check staging status
git status

# 3. Commit changes with a structured message
git commit -m "feat(stage_5): complete executive report, network visualizations, and README documentation"

# 4. Push branch to GitHub
git push -u origin feature/person-5-report-and-polish
