# Stage 3: Baseline LightGBM Model & Artifact Export

## Overview
- Trained baseline LightGBM model on leakage-free engineered features.
- Evaluated performance using PR-AUC, ROC-AUC, Precision, Recall, and F1-Score.

## Key Metrics
- **PR-AUC:** [Insert Value, e.g., 0.82]
- **ROC-AUC:** [Insert Value, e.g., 0.94]
- **F1-Score:** [Insert Value]

## Exported Artifacts (Google Drive)
- `aml_lgbm_baseline.joblib` — Trained model pipeline
- `feature_schema.json` — Final feature names and data types
- `category_mappings.json` — Categorical encodings

## Hand-off Instructions for Person 4
- Load model artifacts from Google Drive to run hyperparameter tuning and model comparison.
- Use `notebooks/03_baseline_model.ipynb` as the evaluation entry point.
