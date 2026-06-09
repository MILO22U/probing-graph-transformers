from pathlib import Path
import json

RESULTS_DIR = Path("results")

dataset_map = {
    "edge": "Edges",
    "triangle": "Triangles",
    "csl": "CSL",
    "actor": "Actor",
    "webkb-cor": "Cornell",
    "webkb-tex": "Texas",
    "webkb-wis": "Wisconsin",
    "wn-chameleon": "Chameleon",
    "wn-squirrel": "Squirrel",
}

model_map = {
    "gin": "GIN",
    "graphormer": "Graphormer",
    "gps": "GPS",
    "tf": "Transformer",
}

def get_dataset_model(path: Path):
    text = str(path).replace("\\", "/").lower()

    dataset = None
    model = None

    for key, name in dataset_map.items():
        if key in text:
            dataset = name
            break

    for key, name in model_map.items():
        if key in text:
            model = name
            break

    return dataset, model

def find_accuracy(data):
    possible_keys = [
        "accuracy",
        "test_accuracy",
        "test_acc",
        "test/accuracy",
        "test/acc",
    ]

    for key in possible_keys:
        if key in data and isinstance(data[key], (int, float)):
            return data[key]

    if "test" in data and isinstance(data["test"], dict):
        for key in ["accuracy", "acc"]:
            if key in data["test"] and isinstance(data["test"][key], (int, float)):
                return data["test"][key]

    return None

rows = []

# IMPORTANT: only use agg/test/best.json
for file in RESULTS_DIR.rglob("agg/test/best.json"):
    dataset, model = get_dataset_model(file)

    if dataset is None or model is None:
        continue

    try:
        with open(file, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Could not read {file}: {e}")
        continue

    acc = find_accuracy(data)

    if acc is None:
        print(f"No accuracy found in {file}")
        continue

    if acc <= 1:
        acc *= 100

    rows.append({
        "dataset": dataset,
        "model": model,
        "accuracy": acc,
        "file": str(file),
    })

rows = sorted(rows, key=lambda x: (x["dataset"], x["model"]))

print("\nCorrect TEST accuracies from agg/test/best.json:\n")
for r in rows:
    print(f"{r['dataset']:12s} | {r['model']:12s} | {r['accuracy']:.2f}% | {r['file']}")

print("\nLaTeX rows:\n")
for r in rows:
    print(f"{r['dataset']} & {r['model']} & {r['accuracy']:.2f} \\\\")