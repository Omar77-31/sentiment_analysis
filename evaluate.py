import os
import django
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from analyzer.services import analyze_text


def main():

    data_path = os.path.join(os.path.dirname(__file__), 'sample_data.csv')
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        return

    df = pd.read_csv(data_path)
    y_true = []
    y_pred = []
    latencies = []

    print(f"Evaluating on {len(df)} samples...")

    for index, row in df.iterrows():
        text = row['text']
        true_label = row['label']

        try:
            result = analyze_text(text)
            pred_label = result['sentiment']
            latency = result['latency_ms']

            y_true.append(true_label)
            y_pred.append(pred_label)
            latencies.append(latency)
            print(f"[{index + 1}/{len(df)}] Text: {text[:30]}... | True: {true_label} | Pred: {pred_label}")
        except Exception as e:
            print(f"Error analyzing text: {text} -> {e}")


    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average='macro')
    cm = confusion_matrix(y_true, y_pred, labels=["positive", "negative", "neutral"])

    avg_latency = np.mean(latencies)
    p95_latency = np.percentile(latencies, 95)

    print("\n" + "=" * 40)
    print("📊 EVALUATION RESULTS")
    print("=" * 40)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Macro F1:  {macro_f1:.4f}")
    print(f"Avg Latency: {avg_latency:.2f} ms")
    print(f"95th Percentile Latency: {p95_latency:.2f} ms")
    print("\nConfusion Matrix (Rows=True, Cols=Pred):")
    print("Order: [Positive, Negative, Neutral]")
    print(cm)


if __name__ == "__main__":
    main()