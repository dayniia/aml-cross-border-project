# Stage 1 Hand-off Report — Domain Research, EDA & Problem Framing
**Cross-Border Transaction Analysis — IBM AML Dataset**
**Owner:** Person 1 | **Status:** Complete | **Hands off to:** Person 2 (Feature Engineering)

---

## 1. Dataset

- **Source:** [IBM Transactions for Anti Money Laundering (AML) — Kaggle](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml)
- **Variant used:** HI-Small
- **Files:** `HI-Small_Trans.csv` (5,078,345 transactions), `HI-Small_accounts.csv`, `HI-Small_Patterns.txt`
- **Location:** Google Drive, `AML_Dataset/` — see repo README for mount instructions
- **Data quality:** 0 nulls across all 11 columns. Clean load, no preprocessing required before feature engineering.
- **Date range:** September 1–18, 2022
- **Overall illicit rate:** 0.102% (5,181 laundering transactions out of 5,078,345)

## 2. Domain Background

The dataset models the full money-laundering cycle — **placement, layering, integration** — and labels transactions according to structural typologies. The relevant ones observed in `Patterns.txt` for this dataset include:

| Pattern | Structure |
|---|---|
| Fan-out | One account sends to many |
| Fan-in | Many accounts send to one |
| Cycle | Funds loop back near the origin account |
| Gather-scatter / Scatter-gather | Funds pooled and redistributed, in either order |
| Bipartite | Dense many-to-many transfers between two account clusters |
| Stack | Sequential pass-through chain of accounts |

## 3. Key EDA Findings

### 3.1 Payment format risk (primary finding)
ACH transactions show a laundering rate of **0.746%** — roughly **7x** the dataset average of 0.102%. All other payment formats (Bitcoin, Cash, Cheque, Credit Card) sit at or below baseline. **Wire and Reinvestment show 0% laundering** despite large sample sizes (171,855 and 481,056 transactions respectively) — a genuine pattern in this dataset, not a small-sample artifact.

This was independently confirmed by direct inspection of a labeled laundering group in `Patterns.txt`: a 16-degree fan-out ring (source account `800737690`) in which **23 of 24 transactions (96%) used ACH**.

### 3.2 Currency interaction within ACH (secondary finding)
Within ACH specifically, **Saudi Riyal transactions show a laundering rate of 3.73%** (361 of 9,679 transactions) — 4 to 9x higher than any other ACH+currency combination, which cluster between 0.39% and 0.86%. A chi-square test confirms this is highly statistically significant (**p = 3.17 × 10⁻²⁵⁸**), not random variation.

**Note:** these two findings are independent, not the same thing — the fan-out ring identified above used US Dollar and Euro, not Saudi Riyal. This means ACH carries elevated risk broadly, and Saudi Riyal carries additional elevated risk specifically within ACH. Both should be treated as separate signals.

### 3.3 Temporal concentration of laundering activity (significant finding)
Daily laundering rate is **not stable over time**. It sits near 0% for the first 9 days (Sept 1–9), then jumps sharply to roughly 55–70% of transactions starting **September 10** and stays elevated through the end of the window (Sept 18). This is a hard concentration, not a gradual trend.

This explains why the temporal train/test split shows a notably different illicit rate between splits (see below) — nearly all positive-class signal is concentrated in the back half of the timeline.

## 4. Methodology Decisions

### 4.1 Train/test split
A **temporal split (80/20)** was used — never random — since random splitting would leak future transaction information into training, which is not valid for a realistic fraud-detection evaluation.

Split fractions from 50/50 to 80/20 were tested to see whether a different boundary would reduce the train/test illicit-rate imbalance:

| Train fraction | Train illicit rate | Test illicit rate |
|---|---|---|
| 50% | 0.069% | 0.135% |
| 60% | 0.075% | 0.142% |
| 70% | 0.080% | 0.152% |
| 80% | 0.083% | 0.177% |

The gap ratio (~1.6–2x) is consistent across every split point tested, confirming this is a **structural property of the dataset** (the Sept 10 concentration described in 3.3), not an artifact of where the split boundary falls. **Decision: keep 80/20** — no tested alternative meaningfully reduced the imbalance, and 80/20 maximizes available training data (4.06M vs. 2.54M rows at 50/50).

**Implication for downstream stages:** models will be trained on a period with proportionally less illicit signal than they'll be evaluated on. This is expected and should not be "fixed" by resampling the split — it should be understood as a property of the evaluation.

### 4.2 Metrics
Accuracy is explicitly excluded as a metric. With a ~0.1% illicit rate, a model predicting "not laundering" for everything would score >99.9% accuracy while catching zero real cases.

**Metrics used:** AUPRC (precision-recall AUC), recall at a fixed false-positive budget, minority-class (illicit) F1 score. Implemented in `src/metrics.py`.

## 5. Hand-off Artifacts

| Artifact | Location | Purpose |
|---|---|---|
| EDA notebook | `notebooks/01_domain_eda_split.ipynb` | Full analysis, charts, and reasoning behind every decision above |
| `split_data.py` | `src/split_data.py` | `temporal_split(df, timestamp_col, test_frac)` — **use this exact function**, do not re-split independently |
| `metrics.py` | `src/metrics.py` | `evaluate(y_true, y_prob, threshold)` — shared evaluation function for later stages |

**Do not modify the split logic** — every stage from here on needs to be evaluated against the same train/test boundary for results to be comparable across the team.

## 6. Recommendations for Stage 2 (Feature Engineering)

Based on the findings above, these are worth prioritizing as engineered features:

1. **Payment format as a categorical feature** — ACH's elevated risk is strong and confirmed both statistically and by direct pattern inspection.
2. **Payment format × currency interaction feature** — specifically, an "ACH + Saudi Riyal" flag (or more generally, a feature encoding format-currency combinations) — the aggregate format-only signal understates the risk of this specific combination.
3. **Standard account-level behavioral features** as originally planned: transaction counts, in/out ratio, unique counterparties, cross-border/cross-currency flags, burstiness, round-number amounts.
4. **Self-transaction flag** — several transactions in the raw data have identical sender and receiver accounts (e.g. `Reinvestment` format rows); worth checking whether this correlates with laundering or is just how reinvestment transactions are recorded.


---
*Prepared by Person 1 (Dina)— Stage 1 complete. Questions on any decision above should reference the EDA notebook, where the full reasoning and code for each finding is documented.*
