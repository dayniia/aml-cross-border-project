# Stage 2: Feature Engineering Handoff

### Overview
This pipeline processes the raw IBM AML transactions into a structured feature table ready for XGBoost modeling. 

### Feature Dictionary
* **`is_cross_border`**: Binary flag (1/0) indicating if the sender and receiver banks are different.
* **`is_cross_currency`**: Binary flag (1/0) indicating if the receiving currency differs from the payment currency.
* **`tx_count_out`**: The total number of transactions initiated by the sending account.
* **`unique_counterparties_out`**: The number of distinct recipient accounts the sender interacted with (Fan-out indicator).
* **`tx_24h_burst`**: The count of transactions made by the sending account within a rolling 24-hour window.
* **`is_round_amount`**: Binary flag (1/0) capturing clean, round amounts (multiples of 1,000) often used in laundering.
* **`in_out_ratio`**: The ratio of total funds received versus total funds sent to detect pass-through accounts.

**Output:** The script exports `features_stage2.parquet` to the `data/` directory.