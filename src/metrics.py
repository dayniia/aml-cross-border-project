from sklearn.metrics import average_precision_score, precision_recall_curve, f1_score


def evaluate(y_true, y_prob, threshold=0.5):
    """Headline metrics for imbalanced AML classification.

    Accuracy is deliberately excluded from this project's evaluation. With an
    illicit rate of roughly 0.1%, a model that always predicts "not laundering"
    would score above 99.9% accuracy while catching zero real cases — so
    accuracy would be actively misleading here.

    Returns:
        dict with:
          - auprc: area under the precision-recall curve
          - minority_f1: F1 score on the illicit (minority) class
          - pr_curve: (precision, recall, thresholds) arrays for plotting
    """
    auprc = average_precision_score(y_true, y_prob)
    y_pred = (y_prob >= threshold).astype(int)
    minority_f1 = f1_score(y_true, y_pred, pos_label=1)
    precision, recall, thresholds = precision_recall_curve(y_true, y_prob)
    return {
        "auprc": auprc,
        "minority_f1": minority_f1,
        "pr_curve": (precision, recall, thresholds),
    }
